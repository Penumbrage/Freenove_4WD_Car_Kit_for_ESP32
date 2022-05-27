import cv2
import urllib.request
import numpy as np
 
def nothing(x):
    pass
 
#change the IP address below according to the
#IP shown in the Serial monitor of Arduino code
url='http://192.168.0.4/cam-lo.jpg'

# Create a window to store the current video transmission from the ESP32 webserver
cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)
 
# Create window to change the different HSV values (hue, saturation, value)
cv2.namedWindow("Tracking")
cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)   #33
cv2.createTrackbar("LS", "Tracking", 0, 255, nothing)   #104
cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)   #12
cv2.createTrackbar("UH", "Tracking", 255, 255, nothing)
cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)
 
# main image obtaining loop
while True:
    # open url
    img_resp=urllib.request.urlopen(url)

    # obtain the current image as a numpy array from webserver
    imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)

    # optains image from buffer
    frame=cv2.imdecode(imgnp,-1)

    # rotate the frame to obtain correct orientation
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    # obtain the HSV values from the original RGB data
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    # obtain current positions of the trackbar for each of the HSV sliders
    l_h = cv2.getTrackbarPos("LH", "Tracking")
    l_s = cv2.getTrackbarPos("LS", "Tracking")
    l_v = cv2.getTrackbarPos("LV", "Tracking")
 
    u_h = cv2.getTrackbarPos("UH", "Tracking")
    u_s = cv2.getTrackbarPos("US", "Tracking")
    u_v = cv2.getTrackbarPos("UV", "Tracking")
 
    # store current positions for the trackbars
    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])
    
    # create HSV mask
    mask = cv2.inRange(hsv, l_b, u_b) 

    # create image that shows what color is being identified by the mask
    res = cv2.bitwise_and(frame, frame, mask=mask)
 
    # display the original video, the mask, and the combined videos
    cv2.imshow("live transmission", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("res", res)

    # break from the Python program using 'q'
    key=cv2.waitKey(5)
    if key==ord('q'):
        break

# eliminate all windows when quitting program
cv2.destroyAllWindows()