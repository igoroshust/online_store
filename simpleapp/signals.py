"""Код обработчика сигнала для отправки сообщуний все пользователям, подписавшимся на обновления в этой категории"""

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product

@receiver(post_save, sender=Product) # sender=модель класса
def product_created(instance, created, **kwargs): # instance - сохраняем фактический экземпляр
    """Создание товара"""
    if not created:
        return

    emails = User.objects.filter(
        subscriptions__category=instance.category
    ).values_list('email', flat=True) # flat=True - результат по одному полю

    subject = f'Новый товар в категории {instance.category}'

    text_content = ( # текстовое сообщение
        f'Товар: {instance.name} <br>'
        f'Цена: {instance.price} <br><br>'
        f'Ссылка на товар: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )

    html_content = ( # html-сообщение
        f'Товар: {instance.name} <br>'
        f'Цена: {instance.price} <br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на товар</a>'
    )

    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()