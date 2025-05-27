from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.password_validation import get_password_validators
from django.contrib.auth.views import PasswordResetConfirmView
from .utils import adicionar_midia, remover_midia, CustomSetPasswordForm
from django.core.exceptions import ValidationError
from django.conf import settings
from .movie_functions import *
from .models import Lista
from django.http import JsonResponse
import asyncio
from asgiref.sync import sync_to_async

#------------------------------------------------- FUNÇÃO PARA VERIFICAR SE A MIDIA ESTA NA LISTA --------------------------------------
def verificar_midia_na_lista(user_id, media_id, midia_type):
    """Verifica se uma mídia já está na lista do usuário.

    Args:
        user_id (int): O ID do usuário.
        media_id (int): O ID da mídia.
        midia_type (str): O tipo da mídia (por exemplo, 'filme', 'série').

    Returns:
        bool: Retorna True se a mídia já estiver na lista, False caso contrário.
    """
    return Lista.objects.filter(user_id=user_id, media_id=media_id, midia_type=midia_type).exists()

#--------------------------------------------------- ADICIONAR FILME/SERIE NA LISTA DO USUARIO -------------------------------------------
@login_required(login_url = '/login/')
async def add_to_list(request, media_id, midia_type):
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
        await asyncio.to_thread(adicionar_midia, request.user, media_id, midia_type)
        
    except Exception:
        messages.error(request, f'Mídia ja está na sua lista.', extra_tags='erro')

#--------------------------------------------------- REMOVE FILME/SÉRIE DA LISTA DO USUARIO ---------------------------------------------
@login_required(login_url = '/login/')
async def remove_from_list(request, media_id, midia_type):
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
        
        await asyncio.to_thread(remover_midia, request.user, media_id, midia_type)
        messages.success(request, 'Foi removido da sua lista!', extra_tags='sucesso')
    except ValueError as e:
        messages.error(request, str(e), extra_tags='erro')
    except Exception:
        messages.error(request, 'Erro ao remover mídia da lista.', extra_tags='erro')

# ----------------------------------------------------- FILMES E SÉRIES EM ALTA ------------------------------------------------
def home(request):
    popular_movie = filme_populares
    popular_serie = serie_populares
    lancamentos_filmes = lancamento_filmes
    search = search_movies
    
    context = {
        'popular_movie' : popular_movie,
        'popular_serie' : popular_serie,
        'lancamentos_filmes' : lancamentos_filmes,
        'search' : search,
    }
    return render(request, 'html/home.html', context)

#--------------------------------------------------------- FUNÇÃO DE PESQUISA --------------------------------------------------
def pesquisa(request):
    query = request.GET.get('q')
    searches = search_movies(query)
    context = {
        'search' : searches,
    }
    return render(request, 'html/search.html', context)

#--------------------------------------------------------- DETALHES DO FILME --------------------------------------------------
async def detail_movie(request, movie_id):
    if request.method == "POST":
        media_id = request.POST.get('media_id')
        midia_type = request.POST.get('midia_type')
        action = request.POST.get('action')
        
        if action == 'add':
            await add_to_list(request, media_id, midia_type)
            return JsonResponse({'status': 'added'})
        elif action == 'remove':
            await remove_from_list(request, media_id, midia_type)
            return JsonResponse({'status': 'removed'})
        
        # Muito importante: colocar return aqui também
        return JsonResponse({'status': 'error'})

    filme = await asyncio.to_thread(info_movie, movie_id)
    trailer = await asyncio.to_thread(get_trailer,'movie', movie_id)
    
    # Verifica se o usuário está autenticado antes de chamar a função
    is_authenticated = await sync_to_async(lambda u: u.is_authenticated)(request.user)
    if is_authenticated:
        esta_na_lista = await asyncio.to_thread(verificar_midia_na_lista, request.user, movie_id, 'movie')
    else:
        esta_na_lista = False  # Se o usuário não estiver autenticado, defina como False
        
    context = {
        'filme': filme,
        'trailer': trailer,
        'esta_na_lista': esta_na_lista,  # Adiciona a variável ao contexto
    }
    return render(request, 'html/infomovie.html', context)

#------------------------------------------------- DETALHES DA SÉRIE ---------------------------------------------------
async def detail_serie(request, series_id):
    if request.method == "POST":
        media_id = request.POST.get('media_id')
        midia_type = request.POST.get('midia_type')
        action = request.POST.get('action')
        
        if action == 'add':
            await add_to_list(request, media_id, midia_type)
            return JsonResponse({'status': 'added'})
        elif action == 'remove':
            await remove_from_list(request, media_id, midia_type)
            return JsonResponse({'status': 'removed'})
        
        # Muito importante: colocar return aqui também
        return JsonResponse({'status': 'error'})
    
    # 
    serie = await asyncio.to_thread(info_serie, series_id)
    trailer = await asyncio.to_thread(get_trailer,'tv', series_id)
    
    
    is_authenticated = await sync_to_async(lambda u: u.is_authenticated)(request.user)
    if is_authenticated:
        esta_na_lista = await asyncio.to_thread(verificar_midia_na_lista, request.user, series_id,'tv')
    else:
        esta_na_lista = False
    
    context = {
        'serie': serie,
        'trailer': trailer,
        'esta_na_lista': esta_na_lista,  # Adiciona a variável ao contexto
    }
    return render(request, 'html/infoserie.html', context)

#----------------------- Lista de filmes/series do usuario -----------------------
@login_required(login_url='/login/')
def lista(request):
    # 1. Consulta todos os objetos da lista do usuário normalmente (ORM síncrono)
    object_list = list(Lista.objects.filter(user_id=request.user))

    # 2. Função assíncrona para buscar detalhes de cada mídia em paralelo usando asyncio.to_thread
    async def get_midia(obj):
        if obj.midia_type == 'movie':
            # info_movie é uma função bloqueante, então executamos em thread separada
            return await asyncio.to_thread(info_movie, obj.media_id)
        elif obj.midia_type == 'tv':
            return await asyncio.to_thread(info_serie, obj.media_id)
        return None

    # 3. Função para criar e executar todas as tarefas de busca em paralelo
    async def gather_midias():
        tasks = [get_midia(obj) for obj in object_list]
        return await asyncio.gather(*tasks)

    # 4. Executa as buscas em paralelo usando um novo event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    detalhes_midias = loop.run_until_complete(gather_midias())
    loop.close()

    # 5. Remove possíveis None (caso algum objeto não seja movie ou tv)
    midias = [m for m in detalhes_midias if m]

    # 6. Passa os detalhes para o template
    context = {
        'midias': midias,
    }
    return render(request, "html/lista.html", context)

#----------------------- Funções de paginação para filmes -----------------------
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

#----------------------- Funções de paginação para séries -----------------------
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
    
#----------------------- Tela de login -----------------------
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/home/')
        else:
            messages.add_message(request, messages.ERROR, 'Usuário ou senha incorretos', extra_tags="login")
            return render(request, 'html/login.html')
    return render(request, 'html/login.html')

#----------------------- Tela de logout -----------------------
def logout_view(request):
    logout(request)
    return redirect('/home')

#----------------------- Tela de cadastro -----------------------
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

        # Se tudo estiver correto, cria o usuário
        user = User.objects.create_user(username=username, email=email1, password=password1)
        # Salva o usuário no banco de dados
        user.save()
        messages.success(request, 'Cadastro realizado com sucesso!', extra_tags='sucesso')
        return redirect('/login/')
    return render(request, 'html/cad.html')
#----------------------- Tela de redefinição de senha -----------------------
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm