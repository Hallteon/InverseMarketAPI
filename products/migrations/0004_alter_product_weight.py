# Generated by Django 3.2.18 on 2023-10-05 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.IntegerField(default=0, verbose_name='Вес (в граммах)'),
        ),
    ]
