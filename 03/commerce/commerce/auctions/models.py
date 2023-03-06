from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bids = models.CharField(null=True, blank=True, max_length=128)

class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    img_url = models.URLField(blank = True, max_length=256)
    create_date = models.DateTimeField ()
    start_bid = models.FloatField()
    best_bid = models.FloatField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    best_bidder = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="current_winner")
    watchlist = models.ManyToManyField(User, null=True, blank=True, related_name="watchlister")

    def __str__ (self):
        return self.title

class Bid(models.Model):
    title = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_b")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    price = models.FloatField()
    bid_date = models.DateTimeField()
    
class Comment(models.Model):
    title = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_c")
    comment = models.CharField(max_length=512)