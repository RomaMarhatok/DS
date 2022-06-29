import json
import pytest
from shop.views.product_views import ProductViewSet
from shop.models.product import (
    Product,
    CategoryProduct,
)
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from shop.serializers.product_serializers import ProductSerializer
from django.template.defaultfilters import slugify

factory: APIRequestFactory = APIRequestFactory()


REQUEST_DICT = {
    "GET": factory.get,
    "POST": factory.post,
    "PUT": factory.put,
    "DELETE": factory.delete,
}


def make_request_factory(method=None, url=None, data=None, format="json", **kwargs):
    if method == "GET" or method == "DELETE":
        return REQUEST_DICT[method](url, kwargs, format=format)
    else:
        return REQUEST_DICT[method](url, data, format=format)


@pytest.mark.django_db
def test_get_all_products():
    view = ProductViewSet.as_view({"get": "list"})
    req = make_request_factory(method="GET", url="http://localhost:8000/shop/product/")
    res = view(req)

    assert res.status_code == 200
    assert isinstance(json.loads(res.content), list)


@pytest.mark.django_db
def test_get_product_by_slug(product_fixture: Product):
    view = ProductViewSet.as_view({"get": "retrieve"})
    product: Product = product_fixture
    req = make_request_factory(
        method="GET",
        url=f"http://localhost:8000/shop/product/{product.slug}",
    )
    res = view(req, slug=product.slug)

    assert res.status_code == 200
    assert isinstance(json.loads(res.content), dict)


@pytest.mark.django_db
def test_create_product(admin_user_fixture, category_fixture):
    view = ProductViewSet.as_view({"post": "create"})
    req_body = {
        "product": {
            "name": "HP ProBook 455 G8 45N00ES",
            "price": 123,
        },
        "category": {"name": "game notebooks"},
    }
    req = make_request_factory(
        method="POST",
        url="http://localhost:8000/shop/product/",
        data=req_body,
        format="json",
    )
    req.user = admin_user_fixture
    res = view(req)

    assert CategoryProduct.objects.all().count() == 1
    assert Product.objects.all().count() == 1
    assert res.status_code == 200


@pytest.mark.django_db
def test_update_product(category_porduct_fixture, admin_user_fixture):

    category_product: CategoryProduct = category_porduct_fixture

    req_body = {"product": {"name": "Haier U1520SD", "price": 999}}
    req = make_request_factory(
        method="PUT",
        url=f"http://localhost:8000/shop/product/{category_product.product.slug}",
        data=req_body,
        format="json",
    )
    req.user = admin_user_fixture
    view = ProductViewSet.as_view({"put": "update"})
    res = view(req, slug=category_product.product.slug)

    # initialization data from request for asserting

    product: Product = Product.objects.get(slug=slugify(req_body["product"]["name"]))
    serializer: ProductSerializer = ProductSerializer(product)
    category_from_serializer = serializer.data["category_product"][0]["category"]

    # initialization data from response for asserting

    data = json.loads(res.content)
    category_from_res = data["category_product"][0]["category"]

    assert res.status_code == 200
    assert product.name == req_body["product"]["name"]
    assert product.price == req_body["product"]["price"]
    assert category_from_res == category_from_serializer


@pytest.mark.django_db
def test_destroy_product(product_fixture, admin_user_fixture):
    product: Product = product_fixture
    req = make_request_factory(
        method="DELETE", url=f"http://localhost:8000/shop/product/{product.slug}"
    )
    req.user = admin_user_fixture
    view = ProductViewSet.as_view({"delete": "destroy"})
    res = view(req, slug=product.slug)
    assert res.status_code == 200
    assert Product.objects.all().count() == 0


@pytest.mark.django_db
def test_update_without_req_body(product_fixture, admin_user_fixture):
    product: Product = product_fixture
    req = make_request_factory(
        method="PUT",
        url=f"http://localhost:8000/shop/product/{product.slug}",
        format="json",
    )
    req.user = admin_user_fixture
    view = ProductViewSet.as_view({"put": "update"})
    res = view(req, slug=product.slug)
    data = json.loads(res.content)

    assert res.status_code == 400
    assert "errors" in data
    assert data["errors"][0] == "bad parameters"


@pytest.mark.django_db
def test_update_with_empty_req_body(product_fixture, admin_user_fixture):
    """"""
    product: Product = product_fixture
    view = ProductViewSet.as_view({"put": "update"})
    req = make_request_factory(
        method="PUT",
        url=f"http://localhost:8000/shop/product/{product.slug}",
        data={"product": {}},
        format="json",
    )
    req.user = admin_user_fixture
    res = view(req, slug=product.slug)
    data = json.loads(res.content)

    assert res.status_code == 400
    assert "errors" in data
    assert data["errors"][0] == "empty request body"


@pytest.mark.django_db
def test_get_not_exist_product():
    view = ProductViewSet.as_view({"get": "retrieve"})
    product_slug: str = "not-exist-slug"
    req = make_request_factory(
        method="GET", url=f"http://localhost:8000/shop/product/{product_slug}"
    )
    res = view(req, slug=product_slug)
    data = json.loads(res.content)

    assert res.status_code == 400
    assert "errors" in data
    assert data["errors"][0] == "object does not exist"


@pytest.mark.django_db
def test_update_not_exist_product(admin_user_fixture):
    view = ProductViewSet.as_view({"put": "update"})
    product_slug: str = "not-exist-slug"
    req_body = {"product": {"name": "Haier U1520SD", "price": 999}}

    req = make_request_factory(
        method="PUT",
        url=f"http://localhost:8000/shop/product/{product_slug}",
        data=req_body,
        format="json",
    )
    req.user = admin_user_fixture
    res = view(req, slug=product_slug)
    data = json.loads(res.content)

    assert res.status_code == 400
    assert "errors" in data
    assert data["errors"][0] == "object does not exist"


class TestApiWithoutPermission:
    @pytest.mark.django_db
    def test_put(self, product_fixture):
        product: Product = product_fixture
        view = ProductViewSet.as_view({"put": "update"})
        req_body = {"product": {"name": "Haier U1520SD", "price": 999}}
        req = make_request_factory(
            method="PUT",
            url=f"http://localhost:8000/shop/product/{product.slug}",
            data=req_body,
            format="json",
        )
        res = view(req, slug=product.slug)
        assert res.status_code == 403

    @pytest.mark.django_db
    def test_delete(self, product_fixture):
        product: Product = product_fixture
        view = ProductViewSet.as_view({"delete": "destroy"})
        req = make_request_factory(
            method="DELETE", url=f"http://localhost:8000/shop/product/{product.slug}"
        )
        res = view(req, slug=product.slug)
        assert res.status_code == 403

    @pytest.mark.django_db
    def test_post(self, product_fixture):
        product: Product = product_fixture
        view = ProductViewSet.as_view({"post": "create"})
        req_body = {
            "product": {
                "name": "HP ProBook 455 G8 45N00ES",
                "price": 123,
            },
            "category": {"name": "game notebooks"},
        }
        req = make_request_factory(
            method="POST",
            url="http://localhost:8000/shop/product/",
            data=req_body,
            format="json",
        )
        res = view(req, slug=product.slug)
        assert res.status_code == 403
