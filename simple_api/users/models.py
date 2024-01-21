from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length = 50, blank = False)
    password = models.CharField(max_length = 50, blank = False)
    email = models.EmailField(default= "user@email.com", blank = False)
    q_posts = models.BigIntegerField(default = 0)
    q_followers = models.BigIntegerField(default = 0)
    q_following = models.BigIntegerField(default = 0)

    def __str__(self):
        return f"User - Username: {self.username}, Posts: {self.q_posts}, Followers: {self.q_followers}, Following: {self.q_following}"
    
class Post(models.Model):
    description = models.CharField(max_length = 200)
    midia = models.URLField(default = "https://cdn.vuetifyjs.com/images/cards/docks.jpg")
    likes = models.BigIntegerField(default = 0)
    date_post = models.DateField(timezone.now())
    locate = models.CharField(max_length = 50, default = "Coxim, Mato Grosso do Sul, Brasil")
    author = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return f"Post - Description: {self.description}, Likes: {self.likes}, Locate: {self.locate}, Date: {self.date_post}, Author: {self.author.username}"