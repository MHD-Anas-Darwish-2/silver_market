# Generated by Django 3.2.13 on 2022-12-18 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=200, null=True),
        ),
    ]
