from django.http import JsonResponse
from rest_framework import viewsets
from shop.models.product import Product, Category, CategoryProduct
from shop.serializers.product_serializers import ProductSerializer, CategorySerializer
from django.db.models import QuerySet
from django.template.defaultfilters import slugify


class ProductViewSet(viewsets.ViewSet):
    lookup_field = "slug"

    def list(self, request):
        if request.method == "GET":
            product_queryset: QuerySet = Product.objects.all()
            serializer: ProductSerializer = ProductSerializer(
                product_queryset, many=True
            )
            return JsonResponse(serializer.data, safe=False)

    def retrieve(self, request, slug):
        if request.method == "GET":
            serializer = ProductSerializer(Product.objects.get(slug=slug))
            return JsonResponse(serializer.data)

    def create(self, request):
        if request.method == "POST":
            try:
                category = Category.objects.get(
                    slug=slugify(request.data["category"]["name"])
                )
            except Category.DoesNotExist:
                return JsonResponse({"errors": ["category doesn't exist"]})
            product_data = request.data["product"]
            serializer = ProductSerializer(data=product_data)
            if not serializer.is_valid(raise_exception=True):
                return JsonResponse(
                    {
                        "is_valid": serializer.is_valid(raise_exception=True),
                        "errors": serializer.errors,
                    }
                )
            product = serializer.save()
            CategoryProduct.objects.create(product=product, category=category)
            return JsonResponse(serializer.data)

    def update(self, request, slug=None):
        if request.method == "PUT":
            try:
                product: Product = Product.objects.get(slug=slug)
                serializer = ProductSerializer(
                    data=request.data["product"], instance=product
                )
            except KeyError:
                return JsonResponse({"errors": ["bad parameters"]})
            if not request.data["product"]:
                return JsonResponse({"errors": ["empty request body"]})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(serializer.data)

    def destroy(self, request, slug=None):
        if request.method == "DELETE":
            instance = Product.objects.get(slug=slug).delete()
            return JsonResponse({"destroed": instance})
