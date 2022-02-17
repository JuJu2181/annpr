from django.contrib import admin

# Register your models here.
from .models import NumberPlate, Image, Video 

admin.site.register(NumberPlate)
admin.site.register(Image)
admin.site.register(Video)
# admin.site.register(MediaFiles)
