# Generated by Django 4.0.3 on 2022-07-16 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_bid_auction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='image',
            field=models.URLField(blank=True, max_length=500),
        ),
    ]
