from authapp.models import ShopUser
from django.db import connection
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from mainapp.models import Product, ProductCategory, StyleCategory
from django.contrib.auth.decorators import user_passes_test
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm, ProductEditForm
from mainapp.forms import StyleCategoryCreateForm
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UsersListView, self).get_context_data()
        context['title'] = 'админка/пользователи'

        return context

    def get_queryset(self):
        return ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'админка/пользователи'
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     context = {
#         'title': title,
#         'objects': users_list
#     }
#
#     return render(request, 'adminapp/users.html', context)


class UsersCreateView(CreateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UsersCreateView, self).get_context_data()
        context['title'] = 'создание пользователя'
        return context


# def user_create(request):
#     title = 'создание пользователя'
#
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:users'))
#     else:
#         user_form = ShopUserRegisterForm()
#
#
#     context = {
#         'title': title,
#         'user_form': user_form
#     }
#
#     return render(request, 'adminapp/user_update.html', context)


class UsersUpdateView(UpdateView):
    model = ShopUser
    form_class = ShopUserAdminEditForm
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')
    context_object_name = 'user_form'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UsersUpdateView, self).get_context_data()
        context['title'] = 'редактирование пользователя'
        return context


# def user_update(request, pk):
#     title = 'редактирование пользователя'
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:user_update', args=[edit_user.pk]))
#     else:
#         edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#     context = {
#         'title': title,
#         'user_form': edit_form
#     }
#
#     return render(request, 'adminapp/user_update.html', context)


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin_staff:users')
    context_object_name = 'user_to_delete'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# def user_delete(request, pk):
#     title = 'удаление пользователя'
#     user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         user.is_active = False
#         user.save()
#         return HttpResponseRedirect(reverse('admin_staff:users'))
#
#
#     context = {
#         'title': title,
#         'user_to_delete': user
#     }
#
#     return render(request, 'adminapp/user_delete.html', context)


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
    title = 'продукты категории'
    style_category = get_object_or_404(StyleCategory, pk=pk)
    products_list = Product.objects.filter(style_category__pk=pk).order_by('name')

    context = {
        'title': title,
        'style_category': style_category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', context)


def product_create(request, pk):
    title = 'создание продукта'
    style_category = get_object_or_404(StyleCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin_staff:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'style_category': style_category})

    context = {
        'title': title,
        'product_form': product_form,
        'style_category': style_category,
    }

    return render(request, 'adminapp/product_update.html', context)


def product_read(request, pk):
    title = 'подробное описание товара'
    product = get_object_or_404(Product, pk=pk)

    context = {
        'title': title,
        'object': product,
    }

    return render(request, 'adminapp/product_read.html', context)


def product_update(request, pk):
    title = 'редактирование товара'
    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:product_update', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    context = {
        'title': title,
        'product_form': edit_form
    }

    return render(request, 'adminapp/product_update.html', context)


def product_delete(request, pk):
    title = 'удаление продукта'
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse('admin_staff:products', args=[product.style_category.pk]))

    context = {
        'title': title,
        'product_to_delete': product
    }

    return render(request, 'adminapp/product_delete.html', context)


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}: ')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=StyleCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        instance.product_set.update(is_active=instance.is_active)
        db_profile_by_type(sender, 'UPDATE', connection.queries)