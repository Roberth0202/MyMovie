from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
    path('filme/<movie_id>', views.detail_movie, name="filme"),
    path('serie/<series_id>', views.detail_serie, name="serie"),
    path('pesquisa/', views.pesquisa, name="pesquisa"),
    path('lista/', views.lista, name="lista"),
    path('filmes/', views.filmes, name="filmes"),
    path('series/', views.series, name="series"),
    # Página para o usuário informar o e-mail
    path('password-reset/', PasswordResetView.as_view(template_name='html/password_reset_form.html'), name='password_reset'),

    # Página que avisa que o e-mail foi enviado
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='html/password_reset_done.html'), name='password_reset_done'),

    # Link enviado por e-mail com token
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(template_name='html/password_reset_confirm.html'), name='password_reset_confirm'),
    
    # Página de confirmação final
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='html/password_reset_complete.html'), name='password_reset_complete'),
    ]
