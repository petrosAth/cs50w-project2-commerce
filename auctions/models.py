from enum import unique

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"title: {self.title}"


class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    starting_price = models.FloatField(max_length=6)
    photo_url = models.URLField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    active = models.BooleanField(blank=True, default=True)
    winner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="purchases", blank=True, null=True
    )
    category = models.ManyToManyField(Category, related_name="listings")

    def __str__(self):
        return f"title: {self.title}<br> description: {self.description}<br> starting_price: {self.starting_price}<br> photo_url: {self.photo_url}<br> owner: {self.owner}<br> active: {self.active}<br> winner: {self.winner}<br>"


class Photos(models.Model):
    name = models.CharField(max_length=200)
    img = models.ImageField(upload_to="photos/")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="photos"
    )
    position = models.IntegerField(blank=True, null=True)


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.FloatField(max_length=6)

    def __str__(self):
        return f"user: {self.user}<br>listing: {self.listing}<br>amount: {self.amount}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments"
    )
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f"user: {self.user}<br>listing: {self.listing}<br>created: {self.created}<br>content: {self.content}"
