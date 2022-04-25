from pytorch_YOLOv4.demo import *
import cv2 
import time
import random
from keras.models import model_from_json #needed to import model from json
from pytorch_YOLOv4.process_image import processImage
import os 
import numpy as np
from pytorch_YOLOv4.sort_tuple_list import sort_tuple_in_list

use_cuda = False
process_fps = 8 
fps_detect_time = int(1000/process_fps) 

def detect_cv2_frame(m1,cv2_image):
    # m1 = MachineQueue.get()    
    # print("Starting the YOLO loop...")
    # namesfile = 'D:\ANNPR_integration\pytorch-YOLOv4\Own_cfg_and_weights\ANNPR.names'
    img = cv2_image
    width,height,_ = img.shape
    if img is None:
        print("Image Empty")
        return None
    sized = cv2.resize(img, (m1.width, m1.height))
    sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)

    # start = time.time()
    boxes = do_detect(m1, sized, 0.4, 0.6, use_cuda)
    
    # finish = time.time()
    # print('Predicted in %f seconds.' % (finish - start))

    return boxes

def detect_characters(m1,cv2_image,boxes):
    if cv2_image is None:
        return False
    width_np,height_np,_ = cv2_image.shape
    print(cv2_image.shape)
    allcharacters = []
    for box in boxes[0]:
        count_j = random.randint(1, 10000)
        x1_np,y1_np,x2_np,y2_np,_,_,_ = box
        x1_np,y1_np,x2_np,y2_np = int(x1_np*height_np),int(y1_np*width_np),int(x2_np*height_np),int(y2_np*width_np)
        print(x1_np,x2_np,y1_np,y2_np)
        #? Cropping each number plate
        img = cv2_image[y1_np:y2_np,x1_np:x2_np]
        # cv2.imwrite(f'pytorch-YOLOv4/detected_number_plates/number_plate{count_j}.jpg',img)
        print(f'Number plate{count_j} cropped')
        width,height,_ = img.shape
        if img is None:
            break
        # print(img)
        numplate_chars = []
        try:
            sized = cv2.resize(img, (m1.width, m1.height))
            sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)
            characters = do_detect(m1, sized, 0.25, 0.4, use_cuda)
            # allcharacters.append(characters[0])
            for character in characters[0]:
                x1,y1,x2,y2,_,_,_ = character
                chars = x1,y1,x2,y2 = x1_np+int(x1*height),y1_np+int(y1*width),x1_np+int(x2*height),y1_np+int(y2*width)
                numplate_chars.append(chars)
        except:
            pass
        allcharacters.append(numplate_chars)
    #         # print((x1_np+x1,y1_np+y1),(x2_np+x2,y2_np+y2))
    #         cv2_image = cv2.rectangle(cv2_image,(x1_np+x1,y1_np+y1),(x1_np+x2,y1_np+y2),(255,0,0),2)
    # # cv2.imshow("Cv2_image",cv2_image) 
    return allcharacters

def validate_numberplate(output_string):
    np = list(output_string)
    if output_string == '':
        return False
    if np[0]!='b':
        return False
    chars = [],[],[],[]
    # num_flag can have value 1 or 3; 1 --> vehicle lot and 3 --> vehicle number
    num_flag = 1
    for i in range(len(np)):
        ch = np[i]
        try: 
            chars[num_flag].append(int(ch))
        except:
            if ch == 'b':
                chars[0].append('ba')
            elif num_flag == 1:
                if ch == 'p':
                    chars[2].append('pa')
                    num_flag = 3
                elif ch == 'c':
                    chars[2].append('cha')
                    num_flag = 3
        
    # print(chars)

    if len(chars[0]) == 0 or len(chars[0]) > 1:
        return False
    if len(chars[1]) == 0 or len(chars[1]) > 2:
        return False
    if len(chars[2]) == 0 or len(chars[2]) > 1:
        return False
    if len(chars[3]) == 0 or len(chars[3]) > 4:
        return False
    number_plate =  chars[0]+chars[1]+chars[2]+chars[3]  
    number_plate = ''.join([str(elem) for elem in number_plate])
    return(number_plate)


