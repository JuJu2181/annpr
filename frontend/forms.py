from django import forms
from .models import NumberPlate,Image,Video

class ModelForm1(forms.ModelForm):
    class Meta:
        model= NumberPlate
        fields =['number']
class ImageForm(forms.ModelForm):
    class Meta:
        model= Image
        fields =['img']

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['videofile']
