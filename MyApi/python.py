import cv2
import numpy as np
from django.http import StreamingHttpResponse
from .views import start_timer, stop_timer,Check_timer
import time
from django.http import JsonResponse
from rest_framework.decorators import api_view
import threading
from django.http import HttpResponse
from .models import *
from django.shortcuts import render ,get_object_or_404
from django.contrib.sessions.models import Session

from django.http import HttpResponseServerError
from decimal import Decimal

# Define the lower and upper bounds for red color in HSV space




# Connect the signal handler
def detectRedObjects(frame):
    lower_red1 = np.array([160, 40, 145])
    upper_red1 = np.array([180, 255, 255])
    lower_red2 = np.array([160, 40, 145])
    upper_red2 = np.array([180, 255, 255])

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
            # print(min_distance)

            if min_distance < threshold_distance:
                return True
            else:
                return False
            

current_frame_position = 0
current_frame = None
gameStarted = False
#////////////////////////////////////////////////////////////////// WEBCAM

def background_video_processing(request,pk,pk1):
    person=get_object_or_404(Person,id=pk1)
    table=get_object_or_404(Table,tableno=pk)

    # video_path = r'C:\Users\Yukesh\Downloads\snookervideo\comined2.mp4'  # Replace with your video file path
    global global_button_state,current_frame, current_frame_position, gameStarted
    # Retrieve session variables
  

    cap = cv2.VideoCapture(cv2.CAP_ANY)  # Use 0 for the default webcam
    if not cap.isOpened():
        raise IOError("Webcam cannot be opened.")
   
    # print('==========================',pk)
    # cap = cv2.VideoCapture(video_path)
    # if not cap.isOpened():
    #         raise IOError("Video file cannot be opened.")
    print('=========================================================================')    
    skip_frames = 2
    frame_count = current_frame_position
    gameStarted=False
    count = 0 
    area=0
    approxed=0
    skip_until=0 
   

    while cap.isOpened():
        current_time=time.time()      #to get the current time
        ret, frame = cap.read()
        if not ret:
            break

        # Skip frames
        frame_count += 1
        current_frame_position = frame_count  # Update the global frame position

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
        median_blur= cv2.medianBlur(red_mask,23)
        median_blur_white= cv2.medianBlur(mask,21)
        # median_blur = median_blur.astype(np.uint8)
        # median_blur_white = median_blur_white.astype(np.uint8)

        # imgGray = cv2.cvtColor(median_blur, cv2.COLOR_BGR2GRAY)
        canny=cv2.Canny(median_blur,l,u)
        canny2=cv2.Canny(median_blur_white,l,u)
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours2, hierarchy = cv2.findContours(canny2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        frame_copy=frame.copy()
       
        def detection(area,approxed,gameStarted,count):  
            for contour in contours:
                epsilon = 0.03 * cv2.arcLength(contour, True)
                approxed = cv2.approxPolyDP(contour, epsilon, True)
                approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

                M = cv2.moments(approx)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])

                    # Define position and size of the text area
                    x = cX - 60  # Adjust as needed
                    y = cY + 40  # Adjust as needed
                    w = 100      # Width of the text area

                # Calculate the area of the contour

                area = cv2.contourArea(contour)
                if 13000 > area > 10000:
                    # Put the area text on the frame, positioned near the bottom right of the contour's bounding rectangle
                    
                    cv2.putText(frame, "Area: " + str(int(area)), (x + w - 60, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
                if len(approxed)==3:     
                    cv2.putText(frame, "Points: " + str(len(approxed)), (x + w - 60, y + 60), cv2.FONT_HERSHEY_COMPLEX, 0.5,(0, 255, 0), 1)
                

                # print('-----boolean----:', gameStarted)

                # if gameStarted :
                #     print(area,'-----------------------',len(approxed))
                #     if 13000 > area > 10000 and len(approxed)==3:


                #         cv2.putText(frame, "end", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)                
                #         print('*******game end*******')
                #         count += 1 
                #         print('count',count)

                #         gameStarted = False
                #         print('boolean:', gameStarted)
            return area , approxed
        
        area, approxed = detection(area,approxed,gameStarted,count)
# Loop through each contour in the second set of contours
        for contour2 in contours2:
            approx = cv2.approxPolyDP(contour2, 0.01 * cv2.arcLength(contour2, True), True)

            M = cv2.moments(approx)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                # Define position and size of the text area
                x = cX - 50  # Adjust as needed
                y = cY + 30  # Adjust as needed
                w = 100      # Width of the text area
            # Calculate the area of the contour
            area2 = cv2.contourArea(contour2)
            
            # Put the area text on the frame, positioned near the bottom right of the contour's bounding rectangle
            cv2.putText(frame, "Area: " + str(int(area2)), (x + w - 60, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)

        for contour in contours:
            epsilon = 0.03 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            cv2.drawContours(frame, [approx], -1, (255, 0, 0), 2)
        cv2.drawContours(frame,contours2,-1,(255,0,0),10)
      

    
        
        # cv2.drawContours(frame_copy,contours2,-1,(255,0,0),10)
        # combined_frame = np.hstack((frame,frame_copy))
        
        threshold_distance = 10
    # Adjust this value according to your requirement

        # Check if the frame is not empty



        if frame is not None:
            # cv2.imshow('binary video',dst)
            # cv2.imshow('median video',median_blur_white)
            if contour_touching(contours, contours2,threshold_distance):
                cv2.putText(frame, "PLAY", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)                
                
                
            if not gameStarted:     #enters if condition if it is false because not gameStarted is true(! of false = true)
                start_timer(request, pk)
                print('timer started==========================')
                frame
                gameStarted=True
                count += 1
                if table.frame_based: 
                    if count>person.frame:
                        print(person.frame)
                        print("Played more than their limited frame")
                    if count :
                        table.price=Decimal('0.0')
                        table.price=table.price+table.per_frame
                        print('-------',table.price)
                        table.save()
                print('count',count)

                skip_until=current_time + 1    # time.sleep(1)  # Delay for 1 second
            if start_timer:                                
                Check_timer(request,pk)

           
            
            # if gameStarted and current_time > skip_until:
            #         print(area,'-----------------------')
            #         if 13000 > area > 10000 and len(approxed)==3:
            #             cv2.putText(frame, "end", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)                
            #             print('*******game end*******')
            #             gameStarted = False
            #             stop_timer(request,pk)
            #             print('boolean:', gameStarted)
            current_frame = frame
           
            # if masks_overlap(red_mask, mask):
            #     print("Play")
            # else:
            #     print("Game Over")
                # cv2.putText(frame, "PLAY", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
           
            # ret, jpeg = cv2.imencode('.jpg', frame)
            # frame = jpeg.tobytes()
            # yield (b'--frame\r\n'
            #     b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
            # cv2.imshow('blur', imgGray)
            # cv2.imshow('binary video',canny2)

            # cv2.imshow('Input', frame_copy)
            # cv2.imshow('red', median_blur)

            # cv2.imshow('white', median_blur_white)
        
    # Update session variables
            

        # Press 'q' to exit the loop
        
         # Update the global current frame

    # Release the video capture object and close all windows
    cap.release()
def video_feed(request, pk):
    def frame_generator():
        global current_frame
        while True:
            if current_frame is not None and isinstance(current_frame, np.ndarray):
                ret, jpeg = cv2.imencode('.jpg', current_frame)
                if ret:
                    frame = jpeg.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            else:
                # Yield a placeholder image or a blank frame if current_frame is not valid
                blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                ret, jpeg = cv2.imencode('.jpg', blank_frame)
                if ret:
                    frame = jpeg.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    return StreamingHttpResponse(frame_generator(), content_type='multipart/x-mixed-replace; boundary=frame')

# def video_feed(request, pk):
#     def generate():
#         global current_frame
#         print(current_frame)
#         while True:
#             cap = cv2.VideoCapture(cv2.CAP_ANY)  # Change to 0 for default webcam
#             if not cap.isOpened():
#                 raise IOError("Webcam cannot be opened.")
            
#             while cap.isOpened():
#                 ret, current_frame = cap.read()
#                 if not ret:
#                     break
#                 # frame  = current_frame
#                 # Convert frame to JPEG format
#                 if current_frame is None or current_frame.size == 0:
#                     continue
                
#                 ret, jpeg = cv2.imencode('.jpg', current_frame)
#                 if not ret:
#                     continue
                
#                 frame_bytes = jpeg.tobytes()

#                 yield (b'--frame\r\n'
#                     b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

#             cap.release()

#     return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')

# def video_feed(request,pk):
#     global current_frame
    
#     # Call your video processing function to ensure current_frame is updated
#     # Note: Replace 'pk' with the appropriate parameter for your function
#     def generate_frames(pk):
#             generator = background_video_processing(request, pk)
#             for chunk in generator:
#                 yield chunk
        
#         # Use a separate generator to avoid interfering with the original generator
#     response = StreamingHttpResponse(generate_frames(pk), content_type='multipart/x-mixed-replace; boundary=frame')
#     return response


def index(request):
    return render(request, 'index.html')



def index(request,pk):
    return render(request, 'index.html',{'pk':pk})

def botton(request,pk):
    table = get_object_or_404(Table, id=pk)  # Replace with the correct logic to identify the Table instance
    if table.button==False:

        table.button=True
    else:
        table.button=False
    table.save()
    if table.button==True:
        start_timer(request,pk)

    else:
        stop_timer(request,pk)



    return JsonResponse({'botton': table.button})
#//////////////////////////////////////////////////////TESTING


def background_run(request,pk,pk1):
        # background_video_processing(request, pk)

        return StreamingHttpResponse(background_video_processing(request, pk,pk1),content_type='multipart/x-mixed-replace; boundary=frame')







# #//////////////////////////////////////////////////////WEBCAM
# def background_run(request,pk):
#          camera = cv2.VideoCapture(0)  # Use 0 for default webcam

#          return StreamingHttpResponse(background_video_processing(camera,request, pk),content_type='multipart/x-mixed-replace; boundary=frame')


# def video_feed(request,pk):
#     camera = cv2.VideoCapture(0)  # Use 0 for default webcam
#     def frame_generator(camera):
#         while True:
#             ret, frame = camera.read()
#             if not ret:
#                 continue
#             ret, jpeg = cv2.imencode('.jpg', frame)
#             if not ret:
#                 continue
#             frame = jpeg.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#     return StreamingHttpResponse(frame_generator(camera), content_type='multipart/x-mixed-replace; boundary=frame'
# )

#//////////////////////////////////////////////////////ORIGINAL
# def video_stream(request,pk):
#         return StreamingHttpResponse(video_feed(request, pk),content_type='multipart/x-mixed-replace; boundary=frame')
    

