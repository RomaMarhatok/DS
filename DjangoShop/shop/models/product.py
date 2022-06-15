from django.db import models
from django.core.validators import MinValueValidator
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, default=None)
    price = models.DecimalField(
        validators=[MinValueValidator(limit_value=0)], max_digits=15, decimal_places=2
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)


class CategoryProduct(models.Model):
    product = models.ForeignKey(
        Product, related_name="products", on_delete=models.SET_NULL, null=True
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)


class Attribute(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CategoryAttribute(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.SET_NULL, null=True)
