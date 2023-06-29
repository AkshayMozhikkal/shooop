# Generated by Django 4.2.1 on 2023-06-11 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_products_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='offers',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='coupons',
            name='code',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='offers',
            name='descr',
            field=models.CharField(max_length=550),
        ),
    ]
