from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path("", views.OrderListCreateAPIView.as_view(), name="order_list_create"),
    path("<uuid:uuid>/", views.OrderDetailAPIView.as_view(), name="order_detail"),
    path("<uuid:uuid>/update/", views.OrderUpdateAPIView.as_view(), name="order_update"),
    path("<uuid:uuid>/update/quantity/", views.OrderQuantityUpdateAPIView.as_view(), name="order_quantity_update"),
]
