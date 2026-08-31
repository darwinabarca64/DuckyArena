"""Management command to load quizzes from JSON files."""
import json
import os
from django.core.management.base import BaseCommand
from quizz_app.models import Quiz


class Command(BaseCommand):
    help = 'Load quizzes from JSON files in the data directory'

    def handle(self, *args, **options):
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data')
        
        if not os.path.exists(data_dir):
            self.stdout.write(self.style.ERROR(f'Data directory not found: {data_dir}'))
            return

        json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
        
        if not json_files:
            self.stdout.write(self.style.WARNING('No JSON files found in data directory'))
            return

        for json_file in json_files:
            file_path = os.path.join(data_dir, json_file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    quizzes_data = json.load(f)
                
                # Handle both single quiz and list of quizzes
                if isinstance(quizzes_data, dict):
                    quizzes_data = [quizzes_data]
                
                for quiz_data in quizzes_data:
                    title = quiz_data.get('title', 'Sin título')
                    
                    # Delete existing quiz with same title
                    Quiz.objects.filter(title=title).delete()
                    
                    quiz = Quiz.objects.create(
                        title=title,
                        description=quiz_data.get('description', ''),
                        category=quiz_data.get('category', 'General'),
                        difficulty=quiz_data.get('difficulty', 'medio'),
                        questions_data=quiz_data.get('questions', [])
                    )
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Quiz "{title}" loaded successfully')
                    )
            except json.JSONDecodeError as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error decoding JSON in {json_file}: {str(e)}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error loading {json_file}: {str(e)}')
                )
