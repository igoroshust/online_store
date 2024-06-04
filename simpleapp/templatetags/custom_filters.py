from django import template

register = template.Library()

CURRENCIES_SYMBOLS = {
    'rub': '₽',
    'usd': '$',
}

BAD_WORDS = [
    'test',
    'testing',
]

@register.filter
def censor(value):
    """Замена астерисками символов в слове (кроме первого и последнего)"""
    words = value.split()
    result = []
    for word in words:
        if word in BAD_WORDS:
            result.append(word[0] + "*" * (len(word) - 2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)

@register.filter
def currency(value, code='rub'):
    """
    value: значение, к которому нужно применить фильтр
    """
    postfix = CURRENCIES_SYMBOLS[code]

    return f'{value}{postfix}'

@register.filter
def pow(value, pow):
    """Возведение числа в степень (для проверки кешировния под нагрузкой вычислений)"""
    return value**pow