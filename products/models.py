import uuid
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver


class ShopCategory(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория магазина'
        verbose_name_plural = 'Категории магазинов'


class Shop(models.Model):
    def get_path(instance, filename):
        extension = filename.split('.')[-1]
        image_uuid = uuid.uuid1().hex
        return f'products/shops/covers/{image_uuid}.{extension}'

    cover = models.ImageField(blank=True, null=True, upload_to=get_path, verbose_name='Обложка')
    name = models.CharField(max_length=256, verbose_name='Название')
    category = models.ForeignKey('ShopCategory', on_delete=models.CASCADE, related_name='shops_category', verbose_name='Категория')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'


class ProductCategory(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    def get_path(instance, filename):
        extension = filename.split('.')[-1]
        image_uuid = uuid.uuid1().hex
        return f'products/covers/{image_uuid}.{extension}'

    cover = models.ImageField(blank=True, null=True, upload_to=get_path, verbose_name='Обложка')
    name = models.CharField(max_length=512, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    category = models.ForeignKey('ProductCategory', blank=True, null=True, on_delete=models.CASCADE, related_name='products_category', verbose_name='Категория')
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, related_name='products_shop', verbose_name='Магазин')
    compound = models.TextField(blank=True, verbose_name='Состав')
    calories = models.FloatField(default=0, verbose_name='Калории')
    protein = models.FloatField(default=0, verbose_name='Протеин')
    fats = models.FloatField(default=0, verbose_name='Жиры')
    carbohydrates = models.FloatField(default=0, verbose_name='Углеводы')
    weight = models.IntegerField(default=0, verbose_name='Вес (в граммах)')
    start_price = models.IntegerField(default=0, verbose_name='Начальная цена')
    current_price = models.IntegerField(default=0, verbose_name='Текущая цена')
    amount = models.IntegerField(default=0, verbose_name='Количество')
    expiration = models.TextField(default='', verbose_name='Срок годности / условия хранения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


@receiver(pre_delete, sender=Product)
def event_model_delete(sender, instance, **kwargs):
    if instance.cover:
        instance.cover.delete(False)
