import datetime
from django.db import models
from products.models import Product


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_products_product', verbose_name='Товар')
    amount = models.IntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f'{self.product.name} - {self.amount} шт.'

    class Meta:
        verbose_name = 'Товар из заказа'
        verbose_name_plural = 'Товары из заказов'


class OrderStatus(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    status_type = models.CharField(max_length=256, verbose_name='Тип статуса')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'


class Order(models.Model):
    order_products = models.ManyToManyField('OrderProduct', blank=True, related_name='orders_order_product', verbose_name='Товары')
    order_datetime = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Время создания заказа')
    delivery_time = models.TimeField(default=datetime.datetime.now().time(), verbose_name='Время доставки')
    delivery_price = models.IntegerField(default=0, verbose_name='Цена доставки')
    delivery_address = models.TextField(default='', verbose_name='Адрес доставки')
    total_price = models.IntegerField(default=0, verbose_name='Итоговая цена')
    total_weight = models.IntegerField(default=0, verbose_name='Суммарный вес')
    fast = models.BooleanField(default=False, verbose_name='Моментальная доставка')
    status = models.ForeignKey('OrderStatus', blank=True, null=True, on_delete=models.CASCADE, related_name='orders_order_status', verbose_name='Статус')
    need_change = models.BooleanField(default=False, verbose_name='Нужен размен')
    

    def __str__(self):
        return f'{self.delivery_time} - {self.total_price} руб. - {self.status}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'