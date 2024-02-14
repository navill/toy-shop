from commons.views import generics
from items.models import Category, Product
from items.serializers.request_serializer import CategoryCreateRequestSerializer, ProductCreateRequestSerializer
from items.serializers.response_serializer import CategoryListResponseSerializer, ProductResponseSerializer
from items.serializers.serializers import ProductUpdateSerializer, CategoryPositionUpdateSerializer, \
    CategoryNameUpdateSerializer


class CategoryCreateListAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    request_serializer_class = CategoryCreateRequestSerializer
    response_serializer_class = CategoryListResponseSerializer

    def get_queryset(self):
        return super().get_queryset().get_cached_trees()


class CategoryNameUpdateAPIView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryNameUpdateSerializer
    lookup_field = "pk"


class CategoryPositionUpdateAPIView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryPositionUpdateSerializer
    lookup_field = "pk"


class CategoryDeleteAPIView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    lookup_field = "pk"


class ProductCreateListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    request_serializer_class = ProductCreateRequestSerializer
    response_serializer_class = ProductResponseSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    response_serializer_class = ProductResponseSerializer
    lookup_field = "pk"


class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductUpdateSerializer
    lookup_field = "pk"

# @extend_schema(exclude=True)
# @api_view(["GET"])
# @permission_classes([AllowAny])
# def test_api_view(request, *args, **kwargs):
#     product = Product.objects.last()
#     product.decrease_quantity(2)
#     return Response({"message": "ok"})
