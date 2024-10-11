from rest_framework import serializers
from django.db.models import Avg
from ..models import (
    Category, Product, ProductFAQ, ProductReview, Banner,
    Cart, Order, OrderProduct, Transaction,
    UserAddress,
    Blog, Review, SubCategory,ContactUs
)
from user.api.serializers import UserInfoSerializer


# Rajendra
"""
    Category Listing Serializer
"""
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image')
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["rating"] = round(ProductReview.objects.filter(
            product__category=instance
            ).aggregate(Avg('rating'))['rating__avg'] or 0)
        data["sold_items"] = OrderProduct.objects.filter(
            product__category=instance
            ).aggregate(Avg('quantity'))['quantity__avg'] or 0
        products = instance.products.select_related().all().order_by('price')
        if products.exists():
            data["price_in_range"] = f"{round(products.first().price)} - {round(products.last().price)}"
        else:
            data["price_in_range"] = "Not Available"
        return data



class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'icon')



"""
Used on Natural Product List Banner serializer using Sub Category model
"""
class SubCategoryNaturalProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'image')



class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["sub_categories"] = SubCategory(instance.subcategories.all(), many=True).data
        return data




"""
    Product FAQs Listing Serializer 
    used in Product Details Serialiser (api)
"""
class ProductFAQsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFAQ
        fields = ('id', 'question', 'answer')



"""
    The ProductReviewSerializer class is a subclass of serializers.ModelSerializer.
    It is used to serialize and deserialize instances of the ProductReview model.
    Take review from user.
"""
class ProductReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(status=True))

    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'product', 'rating', 'review', 'created_at']



"""
    Product Reviews Average Rating Serializer
    Used to get the average rating of a product review.
    It is called by the ProductDetailsViewSet when getting details for a product.
"""
class ProductReviewListSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    class Meta:
        model = ProductReview
        fields = ('id', 'user', 'rating', 'review', 'updated_at')



"""
    Product Listing Serializer
"""
class ProductListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(read_only=True)
    class Meta:
        model = Product
        fields = (
            'id', 'category', 'name', 'sub_name',
            'price', 'discount_price', 'is_featured', 'is_new_arrival', 'image1'
        )
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # data['list_price'] = instance.list_price
        data['rating'] = instance.rating    # Returning Avg Rating of Product
        return data



"""
    Product Detail Serializer,
    includes  all information from ProductListSerializer plus more detailed info.
    Called by ProductDetailsViewSet in views.py
"""
class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(read_only=True)

    class Meta:
        model = Product
        exclude = (
            'discount_price', 'created_at', 'updated_at', 'status'
        )
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        data['list_price'] = instance.list_price
        data['rating'] = instance.rating
        data['faqs'] = ProductFAQsListSerializer(instance.faqs.all(), many=True).data
        
        # Reviews Details
        reviews = instance.reviews.all()
        if reviews:
            ratings_couces = reversed(list(ProductReview.PRODUCT_RATING_CHOICES))
            rating_detail = []
            for rate in ratings_couces:
                review_rates = reviews.filter(rating=rate[0])
                rating_avg = review_rates.aggregate(Avg('rating'))['rating__avg']
                if not rating_avg:
                    rating_detail.append({
                        "value": rate[1],
                        "vote_percentage": 0
                    })
                else:
                    rating_detail.append({
                        "value": rate[1],
                        "vote_percentage": f"{round(review_rates.count() * 100 / reviews.count(), 2)} %"
                    })
        else:
            rating_detail = []
                
        data['reviews'] = {
            "count": reviews.count(),
            "ratings": rating_detail,
            "list": ProductReviewListSerializer(
                reviews.exclude(review=""), many=True).data
        } 
        
        # Related Products
        data['related_products'] = ProductListSerializer(
            Product.objects.filter(
                category=instance.category,
            ).exclude(id=instance.id).order_by('is_featured')[:4],
            many=True
        ).data
        return data



"""
    A serializer for the Cart model.
"""
class CartSerializer(serializers.ModelSerializer):
   
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(
            status = True,
            availability = "IN STOCK",
        ))
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'quantity']

    def create(self, validated_data):
        """
        Create and return a new Cart instance, given the validated data.
        """
        user = validated_data['user']
        product = validated_data['product']
        quantity = validated_data['quantity']

        try:
            existing_cart_item = Cart.objects.get(user=user, product=product)
            existing_cart_item.quantity += quantity
            existing_cart_item.save()
            return existing_cart_item
        except Cart.DoesNotExist:
            return Cart.objects.create(**validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['product'] = ProductListSerializer(
            instance=instance.product,
            context={'request':self.context['request']}).data
        return data



class OrderItemsSerialiser(serializers.ModelSerializer):
    """ Serializer for order items in an order"""
    product = ProductListSerializer(read_only=True)
    class Meta:
        model = OrderProduct
        fields = "__all__"



""" Order from Cart Serializer. """
class TakeUserAddressZipOrderSerializer(serializers.Serializer):
    delivery_address = serializers.CharField(max_length=250)
    delivery_zip_code = serializers.CharField(max_length=10)



class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'total_price', 'status',
            'delivery_address', 'delivery_zip_code',
            'created_at', 'updated_at'
        ]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['products'] = OrderItemsSerialiser(
            instance.order_products.all(),
            many = True
        ).data
        if instance.status == "CANCELED":
            data["cancelation_reason"] = instance.cancelation_reason
        return data




class OrderPaymentScreenShotUploadSerializer(serializers.ModelSerializer):
    payment_screentshot = serializers.ImageField()
    class Meta:
        model = Order
        fields = [
            'id', 'payment_screentshot',
        ]
        


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'id', 'user', 'order', 'amount', 'status',
            'created_at', 'updated_at')



class UserAddressSerializer(serializers.ModelSerializer):
    """
    A serializer for the UserAddress model.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = UserAddress
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['full_address'] = instance.full_address
        return data



class BannerSerializer(serializers.ModelSerializer):
    """
    A serializer for the Banner model.
    """
    class Meta:
        model = Banner
        fields = ("title", "use_for", "image", "page")



class BlogListingSerializer(serializers.ModelSerializer):
    """
    Blog Listing Serializer
    """
    class Meta:
        model = Blog
        fields = ('id', 'title', 'content', 'image', 'updated_at')
        


class BlogDetailSerializer(serializers.ModelSerializer):
    """
    Blog LisDetailting Serializer
    """
    class Meta:
        model = Blog
        fields = ('id', 'title', 'content', 'image', 'updated_at')



class ReviewSerializer(serializers.ModelSerializer):
    """
    Review Serializer
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Review
        fields = ('id', 'user', 'rating', 'review', 'updated_at')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = UserInfoSerializer(instance.user).data
        return data



class ContactUsSerializer(serializers.ModelSerializer):
    """
    Contact US Serializer
    """
    class Meta:
        model = ContactUs
        fields = "__all__"
