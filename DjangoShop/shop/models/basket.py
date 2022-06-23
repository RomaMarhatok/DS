from django.db import models
from django.contrib.auth.models import User
from .product import Product


class Basket(models.Model):
    user = models.ForeignKey(User, related_name="basket", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
