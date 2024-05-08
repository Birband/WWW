from django.db import models
from django.contrib.auth.models import User, Permission
from django.core.validators import MinValueValidator, MaxValueValidator

class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    rating = models.FloatField(default=0.0) 
    developer = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    cover = models.ImageField(upload_to='covers/', blank=True)

class Genre(models.Model):
    name = models.CharField(max_length=255)
    games = models.ManyToManyField(Game, blank=True)

class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

