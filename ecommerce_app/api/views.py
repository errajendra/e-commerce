from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import *
from .exceptions import *
from constance import config


# Auther: Rajendra
"""
    Category Listing Viewsets
"""
class CategoryView(ModelViewSet):
    http_method_names = ('get',)
    serializer_class = CategoryListSerializer
    pagination_class = None
    
    def get_queryset(self):
        product_in_cat = Product.objects.filter(
            status=True).values_list("sub_category__category_title__category", flat=True)
        cat_ids = tuple(set(product_in_cat))
        queryset = Category.objects.select_related().filter(
            id__in = cat_ids).distinct().order_by('level')
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)
    


"""
    Sub Category Listing Viewsets 
    used on the Natual Product Listing Banner
"""
class SubCategoryBannerView(ModelViewSet):
    http_method_names = ('get',)
    serializer_class = SubCategoryNaturalProductListSerializer
    
    def get_queryset(self):
        return SubCategory.objects.exclude(image='')
    
    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


"""
    Banner Listing Viewsets
"""
class BannerView(ModelViewSet):
    http_method_names = ('get',)
    serializer_class = BannerSerializer
    pagination_class = None
    
    def get_queryset(self):
        qs = Banner.objects.all()
        page = self.request.GET.get('on_page', None)
        if page:
            qs = qs.filter(page=page)
        
        use_for = self.request.GET.get('use_for', None)
        if use_for:
            qs = qs.filter(use_for=use_for)
        
        return qs
    


"""
    Product Listing and Detail Viewset
"""
class ProductView(ModelViewSet):
    http_method_names = ('get',)
    serializer_class = ProductListSerializer
    
    def get_queryset(self):
        qs = Product.objects.select_related().filter(status=True)
        
        # Filter by Featured
        if self.request.query_params.get('is_featured'):
            qs = qs.filter(is_featured=True)
        
        # Filter by New Arrivals
        if self.request.query_params.get('is_new_arrival'):
            qs = qs.filter(is_new_arrival=True)
        
        # Filter by Category
        if self.request.query_params.get('category'):
            qs = qs.filter(sub_category__category_title__category__id=self.request.query_params.get('category'))
            
        # Filter by Sub Category
        if self.request.query_params.get('sub_category'):
            qs = qs.filter(sub_category__id=self.request.query_params.get('sub_category'))
            
        # Search by Name, Tag  or Description
        if self.request.query_params.get('search'):
            qs = qs.filter(
                Q(name__icontains = self.request.query_params.get('search')) |
                Q(sub_name__icontains = self.request.query_params.get('search')) |
                Q(description__icontains = self.request.query_params.get('search')) |
                Q(category__name__icontains = self.request.query_params.get('search'))
            )
        
        # Sorting by Price
        sort_by = self.request.query_params.get('sort')
        if sort_by:
            return qs.order_by(sort_by)
        return qs
    
    
    """
        Override Product Detail View to include related data
        Serializer is used here instead of all Detail
        because we need full control over fields in the response
    """
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ProductDetailSerializer
        return super().retrieve(request, *args, **kwargs)



""" 
    Cart Item View Set.
"""
class CartView(ModelViewSet):
    http_method_names = ('get', 'post', 'delete', 'put')
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return Cart.objects.select_related().filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        data = super().list(request, *args, **kwargs)
        context = {
            "total_price": sum([item['product']['price']*item['quantity'] for item in data.data]),
            "list": data.data
        }
        return Response(context)



"""
Product Reviews Viewset
"""
class ProductReviewView(ModelViewSet):
    http_method_names = ('post',)
    serializer_class = ProductReviewSerializer
    
    def get_queryset(self):
        return ProductReview.objects.select_related().all()
    
    def create(self, request, *args, **kwargs):
        self.permission_classes = (IsAuthenticated,)
        data = super().create(request, *args, **kwargs)
        return Response(data.data)



