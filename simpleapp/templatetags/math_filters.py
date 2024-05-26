from django import template

register = template.Library()

@register.filter()
def power(value, item1):
    """Возведение числа в степень (для проверки кешировния под нагрузкой вычислений)"""
    return value ** item1