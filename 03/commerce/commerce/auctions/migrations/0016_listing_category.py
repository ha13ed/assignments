# Generated by Django 4.1.7 on 2023-03-10 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_alter_comment_comment_date_alter_comment_commenter'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]