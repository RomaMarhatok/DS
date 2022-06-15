import pytest
from shop.models.product import Product, Category


class TestProduct:
    @pytest.mark.django_db
    def test_product_save(self, product_fixture):
        product = product_fixture
        assert Product.objects.all().count() == 1
        assert product.slug == "asus-tuf-gaming"


class TestCategory:
    @pytest.mark.django_db
    def test_category_save(self, category_fixture):
        category = category_fixture
        assert Category.objects.all().count() == 1
        assert category.slug == "game-notebooks"
