from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import User


def index(request):
    """
    If request method is POST, create an object of Post class with given attributes, save
    new post object to database and redirect user to index page. If request method is GET,
    render main page with posts from database in reverse chronological order.
    """
    if request.method == "POST":

        # Create new instance of post
        post = Post(
            poster = request.user,
            content = request.POST["content"],
            likes = 0
        )
        # Save post to database
        post.save()

        return HttpResponseRedirect(reverse("index"))
    
    else:

        # Get all posts in sort by reverse chronological order
        posts = Post.objects.all().order_by("-time")

        # Get a list of post user liked
        if request.user.is_authenticated:
            liked = list(Like.objects.filter(liker=request.user).values_list('post', flat=True))
            liked_list = Post.objects.filter(pk__in=liked)
        else:
            liked_list = []

        # create paginator instance with 10 posts per page
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/index.html", {
            "page_obj": page_obj,
            "liked_list": liked_list
        })

    
@csrf_exempt
@login_required
def edit(request, post_id):
    """
    Let an authenticated user edit his or her own post.
    """
    # Get post to edit by post_id
    post = Post.objects.get(pk=post_id)

    # Make sure only authenticated original poster can edit post
    if request.user.is_authenticated and request.user == post.poster:
        if request.method == "PUT":

            # Get data from PUT request
            data = json.loads(request.body)

            # Replace post content with new data
            if data.get("content") is not None:
                post.content = data["content"]

            post.save()

            return HttpResponse(status=204)
        
        else:

            # Make sure user can't edit post through URL route
            return render(request, "network/error.html", {
                "message": "Don't try editting this way, mate!"
            })
        
    else:

        # Error message for unauthoried attempt to edit post
        return render(request, "network/error.html", {
            "message": "Permission denied"
        })

    
@csrf_exempt
@login_required
def like(request, post_id):
    """
    Like or unlike a post.
    """
    # Get post that are being liked or unliked
    post = Post.objects.filter(pk=post_id).first()

    if request.method == "PUT":

        data = json.loads(request.body)

        # Update post like if action is like
        if data.get("action") == "Like":

            post.likes += 1
            like = Like(
                post = post,
                liker = request.user
            )
            like.save()
            post.save()

            return HttpResponse(status=204)
        
        # Update post like if action is unlike
        else:

            post.likes -= 1
            post.save()
            Like.objects.filter(post=post, liker=request.user).delete()

            return HttpResponse(status=204)


def profile(request, id):
    """
    Render the profile page of any user.
    """
    # Get user object
    profile = User.objects.get(pk=id)
    # Get posts created by user
    posts = profile.post.order_by("-time")
    is_following = False

    # Check if is currently following this user
    if request.user.is_authenticated:
        for following in request.user.followers.all():
            if profile == following.follow:
                is_following = True

    return render(request, "network/profile.html", {
        "profile": profile,
        "posts": posts,
        "is_following": is_following
    })


@login_required
def follow(request, id):
    """
    Follow a user.
    """
    follow = Follow(
        user = request.user,
        follow = User.objects.get(pk=id)
    )
    follow.save()
    return HttpResponseRedirect(f"/profile/{id}")


@login_required
def unfollow(request, id):
    """
    Unfollow a user.
    """
    Follow.objects.filter(user=request.user, follow=User.objects.get(pk=id)).delete()
    return HttpResponseRedirect(f"/profile/{id}")


@login_required
def following(request):
    """
    Render a page with all posts from people user is following in reverse chronological order.
    """
    # Get a list of all people user is following
    liked = list(Like.objects.filter(liker=request.user).values_list('post', flat=True))
    liked_list = Post.objects.filter(pk__in=liked)
    followings = [item.follow for item in request.user.followers.all()]
    posts = []

    # Get a list of all post from people user is following
    if followings:
        for following in followings:
            post_objects = Post.objects.filter(poster=following).order_by("-time")
            for post_object in post_objects:
                posts.append(post_object)

    # Sort post in reverse chronological order
    posts.sort(key=lambda x: x.time, reverse=True)

    # Create a paginator object with 10 posts per page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_obj": page_obj,
        "liked_list": liked_list
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
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
