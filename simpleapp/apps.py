from django.apps import AppConfig

class SimpleappConfig(AppConfig):
    """Настройки приложения simpleapp"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simpleapp'

    def ready(self):
        """Импортирование сигналов с целью зарегистрировать их \
        выполнение при завершении конфигурации приложения simpleapp"""
        from . import signals # выполнение модуля -> регистрация сигналов
