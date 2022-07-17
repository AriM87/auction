import datetime
from black import nullcontext
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# Auction model
class Auction(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField(max_length=1000)
    start_bid = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.URLField(blank=True, max_length=5000)
    category = models.CharField(max_length=200, blank=True, default="None")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller", blank=True, null=True)
    close = models.BooleanField(default=False)
    watchlist = models.ManyToManyField(User, related_name="watchlist")
       
    def __str__(self):
        return self.title


# bid Model
class Bid(models.Model):
    bid = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='user', blank=True)
    auction = models.ForeignKey(Auction, null=True, on_delete=models.CASCADE, related_name='bids', blank=True)
   
    def __str__(self):
        return {self.user} | {self.auction.title} | {self.bid}


# comment model
class Comment(models.Model):
    comment = models.TextField(max_length=10000)

    def __str__(self):
        return self.comment

# class Person(models.Model):
#     person = models.CharField(max_length=60)
#     category = models.ManyToManyField('Category', blank=True, null=True)

#     def __str__(self):
#         return self.person
