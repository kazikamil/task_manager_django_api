from django.apps import AppConfig

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rest'
    
    # 1. 👇 Add this line for signals
    def ready(self):
        import rest.signals