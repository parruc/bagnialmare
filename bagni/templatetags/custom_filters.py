from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def batch(thelist, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in range(0, len(thelist), n):
        yield thelist[i:i+n]


@register.filter
def pretty_neighbourhood(neighbourhood):
    """ Return 'Neighborhood, Municipality' if they are different,
    otherwise just 'Municipality'
    """
    neighbourhood_name = neighbourhood.name
    municipality_name = neighbourhood.municipality.name
    if neighbourhood_name.lower() != municipality_name.lower():
        return neighbourhood_name + ', ' + municipality_name
    return municipality_name

@register.filter
def neighbourhood_municipality(bagno):
    """ Return 'Neighborhood, Municipality' of the bagno if they are different,
    otherwise just 'Municipality'
    """
    neighbourhood_name = bagno.neighbourhood.name
    municipality_name = bagno.neighbourhood.municipality.name
    if neighbourhood_name.lower() != municipality_name.lower():
        return neighbourhood_name + ', ' + municipality_name
    return municipality_name


@register.filter
def href_url(website_str):
    """ Returns website_str prefixed with http:// if is not already there. 
    """
    if not website_str.startswith('http://'):
        website_str = 'http://' + website_str 
    return website_str


@register.filter
def non_href_url(website_str):
    """ Returns website_str without http:// if it is there. 
    """
    if website_str.startswith('http://'):
        website_str = website_str.replace('http://', '') 
    return website_str

