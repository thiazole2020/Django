from authapp.models import ShopUser
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
from mainapp.models import Product, ProductCategory, StyleCategory
from django.contrib.auth.decorators import user_passes_test
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm
from mainapp.forms import StyleCategoryCreateForm


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'админка/пользователи'
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'title': title,
        'objects': users_list
    }

    return render(request, 'adminapp/users.html', context)


def user_create(request):
    title = 'создание пользователя'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        user_form = ShopUserRegisterForm()


    context = {
        'title': title,
        'user_form': user_form
    }

    return render(request, 'adminapp/user_update.html', context)


def user_update(request, pk):
    title = 'редактирование пользователя'
    edit_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:user_update', args=[edit_user.pk]))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    context = {
        'title': title,
        'user_form': edit_form
    }

    return render(request, 'adminapp/user_update.html', context)


def user_delete(request, pk):
    title = 'удаление пользователя'
    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin_staff:users'))


    context = {
        'title': title,
        'user_to_delete': user
    }

    return render(request, 'adminapp/user_delete.html', context)


def categories(request):
    title = 'админка/категории'
    style_categories_list = StyleCategory.objects.all()

    context = {
        'title': title,
        'objects': style_categories_list
    }

    return render(request, 'adminapp/categories.html', context)


def category_create(request):
    title = 'создание стилевой категории'

    if request.method == 'POST':
        style_category_form = StyleCategoryCreateForm(request.POST, request.FILES)
        if style_category_form.is_valid():
            style_category_form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))
    else:
        style_category_form = StyleCategoryCreateForm()

    context = {
        'title': title,
        'style_category_form': style_category_form
    }

    return render(request, 'adminapp/style_category_update.html', context)


def category_update(request, pk):
    title = 'редактирование стилевой категории'
    edit_style_category = get_object_or_404(StyleCategory, pk=pk)

    if request.method == 'POST':
        edit_form = StyleCategoryCreateForm(request.POST, instance=edit_style_category)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:category_update', args=[edit_style_category.pk]))
    else:
        edit_form = StyleCategoryCreateForm(instance=edit_style_category)

    context = {
        'title': title,
        'style_category_form': edit_form
    }

    return render(request, 'adminapp/style_category_update.html', context)


def category_delete(request, pk):
    title = 'удаление стилевой категории'
    style_category = get_object_or_404(StyleCategory, pk=pk)

    if request.method == 'POST':
        style_category.is_active = False
        style_category.save()
        return HttpResponseRedirect(reverse('admin_staff:categories'))

    context = {
        'title': title,
        'style_category_to_delete': style_category
    }

    return render(request, 'adminapp/style_category_delete.html', context)


def products(request, pk):
    title = 'админка/продукт'
    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    context = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', context)


def product_create(request, pk):
    pass


def product_read(request, pk):
    pass


def product_update(request, pk):
    pass


def product_delete(request, pk):
    pass
