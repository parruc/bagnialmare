from django.urls import reverse, resolve
from django.utils.translation import activate, get_language
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, *args, **kwargs):
    """
    Get active page's url by a specified language
    Usage: {% change_lang 'en' %}
    """

    path = context['request'].path

    url_parts = resolve( path )

    url = path
    cur_language = get_language()
    try:
        activate(lang)
        for key in url_parts.kwargs.keys():
            if key.endswith("slug"):
                key_parts = key.split("_")
                key_name = "object"
                obj = None
                if len(key_parts) > 1:
                    key_name = key_parts[0]
                if key_name in context:
                    obj = context.get(key_name)
                    url_parts.kwargs[key] = obj.slug
        url = reverse( url_parts.view_name, kwargs=url_parts.kwargs )
    finally:
        activate(cur_language)

    return "%s" % url
