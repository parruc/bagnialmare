# -*- coding: utf-8 -*-

from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.contrib import messages
#from django.utils.translation import ugettext as _

from ..models import Bagno
from ..forms import BagnoForm, TelephoneFormSet, ImageFormSet

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
        is_staff = request.user.is_staff
        try:
            manager = request.user.manager
            can_edit = manager.can_edit(self.object)
        except (ObjectDoesNotExist, AttributeError):
            can_edit = False
        if is_staff or can_edit:
            return super(BagnoEdit, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied

    def post(self, request, *args, **kwargs):
        # this is necessary when overriding post and get
        self.object = self.get_object()
        form = BagnoForm(data=request.POST)
        telephone_formset = TelephoneFormSet(request.POST,
                instance = self.object)
        image_formset = ImageFormSet(request.POST, request.FILES,
                instance = self.object)
        if not telephone_formset.is_valid() or not image_formset.is_valid() or not form.is_valid():
            for index, t_error in enumerate(telephone_formset.errors):
                for field, error_messages in t_error.iteritems():
                    for error_message in error_messages:
                        _msg = "Telephone: %d field: %s error: %s" % (index, field, error_message)
                        messages.add_message(self.request, messages.ERROR, _msg)
                        logger.error(_msg)
            for index, i_error in enumerate(image_formset.errors):
                for field, error_messages in i_error.iteritems():
                    for error_message in error_messages:
                        _msg = "Image: %d field: %s error: %s" % (index, field, error_message)
                        messages.add_message(self.request, messages.ERROR, _msg)
                        logger.error(_msg)
            return self.render_to_response(
                    self.get_context_data(
                        telephone_formset = telephone_formset,
                        image_formset = image_formset,
                        form = form,
                    )
                )
        else:
            telephone_formset.save(commit=False)
            image_formset.save(commit=False)
            telephone_formset.save()
            image_formset.save()
            return super(BagnoEdit, self).post(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(BagnoEdit, self).get_context_data(*args, **kwargs)
        context['telephone_formset'] = TelephoneFormSet(instance = self.object)
        context['image_formset'] = ImageFormSet(instance = self.object)
        return context