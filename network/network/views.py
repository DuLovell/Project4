import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import User, Post, Follow, Like


def index(request, num):
    
    posts = Post.objects.all().order_by("-created")

    posts_pages = Paginator(posts, 10)

    current_page = posts_pages.page(num)
    

    now_date = datetime.now()
    return render(request, "network/index.html", {
        "posts": posts,
        "posts_pages": posts_pages,
        "current_page": current_page,
        "pages_number": range(1, posts_pages.num_pages + 1),
        })

def following_index(request, num):
    following_set = Post.objects.none()
    follow_obj_set = User.objects.get(username=request.user).follows.all()
    
    for follow in follow_obj_set:
        following_set = ( following_set | follow.user_to_follow.posts.all() ).order_by("-created")
    
    posts_pages = Paginator(following_set, 10)
    current_page = posts_pages.page(num)

    return render(request, "network/following.html", {
        "following_set": following_set,
        "posts_pages": posts_pages,
        "current_page": current_page,
        "pages_number": range(1, posts_pages.num_pages + 1),
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
            return HttpResponseRedirect(reverse("index", kwargs={"num": 1}))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index", kwargs={"num": 1}))


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
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index", kwargs={"num": 1}))
    else:
        return render(request, "network/register.html")

def if_authenticated(request):
    if request.user.is_authenticated:
        return JsonResponse("True", safe=False)
    return JsonResponse("False", safe=False)

@csrf_exempt
def create(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        user = request.user
        content = data.get("content", "")
        post = Post(user=user, text=content)
        post.save()
        return HttpResponseRedirect(reverse("index", args={"num": 1}))
    
    return HttpResponse("Anything")

@csrf_exempt
def manage_like(request):
    

    data = json.loads(request.body)
    post_author = data.get("username", "")
    post_content = data.get("content", "")
    post_created = data.get("created_date", "")

    post = Post.objects.filter(text=post_content)[0]
    post_likes = post.likes.filter(user=request.user)
    if not post_likes:
        new_like = Like(user=request.user, post=post)
        new_like.save()
        
        post.liked.add(request.user)

        likes = post.likes.count()
        
        return JsonResponse(f"{likes}", safe=False)

    else:
        old_like = post.likes.get(user=request.user)
        old_like.delete()
        
        post.liked.remove(request.user)
        
        likes = post.likes.count()

        return JsonResponse(f"{likes}", safe=False)  

@csrf_exempt 
def manage_follow(request):
    data = json.loads(request.body)
    current_user = User.objects.get(username=request.user)
    profile_user = User.objects.get(username=data.get('profile_name', "").strip())
    
    if profile_user.all_followers.filter(followers=current_user):
        old_follow_obj = Follow.objects.get(user_to_follow=profile_user)
        old_follow_obj.followers.remove(current_user)

        profile_followers = profile_user.all_followers.first().followers.count()
        return JsonResponse(["Follow", profile_followers], safe=False)
    else:
        try:
            old_follow_obj = Follow.objects.get(user_to_follow=profile_user)
            old_follow_obj.followers.add(current_user)
        except Follow.DoesNotExist:
            follow_obj = Follow(user_to_follow=profile_user)
            follow_obj.save()
            follow_obj.followers.add(current_user)

        profile_followers = profile_user.all_followers.first().followers.count() 
        return JsonResponse(["Unfollow", profile_followers], safe=False)

  
def profile(request, username, num):
    user = User.objects.get(username=username)

    user_following = Follow.objects.all()


    if user.all_followers.filter(followers=request.user):
        is_followed = True
    else:
        is_followed = False

    posts = user.posts.all().order_by("-created")

    posts_pages = Paginator(posts, 10)
    current_page = posts_pages.page(num)
    
    return render(request, "network/profile.html", {
        "profile": user,
        "current_user": request.user,
        "is_followed": is_followed,
        "user_following": user_following,
        "posts": posts,
        "posts_pages": posts_pages,
        "current_page": current_page,
        "pages_number": range(1, posts_pages.num_pages + 1),
        })

@csrf_exempt
def edit_post(request):
    data = json.loads(request.body)

    post_author = data.get("username", "")
    new_content = data.get("new_content")
    old_content = data.get("old_content")
    post_created = data.get("created_date", "")

    post = Post.objects.get(text=old_content)

    post.text = new_content
    post.save()

    return JsonResponse(f"{new_content}", safe=False)
