# Generated by Django 4.2.1 on 2023-12-02 08:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userpages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_person', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.BigIntegerField(null=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=50)),
                ('time_of_order', models.DateTimeField(auto_now_add=True)),
                ('mode_of_payment', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userpages.address')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ordered_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.BigIntegerField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('status', models.CharField(choices=[('Order Confirmed', 'Order Confirmed'), ('Shipped', 'Shipped'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Returned', 'Returned')], default='Order Confirmed', max_length=100)),
                ('order_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.variation')),
            ],
        ),
        migrations.CreateModel(
            name='Used_Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_total_amount', models.BigIntegerField(null=True)),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.coupons')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
        ),
        migrations.CreateModel(
            name='Returned',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(blank=True, max_length=50, null=True)),
                ('comments', models.CharField(blank=True, max_length=250, null=True)),
                ('returned_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.ordered_product')),
            ],
        ),
    ]
