"""URL configuration for quizz_app."""
from django.urls import path
from . import views

app_name = 'quizz_app'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.index, name='index'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('results/<int:result_id>/', views.results, name='results'),
    path('mis-puntuaciones/', views.my_scores, name='my_scores'),
    path('quiz/<int:quiz_id>/leaderboard/', views.leaderboard, name='leaderboard'),
    path('quiz/<int:quiz_id>/qr/', views.generate_qr_code, name='generate_qr'),
    path('quiz/enroll/<str:access_code>/', views.enroll_quiz, name='enroll_quiz'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/statistics/', views.teacher_statistics, name='teacher_statistics'),
    path('teacher/categories/', views.manage_categories, name='manage_categories'),
    path('teacher/create-quiz/', views.create_quiz, name='create_quiz'),
    path('teacher/edit-quiz/<int:quiz_id>/', views.edit_quiz, name='edit_quiz'),
    path('teacher/delete-quiz/<int:quiz_id>/', views.delete_quiz, name='delete_quiz'),
    path('teacher/quiz-students/<int:quiz_id>/', views.quiz_students, name='quiz_students'),
    
    # Live session routes
    path('teacher/start-live/<int:quiz_id>/', views.start_live_session, name='start_live_session'),
    path('teacher/manage-live/<int:session_id>/', views.manage_live_session, name='manage_live_session'),
    path('live/join/', views.join_live_session, name='join_live_session'),
    path('live/<int:session_id>/quiz/<int:participant_id>/', views.live_quiz, name='live_quiz'),
    path('live/<int:session_id>/results/<int:participant_id>/', views.live_results, name='live_results'),
    path('api/session/<int:session_id>/status/', views.api_session_status, name='api_session_status'),
]
