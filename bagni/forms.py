from django.contrib.gis.forms import ModelForm, OSMWidget
from bagni.models import Bagno

class OmbrelloniOLWidget(OSMWidget):
    #TODO: this thing does not work ... shit
    class Media:
        js = ('http://cdnjs.cloudflare.com/ajax/libs/openlayers/2.11/OpenLayers.min.js',)

# Create the form class.
class BagnoForm(ModelForm):
    class Meta:
        model = Bagno
        exclude = ['slug']
        widgets = {
                'point' : OSMWidget(),
                }

