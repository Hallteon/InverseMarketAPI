from rest_framework import permissions
from products.models import *


class IsUserShop(permissions.BasePermission):
    def has_permission(self, request, view):
        return  Shop.objects.get(pk=view.kwargs['pk']) in request.user.organization.shops.all()