from django.urls import path
from .views import redirect_payment_url, create_payu_order_link



urlpatterns = [
    path('redirect-pay/', redirect_payment_url, name='redirect_payurl'),
    path('create-payu-order-link/', create_payu_order_link, name='crate_payu_order_link')
]