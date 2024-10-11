from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from .movie_functions import *
from django.core.exceptions import ValidationError
from .utils import adicionar_midia, remover_midia
from .models import Lista


#Adiciona filme/serie na lista
@login_required(login_url = '/page/login/')
def add_to_list(request, media_id, midia_type):
    try:
        adicionar_midia(request.user, media_id, midia_type)
        messages.success(request, 'Filme/Série adicionado(a) à sua lista!')
    except ValidationError as e:
        messages.error(request, f'Erro: {e}')
    except Exception as e:
        messages.error(request, f'Houve um erro ao adicionar o filme/série: {e}')

#remove o filme da lista
@login_required(login_url ='/page/login/')                
def remove_from_list(request, media_id, midia_type):
    try:
        remover_midia(request.user, media_id, midia_type)
        messages.success(request, 'Filme/Série removido(a) da sua lista!')
    except Exception as e:
        messages.error(request, f'Houve um erro ao remover o filme/série: {e}')
        
#Tela home
def home(request):
    popular_movie = filme_populares
    popular_serie = serie_populares
    search = search_movies
    context = {
        'popular_movie' : popular_movie,
        'popular_serie' : popular_serie,
        'search' : search,
    }
    return render(request, 'html/home.html', context)

#Pesquisa
def pesquisa(request):
    query = request.GET.get('q')
    searches = search_movies(query)
    context = {
        'search' : searches,
    }
    return render(request, 'html/search.html', context)

# Detalhes do filme
def detail_movie(request, movie_id):
    if request.method == "POST":
        media_id = request.POST.get('media_id')
        midia_type = request.POST.get('midia_type')
        action = request.POST.get('action')
        
        if action == 'add':
            add_to_list(request, media_id, midia_type)
        elif action == 'remove':
            remove_from_list(request, media_id, midia_type)

    filme = info_movie(movie_id)
    context = {
        'filme': filme,
    }
    return render(request, 'html/infomovie.html', context)

# Detalhes da série
def detail_serie(request, series_id):
    if request.method == "POST":
        media_id = request.POST.get('media_id')
        midia_type = request.POST.get('midia_type')
        action = request.POST.get('action')
        
        if action == 'add':
            add_to_list(request, media_id, midia_type)
        elif action == 'remove':
            remove_from_list(request, media_id, midia_type)

    serie = info_serie(series_id)
    context = {
        'serie': serie,
    }
    return render(request, 'html/infoserie.html', context)

#Lista de filmes/series do usuario
@login_required(login_url='/page/login/')
def lista(request):
    object_list = Lista.objects.filter(user_id=request.user)
    
    # Inicializa variáveis para evitar erros se as condições não forem atendidas
    midias = []

     # Iterar sobre os objetos encontrados e processar conforme o tipo de mídia
    for obj in object_list:
        if obj.midia_type == 'movie':
            filme = info_movie(obj.media_id)  # Chamar a função para obter os detalhes do filme
            midias.append(filme)
        elif obj.midia_type == 'tv':
            serie = info_serie(obj.media_id)  # Chamar a função para obter os detalhes da série
            midias.append(serie)
    
    context = {
        'midias' : midias,
    }
    return render(request, "html/lista.html", context)

def filmes(request):
    page = request.GET.get("page", 1)
    
    try:
        page = int(page)  # Converte para inteiro
    except ValueError:
        page = 1  # Se falhar, define 1
    
    all_movies = Filmes(page)  # Call Filmes function
    
    # Cria um objeto de paginação simulado
    paginator = {
        'has_previous' : all_movies['page'] > 1,
        'previous_page_number' : all_movies['page'] - 1 if all_movies['page'] > 1 else None,
        'has_next' : all_movies['page'] < all_movies['total_pages'],
        'next_page_number' : all_movies['page'] + 1 if all_movies['page'] < all_movies['total_pages'] else None,
        'number' : all_movies['page'],
        'paginator' : {
            'num_pages': all_movies['total_pages']
        }
    }
    
    context = {
        'all_movies': all_movies['results'], #lista de filmes
        'page_obj' : paginator #objeto de paginação
    }
    return render(request, 'html/filmes.html', context)

def series(request):
    return render(request, 'html/series.html')
    
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
