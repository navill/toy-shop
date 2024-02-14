from django.urls import path

from items import views

app_name = 'items'

category_patterns = [
    path("categories/", views.CategoryCreateListAPIView.as_view(), name="category_list_create"),
    path("categories/<int:pk>/update_name/", views.CategoryNameUpdateAPIView.as_view(), name="category_update_name"),
    path("categories/<int:pk>/update_position/", views.CategoryPositionUpdateAPIView.as_view(),
         name="category_update_position"),
    path("categories/<int:pk>/delete/", views.CategoryDeleteAPIView.as_view(), name="category_delete"),
]

product_patterns = [
    path("products/", views.ProductCreateListAPIView.as_view(), name="product_list_create"),
    path("products/<int:pk>/", views.ProductDetailAPIView.as_view(), name="product_detail"),
    path("products/<int:pk>/update/", views.ProductUpdateAPIView.as_view(), name="product_update"),
]

urlpatterns = product_patterns + category_patterns
