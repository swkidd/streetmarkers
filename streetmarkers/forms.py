from django.forms import ModelForm 

from .models import BasicMarker, Path, Palace

class BasicMarkerForm(ModelForm):
    class Meta:
        model = BasicMarker
        #type: 'basic'
        fields = ['title', 'infoText', 'path', 'palace']
   

    ## only show paths that belong to the 'current' palace
    
class PathForm(ModelForm):
    class Meta:
        model = Path 
        fields = ['title', 'palace', 'type']

class PalaceForm(ModelForm):
    class Meta:
        model = Palace
        fields = ['title']