from django.urls import path
from .views import (
    redirect_payment_url, create_payu_order_link,
)
from .phonepay import create_pg_order_link, check_pg_transaction_status



urlpatterns = [
    path('redirect-pay/', redirect_payment_url, name='redirect_payurl'),
    path('webhook-phonepay/<str:tran_id>/', check_pg_transaction_status, name='phonepay_webhook'),
    path('create-payu-order-link/', create_payu_order_link, name='crate_payu_order_link'),
    path('create-phonerpay-order-link/', create_pg_order_link, name='crate_phonerpay_order_link'),
]