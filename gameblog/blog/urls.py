from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('game/<int:game_id>', views.game_view, name='game'),
    path('delete_post/<int:post_id>', views.delete_post_view, name='delete'),
    path('create_game/', views.create_game_view, name='create_game'),
    path('edit_game/<int:game_id>', views.create_game_view, name='edit_game'),
    path('delete_game/<int:game_id>', views.delete_game_view, name='delete_game'),
    path('create_genre/', views.create_genre_view, name='create_genre'),
    path('add_genre/<int:game_id>/<str:genre>', views.add_genre_view, name='add_genre'),
]