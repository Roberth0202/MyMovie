import json
from decouple import config
import requests

api_key = config("api_key")
#url do geral
base_url = 'https://api.themoviedb.org/3'
# Tamanhos disponíveis: "w92", "w154", "w185", "w342", "w500", "w780", "original"
poster_url = 'https://image.tmdb.org/t/p/'

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {config('api_key')}"
}

#Filmes populares da semana
def filme_populares():
    url = f"{base_url}/trending/movie/week?language=pt-BR"
    parametros = {
        'api_key': api_key,
        'language': 'pt-BR'
    }
    
    resposta = requests.get(url, headers=headers, params=parametros)
    
    max_results = 20
    count = 0
    filmes = [] 
    if resposta.status_code == 200:
        dados = resposta.json()

        if 'results' in dados:
            for movie in dados['results']:
                name = movie['title']
                poster = movie['poster_path']
                id = movie['id']
                
                if count < max_results:
                    filmes.append({
                        'name': name,
                        'poster': poster_url + 'w342' + poster,
                        'id': id,
                    })
                    count += 1
        return filmes

#Series populares na semana
def serie_populares():
    url = f"{base_url}/trending/tv/week?language=pt-BR"
    parametros = {
        'api_key': api_key,
        'language': 'pt-BR'
    }
    
    resposta = requests.get(url, headers=headers, params=parametros)
    
    max_results = 20
    count = 0
    series = [] 
    if resposta.status_code == 200:
        dados = resposta.json()

        if 'results' in dados:
            for serie in dados['results']:
                name = serie['name']
                poster = serie['poster_path']
                id = serie['id']

                if count < max_results:
                    series.append({
                        'name': name,
                        'poster': poster_url + 'w342' + poster,
                        'id': id,
                    })
                    count += 1
        return series
    
#Devolve o filme e suas informções por meio o id 
def info_movie(movie_id):
    url = f"{base_url}/movie/{movie_id}?language=pt-BR"
    parametros = {
        'api_key': api_key,
        'language': 'pt-BR'
    }
    
    resposta = requests.get(url, headers=headers, params=parametros)
    
    if resposta.status_code == 200:
        dados = resposta.json()
        #pega os generos do filme
        generos = [genero['name'] for genero in dados['genres']]
        
        if dados.get('poster_path'):
            poster_url_completo = poster_url + 'w500' + dados['poster_path']
        else:
            poster_url_completo = None
        
        movie_details={
            'name': dados['title'],
            'poster': poster_url_completo,
            'year': dados['release_date'],
            'id': dados['id'],
            'genre': generos,
            'description' : dados['overview'],
            'type' : 'movie',
        }
        return movie_details
    
#Devolve o serie e suas informções por meio o id 
def info_serie(series_id):
    url = f"{base_url}/tv/{series_id}?language=pt-BR"
    parametros = {
        'api_key': api_key,
        'language': 'pt-BR'
    }
    
    resposta = requests.get(url, headers=headers, params=parametros)

    if resposta.status_code == 200:
        dados = resposta.json()
        
        generos = [genero['name'] for genero in dados['genres']]
        
        serie_detail = {
            'name' : dados['name'],
            'poster' : poster_url + 'w500' + dados['poster_path'],
            'year' : dados['first_air_date'],
            'id': dados['id'],
            'genre' : generos,
            'description' : dados['overview'],
            'type' : 'tv',
        }
        return serie_detail
        
#função pega a pesquisa e entrega os filmes e series
def search_movies(query):
    url = f'{base_url}/search/multi'
    parametros = {
        'api_key': api_key,
        'query': query,
        'include_adult': 'false',
        'language': 'pt-BR',
        'page': 1
    }
    
    resposta = requests.get(url, headers=headers, params=parametros)
    
    resultados = []
    ids_unicos = set()
    
    if resposta.status_code == 200:
        dados = resposta.json()
        
        for resultado in dados['results']:
            media_type = resultado.get('media_type')
            if media_type in ['movie', 'tv']:  
                poster_path = resultado.get('poster_path')
                
                # Se o poster_path for None, pula para o próximo item
                if not poster_path:
                    continue             

                name = resultado.get('title') or resultado.get('name')
                poster = poster_url + 'w342' + poster_path if poster_path else None
                id = resultado['id']
                resultados.append({
                    'name': name,
                    'poster': poster,
                    'id': id,
                    'media_type': media_type
                })
        
        return resultados

#mostra uma lista de filme
def Filmes(page):
    url = f'{base_url}/discover/movie'
    
    max_pages = 500  # Limite manual de páginas
    page = min(page, max_pages)  # Garante que a página não ultrapasse o limite
    
    parametros = {
        'api_key': api_key,
        'language': 'pt-BR',
        'page': page,
    }
    
    resposta = requests.get(url, headers=headers, params=parametros)
        
    if resposta.status_code != 200:
        # Handle error (e.g., log error, return empty list)
        return {'results': [], 'page': 1, 'total_pages': 1}

    dados = resposta.json()
    
    total_pages = min(dados['total_pages'], max_pages)  # Limita o total de páginas
    
    lista_filmes = []
    for movie in dados['results']:
        id = movie['id']    
        name = movie['title']
        poster = movie['poster_path']
        
        
        lista_filmes.append({
            'id' : id,
            'name' : name,
            'poster' : poster_url + 'w342' + poster,
        })

    return {
        'results': lista_filmes,
        'page': dados['page'],  # Página atual
        'total_pages': total_pages  # Total de páginas, limitado a 500
    }
    
def Series(page):
    url = f'{base_url}/discover/tv'
    
    max_pages = 500  # Limite manual de páginas
    page = min(page, max_pages)  # Garante que a página não ultrapasse o limite
    
    parametros = {
        'api_key': api_key,
        'language': 'pt-BR',
        'page': page,
    }
    
    resposta = requests.get(url, headers=headers, params=parametros)
    
    if resposta.status_code != 200:
        # Handle error (e.g., log error, return empty list)
        return {'results': [], 'page': 1, 'total_pages': 1}
    
    dados = resposta.json()
    
    total_pages = min(dados['total_pages'], max_pages)  # Limita o total de páginas
    
    lista_series = []
     
    for serie in dados['results']:

        if serie['poster_path'] == None:
            continue # Pula essa série se não houver poster
        
        poster = serie['poster_path']
        id = serie['id']
        name = serie['name']
        
        lista_series.append({
            'id' : id,
            'name' : name,
            'poster' : poster_url + 'w342' + poster,
        })
    
    return {
        'results' : lista_series,
        'page' : dados['page'],
        'total_pages' : total_pages,
    }
    