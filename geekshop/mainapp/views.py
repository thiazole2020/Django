from django.shortcuts import render
import json


def products(request):
    title = 'Каталог'

    f = open('mainapp\data.json', 'r', encoding='utf8')
    links_menu = json.load(f)

    context = {
        'title': title,
        'links_menu': links_menu,
    }

    return render(request, 'mainapp/products.html', context)
