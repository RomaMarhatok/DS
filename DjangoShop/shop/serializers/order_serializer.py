from rest_framework import serializers
from shop.models.order import Order


class OrderSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        depth = 1
