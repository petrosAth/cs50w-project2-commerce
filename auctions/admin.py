from django.contrib import admin
from .models import User, Listing, Bid, Category, Comment


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")


class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "starting_price")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category, CategoryAdmin)
