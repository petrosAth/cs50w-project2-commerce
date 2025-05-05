from enum import unique

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listings(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    starting_price = models.FloatField(max_length=6)
    photo_url = models.URLField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    active = models.BooleanField(blank=True, default=True)
    winner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="purchases", blank=True, null=True
    )

    def __str__(self):
        return f"title: {self.title}\n description: {self.description}\n starting_price: {self.starting_price}\n photo_url: {self.photo_url}\n owner: {self.owner}\n active: {self.active}\n winner: {self.winner}\n"


class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids")
    amount = models.FloatField(max_length=6)

    def __str__(self):
        return f"user: {self.user}\nlisting: {self.listing}\namount: {self.amount}"


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(
        Listings, on_delete=models.CASCADE, related_name="comments"
    )
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f"user: {self.user}\nlisting: {self.listing}\ncreated: {self.created}\ncontent: {self.content}"
