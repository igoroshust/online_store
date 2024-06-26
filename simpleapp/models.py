from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy # импортируем ленивый геттекст с подсказкой

class Material(models.Model):
    """Наименование материала"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'

class Product(models.Model):
    """Товар"""
    name = models.CharField(max_length=200, unique=True, verbose_name=_('Name')) # названия товаров не должны повторяться
    description = models.CharField(max_length=200, verbose_name=_('Description'))
    quantity = models.IntegerField(validators=[MinValueValidator(0, 'Quantity should be >= 0.0')], verbose_name=_('Quantity'))
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='products', verbose_name=_('Category')) # все продукты в категории будут доступны через поле products, поле категории будет ссылаться на модель категории
    # materials = models.ForeignKey(to='Material', on_delete=models.CASCADE)
    price = models.FloatField(validators=[MinValueValidator(0.0, 'Price should be >= 0.0')], verbose_name=_('Price'))
    is_activate = models.BooleanField(default=True)

    @property
    def on_stock(self):
        """Отображение наличия/отсутствия товара на складе"""
        return self.quantity > 0
    def get_absolute_url(self):
        """Отображение конкретной страницы после создания товара"""
        return reverse('product_detail', args=[str(self.id)]) # с помощью reverse указываем не путь типа /products/, а название пути

    def save(self, *args, **kwargs):
        """Сохранение объекта"""
        super().save(*args, **kwargs) # вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'product-{self.pk}') # удаляем его из кэша, чтобы сбросить его

    def __str__(self):
        """Строковое представление"""
        return f'{self.name.title()}: {self.description[:50]}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class ProductMaterial(models.Model):
    """Промежуточная таблица для связки Продукта и Материала - Состав продукта"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

class Category(models.Model):
    """Категория, к которой будет привязываться товар"""
    name = models.CharField(max_length=100, unique=True, help_text=_('category name'))

    def __str__(self):
        return self.name.title()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Subscription(models.Model):
    """Список категорий, на которые подписан пользователь"""
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name=pgettext_lazy('help text for Subscription model', 'This is the help text'),
    )
