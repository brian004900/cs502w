from django.contrib import admin
from .models import User, Comment, Market, Bid, WL



# Register your models here.

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Market)
admin.site.register(Bid)
admin.site.register(WL)