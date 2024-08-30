from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import *
from .models import *


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
                return redirect(reverse("create_listing"))
                
            #insert data to the listing table
            listing = AuctionListing(title = title, description = description, starting_bid = starting_bid,
                           image_url = image_url, category_id = check_category,user_id = user)
            listing.save()
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