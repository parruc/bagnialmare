# -*- coding: utf-8 -*-
from geopy import geocoders

from django.core import paginator
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.gis.geos import Point
from django.utils.translation import ugettext as _

from ..models import Bagno
from ..search import search
from ..constants import MY_POSITION

import logging
logging.basicConfig()
logger = logging.getLogger("bagni.console")


class SearchView(TemplateView):
    """ Search view, which accepts search queries via url, like google.
        accepts 2 params:
        * q is the full text query
        * f is the list of active filters narrowing the search
    """

    template_name = "bagni/search.html"

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        groups = ['services', 'languages']
        q = self.request.GET.get('q', "")
        page = self.request.GET.get('p', "1")
        per_page = int(self.request.GET.get('pp', "10"))
        loc = self.request.GET.get('l', '')
        coords = self.request.GET.get('pos', "")
        place = point = None
        if loc == MY_POSITION and "," in coords:
            lat,lng = coords.split(",")
            point = Point(float(lng), float(lat))
        elif loc:
            g = geocoders.GoogleV3(domain='maps.google.it')
            try:
                matches = g.geocode(loc, exactly_one=False)
                place, (lat, lng) = matches[0]
                point = Point(lng, lat)
            except geocoders.googlev3.GeocoderQueryError as e:
                messages.add_message(self.request, messages.INFO,
                                     _("Cant find place '%s', sorting by relevance" % loc))
                logger.warning("cant find %s, error %s" % (loc, e))
            except geocoders.googlev3.GeocoderQuotaExceeded as e:
                logger.warning("abbiamo sforato il numero massimo di richieste a google per il geocoding")
                #TODO: falback to another backend
            except Exception as e:
                messages.add_message(self.request, messages.ERROR,
                                     _("Error in geocoding"))
                #logger.error would point to a 500 page
                logger.warning("geocoding %s gave error %s" % (loc, e))

        filters = self.request.GET.getlist('f', [])
        new_query_string = self.request.GET.copy()
        query = q or "*"
        raw_hits, facets, active_facets = search(
            q=query, filters=filters, groups=groups,
            query_string=new_query_string,)
        hits = Bagno.objects.prefetch_related("services", "services__category", ).filter(id__in=[h['id'] for h in raw_hits])
        if point:
            hits = hits.distance(point).order_by('distance')
        hits_paginator = paginator.Paginator(hits, per_page)
        try:
            hits = hits_paginator.page(page)
        except paginator.PageNotAnInteger:
            # If page is not an integer, deliver first page.
            hits = hits_paginator.page(1)
        except paginator.EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            hits = hits_paginator.page(hits_paginator.num_pages)
        has_get = self.request.method == 'GET'
        context.update({'q': q, 'l':loc, 'place': place, 'facets': facets, 'active_facets': active_facets,
                        'hits': hits, 'count': len(raw_hits), 'has_get': has_get })

        return context
