import uuid, random, string
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from user.utils import phone_validator
from user.models import BaseModel, CustomUser as User, _



def file_size_10mb(value): # this is file size vaidator for 10 mb
    limit = 10 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 10 MiB.')


class Banner(models.Model):
    PAGE_CHOICES = (
        ("HOME", "HOME"),
        ("PRODUCT LISTING", "PRODUCT LISTING"),
    )
    USE_FOR_CHOICES = (
        ("MOBILE", "MOBILE"),
        ("DESKTOP", "DESKTOP"),
    )
    page = models.CharField(
        _("Show on Page"), max_length=20,
        choices=PAGE_CHOICES, default="HOME PAGE")
    use_for = models.CharField(
        _("Use For"), max_length=20,
        choices=USE_FOR_CHOICES, default="MOBILE")
    image = models.ImageField(help_text="Upload image on size 720*300")
    title = models.CharField(max_length=50)



class UserAddress(BaseModel):
    """
    A model representing a user's address.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    name = models.CharField('House Number', max_length=50, null=True, blank=True)
    mobile_number = models.CharField('Mobile Number', max_length=15, null=True, blank=True)
    alt_mobile_number = models.CharField('Alternet Mobile Number', max_length=15, null=True, blank=True)
    email = models.EmailField('Delivery Email', null=True, blank=True)
    house_number = models.CharField('House Number', max_length=20, null=True, blank=True)
    street = models.CharField('Street Address', max_length=250)
    city = models.CharField('City', max_length=100)
    state = models.CharField('State', max_length=100)
    zip_code = models.CharField('Zip Code', max_length=10)
    country = models.CharField('Country', default="India", max_length=50)
    is_default = models.BooleanField('Is Default', default=False)

    def __str__(self):
        """
        Returns the user and address for the user address.
        """
        return "{} {}, {}, {} - {}, {}".format(self.house_number, self.street, self.city, self.state, self.zip_code, self.country)
    
    @property
    def full_address(self):
        return  "{} {}, {}, {}, {}".format(self.house_number, self.street, self.city, self.state, self.country)
    
    class Meta:
        verbose_name = _("User Address")
        verbose_name_plural = _("User Addresses")



class Category(BaseModel):
    """
    A model representing a product category.
    """
    name = models.CharField("Name", max_length=100)
    image = models.ImageField(
        upload_to='category/', default="product-default.jpg",
        help_text="Upload image on size 720*300")

    def __str__(self):
        return self.name
    
    @property
    def product_count(self):
        return self.products.filter(status=True, stock__gte=1).count() or 0




class SubCategory(BaseModel):
    """
    A model representing a sub category.
    """
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField("Sub Category Name", max_length=100)

    def __str__(self):
        return str(self.name) + " > " + str(self.category)



class Product(BaseModel):
    """
    A model representing a product.
    """
    STATUS_CHOICES = (
        ("IN STOCK", "IN STOCK"),
        ("NOT IN STOCK", "NOT IN STOCK"),
        ("UPCOMMING", "UPCOMMING"),
    )
    
    UNIT_CHOICES = (
        ("CARATS", "CARATS"),
        ("RATTI", "RATTI"),
    )
    
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, verbose_name='Category',
        related_name="products", null=True, blank=True
    )
    
    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.SET_NULL, verbose_name='Sub Category',
        related_name="products", null=True, blank=True
    )
    name = models.CharField(_('Product Name'), max_length=100)
    sub_name = models.CharField(
        _('Product Sort Description'), max_length=250,
        # help_text="Product's short description or tagline"
    )
    description = models.TextField(
        _("Description"), null=True, blank=True,
        help_text="This will not showing in the frontend now")
    price = models.FloatField(_('Listing Price'))
    discount_price = models.FloatField(
        _('Discount Price'), default=0
    )
    selling_price = models.FloatField(
        _('Selling Price'), default=0, help_text=_(
            "= Listing Price - Discount Price, "
            "This will be automaticaly calculated."
        )
    )
    sku = models.CharField(
        _("SKU"), max_length=15, null=True, blank=True)
    stock = models.PositiveIntegerField(_('Stock Count'), default=0)
    image1 = models.ImageField(
        _("Product Image 1"), upload_to='products/', default='product-default.jpg', 
        help_text="Upload image with height=530 px and width=530 px")
    image2 = models.ImageField(
        _("Product Image 2"), upload_to='products/', null=True, blank=True, 
        help_text="Upload image with height=530 px and width=530 px")
    image3 = models.ImageField(
        _("Product Image 3"), upload_to='products/', null=True, blank=True,
        help_text="Upload image with height=530 px and width=530 px")
    image4 = models.ImageField(
        _("Product Image 4"), upload_to='products/', null=True, blank=True, 
        help_text="Upload image with height=530 px and width=530 px")
    image5 = models.ImageField(
        _("Product Image 5"), upload_to='products/', null=True, blank=True, 
        help_text="Upload image with height=530 px and width=530 px")
    video = models.FileField(
        _("Product Video"), upload_to='product-video/', null=True, blank=True,
        max_length=500,
        validators=[
            FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv']),
            file_size_10mb,],
        help_text="Upload Video less then 10 MB.")
    
    details = CKEditor5Field("Product Detail's", config_name='default', null=True, blank=True)
    # cons = CKEditor5Field('Cons', config_name='default', null=True, blank=True)
    # how_to_use = CKEditor5Field('How To Use', config_name='default', null=True, blank=True)
    
    availability = models.CharField(
        'Availability', max_length=14, choices=STATUS_CHOICES, default="IN STOCK"
    )
   
    
    status = models.BooleanField(
        _('Published Status'), default=True,
        help_text=_('If it is not active, the product will be hidden from the site.')
    )
    is_featured = models.BooleanField(_('Is Featured?'), default=False)
    is_new_arrival = models.BooleanField(_('Is New Arrival?'), default=False)

    def save(self, *args, **kwargs):
        self.selling_price = self.price - self.discount_price
        super().save(*args, **kwargs)
    
    class Meta:
        """
        Meta options for the Product model.
        """
        ordering = ['-created_at']
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        """
        Returns the name of the product.
        """
        return f"{self.name} ({self.price})"

    @property
    def list_price(self): # selling price
        return self.price + self.discount_price
    
    @property
    def rating(self):
        """
        Average rating of this product
        """
        rating = self.reviews.aggregate(
            models.Avg('rating'))['rating__avg']
        if not rating:
            return 4.6
        return round(rating, 2)



class ProductFAQ(BaseModel):
    """
    A model representing a frequently asked question (FAQ) for a product.
    """
    product = models.ForeignKey(
        Product, related_name='faqs', on_delete=models.CASCADE
    )
    question = models.CharField('Question', max_length=150)
    answer = models.TextField('Answer')
    status = models.BooleanField('Status', default=True)

    def __str__(self):
        """
        Returns the question of the FAQ.
        """
        return self.question



class ProductReview(BaseModel):
    """
    A model representing a product review.
    """
    PRODUCT_RATING_CHOICES = (
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    )
    product = models.ForeignKey(
        Product, related_name='reviews', on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(_('Rating'), choices=PRODUCT_RATING_CHOICES)
    review = models.TextField('Review', null=True, blank=True)
    status = models.BooleanField('Status', default=True)

    def __str__(self):
        """
        Returns the user and product for the review.
        """
        return f'{self.user} - {self.product}'



class Cart(BaseModel):
    """
    A model representing a product cart.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Cart Items"
        unique_together = ('user', 'product')

    def __str__(self):
        """
        Returns the user, product, and quantity for the product cart.
        """
        return f'{self.user} - {self.product} ({self.quantity})'



