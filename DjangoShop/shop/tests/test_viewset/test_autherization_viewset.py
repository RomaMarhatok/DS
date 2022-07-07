import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_sign_in_user(faker_user_fixture):
    faker_user_data: dict = faker_user_fixture
    client: Client = Client()
    url = reverse("user-sign-in")
    res = client.post(url, faker_user_data)
    assert res.status_code == 200
    assert User.objects.all().count() == 1


@pytest.mark.django_db
def test_sign_in_user_bad_parameters():
    client: Client = Client()
    url = reverse("user-sign-in")
    res = client.post(url, {})
    assert res.status_code == 400


@pytest.mark.django_db
def test_logout_user(faker_user_fixture):
    faker_user_data: dict = faker_user_fixture
    User.objects.create_user(**faker_user_data)
    client: Client = Client()
    url = reverse("user-logout")
    res = client.post(url, faker_user_fixture)
    assert res.status_code == 200


@pytest.mark.django_db
def test_login_user(faker_user_fixture):
    User.objects.create_user(**faker_user_fixture)
    client: Client = Client()
    url = reverse("user-login")
    res = client.post(url, faker_user_fixture)
    assert res.status_code == 200


@pytest.mark.django_db
def test_login_user_bad_parameters(faker_user_fixture):
    User.objects.create_user(**faker_user_fixture)
    client: Client = Client()
    url = reverse("user-login")
    res = client.post(url, {})
    assert res.status_code == 400
