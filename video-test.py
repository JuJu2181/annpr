from pytorch_YOLOv4.main2 import main_annpr_detector

  
    
filename = "D:\ANNPR_Complete_v2\\annpr\media\\videos\\test_vid3.mp4"
filename = "D:\ANNPR_Complete_v2\\annpr\media\\videos\\valid-video_short.mp4"
filename = "D:\ANNPR_Complete_v2\\annpr\media\\videos\\test_vid_4.mp4"

# filename = "D:\ANNPR_Complete_v2\\annpr\media\\videos\\test_vid_2_short.mp4"


main_annpr_detector("video",filename)

# ch = "ba12pa3533"
# print(validate_numberplate(ch))