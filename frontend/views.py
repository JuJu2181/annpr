from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import NumberPlate, Image, Video, VideoNumberPlate
from .forms import ModelForm1, ImageForm, VideoForm
from pytorch_YOLOv4.main2 import main_annpr_detector
from pytorch_YOLOv4.validate_vid_number import validate_vid_number


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
    valid_first_chars = ['ba','ga','lu']
    valid_mid_chars = ['pa','cha']
    # check if the request is post request
    if request.method == "POST":
        # Check if any file is uploaded or NOT
        if len(request.FILES) != 0:
            form = ImageForm(request.POST, request.FILES)
            file = request.FILES.get('img')
            filename = file.name
            # print(filename)
            # print(file)
            # check if input file is actually an image 
            if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
                print("File is an Image")
                if form.is_valid():
                    # saving form and number plate image at end 
                    number_plate_image = form.save(commit=False)
                    number_plate_image.save()
                    # form.save()
                    # get output numbers from main_annpr_detector
                    output_numbers = main_annpr_detector(
                        detector='image', filename=filename)
                    # print(f'Detected Number: {output_number}')
                    detection_count = len(output_numbers)
                    recognition_count = detection_count
                    for output_number in output_numbers:
                        # creating an object for each detected number plate
                        numberplate = NumberPlate()
                        if output_number != '':
                            # get the starting character
                            starting_characters = output_number[0:2]
                            if starting_characters in valid_first_chars:
                                if 'pa' in output_number:
                                    numberplate.vehicle_type = '2-Wheeler'
                                    middle_characters_position = output_number.find('pa')
                                    middle_characters_count = 2
                                elif 'cha' in output_number:
                                    numberplate.vehicle_type = '4-Wheeler Medium'
                                    middle_characters_position = output_number.find('cha')
                                    middle_characters_count = 3
                                else:
                                    numberplate.vehicle_type = '4-Wheeler'
                                    middle_characters_position = -1
                                    recognition_count -= 1
                                # check if numbers are detected between starting and middle character
                                if middle_characters_position != -1:
                                    if(len(output_number[2:middle_characters_position]) <= 2):
                                        try:
                                            # check if middle 2 characters are really a number 
                                            middle_lot_number = int(output_number[2:middle_characters_position])
                                            # again check for last 4 digits 
                                            if(len(output_number[middle_characters_position + middle_characters_count:])<= 4):
                                                ending_number = int(output_number[middle_characters_position+middle_characters_count:])
                                                print("last 4 digits are  numbers")
                                                # saving only when all validation matches
                                                numberplate.number = output_number
                                                numberplate.save()
                                                print("Number Plate Saved") 
                                            else:
                                                print("More than 4 numbers detected")
                                                recognition_count -= 1
                                        except:
                                            print("Character detected instead of number")
                                            recognition_count -= 1
                                    else:
                                        print("More than 2 characters detected between starting and middle")
                                        recognition_count -= 1
                            else:
                                # this means that first character of recognition was not ba or others from list so it was not properly recognized
                                recognition_count -= 1
                                print("Starting character invalid")
                        else:
                            # empty string in list '' means that number plate was detected but recognition failed
                            recognition_count -= 1
                            print("No character was recognized")

                    
                    number_plate_image.name = filename
                    number_plate_image.detections_count = detection_count
                    number_plate_image.recognition_count = recognition_count
                    number_plate_image.save()
                    return redirect('display_image')
            else:
                print("Uploaded file not an image")
                return redirect('get_image')
        else:
            print("No file uploaded")
            return redirect('get_image')
    else:
        return redirect('get_image')


def upload_video(request):
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        file = request.FILES.get('video')
        filename = file.name
        print(f'Filename: {filename}')
        if filename.endswith('.mp4') or filename.endswith('.avi'):
            print(f' {filename} File is a video')
            if form.is_valid():
                number_plate_video = form.save(commit=False)
                number_plate_video.name = filename
                number_plate_video.save()
                output_numbers = main_annpr_detector(detector='video', filename=filename)
                print(f"Before: {output_numbers}")
                output_numbers = validate_vid_number(output_numbers)
                print(f"After: {output_numbers}")
                detection_count = len(output_numbers)
                recognition_count = detection_count
                print(f'Detected: {detection_count}')
                print(f'Recognized: {recognition_count}')
                for output_number in output_numbers:
                    # creating an object for each detected number plate
                    numberplate = VideoNumberPlate()
                    numberplate.number = output_number
                    if 'pa' in output_number:
                        numberplate.vehicle_type = '2-Wheeler'
                    elif 'cha' in output_number:
                        numberplate.vehicle_type = '4-Wheeler-Medium'
                    else:
                        numberplate.vehicle_type = '4-Wheeler'
                    numberplate.save()
                    print("Number Plate Saved") 
        
                number_plate_video.detections_count = detection_count
                number_plate_video.recognition_count = recognition_count
                number_plate_video.save()

                return redirect('display_video')
        else:
            print('File not a video')
            return redirect('get_video')
    else:
        return redirect('get_video')


def display_image(request):
    # getting latest image from database
    latest_image = Image.objects.latest('id')
    # getting image, name, detection count and recognition count from database
    image = latest_image.img
    filename = latest_image.name 
    detection_count = latest_image.detections_count
    recognition_count = latest_image.recognition_count
    # get last 10 number plates from database
    number_plates = NumberPlate.objects.all()[::-1][0:10]
    # get current number plates from the database
    current_number_plates = number_plates[0:recognition_count]
    # print(f'File: {filename}')
    context = {
        'image': image,
        'number_plates': number_plates,
        # 'current_number': current_number_plate.number,
        'current_number_plates': current_number_plates,
        'filename': filename,
        'title': 'DETECTIONS',
        'detection_count': detection_count,
        'recognition_count': recognition_count
    }
    return render(request, 'detections/image.html', context)
    


def display_video(request):
    latest_video = Video.objects.latest('id')
    # getting video details from database 
    video = latest_video.video
    filename = latest_video.name 
    detection_count = latest_video.detections_count
    recognition_count = latest_video.recognition_count
    # get last 10 number plates from database
    number_plates = VideoNumberPlate.objects.all()[::-1][0:10]
    # get current number plates from the database
    current_number_plates = number_plates[0:recognition_count]
    context = {
        'video': video,
        'number_plates': number_plates,
        'current_number_plates': current_number_plates,
        'filename': filename,
        'title': 'DETECTIONS',
        'detection_count': detection_count,
        'recognition_count': recognition_count
    }

    return render(request, 'detections/video.html', context)
