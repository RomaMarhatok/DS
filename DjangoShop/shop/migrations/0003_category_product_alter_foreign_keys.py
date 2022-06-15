# Generated by Django 4.0.5 on 2022-06-15 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0002_alter_categoryproduct_product"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attribute",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="attributes",
                to="shop.product",
            ),
        ),
        migrations.AlterField(
            model_name="categoryproduct",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="category_product",
                to="shop.category",
            ),
        ),
        migrations.AlterField(
            model_name="categoryproduct",
            name="product",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="category_product",
                to="shop.product",
            ),
        ),
    ]
