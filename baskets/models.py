from django.db import models

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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Корзиня для {self.user.username} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    def total_sum(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.sum() for basket in baskets)

    def total_quantity(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.quantity for basket in baskets)

#    def save(self, *args, **kwargs):
#        if self.pk:
#            self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
#        else:
#            self.product.quantity -= self.quantity
#        self.product.save()
#        super(self.__class__, self).save(*args, **kwargs)
