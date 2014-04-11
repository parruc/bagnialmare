from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import TemplateView

from ..models import Service, ServiceCategory

import logging
logging.basicConfig()
logger = logging.getLogger("bagni.console")


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
    """ Shows the list of bagni offering the service
    """
    model = Service
    queryset = Service.objects.prefetch_related("bagni__neighbourhood", "bagni__neighbourhood__municipality")

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
