from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Core'

    def data(self):
        from .models import Perfil
        if not Perfil.objects.exists():
            Perfil.objects.create(nome='Administrador', email='admin@braga.com', is_staff=True)