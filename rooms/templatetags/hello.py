from django import template

register = template.Library()


@register.filter
def hello(value):
    print(value)

    return "lalalala"
