from django.urls import path
from django.views.decorators.cache import cache_page
from products.views import ProductsListView

app_name = 'products'

urlpatterns = [
    path('', cache_page(3600)(ProductsListView.as_view()), name='product'),
    path('<int:category_id>/', cache_page(3600)(ProductsListView.as_view()), name='category'),
    path('page/<int:page>', cache_page(3600)(ProductsListView.as_view()), name='page')
]