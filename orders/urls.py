from django.urls import path
from django.views.decorators.cache import cache_page

from orders.views import OrderList, OrderCreate, OrderUpdate, OrderDelete, OrderRead, order_forming_complete, \
    get_product_price

app_name = 'orders'

urlpatterns = [
    path('', cache_page(3600)(OrderList.as_view()), name='orders_list'),
    path('forming/complete/<int:pk>', order_forming_complete, name='order_forming_complete'),
    path('create/', cache_page(3600)(OrderCreate.as_view()), name='order_create'),
    path('read/<int:pk>', cache_page(3600)(OrderRead.as_view()), name='order_read'),
    path('update/<int:pk>', cache_page(3600)(OrderUpdate.as_view()), name='order_update'),
    path('delete/<int:pk>', cache_page(3600)(OrderDelete.as_view()), name='order_delete'),
    path('product/<int:pk>/price/', get_product_price)
    ]
