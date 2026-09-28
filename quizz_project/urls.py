"""URL configuration for quizz_project project."""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('quizzes:quiz_list'), name='root_redirect'),
    path('admin/', admin.site.urls),
    path('quizzes/', include('quizzes.urls')),
]
