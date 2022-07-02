import json
import pytest
from rest_framework.test import APIRequestFactory
from shop.models.product import Product
from shop.views.inventory_views import IventoryViewSet
from django.contrib.auth.models import User
from shop.models.basket import Basket


@pytest.mark.django_db
def test_create_not_exist_product(user_fixture):
    factory = APIRequestFactory()
    req_body = {"product": {"name": "doesn't exist"}}
    req = factory.post("http://localhost:8000/shop/inventory/", req_body, format="json")
    req.user = user_fixture
    view = IventoryViewSet.as_view({"post": "create"})
    res = view(req)
    data = json.loads(res.content)
    assert res.status_code == 404
    assert "errors" in data
    assert data["errors"][0] == "object does not exist"


@pytest.mark.django_db
def test_create_with_not_exist_user(product_fixture, user_fixture):
    factory = APIRequestFactory()
    product: Product = product_fixture
    req = factory.post("http://localhost:8000/shop/inventory/", format="json")
    req.user = user_fixture
    req.user.pk = -1
    view = IventoryViewSet.as_view({"post": "create"})
    res = view(req, slug=product.slug)
    data = json.loads(res.content)
    assert res.status_code == 404
    assert "errors" in data
    assert data["errors"][0] == "user does not exist"


@pytest.mark.django_db
def test_create_with(product_fixture, user_fixture):
    factory = APIRequestFactory()
    product: Product = product_fixture
    req = factory.post("http://localhost:8000/shop/inventory/", format="json")
    req.user = user_fixture
    view = IventoryViewSet.as_view({"post": "create"})
    res = view(req, slug=product.slug)
    assert res.status_code == 200


@pytest.mark.django_db
def test_remove_basket(user_fixture, basket_fixture):
    factory = APIRequestFactory()
    basket: Basket = basket_fixture
    product: Product = basket.product
    req = factory.delete(
        f"http://localhost:8000/shop/inventory/{product.slug}",
        format="json",
    )
    req.user = user_fixture
    view = IventoryViewSet.as_view({"delete": "destroy"})
    res = view(req, slug=product.slug)
    assert res.status_code == 200


@pytest.mark.django_db
def test_remove_not_exist_basket(user_fixture):
    factory = APIRequestFactory()
    slug = "not-exist"
    req = factory.delete(
        f"http://localhost:8000/shop/inventory/{slug}",
    )
    view = IventoryViewSet.as_view({"delete": "destroy"})
    req.user = user_fixture
    res = view(req, slug=slug)
    assert res.status_code == 404
