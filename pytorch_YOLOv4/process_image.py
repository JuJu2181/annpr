import cv2
import numpy as np 
import os 

def processImage(img):
    kernel = np.ones((3,3),np.uint8)
    # grayscale conversion
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #eroison(Morphological Transformation)
    # img = cv2.erode(img,kernel,iterations=1)

    # applying Otsu Binary thresholding
    # as an extra flag in binary 
    # thresholding
    # params: source, threshold value, max value, thresholding technique  
    ret, thresh1 = cv2.threshold(img, 125, 255, cv2.THRESH_BINARY +cv2.THRESH_OTSU)
    # median blur
    img = cv2.medianBlur(thresh1, 3)
    # resizing 
    # for lenet (32,32)
    # for alexnet (128,128)
    img = cv2.resize(img, (32,32))

    return img 


if __name__ == '__main__':
    for class_val in range(12):
        ip_dir_path = 'test/'+str(class_val)+'/' 
        op_dir_path = 'test2/'+str(class_val)+'/'
        # create directories in path if not exists
        if not os.path.isdir(op_dir_path):
            os.mkdir(op_dir_path)
        images = os.listdir(ip_dir_path)
        for img_path in images:
            img = cv2.imread(ip_dir_path+img_path)
            img = processImage(img)
            cv2.imwrite(op_dir_path+img_path, img)

    # ip_dir_path = 'test3/0/'
    # op_dir_path = 'test4/0_2/'
    # images = os.listdir(ip_dir_path)
    # for img_path in images:
    #     img = cv2.imread(ip_dir_path+img_path)
    #     img = processImage(img)
    #     cv2.imwrite(op_dir_path+img_path, img)    
    print('Preprocessing done')
