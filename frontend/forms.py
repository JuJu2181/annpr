from django import forms
from .models import NumberPlate,Image,Video

class ModelForm1(forms.ModelForm):
    class Meta:
        model= NumberPlate
        fields =['number']
class ImageForm(forms.ModelForm):
    class Meta:
        model= Image
        exclude =['name','detections_count','recognition_count']

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        exclude =['name','detections_count','recognition_count']
