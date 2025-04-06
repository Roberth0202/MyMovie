from .models import Lista
from django.core.exceptions import ValidationError

def adicionar_midia(usuario, media_id, midia_type):
    """
    Adiciona uma mídia à lista de um usuário.
    Args:
        usuario (int): O ID do usuário.
        media_id (int): O ID da mídia a ser adicionada.
        midia_type (str): O tipo da mídia (por exemplo, 'filme', 'série').
    Raises:
        ValidationError: Se a mídia já estiver na lista do usuário.
    """
    if Lista.objects.filter(user_id=usuario, media_id=media_id, midia_type=midia_type).exists():
        raise ValidationError('Mídia já está na sua lista.')
    
    nova_entrada = Lista(user_id=usuario, media_id=media_id, midia_type=midia_type)
    nova_entrada.save()


def remover_midia(usuario, media_id, midia_type):
    """
    Remove uma mídia da lista de um usuário.

    Args:
        usuario (int): O ID do usuário.
        media_id (int): O ID da mídia.
        midia_type (str): O tipo da mídia (por exemplo, 'filme', 'série').

    Returns:
        bool: Retorna True se a mídia foi removida com sucesso, False se a mídia não foi encontrada.
    """
    try:
        entrada = Lista.objects.get(user_id=usuario, media_id=media_id, midia_type=midia_type)
        entrada.delete()
    except Lista.DoesNotExist:
        return False
    return True
