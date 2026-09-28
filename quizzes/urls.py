from django.urls import path
from .views import (
    QuizListView,
    QuizDetailView,
    QuizCreateView,
    QuizUpdateView,
    QuizDeleteView,
    QuizTogglePublishView,
)

app_name = 'quizzes'

urlpatterns = [
    path('', QuizListView.as_view(), name='quiz_list'),
    path('<int:pk>/', QuizDetailView.as_view(), name='quiz_detail'),
    path('create/', QuizCreateView.as_view(), name='quiz_create'),
    path('<int:pk>/edit/', QuizUpdateView.as_view(), name='quiz_edit'),
    path('<int:pk>/delete/', QuizDeleteView.as_view(), name='quiz_delete'),
    path('<int:pk>/toggle-publish/', QuizTogglePublishView.as_view(), name='quiz_toggle_publish'),
]
