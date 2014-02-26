from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

@register.filter
def batch(thelist, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(thelist), n):
        yield thelist[i:i+n]
