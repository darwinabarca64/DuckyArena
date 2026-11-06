"""URL configuration for quizz_project project."""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.shortcuts import redirect

from quizz_project.views import PasswordlessLoginView

urlpatterns = [
    path('', lambda request: redirect('quizzes:quiz_list'), name='root_redirect'),
    path('admin/', admin.site.urls),
    path('accounts/login/', PasswordlessLoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/quizzes/'), name='logout'),
    path('quizzes/', include('quizzes.urls')),
    path('games/', include('quiz_games.urls')),
]
