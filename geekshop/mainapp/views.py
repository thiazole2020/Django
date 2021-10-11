from django.shortcuts import render
from mainapp.models import StyleCategory

def products(request):
    title = 'Каталог'
    links_menu = StyleCategory.objects.all()

    context = {
        'title': title,
        'links_menu': links_menu,
    }

    return render(request, 'mainapp/products.html', context)
