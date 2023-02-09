from time import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import CharField
from django.utils import timezone





class User(AbstractUser):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.username}"

class Market(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.CharField(max_length=200, default=None, blank=True, null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True)
    comment = models.ManyToManyField('Comment', blank=True)
    category = models.CharField(max_length=100, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    og_bid = models.IntegerField()
    bid = models.ManyToManyField('bid',blank=True)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    status = models.BooleanField(default=True)
    last_bid = models.IntegerField(blank=True, null=True)
    winner = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.product}"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.TextField()
    def __str__(self):
        return f"{self.user},{self.content}"


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    bid_prize = models.IntegerField()
    time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.bid_prize}"

class WL(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, blank=False, null=True) 
    wl = models.ForeignKey('Market', on_delete=models.CASCADE, blank=False, null=True)
    def __str__(self):
        return f"{self.user}:{self.wl}"