class Order(BaseModel):
    """
    A model representing a product order.
    """
    ORDER_STATUS_CHOICES = (
        ("PENDING", "PENDING"),
        ("ORDERED", "ORDERED"),
        ("IN-PROGRESS", "IN-PROGRESS"),
        ("DELIVERED", "DELIVERED"),
        ("FAILED", "FAILED"),
        ("CENCELED", "CENCELED"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.FloatField(default=0)
    status = models.CharField(max_length=12, choices=ORDER_STATUS_CHOICES, default="PENDING")
    delivery_address = models.CharField(_("Delivery Address"), max_length=250, null=True, blank=True)
    delivery_zip_code = models.CharField(_("Delivery ZIP Code"), max_length=10, null=True, blank=True)
    cancelation_reason = models.CharField(
        _("Order Cancelation Reason"), max_length=100,
        help_text = _("If User Cencel the order they can specify the cancelation reason"),
        null=True, blank=True)
    payment_screentshot = models.ImageField(
        verbose_name="Payment Sceenshot", null=True, blank=True,
        upload_to="order/payments-screenshots/",
        help_text="Custumer will upload screenshot of payment after order the product.")

    def __str__(self):
        """
        Returns the user and order date for the order.
        """
        return f'{self.user} - {self.created_at}'
    
    @property
    def order_id(self):
        """
        This is an id to show only
        """
        return f"#{str(self.pk).zfill(3)}"
    


class OrderProduct(BaseModel):
    """
    A model representing the relationship between an order and a product.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_products')
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField()

    class Meta:
        verbose_name = "Order Product"
        verbose_name_plural = "Order Products"
        unique_together = ('order', 'product',)

    def __str__(self):
        """
        Returns the order, product, and quantity for the order product.
        """
        return f'{self.order} - {self.product} ({self.quantity})'



class Transaction(BaseModel):
    """
    A model representing a financial transaction.
    """
    TRANSACTION_STATUS_CHOICES = (
        ("PENDING", "PENDING"),
        ("SUCCESS", "SUCCESS"),
        ("FAILED", "FAILED"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions')
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=TRANSACTION_STATUS_CHOICES, default="PENDING")
    mode = models.CharField(
        _("Transaction Mode"),
        max_length=10,
        choices=(
            ("CASH", 'CASH'),
            ("ONLINE", 'ONLINE'),
            ),
        default="CASH")
    # method = models.CharField(
    #     _("Transaction Method"),
    #     max_length=10,
    #     choices=(
    #         ("RazorPay", 'RazorPay'),
    #         ("PayU", 'PayU'),
    #         ("CASH", 'CASH'),
    #     ), default="CASH")
    
    # Bank Transaction  Details
    tracking_id = models.CharField(
        _("Bank Tracking/UTR Number"),
        max_length=100,
        null = True, blank=True
    )
    pay_sign = models.CharField(
        _("Payment Signature"),
        max_length=250,
        null = True, blank=True
    )

    def __str__(self):
        """
        Returns the user, order, and status for the transaction.
        """
        return f'{self.user} - {self.order} - {self.status}'


class Blog(BaseModel):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blog/', default="product-default.jpg")
    content = CKEditor5Field(config_name='extends', null=True, blank=True)
    published = models.BooleanField(_('Is Published'), default=False)



class Review(BaseModel):
    """
    A model representing a review.
    """
    RATING_CHOICES = (
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(_('Rating'), choices=RATING_CHOICES)
    review = models.TextField('Review', null=True, blank=True)
    status = models.BooleanField('Status', default=True)

    def __str__(self):
        """
        Returns the user and rating for the review.
        """
        return f'{self.user} - {self.rating}'



class ContactUs(BaseModel):
    """
    A model representing a Contact or Help.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True, blank=True)
    mobile_number = models.CharField(
        _("Mobile Number"), max_length=20,
        validators = [phone_validator],
        null=True, blank=True
    )
    message = models.TextField('Message', null=True, blank=True)
    status = models.BooleanField('Status', default=True)

    def __str__(self):
        """
        Returns the user and rating for the review.
        """
        return f'{self.name} - {self.mobile_number}'
