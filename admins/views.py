from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from users.models import User
from products.models import Product, ProductCategory
from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm, ProductAdmin, CategoryAdmin
from common.view import CommonContextMixin


class UserPageView(CommonContextMixin, TemplateView):
    template_name = 'admins/index.html'
    title = 'GeekShop - Admin'

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserPageView, self).dispatch(request, *args, **kwargs)


class UserListView(CommonContextMixin, ListView):
    model = User
    template_name = 'admins/admin-users.html'
    title = 'Geekshop - Пользователи'


class UserCreateView(CommonContextMixin, CreateView):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegistrationForm
    success_url = reverse_lazy('admins:admin_users')
    title = 'Geekshop - Создание пользователя'


class UserUpdateView(UpdateView):
    model = User
    template_name = 'admins/admin-user-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')
    title = 'Geekshop - Редактирование пользователя'


class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/admin-user-update-delete.html'
    success_url = reverse_lazy('admins:admin_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.safe_delete()
        return HttpResponseRedirect(self.get_success_url())


class ProductPageView(CommonContextMixin, ListView):
    model = Product
    template_name = 'admins/admin-product.html'
    title = 'GeekShop - Продукты'


class ProductCreateView(CommonContextMixin,CreateView):
    model = Product
    template_name = 'admins/admin-product-create.html'
    form_class = ProductAdmin
    success_url = reverse_lazy('admins:admin_product')
    title = 'Geekshop - Добавление продукта'


class CategoryPageView(ListView):
    model = ProductCategory
    template_name = 'admins/admin-category.html'
    title = 'GeekShop - Категории'


class CategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'admins/admin-category-create.html'
    form_class = CategoryAdmin
    success_url = reverse_lazy('admins:admin_category')
    title = 'Geekshop - Добавление категории'