# This is portion to reject numberplates where
def validate_chars_position_main(sorted_list):
    if len(sorted_list)>3:
        x1 = sorted_list[0][0]
        x1_sum = 0
        for chars in sorted_list:
            ch_x1,ch_y1,ch_x2,ch_y2 = chars
            x1_sum += ch_x2-ch_x1
        avg_x1 = x1_sum/len(sorted_list)
        limit = avg_x1*1.75
        for i in range(len(sorted_list)-1):
            prev = sorted_list[i]
            now = sorted_list[i+1]
            if abs(prev[0]-now[0])>limit:
                print("invalid")
                return False
    return sorted_list
    
def validate_chars_position(segmented_characters,list_sorted):
    upper_list,lower_list,is_2_row = list_sorted
    if is_2_row:
        if not (validate_chars_position_main(upper_list) or validate_chars_position_main(lower_list)):
            segmented_characters = []
    else:
        if not validate_chars_position_main(segmented_characters):
            segmented_characters = []
    return segmented_characters



def detect_video(YOLO_Detection,YOLO_Seperation,filename):
    cnn_img_dimensions = (32,32)
    #dictionary for class names 
    cnn_class_names = {
        0: '0',
        1: '१',
        2: '२',
        3: '३',
        4: '४',
        5: '५',
        6: '६',
        7: '७',
        8: '८',
        9: '९',
        10: 'बा',
        11: 'प',
        12: 'च'
    }

    cnn_class_names_en = {
            0: '0',
            1: '1',
            2: '2',
            3: '3',
            4: '4',
            5: '5',
            6: '6',
            7: '7',
            8: '8',
            9: '9',
            10: 'ba',
            11: 'pa',
            12: 'cha'
        }
    
    original_filename = filename
    print(f'File: {filename}')
    video_path = f'media\\videos\\{filename}'
    
    cfgfile,weightfile = YOLO_Detection
    cfgfile_sep,weightfile_sep = YOLO_Seperation
    
    m1 = Darknet(cfgfile)
    m2 = Darknet(cfgfile_sep)

    m3_json = open('pytorch_YOLOv4/cnn_weights/model_lenet_200_25.json','r')
    loaded_m3_json = m3_json.read()
    m3_json.close() 
    m3 = model_from_json(loaded_m3_json)
    m3.load_weights('pytorch_YOLOv4/cnn_weights/model_lenet_200_25.h5')


    # m2.print_network()
    # m1.print_network()
    m1.load_weights(weightfile)
    m2.load_weights(weightfile_sep)
    print('Loading weights from %s... Done!' % (weightfile))
    print('Loading weights from %s... Done!' % (weightfile_sep))
    cap = cv2.VideoCapture(video_path)
    ret,frame = cap.read()
    height,width,_=frame.shape
    # fps
    # original
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    # 6 fps
    # fps = 6
    # fourcc=cv2.VideoWriter_fourcc('M','J','P','G') # For avi
    # fourcc = cv2.VideoWriter_fourcc('F','M','P','4') #for mp4
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v') # For mp4
    # for h264 mp4 for html video player
    fourcc = cv2.VideoWriter_fourcc(*'H264')
    #or 
    #fourcc = cv2.cv.CV_FOURCC(*'X264')
    out = cv2.VideoWriter(f'media\\detected_videos\\{original_filename}',fourcc,fps,(int(width),int(height)))
    output_numbers = []
    output_numbers_fraemwise = []
    while ret:
        boxes = detect_cv2_frame(m1,frame)
        characters_boxes = detect_characters(m2,frame,boxes)
        output_numbers_in_frame = []
        for i in range(len(boxes[0])):
            x1,y1,x2,y2,_,_,_ = number_plate_bbox = boxes[0][i]
            x1,y1,x2,y2 = int(x1*width), int(y1*height), int(x2*width), int(y2*height)
            segmented_charcters,list_sorted = sort_tuple_in_list(characters_boxes[i])
            output_number = ""
            
            segmented_charcters =  validate_chars_position(segmented_charcters,list_sorted)                
            # This portion ends here
            
            
            
            for individual_char in segmented_charcters:
                ch_x1,ch_y1,ch_x2,ch_y2 = individual_char
                croped_char = frame[ch_y1:ch_y2,ch_x1:ch_x2]
                frame = cv2.rectangle(frame,(ch_x1,ch_y1),(ch_x2,ch_y2),(255,0,0),1)
                croped_char = cv2.resize(croped_char,cnn_img_dimensions)
                croped_char = processImage(croped_char)
                croped_char = croped_char.reshape(1,32,32,1)
                predict_x = m3.predict(croped_char)
                class_of_x=np.argmax(predict_x,axis=1)
                class_id = class_of_x[0]
                # img1 = cv2.resize(cropped_img,(300,300))
                # print(class_id,cnn_class_names[class_id])
                output_number+=cnn_class_names_en[class_id]
            frame = cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
            exists = False
            
            for items in output_numbers:
                if output_number == items:
                    exists = True
                    break
            result = validate_numberplate(output_number)
            if not exists:
                if result: 
                    output_numbers.append(result)
            output_numbers_in_frame.append(output_number)
        print(f"Output Numbers:{output_number}")
        out.write(frame)
        
        # output_numbers_fraemwise.append(output_numbers_in_frame)
        
        
        ret,frame = cap.read()
        try:
            frame.shape
        except:
            break
    print(f"All number_plates Recognized:{output_numbers}")
    cap.release()
    out.release()
    return output_numbers
    # print(f"Number-plates framewise:{output_numbers_fraemwise}")

    

