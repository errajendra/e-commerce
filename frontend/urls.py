from django.urls import path, include
from .views import *


urlpatterns = [
    path('ajax/', include('user.ajax.urls')),
    path('', index, name='home'),
    path('login-user/', login_customer, name='login_customer'),
    path('register-user/', register_customer, name='register_customer'),
    path('product-list/', product_list, name='product_list'),
    path('product/<int:id>/', product_details, name='product_detail'),
    path('checkout/<int:product_id>/', checkout, name='checkout'),
    path('account/', account, name='account'),
    path('contact-us/', contact, name='contact'),
    path('tc/', tc, name='tc'),
    path('privacy-policy/', privacy_policy, name='pc'),
    path('refund-policy/', refund_policy, name='refund_policy'),

]
