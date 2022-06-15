from rest_framework import serializers
from shop.models.product import (
    Product,
    Category,
    Attribute,
    CategoryAttribute,
    CategoryProduct,
)
from django.template.defaultfilters import slugify


class CategoryProductSerailizer(serializers.ModelSerializer):
    class Meta:
        model = CategoryProduct
        fields = "__all__"
        depth = 1


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = "__all__"
        depth = 1


class CategorySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        if (
            "data" in kwargs
            and "name" in kwargs["data"]
            and "slug" not in kwargs["data"]
        ):
            kwargs["data"].update({"slug": slugify(kwargs["data"]["name"])})
        super().__init__(*args, **kwargs)

    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category_product = CategoryProductSerailizer(many=True, required=False)
    attributes = AttributeSerializer(many=True, read_only=True)

    def __init__(self, *args, **kwargs):
        if (
            "data" in kwargs
            and "name" in kwargs["data"]
            and "slug" not in kwargs["data"]
        ):
            kwargs["data"].update({"slug": slugify(kwargs["data"]["name"])})
        super().__init__(*args, **kwargs)

    class Meta:
        model = Product
        fields = ["name", "slug", "price", "category_product", "attributes"]


class CategoryAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryAttribute
        fields = "__all__"
        depth = 1
