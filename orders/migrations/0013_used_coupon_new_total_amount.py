# Generated by Django 4.2.1 on 2023-06-20 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_used_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='used_coupon',
            name='new_total_amount',
            field=models.BigIntegerField(null=True),
        ),
    ]
