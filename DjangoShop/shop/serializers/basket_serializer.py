from rest_framework import serializers
from shop.models.basket import Basket


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = "__all__"
        depth = 1
