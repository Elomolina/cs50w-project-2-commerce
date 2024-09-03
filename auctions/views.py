from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Max
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import *
from .models import *

#creation of watchlist
watchlist_list = set()

def index(request):
    listings = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
        "listings":listings
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


def listing_detail(request, id):
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data['bid']
            starting_bid = AuctionListing.objects.get(pk = id)
            bids_placed = Bid.objects.filter(listing_id = starting_bid)
            #bid too small
            if bid < starting_bid.starting_bid:
                return bids_for_listing(request,id, form, "The bid must be bigger than the starting bid")
            #no bids placed yet
            elif len(bids_placed) == 0 and bid >= starting_bid.starting_bid:
                #create new bid
                new_bid = Bid(listing_id = starting_bid, user_biding = request.user, bid = bid)
                new_bid.save()
                return redirect(reverse("listing_detail",args=[id]))
            #bids already placed
            else:
                #check the max
                max_bid = Bid.objects.filter(listing_id = starting_bid).aggregate(Max("bid"))
                if bid > max_bid['bid__max']:
                    new_bid = Bid(listing_id = starting_bid, user_biding = request.user, bid = bid)
                    new_bid.save()
                    return redirect(reverse("listing_detail",args=[id]))
                #bid is smaller than the current one
                else:
                    return bids_for_listing(request,id, form, "The bid must be bigger than the current bid")
            #check that bid is greater than the current bid
        else:
             return redirect(reverse("listing_detail", args=[id])) 
    form = BidForm()
    return bids_for_listing(request,id, form, "")


def bids_for_listing(request, id, form, error_bid):
    listing = AuctionListing.objects.get(pk = id)
    #get the bids made and the maximum one
    bid = len(Bid.objects.filter(listing_id = listing))
    max_bid = Bid.objects.filter(listing_id = listing).aggregate(Max("bid"))
    current_bid = ''
    if max_bid['bid__max'] is None:
        current_bid = "There are no bids placed yet"
    else:
        current_bid = f"The current bid is at ${max_bid['bid__max']}"
    if listing in watchlist_list:
        return render(request, "auctions/listing_detail.html", {
        "listing": listing,
        "watchlist": 'Remove from watchlist',
        "state": "remove", 
        "form":form,
        "bid": bid,
        "current_bid": current_bid,
        "error_bid": error_bid
    })    
    return render(request, "auctions/listing_detail.html", {
        "listing": listing,
        "watchlist": 'Add to watchlist',
        "state":"add",
        "form":form,
        "bid":bid,
        "current_bid": current_bid,
        "error_bid": error_bid
    })

@login_required(login_url='/login')
def create_listing(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            #get the inputs
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            starting_bid = form.cleaned_data['starting_bid']
            image_url = form.cleaned_data['image_url']
            category = request.POST['category']
            user = request.user
            # check if category is in the category table
            check_category = ''
            try:
                check_category = Category.objects.get(category = category)
            except Category.DoesNotExist:
                category = category.lower()
                category = category.capitalize()
                category_obj = Category(category = category)
                #add category if doesnt exist
                category_obj.save()
                #insert data to the listing table
                listing = AuctionListing(title = title, description = description, starting_bid = starting_bid,
                           image_url = image_url, category_id = category_obj, user_id = user)
                listing.save()
                return redirect(reverse("index"))
                
            #insert data to the listing table
            listing = AuctionListing(title = title, description = description, starting_bid = starting_bid,
                           image_url = image_url, category_id = check_category,user_id = user)
            listing.save()
            return redirect(reverse("index"))
        else:
            return render(request, "auctions/create.html",
                          {
                              "form":form
                          })   
    form = CreateForm()
    categories = Category.objects.all()
    return render(request, "auctions/create.html", {
                      "form": form,
                      "categories": categories
                  })

def watchlist(request, id):
    if request.method == "POST":
        state = request.POST
        listing = AuctionListing.objects.get(pk = id)
        # delete element from watchlist
        if 'remove' in state:
            watchlist_list.remove(listing)
            return redirect(reverse("listing_detail", args=[id]))
        #add element to watchlist
        elif 'add' in state:
            watchlist_list.add(listing)
            return redirect(reverse("listing_detail", args=[id]))
    return redirect(reverse("index"))