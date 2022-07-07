from django.http import (
    HttpRequest,
    HttpResponseBadRequest,
    JsonResponse,
)
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from shop.models.basket import Basket
from shop.serializers.basket_serializer import BasketSerializer
from rest_framework.permissions import IsAuthenticated
from shop.models.product import Product
from django.contrib.auth.models import User
from shop.mixins.view_mixins.permission_mixin import PermissionMixin
from django.db.models import Q
from django.template.defaultfilters import slugify


class IventoryViewSet(viewsets.ViewSet, PermissionMixin):
    lookup_field = "slug"

    permission_classes_by_action = {
        "list": [IsAuthenticated],
        "create": [IsAuthenticated],
        "destroy": [IsAuthenticated],
    }

    def list(self, request: HttpRequest):
        if request.method == "GET":
            baskets_queryset = Basket.objects.filter(user__pk=request.user.pk).all()
            serializer = BasketSerializer(baskets_queryset, many=True)
            return JsonResponse(serializer.data, safe=False)

    def create(self, request: HttpRequest):
        if request.method == "POST":
            try:
                product = get_object_or_404(Product, slug=slugify(request.data["name"]))
                user: User = get_object_or_404(User, pk=request.user.pk)
                basket: Basket = Basket.objects.create(product=product, user=user)
                serializer = BasketSerializer(instance=basket)
                return JsonResponse(serializer.data["product"], status=200)
            except KeyError:
                return HttpResponseBadRequest()

    def destroy(self, request: HttpRequest, slug=None):
        if request.method == "DELETE":
            try:
                basket: Basket = get_object_or_404(
                    Basket, product__slug=slug, user__pk=request.user.pk
                )
                destroyed = basket.delete()
            except KeyError:
                return HttpResponseBadRequest()
            return JsonResponse({"destroyed ": destroyed}, status=200)

    def get_permissions(self):
        return self.get_permissions_by_action(
            self.permission_classes_by_action, self.action, self.permission_classes
        )
