from django.views.generic import TemplateView
from ..models.services import ServiceCategory

import logging
logging.basicConfig()
logger = logging.getLogger("bagni.console")


class HomepageView(TemplateView):
    """ Homepage view with search form that points to the SearchView
    """

    template_name = "bagni/homepage.html"
    queryset = ServiceCategory.objects.prefetch_related("services")

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context.update({'facility_categories': self.queryset.all().order_by('order')})
        return context


class AboutUsView(TemplateView):
    """ About us view with a description ot 4hm
    """

    template_name = "bagni/about-us.html"

    def get_context_data(self, **kwargs):
        context = super(AboutUsView, self).get_context_data(**kwargs)
        return context

class UserTermsAndPrivacyView(TemplateView):
    """ Terms and privacy page for user who visit the website
    """

    template_name = "bagni/user-terms-and-privacy.html"

    def get_context_data(self, **kwargs):
        context = super(UserTermsAndPrivacyView, self).get_context_data(**kwargs)
        return context

class ManagerPrivacyView(TemplateView):
    """ Privacy page for managers who sign up in the site
    """

    template_name = "bagni/manager-privacy.html"

    def get_context_data(self, **kwargs):
        context = super(ManagerPrivacyView, self).get_context_data(**kwargs)
        return context

class ManagerTermsView(TemplateView):
    """ Terms page for managers who sign up in the site
    """

    template_name = "bagni/manager-terms.html"

    def get_context_data(self, **kwargs):
        context = super(ManagerTermsView, self).get_context_data(**kwargs)
        return context
