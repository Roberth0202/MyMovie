from django.urls import path
from . import views

app_name = "anilist"
urlpatterns = [
    path('home/', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
    path('filme/<movie_id>', views.detail_movie, name="filme"),
    path('serie/<series_id>', views.detail_serie, name="serie"),
    path('pesquisa/', views.pesquisa, name="pesquisa"),
    ]
