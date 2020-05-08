from django.forms import ModelForm 

from .models import BasicMarker, Path, Palace

class BasicMarkerForm(ModelForm):
    class Meta:
        model = BasicMarker
        #type: 'basic'
        fields = ['title', 'infoText', 'path']

    ## only show paths that belong to the 'current' palace
    ## this code doesn't work
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['path'].queryset = Path.objects.none()
        if 'palace' in self.data:
            try:
                palace_id = int(self.data.get('palace'))
                self.fields['path'].queryset = Path.objects.filter(palace_id=palace_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['path'].queryset = self.instance.palace.path_set
    
class PathForm(ModelForm):
    class Meta:
        model = Path 
        fields = ['title', 'palace', 'type']

class PalaceForm(ModelForm):
    class Meta:
        model = Palace
        fields = ['title']