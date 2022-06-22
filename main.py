import fitz
import cv2
from pyzbar.pyzbar import decode

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


img = cv2.imread("bubble_sheet_293_0_pages/test.png") 

def detect_qr(img):
    qr = decode(img)
    # print(qr[0][4])
    modified_img = img
    if(qr[0][4]==1):
        modified_img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif(qr[0][4]==2):
        modified_img = cv2.rotate(img, cv2.ROTATE_180)
    elif(qr[0][4]==3):
        modified_img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    modified_qr = decode(modified_img)
    return modified_qr,modified_img

modified_qr,modified_img = detect_qr(img)
# print(decode(modified_img))


def draw_rect_qr(qr,img):
    start = (qr[0][2][0],qr[0][2][1])
    end = (qr[0][2][0]+qr[0][2][2],qr[0][2][1]+qr[0][2][3])
    color = (255,0,0)
    thickness = 5

    qr_img = cv2.rectangle(img,start,end,color,thickness)
    cv2.imshow("frame",qr_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows("q")

draw_rect_qr(modified_qr,modified_img)