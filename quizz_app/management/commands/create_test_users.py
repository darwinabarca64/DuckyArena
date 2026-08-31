"""Management command to create test users."""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from quizz_app.models import UserProfile


class Command(BaseCommand):
    help = 'Create test users for development'

    def handle(self, *args, **options):
        test_users = ['estudiante1', 'estudiante2']
        
        for username in test_users:
            user, created = User.objects.get_or_create(username=username)
            
            if created:
                user.set_password('123456')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Usuario creado: {username}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Usuario ya existe: {username}'))
            
            profile, profile_created = UserProfile.objects.get_or_create(user=user)
            
            if profile_created:
                self.stdout.write(self.style.SUCCESS('  → Perfil creado: estudiante'))
            else:
                self.stdout.write(self.style.WARNING(f'  → Perfil existente: {profile.role}'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Usuarios de prueba listos'))
        self.stdout.write('\n📝 Credenciales:')
        self.stdout.write('  Estudiante: estudiante1 / 123456')
