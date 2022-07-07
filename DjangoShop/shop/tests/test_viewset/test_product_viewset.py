import json
import pytest
from django.urls import reverse
from shop.models.product import (
    Product,
    CategoryProduct,
    Category,
)
from django.test import Client
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from shop.serializers.product_serializers import ProductSerializer


@pytest.mark.django_db
def test_get_all_products():

    client: Client = Client()
    url = reverse("product-list")

    res = client.get(url)
    assert res.status_code == 200
    assert isinstance(json.loads(res.content), list)


@pytest.mark.django_db
def test_get_product_by_slug(product_fixture: Product):
    product: Product = product_fixture
    url = reverse("product-detail", args=(product.slug,))
    client: Client = Client()
    res = client.get(url)
    assert res.status_code == 200
    assert isinstance(json.loads(res.content), dict)


@pytest.mark.django_db
def test_create_product(faker_user_fixture):
    body = {
        "product": {
            "name": "HP ProBook 455 G8 45N00ES",
            "price": 123,
        },
        "category": "game notebooks",
    }
    Category.objects.create(name=body["category"])
    User.objects.create_superuser(**faker_user_fixture)
    client: Client = Client()
    client.login(
        username=faker_user_fixture["username"], password=faker_user_fixture["password"]
    )
    url = reverse("product-list")
    res = client.post(
        url,
        json.dumps(body),
        content_type="application/json",
    )
    assert res.status_code == 200
    assert CategoryProduct.objects.all().count() == 1
    assert Product.objects.all().count() == 1


@pytest.mark.django_db
def test_update_product(category_porduct_fixture, faker_user_fixture):

    body = {"product": {"name": "Haier U1520SD", "price": 999}}
    category_product: CategoryProduct = category_porduct_fixture

    User.objects.create_superuser(**faker_user_fixture)

    client: Client = Client()
    client.login(
        username=faker_user_fixture["username"], password=faker_user_fixture["password"]
    )
    url = reverse("product-detail", args=(category_product.product.slug,))

    res = client.put(
        url,
        json.dumps(body),
        content_type="application/json",
    )

    # initialization data from request for asserting

    product: Product = Product.objects.get(slug=slugify(body["product"]["name"]))
    serializer: ProductSerializer = ProductSerializer(product)
    category_from_serializer = serializer.data["category_product"][0]["category"]

    # initialization data from response for asserting

    data = json.loads(res.content)
    category_from_res = data["category_product"][0]["category"]

    assert res.status_code == 200
    assert product.name == body["product"]["name"]
    assert product.price == body["product"]["price"]
    assert category_from_res == category_from_serializer


@pytest.mark.django_db
def test_destroy_product(product_fixture, faker_user_fixture):
    product: Product = product_fixture
    User.objects.create_superuser(**faker_user_fixture)

    url = reverse("product-detail", args=(product.slug,))

    client: Client = Client()
    client.login(
        username=faker_user_fixture["username"], password=faker_user_fixture["password"]
    )
    res = client.delete(url)
    assert res.status_code == 200
    assert Product.objects.all().count() == 0


@pytest.mark.django_db
def test_update_without_req_body(product_fixture, faker_user_fixture):
    product: Product = product_fixture
    User.objects.create_superuser(**faker_user_fixture)
    client: Client = Client()

    client.login(
        username=faker_user_fixture["username"], password=faker_user_fixture["password"]
    )

    url = reverse("product-detail", args=(product.slug,))
    res = client.put(
        url,
        content_type="application/json",
    )
    assert res.status_code == 400


@pytest.mark.django_db
def test_update_with_empty_req_body(product_fixture, faker_user_fixture):

    product: Product = product_fixture
    User.objects.create_superuser(**faker_user_fixture)
    client: Client = Client()

    client.login(
        username=faker_user_fixture["username"], password=faker_user_fixture["password"]
    )

    url = reverse("product-detail", args=(product.slug,))
    res = client.put(
        url,
        {"product": {}},
        content_type="application/json",
    )
    assert res.status_code == 400


@pytest.mark.django_db
def test_get_not_exist_product():
    product_slug: str = "not-exist-slug"

    url = reverse("product-detail", args=(product_slug,))
    client: Client = Client()
    res = client.get(url)
    assert res.status_code == 404


@pytest.mark.django_db
def test_update_not_exist_product(faker_user_fixture):
    product_slug: str = "not-exist-slug"

    body = {"product": {"name": "Haier U1520SD", "price": 999}}
    User.objects.create_superuser(**faker_user_fixture)
    client: Client = Client()

    client.login(
        username=faker_user_fixture["username"], password=faker_user_fixture["password"]
    )

    url = reverse("product-detail", args=(product_slug,))
    res = client.put(
        url,
        json.dumps(body),
        content_type="application/json",
    )
    assert res.status_code == 404


@pytest.mark.django_db
def test_put(product_fixture):
    product: Product = product_fixture
    client: Client = Client()
    body = {"product": {"name": "Haier U1520SD", "price": 999}}

    url = reverse("product-detail", args=(product.slug,))
    res = client.put(url, body, content_type="application/json")
    assert res.status_code == 403


@pytest.mark.django_db
def test_delete(product_fixture):
    product: Product = product_fixture
    url = reverse("product-detail", args=(product.slug,))
    client: Client = Client()
    res = client.delete(url)
    assert res.status_code == 403


@pytest.mark.django_db
def test_post():
    body = {
        "product": {
            "name": "HP ProBook 455 G8 45N00ES",
            "price": 123,
        },
        "category": "game notebooks",
    }
    Category.objects.create(name=body["category"])
    client: Client = Client()
    url = reverse("product-list")
    res = client.post(
        url,
        json.dumps(body),
        content_type="application/json",
    )
    assert res.status_code == 403
