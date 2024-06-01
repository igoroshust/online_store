from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.cache import cache

class Material(models.Model):
    """Наименование материала"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Product(models.Model):
    """Товар"""
    name = models.CharField(max_length=200, unique=True, verbose_name='Название') # названия товаров не должны повторяться
    description = models.CharField(max_length=200, verbose_name='Описание')
    quantity = models.IntegerField(validators=[MinValueValidator(0, 'Quantity should be >= 0.0')], verbose_name='Количество')
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='products', verbose_name='Категория') # все продукты в категории будут доступны через поле products, поле категории будет ссылаться на модель категории
    # materials = models.ForeignKey(to='Material', on_delete=models.CASCADE)
    price = models.FloatField(validators=[MinValueValidator(0.0, 'Price should be >= 0.0')], verbose_name='Цена')

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

class ProductMaterial(models.Model):
    """Промежуточная таблица для связки Продукта и Материала - Состав продукта"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

class Category(models.Model):
    """Категория, к которой будет привязываться товар"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.title()

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
    )
