from django import template
import locale

register = template.Library()

@register.filter(name='currency')
def currency(value):
    if value is None:
        return "R$ 0,00"
    try:
        # Tenta formatar como moeda brasileira manualmente para evitar problemas de locale do sistema
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return f"R$ {value}"
