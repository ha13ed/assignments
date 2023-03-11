from django.contrib import admin
from .models import Listing, User, Bid, Comment

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "create_date", "start_bid")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "bidder", "bid_date", "price")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "commenter", "comment_date", "comment")

# Register your models here.
admin.site.register(Listing, ListingAdmin)
admin.site.register(User)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)