from datetime import datetime

from django import template

register = template.Library()

@register.simple_tag()
def current_time(format_string='%b %d %Y'):
   return datetime.now().strftime(format_string)

"""Создаём тег, который будет брать текущие параметры запроса  и по указанному аргументу производить замену (фильтрация+пагинация)"""
@register.simple_tag(takes_context=True) # сообщаем Django, что для работы тега требуется передать context
def url_replace(context, **kwargs):
   d = context['request'].GET.copy() # копируем все параметры текущего запроса
   for k, v in kwargs.items(): # по указанным полям
      d[k] = v # устанавливаем новые значения, которые нам передали при использовании тега
   return d.urlencode() # кодируем параметры в формат, который может быть указан в строке браузера.