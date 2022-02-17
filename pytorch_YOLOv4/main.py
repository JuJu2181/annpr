from demo import *
import multiprocessing
use_cuda = False

def detect_cv2_video(cfgfile, weightfile,video_path):
    import cv2
    m1 = Darknet(cfgfile)

    m1.print_network()
    m1.load_weights(weightfile)
    print('Loading weights from %s... Done!' % (weightfile))
    cap = cv2.VideoCapture(video_path)
    width  = cap.get(3)         # get(3) gives width and 4 gives height
    height = cap.get(4)  
    # cap = cv2.VideoCapture("./test.mp4")
    cap.set(3, 1280)
    cap.set(4, 720)
    print("Starting the YOLO loop...")
    namesfile = 'D:\ANNPR_integration\pytorch-YOLOv4\Own_cfg_and_weights\ANNPR.names'
    class_names = load_class_names(namesfile)
    while True:
        ret, img = cap.read()
        if not ret:
            print("Image Empty")
            break
        sized = cv2.resize(img, (m1.width, m1.height))
        sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)

        start = time.time()
        boxes = do_detect(m1, sized, 0.4, 0.6, use_cuda)
        
        finish = time.time()
        print('Predicted in %f seconds.' % (finish - start))


        for box in boxes[0]:
            x1,y1,x2,y2,cf,_,_ = box
            x1,y1,x2,y2 = int(x1*width),int(y1*height),int(x2*width),int(y2*height)
            img = cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)

        # result_img = plot_boxes_cv2(img, boxes[0], savename=None, class_names=class_names)
        
        # cv2.rectangle()
        cv2.imshow('Yolo demo', img)
        # q
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.waitKey(0)


if __name__ == "__main__":
    cfg = 'D:\ANNPR_integration\pytorch-YOLOv4\Own_cfg_and_weights\ANNPR.cfg'
    wgts = 'D:\ANNPR_integration\pytorch-YOLOv4\Own_cfg_and_weights\ANNPR.weights'
    vidfile = 'D:\ANNPR_integration\pytorch-YOLOv4\data\\test.mp4'

    detect_cv2_video(cfg,wgts,vidfile)


