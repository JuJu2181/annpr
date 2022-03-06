from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/',views.about, name='about'),
    path('imageform/',views.get_image,name='get_image'),
    path('videoform/',views.get_video,name='get_video'), 
    path('upload_image',views.upload_image,name='upload_image'),
    path('upload_video',views.upload_video,name='upload_video'),
    # path('image_detection/<filename>/<detection_count>/<recognition_count>',views.display_image,name='display_image'),
    path('image_detection/',views.display_image,name='display_image'),
    path('video_detection/',views.display_video,name='display_video'),
]
