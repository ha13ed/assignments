from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Listing, Bid, Comment
import datetime
from django.db.models import Max, Q
from django.db.models.functions import Random


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'
        fields = ['title', 'description','category', 'start_bid', 'img_url']
        labels = {
            'title': '', 'description': '','category': '', 'start_bid': '', 'img_url': ''
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'm-2 rounded-5 form-control form-control-lg',
             'placeholder': 'Title', 'style': 'text-align: center;'}),
            'description': forms.Textarea(attrs={'class': 'm-2 rounded-5 form-control', 'rows': 10,
             'cols': 150, 'placeholder': 'Description', 'style': 'height: auto;'}),
             'category': forms.Select(attrs={'class': 'm-2 rounded-5 form-control'}),
            'start_bid': forms.NumberInput(attrs={'class': 'm-2 rounded-5 form-control', 'min': 0,
             'max': 100, 'placeholder': 'Bid start'}),
            'img_url': forms.URLInput(attrs={'class': 'm-2 rounded-5 form-control', 'placeholder': 'Iamge URL'}),
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['price']
        labels = {
            'price': ''
        }
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'mt-4 m-2 rounded-5 form-control',
             'min': 0, 'max': 100, 'Placeholder': 'Bid price'})
        }

    def __init__(self, *args, **kwargs):
        min_value = kwargs.pop('min_value', None)
        super().__init__(*args, **kwargs)
        if min_value is not None:
            self.fields['price'].widget.attrs['min'] = min_value

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        labels = {
            'comment': ''
        }
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'm-2 rounded-5 form-control', 'rows': 5, 'cols': 50,
        'placeholder': 'Your Comment', 'style': 'height: auto;'})
        }

def index(request):
    # it should modify to active except all objects
    listings = Listing.objects.filter(is_active = True).order_by(Random())
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="/login")
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = Listing()
            listing.title = form.cleaned_data["title"]
            listing.description = form.cleaned_data["description"]
            listing.start_bid = form.cleaned_data["start_bid"]
            listing.img_url = form.cleaned_data["img_url"]
            listing.is_active = True
            listing.category = form.cleaned_data["category"]
            listing.create_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            listing.owner = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    form = ListingForm()
    return render(request, "auctions/new.html", {
        "form": form
    })

def listing(request, id):
    listing = Listing.objects.get(id = id)
    if request.method == "POST":
        print(request.POST)
        if "watchlist" in request.POST:
            if request.user in listing.watchlist.all():
                listing.watchlist.remove(request.user)
            else:
                listing.watchlist.add(request.user)
        elif "price" in request.POST:
            form_bid = BidForm(request.POST)
            if form_bid.is_valid():
                bid = Bid()
                bid.title = listing
                bid.bidder = request.user
                bid.bid_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                bid.price = form_bid.cleaned_data["price"]
                bid.save()
                listing.best_bid = bid.price
                listing.best_bidder = bid.bidder
                listing.save()
        elif "closing" in request.POST:
            listing.is_active = False
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            form_comment = CommentForm(request.POST)
            if form_comment.is_valid():
                comment = Comment()
                comment.title = listing
                comment.commenter = request.user
                comment.comment_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                comment.comment = form_comment.cleaned_data["comment"]
                comment.save()

    """max_price_bid = Bid.objects.aggregate(Max('price'))
    max_price = max_price_bid['price__max']"""
    if listing.best_bid:
        min_value = 1.01 * listing.best_bid
    else:
        min_value = listing.start_bid
    form_bid = BidForm(min_value = min_value)
    form_comment = CommentForm()
    bids = Bid.objects.filter(title = listing.id)
    comments = Comment.objects.filter(title = listing.id)
    return render(request, "auctions/listing.html", {
        "listing": listing, "bids": bids, "comments": comments, "form_bid": form_bid,
        "form_comment":form_comment, "watchlist": request.user in listing.watchlist.all()
    })

@login_required(login_url="/login")
def watchlist(request):
    criterion1 = Q(watchlist = request.user)
    criterion2 = Q(is_active = True)
    listings = Listing.objects.filter(criterion1 & criterion2)
    return render(request, "auctions/index.html", {
        "listings": listings
    })

def categories_index(request):
    categories = Listing.Category.choices
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def categories(request, q):
    criterion1 = Q(category = q)
    criterion2 = Q(is_active = True)
    listings = Listing.objects.filter(criterion1 & criterion2)
    return render(request, "auctions/index.html", {
        "listings": listings
    })

def closed(request):
    listings = Listing.objects.filter(is_active = False)
    return render(request, "auctions/closed.html", {
        "listings": listings
    })