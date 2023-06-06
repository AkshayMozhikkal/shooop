# Generated by Django 4.2.1 on 2023-06-02 15:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_products_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0002_order_address_order_name_of_person_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ordered_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.BigIntegerField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('order_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.products')),
            ],
        ),
    ]
