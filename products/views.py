from products.models import Product, ProductCategory

from django.shortcuts import render


def index(request):
    context = {'title': 'GeekShop', 'header': 'GeekShop Store'}
    return render(request, 'products/index.html', context)


def products(request):
    goods = Product.objects.all()
    items = ProductCategory.objects.all()
    context = {
        'title': 'GeekShop - Каталог',
        'header': 'GeekShop',
        'products': goods,
        'category': items

    }
    return render(request, 'products/products.html', context)
