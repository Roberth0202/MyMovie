from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class UppercaseValidator:
    """Valida se a senha contém pelo menos uma letra maiúscula"""
    
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _('A senha deve conter pelo menos uma letra maiúscula.'),
                code='password_no_upper',
            )
            
    def get_help_text(self):
        return _('Sua senha deve conter pelo menos uma letra maiúscula.')

class SymbolValidator:
    """Valida se a senha contém pelo menos um símbolo"""
    
    def validate(self, password, user=None):
        symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=']
        if not any(char in symbols for char in password):
            raise ValidationError(
                _('A senha deve conter pelo menos um símbolo (!, @, #, etc).'),
                code='password_no_symbol',
            )
            
    def get_help_text(self):
        return _('Sua senha deve conter pelo menos um símbolo (!, @, #, etc).')