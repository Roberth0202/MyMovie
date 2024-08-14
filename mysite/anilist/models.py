from django.db import models, transaction
from django.contrib.auth.models import User

# Create your models here.
class Lista(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lista_de_filmes')  # id do usuário
    movie_id = models.IntegerField()  # id do filme ou série

    class Meta:
        unique_together = ('user_id', 'movie_id')

    def __str__(self):
        return str(self.movie_id)