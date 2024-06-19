from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Category
from django.utils.translation import gettext_lazy as _

class ProductForm(forms.ModelForm):
    pass
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'category',
            'price',
            'quantity',
        ]

        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'category': _('Category'),
            'price': _('Price'),
            'quantity': _('Quantity'),
        }


        # fields = '__all__' # all означает, что Джанго сам должен пойти в модель и взять все поля, кроме pk

    def clean(self):
        """Второй способ валидации данных, если есть возможность указать min_length, то лучше пользоваться им"""
        cleaned_data = super().clean() # вызываем метод .clean() из родительского класса и сохраняем данные формы в cleaned_data
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")

        if name == description:
            raise ValidationError(
                "Описание не должно быть идентичным названию."
            )

        return cleaned_data

    # def clean_name(self):
    #     """Третий способ - с помощью функции проверяем данные конкретного поля. Если требуется сложная проверка."""
    #     name = self.cleaned_data["name"]
    #     if name[0].islower():
    #         raise ValidationError(
    #             "Название должно начинаться с заглавной буквы."
    #         )
    #     return name

    # def clean(self):
    #     """Первый способ валидации данных - для проверки нескольких полей одновременно"""
    #     cleaned_data = super().clean()  # вызываем метод .clean() из родительского класса и сохраняем данные формы в cleaned_data
    #     description = cleaned_data.get("description")  # получаем description и проверяем его значение
    #     if description is not None and len(description) < 20:  # если значение не проходит по длине
    #         raise ValidationError({
    #             "description": "Описание не может быть менее 20 символов"
    #         })
    #
    #     name = cleaned_data.get("name")
    #     if name == description:
    #         raise ValidationError(
    #             "Описание не должно быть идентичным названию"
    #         )
    #
    #     return cleaned_data  # если проверка прошла успешно, возвращаем из функции проверенные данные формы.



