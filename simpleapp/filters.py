import django_filters
from django_filters import FilterSet, ModelChoiceFilter
from .models import Product, Material

class ProductFilter(FilterSet):
    material = ModelChoiceFilter(
        field_name='productmaterial__material',
        queryset=Material.objects.all(),
        label='Material',
        empty_label='любой', # значение по умолчанию
        # conjoined=False, # фильтрация по двум материалам сразу
    )

    class Meta:
        """В классе Мета указывается Django-модель, в которой фильтруются записи"""
        model = Product
        # В fields описываем поля модели, по которым будет производиться фильтрация (словарь настройки фильтров)
        # ключи - название полей модели, значения - списки операторов фильтрации (использ. при составлении запроса по типу Product.objeacts.filter(price__gt=10).
        fields = {
            'productmaterial__material': ['exact'],
            # полное сопоставление с моделью (не больше-меньше, а один в один).
            'name': ['icontains'], # поиск по названию
            'quantity': ['gt'], # количество товаров должно быть больше или равно
            'price': [
                'lt', # цена меньше либо равна указанной
                'gt', # цена больше либо равна указанной
            ],
        }


# фильтрация продукта по материалу: Product.objects.filter(productmaterial__material). -таблица__поле-