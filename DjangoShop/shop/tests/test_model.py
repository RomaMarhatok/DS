import pytest
from shop.models.product import Product, Category, CategoryProduct, Attribute
from django.db.models.query import QuerySet


class TestProduct:
    @pytest.mark.django_db
    def test_product_save(self, product_fixture):
        product = product_fixture
        assert Product.objects.all().count() == 1
        assert product.slug == "asus-tuf-gaming"

    @pytest.mark.django_db
    def test_related_name(self, product_fixture, category_fixture):
        product = product_fixture
        category1 = category_fixture
        category2 = category_fixture
        CategoryProduct.objects.create(product=product, category=category1)
        CategoryProduct.objects.create(product=product, category=category2)
        assert isinstance(product.category_product.all(), QuerySet)


class TestCategory:
    @pytest.mark.django_db
    def test_category_save(self, category_fixture):
        category = category_fixture
        assert Category.objects.all().count() == 1
        assert category.slug == "game-notebooks"

    @pytest.mark.django_db
    def test_related_name(self, product_fixture, category_fixture):
        product1 = product_fixture
        product2 = product_fixture
        category = category_fixture
        CategoryProduct.objects.create(product=product1, category=category)
        CategoryProduct.objects.create(product=product2, category=category)
        assert isinstance(category.category_product.all(), QuerySet)


class TestAttribute:
    @pytest.mark.django_db
    def test_related_name(self, attribute_fixture):
        attribute: Attribute = attribute_fixture
        product: Product = attribute.product
        assert isinstance(product.attributes.all(), QuerySet)
