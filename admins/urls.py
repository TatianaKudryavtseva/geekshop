from django.urls import path

from admins.views import UserPageView, UserListView, UserCreateView, UserUpdateView, UserDeleteView
from admins.views import ProductPageView, ProductCreateView, CategoryPageView, CategoryCreateView, \
    CategoryUpdateView

app_name = 'admins'

urlpatterns = [
    path('', UserPageView.as_view(), name='index'),
    path('users/', UserListView.as_view(), name='admin_users'),
    path('users-create/', UserCreateView.as_view(), name='admin_users_create'),
    path('users-update/<int:pk>', UserUpdateView.as_view(), name='admin_user_update'),
    path('users-delete/<int:pk>', UserDeleteView.as_view(), name='admin_user_delete'),
    path('product/', ProductPageView.as_view(), name='admin_product'),
    path('product/product-create/', ProductCreateView.as_view(), name='admin_product_create'),
    path('category/', CategoryPageView.as_view(), name='admin_category'),
    path('category/category-create', CategoryCreateView.as_view(), name='admin_category_create'),
    path('category/category-update/<int:pk>/', CategoryUpdateView.as_view(), name='admin_category_update'),
]
