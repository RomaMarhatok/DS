import pytest
from django.contrib.auth.models import User
from shop.models.product import Product, Category, Attribute, CategoryProduct
from shop.models.order import Order
from shop.models.basket import Basket
from faker import Faker

faker = Faker()

# fixtures for category Model


@pytest.fixture
def faker_category_fixture() -> dict:
    return {"name": faker.name()}


@pytest.fixture
def category_fixture() -> Category:
    category: Category = Category.objects.create(name="game notebooks")
    return category


# fixtures for product model


@pytest.fixture
def faker_product_fixture() -> dict:
    return {
        "name": faker.name(),
        "price": faker.pyfloat(right_digits=2, positive=True),
    }


@pytest.fixture
def product_fixture() -> Product:
    product: Product = Product.objects.create(name="Asus tuf gaming", price=123)
    return product


# fixtures for attribute Model


@pytest.fixture
def faker_attribute_fixture(faker_product_fixture) -> dict:
    return {
        "name": faker.pystr(),
        "value": faker.pystr(),
        "product": faker_product_fixture,
    }


@pytest.fixture
def attribute_fixture(product_fixture) -> Category:
    product: Product = product_fixture
    attribute: Attribute = Attribute.objects.create(
        name="screen resolution", value="1970x1292", product=product
    )
    return attribute


# fixtures for attribute CategoryProduct model


@pytest.fixture
def category_porduct_fixture(category_fixture, product_fixture) -> CategoryProduct:
    category: Category = category_fixture
    product: Product = product_fixture
    category_product = CategoryProduct.objects.create(
        category=category, product=product
    )
    return category_product


@pytest.fixture
def faker_category_product_fixture(faker_product_fixture, faker_category_fixture):
    return {"product": faker_product_fixture, "category": faker_category_fixture}


# fixtures for User model
@pytest.fixture
def fake_user_fixture() -> dict:
    return {"username": faker.name(), "password": faker.pystr()}


@pytest.fixture
def user_fixture(fake_user_fixture) -> User:
    data: dict = fake_user_fixture
    user: User = User.objects.create(**data)
    return user


@pytest.fixture
def admin_user_fixture(fake_user_fixture) -> User:
    data: dict = fake_user_fixture
    data.update({"is_staff": True})
    user: User = User.objects.create(**data)
    return user


# fixtures for Order model


@pytest.fixture
def faker_order_fixture(user_fixture, product_fixture) -> dict:
    return {
        "user": user_fixture,
        "product": product_fixture,
        "country": faker.country(),
        "city": faker.city(),
        "street": faker.street_address(),
    }


@pytest.fixture
def order_fixture(faker_order_fixture) -> Order:
    data: dict = faker_order_fixture
    order: Order = Order.objects.create(**data)
    return order


# fixtures for Basket model


@pytest.fixture
def faker_basket_fixture(user_fixture, product_fixture) -> dict:
    return {"user": user_fixture, "product": product_fixture}


@pytest.fixture
def basket_fixture(faker_basket_fixture) -> Basket:
    data: dict = faker_basket_fixture
    basket: Basket = Basket.objects.create(**data)
    return basket
