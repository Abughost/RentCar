from django.forms import ClearableFileInput
from django.forms.models import ModelForm

from apps.models import CarImage


class CarImageForm(ModelForm):
    class Meta:
        model = CarImage
        fields = '__all__'
        widgets = {
            'image': ClearableFileInput(attrs={'class': 'dropzone'})}
