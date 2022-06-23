def draw_circles_2(img,circles,params,offset):
    circles = np.uint16(np.around(circles))
    to_add = 23
    x_offset = 0
    for i in range(4):
        img = cv2.circle(img,(circles[0][0][0]+params["left"]+x_offset,circles[0][0][1]+params["top"]+offset),8,(255,0,0),1)
        x_offset = x_offset + to_add
    return img