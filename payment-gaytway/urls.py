from django.urls import path
from .views import (
    redirect_payment_url, create_payu_order_link,
    payment_failed, payment_successful
)
from .phonepay import create_pg_order_link, check_pg_transaction_status
from .rzp_views import create_rzp_order_link, verify_rzp_payment



urlpatterns = [
    # link for Trading App
    path('redirect-pay/', redirect_payment_url, name='redirect_payurl'),
    path('create-payu-order-link/', create_payu_order_link, name='crate_payu_order_link'),
    path('webhook-phonepay/<str:tran_id>/', check_pg_transaction_status, name='phonepay_webhook'),
    path('create-phonerpay-order-link/', create_pg_order_link, name='crate_phonerpay_order_link'),
    path('create-rzp-order-link/', create_rzp_order_link, name='crate_rzp_order_link'),
    path('webhook-rzp/', verify_rzp_payment, name='rzp_webhook'),
    path('payment-failed/', payment_failed, name='payment_failed'),
    path('payment-successful/', payment_successful, name='payment_successful'),
]