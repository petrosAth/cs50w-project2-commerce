from django.contrib.auth import authenticate, login, logout, decorators
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Photo, Bid, Comment, Watchlist


def index(request):
    return active_listings(request)


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
        return render(request, "auctions/login.html", {"title": "Login"})


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
                request,
                "auctions/register.html",
                {"title": "Register", "message": "Passwords must match."},
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
    auctions_list = Listing.objects.filter(active=True)
    return render(
        request,
        "auctions/auctions.html",
        {"title": "Active Listings", "auctions_list": auctions_list},
    )


def auction(request, listing_id, message=""):
    auction = Listing.objects.get(pk=listing_id)
    bid = auction.bids.filter(listing_id=listing_id)  # type: ignore
    current_bid = (
        (
            auction.bids.filter(listing_id=listing_id)  # type: ignore
            .order_by("-amount")
            .first()
            .amount
        )
        if bid.exists()
        else None
    )
    is_watched = auction.watched.filter(  # type: ignore
        user_id=request.user.id, auction_id=listing_id
    ).exists()

    if "watch" in request.POST:
        if not Watchlist.objects.filter(
            user_id=request.user.id, auction_id=request.POST["watch"]
        ).exists():
            watchlist_user = User.objects.get(pk=request.user.id)
            watchlist_auction = Listing.objects.get(pk=request.POST["watch"])
            watched_auction = Watchlist(user=watchlist_user, auction=watchlist_auction)
            watched_auction.save()
    elif "unwatch" in request.POST:
        Watchlist.objects.get(
            user_id=request.user.id, auction_id=request.POST["unwatch"]
        ).delete()

    is_watched = auction.watched.filter(  # type: ignore
        user_id=request.user.id, auction_id=listing_id
    ).exists()

    return render(
        request,
        "auctions/auction.html",
        {
            "title": "Auction Details",
            "auction": auction,
            "is_watched": is_watched,
            "current_bid": current_bid,
            "message": message,
        },
    )


def categories(request):
    categories = Category.objects.all()

    return render(
        request,
        "auctions/categories.html",
        {"title": "Categories", "categories": categories},
    )


def category(request, category_id):
    category = Category.objects.get(pk=category_id)
    auctions_list = category.listings.filter(active=True)  # type: ignore
    return render(
        request,
        "auctions/auctions.html",
        {"title": category.title, "auctions_list": auctions_list},
    )


@decorators.login_required(login_url="auctions:login")
def watchlist(request):
    watched = User.objects.get(pk=request.user.id).watched.all()  # type: ignore
    auctions_list = [entry.auction for entry in watched]

    return render(
        request,
        "auctions/auctions.html",
        {"title": "Watchlist", "auctions_list": auctions_list},
    )


@decorators.login_required(login_url="auctions:login")
def place_bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    message = ""
    if listing.owner.id == request.user.id:
        message = "You cannot bid on your own auction."
    else:
        if "bid_amount" in request.POST:
            bid_amount = request.POST["bid_amount"]
            if listing.bids.exists():  # type: ignore
                highest_bid = listing.bids.all().order_by("-amount").first()  # type: ignore
                if float(bid_amount) > highest_bid.amount:
                    if highest_bid.user.id != request.user.id:  # type: ignore
                        bid_user = User.objects.get(pk=request.user.id)
                        bid_auction = Listing.objects.get(pk=listing_id)
                        bid = Bid(user=bid_user, listing=bid_auction, amount=bid_amount)
                        bid.save()
                    else:
                        message = "You are already the highest bidder."
                else:
                    message = "Your bid must be higher than the current bid."
            elif float(bid_amount) > listing.starting_price:
                bid_user = User.objects.get(pk=request.user.id)
                bid_auction = Listing.objects.get(pk=listing_id)
                bid = Bid(user=bid_user, listing=bid_auction, amount=bid_amount)
                bid.save()
            else:
                message = "Your bid must be higher than the starting price."
    return auction(request, listing_id, message)
