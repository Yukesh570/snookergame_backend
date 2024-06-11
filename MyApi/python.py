import cv2
import numpy as np
from django.http import StreamingHttpResponse
from .views import start_timer

# Define the lower and upper bounds for red color in HSV space


lower_red1 = np.array([0, 170, 40])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 170, 40])
upper_red2 = np.array([180, 255, 255])


def detectRedObjects(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)
    return red_mask

def detectObjects(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 170])
    upper_white = np.array([180,40, 255])
    mask = cv2.inRange(hsv, lower_white, upper_white)
    return mask



def contour_touching(contour1,contour2,threshold_distance):
    if contour2 is None:
        return False
    for contour1 in contour1:
        for contour2 in contour2:
            # Convert contours to numpy arrays

            contour1 = np.squeeze(contour1)
            contour2 = np.squeeze(contour2)

            # Calculate distances between points on the two contours
            distances = np.linalg.norm(contour1[:, None] - contour2, axis=-1)

            # Check if minimum distance is less than threshold
            min_distance = np.min(distances)
            print(min_distance)

            if min_distance < threshold_distance:
                return True
            else:
                return False



def video_feed(request, pk):
    video_path = r'C:\Users\Yukesh\Downloads\snookervideo\wedxx.mp4'  # Replace with your video file path

   
    print('==========================',pk)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
            raise IOError("Video file cannot be opened.")
        
    skip_frames = 2
    frame_count = 0
    gameStarted=False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Skip frames
        frame_count += 1
        if frame_count % skip_frames != 0:
            continue

        #retreive values
        frame=cv2.resize(frame,(500,500))
        # l = cv2.getTrackbarPos('Lower','Trackbars')
        # u = cv2.getTrackbarPos('Upper', 'Trackbars')
        l=20
        u=145
        # print(l,u)
        # imgBlur = cv2.GaussianBlur(frame, (25, 25), 1)

        # dst = cv2.fastNlMeansDenoisingColored(frame,None,15,15,3,10)
        red_mask=detectRedObjects(frame)
        mask=detectObjects(frame)
        median_blur= cv2.medianBlur(red_mask,21)
        median_blur_white= cv2.medianBlur(mask,21)
        # median_blur = median_blur.astype(np.uint8)
        # median_blur_white = median_blur_white.astype(np.uint8)

        # imgGray = cv2.cvtColor(median_blur, cv2.COLOR_BGR2GRAY)
        canny=cv2.Canny(median_blur,l,u)
        canny2=cv2.Canny(median_blur_white,l,u)
        print(pk)
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours2, hierarchy = cv2.findContours(canny2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        frame_copy=frame.copy()
        cv2.drawContours(frame,contours,-1,(255,0,0),5)
        cv2.drawContours(frame_copy,contours2,-1,(255,0,0),10)

        threshold_distance = 60
    # Adjust this value according to your requirement

        # Check if the frame is not empty
        if frame is not None:
            # cv2.imshow('binary video',dst)
            # cv2.imshow('median video',median_blur_white)
            if contour_touching(contours, contours2,threshold_distance):
                cv2.putText(frame, "PLAY", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)                
                
                
                if not gameStarted: 
                    start_timer(request, pk)
                    print('timerbdfbdfb started==========================')
                    gameStarted=True
                    
            # if masks_overlap(red_mask, mask):
            #     print("Play")
            # else:
            #     print("Game Over")
                # cv2.putText(frame, "PLAY", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            # cv2.imshow('blur', imgGray)
            # cv2.imshow('binary video',canny2)

            # cv2.imshow('Input', frame_copy)
            # cv2.imshow('red', median_blur)

            # cv2.imshow('white', median_blur_white)
        
                    

        # Press 'q' to exit the loop
        

    # Release the video capture object and close all windows
    cap.release()
    


# def index(request,pk):
#     return render(request, 'index.html',{'pk':pk})


def video_stream(request,pk):
    return StreamingHttpResponse(video_feed(request, pk),content_type='multipart/x-mixed-replace; boundary=frame')
