from django.forms import ModelForm
from models import Manager

# Create the form class.
class ManagerSignupForm(ModelForm):
    class Meta:
        model = Manager
        fields = ['bagno', 'privacy']
    def save(self, user):
        m = Manager.objects.create()
        m.user = user
        m.bagno = self.cleaned_data['bagno']
        m.privacy = self.cleaned_data['privacy']
        m.save()
