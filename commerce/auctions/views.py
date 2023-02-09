from cProfile import label
from itertools import product
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Comment, Market, Bid, WL




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


def index(request):
    listing = Market.objects.all().order_by('id').reverse()
    return render(request, "auctions/index.html", {"listing":listing}
    )

@login_required
def createl(request):
    if request.method == "POST":
        
        product = request.POST['product']
        user = request.user 
        og_bid = request.POST['og_bid']
        description = request.POST['description']
        category = request.POST['category']
        image = request.POST['image']


        l=Market.objects.create(
            user=user,
            product = product,
            og_bid = og_bid,
            description = description,
            category = category,
            image = image
            )
        l.save()
    return render(request, "auctions\createl.html")

@login_required(login_url='login')
def inpage(request, id):
    inside = Market.objects.get(id=id)
    if request.method == 'POST':
        inside.status = False
        inside.save()
    bidwinner = inside.user

    if request.user:
        Wlist = WL.objects.filter(user=request.user)
        Wlisted = []
        for i in range(len(Wlist)):
            Wlisted.append(Wlist[i].wl)
        N = False
        if inside in Wlisted:
            N=True
    return render(request, "auctions\inpage.html", {"inside":inside,"bidwinener":bidwinner,"N":N})



@login_required(login_url='login')
def addcomment(request,id):
    inside = Market.objects.get(id=id)
    if request.method == 'POST':
        comment = request.POST['comment']
        commentin = Comment.objects.create(content=comment,
        user=request.user)
        inside.comment.add(commentin)
        inside.save()
    return redirect('inpage', id=id)

@login_required(login_url='login')
def addbid(request,id):
    inside = Market.objects.get(id=id)
    if request.method == 'POST':
        value = request.POST['bid']
        if inside.last_bid == None:
            bidq = int(inside.og_bid)
        else:
            bidq = int(inside.last_bid)

        if int(value) > bidq :

            bidin =Bid.objects.create(
                        bid_prize=int(value),
                        user=request.user,
                    )

            inside.winner = request.user.username
            inside.save()

            inside.last_bid=int(value)
            inside.bid.add(bidin)
            inside.save()
            return redirect('inpage', id=id)

        else:
            return HttpResponse('failed')

@login_required(login_url='login')
def watchadd(request, id):   
    if request.method == 'POST':
        user = request.user
        inside = Market.objects.filter(id=id).first()
        Wlist = WL.objects.filter(user=user, wl=inside).first()

        if Wlist is None:
            twl = WL.objects.create(user=user, wl=inside)
            twl.save()
        else:
            Wlist.delete()     
    return redirect('inpage', id=id)

@login_required(login_url='login')
def watchlist(request):
    wl = WL.objects.filter(user=request.user)
    return render(request, "auctions\watchlist.html", {"watchlist":wl})

def categories(request):
    list=[]
    categories_list = Market.objects.all()
    for i in categories_list:
            if i.category not in list:
                list.append(i.category)
    return render(request, "auctions\categories.html", {"catelist":list})

def incategories(request, name):
    incate = Market.objects.filter(category=name)
    return render(request, "auctions\incategories.html", {"incate":incate})







