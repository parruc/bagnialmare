# -*- coding: utf-8 -*-
from collections import OrderedDict

import bottlenose
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from contacts.views import ContactView
from contacts.forms import ContactForm
from booking.views import BookingModalView
import random
from django.conf import settings

from ..models import Bagno, ServiceCategory, District, Service, Neighbourhood
from ..forms import BagnoForm, TelephoneFormSet, ImageFormSet

import logging
logging.basicConfig()
logger = logging.getLogger("bagni.console")

AMAZON_KEYWORDS = [
    ["formine spiaggia", "piscinetta", "mulinello spiaggia"],
    ["borsa mare", "infradito", "pareo", "boxer mare"],
    ["ombrellone mare", "telo mare", "tenda spiaggia", "sdraio spiaggia"],
    ["bocce spiaggia", "palla mare", "racchettoni"],
    ["crema solare", "crema abbronzante", "doposole"],
    ["cavalcabile mare", "maschera mare", "canotto mare", "materassino"],
]

AMAZON_PRODUCTS = [
    ["B00YSU01ES", "B07CL45716", "B07BRVS8R2", "B01MU4RFF7", ],
    ["B07CSND5KQ", "B073P88SYS", "B007WPOB38", "B00M17LFWM", "B07N66ZND4", "B07PM26YXT", ],
    ["B06ZXXSHY8", "B073RL9JK1", "B07MT9QWPP", "B00URK01BQ", ],
    ["B00E7GP4EU", "B002VZGPG0", "B00D6C90NM", ],
    ["B00E4L4840", "B0009R14XQ", "B00B4TN436", "B00E4KZ2KK", ],
    ["B01MR054CS", "B079GRSZV9", "B005DUW6RM", "B000KHZ044", "B0006N01BO"],
]

class BagniByFacilityAndNeighbourhoodView(TemplateView):
    """ List of bagni in the neighbourhood offering the facility
    """

    template_name = "bagni/bagni-by-facility-and-neighbourhood.html"

    def get_context_data(self, **kwargs):
        context = super(BagniByFacilityAndNeighbourhoodView, self).get_context_data(**kwargs)
        facility_slug = str(self.kwargs['facility_slug'])
        neighbourhood_slug = str(self.kwargs['neighbourhood_slug'])
        neighbourhood = Neighbourhood.objects.filter(slug=neighbourhood_slug).first()
        facility = Service.objects.filter(slug=facility_slug).first()
        if not neighbourhood or not facility:
            raise Http404
        bagni_with_facility_in_neighbourhood = Bagno.objects.filter(neighbourhood__slug=neighbourhood_slug).filter(services__slug__contains=facility_slug)
        context.update({'neighbourhood': neighbourhood})
        context.update({'facility': facility})
        context.update({'bagni': bagni_with_facility_in_neighbourhood})
        #add facility name or obj?
        #add neighbourhood name or obj?
        return context


class BagniView(TemplateView):
    """ View for a list of bagni
    """

    template_name = "bagni/bagni.html"

    def get_context_data(self, **kwargs):
        context = super(BagniView, self).get_context_data(**kwargs)
        context.update({'districts': District.objects.all()})
        context.update({'facility_categories': ServiceCategory.objects.all().order_by('order')})
        return context


CITY_BOOKING_ID_BY_SLUG = {
    'cervia': '-115207',
    'tagliata': '-115207',
    'milano-marittima': '-121733',
    'pinarella': '-124859',
    'lido-di-classe': '93840',
    'lido-adriano': '93899',
    'marina-romea': '93927',
    'casal-borsetti': '-113712',
    'lido-di-savio': '-120155',
    'lido-di-dante': '93890',
    'punta-marina-terme': '-125914',
    'marina-di-ravenna': '-121120',
    'porto-corsini': '-125534',
    'zadina': '93612',
    'villamarina': '93567',
    'valverde': '93569',
    'cesenatico': '-115252',
    'gatteo-a-mare': '93565',
    'san-mauro-mare': '93561',
    'lido-di-spina': '94174',
    'lido-degli-estensi': '94180',
    'porto-garibaldi': '-125548',
    'lido-di-volano': '94217',
    'lido-di-pomposa': '94182',
    'lido-delle-nazioni': '94206',
    'lido-degli-scacchi': '94181',
    'marebello': '93673',
    'rivabella': '93664',
    'bellariva': '-126373',
    'torre-pedrera': '93655',
    'viserba': '1655',
    'viserbella': '93656',
    'miramare': '-126373',
    'rivazzurra': '-126373',
    'san-giuliano': '-126373',
    'rimini': '-126373',
    'misano-adriatico': '-121826',
    'riccione': '-126305',
    'igea-marina': '-119128',
    'cattolica': '-114819'
}


