import pytest
from typing import OrderedDict
from shop.serializers.product_serializers import (
    ProductSerializer,
    CategoryProductSerailizer,
    CategoryAttributeSerializer,
    AttributeSerializer,
    CategorySerializer,
)
from shop.models.product import (
    Product,
    Category,
    CategoryProduct,
    Attribute,
    CategoryAttribute,
)


class TestProductSerializer:
    @pytest.mark.django_db
    def test_product_serializer_from_json(self, faker_product_fixture):
        data: dict = faker_product_fixture
        serializer: ProductSerializer = ProductSerializer(data=data)
        serializer.is_valid()
        assert serializer.errors == {}
        assert "slug" in serializer.data
        assert "name" in serializer.data

    @pytest.mark.django_db
    def test_product_serializer_from_object(self, product_fixture, category_fixture):
        product: Product = product_fixture
        serializer: ProductSerializer = ProductSerializer(product)
        category: Category = category_fixture
        CategoryProduct.objects.create(product=product, category=category)
        assert "attributes" in serializer.data
        assert "category_product" in serializer.data
        assert isinstance(serializer.data["category_product"], list)
        assert isinstance(serializer.data["attributes"], list)


class TestCategoryProductSerializer:
    @pytest.mark.django_db
    def test_category_product_serializer(self, category_porduct_fixture):
        category_product: CategoryProduct = category_porduct_fixture
        serializer: CategoryProductSerailizer = CategoryProductSerailizer(
            instance=category_product
        )
        assert "product" in serializer.data
        assert "category" in serializer.data
        assert isinstance(serializer.data["category"], OrderedDict)
        assert isinstance(serializer.data["product"], OrderedDict)


class TestCategoryAttributeSerializer:
    @pytest.mark.django_db
    def test_category_attribute_serializer(self, category_fixture, attribute_fixture):
        category: Category = category_fixture
        attribute: Attribute = attribute_fixture
        category_attribute: CategoryAttribute = CategoryAttribute.objects.create(
            category=category, attribute=attribute
        )
        serializer: CategoryAttributeSerializer = CategoryAttributeSerializer(
            instance=category_attribute
        )
        assert "category" in serializer.data
        assert "attribute" in serializer.data
        assert isinstance(serializer.data["category"], OrderedDict)
        assert isinstance(serializer.data["attribute"], OrderedDict)


class TestAttributeSerializer:
    @pytest.mark.django_db
    def test_attribute_foreign_keys(self, attribute_fixture):
        attribute: Attribute = attribute_fixture
        serializer: AttributeSerializer = AttributeSerializer(instance=attribute)
        assert "product" in serializer.data
        assert isinstance(serializer.data["product"], OrderedDict)


class TestCategorySerializer:
    @pytest.mark.django_db
    def test_category_unique_value(self, category_fixture):
        category: Category = category_fixture
        serializer: CategorySerializer = CategorySerializer(instance=category)
        assert "slug" in serializer.data
        assert "name" in serializer.data
        assert "category_product" in serializer.data
        assert isinstance(serializer.data["category_product"], list)
