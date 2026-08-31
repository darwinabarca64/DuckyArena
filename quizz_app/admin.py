"""Admin configuration for quizz_app."""
from django.contrib import admin
from .models import Category, UserProfile, Quiz, QuizEnrollment, QuizResult


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username']

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher', 'created_at']
    search_fields = ['name', 'teacher__username']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'creator', 'access_code', 'is_active', 'created_at']
    list_filter = ['category', 'difficulty', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['access_code']


@admin.register(QuizEnrollment)
class QuizEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz', 'completed', 'enrolled_at']
    list_filter = ['quiz', 'completed', 'enrolled_at']
    search_fields = ['student__username', 'quiz__title']


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['player_name', 'quiz', 'student', 'score', 'percentage', 'time_taken', 'created_at']
    list_filter = ['quiz', 'created_at']
    search_fields = ['player_name', 'student__username']
    readonly_fields = ['created_at', 'updated_at']
