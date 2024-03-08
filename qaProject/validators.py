from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('Password must contain at least 1 digit.'))
        if not any(char.isupper() for char in password):
            raise ValidationError(_('Password must contain at least 1 uppercase letter.'))

    def get_help_text(self):
        return _('Your password must contain at least 1 digit and 1 uppercase letter.')