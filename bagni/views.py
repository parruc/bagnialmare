# -*- coding: utf-8 -*-
from django.core import paginator
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.gis.geos import Point
from django.utils.translation import ugettext as _

from geopy import geocoders

from models import Bagno, Service, District, Municipality, ServiceCategory
from forms import BagnoForm
from search import search

import logging
logging.basicConfig()
logger = logging.getLogger("bagni.console")

class BagniView(ListView):
    """ View for a list of bagni
    """
    model = Bagno

    def get_context_data(self, **kwargs):
        context = super(BagniView, self).get_context_data(**kwargs)
        return context


class BagnoView(DetailView):
    """ Detail view for a single bagno
    """
    model = Bagno
    queryset = Bagno.objects.prefetch_related("services", "services__category")

    def get_context_data(self, **kwargs):
        context = super(BagnoView, self).get_context_data(**kwargs)
        return context

class BagnoEdit(UpdateView):
    """ Edit a single bagno
    """
    model = Bagno
    template_name = "bagni/bagno_edit.html"

    def get_context_data(self, **kwargs):
        context = super(BagnoEdit, self).get_context_data(**kwargs)
        context['form'] = BagnoForm(instance=self.object)
        return context

    def dispatch(self, request, *args, **kwargs):
        """Controllo che il manager possa modificare il bagno
        """
        obj = self.model.objects.get(**kwargs)
        is_staff = request.user.is_staff
        try:
            manager = request.user.manager
            can_edit = manager.can_edit(obj)
        except ObjectDoesNotExist:
            can_edit = False
        if is_staff or can_edit:
            return super(BagnoEdit, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied



class ServiceCategoryView(DetailView):
    """ Detail view for a single service category
    """
    model = ServiceCategory
    queryset = ServiceCategory.objects.prefetch_related("services", "services__bagni")

    def get_context_data(self, **kwargs):
        context = super(ServiceCategoryView, self).get_context_data(**kwargs)
        return context


class ServiceCategoriesView(ListView):
    """ List view for a the service categories
    """
    model = ServiceCategory

    def get_context_data(self, **kwargs):
        context = super(ServiceCategoriesView, self).get_context_data(**kwargs)
        return context

class ServiceView(DetailView):
    """ Detail view for a single service
    """
    model = Service
    queryset = Service.objects.prefetch_related("bagni", "category")

    def get_context_data(self, **kwargs):
        context = super(ServiceView, self).get_context_data(**kwargs)
        return context


class ServicesView(ListView):
    """ List view for a the services
    """
    model = Service

    def get_context_data(self, **kwargs):
        context = super(ServicesView, self).get_context_data(**kwargs)
        return context


class MunicipalityView(DetailView):
    """ Detail view for a single municipality
    """
    model = Municipality

    def get_context_data(self, **kwargs):
        context = super(MunicipalityView, self).get_context_data(**kwargs)
        return context


class MunicipalitiesView(ListView):
    """ List view for the municipalities
    """
    model = Municipality

    def get_context_data(self, **kwargs):
        context = super(MunicipalitiesView, self).get_context_data(**kwargs)
        return context


class DistrictView(DetailView):
    """ Detail view for a single district
    """
    model = District

    def get_context_data(self, **kwargs):
        context = super(DistrictView, self).get_context_data(**kwargs)
        return context


class DistrictsView(ListView):
    """ Detail view for a single district
    """
    model = District

    def get_context_data(self, **kwargs):
        context = super(DistrictsView, self).get_context_data(**kwargs)
        return context


class HomepageView(TemplateView):
    """ Homepage view with search form that points to the SearchView
    """

    template_name = "bagni/homepage.html"

    def get_context_data(self, **kwargs):
        pass


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
        loc = self.request.GET.get('l', "")
        place = point = None
        if loc:
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

## VISTE TEMPORANEE
# Non servono più?!?
#class GlobalMapView(ListView):
#    template_name = "bagni/globalmap.html"
#    model = Bagno
#    def get_context_data(self, **kwargs):
#        context = super(GlobalMapView, self).get_context_data(**kwargs)
#        return context
#
#class BenveView(ListView):
#    """ Simple view for Service listing everyone with his bagni
#        TODO: Will soon be removed
#    """
#    template_name = "bagni/benve.html"
#    queryset = Service.objects.all().prefetch_related("bagni", "bagni__municipality", "category")
#    def get_context_data(self, **kwargs):
#        context = super(BenveView, self).get_context_data(**kwargs)
#        return context


#class Benve2View(ListView):
#    """ Simple view for Service listing everyone with his bagni
#        TODO: Will soon be removed
#    """
#    template_name = "bagni/benve2.html"
#    queryset = Bagno.objects.filter(mail="")
#
#    def get_context_data(self, **kwargs):
#        context = super(Benve2View, self).get_context_data(**kwargs)
#        return context
#
