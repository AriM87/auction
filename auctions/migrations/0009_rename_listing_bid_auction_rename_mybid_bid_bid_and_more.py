# Generated by Django 4.0.3 on 2022-07-13 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_remove_bid_bid_bid_bidder_bid_listing_bid_mybid_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='listing',
            new_name='auction',
        ),
        migrations.RenameField(
            model_name='bid',
            old_name='mybid',
            new_name='bid',
        ),
        migrations.RenameField(
            model_name='bid',
            old_name='bidder',
            new_name='user',
        ),
    ]