"""
Order Items of Cart Viewset
"""
class OrderCartProduct(ModelViewSet):
    http_method_names = ('post',)
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        address_serializer = TakeUserAddressZipOrderSerializer(data=request.data)
        
        if address_serializer.is_valid(raise_exception=True):
            print( address_serializer.validated_data)
            delivery_address = address_serializer.validated_data['delivery_address']
            delivery_zip_code = address_serializer.validated_data['delivery_zip_code']
            
        user = request.user
        cart_items = user.cart.select_related().all()
        
        if not cart_items:
            raise CartIsEmpaty()
        
        total_price = 0
        
        for cart in cart_items:
            price = cart.quantity * cart.product.price
            total_price += price
        
        order = Order.objects.create(
            user = user,
            total_price = total_price,
            delivery_address = delivery_address,
            delivery_zip_code = delivery_zip_code
        )
        order.save()
        order_products_qs = []
        for cart in cart_items:
            order_products_qs.append(
                OrderProduct(
                    order = order,
                    product = cart.product,
                    quantity = cart.quantity,
                    price = cart.quantity * cart.product.price
                )
            )
        
        try:
            OrderProduct.objects.bulk_create(order_products_qs)
        except Exception as e:
            return Response(
                data={
                    "message": f"{str(e)}"
                },
                status=status.HTTP_400_BAD_REQUEST)
        
        cart_items.delete()
        
        return Response(
            status=status.HTTP_201_CREATED,
            data = {
                "order": OrderSerializer(order).data,
                "qr_pay": "#"
                
            }
        )



"""
Order List Viewset
"""
class OrderListView(ModelViewSet):
    http_method_names = ('get',)
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        return self.request.user.orders.all()



"""
Order Payment Screenshot upload Viewset
"""
class OrderPaymentScreenShotUploadView(ModelViewSet):
    http_method_names = ('put',)
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderPaymentScreenShotUploadSerializer
    
    def get_queryset(self):
        return self.request.user.orders.all()



"""
Order Cancel Viewset
"""
class OrderCancelView(ModelViewSet):
    http_method_names = ('put',)
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        return self.request.user.orders.all().exclude(
            status__in = ["DELIVERED", "FAILED", "CENCELED"]
        )
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        cancelation_reason = request.data.get("cancelation_reason", None)
        instance.status = "CANCELED"
        instance.cancelation_reason = cancelation_reason
        instance.save()
        return Response(
            self.serializer_class(instance).data
        )



"""
Re Order Viewset
"""
class ReOrderlView(ModelViewSet):
    http_method_names = ('post',)
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    
    def create(self, request, *args, **kwargs):
        order_id = request.POST.get("order_id", None)
        old_instance = get_object_or_404(Order, id=order_id)
        old_order_products = old_instance.order_products.all()
        products = Product.objects.filter(
            id__in = old_order_products.values_list('product', flat=True)
        )
        
        # Create a new Order Instance and set the user to be the same as the original one
        
        total_price = products.aggregate(total=Sum('price'))['total'] or 0
        instance = Order(
            user = old_instance.user,
            total_price = total_price,
            delivery_address = old_instance.delivery_address,
            delivery_zip_code = old_instance.delivery_zip_code,
        )
        instance.save()
        
        # create order product detail
        order_product_qs = []
        for op in old_order_products:
            order_product_qs.append(
                OrderProduct(
                    order = instance,
                    product = op.product,
                    quantity = op.quantity,
                    price = op.product.price
                )
            )
        OrderProduct.objects.bulk_create(order_product_qs, ignore_conflicts=True)
        return Response(
            self.serializer_class(instance).data
        )



"""
User Transaction List Viewset
"""
class TransactionListView(ModelViewSet):
    http_method_names = ('get',)
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        return self.request.user.transactions.all()



""" User Address View. """
class UserAddressView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserAddressSerializer
    
    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)




""" BLogs View. """
class BlogView(ModelViewSet):
    serializer_class = BlogListingSerializer
    
    def get_queryset(self):
        return Blog.objects.filter(published=True)
    
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = BlogDetailSerializer
        return super().retrieve(request, *args, **kwargs)



""" Reviews List Views"""
class ReviewListView(ModelViewSet):
    http_method_names = ("get",)
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(status=True)



""" Reviews Views"""
class ReviewView(ModelViewSet):
    http_method_names = ("post", "put", "delete")
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(status=True)
        
    def destroy(self, request, *args, **kwargs):
        self.queryset = Review.objects.filter(user=request.user)
        return super().destroy(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        self.queryset = Review.objects.filter(user=request.user)
        return super().update(request, *args, **kwargs)



@api_view(["POST"])
def get_service_area_by_zipcode(request, format=None):
    zip_code = request.data.get("zip_code").strip()
    service_area = [i.strip() for i in config.SERVICEABLE_AREA_ZIPCODE.strip().split(',')]
    allowed = False
    
    if zip_code in service_area:
        allowed = True
        message = "OK"
    
    else:
        allowed = False
        message = "This location is out of our service area."
    
    return Response({
        "status": 200,
        "allowed": allowed,
        "message": message,
    })



class ConactUsView(ModelViewSet):
    http_method_names = ("post", )
    serializer_class = ContactUsSerializer
    queryset = ContactUs.objects.all()
    