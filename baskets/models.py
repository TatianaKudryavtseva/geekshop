from django.db import models
from django.utils.functional import cached_property

from users.models import User
from products.models import Product


class BasketQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super(BasketQuerySet, self).delete(*args, **kwargs)


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    def __str__(self):
        return f'Корзиня для {self.user.username} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    def get_summary(self):
        items = self.get_items_cached
        return {
            'total_cost': sum(list(map(lambda x: x.quantity * x.product.price, items))),
            'total_quantity': sum(list(map(lambda x: x.quantity, items)))
    }

#   def total_sum(self):
#        baskets = self.get_items_cached
#        return sum(list(map(lambda x: x.quantity * x.product.price, baskets))),

#    def total_quantity(self):
#        baskets = self.get_items_cached
#        return sum(list(map(lambda x: x.quantity, baskets)))

#    def save(self, *args, **kwargs):
#        if self.pk:
#            self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
#        else:
#            self.product.quantity -= self.quantity
#        self.product.save()
#        super(self.__class__, self).save(*args, **kwargs)
