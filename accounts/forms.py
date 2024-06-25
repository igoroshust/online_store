from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm # импорт класса формы
# from django.core.mail import send_mail # отправка писем
# from django.core.mail import EmailMultiAlternatives # отправка html-письма
from django.core.mail import mail_managers # рассылка для менеджеров
# from django.core.mail import mail_admins # рассылка для админов


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Электронная почта")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    password1 = forms.CharField(label="Пароль")
    username = forms.CharField(label="Логин")
    password2 = forms.CharField(label="Подтверждение пароля")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

class CustomSignupForm(SignupForm):
    """Добавление пользователя в группу"""
    def save(self, request):
        user = super().save(request) # вызываем метод у класса-родителя для выполнения проверок и сохраненя в модель User

        # mail_admins(
        #     subject='Новый пользователь!',
        #     message=f'Пользователь {user.username} зарегистрировался на сайте.'
        # )

        mail_managers(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте',
        )

        # subject = 'Добро пожаловать в наш интернет-магазин!'
        # text = f'{user.username}, вы успешно зарегистрировались на сайте!' # текстовая версия письма
        # html = ( # html-версия письма
        #     f'<b>{user.username}</b>, вы успешно зарегистрировались на '
        #     f'<a href="http://127.0.0.1:8000/products">сайте</a>!'
        # )
        # msg = EmailMultiAlternatives( # в иницииализоватор класса EmailMultiAlternatives передаём текстовую версию
        #     subject=subject, body=text, from_email=None, to=[user.email] # to - получатель
        # )
        # msg.attach_alternative(html, "text/html") # html-версию применяем как альтернативный вариант письма.
        # msg.send() # отправка составленного письма.


        # send_mail( # отправка письма указанному получателю
        #     subject='Добро пожаловать в наш интернет-магазин!', # тема письма
        #     message=f'{user.username}, вы успешно зарегистрировались!', # сообщение
        #     from_email=None, # отправитель (будет использовано значение DEFAULT_FROM_EMAIL)
        #     recipient_list=[user.email], # почта пользователя
        # )

        # common_users = Group.objects.get(name="common users") # получаем объект модели группы с названием common users
        # user.groups.add(common_users) # добавляем нового пользователя в эту группу

        return user # обязательным требованием метода save() является возвращение объекта модели User по итогу выполнения функции