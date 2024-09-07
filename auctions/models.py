from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.category}"

class AuctionListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    starting_bid = models.FloatField()
    image_url = models.URLField(max_length=1500, blank=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    datetime = models.DateField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    closed_auction = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.title}, {self.description}, {self.starting_bid}, {self.image_url}, {self.category_id}, {self.datetime}, {self.user_id}"

class Bid(models.Model):
    listing_id = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    user_biding = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_bidings")
    bid = models.FloatField()
    datetime = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.listing_id}, {self.user_biding}, {self.bid}"

class ClosedBid(models.Model):
    winning_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winning_user")
    listing_id = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing_won")
    original_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="original_user")
    selling_price = models.FloatField()
    def __str__(self):
        return f"{self.winning_user}, {self.selling_price}"

class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing_id = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing_comments")
    comment = models.CharField(max_length=300)
    datetime = models.DateField(auto_now_add=True)