from django.urls import path
from .views import payu_success_webhook, payu_fail_webhook


urlpatterns = [
    path('payu-success/', payu_success_webhook, name='payu_success_webhook'),
    path('payu-failed/', payu_fail_webhook, name='payu_fail_webhook'),
]
