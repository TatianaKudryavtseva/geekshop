from django.dispatch import receiver
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from users.models import User
from products.models import Product, ProductCategory
from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm, ProductAdmin, CategoryAdmin, CategoryEditForm
from common.view import CommonContextMixin
from django.db.models.signals import pre_save
from django.db import connection
from django.db.models import F, Q


class UserPageView(CommonContextMixin, TemplateView):
    template_name = 'admins/index.html'
    title = 'GeekShop - Admin'

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/users/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(UserPageView, self).dispatch(request, *args, **kwargs)


class UserListView(CommonContextMixin, ListView):
    model = User
    template_name = 'admins/admin-users.html'
    title = 'Geekshop - Пользователи'

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/users/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)


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

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/users/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductPageView, self).dispatch(request, *args, **kwargs)


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


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_category_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)
        db_profile_by_type(sender, 'UPDATE', connection.queries)


class CategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'admins/admin-category-update.html'
    form_class = CategoryEditForm
    success_url = reverse_lazy('admins:admin_category')

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Редактирование категории'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/'))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryUpdateView, self).dispatch(request, *args, **kwargs)