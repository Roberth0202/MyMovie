from django.db import models
from django.contrib.auth.models import User

class Lista(models.Model):
    """
    Modelo que representa uma lista de mídias associadas a um usuário.
    Atributos:
        user_id (ForeignKey): Chave estrangeira para o modelo User, representando o id do usuário.
        media_id (IntegerField): Campo inteiro representando o id do filme ou série.
        midia_type (CharField): Campo de texto com no máximo 10 caracteres, representando o tipo de mídia ('movie' ou 'tv').
    Meta:
        unique_together: Garante que a combinação de user_id, media_id e midia_type seja única.
    Métodos:
        __str__: Retorna uma string representando a mídia no formato "media_id (midia_type)".
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lista_de_midias')  # id do usuário
    media_id = models.IntegerField()  # id do filme ou série
    midia_type = models.CharField(default=None, max_length=10)  # Tipo de mídia ('movie' ou 'tv')

    class Meta:
        unique_together = ('user_id', 'media_id', 'midia_type')

    def __str__(self):
        return f"{self.media_id} ({self.midia_type})"
