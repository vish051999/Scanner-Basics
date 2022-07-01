import json
import fitz
import cv2
import random
from src.utils import detect_qr,draw_rect_qr,draw_circles


def split_pdf(event,context):
    req_body = json.loads(event["body"])
    source_path = req_body["source_path"]
    dest_path = req_body["dest_path"]

    pdf = fitz.open(source_path)
    num_pages = pdf.pageCount
    # print(num_pages)
    image_matrix = fitz.Matrix(fitz.Identity)
    # image_matrix.preScale(1, 1)
    for i in range(num_pages):
        pix = pdf[i].getPixmap(alpha = False,colorspace=fitz.csGRAY, matrix=image_matrix)
        pix.writePNG(f"{dest_path}/{i+1}.png")
    return {"statusCode":200,"body":json.dumps({"message":"Success","output_path":f"/{dest_path}"})}


def detect_regions(event,context):
    req_body = json.loads(event["body"])
    img_path = req_body["img_path"]
    num_ques = req_body["num_ques"]
    
    img = cv2.imread(img_path)

    params = {"left":181,"top":129,"height":16,"width_mcq":87,"width_nmcq":147,"offset":18}

    # get the image with QR code
    qr,modified_img = detect_qr(img = img)
    img = draw_rect_qr(qr = qr,img = modified_img)

    # Detecting Regions 
    offset = 0
    new_img = cv2.medianBlur(img,ksize=3)
    new_img = cv2.cvtColor(new_img,cv2.COLOR_BGR2GRAY)
    for i in range(num_ques):
        region = new_img[params["top"]+offset:params["top"]+params["height"]+offset,params["left"]:params["left"]+params["width_nmcq"]]
        circles = cv2.HoughCircles(region,cv2.HOUGH_GRADIENT,dp=1.5,minDist=22,param1=300,param2=0.5,minRadius=6,maxRadius=8)
        # print(type(circles))
        if(circles is not None and len(circles[0])==4):
            # highlight circles 
            img = draw_circles(img = img,circles = circles,params = params,offset = offset)
            
            img = cv2.rectangle(img=img,pt1=(params["left"],params["top"]+offset),pt2=(params["left"]+params["width_mcq"],params["top"]+params["height"]+offset),color=(0,255,0),thickness=1)
        else:
            img = cv2.rectangle(img=img,pt1=(params["left"],params["top"]+offset),pt2=(params["left"]+params["width_nmcq"],params["top"]+params["height"]+offset),color=(0,255,0),thickness=1)

        offset+=params["offset"]
    
    # img_num = random.randint(1,50)

    output_path = f"results/output.png"
    cv2.imwrite(output_path,img)

    return {"statusCode":200,"body":json.dumps({"message":"Success","ouput_path":f"/{output_path}"})}