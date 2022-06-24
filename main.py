import fitz
import cv2
from pyzbar.pyzbar import decode
import numpy as np 

pdf_1 = fitz.open("bubble_sheet_292_0.pdf")
path_1 = "bubble_sheet_292_0_pages"

pdf_2 = fitz.open("bubble_sheet_293_0.pdf")
path_2 = "bubble_sheet_293_0_pages"

def _pdfToImages(pdf,path):
    num_pages = pdf.pageCount
    image_matrix = fitz.Matrix(fitz.Identity)
    image_matrix.preScale(1, 1)
    for i in range(num_pages):
        pix = pdf[1].getPixmap(alpha = False,colorspace=fitz.csGRAY, matrix=image_matrix)
        pix.writePNG(f"{path}/{i+1}.png")

# _pdfToImages(pdf_1,path_1)
# _pdfToImages(pdf_2,path_2)


input_img = cv2.imread(f"bubble_sheet_293_0_pages/test.png") 

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

 
params = {"left":181,"top":130,"height":15,"width_mcq":86,"width_nmcq":147,"offset":18}

# Function of detect desired regions
def detect_regions(img,params,num_ques):
    # get the image with QR code
    modified_qr,modified_img = detect_qr(img)
    img = draw_rect_qr(modified_qr,modified_img)

    # Detecting Regions 
    offset = 0
    new_img = cv2.medianBlur(img,3)
    new_img = cv2.cvtColor(new_img,cv2.COLOR_BGR2GRAY)
    for i in range(num_ques):
        region = new_img[params["top"]+offset:params["top"]+params["height"]+offset,params["left"]:params["left"]+params["width_nmcq"]]
        circles = cv2.HoughCircles(region,cv2.HOUGH_GRADIENT,1.5,22,param1=300,param2=0.5,minRadius=6,maxRadius=8)
        # print(type(circles))
        if(circles is not None and len(circles[0])==4):
            # highlight circles 
            img = draw_circles(img,circles,params,offset)
            
            img = cv2.rectangle(img,(params["left"],params["top"]+offset),(params["left"]+params["width_mcq"],params["top"]+params["height"]+offset),color=(0,255,0),thickness=1)
        else:
            img = cv2.rectangle(img,(params["left"],params["top"]+offset),(params["left"]+params["width_nmcq"],params["top"]+params["height"]+offset),color=(0,255,0),thickness=1)

        offset+=params["offset"]

    cv2.imshow("frame",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

detect_regions(input_img,params,10)




