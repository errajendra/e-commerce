from django.urls import path, include
from .views import *

urlpatterns = [
    # Api
    path('api/', include('ecommerce_app.api.urls')),
    # Ajax
    path('ajax/', include('ecommerce_app.ajax.urls')),
    
    # Category Urls
    path('add-category/', add_category, name='add_category'),
    path('update-category/<int:pk>/', update_category, name='update_category'),
    path('list-categories/', list_categories, name='list_categories'),
    path('delete-category/<int:pk>/', delete_category, name='delete_category'),
    
    # Sub Category Urls
    path('add-sub-category/', add_sub_category, name='add_sub_category'),
    path('update-sub-category/<int:pk>/', update_sub_category, name='update_sub_category'),
    path('list-sub-categories/', list_sub_categories, name='list_sub_categories'),
    path('delete-sub-category/<int:pk>/', delete_sub_category, name='delete_sub_category'),
    
    # Product Urls
    path('add-product/', add_product, name='add_product'),
    path('update-product/<int:pk>/', update_product, name='update_product'),
    path('list-products/', list_products, name='list_products'),
    path('delete-product/<int:pk>/', delete_product, name='delete_product'),
    
    # Product FAQs Urls
    path('add-productfaq/', add_productfaq, name='add_productfaq'),
    path('update-productfaq/<int:pk>/', update_productfaq, name='update_productfaq'),
    path('list-productfaqs/', list_productfaqs, name='list_productfaqs'),
    path('delete-productfaq/<int:pk>/', delete_productfaq, name='delete_productfaq'),
    
    # Product Reviews  Urls
    path('add-productreview/', add_productreview, name='add_productreview'),
    path('update-productreview/<int:pk>/', update_productreview, name='update_productreview'),
    path('list-productreviews/<int:id>/', list_productreviews, name='list_productreviews'),
    path('delete-productreview/<int:pk>/', delete_productreview, name='delete_productreview'),
    
    # Banner  Urls
    path('add-banner/', add_banner, name='add_banner'),
    path('update-banner/<int:pk>/', update_banner, name='update_banner'),
    path('list-banners/', list_banners, name='list_banners'),
    path('delete-banner/<int:pk>/', delete_banner, name='delete_banner'),
    
    # blog  Urls
    path('add-blog/', add_blog, name='add_blog'),
    path('update-blog/<int:pk>/', update_blog, name='update_blog'),
    path('list-blogs/', list_blogs, name='list_blogs'),
    path('delete-blog/<int:pk>/', delete_blog, name='delete_blog'),
    
    # Reviews  Urls
    path('add-review/', add_review, name='add_review'),
    path('update-review/<int:pk>/', update_review, name='update_review'),
    path('list-reviews/', list_reviews, name='list_reviews'),
    path('delete-review/<int:pk>/', delete_review, name='delete_review'),
    
    # Cart  Urls
    path('list-user-cart/<int:pk>/', user_cart_list, name='list_user_cart'),
    path('delete-cart/<int:pk>/', delete_cart, name='delete_cart'),
    
    # Order Urls
    path('orders/', order_list, name="orders"),
    path('orders/<int:user_id>/', order_list, name="user-orders"),
    
    # Transactions Urls
    path('transactions/', transaction_list, name="transactions"),
    path('transactions/<int:user_id>/', transaction_list, name="user-tnxs"),
]
