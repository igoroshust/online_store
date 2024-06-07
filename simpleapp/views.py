from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView
from .models import Product, Subscription, Category
from .forms import ProductForm
from .filters import ProductFilter # фильтрация списка товаров
from datetime import datetime
from pprint import pprint # вывод словаря в красивом виде
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin # проверка прав доступа
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache

from django.views.decorators.cache import cache_page # кэшируемая страничка

import logging
logger = logging.getLogger(__name__)

def index(request):
    logger.warning('Hi there!')
    return JsonResponse({'success': 'True'})

class ProductsList(ListView):
    model = Product # модель, объекты которой предполагается выводить
    ordering = 'name' # поле для сортировки объектов
    template_name = 'products.html' # шаблон с инструкциями о способах отображения пользователю всех объектов
    context_object_name = 'products' # список, в котором будут лежать все объекты
    paginate_by = 4 # количество записей на странице

    def get_queryset(self):
        """Функция получения списка товаров"""
        # получаем обычный запрос
        queryset = super().get_queryset()
        # используем класс фильтрации
        # self.request.GET содержит объект QueryDict
        # сохраняем фильтрацию в объекте класса, чтобы потом добавить в контекст и использовать в шаблоне
        self.filterset = ProductFilter(self.request.GET, queryset)
        # возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """Метод, позволяющий изменить набор данных, передаваемых в шаблон"""
        context = super().get_context_data(**kwargs) # с помощью super() мы обращаемся к родительским классам и ...
        # вызываем у них метод get_context_data с теми же аргументами, что и были переданы нам.
        # в ответе мы должны получить словарь
        context['filterset'] = self.filterset # добавляем в контекст объект фильтрации
        # context['time_now'] = datetime.utcnow() # к словарю добавляем текущую дату в ключ 'time_now'
        # context['next_sale'] = 'Распродажа в среду!' # пустая переменная для рассмотрения работы ещё одного фильтра.
        # pprint(context) # вывод словаря в красивом виде
        return context  # контекст - это словарь, который мы передаём в тэмлейт (в product и products).

class ProductDetail(DetailView):
    """Информация об одном товаре"""
    model = Product
    template_name = 'product.html' # не путать с products.html
    context_object_name = 'product' # название объекта, в котором будет выбранный пользователем продукт
    queryset = Product.objects.all()

    def get_object(self, *args, **kwargs): # переопределяем метод получения объекта
        obj = cache.get(f'product-{self.kwargs["pk"]}', None) # кэш забирает значение по ключу, а если его нет, то забирает None

        if not obj: # если объекта нет в кэше, то получаем его и записываем в кэш
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)
        return obj

class ProductCreate(PermissionRequiredMixin, CreateView): # LoginRequiredMixin
    """Представление для создания товаров"""
    permission_required = ('simpleapp.add_product')
    raise_exception = True # вывод ошибки (403) для пользователей
    form_class = ProductForm # указываем разработанную форму
    model = Product # модель товаров
    template_name = 'product_edit.html' # шаблон, в котором используется форма

class ProductUpdate(PermissionRequiredMixin, UpdateView):
    """Представление для изменения товара"""
    permission_required = ('simpleapp.change_product')
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'

class ProductDelete(PermissionRequiredMixin, DeleteView):
    """Представление для удаления товара"""
    permission_required = ('simpleapp.delete_product')
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list') # указываем шаблон, на который перенаправим пользователя после удаления товара.

def multiply(request):
    number = request.GET.get('number')
    multiplier = request.GET.get('multiplier')

    try:
        result = int(number) * int(multiplier)
        html = f"<html><body>{number}*{multiplier}={result}</body></html>"
    except (ValueError, TypeError):
        html = f"<html><body>Invalid input.</body></html>"

    return HttpResponse(html)

@login_required
def show_protected_page(request):
    pass

# def create_product(request):
#     """Создание продукта"""
#     form = ProductForm() # если пустую форму добавить изначально, то при ПОСТ-запросе после инициализации формы пользователю вернётся страница с информацией об ошибках.
#     if request.method == 'POST': # если пользователь отправил ПОСТ-запрос (информацию об этом получаем из .method)
#         form = ProductForm(request.POST) # создадим новую форму
#         if form.is_valid(): # проверяем корректность значений
#             form.save() # если форма валидна, сохраняем
#             return HttpResponseRedirect('/products') # возвращаем пользователя на главную страницу
#
#     return render(request, 'product_edit.html', {'form': form}) # отображение объекта на странице: принимает запрос пользователя, темплейт и контекст.


@login_required # только для зарегистрированных пользователей
@csrf_protect # автоматически проверяется CSRF-токен в получаемых формах
def subscriptions(request):
    """Подписки пользователя для рассылки писем"""
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )