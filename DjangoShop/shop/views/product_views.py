from django.http import (
    HttpRequest,
    HttpResponseBadRequest,
    JsonResponse,
)
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from shop.models.product import Product, Category, CategoryProduct
from shop.serializers.product_serializers import ProductSerializer
from django.db.models import QuerySet
from django.template.defaultfilters import slugify
from shop.mixins.view_mixins.permission_mixin import PermissionMixin


class ProductViewSet(viewsets.ViewSet, PermissionMixin):
    lookup_field = "slug"
    permission_classes_by_action = {
        "list": [IsAuthenticatedOrReadOnly],
        "retrieve": [IsAuthenticatedOrReadOnly],
        "create": [IsAdminUser],
        "update": [IsAdminUser],
        "destroy": [IsAdminUser],
    }

    def list(self, request: HttpRequest):
        if request.method == "GET":
            product_queryset: QuerySet = Product.objects.all()
            serializer: ProductSerializer = ProductSerializer(
                product_queryset, many=True
            )
            return JsonResponse(serializer.data, safe=False)

    def retrieve(self, request: HttpRequest, slug=None):
        if request.method == "GET":
            product: Product = get_object_or_404(Product, slug=slug)
            serializer = ProductSerializer(instance=product)
            return JsonResponse(serializer.data)

    def create(self, request: HttpRequest):
        if request.method == "POST":
            category: Category = get_object_or_404(
                Category, slug=slugify(request.data["category"])
            )
            serializer = ProductSerializer(data=request.data["product"])
            if not serializer.is_valid(raise_exception=True):
                return HttpResponseBadRequest(
                    {
                        "is_valid": serializer.is_valid(raise_exception=True),
                        "errors": serializer.errors,
                    },
                )
            product = serializer.save()
            CategoryProduct.objects.create(product=product, category=category)
            return JsonResponse(serializer.data)

    def update(self, request: HttpRequest, slug=None):
        if request.method == "PUT":
            try:
                product: Product = get_object_or_404(Product, slug=slug)
                serializer = ProductSerializer(
                    data=request.data["product"], instance=product
                )
            except KeyError:
                return HttpResponseBadRequest("bad request")
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(serializer.data, status=200)

    def destroy(self, request: HttpRequest, slug=None):
        if request.method == "DELETE":
            product: Product = get_object_or_404(Product, slug=slug)
            destroyed = product.delete()
            return JsonResponse({"destroyed ": destroyed})

    def get_permissions(self):
        return self.get_permissions_by_action(
            self.permission_classes_by_action, self.action, self.permission_classes
        )
