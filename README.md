# Projeto MyMovie

Este projeto é um sistema web para gerenciamento de listas de filmes e séries, inspirado no MyMovie, desenvolvido com Django.

## Funcionalidades
- Cadastro e autenticação de usuários
- Adição de filmes e séries à lista pessoal
- Visualização de detalhes de filmes e séries
- Busca por títulos
- Interface moderna e responsiva

## Estrutura do Projeto
- `mymovie/`: App principal com modelos, views, urls e templates
- `mysite/`: Configurações do projeto Django
- `templates/`: Templates HTML para as páginas
- `static/`: Arquivos estáticos (CSS, JS, imagens)
- `requirements.txt` e `uv.lock`: Dependências do projeto

## Instalação
1. Clone o repositório:
   ```sh
   git clone <url-do-repositorio>
   cd filmes
   ```
2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```sh
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
   ou use
   ```sh
   uv pip sync
   ```
4. Realize as migrações do banco de dados:
   ```sh
   python manage.py migrate
   ```
5. Inicie o servidor de desenvolvimento:
   ```sh
   python manage.py runserver
   ```
6. Acesse em [http://localhost:8000](http://localhost:8000)

## Licença
Este projeto está sob a licença MIT.
