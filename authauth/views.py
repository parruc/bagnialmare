from allauth.account.views import SignupView
from bagni.models import Bagno, Neighbourhood

class ManagerSignupView(SignupView):
    """ Passes a dictionary of neghbourhoods and associated Bagno instances for
    a better select form"""
    def get_context_data(self, **kwargs):
        context = super(ManagerSignupView, self).get_context_data(**kwargs)
        try:
            if self.request.GET.has_key('selected'):
                _pre_selected_key = int(self.request.GET['selected'])
                _selected_bagno = Bagno.objects.get(pk=_pre_selected_key)
                context.update(dict(pre_selected = (_selected_bagno.neighbourhood.pk,
                                                    _selected_bagno.pk,)))
        except:
            pass
        _select_neighbourhood = [(_neighbourhood.pk, _neighbourhood.name)
                                for _neighbourhood in Neighbourhood.objects.all().order_by("name")]
        context.update(dict(select_neighbourhood = _select_neighbourhood))
        return context

