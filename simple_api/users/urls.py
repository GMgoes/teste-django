from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="GET - Posts (feed)"),
    path("search-user/<str:username>", views.get_user, name="search_user"),
    path("<str:username>/new-post", views.create_post, name="create_post"),
    path("search-post/<int:post_id>", views.get_post, name="search_post"),
    path("<str:username>/user-posts", views.list_posts, name = "search_posts_of_a_user"),
    path("like-post/<int:post_id>", views.update_post, name="like_a_post"),
]