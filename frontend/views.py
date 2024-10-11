from django.shortcuts import render, get_object_or_404
from ecommerce_app.models import Product, Cart, Banner, Category


def index(request):
    """ Home page"""
    context = {
        'title': 'Home',
        'products': Product.objects.filter(status=True)[:8],
        'categories': Category.objects.all(),
    }
    return render(request, 'frontend/index.html', context)


def product_list(request, category: int):
    """ List of products by category & searches """
    category = get_object_or_404(Category, id=category)
    context = {
        'title': category.name,
    }
    return render(request, 'frontend/product-list.html', context)


def product_details(request, id:int):
    """ Product details """
    product = get_object_or_404(Product, id=id)
    context = {
        'product': product
    }
    return render(request, 'frontend/product-detail.html', context)


def cart(request):
    """ Cart page """
    context = {
        'title': 'Cart',
    }
    return render(request, "frontend/cart.html", context)
