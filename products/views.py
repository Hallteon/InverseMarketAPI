import json
import requests
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from users.permissions import *
from users.serializers import UserRegistrationSerializer
from products.permissions import *
from products.serializers import *
from products.models import *


class ProductAPICreateView(generics.CreateAPIView):
    serializer_class = ProductWriteSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class ProductAPIListView(generics.ListAPIView):
    serializer_class = ProductReadListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(shop__organizations_shop__in=[self.request.user.organization.pk], amount__gt=0)
    

class ProductAPIShopListView(generics.ListAPIView):
    serializer_class = ProductReadListSerializer
    permission_classes = [IsAuthenticated, IsUserShop]

    def get_queryset(self):
        return Product.objects.filter(shop__pk=self.kwargs['pk'], shop__organizations_shop__in=[self.request.user.organization.pk])


class ProductAPICategoryListView(generics.ListAPIView):
    serializer_class = ProductReadListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs['pk'], shop__organizations_shop__in=[self.request.user.organization.pk])


class ProductAPIFilterListView(generics.ListAPIView):
    serializer_class = ProductReadListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        products = Product.objects
        shop = self.request.GET.get('shop', None)
        categories = self.request.GET.get('categories', None)

        if shop:
            products = products.filter(shop=shop)

        if categories:
            categories = categories.split(',')
            products = products.filter(category__in=categories)

        return products
    

class ProductAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWriteSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if self.kwargs['pk']:
            product = Product.objects.get(pk=self.kwargs['pk'])
            serializer = ProductReadDetailSerializer(product)
                
            return Response(serializer.data)
    

class ProductAPIAddToBasketView(generics.UpdateAPIView):
    serializer_class = ProductReadDetailSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        obj = get_object_or_404(Product.objects.all(), pk=self.kwargs['pk'])
        user = self.request.user

        user.basket.add(obj.pk)
        
        user.save()
        obj.save()

        serializer = ProductReadDetailSerializer(obj, required=False)

        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)


class ProductCategoryAPIListView(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAuthenticated]


class ShopAPIListView(generics.ListAPIView):
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Shop.objects.filter(organizations_shop__in=[self.request.user.organization.pk])
    

@api_view(['POST'])
def generate_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name', None)
        description = data.get('description', None)
        category = data.get('category', None)
        shop = data.get('shop', None)
        weight = data.get('weight', None)
        price = data.get('price', None)
        amount = data.get('amount', None)
        compound = data.get('compound', None)
        calories = data.get('calories', None)
        fats = data.get('fats', None)
        protein = data.get('protein', None)
        carbohydrates = data.get('carbohydrates', None)
        cover = data.get('cover', None)

        if not Product.objects.filter(name=name).exists():
            if not ProductCategory.objects.filter(name=category).exists():
                ProductCategory.objects.create(name=category).save()

            if not Shop.objects.filter(name=shop).exists():
                Shop.objects.create(name=shop, category=ShopCategory.objects.get(pk=1)).save()

            product = Product(name=name, description=description, weight=weight,
                              current_price=price, start_price=price, amount=amount, 
                              compound=compound, calories=calories, fats=fats,
                              protein=protein, carbohydrates=carbohydrates)
            
            product.shop = Shop.objects.filter(name=shop)[0]
            product.category = ProductCategory.objects.filter(name=category)[0]
            
            if cover:
                image = requests.get(cover)
                image_data = ContentFile(image.content)
                image_name = str(uuid.uuid4())
                product.cover.save(f'{image_name}.jpg', image_data, save=True)

            product.save()

        return Response({'message': 'Events were generated', 'data': request.data})

    return Response({'message': 'Error'}) 