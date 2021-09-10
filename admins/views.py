from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from users.models import User
from products.models import Product, ProductCategory
from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm, ProductAdmin, CategoryAdmin


class UserPageView(TemplateView):
    template_name = 'admins/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserPageView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Admin'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserPageView, self).dispatch(request, *args, **kwargs)


class UserListView(ListView):
    model = User
    template_name = 'admins/admin-users.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'Geekshop - Пользователи'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)


class UserCreateView(CreateView):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegistrationForm
    success_url = reverse_lazy('admins:admin_users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Geekshop - Создание пользователя'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)


class UserUpdateView(UpdateView):
    model = User
    template_name = 'admins/admin-user-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Geekshop - Редактирование пользователя'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)


class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/admin-user-update-delete.html'
    success_url = reverse_lazy('admins:admin_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.safe_delete()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)


class ProductPageView(ListView):
    model = Product
    template_name = 'admins/admin-product.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductPageView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Продукты'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductPageView, self).dispatch(request, *args, **kwargs)


class ProductCreateView(CreateView):
    model = Product
    template_name = 'admins/admin-product-create.html'
    form_class = ProductAdmin
    success_url = reverse_lazy('admins:admin_product')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Geekshop - Добавление продукта'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductCreateView, self).dispatch(request, *args, **kwargs)


class CategoryPageView(ListView):
    model = ProductCategory
    template_name = 'admins/admin-category.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryPageView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Категории'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryPageView, self).dispatch(request, *args, **kwargs)


class CategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'admins/admin-category-create.html'
    form_class = CategoryAdmin
    success_url = reverse_lazy('admins:admin_category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Geekshop - Добавление категории'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryCreateView, self).dispatch(request, *args, **kwargs)
