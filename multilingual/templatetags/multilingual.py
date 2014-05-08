from django.core.urlresolvers import resolve, reverse
from django.utils.translation import activate, get_language
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, *args, **kwargs):
    """
    Get active page's url by a specified language
    Usage: {% change_lang 'en' %}
    TODO: To move inside multilingual app
    """

    path = context['request'].path
    obj = None
    if "object" in context:
        obj = context.get("object")

    url_parts = resolve( path )

    url = path
    cur_language = get_language()
    try:
        activate(lang)
        if "slug" in url_parts.kwargs and obj:
            url_parts.kwargs['slug'] = obj.slug
        url = reverse( url_parts.view_name, kwargs=url_parts.kwargs )
    finally:
        activate(cur_language)

    return "%s" % url