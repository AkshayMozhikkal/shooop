# Generated by Django 4.2.1 on 2023-06-22 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_alter_cart_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.BigIntegerField(),
        ),
    ]
