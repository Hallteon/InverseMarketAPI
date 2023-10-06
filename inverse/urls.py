"""
URL configuration for HelloDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include, re_path
from inverse.settings import MEDIA_ROOT, MEDIA_URL
from django.contrib import admin
from rest_framework import routers
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from users.views import *
from products.views import *
from orders.views import *


schema_view = get_schema_view(
   openapi.Info(
      title='Inverse Market API',
      default_version='v1',
      description='Платформа корпоративного питания на основе кейтерингов',
      terms_of_service='https://www.google.com/policies/terms/',
      contact=openapi.Contact(email='belogurov.ivan@list.ru'),
      license=openapi.License(name='BSD License'),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Products 
    path('api/products/create/', ProductAPICreateView.as_view()),
    path('api/products/', ProductAPIListView.as_view()),
    path('api/products/filter/', ProductAPIFilterListView.as_view()),
    path('api/products/<int:pk>/', ProductAPIDetailView.as_view()),
    path('api/products/shops/<int:pk>/', ProductAPIShopListView.as_view()),
    path('api/products/<int:pk>/add_to_basket/', ProductAPIAddToBasketView.as_view()),
    path('api/products/shops/', ShopAPIListView.as_view()),
    path('api/products/categories/', ProductCategoryAPIListView.as_view()),
    path('api/products/categories/<int:pk>/', ProductAPICategoryListView.as_view()),
    path('api/products/generate/', generate_product),

    # Orders
    path('api/orders/create/', OrderAPICreateView.as_view()),
    path('api/orders/my/', OrderAPIListView.as_view()),
    path('api/orders/<int:pk>/', OrderAPIDetailView.as_view()),
    path('api/orders/', OrderAPIDetailView.as_view()),
    path('api/orders/products/create/', OrderProductAPICreateView.as_view()),
    path('api/orders/statuses/', OrderStatusAPIListView.as_view()),

    # Users
    path('api/users/organizations/', OrganizationAPIListView.as_view()),
    path('api/users/roles/', RoleAPIListView.as_view()),
    path('api/users/auth/', include('djoser.urls')),
    re_path(r'^api/users/auth/', include('djoser.urls.authtoken')),

    # Swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)