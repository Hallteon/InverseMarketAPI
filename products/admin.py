from django.contrib import admin
from products.models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'category', 'shop', 'calories', 'protein', 'fats', 'carbohydrates', 'weight', 'start_price', 'current_price', 'amount', 'compound', 'expiration', 'cover')
    search_fields = ('id', 'name', 'amount')
    list_filter = ('name', 'amount', 'category', 'shop')


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'cover')
    search_fields = ('id', 'name', 'category')
    list_filter = ('name', 'category')


class ShopCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(ShopCategory, ShopCategoryAdmin)