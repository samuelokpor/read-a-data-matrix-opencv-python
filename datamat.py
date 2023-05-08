import numpy as np
import cv2
from pylibdmtx import pylibdmtx
import ctypes

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def on_trackbar(val):
    global gray, thresh, image

    # Apply threshold with the new value of val
    ret, thresh = cv2.threshold(gray, val, 255, cv2.THRESH_BINARY)
    
    # Decode the new thresholded image
    codes = pylibdmtx.decode(thresh)
    
    # Draw a green bounding box around the code in the image
    if len(codes) > 0:
        rect = codes[0].rect
        pts = [(rect.left + 0, rect.top - 20),
           (rect.left + rect.width - 0, rect.top - 20),
           (rect.left + rect.width - 0, rect.top + rect.height - 15),
           (rect.left + 0, rect.top + rect.height - 15)]
        cv2.polylines(image, [np.array(pts)], True, (0, 255, 0), 2)
        
        # Get the decoded message and show it in a message box
        message = codes[0].data.decode("utf-8")
        Mbox("Decoded Message", message, 0)
    
    # Display the thresholded image
    cv2.imshow('Thresholded Image', thresh)
    # Display the original image with the bounding box drawn on it
    cv2.imshow('Data Matrix QR Code', image)

if __name__ == '__main__':

    image = cv2.imread('codes/test4.jpg', cv2.IMREAD_UNCHANGED)
    image = cv2.resize(image, (300,300))

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Set an initial threshold value
    thresh_val = 100

    # Apply threshold with initial value of thresh_val
    ret,thresh = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    codes = pylibdmtx.decode(thresh)

    # Draw a green bounding box around the code in the image
    rect = codes[0].rect
    pts = [(rect.left + 0, rect.top - 20),
           (rect.left + rect.width - 0, rect.top - 20),
           (rect.left + rect.width - 0, rect.top + rect.height - 15),
           (rect.left + 0, rect.top + rect.height - 15)]
    cv2.polylines(image, [np.array(pts)], True, (0, 255, 0), 2)

    # Create a window to display the images
    cv2.namedWindow('Data Matrix QR Code', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Data Matrix QR Code', 600, 600)

    # Create a trackbar to adjust the threshold value
    cv2.createTrackbar('Threshold', 'Data Matrix QR Code', thresh_val, 255, on_trackbar)

    # Display the thresholded image
    cv2.imshow('Thresholded Image', thresh)

    # Display the original image with the bounding box drawn on it
    cv2.imshow('Data Matrix QR Code', image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
