# -*- coding: utf-8 -*-
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from ..models import District, Municipality, Neighbourhood

import logging
logging.basicConfig()
logger = logging.getLogger("bagni.console")

class NeighbourhoodView(DetailView):
    """ Detail view for a single neighbourhood
    """
    model = Neighbourhood

    def get_context_data(self, **kwargs):
        context = super(NeighbourhoodView, self).get_context_data(**kwargs)
        return context


class NeighbourhoodsView(ListView):
    """ List view for the neighbourhoods
    """
    model = Neighbourhood

    def get_context_data(self, **kwargs):
        context = super(NeighbourhoodsView, self).get_context_data(**kwargs)
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
