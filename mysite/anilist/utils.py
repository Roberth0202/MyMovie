from .models import Lista
from django.core.exceptions import ValidationError

def adicionar_midia(usuario, media_id, midia_type):
    if Lista.objects.filter(user_id=usuario, media_id=media_id, midia_type=midia_type).exists():
        raise ValidationError('Mídia já está na sua lista.')
    
    nova_entrada = Lista(user_id=usuario, media_id=media_id, midia_type=midia_type)
    nova_entrada.save()

def remover_midia(usuario, media_id, midia_type):
    try:
        entrada = Lista.objects.get(user_id=usuario, media_id=media_id, midia_type=midia_type)
        entrada.delete()
    except Lista.DoesNotExist:
        return False
    return True
