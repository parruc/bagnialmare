# -*- coding: utf-8 -*-
import json

from django import http
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from django.contrib.gis import geos

from ..models import Service, District, Municipality, Neighbourhood, Bagno
from ..constants import MY_POSITION

import logging
logging.basicConfig()
logger = logging.getLogger("bagni.console")

class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)

class JsonSearchBoundingBox(JSONResponseMixin, BaseListView):
    """ Json list of bagni within given coordinates for dynamic map update
    """
    def get_queryset(self):
        bbox = geos.Polygon.from_bbox((self.kwargs['x1'],
                                       self.kwargs['y1'],
                                       self.kwargs['x2'],
                                       self.kwargs['y2'],))
        return Bagno.objects.filter(point__within=bbox)

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', self.object_list)
        return dict(items=[(b.name, b.address, b.get_absolute_url(), ) for b in queryset])


class JsonBagniInNeighbourhood(JSONResponseMixin, BaseListView):
    """Json dict of the beach resort in a newighbourhood
    """
    def get_queryset(self):
        neighbourhood_id = int(self.kwargs['id'])
        queryset = Neighbourhood.objects.get(pk=neighbourhood_id).bagni.all().order_by("name")
        return queryset

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', self.object_list)
        return dict(items=[(b.pk, b.get_complete_name()) for b in queryset if not b.is_managed()])


class JsonAutocompletePlaces(JSONResponseMixin, BaseDetailView):
    """ Json list of places for the autocomplete in search field
    """
    def get(self, request, *args, **kwargs):
        results = []
        query = self.request.GET.get('query', "")
        results = list(Neighbourhood.objects.filter(name__icontains=query))
        results += list(Municipality.objects.filter(name__icontains=query))
        results += list(District.objects.filter(name__icontains=query))
        names = list(set([r.name for r in results]))
        names.sort()
        names.insert(0, MY_POSITION)
        context = {'success':names}
        return self.render_to_response(context)

class JsonAutocompleteSearchterms(JSONResponseMixin, BaseDetailView):
    """ Json list of search terms for the autocomplete in search field
    """

    def get(self, request, *args, **kwargs):
        results = []
        query = self.request.GET.get('query', "")
        results = list(Service.objects.filter(name__icontains=query))
        names = list(set([r.name for r in results]))
        names.sort()
        context = {'success':names}
        return self.render_to_response(context)
