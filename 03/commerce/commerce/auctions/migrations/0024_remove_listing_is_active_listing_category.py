# Generated by Django 4.1.7 on 2023-03-10 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0023_remove_listing_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='is_active',
        ),
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('1', 'Fashion'), ('2', 'Toys'), ('3', 'Electronics'), ('4', 'Home'), ('5', 'Groceries'), ('6', 'Others')], default='6', max_length=2),
        ),
    ]
