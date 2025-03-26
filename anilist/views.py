from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.password_validation import get_password_validators
from django.core.exceptions import ValidationError
from django.conf import settings
from .movie_functions import *
from django.core.exceptions import ValidationError
from .utils import adicionar_midia, remover_midia
from .models import Lista

# Função para verificar se a mídia já está na lista
def verificar_midia_na_lista(user_id, media_id, midia_type):
    return Lista.objects.filter(user_id=user_id, media_id=media_id, midia_type=midia_type).exists()

#Adiciona filme/serie na lista
@login_required(login_url = '/page/login/')
def add_to_list(request, media_id, midia_type):
    """Adiciona uma mídia à lista do usuário.

    Args:
        request (HttpRequest): O objeto de solicitação HTTP.
        media_id (int): O ID da mídia a ser adicionada.
        midia_type (str): O tipo de mídia (por exemplo, 'filme', 'série').

    Returns:
        HttpResponse: Redireciona para a página de login se o usuário não estiver autenticado.
        Caso contrário, adiciona a mídia à lista do usuário e exibe uma mensagem de sucesso.
        Se ocorrer um erro (por exemplo, a mídia já está na lista), exibe uma mensagem de erro.
    """
    try:
        adicionar_midia(request.user, media_id, midia_type)
        messages.success(request, 'Foi adicionado á sua lista!', extra_tags='sucesso')
    except Exception:
        messages.error(request, f'Mídia ja está na sua lista.', extra_tags='erro')

@login_required(login_url = '/page/login/')
def remove_from_list(request, media_id, midia_type):
    """Remove uma mídia da lista do usuário.
    Args:
        request (HttpRequest): O objeto de solicitação HTTP que contém informações sobre a solicitação atual.
        media_id (int): O ID da mídia a ser removida.
        midia_type (str): O tipo de mídia a ser removida.
    Raises:
        ValueError: Se a mídia não estiver na lista do usuário.
    Exceções:
        ValueError: Se a mídia não estiver na lista do usuário.
        Exception: Se ocorrer um erro ao remover a mídia da lista.
    Mensagens:
        messages.success: Se a mídia for removida com sucesso da lista do usuário.
        messages.error: Se ocorrer um erro ao remover a mídia da lista ou se a mídia não estiver na lista do usuário.
    """
    try:
        if not verificar_midia_na_lista(request.user, media_id, midia_type):  # Adicione uma verificação
            raise ValueError("Mídia não está na lista.")
        
        remover_midia(request.user, media_id, midia_type)
        messages.success(request, 'Foi removido da sua lista!', extra_tags='sucesso')
    except ValueError as e:
        messages.error(request, str(e), extra_tags='erro')
    except Exception:
        messages.error(request, 'Erro ao remover mídia da lista.', extra_tags='erro')

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
        'page_range' : range(1 , all_movies['total_pages'] + 1),
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
    page = request.GET.get("page", 1)
    
    try:
        page = int(page)  # Converte para inteiro
    except ValueError:
        page = 1  # Se falhar, define 1
        
    all_series = Series(page)
    
    # Cria um objeto de paginação simulado
    paginator = {
        'has_previous' : all_series['page'] > 1,
        'previous_page_number' : all_series['page'] - 1 if all_series['page'] > 1 else None,
        'has_next' : all_series['page'] < all_series['total_pages'],
        'next_page_number' : all_series['page'] + 1 if all_series['page'] < all_series['total_pages'] else None,
        'number' : all_series['page'],
        'page_range' : range(1 , all_series['total_pages'] + 1),
        'paginator' : {
            'num_pages': all_series['total_pages']
        }
    }
    
    context = {
        'all_series' : all_series['results'],
        'page_obj' : paginator
    }
    return render(request, 'html/series.html', context)
    
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
            messages.add_message(request, messages.ERROR, 'Usuário ou senha incorretos', extra_tags="login")
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
        
        # Verificar se as senhas e emails são iguais
        if password1 != password2:
            messages.error(request, 'As senhas não conferem.', extra_tags='erro')
            return render(request, 'html/cad.html')

        # Verificar se os emails são iguais
        if email1 != email2:
            messages.error(request, 'Os emails não conferem.', extra_tags='erro')
            return render(request, 'html/cad.html')

        # Obtém os validadores configurados no settings.py
        validators = get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
        
        # Verifica cada validador sequencialmente
        for validator in validators:
            try:
                validator.validate(password1)
            except ValidationError as e:
                messages.error(request, e.messages[0], extra_tags='erro')
                return render(request, 'html/cad.html')

        # Verificar se o nome de usuário ou email já existem
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já existe.', extra_tags='erro')
            return render(request, 'html/cad.html')
        
        # Verificar se o email já está em uso
        if User.objects.filter(email=email1).exists():
            messages.error(request, 'Email já está em uso.', extra_tags='erro')
            return render(request, 'html/cad.html')

        user = User.objects.create_user(username=username, email=email1, password=password1)
        user.save()
        messages.success(request, 'Cadastro realizado com sucesso!', extra_tags='sucesso')
        return redirect('/page/login/')
    
    return render(request, 'html/cad.html')