from django.contrib import admin
from .models import Listing, User, Bid

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "create_date", "start_bid")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "bidder", "bid_date", "price")

# Register your models here.
admin.site.register(Listing, ListingAdmin)
admin.site.register(User)
admin.site.register(Bid, BidAdmin)
