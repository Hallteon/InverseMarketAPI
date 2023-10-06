from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from products.models import *
from orders.models import *
from orders.serializers import *
from orders.permissions import *


class OrderAPICreateView(generics.CreateAPIView):
    serializer_class = OrderWriteSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = OrderWriteSerializer(data=request.data)

        if serializer.is_valid():
            user = self.request.user
            
            try:
                total_price = serializer.validated_data['delivery_price']
            
            except:
                total_price = 0

            total_weight = 0
            products = []

            for order_product in serializer.validated_data['order_products']:
                total_price += order_product.product.current_price * order_product.amount
                total_weight += order_product.product.weight * order_product.amount
                product = order_product.product
                
                if product.amount - order_product.amount >= 0:
                    products.append(order_product)

                else:
                    return Response({'errors': 'There is no such amount of products!'}, status=status.HTTP_400_BAD_REQUEST)
                
            for order_product in products:
                order_product.product.amount -= order_product.amount
                order_product.product.save()

            serializer.save()
            
            order = Order.objects.get(pk=serializer.validated_data['pk']) 

            order.total_price = total_price
            order.total_weight = total_weight
            order.status = OrderStatus.objects.get(status_type='order_processed')
            order.save()
            
            user.orders.add(order.pk)
            user.basket.remove(*[order_product.product.pk for order_product in order.order_products.all()])
            user.save()

            return Response(OrderReadSerializer(order).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderAPIListView(generics.ListAPIView):
    serializer_class = OrderReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.orders.all()
    

class OrderAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderWriteSerializer
    permission_classes = [IsAuthenticated, IsUserOrder]

    def get(self, request, *args, **kwargs):
        if self.kwargs['pk']:
            order = Order.objects.get(pk=self.kwargs['pk'])
            serializer = OrderReadSerializer(order)
                
            return Response(serializer.data)


class OrderProductAPICreateView(generics.CreateAPIView):
    serializer_class = OrderProductWriteSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = OrderProductWriteSerializer(data=request.data)

        if serializer.is_valid():
            product_amount = serializer.validated_data['product'].amount
            order_product_amount = serializer.validated_data['amount']
                
            if product_amount - order_product_amount >= 0:
                serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            else:
                return Response({'errors': 'There is no such amount of products!'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderStatusAPIListView(generics.ListAPIView):
    queryset = OrderStatus.objects.all()
    serializer_class = OrderStatusSerializer
    permission_classes = [IsAuthenticated]
