from modeltranslation.admin import TranslationAdmin # импорт модели админки
from django.contrib import admin
from .models import Category, Product, Material
from .templatetags import *

class CategoryAdmin(TranslationAdmin):
    model = Category

class ProductsAdmin(TranslationAdmin):
    model = Product

def nullfy_quantity(modeladmin, request, queryset):
    """Обнуление товара на складе"""
    # request - хранит информацию о запросе,
    # queryset - набор выделенных галочкой объектов

    queryset.update(quantity=0)
nullfy_quantity.short_description = 'Обнулить товары' # описание для более понятного представления в админ-панеле задаётся в виде объекта

class ProductAdmin(admin.ModelAdmin):
    # list_display - это список или кортеж со всеми полями, которые будут отображены в таблице с товарами
    list_display = ('name', 'description', 'quantity', 'price', 'on_stock',) # генерация списка имён всех полей для удобочитаемого отображения

    # list_filter - добавление фильтров в админку
    list_filter = ('price', 'quantity', 'name',)

    # search_fields - добавление поисковой строчки по фильтрам (вместо дефолтной таблицы)
    search_fields = ('name', 'category__name')

    # actions - добавляет действия в список
    actions = [nullfy_quantity]


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Material)

