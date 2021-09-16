from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from common.view import CommonContextMixin
from products.models import Product, ProductCategory


class IndexView(CommonContextMixin, TemplateView):
    title = 'GeekShop'
    template_name = 'products/index.html'
    paginate_by = 3


class ProductsListView(CommonContextMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    title = 'GeekShop - Каталог'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        return context
