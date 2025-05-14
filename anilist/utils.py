from .models import Lista
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.password_validation import validate_password

class CustomSetPasswordForm(SetPasswordForm):
    """
    Formulário personalizado para redefinir a senha do usuário.
    Adiciona validação de senha personalizada.
    """
    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        try:
            validate_password(password, self.user)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        return password

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
