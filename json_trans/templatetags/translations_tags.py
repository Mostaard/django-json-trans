from django import template

from ..models import get_translated_value

register = template.Library()


@register.simple_tag(takes_context=True)
def get_translation(context, multilingual):
    return get_translated_value(multilingual, context.request.LANGUAGE_CODE)
