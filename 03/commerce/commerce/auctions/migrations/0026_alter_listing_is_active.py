# Generated by Django 4.1.7 on 2023-03-10 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0025_listing_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
