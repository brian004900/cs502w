from operator import truediv
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass
    def __str__(self):
        return f"{self.id}"

class Person(models.Model):
    user = models.ForeignKey("User",on_delete=models.CASCADE)
    follower = models.ManyToManyField("User", related_name="following", blank=True)

class Post(models.Model):
    user = models.ForeignKey("User" ,on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    datentime = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("User", blank=True, related_name="allpost")

    def serialize(self):
        return {
            "user": self.user.username,
            "content":self.content,
            "likes": self.likes.count(),
            "datentime": self.datentime.strftime("%b %#d %Y, %#I:%M %p"),
        }
