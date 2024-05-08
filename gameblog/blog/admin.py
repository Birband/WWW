from django.contrib import admin

from .models import Game, Post, Genre

# Register your models here.
admin.site.register(Game)
admin.site.register(Post)
admin.site.register(Genre)