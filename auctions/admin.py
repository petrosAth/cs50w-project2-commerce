from django.contrib import admin
from .models import User, Listing, Photo, Bid, Category, Comment


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")


class PhotoInline(admin.StackedInline):
    model = Photo


class BidInline(admin.StackedInline):
    model = Bid


class CommentInline(admin.StackedInline):
    model = Comment


class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "starting_price")
    inlines = [PhotoInline, BidInline, CommentInline]


class PhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class BidAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


class CommentAdmin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
