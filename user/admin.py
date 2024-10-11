from django.contrib import admin
from .models import *


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'dialing_code', 'mobile_number', 'otp',
        'date_joined', 'is_active'
    )
    readonly_fields = ("password",)
    list_editable = ('is_active',)
    list_filter = ('dialing_code', 'date_joined', 'is_active')
    search_fields = ('name', 'email', 'mobile_number')
    
    fieldsets = (
        ("Profile", {
            "classes": ("wide",),  # A custom CSS class that will be applied to the fieldset.
            "fields": ("name", "email", "dialing_code", "mobile_number")
        }),
        ("Password and Authorization", {
            "classes": ("collapse",),  # A custom CSS class that will be applied to the fieldset, and makes it collaps
            "fields": ("password", "otp"),
        }),
        ("More options", {
            "classes": ("collapse",),
            "fields": (
                "is_active", "is_staff", "is_superuser", 
                "login_method", "social_id"
            )
        })
    )
    

@admin.register(CountryCode)
class CountryCodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'dialing_code', 'country_code')
    search_fields = ('name', 'dialing_code')
