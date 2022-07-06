from django.http import HttpRequest, JsonResponse
from rest_framework import viewsets
from shop.models.basket import Basket
from shop.serializers.basket_serializer import BasketSerializer
from rest_framework.permissions import IsAuthenticated
from shop.models.product import Product
from django.contrib.auth.models import User
from shop.mixins.view_mixins.permission_mixin import PermissionMixin
from django.db.models import Q


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

    def create(self, request: HttpRequest, slug=None):
        if request.method == "POST":
            try:
                product: Product = Product.objects.get(slug=slug)
                user: User = User.objects.get(pk=request.user.pk)
                basket: Basket = Basket.objects.create(product=product, user=user)
                serializer = BasketSerializer(instance=basket)
                return JsonResponse(serializer.data, status=200)

            except User.DoesNotExist:
                return JsonResponse({"errors": ["user does not exist"]}, status=404)
            except Product.DoesNotExist:
                return JsonResponse({"errors": ["object does not exist"]}, status=404)
            except KeyError:
                return JsonResponse({"errors": ["bad request parameters"]}, status=400)

    def destroy(self, request: HttpRequest, slug=None):
        if request.method == "DELETE":
            try:
                instance: Basket = Basket.objects.get(
                    Q(product__slug=slug) & Q(user__pk=request.user.pk)
                )
                destroyed = instance.delete()
            except Basket.DoesNotExist:
                return JsonResponse({"errors": ["object does not exist"]}, status=404)
            except KeyError:
                return JsonResponse({"errors": ["bad parameters"]}, status=400)
            return JsonResponse({"destroyed ": destroyed}, status=200)

    def get_permissions(self):
        return self.get_permissions_by_action(
            self.permission_classes_by_action, self.action, self.permission_classes
        )
