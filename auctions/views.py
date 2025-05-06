from django.contrib.auth import authenticate, login, logout, decorators
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Photo, Bid, Comment


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


@decorators.login_required(login_url="auctions:login")
def create_auction(request):
    if "title" and "description" and "starting_bid" not in request.POST:
        return render(
            request,
            "auctions/create.html",
            {"title": "Create Auction", "categories": Category.objects.all()},
        )
    else:
        title = request.POST["title"] or ""
        description = request.POST["description"] or ""
        starting_bid = request.POST["starting_bid"] or ""
        owner = User.objects.get(pk=request.user.id)
        listing = Listing(
            title=title,
            description=description,
            starting_price=starting_bid,
            owner=owner,
            active=True,
        )
        listing.save()

        selected_categories = request.POST.getlist("category_list")
        for category_title in selected_categories:
            category = Category.objects.get(title=category_title)
            listing.category.add(category)

        if "image" in request.FILES:
            image_file = request.FILES["image"]
            Photo.objects.create(name=image_file.name, img=image_file, listing=listing)

        return HttpResponseRedirect(reverse("auctions:index"))


def active_listings(request):
    active_auctions = Listing.objects.filter(active=True)
    return render(request, "auctions/active.html", {"active_auctions": active_auctions})
