"""
URL configuration for eCommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user.utils import render_index_page
from .constance_config_view import update_confi_setting


admin.site.site_header = "AstroStone E-Commerce"
admin.site.site_title = "Admin"
admin.site.index_title = "Administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('frontend.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls'),
         name="ck_editor_5_upload_file"),
    path('user/', include('user.urls')),
    path('ecommerce/', include('ecommerce_app.urls')),
    path('update-constance-setting/', update_confi_setting, name="update-constance"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
