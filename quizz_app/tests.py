"""Tests for quizz_app."""
import json

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Quiz, QuizResult, UserProfile


class QuizModelTest(TestCase):
    """Tests for Quiz model."""

    def setUp(self):
        """Create test data."""
        self.quiz = Quiz.objects.create(
            title='Test Quiz',
            description='Test description',
            category='Test',
            difficulty='medio',
            questions_data=[
                {
                    'question': 'Test question?',
                    'options': ['A', 'B', 'C', 'D'],
                    'correct_answer': '0'
                }
            ]
        )

    def test_quiz_creation(self):
        """Test quiz creation."""
        self.assertEqual(self.quiz.title, 'Test Quiz')
        self.assertEqual(len(self.quiz.get_questions()), 1)

    def test_quiz_string_representation(self):
        """Test quiz string representation."""
        self.assertEqual(str(self.quiz), 'Test Quiz')


class QuizResultModelTest(TestCase):
    """Tests for QuizResult model."""

    def setUp(self):
        """Create test data."""
        self.quiz = Quiz.objects.create(
            title='Test Quiz',
            description='Test description',
            category='Test',
            difficulty='medio',
            questions_data=[]
        )
        self.result = QuizResult.objects.create(
            quiz=self.quiz,
            quiz_name=self.quiz.title,
            player_name='Test Player',
            score=8,
            total_questions=10,
            percentage=80.0,
            answers={'0': '0', '1': '1'},
            question_times={'0': 12, '1': 18},
            average_time_per_question=15.0,
        )

    def test_result_creation(self):
        """Test result creation."""
        self.assertEqual(self.result.player_name, 'Test Player')
        self.assertEqual(self.result.percentage, 80.0)
        self.assertEqual(self.result.quiz_name, 'Test Quiz')
        self.assertEqual(self.result.question_times, {'0': 12, '1': 18})
        self.assertEqual(self.result.average_time_per_question, 15.0)

    def test_result_string_representation(self):
        """Test result string representation."""
        self.assertIn('Test Player', str(self.result))
        self.assertIn('80.0%', str(self.result))


