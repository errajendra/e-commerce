from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import (
    Category, Product,
    ProductFAQ, ProductReview,
    Banner, Blog, Review,
    SubCategory,
)


"""
Category Forms
"""
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }



"""
Sub Category Forms
"""
class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = "__all__"
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category_title': forms.Select(attrs={'class': 'form-control'}),
        }



""" 
Product Form
- Includes a form field for the category that this product belongs to.
"""
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ('sub_category', 'selling_price')
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'sub_category': forms.Select(attrs={'class': 'form-control'}),
            'sub_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'availability': forms.Select(attrs={'class': 'form-control'}),
            # 'unit': forms.Select(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            # 'treatment': forms.TextInput(attrs={'class': 'form-control'}),
            # 'transparency': forms.TextInput(attrs={'class': 'form-control'}),
            # 'shape': forms.TextInput(attrs={'class': 'form-control'}),
            # 'origin': forms.TextInput(attrs={'class': 'form-control'}),
            # 'color': forms.TextInput(attrs={'class': 'form-control'}),
            # 'specific_gravity': forms.TextInput(attrs={'class': 'form-control'}),
            # 'refractive_index': forms.TextInput(attrs={'class': 'form-control'}),
            # 'exact_dimension': forms.TextInput(attrs={'class': 'form-control'}),
            # 'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'certification': forms.TextInput(attrs={'class': 'form-control'}),
            
            "details": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="default"
            ),
        }
        


"""
Product FAQs Form
"""
class ProductFAQsForm(forms.ModelForm):
    class Meta:
        model = ProductFAQ
        fields = "__all__"

        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'class': 'form-control'}),
        }



"""
Product Review Form
"""
class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = "__all__"

        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'class': 'form-control'}),
        }



"""
Home Page Banner Form
"""
class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = "__all__"

        widgets = {
            'page': forms.Select(attrs={'class': 'form-control'}),
            'use_for': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }



"""
Blogs Form
"""
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'sub_title': forms.TextInput(attrs={'class': 'form-control'}),
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            )
        }



"""
Reviews Form
"""
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = "__all__"
        
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'review': forms.Textarea(attrs={'class': 'form-control'}),
        }