def detect_cv2_image(YOLO_Detection,YOLO_Seperation,filename):
   ##############################Params###################################
    cnn_width = 640
    cnn_height = 480
    cnn_img_dimensions = (32,32)
    #dictionary for class names 
    cnn_class_names = {
        0: '0',
        1: '१',
        2: '२',
        3: '३',
        4: '४',
        5: '५',
        6: '६',
        7: '७',
        8: '८',
        9: '९',
        10: 'बा',
        11: 'प',
        12: 'च'
    }

    cnn_class_names_en = {
            0: '0',
            1: '1',
            2: '2',
            3: '3',
            4: '4',
            5: '5',
            6: '6',
            7: '7',
            8: '8',
            9: '9',
            10: 'ba',
            11: 'pa',
            12: 'cha'
        }

    cnn_no_of_classes = 19
    ####################################################################### 
    original_filename = filename
    image_path = f'media\images\\{filename}'

    print(f'image_path: {image_path}')
    cfgfile,weightfile = YOLO_Detection
    cfgfile_sep,weightfile_sep = YOLO_Seperation
    
    m1 = Darknet(cfgfile)
    m2 = Darknet(cfgfile_sep)
    m3_json = open('pytorch_YOLOv4/cnn_weights/model_lenet_200_25.json','r')
    loaded_m3_json = m3_json.read()
    m3_json.close() 
    m3 = model_from_json(loaded_m3_json)
    m3.load_weights('pytorch_YOLOv4/cnn_weights/model_lenet_200_25.h5')

    print("Model has been loaded from disk")

    m2.print_network()
    m1.print_network()
    m1.load_weights(weightfile)
    m2.load_weights(weightfile_sep) 
    
    print(f"=---------------{image_path}-----------")
    img = cv2.imread(image_path)
    # print(img)
    img = cv2.resize(img,(800,600))
    # print(f'Original Shape: {img.shape}')
    height,width,_ = img.shape
    
    boxes = detect_cv2_frame(m1,img)
    characters_bbox = detect_characters(m2,img,boxes)
    output_numbers = []
    for i in range(len(boxes[0])):
        box = boxes[0][i]
        x1,y1,x2,y2,cf,_,_ = box
        x1,y1,x2,y2 = int(x1*width),int(y1*height),int(x2*width),int(y2*height)
        img = cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
        segmented_characters,sorted_list = sort_tuple_in_list(characters_bbox[i]) 
        
        
        segmented_characters = validate_chars_position(segmented_characters,sorted_list)
        
        
        
        # segmented_characters = characters_bbox[i]
        # print(segmented_characters)
        output_number = ""
        for character_bbox in segmented_characters:
            count_i = random.randint(1, 100000)
            filename = f'char_{count_i}.jpg'
            xx1,yy1,xx2,yy2 = character_bbox
            # print(characters_bbox[i])
            # x1,y1,x2,y2 = int(x1*width),int(y1*height),int(x2*width),int(y2*height)
            img = cv2.rectangle(img,(xx1,yy1),(xx2,yy2),(255,0,0),2)
            #?cropping for character
            cropped_img = img[yy1:yy2,xx1:xx2]
            # print(f'shape: {cropped_img.shape}')
            # cv2.imwrite(f'pytorch-YOLOv4/detected_characters/detected_char{count_i}.jpg',cropped_img)
            # print(f'character_{count_i} Saved') 
            # img1 = cv2.imread(f'pytorch-YOLOv4/detected_characters/detected_char{count_i}.jpg',1)
            img1 = cv2.resize(cropped_img,cnn_img_dimensions)
            # preprocessing image ww
            img1 = processImage(img1)
            # cv2.imshow("Processed Image",img)
            # reshape image before sending it to predictor 
            img1 = img1.reshape(1,32,32,1)
            #predict 
            # classIndex = int(model.predict_classes(img))
            #predicting using model m3 for CNN
            predict_x=m3.predict(img1)
            class_of_x=np.argmax(predict_x,axis=1)
            class_id = class_of_x[0]
            img1 = cv2.resize(cropped_img,(300,300))
            print(class_id,cnn_class_names[class_id])
            output_number+=cnn_class_names_en[class_id]
            # cv2.putText(img,cnn_class_names_en[class_id], (50,50),fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=3, color=(0, 255, 0),thickness=3)
            # cv2.imwrite(filename, img)
        output_numbers.append(output_number)
    print(f"Output Numbers: {output_numbers}")
    cv2.imwrite(f'media\detected_images\\{original_filename}', img)
    # cv2.imshow("Detected",img)
    # cv2.waitKey(0)
    return output_numbers

