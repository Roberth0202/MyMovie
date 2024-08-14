from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from .movie_functions import *
from django.core.exceptions import ValidationError
from .utils import adicionar_filme, remover_filme


def add_to_list(request, movie_id):
    try:
        adicionar_filme(request.user, movie_id)
        messages.success(request, 'Filme adicionado à sua lista!')
    except ValidationError as e:
        messages.error(request, f'Erro: {e}')
    except Exception as e:
        messages.error(request, f'Houve um erro ao adicionar o filme: {e}')

@login_required
def remove_from_list(request, movie_id):
    try:
        remover_filme(request.user, movie_id)
        messages.success(request, 'Filme removido da sua lista!')
    except Exception as e:
        messages.error(request, f'Houve um erro ao remover o filme: {e}')
        

#Tela home
def home(request):
    if request.method == "POST":
        # Verifica qual botão/formulário foi enviado
        movie_id = request.POST.get('movie_id')  # O 'movie_id' deve vir do formulário/elemento HTML
        action = request.POST.get('action')  # O 'action' pode ser 'add' ou 'remove' dependendo do formulário

        if action == 'add':
            add_to_list(request, movie_id)
        elif action == 'remove':
            remove_from_list(request, movie_id)

    popular_movie = filme_populares
    popular_serie = serie_populares
    search = search_movies
    context = {
        'popular_movie' : popular_movie,
        'popular_serie' : popular_serie,
        'search' : search,
    }
    return render(request, 'html/home.html', context)

def pesquisa(request):
    query = request.GET.get('q')
    searches = search_movies(query)
    context = {
        'search' : searches,
    }
    return render(request, 'html/search.html', context)

def detail_movie(request, movie_id):
    if request.method == "POST":
        # Verifica qual botão/formulário foi enviado
        movie_id = request.POST.get('movie_id')  # O 'movie_id' deve vir do formulário/elemento HTML
        action = request.POST.get('action')  # O 'action' pode ser 'add' ou 'remove' dependendo do formulário

        if action == 'add':
            add_to_list(request, movie_id)
        elif action == 'remove':
            remove_from_list(request, movie_id)
            
    filme = info_movie(movie_id)
    context ={
        'filme' : filme,
    }
    return render(request, 'html/infomovie.html', context)

@login_required
def detail_serie(request, series_id):
    if request.method == "POST":
        # Verifica qual botão/formulário foi enviado
        movie_id = request.POST.get('movie_id')  # O 'movie_id' deve vir do formulário/elemento HTML
        action = request.POST.get('action')  # O 'action' pode ser 'add' ou 'remove' dependendo do formulário

        if action == 'add':
            add_to_list(request, movie_id)
        elif action == 'remove':
            remove_from_list(request, movie_id)
    serie = info_serie(series_id)
    context = {
        'serie' : serie,
    }
    return render(request, 'html/infoserie.html', context)

#tela de login
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/page/home/')
        else:
            messages.add_message(request, messages.ERROR, 'Usuário ou senha incorretos')
            return render(request, 'html/login.html')
    return render(request, 'html/login.html')

#logout
def logout_view(request):
    logout(request)
    return redirect('/page/home')

#tela de cadastro
def register(request):
    if request.method == "POST":
        username = request.POST.get("name")
        email1 = request.POST.get("1email")
        email2 = request.POST.get("2email")
        password1 = request.POST.get("pass1")
        password2 = request.POST.get("pass2")
        
        if password1 == password2 and email1 == email2:
            user = User.objects.create_user(username=username, email=email1, password=password1)
            user.save()
            return render(request, 'html/login.html')
        else:
            messages.add_message(request, messages.ERROR, 'Senha ou email não conferem')
            return render(request, 'html/cad.html')


    return render(request, 'html/cad.html')
