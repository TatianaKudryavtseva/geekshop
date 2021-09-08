from django.urls import path

from admins.views import index, UserListView, UserCreateView, UserUpdateView, UserDeleteView
from admins.views import admin_product, admin_product_create, admin_category, admin_category_create

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admin_users'),
    path('users-create/', UserCreateView.as_view(), name='admin_users_create'),
    path('users-update/<int:pk>', UserUpdateView.as_view(), name='admin_user_update'),
    path('users-delete/<int:pk>', UserDeleteView.as_view(), name='admin_user_delete'),
    path('product/', admin_product, name='admin_product'),
    path('product/product-create/', admin_product_create, name='admin_product_create'),
    path('category/', admin_category, name='admin_category'),
    path('category/category-create', admin_category_create, name='admin_category_create'),
]
