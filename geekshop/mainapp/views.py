from django.shortcuts import render, get_object_or_404
from mainapp.models import StyleCategory, Product
from basketapp.models import Basket
import random

def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(style_category=hot_product.style_category).exclude(pk=hot_product.pk)[:3]
    return same_products


def products(request, pk=None):
    title = 'Каталог'
    links_menu = StyleCategory.objects.all()

    products = Product.objects.all().order_by('price')
    basket = get_basket(request.user)


    if pk is not None:
        if pk == 0:
            style_category = {'name': 'все'}
        else:
            style_category = get_object_or_404(StyleCategory, pk=pk)
            products = Product.objects.filter(style_category__pk=pk).order_by('price')

        context = {
            'title': title,
            'links_menu': links_menu,
            'style_category': style_category,
            'products': products,
            'basket': basket,
        }

        return render(request, 'mainapp/products.html', context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    context = {
        'title': title,
        'links_menu': links_menu,
        'products': products,
        'same_products': same_products,
        'hot_product': hot_product,
        'basket': basket,
    }

    return render(request, 'mainapp/products.html', context)


def product(request, pk):
    title = 'Товар'
    product = get_object_or_404(Product, pk=pk)
    same_products = get_same_products(product)

    context = {
        'title': title,
        'links_menu': StyleCategory.objects.all(),
        'product': product,
        'basket': get_basket(request.user),
        'same_products': same_products,
    }

    return render(request, 'mainapp/product.html', context)