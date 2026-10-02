import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from django.db import transaction
from .models import Game, GamePlayer, PlayerAnswer
from quizzes.models import Question, Answer


class GameRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.code = self.scope['url_route']['kwargs']['code']
        self.room_group_name = f"game_{self.code}"
        self.user = self.scope.get('user')

        if self.user and self.user.is_authenticated:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            await self.send(text_data=json.dumps({
                'type': 'connection_established',
                'message': f'Conectado exitosamente a la sala {self.code}',
                'user': self.user.username
            }))
        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except (ValueError, TypeError):
            return

        action = data.get('action')

        if action == 'submit_answer':
            await self.handle_submit_answer(data)
        elif action == 'update_avatar':
            await self.handle_update_avatar(data)
        elif action == 'host_next_question':
            await self.handle_host_next_question()
        elif action == 'host_start_game':
            await self.handle_host_start_game()
        elif action == 'ping':
            await self.send(text_data=json.dumps({'type': 'pong', 'status': 'alive'}))

    async def handle_submit_answer(self, data):
        """Procesa y califica la respuesta del alumno de forma segura en backend."""
        question_id = data.get('question_id')
        selected_answer_id = data.get('selected_answer_id')

        result = await self.process_answer_db(self.user, self.code, question_id, selected_answer_id)

        # Enviar feedback privado individual al alumno que respondió
        await self.send(text_data=json.dumps({
            'type': 'answer_result',
            'is_correct': result.get('is_correct', False),
            'ducky_coins_awarded': result.get('ducky_coins_awarded', 0),
            'total_score': result.get('total_score', 0),
            'streak': result.get('streak', 0),
            'already_answered': result.get('already_answered', False),
            'error': result.get('error')
        }))

        # Notificar al anfitrión y sala que se ha registrado una respuesta nueva
        if not result.get('already_answered') and not result.get('error'):
            live_data = await self.get_live_ranking_db(self.code)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'broadcast_payload',
                    'payload': {
                        'event': 'player_answered_update',
                        'ranking': live_data.get('ranking', []),
                        'answered_count': live_data.get('answered_count', 0),
                        'total_players': live_data.get('total_players', 0)
                    }
                }
            )

    @database_sync_to_async
    def process_answer_db(self, user, code, question_id, selected_answer_id):
        game = Game.objects.filter(code=code).first()
        if not game or game.status != Game.Status.RUNNING:
            return {'error': 'Partida no disponible'}

        with transaction.atomic():
            player_entry = GamePlayer.objects.select_for_update().filter(game=game, player=user).first()
            if not player_entry:
                return {'error': 'Jugador no registrado'}

            question = Question.objects.filter(pk=question_id, quiz=game.quiz).first()
            selected_answer = Answer.objects.filter(pk=selected_answer_id, question=question).first()

            if not question or not selected_answer:
                return {'error': 'Pregunta o alternativa inválida'}

            if PlayerAnswer.objects.filter(game_player=player_entry, question=question).exists():
                return {'already_answered': True}

            # Cálculo de tiempo en backend contra el inicio de la pregunta (Anti-cheat)
            now = timezone.now()
            start = game.question_started_at or game.started_at or now
            server_time_taken = max(0.1, (now - start).total_seconds())
            time_limit = float(question.time_limit)

            is_correct = selected_answer.is_correct
            ducky_coins_awarded = 0

            # Solo asigna puntos si es correcta y respondió dentro del límite
            if is_correct and server_time_taken <= (time_limit + 1.5):
                player_entry.current_streak += 1
                player_entry.correct_answers += 1
                puntos_base = float(question.points)
                factor_tiempo = max(0.5, 1.0 - (server_time_taken / time_limit)) if time_limit > 0 else 0.5
                bono_racha = min(500, max(0, (player_entry.current_streak - 1) * 100))
                ducky_coins_awarded = int((puntos_base * factor_tiempo) + bono_racha)
                player_entry.score += ducky_coins_awarded
            else:
                player_entry.current_streak = 0

            player_entry.save(update_fields=['score', 'correct_answers', 'current_streak'])

            PlayerAnswer.objects.create(
                game_player=player_entry,
                question=question,
                selected_answer=selected_answer,
                is_correct=is_correct,
                points_awarded=ducky_coins_awarded,
                answered_at=now
            )

            return {
                'is_correct': is_correct,
                'ducky_coins_awarded': ducky_coins_awarded,
                'total_score': player_entry.score,
                'streak': player_entry.current_streak,
            }

    async def handle_update_avatar(self, data):
        """Actualiza el avatar del jugador y lo transmite a toda la sala en tiempo real."""
        if not (self.user and self.user.is_authenticated):
            return

        body = data.get('body', 'body_yellow')
        clothes = data.get('clothes', '')
        head = data.get('head', '')
        face = data.get('face', 'face_calm')

        res = await self.update_avatar_db(self.code, self.user, body, clothes, head, face)
        if res.get('success'):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'broadcast_payload',
                    'payload': {
                        'event': 'player_avatar_updated',
                        'player_id': res.get('player_id'),
                        'username': self.user.username,
                        'avatar': res.get('avatar')
                    }
                }
            )

    @database_sync_to_async
    def update_avatar_db(self, code, user, body, clothes, head, face):
        game = Game.objects.filter(code=code).first()
        if not game:
            return {'success': False, 'error': 'Partida no encontrada'}

        with transaction.atomic():
            player_entry = GamePlayer.objects.select_for_update().filter(game=game, player=user).first()
            if not player_entry:
                return {'success': False, 'error': 'Jugador no registrado en la sala'}

            player_entry.avatar_body = body
            player_entry.avatar_clothes = clothes
            player_entry.avatar_head = head
            player_entry.avatar_face = face
            player_entry.save(update_fields=['avatar_body', 'avatar_clothes', 'avatar_head', 'avatar_face'])

            return {
                'success': True,
                'player_id': player_entry.id,
                'avatar': player_entry.avatar_dict
            }

    @database_sync_to_async
    def get_live_ranking_db(self, code):
        game = Game.objects.filter(code=code).first()
        if not game:
            return {'ranking': [], 'answered_count': 0, 'total_players': 0}

        ranking_qs = game.players.select_related('player').order_by('-score', '-correct_answers', 'joined_at')
        ranking_list = [
            {
                'player_id': p.id,
                'username': p.player.username,
                'score': p.score,
                'streak': p.current_streak,
                'avatar': p.avatar_dict
            }
            for p in ranking_qs
        ]

        questions = list(game.quiz.questions.order_by('order'))
        current_idx = game.current_question - 1
        answered_count = 0
        if 0 <= current_idx < len(questions):
            answered_count = PlayerAnswer.objects.filter(
                game_player__game=game,
                question=questions[current_idx]
            ).count()

        return {
            'ranking': ranking_list,
            'answered_count': answered_count,
            'total_players': len(ranking_list)
        }

    async def handle_host_next_question(self):
        """Avanza la pregunta y notifica a todos los clientes suscritos."""
        if not (self.user and self.user.is_authenticated):
            return

        advance_data = await self.advance_question_db(self.code, self.user)
        if advance_data.get('success'):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'broadcast_payload',
                    'payload': advance_data
                }
            )

    @database_sync_to_async
    def advance_question_db(self, code, user):
        game = Game.objects.filter(code=code).first()
        if not game or game.host != user:
            return {'success': False, 'error': 'No autorizado'}

        total_questions = game.quiz.questions.count()
        with transaction.atomic():
            if game.current_question < total_questions:
                game.current_question += 1
                game.question_started_at = timezone.now()
                game.save(update_fields=['current_question', 'question_started_at'])
                return {
                    'success': True,
                    'event': 'next_question',
                    'current_question': game.current_question,
                    'total_questions': total_questions
                }
            else:
                game.status = Game.Status.FINISHED
                game.finished_at = timezone.now()
                game.save(update_fields=['status', 'finished_at'])
                return {
                    'success': True,
                    'event': 'game_finished',
                    'leaderboard_url': f"/games/leaderboard/{game.code}/"
                }

    async def handle_host_start_game(self):
        """Inicia la partida desde el Lobby vía WebSocket."""
        if not (self.user and self.user.is_authenticated):
            return

        start_data = await self.start_game_db(self.code, self.user)
        if start_data.get('success'):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'broadcast_payload',
                    'payload': start_data
                }
            )

    @database_sync_to_async
    def start_game_db(self, code, user):
        game = Game.objects.filter(code=code).first()
        if not game or game.host != user:
            return {'success': False, 'error': 'No autorizado'}

        if game.status == Game.Status.LOBBY:
            with transaction.atomic():
                now = timezone.now()
                game.status = Game.Status.RUNNING
                game.started_at = now
                game.question_started_at = now
                game.current_question = 1
                game.save(update_fields=['status', 'started_at', 'question_started_at', 'current_question'])
            return {
                'success': True,
                'event': 'game_started',
                'current_question': 1
            }
        return {'success': False, 'error': 'Estado no válido'}

    async def broadcast_payload(self, event):
        await self.send(text_data=json.dumps(event['payload']))
