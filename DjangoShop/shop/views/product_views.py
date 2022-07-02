from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from shop.models.product import Product, Category, CategoryProduct
from shop.serializers.product_serializers import ProductSerializer
from django.db.models import QuerySet
from django.template.defaultfilters import slugify
from ..mixins.view_mixins.permission_mixin import PermissionMixin


class ProductViewSet(viewsets.ViewSet, PermissionMixin):
    lookup_field = "slug"
    permission_classes_by_action = {
        "list": [IsAuthenticatedOrReadOnly],
        "retrieve": [IsAuthenticatedOrReadOnly],
        "create": [IsAdminUser],
        "update": [IsAdminUser],
        "destroy": [IsAdminUser],
    }

    def list(self, request):
        if request.method == "GET":
            product_queryset: QuerySet = Product.objects.all()
            serializer: ProductSerializer = ProductSerializer(
                product_queryset, many=True
            )
            return JsonResponse(serializer.data, safe=False)

    def retrieve(self, request, slug):
        if request.method == "GET":
            try:
                serializer = ProductSerializer(Product.objects.get(slug=slug))
            except Product.DoesNotExist:
                return JsonResponse({"errors": ["object does not exist"]}, status=400)
            return JsonResponse(serializer.data)

    def create(self, request):
        if request.method == "POST":
            try:
                category = Category.objects.get(
                    slug=slugify(request.data["category"]["name"])
                )
            except Category.DoesNotExist:
                return JsonResponse({"errors": ["category doesn't exist"]}, status=400)
            product_data = request.data["product"]
            serializer = ProductSerializer(data=product_data)
            if not serializer.is_valid(raise_exception=True):
                return JsonResponse(
                    {
                        "is_valid": serializer.is_valid(raise_exception=True),
                        "errors": serializer.errors,
                    },
                    status=400,
                )
            product = serializer.save()
            CategoryProduct.objects.create(product=product, category=category)
            return JsonResponse(serializer.data)

    def update(self, request, slug=None):
        if request.method == "PUT":
            try:
                if not request.data["product"]:
                    return JsonResponse({"errors": ["empty request body"]}, status=400)
                product: Product = Product.objects.get(slug=slug)
                serializer = ProductSerializer(
                    data=request.data["product"], instance=product
                )
            except Product.DoesNotExist:
                return JsonResponse({"errors": ["object does not exist"]}, status=400)
            except KeyError:
                return JsonResponse({"errors": ["bad parameters"]}, status=400)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(serializer.data)

    def destroy(self, request, slug=None):
        if request.method == "DELETE":
            try:
                destroyed = Product.objects.get(slug=slug).delete()
            except Product.DoesNotExist:
                return JsonResponse({"errors": ["object does not exist"]}, status=400)
            return JsonResponse({"destroyed ": destroyed})

    def get_permissions(self):
        return self.get_permissions_by_action(
            self.permission_classes_by_action, self.action, self.permission_classes
        )
