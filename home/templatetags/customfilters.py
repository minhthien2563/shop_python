from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
     return value * arg

@register.filter
def calPercent(value, arg):
     return value * arg/100

@register.filter
def sub(value, arg):
     return value-arg

@register.filter
def custom_range(value, arg):
     return range(arg+1, value)

@register.filter
def division(value, arg):
     return value/arg
