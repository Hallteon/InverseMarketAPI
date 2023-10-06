from rest_framework import permissions
from orders.models import *


class IsUserOrder(permissions.BasePermission):
    def has_object_permission(self, request, view):
        return Order.objects.get(pk=view.kwargs['pk']) in request.user.orders.all()