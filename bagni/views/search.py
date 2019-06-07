# -*- coding: utf-8 -*-
from geopy import geocoders
from geopy.exc import GeocoderQueryError, GeocoderQuotaExceeded

from django.core import paginator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.utils.translation import ugettext as _

from ..models import Bagno, Service
from ..search import search

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
        groups = ['services', ]
        q = self.request.GET.get('q', "").strip()
        try:
            selected_facet = Service.objects.get(name__iexact=q)
            if selected_facet.hidden:
                selected_facet = None
        except ObjectDoesNotExist:
            selected_facet = None
        page = self.request.GET.get('p', "1")
        per_page = int(self.request.GET.get('pp', "15"))
        loc = self.request.GET.get('l', '')
        coords = self.request.GET.get('coords', "")
        place = point = None
        if loc == _("near_me") and "," in coords:
            lat,lng = coords.split(",")
            point = Point(float(lng), float(lat), srid=4326)
        elif loc:
            g = geocoders.OpenMapQuest(api_key="mT6OVf3XpNah5OAuxSJ7vzG3GjpYjs9V")
            try:
                matches = g.geocode(loc + ", Emilia Romagna", exactly_one=False)
                # TODO: if len(matches) > 1 prompt the user a choice between matches
                place, (lat, lng) = matches[0]
                point = Point(lng, lat, srid=4326)
            except GeocoderQueryError as e:
                messages.add_message(self.request, messages.INFO,
                                     _("Cant find place '%s', sorting by relevance" % loc))
                logger.warning("cant find %s, error %s" % (loc, e))
            except GeocoderQuotaExceeded as e:
                logger.warning("abbiamo sforato il numero massimo di richieste a google per il geocoding")
                #TODO: falback to another backend
            except Exception as e:
                messages.add_message(self.request, messages.ERROR,
                                     _("Cant find place '%s', sorting by relevance" % loc))
                #logger.error would point to a 500 page
                logger.warning("geocoding %s gave error %s" % (loc, e))

        new_query_string = self.request.GET.copy()
        filters = self.request.GET.getlist('f', [])
        if selected_facet:
            filter = "services:" + selected_facet.slug
            filters.append(filter)
            q = ""
            new_query_string['q'] = ""
            new_query_string.appendlist("f", filter)
        query = q or "*"
        raw_hits, facets, active_facets = search(
            q=query, filters=filters, groups=groups,
            query_string=new_query_string,)
        hits = Bagno.objects.prefetch_related("services", "services__category", "neighbourhood", "neighbourhood__municipality", "managers", "images").filter(id__in=[h['id'] for h in raw_hits]).exclude(slug="test")
        hits = hits.annotate(num_managers=Count("managers"), num_images=Count("images")).order_by("-num_managers", "-num_images", "name")
        if point:
            hits = hits.annotate(distance=Distance('point', point)).order_by('distance')
        hits_paginator = paginator.Paginator(hits, per_page)
        num_pages = hits_paginator.num_pages
        try:
            hits = hits_paginator.page(page)
        except paginator.PageNotAnInteger:
            # If page is not an integer, deliver first page.
            hits = hits_paginator.page(1)
        except paginator.EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            hits = hits_paginator.page(num_pages)
        search_results = {}
        search_results['num_pages'] = num_pages
        search_results['count'] = len(raw_hits)
        search_results['q'] = q
        search_results['l'] = loc
        search_results['coords'] = coords
        search_results['place'] = place
        search_results['point'] = point
        search_results['facets'] = facets
        search_results['filters'] = filters
        search_results['active_facets'] = active_facets
        search_results['has_get'] = self.request.method == 'GET'
        context.update({'search_results': search_results, 'hits': hits})

        return context
