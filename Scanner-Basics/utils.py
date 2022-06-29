import fitz
import cv2
from pyzbar.pyzbar import decode
import numpy as np

def detect_qr(img):
    qr = decode(img)
    # print(qr)
    modified_img = img
    if(qr[0][4]==1): #check if the qr is rotated left
        modified_img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif(qr[0][4]==2): #check if the qr is rotated 180 degrees
        modified_img = cv2.rotate(img, cv2.ROTATE_180)
    elif(qr[0][4]==3): #check if the qr is rotated right
        modified_img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    modified_qr = decode(modified_img)
    return modified_qr,modified_img

# print(decode(modified_img))


def draw_rect_qr(qr,img):
    start = (qr[0][2][0],qr[0][2][1])
    end = (qr[0][2][0]+qr[0][2][2],qr[0][2][1]+qr[0][2][3])
    color = (255,0,0)
    thickness = 2

    qr_img = cv2.rectangle(img,start,end,color,thickness)
    return qr_img

def draw_circles(img,circles,params,offset):
    # print(len(circles[0]))
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        img = cv2.circle(img,(i[0]+params["left"],i[1]+params["top"]+offset),i[2],(255,0,0),1)
    return img