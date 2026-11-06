from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import transaction

User = get_user_model()


class PasswordlessLoginForm(forms.Form):
    """
    Formulario de autenticación sin contraseña para estudiantes y jugadores.
    Permite el acceso inmediato mediante Nickname o Usuario, creando la cuenta
    automáticamente si no existe y protegiendo el acceso de cuentas docentes/admin.
    """
    username = forms.CharField(
        label="Usuario / Nickname",
        max_length=150,
        strip=True,
        error_messages={
            'required': 'Por favor, introduce un nombre de usuario o nickname.',
        },
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'id': 'id_username',
            'placeholder': 'Ej: PatoMaster, Jugador1...',
            'autofocus': True,
            'autocomplete': 'username',
            'required': True,
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_cache = None

    def clean_username(self):
        raw_username = self.cleaned_data.get('username', '')
        username = raw_username.strip() if isinstance(raw_username, str) else ''
        if not username:
            raise ValidationError("Por favor, introduce un nombre de usuario o nickname.")

        validator = UnicodeUsernameValidator()
        validator(username)
        return username

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        if not username:
            return cleaned_data

        with transaction.atomic():
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_unusable_password()
                user.save()

                if hasattr(user, 'profile'):
                    profile = user.profile
                    if hasattr(profile, 'role') and not profile.role:
                        profile.role = 'STUDENT'
                    if hasattr(profile, 'ducky_coins') and profile.ducky_coins is None:
                        profile.ducky_coins = 0
                    if callable(getattr(profile, 'save', None)):
                        try:
                            profile.save()
                        except Exception:
                            pass
            else:
                if user.is_staff or user.is_superuser:
                    raise ValidationError(
                        "Las cuentas de docentes y administradores no pueden acceder sin contraseña. "
                        "Por favor, inicia sesión a través del Panel Django (/admin/) con tu contraseña."
                    )

            self.user_cache = user

        return cleaned_data

    def get_user(self):
        return getattr(self, 'user_cache', None)
