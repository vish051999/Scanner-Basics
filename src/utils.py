import fitz
import cv2
from pyzbar.pyzbar import decode
import numpy as np

def detect_qr(img):
    qr = decode(img)[0]
    # print(qr)
    qr_orientation = qr.orientation.name
    # print(qr_orientation)
    modified_img = img
    if(qr_orientation=="LEFT"): #check if the qr is rotated left
        modified_img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif(qr_orientation=="DOWN"): #check if the qr is rotated 180 degrees
        modified_img = cv2.rotate(img, cv2.ROTATE_180)
    elif(qr_orientation=="RIGHT"): #check if the qr is rotated right
        modified_img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    modified_qr = decode(modified_img)[0]
    return modified_qr,modified_img

# print(decode(modified_img))


def draw_rect_qr(qr,img):
    left = qr.rect.left   # x-coordinate of top-left corner of qr
    top = qr.rect.top     # y-coordinate of top-left corner of qr

    width = qr.rect.width
    height = qr.rect.height

    start = (left,top)    # coordinates of top-left corner of qr
    end = (left+width,top+height)  # coordinates of bottom-right corner of qr

    color = (255,0,0)
    thickness = 2

    qr_img = cv2.rectangle(img,start,end,color,thickness)
    return qr_img

def draw_circles(img,circles,params,offset):
    # print(len(circles[0]))
    circles = np.uint16(np.around(circles))
    # print(circles)
    for i in circles[0,:]:
        center = {"x":i[0],"y":i[1]}  #coordinates of center of circle
        radius = i[2]

        # draw the outer circle
        img = cv2.circle(img,(center["x"]+params["left"],center["y"]+params["top"]+offset),radius,(0,255,255),2)
    return img

