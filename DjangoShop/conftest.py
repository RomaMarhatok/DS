import pytest
from shop.models.product import Product, Category, Attribute, CategoryProduct
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
def faker_attribute_fixture() -> dict:
    return {
        "name": faker.pystr(),
        "attribute": faker.pystr(),
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
def category_porduct_fixture(category_fixture, product_fixture):
    category: Category = category_fixture
    product: Product = product_fixture
    category_product = CategoryProduct.objects.create(
        category=category, product=product
    )
    return category_product
