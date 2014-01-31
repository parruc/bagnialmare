from django.forms import ModelForm
from bagni.models import Bagno

# Create the form class.
class BagnoForm(ModelForm):
    class Meta:
        model = Bagno
        exclude = ['slug']
