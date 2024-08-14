from .models import Lista
from django.core.exceptions import ValidationError

def adicionar_filme(usuario, filme_id):
    if Lista.objects.filter(user_id=usuario, movie_id=filme_id).exists():
        raise ValidationError('Filme já está na sua lista.')
    nova_entrada = Lista(user_id=usuario, movie_id=filme_id)
    nova_entrada.save()

def remover_filme(usuario, filme_id):
    try:
        entrada = Lista.objects.get(user_id=usuario, movie_id=filme_id)
        entrada.delete()
    except Lista.DoesNotExist:
        return False
    return True