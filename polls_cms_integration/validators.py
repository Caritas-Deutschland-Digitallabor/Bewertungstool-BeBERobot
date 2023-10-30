import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class NumberValidator(object):
    def __init__(self, min_digits=0):
        self.min_digits = min_digits

    def validate(self, password, user=None):
        if not len(re.findall('\d', password)) >= self.min_digits:
            raise ValidationError(
                _("Das Passwort muss mindestens %(min_digits)d Ziffer(n) enthalten, 0-9."),
                code='password_no_number',
                params={'min_digits': self.min_digits},
            )

    def get_help_text(self):
        return _(
            "Das Passwort muss mindestens %(min_digits)d Ziffer(n) enthalten, 0-9." % {'min_digits': self.min_digits}
        )

class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("Das Passwort muss mindestens einen Großbuchstaben enthalten, A-Z."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Das Passwort muss mindestens einen Großbuchstaben enthalten, A-Z."
        )


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _("Das Passwort muss mindestens einen Kleinbuchstaben enthalten, a-z."),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _(
            "Das Passwort muss mindestens einen Kleinbuchstaben enthalten, a-z."
        )


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                _("Das Passwort muss mindestens 1 Symbol enthalten: " +
                  "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "Das Passwort muss mindestens 1 Symbol enthalten: " +
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )