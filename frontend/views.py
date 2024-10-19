from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from ecommerce_app.models import Product, Category
from user.models import CustomUser as User
from user.forms import UserUpdateForm


def index(request):
    """ Home page"""
    all_products = Product.objects.select_related().filter(
        status = True,
        stock__gte = 1
    )
    categories = Category.objects.filter(
        id__in = all_products.values_list('category', flat=True).distinct())[:5]

    recommended = []
    recommended.append({
        'title': 'All',
        'slug': '0',
        'list': all_products[:12]
    })

    for cat in categories:
        recommended.append({
            'title': f'{cat.name}',
            'slug': f'{cat.id}',
            'list': all_products.filter(category=cat)[:6]
        })
    
    context = {
        'title': 'Home',
        'products': all_products.filter(is_featured=True)[:6],
        'recommendeds': recommended,
    }
    return render(request, 'frontend/index.html', context)


def product_list(request):
    """ List of products by category & searches """
    
    title = "Shop"
    products = Product.objects.filter(
        status = True,
        stock__gte = 1)
    categories = Category.objects.filter(
        id__in = products.values_list('category', flat=True)
        .distinct())[:10]
    context = {
        'title': title,
        'products': products,
        'categories': categories
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


def checkout(request, product_id):
    """ Checkout page 
    User can buy the product direct without adding to cart.
    """
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,
    }
    return render(request, "frontend/checkout.html", context)


def contact(request):
    """ Contact page """
    context = {
        'title': 'Contact',
        }
    return render(request, "frontend/contact.html", context)


def account(request):
    """ Account page """
    user = request.user
    context = {
        "title": "Account"
    }
    if user.is_authenticated:
        user = get_object_or_404(User, id=user.id)
        if request.method == "POST":
            form = UserUpdateForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
    return render(request, "frontend/user-account.html", context)


def login_customer(request):
    """ Custumer Login Method. """
    if request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        try:
            user = User.objects.get(email=email)
        except:
            user = None
        print(password)
        if user:
            if user.check_password(password):
                login(request, user)
                next = request.GET.get('next', None)
                if next:
                    return redirect(next)
                return redirect('home')
    return redirect('account')


def tc(request):
    """ Terms and Conditions page """
    context = {
        'title': 'Terms and Conditions',
        }
    return render(request, "frontend/terms-and-conditions.html", context)


def privacy_policy(request):
    """ Privacy Policy page """
    context = {
        'title': "Privacy Policy",
    }
    return render(request, "frontend/privacy-policy.html", context)

def refund_policy(request):
    """ Refund Policy page """
    context = {
        'title': "Refund Policy",
    }
    return render(request, "frontend/refund-policy.html", context)
