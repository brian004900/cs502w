from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json

from .models import User,Post, Person





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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            person = Person.objects.create(user=user)
            user.save()
            person.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def index(request):
    return render(request, "network/index.html")

def addpost(request):   
    if request.method == "POST":
        user=request.user
        content=request.POST['content']
        l=Post.objects.create(
            user=user,
            content=content,
        )
        l.save() 
    if request.method == "PUT":
        data=json.loads(request.body)
        post_id = int(data["post_id"])
        newcontent = data["newcontent"]
        post = Post.objects.filter(id=post_id).first() 
        post.content= newcontent
        post.save()
    return index(request)

def updatef(request,user_id):
    person = request.user
    profile = Person.objects.filter(user_id=user_id).first()
    following = Person.objects.get(user_id=user_id)
    usersid = user_id
    if following in person.following.all():
        status = False
        following.follower.remove(person)
    else:
        status = True
        following.follower.add(person)
    following.save()
    return JsonResponse({'follower':profile.follower.count(),'following':User.objects.get(id=user_id).following.all().count(),"followed":status, "usersid":usersid}, status=200)

def updatel(request,post_id):
    person = request.user
    post = Post.objects.get(id=post_id)
    if post in person.allpost.all():
        status = False
        post.likes.remove(person)
    else:
        status = True
        post.likes.add(person)
    post.save()
    return JsonResponse({"liked": status, "newamount": post.likes.count()},status=200)

def profile(request,user_id):
    profile = Person.objects.filter(user_id=user_id).first()
    following = Person.objects.get(user_id=user_id)
    person = request.user
    user = profile.user.username
    followstatus = following in person.following.all()

    if request.user.id == user_id:
        followallow = False
    else:
        followallow = True

    status={
        'userid':profile.id,
        'user':user,
        'status':followstatus,
        'follower':profile.follower.count(),
        'following':User.objects.get(id=user_id).following.all().count(),
        'followallow':followallow,
    }
    return JsonResponse(status,safe=False)

def load(request):
    user=request.user
    allpost=Post.objects.all()
    allpost=allpost.order_by("-datentime").all()
    posts = []
    for i in range(len(allpost)):
        likedstatus=request.user in allpost[i].likes.all()
        posts.append({'date': allpost[i].datentime.strftime('%H:%M %d %b %Y'), 
                    'content': allpost[i].content,
                    'likes': allpost[i].likes.count(),
                    'edit':allpost[i].user == user,
                    'liked':likedstatus,
                    'id':allpost[i].id
                    })

    return JsonResponse(posts, safe=False)


def paginate(request):
    posts=Post.objects.all().order_by('datentime').reverse()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    lastpage = paginator.num_pages
    poster = []
    for i in range(len(page_obj)):
        likedstatus=request.user in page_obj[i].likes.all()
        poster.append({
                    'user':page_obj[i].user.username,
                    'userid':page_obj[i].user.id,
                    'datentime': page_obj[i].datentime.strftime('%H:%M %d %b %Y'), 
                    'content': page_obj[i].content,
                    'likes': page_obj[i].likes.count(),
                    'edit':page_obj[i].user == request.user,
                    'liked':likedstatus,
                    'id':page_obj[i].id,
                    'lastpage':lastpage
                    })

    return JsonResponse(poster, safe=False)

def loadfpost(request):
    followedperson = request.user.following.all()
    easy=[]
    for i in range(len(followedperson)):
        easy.append(followedperson[i].user.id)
    posts = Post.objects.filter(user__in=easy).all().reverse()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    lastpage = paginator.num_pages
    poster = []
    for i in range(len(page_obj)):
        likedstatus=request.user in page_obj[i].likes.all()
        poster.append({
                    'user':page_obj[i].user.username,
                    'userid':page_obj[i].user.id,
                    'datentime': page_obj[i].datentime.strftime('%H:%M %d %b %Y'), 
                    'content': page_obj[i].content,
                    'likes': page_obj[i].likes.count(),
                    'edit':page_obj[i].user == request.user,
                    'liked':likedstatus,
                    'id':page_obj[i].id,
                    'lastpage':lastpage,
                    })
    
    return JsonResponse(poster, safe=False)

def loadppost(request,user_id):
    posts=Post.objects.filter(user_id=user_id).order_by('datentime').reverse()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    lastpage = paginator.num_pages
    poster = []
    for i in range(len(page_obj)):
        likedstatus=request.user in page_obj[i].likes.all()
        poster.append({
                    'user':page_obj[i].user.username,
                    'datentime': page_obj[i].datentime.strftime('%H:%M %d %b %Y'), 
                    'content': page_obj[i].content,
                    'likes': page_obj[i].likes.count(),
                    'edit':page_obj[i].user == request.user,
                    'liked':likedstatus,
                    'id':page_obj[i].id,
                    'lastpage':lastpage,
                    })
    return JsonResponse(poster, safe=False)


    


