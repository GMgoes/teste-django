from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from .models import User, Post
from django.views.decorators.csrf import csrf_exempt
import json
import random

# Create your views here.

@require_http_methods("GET")
def index(request):
    random_numbers = []
    number_of_posts = len(Post.objects.all())
    feed = []
    while len(random_numbers) < 5:
        random_number = random.randint(1, number_of_posts)
        if random_number not in random_numbers:
            random_numbers.append(random_number)
    for i in random_numbers:
        post = Post.objects.get(id=i)
        feed.append(post)
    feed_data = {"posts":[{'id': post.id, 'description': post.description,'midia': post.midia,'locate': post.locate, 'likes': post.likes, 'date_post': post.date_post, 'author': post.author.username} for post in feed], "posts_quantity": len(feed)}
    return JsonResponse(feed_data, safe=False)

@require_http_methods("GET")
def get_user(request, username):
    user = get_object_or_404(User, username=username)
    user_data = {"user":{"username":user.username, "posts": user.q_posts, "followers": user.q_followers, "following": user.q_following}}
    return JsonResponse(user_data, safe=False)

@csrf_exempt
@require_http_methods("POST")
def create_post(request, username):
    user = get_object_or_404(User, username=username)
    data = json.loads(request.body.decode("utf-8"))
    new_post = Post(description=data.get("description"),midia=data.get("midia"),locate=data.get("locate"),date_post=timezone.now(),author=user)
    new_post.save()
    user.q_posts = user.q_posts + 1
    user.save()
    return HttpResponse(status=201)

@require_http_methods("GET")
def list_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    posts_data = {"posts":[{'description': post.description,'midia': post.midia,'locate': post.locate, 'likes': post.likes, 'date_post': post.date_post, 'author': post.author.username} for post in posts], "posts_quantity": len(posts), "user":username}
    return JsonResponse(posts_data, safe=False)

@require_http_methods("GET")
def get_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_data = {'id': post.id, 'description': post.description,'midia': post.midia,'locate': post.locate, 'likes': post.likes, 'date_post': post.date_post, 'author': post.author.username}
    return JsonResponse(post_data, safe=False)

@csrf_exempt
@require_http_methods("PUT")
def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.likes = post.likes + 1
    post.save()
    post_data = {'id': post.id, 'description': post.description,'midia': post.midia,'locate': post.locate, 'likes': post.likes, 'date_post': post.date_post, 'author': post.author.username}
    return JsonResponse(post_data, safe=False)
