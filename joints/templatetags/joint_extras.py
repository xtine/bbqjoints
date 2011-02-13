from django import template

register = template.Library()

def dashreplace(value, arg):
    return value.replace(arg, '-')
    
register.filter('dashreplace', dashreplace)