class BagnoView(DetailView):
    """ Detail view for a single bagno
    """
    model = Bagno
    queryset = Bagno.objects.prefetch_related("services", "services__category")

    @property
    def amazon_items(self):
        categories = AMAZON_PRODUCTS[:]
        for count in range(6):
            category = random.choice(categories)
            categories.remove(category)
            yield random.choice(category)
    

    def get_amazon_products(self):
        amazon = bottlenose.Amazon(
            settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_ASSOCIATE_TAG)
        response = amazon.ItemLookup(ItemId="B007OZNUCE")


    def get_context_data(self, **kwargs):
        context = super(BagnoView, self).get_context_data(**kwargs)
        context['can_edit'] = self.object.can_be_managed_by(self.request.user)
        services_by_category = OrderedDict()
        for s in self.object.services.order_by("category__order"):
            if s.category not in services_by_category:
                services_by_category[s.category] = []
            services_by_category[s.category].append(s)
        context['services_by_category'] = services_by_category
        neighbourhood_slug = self.object.neighbourhood.slug
        context['booking_city_id'] = CITY_BOOKING_ID_BY_SLUG[neighbourhood_slug]
        return context


# this one is cleaner then out custom made approach but does not
# handle well inline formset validation
#class BagnoUpdate(UpdateWithInlinesView):
#   model = Bagno
#   form_class = BagnoForm
#   inlines = [TelephoneInline, ImageInline]
#   template_name = "bagni/bagno_update.html"

#   def dispatch(self, request, *args, **kwargs):
#       is_staff = request.user.is_staff
#       try:
#           manager = request.user.manager
#           can_edit = manager.can_edit(self.object)
#       except (ObjectDoesNotExist, AttributeError):
#           can_edit = False
#       if is_staff or can_edit:
#           return super(BagnoUpdate, self).dispatch(request, *args, **kwargs)
#       raise PermissionDenied


#This one is our homemade form view with inlines, it also forwards inline formsets errors as messages
class BagnoEdit(UpdateView):
    """ Edit a single bagno
    """
    model = Bagno
    template_name = "bagni/bagno_edit.html"
    form_class = BagnoForm

    def dispatch(self, request, *args, **kwargs):
        """Controllo che il manager possa modificare il bagno
        """
        self.object = self.get_object()
        if self.object.can_be_managed_by(request.user):
            return super(BagnoEdit, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied

    def post(self, request, *args, **kwargs):
        # this is necessary when overriding post and get
        self.object = self.get_object()
        form = BagnoForm(data=request.POST)
        telephone_formset = TelephoneFormSet(request.POST,
                instance=self.object)
        image_formset = ImageFormSet(request.POST, request.FILES,
                instance=self.object)
        if not telephone_formset.is_valid() or not image_formset.is_valid() or not form.is_valid():
            for index, t_error in enumerate(telephone_formset.errors):
                for field, error_messages in t_error.items():
                    for error_message in error_messages:
                        _msg = "Telephone: %d field: %s error: %s" % (index, field, error_message)
                        messages.add_message(self.request, messages.ERROR, _msg)
                        logger.error(_msg)
            for index, i_error in enumerate(image_formset.errors):
                for field, error_messages in i_error.items():
                    for error_message in error_messages:
                        _msg = "Image: %d field: %s error: %s" % (index, field, error_message)
                        messages.add_message(self.request, messages.ERROR, _msg)
                        logger.error(_msg)
            return self.render_to_response(
                    self.get_context_data(
                        telephone_formset=telephone_formset,
                        image_formset=image_formset,
                        form=form,
                    )
                )
        else:
            # telephone_formset.save(commit=False)
            # image_formset.save(commit=False)
            telephone_formset.save()
            image_formset.save()
            return super(BagnoEdit, self).post(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(BagnoEdit, self).get_context_data(*args, **kwargs)
        context['telephone_formset'] = TelephoneFormSet(instance=self.object)
        context['image_formset'] = ImageFormSet(instance=self.object)
        return context


class BagnoBooking(BookingModalView):

    def form_valid(self, form):
        msg = _("Thank you for your booking request. We will let you know the\
                 result as soon as possible")
        messages.add_message(self.request, messages.INFO, msg)
        return super(BagnoBooking, self).form_valid(form)

    def get_bagno(self):
        if "slug" not in self.kwargs:
            raise Http404()
        return Bagno.objects.get(slug=self.kwargs['slug'])

    def get_success_url(self):
        bagno = self.get_bagno()
        return bagno.get_absolute_url()

    def get_context_data(self, *args, **kwargs):
        context = super(BagnoBooking, self).get_context_data(*args, **kwargs)
        context['bagno'] = self.get_bagno()
        return context


class BagnoContacts(ContactView):
    """ Contact info and form view for a single bagno
    """
    template_name = "bagni/bagno_contacts.html"
    form_class = ContactForm
    success_message = _("We forwarded your message to the beach resort. As soon as possible you'll receive a feedback to the email address provided.")

    def dispatch(self, request, *args, **kwargs):
        if "slug" not in kwargs:
            raise ObjectDoesNotExist
        slug = kwargs['slug']
        self.object = Bagno.objects.get(slug=slug)
        if not self.object.is_managed():
            raise PermissionDenied
        self.success_url = self.object.get_absolute_url()
        self.recipients = [m.user.email for m in self.object.managers.all()]
        self.form = self.get_form(self.form_class)
        self.submit_url = self.object.get_contactform_url()
        return super(BagnoContacts, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(BagnoContacts, self).get_context_data(*args, **kwargs)
        context.update({"form": self.form})
        return context
