from django.db import models

class NumberPlate(models.Model):
    number=models.CharField(max_length=15)   
    entrydate= models.DateTimeField(auto_now_add=True, auto_now=False, blank= True)
    vehicle_type = models.CharField(max_length=30)
    def __str__(self):
        return self.number

class VideoNumberPlate(models.Model):
    number=models.CharField(max_length=15)
    entrydate = models.DateTimeField(auto_now_add=True,auto_now=False,blank=True)
    vehicle_type = models.CharField(max_length=30)
    def __str__(self):
        return self.number
    
    
class Image(models.Model):
    img = models.ImageField(upload_to='images/',blank=True)
    name = models.CharField(max_length=50,blank=True)
    detections_count = models.IntegerField(blank=True,default=0)
    recognition_count = models.IntegerField(blank=True,default=0)


class Video(models.Model):
    video= models.FileField(upload_to='videos/', blank=True)  
    name = models.CharField(max_length=50,blank=True)
    detections_count = models.IntegerField(blank=True,default=0)
    recognition_count = models.IntegerField(blank=True,default=0)
