from django.core.management.base import BaseCommand, CommandError
from simpleapp.models import Product

class Command(BaseCommand):
    help = 'Удаление всех товаров'
    requires_migrations_checks = True # напоминание о миграциях

    def handle(self, *args, **options):
        """Выполнение кода при запуске программы"""
        self.stdout.readable()
        self.stdout.write('Вы действительно хотите удалить все продукты? \t yes/no')
        answer = input() # считываем подтверждение

        if answer == 'yes':
            Product.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('>>> Продукты успешно удалены!'))
            return

        self.stdout.write(self.style.ERROR('>>> Отказано в доступе!'))