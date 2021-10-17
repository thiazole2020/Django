from django.shortcuts import render, get_object_or_404
from mainapp.models import StyleCategory, Product
from basketapp.models import Basket


def products(request, pk=None):
    title = 'Каталог'
    links_menu = StyleCategory.objects.all()

    products = Product.objects.all().order_by('price')
    same_products = Product.objects.all()[0:2]
    basket = Basket.objects.filter(user=request.user)

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
            'same_products': same_products,
            'basket': basket,
        }

        return render(request, 'mainapp/products.html', context)


    context = {
        'title': title,
        'links_menu': links_menu,
        'products': products,
        'same_products': same_products,
        'basket': basket,
    }

    return render(request, 'mainapp/products.html', context)
