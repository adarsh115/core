from website import models
from django import template
from accounting import models

register = template.Library()

@register.filter
def subtract(number, other):
    return number - other

@register.filter
def currency(price, currency):
    default = models.WebSettings.objects.first().default_currency.symbol
    if currency == default:
        return "%.2f" % price

    from_ = models.Currency.objects.get(symbol=default)
    to = models.Currency.objects.get(symbol=currency)
    qs = models.ExchangeRate.objects.filter(from_currency=from_, to_currency=to).order_by('date')
    if qs.exists():
        exchange = qs.first()
        return "%.2f" % (price * exchange.rate)

    return "%.2f" % 0

