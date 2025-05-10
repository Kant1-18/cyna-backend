from django import template

register = template.Library()


@register.filter
def div100(value):
    try:
        return f"{value / 100:.2f}"
    except (ValueError, TypeError):
        return "0.00"
