from django.db import models

class NumberPlate(models.Model):
    number=models.CharField(max_length=15)   
    entrydate= models.DateTimeField(auto_now_add=True, auto_now=False, blank= True)
    def __str__(self):
        return self.number
 
    
class Image(models.Model):
    img = models.ImageField(upload_to='images/',blank=True)

class Video(models.Model):
    videofile= models.FileField(upload_to='videos/', blank=True)  
