import unittest
from django.core.exceptions import ValidationError
from .validators import UppercaseValidator, SymbolValidator

# FILE: mysite/mysite/test_validators.py


class TestUppercaseValidator(unittest.TestCase):
    
    def setUp(self):
        self.validator = UppercaseValidator()
    
    def test_password_no_uppercase(self):
        with self.assertRaises(ValidationError) as context:
            self.validator.validate('password')
        self.assertEqual(context.exception.code, 'password_no_upper')
        self.assertEqual(str(context.exception), 'A senha deve conter pelo menos uma letra maiúscula.')

    def test_password_with_uppercase(self):
        try:
            self.validator.validate('Password')
        except ValidationError:
            self.fail("validate() raised ValidationError unexpectedly!")

class TestSymbolValidator(unittest.TestCase):
    
    def setUp(self):
        self.validator = SymbolValidator()
    
    def test_password_no_symbol(self):
        with self.assertRaises(ValidationError) as context:
            self.validator.validate('Password')
        self.assertEqual(context.exception.code, 'password_no_symbol')
        self.assertEqual(str(context.exception), 'A senha deve conter pelo menos um símbolo (!, @, #, etc).')

    def test_password_with_symbol(self):
        try:
            self.validator.validate('Password!')
        except ValidationError:
            self.fail("validate() raised ValidationError unexpectedly!")

if __name__ == '__main__':
    unittest.main()