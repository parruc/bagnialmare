from allauth.account.views import SignupView
from bagni.models import Bagno, Neighbourhood

class ManagerSignupView(SignupView):
    """ Passes a dictionary of neghbourhoods and associated Bagno instances for
    a better select form"""
    def get_context_data(self, **kwargs):
        context = super(ManagerSignupView, self).get_context_data(**kwargs)
        _pre_selected_key = self.request.GET.get('selected', None)
        if not _pre_selected_key:
            _pre_selected_key = self.request.POST.get('bagni', None)
        if _pre_selected_key:
            try:
                _selected_bagno = Bagno.objects.get(pk=int(_pre_selected_key))
                context.update(dict(pre_selected = (_selected_bagno.neighbourhood.pk, _selected_bagno.pk,)))
            except:
                pass
        _select_neighbourhood = [(_neighbourhood.pk, _neighbourhood)
                                for _neighbourhood in Neighbourhood.objects.all().order_by("municipality__name")]
        context.update(dict(select_neighbourhood = _select_neighbourhood))
        return context

