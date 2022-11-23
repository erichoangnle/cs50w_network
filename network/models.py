from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.username} created on {self.time}"

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return f"{self.user.username} following {self.follow.username}"

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    content = models.CharField(max_length=1300)
    likes = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Posted by {self.poster.username} on {self.time}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likers_list")
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked")

    def __str__(self):
        return f"{self.liker.username} liked {self.post}"
