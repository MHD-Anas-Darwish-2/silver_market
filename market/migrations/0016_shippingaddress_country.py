# Generated by Django 3.2.16 on 2023-01-11 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0015_delete_myuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='country',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
