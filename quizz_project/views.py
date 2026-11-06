from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View

from quizz_project.forms import PasswordlessLoginForm


class PasswordlessLoginView(View):
    """
    Vista de autenticación frictionless para jugadores y estudiantes.
    Permite iniciar sesión usando únicamente su nombre de usuario/nickname,
    preservando el flujo de redirecciones con 'next' y restringiendo el acceso
    sin contraseña a usuarios staff o superusuarios.
    """
    template_name = 'registration/login.html'
    form_class = PasswordlessLoginForm

    def get_redirect_url(self):
        redirect_to = self.request.POST.get(
            'next',
            self.request.GET.get('next', '')
        )
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        )
        if url_is_safe and redirect_to:
            return redirect_to
        return getattr(settings, 'LOGIN_REDIRECT_URL', '/quizzes/')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_redirect_url())

        form = self.form_class()
        next_url = request.GET.get('next', '')
        return render(request, self.template_name, {
            'form': form,
            'next': next_url,
        })

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_redirect_url())

        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(self.get_redirect_url())

        next_url = request.POST.get('next', request.GET.get('next', ''))
        return render(request, self.template_name, {
            'form': form,
            'next': next_url,
        })
