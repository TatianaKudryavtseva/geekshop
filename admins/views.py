from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test

from users.models import User
from products.models import Product, ProductCategory
from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm, ProductAdmin, CategoryAdmin


@user_passes_test(lambda u: u.is_staff)
def index(request):
    context = {'title': 'GeekShop - Admin'}
    return render(request, 'admins/index.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_users(request):
    context = {'title': 'Geekshop - Пользователи', 'users': User.objects.all()}
    return render(request, 'admins/admin-users.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_users_create(request):
    if request.method == 'POST':
        form = UserAdminRegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_users'))
    else:
        form = UserAdminRegistrationForm()
    context = {'title': 'Geekshop - Создание пользователя', 'form': form}
    return render(request, 'admins/admin-users-create.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_user_update(request, id):
    selected_user = User.objects.get(id=id)
    if request.method == 'POST':
        form = UserAdminProfileForm(instance=selected_user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_users'))
    else:
        form = UserAdminProfileForm(instance=selected_user)
    context = {
        'title': 'Geekshop - Редактирование пользователя',
        'selected_user': selected_user,
        'form': form
    }
    return render(request, 'admins/admin-user-update-delete.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_user_delete(requets, id):
    user = User.objects.get(id=id)
    user.is_active = False
    user.save()
    return HttpResponseRedirect(reverse('admins:admin_users'))


@user_passes_test(lambda u: u.is_staff)
def admin_product(request):
    context = {'title': 'GeekShop - Продукты', 'products': Product.objects.all()}
    return render(request, 'admins/admin-product.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_product_create(request):
    if request.method == 'POST':
        form = ProductAdmin(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_product'))
    else:
        form = ProductAdmin()
    context = {'title': 'Geekshop - Добавление продукта', 'form': form}
    return render(request, 'admins/admin-product-create.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_category(request):
    context = {'title': 'GeekShop - Категории', 'category': ProductCategory.objects.all()}
    return render(request, 'admins/admin-category.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_category_create(request):
    if request.method == 'POST':
        form = CategoryAdmin(data=request.POST)
        if form.is_valid():
            form.save()
            print(form.errors)
            return HttpResponseRedirect(reverse('admins:admin_category'))
    else:
        form = CategoryAdmin()
    context = {'title': 'Geekshop - Добавление категории', 'form': form}
    return render(request, 'admins/admin-category-create.html', context)