# making this a function so I can then import it in django
def main_annpr_detector(detector,filename):
    # For YOLO Detection
    cfg = 'pytorch_YOLOv4\Own_cfg_and_weights\ANNPR.cfg'
    wgts = 'pytorch_YOLOv4\Own_cfg_and_weights\ANNPR.weights'
    
    YOLO_detection = (cfg,wgts)
    
    #For YOLO Character Saperation
    
    cfg = 'pytorch_YOLOv4\Own_cfg_and_weights\Character_saperation.cfg'
    wgts = 'pytorch_YOLOv4\Own_cfg_and_weights\Character_saperation.weights'
    
    YOLO_seperation = (cfg,wgts)
    
    
    # vidfile = 'D:\ANNPR_integration\pytorch-YOLOv4\data\\test_video_characters.mp4'
    # vidfile = 'D:\ANNPR_integration\pytorch-YOLOv4\data\\testvideo_multi.mp4'
    # vidfile = 'pytorch-YOLOv4\data\\test.mp4'
    # vidfile = 'D:/Documents/6th_Sem/Minor_Project/Codes/annpr/annpr-integration/videos/video6.mp4'
    # filename = 'a127.jpg'
    # image_path = 'pytorch-YOLOv4\data\\a127.jpg'
    
    start_time = time.time()
    # detect_cv2_video(YOLO_detection,YOLO_seperation,vidfile)
    if detector == 'image': 
        print(f'File: {filename}')
        output_numbers = detect_cv2_image(YOLO_detection, YOLO_seperation, filename)
        return output_numbers
    elif detector == 'video':
        output_numbers = detect_video(YOLO_detection, YOLO_seperation, filename)
        return output_numbers
    else:
        print("Invalid Option!")
    end_time = time.time() 
    total_time = end_time - start_time
    print(f"Total Time Taken: {total_time} sec")
    
