from django.db import models
from django.contrib.auth.models import User

class Lista(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lista_de_midias')  # id do usuário
    media_id = models.IntegerField()  # id do filme ou série
    midia_type = models.CharField(default=None, max_length=10)  # Tipo de mídia ('movie' ou 'tv')

    class Meta:
        unique_together = ('user_id', 'media_id', 'midia_type')

    def __str__(self):
        return f"{self.media_id} ({self.midia_type})"
