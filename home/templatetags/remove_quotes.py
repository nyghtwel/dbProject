from django import template


register = template.Library()

@register.filter
def remove_quotes(str):
	return str.replace('"', '')