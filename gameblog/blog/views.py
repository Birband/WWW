from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, CreateUserForm, PostForm, GameForm, GenreForm
from .models import Game, Post, Genre


def home_view(request):
    # check session, if logged in display name
    name = None
    if request.user.is_authenticated:
        name = request.user.username
    
    search_phrase = request.GET.get('search', '')
    if search_phrase:
        games = Game.objects.filter(title__icontains=search_phrase)
    else:
        games = Game.objects.all()
        
    return render(request, 'blog/home.html', {'name': name, 'games': games})

def login_view(request):
    wrong_credentials = False
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            wrong_credentials = True
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form, 'wrong_credentials': wrong_credentials})
    
def logout_view(request):
    logout(request)
    return redirect('home')

def game_view(request, game_id):
    game = Game.objects.get(id=game_id)
    posts = Post.objects.filter(game=game)
    genres = Genre.objects.filter(games=game)
    all_genres = Genre.objects.all()

    already_posted = False
    # check if user is authenticated
    if request.user.is_authenticated:
        # check if user already posted
        user_post = Post.objects.filter(game=game, author=request.user)
        if user_post:
            already_posted = True

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post(
                content=form.cleaned_data['content'],
                rating=form.cleaned_data['rating'],
                author=request.user,
                game=game
            )
            if already_posted:
                posts_count = Post.objects.filter(game=game).count()
                game.rating = (game.rating * posts_count - user_post[0].rating + post.rating) / posts_count
                game.save()
                user_post[0].content = form.cleaned_data['content']
                user_post[0].rating = form.cleaned_data['rating']
                user_post[0].save()
            else:
                post.save()
                posts_count = Post.objects.filter(game=game).count()
                game.rating = (game.rating * (posts_count - 1) + post.rating) / posts_count
                game.save()
            return redirect('game', game_id=game_id)
    else:
        if already_posted:
            form = PostForm(initial={'content': user_post[0].content, 'rating': user_post[0].rating})
        else:
            form = PostForm()

    return render(request, 'blog/game.html', {'game': game, 'posts': posts, 'genres': genres, 'form': form, 'already_posted': already_posted, 'post_id': user_post[0].id if already_posted else None, 'game_id': game_id, 'all_genres': all_genres})

def register_view(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CreateUserForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required(login_url='/login/')
def delete_post_view(request, post_id):
    post = Post.objects.get(id=post_id)
    game_id = post.game.id
    posts_count = Post.objects.filter(game=post.game).count()
    if posts_count == 1:
        post.game.rating = 0
    else:
        post.game.rating = (post.game.rating * posts_count - post.rating) / (posts_count - 1)

    post.game.save()
    post.delete()
    return redirect('game', game_id=game_id)

@login_required(login_url='/login/')
def create_game_view(request, game_id=None):
    edit = False
    if game_id is not None:
        edit = True
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            if edit:
                game = Game.objects.get(id=game_id)
                game.title = form.cleaned_data['title']
                game.description = form.cleaned_data['description']
                game.release_date = form.cleaned_data['release_date']
                game.developer = form.cleaned_data['developer']
                game.publisher = form.cleaned_data['publisher']
                if form.cleaned_data['cover']:
                    game.cover = form.cleaned_data['cover']
                game.save()
            else:
                game = Game(
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    release_date=form.cleaned_data['release_date'],
                    developer=form.cleaned_data['developer'],
                    publisher=form.cleaned_data['publisher'],
                    cover=form.cleaned_data['cover']
                )
                game.save()
            return redirect('home')
    else:
        if game_id:
            try:
                game = Game.objects.get(id=game_id)
                form = GameForm(initial={'title': game.title, 'description': game.description, 'release_date': game.release_date, 'developer': game.developer, 'publisher': game.publisher})
            except Game.DoesNotExist:
                form = GameForm()
        else:
            form = GameForm()

    return render(request, 'blog/create_game.html', {'form': form, 'edit': edit})

@login_required(login_url='/login/')
def delete_game_view(request, game_id):
    posts = Post.objects.filter(game=game_id)
    for post in posts:
        post.delete()
    game = Game.objects.get(id=game_id)
    game.delete()
    return redirect('home')

@login_required(login_url='/login/')
def add_genre_view(request, game_id, genre):
    return_to = request.META.get('HTTP_REFERER')
    game = Game.objects.get(id=game_id)
    genre = Genre.objects.get(name=genre)
    # if game already in genre.games, remove it
    if game in genre.games.all():
        genre.games.remove(game)
    else:
        genre.games.add(game)
    genre.save()
    return redirect(return_to)

@login_required(login_url='/login/')
def create_genre_view(request):
    already_exists = False
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            if Genre.objects.filter(name=form.cleaned_data['name']):
                already_exists = True
                form = GenreForm()
            else:  
                genre = Genre(name=form.cleaned_data['name'])
                genre.save()
                return redirect('create_genre')
    else:
        form = GenreForm()
    return render(request, 'blog/create_genre.html', {'form': form, 'already_exists': already_exists})