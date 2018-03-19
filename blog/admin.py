from django.contrib import admin
from .models import Post
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


admin.site.unregister(Group)
admin.site.register(Post)
