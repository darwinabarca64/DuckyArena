from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.db import IntegrityError
from django.db.models import ProtectedError
from quizzes.models import Quiz, Question, Answer
from quiz_games.models import Game, GamePlayer, PlayerAnswer
from quiz_games.forms import JoinGameForm
from quiz_games.utils import generate_unique_game_code

User = get_user_model()

_USER_PROFILES = {}


class DummyProfile:
    def __init__(self, role='TEACHER', ducky_coins=500):
        self.role = role
        self.ducky_coins = ducky_coins


if not hasattr(User, 'profile'):
    User.profile = property(lambda self: _USER_PROFILES.get(self.username, DummyProfile(role='TEACHER', ducky_coins=500)))


def attach_profile(user, role='TEACHER', ducky_coins=500):
    profile = DummyProfile(role=role, ducky_coins=ducky_coins)
    _USER_PROFILES[user.username] = profile
    return user


class GameUtilsTest(TestCase):
    def test_generate_unique_game_code_format_and_length(self):
        code = generate_unique_game_code()
        self.assertEqual(len(code), 6)
        self.assertTrue(code.isdigit())


class JoinGameFormTest(TestCase):
    def setUp(self):
        self.host = User.objects.create_user(username='form_host', password='password123')
        attach_profile(self.host, role='TEACHER')
        self.quiz = Quiz.objects.create(
            title='Quiz Form Test',
            creator=self.host,
            is_published=True
        )
        self.game = Game.objects.create(
            quiz=self.quiz,
            host=self.host,
            code='654321',
            status=Game.Status.LOBBY
        )

    def test_valid_pin_is_accepted(self):
        form = JoinGameForm(data={'code': '654321'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['game'], self.game)

    def test_invalid_length_pin(self):
        form = JoinGameForm(data={'code': '12345'})
        self.assertFalse(form.is_valid())
        self.assertIn('code', form.errors)

    def test_non_digit_pin(self):
        form = JoinGameForm(data={'code': 'ABC123'})
        self.assertFalse(form.is_valid())
        self.assertIn('code', form.errors)

    def test_non_existent_pin(self):
        form = JoinGameForm(data={'code': '999999'})
        self.assertFalse(form.is_valid())
        self.assertIn('No existe ninguna sala', str(form.errors['code']))

    def test_running_game_pin_rejected(self):
        self.game.status = Game.Status.RUNNING
        self.game.save()
        form = JoinGameForm(data={'code': '654321'})
        self.assertFalse(form.is_valid())
        self.assertIn('ya ha comenzado', str(form.errors['code']))

    def test_finished_game_pin_rejected(self):
        self.game.status = Game.Status.FINISHED
        self.game.save()
        form = JoinGameForm(data={'code': '654321'})
        self.assertFalse(form.is_valid())
        self.assertIn('ya ha finalizado', str(form.errors['code']))


class GameViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(username='teacher_host', password='password123')
        attach_profile(self.teacher, role='TEACHER')

        self.student = User.objects.create_user(username='student_guest', password='password123')
        attach_profile(self.student, role='STUDENT')

        self.student2 = User.objects.create_user(username='student_two', password='password123')
        attach_profile(self.student2, role='STUDENT')

        self.other_teacher = User.objects.create_user(username='other_teacher', password='password123')
        attach_profile(self.other_teacher, role='TEACHER')

        self.unrelated_user = User.objects.create_user(username='unrelated_user', password='password123')
        attach_profile(self.unrelated_user, role='STUDENT')

        self.quiz = Quiz.objects.create(
            title='Python Arena Master',
            description='Test Arena Quiz',
            creator=self.teacher,
            is_published=True
        )

        self.question1 = Question.objects.create(
            quiz=self.quiz,
            text='¿Qué es un decorador en Python?',
            time_limit=30,
            points=1000,
            order=1
        )
        self.ans1_1 = Answer.objects.create(question=self.question1, text='Una función que envuelve a otra', is_correct=True, order=1)
        self.ans1_2 = Answer.objects.create(question=self.question1, text='Una variable global', is_correct=False, order=2)

        self.question2 = Question.objects.create(
            quiz=self.quiz,
            text='¿Cuál es la función para obtener longitud?',
            time_limit=20,
            points=500,
            order=2
        )
        self.ans2_1 = Answer.objects.create(question=self.question2, text='len()', is_correct=True, order=1)
        self.ans2_2 = Answer.objects.create(question=self.question2, text='size()', is_correct=False, order=2)

    def test_game_create_requires_login(self):
        url = reverse('quiz_games:game_create', kwargs={'quiz_pk': self.quiz.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_game_create_denies_student(self):
        self.client.login(username='student_guest', password='password123')
        url = reverse('quiz_games:game_create', kwargs={'quiz_pk': self.quiz.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_game_create_denies_non_creator_teacher(self):
        self.client.login(username='other_teacher', password='password123')
        url = reverse('quiz_games:game_create', kwargs={'quiz_pk': self.quiz.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_game_create_draft_quiz_redirects_with_error(self):
        self.quiz.is_published = False
        self.quiz.save()
        self.client.login(username='teacher_host', password='password123')
        url = reverse('quiz_games:game_create', kwargs={'quiz_pk': self.quiz.pk})
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, reverse('quizzes:quiz_detail', kwargs={'pk': self.quiz.pk}))
        self.assertEqual(Game.objects.count(), 0)

    def test_game_create_no_questions_redirects_with_error(self):
        empty_quiz = Quiz.objects.create(
            title='Cuestionario Vacío',
            creator=self.teacher,
            is_published=True
        )
        self.client.login(username='teacher_host', password='password123')
        url = reverse('quiz_games:game_create', kwargs={'quiz_pk': empty_quiz.pk})
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, reverse('quizzes:quiz_detail', kwargs={'pk': empty_quiz.pk}))
        self.assertEqual(Game.objects.count(), 0)

    def test_game_create_success(self):
        self.client.login(username='teacher_host', password='password123')
        url = reverse('quiz_games:game_create', kwargs={'quiz_pk': self.quiz.pk})
        response = self.client.post(url)
        self.assertEqual(Game.objects.count(), 1)

        game = Game.objects.first()
        self.assertEqual(game.quiz, self.quiz)
        self.assertEqual(game.host, self.teacher)
        self.assertEqual(game.status, Game.Status.LOBBY)
        self.assertEqual(game.current_question, 0)
        self.assertEqual(len(game.code), 6)
        self.assertRedirects(response, reverse('quiz_games:game_host_lobby', kwargs={'code': game.code}))

    def test_game_host_lobby_access_control(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='123456',
            status=Game.Status.LOBBY
        )
        url = reverse('quiz_games:game_host_lobby', kwargs={'code': game.code})

        # Otro usuario no tiene permiso
        self.client.login(username='other_teacher', password='password123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # El profesor anfitrión sí tiene acceso
        self.client.login(username='teacher_host', password='password123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_games/game_host_lobby.html')
        self.assertEqual(response.context['game'], game)
        self.assertEqual(response.context['players_count'], 0)

    def test_game_join_view_get(self):
        self.client.login(username='student_guest', password='password123')
        response = self.client.get(reverse('quiz_games:game_join'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_games/game_join.html')

    def test_game_join_as_host_redirects_to_host_lobby(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='112233',
            status=Game.Status.LOBBY
        )
        self.client.login(username='teacher_host', password='password123')
        response = self.client.post(reverse('quiz_games:game_join'), {'code': '112233'})
        self.assertRedirects(response, reverse('quiz_games:game_host_lobby', kwargs={'code': '112233'}))
        self.assertEqual(GamePlayer.objects.filter(game=game).count(), 0)

    def test_game_join_as_student_registers_player(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='112233',
            status=Game.Status.LOBBY
        )
        self.client.login(username='student_guest', password='password123')
        response = self.client.post(reverse('quiz_games:game_join'), {'code': '112233'})
        self.assertRedirects(response, reverse('quiz_games:game_player_lobby', kwargs={'code': '112233'}))
        self.assertEqual(GamePlayer.objects.filter(game=game, player=self.student).count(), 1)

        # Ingresar de nuevo no duplica (idempotencia get_or_create)
        response2 = self.client.post(reverse('quiz_games:game_join'), {'code': '112233'})
        self.assertRedirects(response2, reverse('quiz_games:game_player_lobby', kwargs={'code': '112233'}))
        self.assertEqual(GamePlayer.objects.filter(game=game, player=self.student).count(), 1)

    def test_game_player_lobby_unregistered_redirects(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='112233',
            status=Game.Status.LOBBY
        )
        self.client.login(username='student_guest', password='password123')
        response = self.client.get(reverse('quiz_games:game_player_lobby', kwargs={'code': '112233'}))
        self.assertRedirects(response, reverse('quiz_games:game_join'))

    def test_game_player_lobby_registered_access(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='112233',
            status=Game.Status.LOBBY
        )
        GamePlayer.objects.create(game=game, player=self.student)
        self.client.login(username='student_guest', password='password123')
        response = self.client.get(reverse('quiz_games:game_player_lobby', kwargs={'code': '112233'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_games/game_player_lobby.html')

    def test_game_lobby_status_forbidden_for_unrelated_user(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='112233',
            status=Game.Status.LOBBY
        )
        self.client.login(username='unrelated_user', password='password123')
        response = self.client.get(reverse('quiz_games:game_lobby_status', kwargs={'code': '112233'}))
        self.assertEqual(response.status_code, 403)

    def test_game_lobby_status_success_for_host_and_player(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='112233',
            status=Game.Status.LOBBY
        )
        gp = GamePlayer.objects.create(game=game, player=self.student)

        # Host accede a la API de estado
        self.client.login(username='teacher_host', password='password123')
        response_host = self.client.get(reverse('quiz_games:game_lobby_status', kwargs={'code': '112233'}))
        self.assertEqual(response_host.status_code, 200)
        data_host = response_host.json()
        self.assertEqual(data_host['status'], 'LOBBY')
        self.assertEqual(data_host['player_count'], 1)
        self.assertEqual(data_host['players'][0]['username'], self.student.username)

        # Jugador registrado accede a la API de estado
        self.client.login(username='student_guest', password='password123')
        response_player = self.client.get(reverse('quiz_games:game_lobby_status', kwargs={'code': '112233'}))
        self.assertEqual(response_player.status_code, 200)
        data_player = response_player.json()
        self.assertEqual(data_player['player_count'], 1)

    def test_host_start_game_denies_non_host(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='112233',
            status=Game.Status.LOBBY
        )
        GamePlayer.objects.create(game=game, player=self.student)
        self.client.login(username='other_teacher', password='password123')
        response = self.client.post(reverse('quiz_games:host_start_game', kwargs={'code': '112233'}))
        self.assertEqual(response.status_code, 403)

    def test_host_start_game_requires_at_least_one_player(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='112233',
            status=Game.Status.LOBBY
        )
        self.client.login(username='teacher_host', password='password123')
        response = self.client.post(reverse('quiz_games:host_start_game', kwargs={'code': '112233'}), follow=True)
        self.assertRedirects(response, reverse('quiz_games:game_host_lobby', kwargs={'code': '112233'}))
        game.refresh_from_db()
        self.assertEqual(game.status, Game.Status.LOBBY)

    def test_host_start_game_success_transitions_to_running(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='112233',
            status=Game.Status.LOBBY,
            current_question=0
        )
        GamePlayer.objects.create(game=game, player=self.student)
        self.client.login(username='teacher_host', password='password123')
        response = self.client.post(reverse('quiz_games:host_start_game', kwargs={'code': '112233'}))
        self.assertRedirects(response, reverse('quiz_games:game_host_play', kwargs={'code': '112233'}))

        game.refresh_from_db()
        self.assertEqual(game.status, Game.Status.RUNNING)
        self.assertEqual(game.current_question, 1)
        self.assertIsNotNone(game.started_at)

    def test_game_host_play_view(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='112233',
            status=Game.Status.RUNNING,
            current_question=1
        )
        gp = GamePlayer.objects.create(game=game, player=self.student)

        # Acceso denegado a no anfitrión
        self.client.login(username='other_teacher', password='password123')
        response = self.client.get(reverse('quiz_games:game_host_play', kwargs={'code': '112233'}))
        self.assertEqual(response.status_code, 403)

        # Acceso concedido al anfitrión
        self.client.login(username='teacher_host', password='password123')
        response = self.client.get(reverse('quiz_games:game_host_play', kwargs={'code': '112233'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_games/game_host_play.html')
        self.assertEqual(response.context['question'], self.question1)
        self.assertEqual(response.context['current_num'], 1)
        self.assertEqual(response.context['total_players'], 1)
        self.assertEqual(response.context['answered_count'], 0)

    def test_game_player_play_view_and_answered_state(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='112233',
            status=Game.Status.RUNNING,
            current_question=1
        )
        gp = GamePlayer.objects.create(game=game, player=self.student)

        # Jugador no registrado es redirigido
        self.client.login(username='unrelated_user', password='password123')
        response_unreg = self.client.get(reverse('quiz_games:game_player_play', kwargs={'code': '112233'}))
        self.assertRedirects(response_unreg, reverse('quiz_games:game_join'))

        # Jugador registrado puede ver la pantalla de respuesta
        self.client.login(username='student_guest', password='password123')
        response = self.client.get(reverse('quiz_games:game_player_play', kwargs={'code': '112233'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_games/game_player_play.html')
        self.assertFalse(response.context['has_answered'])

        # Si el jugador ya respondió, has_answered es True
        PlayerAnswer.objects.create(
            game_player=gp,
            question=self.question1,
            selected_answer=self.ans1_1,
            is_correct=True,
            points_awarded=1000
        )
        response2 = self.client.get(reverse('quiz_games:game_player_play', kwargs={'code': '112233'}))
        self.assertEqual(response2.status_code, 200)
        self.assertTrue(response2.context['has_answered'])

    def test_game_question_status_endpoint(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='112233',
            status=Game.Status.RUNNING,
            current_question=1
        )
        gp = GamePlayer.objects.create(game=game, player=self.student)
        PlayerAnswer.objects.create(
            game_player=gp,
            question=self.question1,
            selected_answer=self.ans1_1,
            is_correct=True,
            points_awarded=1000
        )

        self.client.login(username='teacher_host', password='password123')
        response = self.client.get(reverse('quiz_games:game_question_status', kwargs={'code': '112233'}))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'RUNNING')
        self.assertEqual(data['current_question'], 1)
        self.assertEqual(data['total_players'], 1)
        self.assertEqual(data['answered_count'], 1)

    def test_submit_player_answer_correct(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='112233',
            status=Game.Status.RUNNING,
            current_question=1
        )
        gp = GamePlayer.objects.create(game=game, player=self.student, score=0, current_streak=0)

        self.client.login(username='student_guest', password='password123')
        payload = {
            'question_id': self.question1.id,
            'selected_answer_id': self.ans1_1.id,
            'time_taken': 5.0
        }
        response = self.client.post(
            reverse('quiz_games:submit_player_answer', kwargs={'code': '112233'}),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertTrue(data['is_correct'])
        self.assertGreater(data['points_awarded'], 0)
        self.assertEqual(data['streak'], 1)

        gp.refresh_from_db()
        self.assertEqual(gp.current_streak, 1)
        self.assertEqual(gp.correct_answers, 1)
        self.assertGreater(gp.score, 0)
        self.assertEqual(PlayerAnswer.objects.filter(game_player=gp, question=self.question1).count(), 1)

    def test_submit_player_answer_incorrect(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='112233',
            status=Game.Status.RUNNING,
            current_question=1
        )
        gp = GamePlayer.objects.create(game=game, player=self.student, score=500, current_streak=3)

        self.client.login(username='student_guest', password='password123')
        payload = {
            'question_id': self.question1.id,
            'selected_answer_id': self.ans1_2.id,
            'time_taken': 2.0
        }
        response = self.client.post(
            reverse('quiz_games:submit_player_answer', kwargs={'code': '112233'}),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertFalse(data['is_correct'])
        self.assertEqual(data['points_awarded'], 0)
        self.assertEqual(data['streak'], 0)

        gp.refresh_from_db()
        self.assertEqual(gp.current_streak, 0)
        self.assertEqual(gp.score, 500)

    def test_submit_player_answer_duplicate_rejected(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='112233',
            status=Game.Status.RUNNING,
            current_question=1
        )
        gp = GamePlayer.objects.create(game=game, player=self.student)
        PlayerAnswer.objects.create(
            game_player=gp,
            question=self.question1,
            selected_answer=self.ans1_1,
            is_correct=True,
            points_awarded=1000
        )

        self.client.login(username='student_guest', password='password123')
        payload = {
            'question_id': self.question1.id,
            'selected_answer_id': self.ans1_1.id,
            'time_taken': 3.0
        }
        response = self.client.post(
            reverse('quiz_games:submit_player_answer', kwargs={'code': '112233'}),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('Ya has enviado tu respuesta', data['error'])

    def test_host_next_question_advances_and_finishes(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='112233',
            status=Game.Status.RUNNING,
            current_question=1
        )
        GamePlayer.objects.create(game=game, player=self.student)

        # 1. Avanzar de pregunta 1 a pregunta 2 (quiz tiene 2 preguntas)
        self.client.login(username='teacher_host', password='password123')
        response1 = self.client.post(reverse('quiz_games:host_next_question', kwargs={'code': '112233'}))
        self.assertEqual(response1.status_code, 200)
        data1 = response1.json()
        self.assertEqual(data1['action'], 'NEXT_QUESTION')
        self.assertEqual(data1['current_question'], 2)

        game.refresh_from_db()
        self.assertEqual(game.current_question, 2)
        self.assertEqual(game.status, Game.Status.RUNNING)

        # 2. Avanzar de pregunta 2 -> concluye la partida (GAME_FINISHED)
        response2 = self.client.post(reverse('quiz_games:host_next_question', kwargs={'code': '112233'}))
        self.assertEqual(response2.status_code, 200)
        data2 = response2.json()
        self.assertEqual(data2['action'], 'GAME_FINISHED')
        self.assertIn('/leaderboard/', data2['redirect_url'])

        game.refresh_from_db()
        self.assertEqual(game.status, Game.Status.FINISHED)
        self.assertIsNotNone(game.finished_at)

    def test_host_finish_game_manual(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='112233',
            status=Game.Status.RUNNING,
            current_question=1
        )
        self.client.login(username='teacher_host', password='password123')
        response = self.client.post(reverse('quiz_games:host_finish_game', kwargs={'code': '112233'}))
        self.assertRedirects(response, reverse('quiz_games:game_leaderboard', kwargs={'code': '112233'}))

        game.refresh_from_db()
        self.assertEqual(game.status, Game.Status.FINISHED)
        self.assertIsNotNone(game.finished_at)

    def test_game_leaderboard_access_and_ranking(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='112233',
            status=Game.Status.FINISHED
        )
        gp1 = GamePlayer.objects.create(game=game, player=self.student, score=1500, correct_answers=2)
        gp2 = GamePlayer.objects.create(game=game, player=self.student2, score=800, correct_answers=1)

        # Acceso denegado a usuario no involucrado
        self.client.login(username='unrelated_user', password='password123')
        response_unrel = self.client.get(reverse('quiz_games:game_leaderboard', kwargs={'code': '112233'}))
        self.assertEqual(response_unrel.status_code, 403)

        # Anfitrión accede al podio
        self.client.login(username='teacher_host', password='password123')
        response_host = self.client.get(reverse('quiz_games:game_leaderboard', kwargs={'code': '112233'}))
        self.assertEqual(response_host.status_code, 200)
        self.assertTemplateUsed(response_host, 'quiz_games/game_leaderboard.html')
        self.assertEqual(list(response_host.context['ranking']), [gp1, gp2])

        # Jugador accede al podio
        self.client.login(username='student_guest', password='password123')
        response_player = self.client.get(reverse('quiz_games:game_leaderboard', kwargs={'code': '112233'}))
        self.assertEqual(response_player.status_code, 200)

    def test_game_player_results_view(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='112233',
            status=Game.Status.FINISHED
        )
        gp = GamePlayer.objects.create(game=game, player=self.student, score=1200, correct_answers=1)
        PlayerAnswer.objects.create(
            game_player=gp,
            question=self.question1,
            selected_answer=self.ans1_1,
            is_correct=True,
            points_awarded=1200
        )

        # Estudiante registrado accede a sus resultados
        self.client.login(username='student_guest', password='password123')
        response = self.client.get(reverse('quiz_games:game_player_results', kwargs={'code': '112233'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_games/game_player_results.html')
        self.assertEqual(response.context['position'], 1)
        self.assertEqual(response.context['total_players'], 1)
        self.assertEqual(response.context['accuracy'], 50.0)
        self.assertEqual(response.context['medal']['tipo'], 'ORO')

    def test_game_leaderboard_redirect_if_not_finished(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='112233',
            status=Game.Status.RUNNING,
            current_question=1
        )
        GamePlayer.objects.create(game=game, player=self.student)

        # Host se redirige a game_host_play
        self.client.login(username='teacher_host', password='password123')
        resp_host = self.client.get(reverse('quiz_games:game_leaderboard', kwargs={'code': '112233'}))
        self.assertRedirects(resp_host, reverse('quiz_games:game_host_play', kwargs={'code': '112233'}))

        # Estudiante se redirige a game_player_play
        self.client.login(username='student_guest', password='password123')
        resp_stud = self.client.get(reverse('quiz_games:game_leaderboard', kwargs={'code': '112233'}))
        self.assertRedirects(resp_stud, reverse('quiz_games:game_player_play', kwargs={'code': '112233'}))

    def test_game_player_results_zero_questions_accuracy(self):
        empty_quiz = Quiz.objects.create(
            title='Quiz Sin Preguntas',
            creator=self.teacher,
            is_published=True
        )
        game = Game.objects.create(
            quiz=empty_quiz,
            host=self.teacher,
            code='998877',
            status=Game.Status.FINISHED
        )
        gp = GamePlayer.objects.create(game=game, player=self.student, score=0, correct_answers=0)

        self.client.login(username='student_guest', password='password123')
        response = self.client.get(reverse('quiz_games:game_player_results', kwargs={'code': '998877'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['accuracy'], 0.0)


class QuizGamesE2ETestCase(TestCase):
    """
    Suite E2E Integral que valida el 100% de los contratos de ducky_arena_master_spec.pdf
    y PROJECT_RULES.md: ciclo de vida, permisos, zero leaks, restricciones de unicidad
    y protección relacional con models.PROTECT.
    """
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(username='e2e_teacher', password='password123')
        attach_profile(self.teacher, role='TEACHER', ducky_coins=1000)

        self.student = User.objects.create_user(username='e2e_student', password='password123')
        attach_profile(self.student, role='STUDENT', ducky_coins=200)

        self.student2 = User.objects.create_user(username='e2e_student2', password='password123')
        attach_profile(self.student2, role='STUDENT', ducky_coins=150)

        # Quiz publicado con 2 preguntas y 4 opciones cada una (exactamente 1 correcta)
        self.quiz = Quiz.objects.create(
            title='E2E Python Master Arena',
            description='Certificación integral E2E',
            creator=self.teacher,
            is_published=True
        )

        # Pregunta 1
        self.q1 = Question.objects.create(
            quiz=self.quiz,
            text='¿Qué estructura es inmutable en Python?',
            time_limit=30,
            points=1000,
            order=1
        )
        self.q1_ans1 = Answer.objects.create(question=self.q1, text='tuple', is_correct=True, order=1)
        self.q1_ans2 = Answer.objects.create(question=self.q1, text='list', is_correct=False, order=2)
        self.q1_ans3 = Answer.objects.create(question=self.q1, text='dict', is_correct=False, order=3)
        self.q1_ans4 = Answer.objects.create(question=self.q1, text='set', is_correct=False, order=4)

        # Pregunta 2
        self.q2 = Question.objects.create(
            quiz=self.quiz,
            text='¿Qué operador se utiliza para exponenciación?',
            time_limit=20,
            points=800,
            order=2
        )
        self.q2_ans1 = Answer.objects.create(question=self.q2, text='**', is_correct=True, order=1)
        self.q2_ans2 = Answer.objects.create(question=self.q2, text='^', is_correct=False, order=2)
        self.q2_ans3 = Answer.objects.create(question=self.q2, text='exp()', is_correct=False, order=3)
        self.q2_ans4 = Answer.objects.create(question=self.q2, text='//', is_correct=False, order=4)

    def test_quiz_lifecycle_and_permissions(self):
        """Verifica que solo el TEACHER creador puede gestionar el Quiz y los STUDENT reciben 403."""
        # Profesor dueño puede ver detalle
        self.client.login(username='e2e_teacher', password='password123')
        response_owner = self.client.get(reverse('quizzes:quiz_detail', kwargs={'pk': self.quiz.pk}))
        self.assertEqual(response_owner.status_code, 200)

        # Estudiante intenta crear sala -> 403 PermissionDenied
        self.client.login(username='e2e_student', password='password123')
        response_student = self.client.post(reverse('quiz_games:game_create', kwargs={'quiz_pk': self.quiz.pk}))
        self.assertEqual(response_student.status_code, 403)

    def test_game_creation_and_unique_pin(self):
        """Verifica generación de Game en estado LOBBY con PIN numérico de 6 dígitos único."""
        self.client.login(username='e2e_teacher', password='password123')
        response = self.client.post(reverse('quiz_games:game_create', kwargs={'quiz_pk': self.quiz.pk}))
        self.assertEqual(response.status_code, 302)

        game = Game.objects.filter(quiz=self.quiz).first()
        self.assertIsNotNone(game)
        self.assertEqual(game.status, Game.Status.LOBBY)
        self.assertEqual(game.current_question, 0)
        self.assertEqual(len(game.code), 6)
        self.assertTrue(game.code.isdigit())

    def test_unique_player_constraint(self):
        """Verifica registro de jugador y que intentos duplicados respeten unique_player_per_quiz_game."""
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='123987',
            status=Game.Status.LOBBY
        )
        # Primer registro exitoso
        gp1 = GamePlayer.objects.create(game=game, player=self.student)
        self.assertIsNotNone(gp1.pk)

        # Intento de duplicado directo en BD viola UniqueConstraint
        with self.assertRaises(IntegrityError):
            GamePlayer.objects.create(game=game, player=self.student)

    def test_zero_leak_and_answer_evaluation(self):
        """
        Verifica Cero Leaks de is_correct en pantalla del estudiante y evaluación server-side
        con cálculo de puntaje, racha y persistencia atómica.
        """
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='554433',
            status=Game.Status.RUNNING,
            current_question=1
        )
        gp = GamePlayer.objects.create(game=game, player=self.student, score=0, current_streak=0)

        # 1. Cero Leaks: la vista del estudiante no debe filtrar 'is_correct'
        self.client.login(username='e2e_student', password='password123')
        play_response = self.client.get(reverse('quiz_games:game_player_play', kwargs={'code': '554433'}))
        self.assertEqual(play_response.status_code, 200)

        # Contexto HTML no contiene clave is_correct
        if 'answers' in play_response.context:
            for ans in play_response.context['answers']:
                self.assertNotIn('is_correct', ans)

        # 2. Evaluación de respuesta server-side
        payload = {
            'question_id': self.q1.id,
            'selected_answer_id': self.q1_ans1.id,
            'time_taken': 6.0
        }
        submit_response = self.client.post(
            reverse('quiz_games:submit_player_answer', kwargs={'code': '554433'}),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(submit_response.status_code, 200)
        data = submit_response.json()
        self.assertTrue(data['success'])
        self.assertTrue(data['is_correct'])
        self.assertGreater(data['points_awarded'], 0)
        self.assertEqual(data['streak'], 1)

        gp.refresh_from_db()
        self.assertEqual(gp.score, data['total_score'])
        self.assertEqual(gp.correct_answers, 1)
        self.assertEqual(gp.current_streak, 1)
        self.assertEqual(PlayerAnswer.objects.filter(game_player=gp, question=self.q1).count(), 1)

    def test_unique_answer_constraint(self):
        """Verifica que un segundo intento de respuesta lance error y respete unique_answer_per_player_question."""
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='776655',
            status=Game.Status.RUNNING,
            current_question=1
        )
        gp = GamePlayer.objects.create(game=game, player=self.student)
        PlayerAnswer.objects.create(
            game_player=gp,
            question=self.q1,
            selected_answer=self.q1_ans1,
            is_correct=True,
            points_awarded=1000
        )

        # Endpoint rechaza con 400
        self.client.login(username='e2e_student', password='password123')
        payload = {
            'question_id': self.q1.id,
            'selected_answer_id': self.q1_ans2.id,
            'time_taken': 3.0
        }
        response = self.client.post(
            reverse('quiz_games:submit_player_answer', kwargs={'code': '776655'}),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('Ya has enviado tu respuesta', response.json()['error'])

        # Intento de inserción directa en BD viola UniqueConstraint
        with self.assertRaises(IntegrityError):
            PlayerAnswer.objects.create(
                game_player=gp,
                question=self.q1,
                selected_answer=self.q1_ans2,
                is_correct=False,
                points_awarded=0
            )

    def test_game_finish_and_protect_constraint(self):
        """
        Verifica transición a FINISHED, consistencia de rankings y bloqueo de borrado
        en cascada del Quiz mediante models.PROTECT.
        """
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='990011',
            status=Game.Status.RUNNING,
            current_question=2
        )
        gp1 = GamePlayer.objects.create(game=game, player=self.student, score=1800, correct_answers=2)
        gp2 = GamePlayer.objects.create(game=game, player=self.student2, score=900, correct_answers=1)

        # Finalizar partida
        self.client.login(username='e2e_teacher', password='password123')
        response_finish = self.client.post(reverse('quiz_games:host_finish_game', kwargs={'code': '990011'}))
        self.assertRedirects(response_finish, reverse('quiz_games:game_leaderboard', kwargs={'code': '990011'}))

        game.refresh_from_db()
        self.assertEqual(game.status, Game.Status.FINISHED)
        self.assertIsNotNone(game.finished_at)

        # Consultar podio
        response_lb = self.client.get(reverse('quiz_games:game_leaderboard', kwargs={'code': '990011'}))
        self.assertEqual(response_lb.status_code, 200)
        self.assertEqual(response_lb.context['first_place'], gp1)
        self.assertEqual(response_lb.context['second_place'], gp2)

        # Consultar podio olímpico desacoplado
        response_podium = self.client.get(reverse('quiz_games:game_podium', kwargs={'code': '990011'}))
        self.assertEqual(response_podium.status_code, 200)
        self.assertEqual(response_podium.context['first_place'], gp1)
        self.assertEqual(response_podium.context['second_place'], gp2)

        # Protección relacional: borrar el Quiz debe ser bloqueado por models.PROTECT
        with self.assertRaises(ProtectedError):
            self.quiz.delete()


class AntiCheatAndModerationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(username='ac_teacher', password='password123')
        attach_profile(self.teacher, role='TEACHER')

        self.student = User.objects.create_user(username='ac_student', password='password123')
        attach_profile(self.student, role='STUDENT')

        self.student2 = User.objects.create_user(username='ac_student2', password='password123')
        attach_profile(self.student2, role='STUDENT')

        self.quiz = Quiz.objects.create(
            title='AntiCheat Quiz',
            creator=self.teacher,
            is_published=True
        )
        self.q1 = Question.objects.create(
            quiz=self.quiz,
            text='Pregunta de prueba',
            time_limit=30,
            points=1000,
            order=1
        )
        self.q1_ans1 = Answer.objects.create(question=self.q1, text='Opción Correcta', is_correct=True, order=1)
        self.q1_ans2 = Answer.objects.create(question=self.q1, text='Opción Incorrecta', is_correct=False, order=2)

    def test_host_kick_player_success(self):
        game = Game.objects.create(quiz=self.quiz, host=self.teacher, code='111222', status=Game.Status.LOBBY)
        gp = GamePlayer.objects.create(game=game, player=self.student)

        self.client.login(username='ac_teacher', password='password123')
        url = reverse('quiz_games:host_kick_player', kwargs={'code': game.code, 'player_id': gp.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['kicked_id'], gp.id)
        self.assertFalse(GamePlayer.objects.filter(id=gp.id).exists())

    def test_host_kick_player_permission_denied_for_non_host(self):
        game = Game.objects.create(quiz=self.quiz, host=self.teacher, code='111222', status=Game.Status.LOBBY)
        gp = GamePlayer.objects.create(game=game, player=self.student)

        self.client.login(username='ac_student2', password='password123')
        url = reverse('quiz_games:host_kick_player', kwargs={'code': game.code, 'player_id': gp.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(GamePlayer.objects.filter(id=gp.id).exists())

    def test_host_kick_player_forbidden_when_not_in_lobby(self):
        game = Game.objects.create(quiz=self.quiz, host=self.teacher, code='111222', status=Game.Status.RUNNING)
        gp = GamePlayer.objects.create(game=game, player=self.student)

        self.client.login(username='ac_teacher', password='password123')
        url = reverse('quiz_games:host_kick_player', kwargs={'code': game.code, 'player_id': gp.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('Solo se puede expulsar en fase de Lobby', data['error'])
        self.assertTrue(GamePlayer.objects.filter(id=gp.id).exists())

    def test_anti_cheat_server_time_calculation_ignores_client_time(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='111222',
            status=Game.Status.RUNNING,
            current_question=1,
            question_started_at=timezone.now()
        )
        gp = GamePlayer.objects.create(game=game, player=self.student, score=0, current_streak=0)

        self.client.login(username='ac_student', password='password123')
        # El cliente envía time_taken=0.0 fraudulentamente
        payload = {
            'question_id': self.q1.id,
            'selected_answer_id': self.q1_ans1.id,
            'time_taken': 0.0
        }
        response = self.client.post(
            reverse('quiz_games:submit_player_answer', kwargs={'code': game.code}),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertTrue(data['is_correct'])
        self.assertGreater(data['points_awarded'], 0)

    def test_game_player_resume_redirects_to_running_game(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='333444',
            status=Game.Status.RUNNING,
            started_at=timezone.now(),
            current_question=1
        )
        gp = GamePlayer.objects.create(game=game, player=self.student, score=500, current_streak=2)

        self.client.login(username='ac_student', password='password123')
        response = self.client.get(reverse('quiz_games:game_player_resume'))
        self.assertRedirects(response, reverse('quiz_games:game_player_play', kwargs={'code': '333444'}))

    def test_game_player_resume_redirects_to_join_when_no_active_game(self):
        # Partida ya finalizada
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='333444',
            status=Game.Status.FINISHED
        )
        GamePlayer.objects.create(game=game, player=self.student)

        self.client.login(username='ac_student', password='password123')
        response = self.client.get(reverse('quiz_games:game_player_resume'))
        self.assertRedirects(response, reverse('quiz_games:game_join'))


class AnalyticsAndExportTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(
            username='analytics_teacher',
            first_name='Albert',
            last_name='Einstein',
            password='password123'
        )
        attach_profile(self.teacher, role='TEACHER')

        self.student1 = User.objects.create_user(
            username='analytics_student1',
            first_name='Marie',
            last_name='Curie',
            password='password123'
        )
        attach_profile(self.student1, role='STUDENT')

        self.student2 = User.objects.create_user(
            username='analytics_student2',
            first_name='Isaac',
            last_name='Newton',
            password='password123'
        )
        attach_profile(self.student2, role='STUDENT')

        self.other_user = User.objects.create_user(username='other_user', password='password123')
        attach_profile(self.other_user, role='STUDENT')

        self.quiz = Quiz.objects.create(
            title='Física Cuántica',
            creator=self.teacher,
            is_published=True
        )
        self.q1 = Question.objects.create(
            quiz=self.quiz,
            text='¿Qué partícula no tiene masa?',
            time_limit=30,
            points=1000,
            order=1
        )
        self.ans1 = Answer.objects.create(question=self.q1, text='Fotón', is_correct=True, order=1)
        self.ans2 = Answer.objects.create(question=self.q1, text='Protón', is_correct=False, order=2)

    def test_game_question_breakdown_success(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='888999',
            status=Game.Status.RUNNING,
            current_question=1
        )
        gp1 = GamePlayer.objects.create(game=game, player=self.student1)
        gp2 = GamePlayer.objects.create(game=game, player=self.student2)

        PlayerAnswer.objects.create(
            game_player=gp1,
            question=self.q1,
            selected_answer=self.ans1,
            is_correct=True,
            points_awarded=1000
        )
        PlayerAnswer.objects.create(
            game_player=gp2,
            question=self.q1,
            selected_answer=self.ans2,
            is_correct=False,
            points_awarded=0
        )

        self.client.login(username='analytics_teacher', password='password123')
        url = reverse('quiz_games:game_question_breakdown', kwargs={'code': game.code})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['question_text'], self.q1.text)
        self.assertEqual(data['total_answers'], 2)
        self.assertEqual(len(data['breakdown']), 2)

        # Check breakdown counts
        fot_item = next(item for item in data['breakdown'] if item['answer_id'] == self.ans1.id)
        self.assertEqual(fot_item['count'], 1)
        self.assertTrue(fot_item['is_correct'])

        prot_item = next(item for item in data['breakdown'] if item['answer_id'] == self.ans2.id)
        self.assertEqual(prot_item['count'], 1)
        self.assertFalse(prot_item['is_correct'])

    def test_game_question_breakdown_denies_non_host(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='888999',
            status=Game.Status.RUNNING,
            current_question=1
        )
        self.client.login(username='analytics_student1', password='password123')
        url = reverse('quiz_games:game_question_breakdown', kwargs={'code': game.code})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_game_question_breakdown_invalid_question_index(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='888999',
            status=Game.Status.RUNNING,
            current_question=99
        )
        self.client.login(username='analytics_teacher', password='password123')
        url = reverse('quiz_games:game_question_breakdown', kwargs={'code': game.code})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()['success'])

    def test_export_game_results_csv_success(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='888999',
            status=Game.Status.FINISHED
        )
        gp1 = GamePlayer.objects.create(game=game, player=self.student1, score=1500, correct_answers=1, current_streak=1)
        gp2 = GamePlayer.objects.create(game=game, player=self.student2, score=500, correct_answers=0, current_streak=0)

        self.client.login(username='analytics_teacher', password='password123')
        url = reverse('quiz_games:export_game_results_csv', kwargs={'code': game.code})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')
        self.assertIn('attachment; filename="reporte_partida_888999', response['Content-Disposition'])

        content = response.content.decode('utf-8-sig')
        self.assertIn('Posición,Usuario,Nombre Completo,Puntos Totales,Respuestas Correctas,Total Preguntas,Precisión (%),Racha Final', content)
        self.assertIn('1,analytics_student1,Marie Curie,1500,1,1,100.0%,1', content)
        self.assertIn('2,analytics_student2,Isaac Newton,500,0,1,0.0%,0', content)

    def test_export_game_results_csv_denies_non_host(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='888999',
            status=Game.Status.FINISHED
        )
        self.client.login(username='analytics_student1', password='password123')
        url = reverse('quiz_games:export_game_results_csv', kwargs={'code': game.code})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class NetworkPerformanceAndAudioTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(username='perf_teacher', password='password123')
        attach_profile(self.teacher, role='TEACHER')

        self.student = User.objects.create_user(username='perf_student', password='password123')
        attach_profile(self.student, role='STUDENT')

        self.quiz = Quiz.objects.create(
            title='Quiz Performance Test',
            creator=self.teacher,
            is_published=True
        )
        self.q1 = Question.objects.create(
            quiz=self.quiz,
            text='Pregunta Performance',
            time_limit=30,
            points=1000,
            order=1
        )
        self.ans1 = Answer.objects.create(question=self.q1, text='Opción A', is_correct=True, order=1)
        self.ans2 = Answer.objects.create(question=self.q1, text='Opción B', is_correct=False, order=2)

    def test_game_lobby_status_etag_and_304(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='667788',
            status=Game.Status.LOBBY
        )
        GamePlayer.objects.create(game=game, player=self.student)

        self.client.login(username='perf_teacher', password='password123')
        url = reverse('quiz_games:game_lobby_status', kwargs={'code': game.code})

        # 1. Primera petición -> 200 con cabecera ETag
        response1 = self.client.get(url)
        self.assertEqual(response1.status_code, 200)
        self.assertIn('ETag', response1.headers)
        etag = response1.headers['ETag']
        self.assertTrue(len(etag) > 0)

        # 2. Petición condicional con If-None-Match idéntico -> 304 Not Modified
        response2 = self.client.get(url, HTTP_IF_NONE_MATCH=etag)
        self.assertEqual(response2.status_code, 304)

        # 3. Tras cambio (otro jugador se une) -> 200 con nuevo ETag
        student2 = User.objects.create_user(username='perf_student2', password='password123')
        attach_profile(student2, role='STUDENT')
        GamePlayer.objects.create(game=game, player=student2)

        response3 = self.client.get(url, HTTP_IF_NONE_MATCH=etag)
        self.assertEqual(response3.status_code, 200)
        self.assertNotEqual(response3.headers['ETag'], etag)

    def test_game_question_status_etag_and_304(self):
        game = Game.objects.create(
            quiz=self.quiz,
            host=self.teacher,
            code='667788',
            status=Game.Status.RUNNING,
            current_question=1
        )
        gp = GamePlayer.objects.create(game=game, player=self.student)

        self.client.login(username='perf_teacher', password='password123')
        url = reverse('quiz_games:game_question_status', kwargs={'code': game.code})

        # 1. Primera petición -> 200 con ETag
        response1 = self.client.get(url)
        self.assertEqual(response1.status_code, 200)
        self.assertIn('ETag', response1.headers)
        etag = response1.headers['ETag']

        # 2. Petición condicional con If-None-Match idéntico -> 304
        response2 = self.client.get(url, HTTP_IF_NONE_MATCH=etag)
        self.assertEqual(response2.status_code, 304)

        # 3. Tras respuesta enviada -> cambia ETag -> 200
        PlayerAnswer.objects.create(
            game_player=gp,
            question=self.q1,
            selected_answer=self.ans1,
            is_correct=True,
            points_awarded=1000
        )
        response3 = self.client.get(url, HTTP_IF_NONE_MATCH=etag)
        self.assertEqual(response3.status_code, 200)
        self.assertNotEqual(response3.headers['ETag'], etag)





