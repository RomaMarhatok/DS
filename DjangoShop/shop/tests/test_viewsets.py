import json
import pytest
from shop.views.product_views import ProductViewSet
from shop.models.product import (
    Product,
    Category,
    CategoryProduct,
    Attribute,
    CategoryAttribute,
)
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from shop.serializers.product_serializers import ProductSerializer
from django.template.defaultfilters import slugify


class TestProductViewSet:
    """testing base functionality in product viewset"""

    @pytest.mark.django_db
    def test_get_all_products(self, category_fixture, product_fixture):
        factory: APIRequestFactory = APIRequestFactory()
        product: Product = product_fixture
        category: Category = category_fixture
        CategoryProduct.objects.create(product=product, category=category)
        view = ProductViewSet.as_view({"get": "list"})
        req = factory.get(reverse("product-list"))
        res = view(req)
        assert res.status_code == 200
        assert isinstance(res.content, bytes)

    @pytest.mark.django_db
    def test_get_product_by_slug(self, product_fixture):
        factory: APIRequestFactory = APIRequestFactory()
        view = ProductViewSet.as_view({"get": "retrieve"})
        product: Product = product_fixture
        req = factory.get("http://localhost:8000/shop/product/", {"slug": product.slug})
        res = view(req, slug=product.slug)
        assert res.status_code == 200
        assert isinstance(res.content, bytes)

    @pytest.mark.django_db
    def test_create_product(self, category_fixture):
        factory: APIRequestFactory = APIRequestFactory()
        category_fixture
        view = ProductViewSet.as_view({"post": "create"})
        req = factory.post(
            "http://localhost:8000/shop/product/",
            {
                "product": {
                    "name": "HP ProBook 455 G8 45N00ES",
                    "price": 123,
                },
                "category": {"name": "game notebooks"},
            },
            format="json",
        )
        res = view(req)
        assert CategoryProduct.objects.all().count() == 1
        assert res.status_code == 200
        assert isinstance(res.content, bytes)

    @pytest.mark.django_db
    def test_update_product(self, product_fixture, category_fixture):

        # initialization data
        product: Product = product_fixture
        category: Category = category_fixture
        CategoryProduct.objects.create(product=product, category=category)

        # make request
        factory: APIRequestFactory = APIRequestFactory()
        req_body = {"product": {"name": "Haier U1520SD", "price": 999}}
        req = factory.put(
            f"http://localhost:8000/shop/product/{product.slug}",
            req_body,
            format="json",
        )
        view = ProductViewSet.as_view({"put": "update"})
        res = view(req, slug=product.slug)

        # initialization data from asserting
        product: Product = Product.objects.get(
            slug=slugify(req_body["product"]["name"])
        )
        serializer: ProductSerializer = ProductSerializer(product)
        category_from_res = json.loads(res.content)["category_product"][0]["category"]
        category_from_serializer = serializer.data["category_product"][0]["category"]

        # asserting
        assert res.status_code == 200
        assert isinstance(res.content, bytes)
        assert product.name == req_body["product"]["name"]
        assert product.price == req_body["product"]["price"]
        assert category_from_res == category_from_serializer

    @pytest.mark.django_db
    def test_destroy_product(self, product_fixture):
        product: Product = product_fixture
        factory: APIRequestFactory = APIRequestFactory()
        req = factory.delete(f"http://localhost:8000/shop/product/{product.slug}")
        view = ProductViewSet.as_view({"delete": "destroy"})
        res = view(req, slug=product.slug)
        assert res.status_code == 200
        assert isinstance(res.content, bytes)
        assert Product.objects.all().count() == 0

    """test exceptions in viewset"""

    @pytest.mark.django_db
    def test_update_without_req_body(self, product_fixture):
        product: Product = product_fixture
        factory: APIRequestFactory = APIRequestFactory()
        req = factory.put(
            f"http://localhost:8000/shop/product/{product.slug}",
            format="json",
        )
        view = ProductViewSet.as_view({"put": "update"})
        res = view(req, slug=product.slug)
        data = json.loads(res.content)
        assert "errors" in data
        assert data["errors"][0] == "bad parameters"

    @pytest.mark.django_db
    def test_update_with_empty_req_body(self, product_fixture):
        product: Product = product_fixture
        factory: APIRequestFactory = APIRequestFactory()
        view = ProductViewSet.as_view({"put": "update"})
        req = factory.put(
            f"http://localhost:8000/shop/product/{product.slug}",
            {"product": {}},
            format="json",
        )
        res = view(req, slug=product.slug)
        data = json.loads(res.content)
        assert "errors" in data
        assert data["errors"][0] == "empty request body"

    @pytest.mark.django_db
    def test_get_not_exist_product(self):
        factory: APIRequestFactory = APIRequestFactory()
        view = ProductViewSet.as_view({"get": "retrieve"})
        product_slug: str = "not-exist-slug"
        req = factory.get(
            f"http://localhost:8000/shop/product/{product_slug}",
        )
        res = view(req, slug=product_slug)
        data = json.loads(res.content)
        assert "errors" in data
        assert data["errors"][0] == "object does not exist"

    @pytest.mark.django_db
    def test_update_not_exist_product(self):
        factory: APIRequestFactory = APIRequestFactory()
        view = ProductViewSet.as_view({"put": "update"})
        product_slug: str = "not-exist-slug"
        req_body = {"product": {"name": "Haier U1520SD", "price": 999}}

        req = factory.put(
            f"http://localhost:8000/shop/product/{product_slug}",
            req_body,
            format="json",
        )
        res = view(req, slug=product_slug)
        data = json.loads(res.content)
        assert "errors" in data
        assert data["errors"][0] == "object does not exist"
