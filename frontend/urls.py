from django.urls import path, include
from .views import *


urlpatterns = [
    path('ajax/', include('user.ajax.urls')),
    path('', index, name='home'),
    path('product-list/<int:category>/', product_list, name='product_list'),
    path('product/<int:id>/', product_details, name='product_detail'),

]
