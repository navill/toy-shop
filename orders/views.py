from rest_framework.permissions import IsAuthenticated

from commons.permissions import IsOwner
from commons.views import generics
from orders.exceptions import OrderExceptions
from orders.models import Order, ProductOrder, OrderStatus
from orders.serializers.request_serializers import OrderCreateRequestSerializer, ProductOrderUpdateRequestSerializer, \
    OrderUpdateRequestSerializer
from orders.serializers.response_serializers import OrderResponseSerializer, ProductOrderUpdateResponseSerializer


class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.prefetch_related("product_order_set")
    request_serializer_class = OrderCreateRequestSerializer
    response_serializer_class = OrderResponseSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.prefetch_related("product_order_set")
    response_serializer_class = OrderResponseSerializer
    permission_classes = [IsOwner]
    lookup_field = "uuid"


class OrderUpdateAPIView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateRequestSerializer
    permission_classes = [IsOwner]
    lookup_field = "uuid"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if obj.status < OrderStatus.SHIPPING:
            return obj
        else:
            raise OrderExceptions.OrderException(detail=f"{obj.get_status_display()} - 수정 불가 상태")


class OrderQuantityUpdateAPIView(generics.UpdateAPIView):
    queryset = ProductOrder.objects.all()
    request_serializer_class = ProductOrderUpdateRequestSerializer
    response_serializer_class = ProductOrderUpdateResponseSerializer

    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"

    def get_queryset(self):
        return super().get_queryset().filter(order__user=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if obj.order.status < OrderStatus.PAID:
            return obj
        else:
            raise OrderExceptions.OrderException(detail=f"{obj.get_status_display()} - 수정 불가 상태")
