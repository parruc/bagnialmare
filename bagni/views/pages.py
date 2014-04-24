from django.views.generic import TemplateView
from ..models.services import ServiceCategory

import logging
logging.basicConfig()
logger = logging.getLogger("bagni.console")


class HomepageView(TemplateView):
    """ Homepage view with search form that points to the SearchView
    """

    template_name = "bagni/homepage.html"

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context.update({'facility_categories': ServiceCategory.objects.all().order_by('order')})
        return context


class AboutUsView(TemplateView):
    """ About us view with a description ot 4hm
    """

    template_name = "bagni/about-us.html"

    def get_context_data(self, **kwargs):
        context = super(AboutUsView, self).get_context_data(**kwargs)
        return context
