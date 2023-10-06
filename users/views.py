from django.shortcuts import render
from rest_framework.permissions import *
from rest_framework import generics
from users.serializers import *
from users.models import *
    

class RoleAPIListView(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class OrganizationAPIListView(generics.ListAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
 