import pytest
from django.urls import reverse
from shop.models.product import Product
from shop.models.basket import Basket
from django.test.client import Client
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_create(product_fixture, faker_user_fixture):
    product: Product = product_fixture
    User.objects.create_user(**faker_user_fixture)
    client: Client = Client()
    client.login(
        username=faker_user_fixture["username"], password=faker_user_fixture["password"]
    )
    url = reverse("inventory-list")
    res = client.post(url, {"name": product.name}, content_type="application/json")
    assert res.status_code == 200


@pytest.mark.django_db
def test_create_not_exist_product(faker_user_fixture):
    User.objects.create_user(**faker_user_fixture)
    body = {"product": {"name": "doesn't exist"}}
    client: Client = Client()
    client.login(
        username=faker_user_fixture["username"], password=faker_user_fixture["password"]
    )
    url = reverse("inventory-list")
    res = client.post(url, body, content_type="application/json")
    assert res.status_code == 400


@pytest.mark.django_db
def test_remove_basket(faker_user_fixture, faker_product_fixture):
    user: User = User.objects.create_user(**faker_user_fixture)
    product: Product = Product.objects.create(**faker_product_fixture)
    Basket.objects.create(user=user, product=product)
    client: Client = Client()
    client.login(
        username=faker_user_fixture["username"], password=faker_user_fixture["password"]
    )
    url = reverse("inventory-detail", args=(product.slug,))
    res = client.delete(url, content_type="application/json")
    assert res.status_code == 200


@pytest.mark.django_db
def test_remove_not_exist_basket(faker_user_fixture):
    User.objects.create_user(**faker_user_fixture)
    client: Client = Client()
    client.login(
        username=faker_user_fixture["username"], password=faker_user_fixture["password"]
    )
    slug = "not-exist"
    url = reverse("inventory-detail", args=(slug,))
    res = client.delete(url)
    assert res.status_code == 404
