# Generated by Django 4.1.7 on 2023-03-10 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0026_alter_listing_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('1', 'Fashion'), ('2', 'Toys'), ('3', 'Electronics'), ('4', 'Home'), ('5', 'Groceries'), ('6', 'Others')], max_length=2),
        ),
        migrations.AlterField(
            model_name='listing',
            name='is_active',
            field=models.BooleanField(),
        ),
    ]