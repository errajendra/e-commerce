from django.urls import path
from .views import *


urlpatterns = [
    #update order status url
    path('update-order-status/', update_order_status, name='update-order-status-ajax'),
    # Update Transaction status
    path('update-tnx-status/', update_tnx_status, name='update-tnx-status-ajax'),
]
