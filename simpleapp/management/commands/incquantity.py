from django.core.management.base import BaseCommand, CommandError
from simpleapp.models import Product

class Command(BaseCommand):
    help = 'Увеличивает количество товаров' # поле вывода подсказки команды
    missing_args_message = 'Недостаточно аргументов'
    requires_migrations_checks = True # напоминание о миграциях

    def handle(self, *args, **kwargs):
        """Выполнение тела функции при запуске команды incquantity"""
        for product in Product.objects.all():
            product.quantity += 1
            product.save()

            self.stdout.write(self.style.SUCCESS('Successfully updated product "%s"' % str(product.quantity))) #


