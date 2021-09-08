from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from users.models import User
from products.models import Product, ProductCategory
from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm, ProductAdmin, CategoryAdmin


@user_passes_test(lambda u: u.is_staff)
def index(request):
    context = {'title': 'GeekShop - Admin'}
    return render(request, 'admins/index.html', context)


#@user_passes_test(lambda u: u.is_staff)
#def admin_users(request):
  #  context = {'title': 'Geekshop - Пользователи', 'users': User.objects.all()}
  #  return render(request, 'admins/admin-users.html', context)


class UserListView(ListView):
    model = User
    template_name = 'admins/admin-users.html'


#@user_passes_test(lambda u: u.is_staff)
#def admin_users_create(request):
#    if request.method == 'POST':
#        form = UserAdminRegistrationForm(data=request.POST, files=request.FILES)
#        if form.is_valid():
#            form.save()
#            return HttpResponseRedirect(reverse('admins:admin_users'))
#    else:
#        form = UserAdminRegistrationForm()
#    context = {'title': 'Geekshop - Создание пользователя', 'form': form}
#    return render(request, 'admins/admin-users-create.html', context)


class UserCreateView(CreateView):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegistrationForm
    success_url = reverse_lazy('admins:admin_users')


#@user_passes_test(lambda u: u.is_staff)
#def admin_user_update(request, id):
#   selected_user = User.objects.get(id=id)
#    if request.method == 'POST':
#        form = UserAdminProfileForm(instance=selected_user, data=request.POST, files=request.FILES)
#        if form.is_valid():
#            form.save()
#            return HttpResponseRedirect(reverse('admins:admin_users'))
#    else:
#        form = UserAdminProfileForm(instance=selected_user)
#    context = {
#        'title': 'Geekshop - Редактирование пользователя',
#        'selected_user': selected_user,
#        'form': form
#    }
#    return render(request, 'admins/admin-user-update-delete.html', context)


class UserUpdateView(UpdateView):
    model = User
    template_name = 'admins/admin-user-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')


class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/admin-user-update-delete.html'
    success_url = reverse_lazy('admins:admin_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.safe_delete()
        return HttpResponseRedirect(self.get_success_url())


#@user_passes_test(lambda u: u.is_staff)
#def admin_user_delete(requets, id):
#    user = User.objects.get(id=id)
#    user.is_active = False
#    user.save()
#    return HttpResponseRedirect(reverse('admins:admin_users'))


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
