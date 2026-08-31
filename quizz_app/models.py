"""Models for the quizz application."""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json
import uuid


class UserProfile(models.Model):
    """Extended user profile with role."""
    ROLE_CHOICES = [
        ('profesor', 'Profesor'),
        ('estudiante', 'Estudiante'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='estudiante')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


class Category(models.Model):
    """Quiz category managed by its teacher."""
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_categories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['teacher', 'name'], name='unique_category_per_teacher')
        ]

    def __str__(self):
        return self.name


class Quiz(models.Model):
    """Model to store quiz data."""
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes_created', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, default='General')
    difficulty = models.CharField(
        max_length=20,
        choices=[('fácil', 'Fácil'), ('medio', 'Medio'), ('difícil', 'Difícil')],
        default='medio'
    )
    questions_data = models.JSONField(default=list)
    time_limit = models.IntegerField(default=0, help_text="Tiempo límite en segundos (0 = sin límite)")
    access_code = models.CharField(max_length=10, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Generate access_code if not set."""
        if not self.access_code:
            self.access_code = str(uuid.uuid4())[:10].upper()
        super().save(*args, **kwargs)

    def get_questions(self):
        """Return the questions as a list of dictionaries."""
        if isinstance(self.questions_data, str):
            return json.loads(self.questions_data)
        return self.questions_data


class QuizEnrollment(models.Model):
    """Model to track students enrolled in quizzes."""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_enrollments')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'quiz')
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title}"


class QuizResult(models.Model):
    """Model to store quiz results with persistence."""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    quiz_name = models.CharField(max_length=200, default='')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_results', null=True, blank=True)
    player_name = models.CharField(max_length=100)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    percentage = models.FloatField()
    answers = models.JSONField(default=dict)
    question_times = models.JSONField(default=dict, help_text="Tiempo por pregunta en segundos")
    time_taken = models.IntegerField(default=0, help_text="Tiempo empleado en segundos")
    average_time_per_question = models.FloatField(default=0, help_text="Tiempo promedio por pregunta en segundos")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['student', '-created_at']),
            models.Index(fields=['quiz', '-created_at']),
        ]

    def __str__(self):
        return f"{self.player_name} - {self.quiz.title} ({self.percentage}%)"

    def get_time_display(self):
        """Return formatted time."""
        minutes = self.time_taken // 60
        seconds = self.time_taken % 60
        return f"{minutes}m {seconds}s"


class LiveSession(models.Model):
    """Model to manage live quiz sessions for teachers."""
    STATUS_CHOICES = [
        ('waiting', 'Esperando'),
        ('active', 'Activo'),
        ('paused', 'Pausado'),
        ('finished', 'Finalizado'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='live_sessions')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='live_sessions_created')
    session_code = models.CharField(max_length=10, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    current_question = models.IntegerField(default=0)
    allow_join = models.BooleanField(default=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Sesión {self.session_code} - {self.quiz.title}"
    
    def save(self, *args, **kwargs):
        """Generate session_code if not set."""
        if not self.session_code:
            self.session_code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)
    
    def get_students_count(self):
        """Return count of joined students."""
        return self.live_participants.count()
    
    def get_completed_count(self):
        """Return count of completed students."""
        return self.live_participants.filter(completed=True).count()


class LiveParticipant(models.Model):
    """Model to track students in a live session."""
    session = models.ForeignKey(LiveSession, on_delete=models.CASCADE, related_name='live_participants')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='live_participations', null=True, blank=True)
    student_name = models.CharField(max_length=100)
    answers = models.JSONField(default=dict)
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-joined_at']
        unique_together = ('session', 'student_name')
    
    def __str__(self):
        return f"{self.student_name} - {self.session.session_code}"
