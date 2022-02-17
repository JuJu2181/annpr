from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import NumberPlate, Image, Video
from .forms import ModelForm1,ImageForm, VideoForm
from pytorch_YOLOv4.main2 import main_annpr_detector

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request, 'about.html')

def get_image(request):
    numb=NumberPlate.objects.all()
    form = ImageForm()  
    context={
        'numb':numb,
        'form': form,
        'title': 'Image'
    }
    return render(request,'upload_form.html',context)

def get_video(request):
    numb=NumberPlate.objects.all()
    form = VideoForm()  
    context={
        'numb':numb,
        'form': form,
        'title': 'Video'
    }
    return render(request,'upload_form.html',context)

def upload_image(request):
    if request.method == "POST":
        form = ImageForm(request.POST,request.FILES)
        numberplate = NumberPlate()
        file = request.FILES.get('img')
        filename = file.name
        # print(filename)
        # print(file)
        if form.is_valid():
            form.save()
            output_number = main_annpr_detector(detector='image', filename=filename)
            # print(f'Detected Number: {output_number}')
            numberplate.number = output_number
            numberplate.save()
            
            return redirect('display_image',filename)
    else:
        return redirect('get_image')
    

def upload_video(request):
    if request.method == "POST":
        form = VideoForm(request.POST,request.FILES)
        file = request.FILES.get('videofile')
        filename = file.name
        if filename.endswith('.mp4') or filename.endswith('.avi'):
            print('File is a video')
            if form.is_valid():
                form.save()
                return redirect('display_video')
        else:
            print('File not a video')
            return redirect('get_video')
    else:
        return redirect('get_video')

def display_image(request,filename):
    latest_image = Image.objects.latest('id');
    number_plates = NumberPlate.objects.all()[::-1];
    current_number_plate = NumberPlate.objects.latest('id');
    image = latest_image.img
    print(f'File: {filename}')
    context = {
        'image': image,
        'number_plates': number_plates,
        'current_number': current_number_plate.number,
        'filename': filename
    }
    return render(request, 'detections/image.html',context)

def display_video(request):
    latest_video = Video.objects.latest('id');
    number_plate = NumberPlate.objects.all();
    video = latest_video.videofile
    context = {
        'video': video,
        'number_plate': number_plate
    }

    return render(request,'detections/video.html',context)