class QuizAuthenticationTest(TestCase):
    """Tests access control for standard quizzes."""

    def setUp(self):
        """Create a quiz that an anonymous visitor may try to access."""
        self.quiz = Quiz.objects.create(
            title='Protected Quiz',
            description='Only for logged-in users',
            category='Test',
            difficulty='medio',
            questions_data=[]
        )

    def test_anonymous_user_cannot_start_or_submit_quiz(self):
        """Anonymous users are redirected to login without recording a result."""
        detail_url = reverse('quizz_app:quiz_detail', args=[self.quiz.id])
        submit_url = reverse('quizz_app:submit_quiz', args=[self.quiz.id])

        detail_response = self.client.get(detail_url)
        submit_response = self.client.post(
            submit_url,
            data=json.dumps({'answers': {}}),
            content_type='application/json'
        )

        self.assertRedirects(detail_response, f'/login/?next={detail_url}')
        self.assertRedirects(submit_response, f'/login/?next={submit_url}')
        self.assertEqual(QuizResult.objects.filter(quiz=self.quiz).count(), 0)

    def test_quiz_result_uses_authenticated_username(self):
        """The submitted result cannot override the authenticated user's name."""
        user = User.objects.create_user(username='alumno', password='clave-segura-123')
        self.client.force_login(user)

        response = self.client.post(
            reverse('quizz_app:submit_quiz', args=[self.quiz.id]),
            data=json.dumps({'player_name': 'Nombre falso', 'answers': {}}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(QuizResult.objects.get(quiz=self.quiz).player_name, user.username)

    def test_quiz_result_persists_timing_metrics(self):
        """Question timings, total, and average are saved with the quiz result."""
        user = User.objects.create_user(username='alumno_tiempos', password='clave-segura-123')
        quiz = Quiz.objects.create(
            title='Quiz cronometrado',
            description='Prueba de tiempos',
            category='Test',
            difficulty='medio',
            questions_data=[
                {'question': 'Uno', 'options': ['A', 'B'], 'correct_answer': 0},
                {'question': 'Dos', 'options': ['A', 'B'], 'correct_answer': 1},
            ]
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse('quizz_app:submit_quiz', args=[quiz.id]),
            data=json.dumps({
                'answers': {'0': 0, '1': 1},
                'question_times': {'0': 12, '1': 18},
            }),
            content_type='application/json'
        )

        result = QuizResult.objects.get(quiz=quiz)
        self.assertEqual(response.json()['time_taken'], 30)
        self.assertEqual(result.quiz_name, quiz.title)
        self.assertEqual(result.question_times, {'0': 12, '1': 18})
        self.assertEqual(result.time_taken, 30)
        self.assertEqual(result.average_time_per_question, 15)

    def test_my_scores_only_shows_current_users_results(self):
        """The score history is private to the authenticated user."""
        current_user = User.objects.create_user(username='alumno_historial', password='clave-segura-123')
        other_user = User.objects.create_user(username='otro_alumno', password='clave-segura-123')
        own_result = QuizResult.objects.create(
            quiz=self.quiz, quiz_name='Mi quiz', student=current_user,
            player_name=current_user.username, score=3, total_questions=4,
            percentage=75, answers={}
        )
        QuizResult.objects.create(
            quiz=self.quiz, quiz_name='Quiz ajeno', student=other_user,
            player_name=other_user.username, score=4, total_questions=4,
            percentage=100, answers={}
        )
        self.client.force_login(current_user)

        response = self.client.get(reverse('quizz_app:my_scores'))

        self.assertContains(response, 'Mi quiz')
        self.assertNotContains(response, 'Quiz ajeno')
        self.assertContains(response, reverse('quizz_app:results', args=[own_result.id]))

    def test_teacher_can_view_aggregate_statistics(self):
        """Statistics aggregate only quizzes created by the logged-in teacher."""
        teacher = User.objects.create_user(username='profesor_estadisticas', password='clave-segura-123')
        UserProfile.objects.create(user=teacher, role='profesor')
        student = User.objects.create_user(username='alumno_estadisticas', password='clave-segura-123')
        quiz = Quiz.objects.create(
            creator=teacher, title='Historia', category='Historia', difficulty='medio', questions_data=[]
        )
        QuizResult.objects.create(
            quiz=quiz, quiz_name=quiz.title, student=student, player_name=student.username,
            score=4, total_questions=5, percentage=80, answers={}, time_taken=50
        )
        self.client.force_login(teacher)

        response = self.client.get(reverse('quizz_app:teacher_statistics'))

        self.assertContains(response, 'Historia')
        self.assertContains(response, '50 s')
        self.assertEqual(response.context['average_score'], 80)

    def test_quiz_displays_step_navigation_controls(self):
        """The quiz page includes controls for step-by-step navigation and exit."""
        user = User.objects.create_user(username='alumno_navegacion', password='clave-segura-123')
        self.client.force_login(user)

        response = self.client.get(reverse('quizz_app:quiz_detail', args=[self.quiz.id]))

        self.assertContains(response, 'id="previousQuestion"')
        self.assertContains(response, 'id="nextQuestion"')
        self.assertContains(response, 'id="questionIndicator"')
        self.assertContains(response, 'aria-label="Salir del quiz"')
        self.assertContains(response, 'id="notificationContainer"')
        self.assertContains(response, 'id="questionNavigator"')

    def test_options_for_a_question_share_one_radio_group(self):
        """Selecting an option leaves only one answer selected per question."""
        user = User.objects.create_user(username='alumno_opciones', password='clave-segura-123')
        quiz = Quiz.objects.create(
            title='Quiz con opciones',
            description='Prueba de radios',
            category='Test',
            difficulty='medio',
            questions_data=[{
                'question': 'Elige una opción',
                'options': ['A', 'B', 'C', 'D'],
                'correct_answer': 0,
            }]
        )
        self.client.force_login(user)

        response = self.client.get(reverse('quizz_app:quiz_detail', args=[quiz.id]))

        self.assertContains(response, 'name="question_0"', count=4)
        self.assertContains(response, 'data-question-index="0"', count=2)
        self.assertNotContains(response, '>1</button>')


class AuthenticationFlowTest(TestCase):
    """Tests user registration and login role handling."""

    def test_registration_creates_student_profile_and_redirects_to_login(self):
        """A new account is a student and must log in after registration."""
        response = self.client.post(reverse('quizz_app:register'), {
            'username': 'nuevo_alumno',
            'email': 'nuevo_alumno@example.com',
            'password': 'clave-segura-123',
            'password_confirmation': 'clave-segura-123',
        })

        self.assertRedirects(response, reverse('quizz_app:login'))
        self.assertEqual(UserProfile.objects.get(user__username='nuevo_alumno').role, 'estudiante')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_does_not_require_role(self):
        """Users log in with their credentials only."""
        self.client.post(reverse('quizz_app:register'), {
            'username': 'alumno_login',
            'email': 'alumno_login@example.com',
            'password': 'clave-segura-123',
            'password_confirmation': 'clave-segura-123',
        })
        self.client.logout()

        response = self.client.post(reverse('quizz_app:login'), {
            'username': 'alumno_login',
            'password': 'clave-segura-123',
        })

        self.assertRedirects(response, reverse('quizz_app:index'))

    def test_login_accepts_email(self):
        """Users can authenticate with their registered email address."""
        self.client.post(reverse('quizz_app:register'), {
            'username': 'alumno_email',
            'email': 'alumno_email@example.com',
            'password': 'clave-segura-123',
            'password_confirmation': 'clave-segura-123',
        })

        response = self.client.post(reverse('quizz_app:login'), {
            'username': 'alumno_email@example.com',
            'password': 'clave-segura-123',
        })

        self.assertRedirects(response, reverse('quizz_app:index'))
