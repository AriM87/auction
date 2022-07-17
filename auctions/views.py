from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
import pkg_resources

from .models import User, Auction, Comment, Bid
from .forms import AuctionForm, CommentForm, BidForm

from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.contrib import messages
from decimal import Decimal

def index(request):
    active_listings = Auction.objects.all
    context = {'active_listings': active_listings}
    return render(request, "auctions/index.html", context)


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


@login_required(login_url='/login/')
def new_listing(request):
    form = AuctionForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = AuctionForm()
    context = {'form': form}
    return render(request, "auctions/new_listing.html", context)


@login_required(login_url='/login/')
def show_listing(request, pk):
    
    # need to chekc if a listing is still open?
    # try:
    #     listing = Auction.objects.get(id=pk)
    # except:
    #     return HttpResponse("Entry does not exist")
    
    auction = Auction.objects.get(id=pk)
    watching = get_object_or_404(Auction, id=pk)
    
    watched = False
    if watching.watchlist.filter(id=request.user.id).exists():
        watched = True
    
    form = CommentForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = CommentForm()
    comments = Comment.objects.all()
    bid = BidForm()
    
    if auction.bids.exists():
        highest_bid = auction.bids.aggregate(Max('bid')).get('bid__max')
    else:
        highest_bid = auction.start_bid
          
    context = {'auction': auction, 'form': form,'comments': comments,
               'watched' : watched, 'bid': bid, 'highest_bid': highest_bid}
    return render(request, "auctions/show_listing.html", context)


@login_required(login_url='/login/')
def user_watchlist(request):
    user = User.objects.get(username=request.user)
    watchlist = user.watchlist.all
    context = {'watchlist': watchlist}
    return render(request, "auctions/user_watchlist.html", context)

def watchlist(request, pk):
    listing = get_object_or_404(Auction, id=request.POST.get('listing_id'))
    watched = False
    if listing.watchlist.filter(id=request.user.id).exists():
        listing.watchlist.remove(request.user)
        watched = False
    else:
        listing.watchlist.add(request.user)
        watched = True
    return HttpResponseRedirect(reverse('show-listing', args=[str(pk)]))

def new_bid(request, pk):
    user = request.user
    auction = Auction.objects.get(id=pk)
    if request.method == 'POST':
        bid = Decimal(request.POST.get('bid'))
        if auction.bids.exists():
            highest_bid = auction.bids.aggregate(Max('bid')).get('bid__max')
        else:
            highest_bid = auction.start_bid
        if bid > highest_bid:
            new_bid = Bid(user=user, auction=auction, bid=bid)
            new_bid.save()
        else:
            messages.warning(request, 'Your bid needs to be higher than current bid!') 
    return HttpResponseRedirect(reverse('show-listing', kwargs={'pk': pk}))    

def close_listing(request, pk):
    auction = Auction.objects.get(id=pk)
    if request.user == auction.user:
        auction.close = True
        auction.save()
    else:
        messages.error(request, 'This is not your listing, you can not end bidding, FUCK U Izi') 
    return HttpResponseRedirect(reverse('show-listing', kwargs={'pk': pk} ))
    
    