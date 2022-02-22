from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import NumberPlate, Image, Video
from .forms import ModelForm1, ImageForm, VideoForm
from pytorch_YOLOv4.main2 import main_annpr_detector


def index(request):
    context = {
        'title': 'HOME'
    }
    return render(request, 'index.html', context)


def about(request):
    context = {
        'title': 'ABOUT'
    }
    return render(request, 'about.html', context)


def get_image(request):
    numb = NumberPlate.objects.all()
    form = ImageForm()
    context = {
        'numb': numb,
        'form': form,
        'title': 'IMAGE'
    }
    return render(request, 'upload_form.html', context)


def get_video(request):
    numb = NumberPlate.objects.all()
    form = VideoForm()
    context = {
        'numb': numb,
        'form': form,
        'title': 'VIDEO'
    }
    return render(request, 'upload_form.html', context)


def upload_image(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        file = request.FILES.get('img')
        filename = file.name
        # print(filename)
        # print(file)
        if form.is_valid():
            form.save()
            output_numbers = main_annpr_detector(
                detector='image', filename=filename)
            # print(f'Detected Number: {output_number}')
            numbers_count = len(output_numbers)
            for output_number in output_numbers:
                numberplate = NumberPlate()
                if output_number != '':
                    numberplate.number = output_number
                    numberplate.save()
                    print("Number Plate Saved")
                else:
                    numbers_count -= 1

            return redirect('display_image', filename, numbers_count)
    else:
        return redirect('get_image')


def upload_video(request):
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
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


def display_image(request, filename, numbers_count):
    
    numbers_count = int(numbers_count)
    print(f"filename: {filename}\nNumbers_count:{numbers_count}")
    latest_image = Image.objects.latest('id')
    number_plates = NumberPlate.objects.all()[::-1][0:10]
    # current_number_plate = NumberPlate.objects.latest('id');
    current_number_plates = number_plates[0:numbers_count]
    image = latest_image.img
    print(f'File: {filename}')
    context = {
        'image': image,
        'number_plates': number_plates,
        # 'current_number': current_number_plate.number,
        'current_number_plates': current_number_plates,
        'filename': filename,
        'title': 'DETECTIONS'
    }
    return render(request, 'detections/image.html', context)
    


def display_video(request):
    latest_video = Video.objects.latest('id')
    number_plate = NumberPlate.objects.all()
    video = latest_video.videofile
    context = {
        'video': video,
        'number_plate': number_plate
    }

    return render(request, 'detections/video.html', context)
