import cv2
import numpy as np
import pandas as pd
import argparse

def read_csv(csvf):
    """
    Read csv file with pandas. Name columns "color","color_name","hex","R","G","B"
    csvf: csv file name
    return: pandas object holding csv content of various colors
    """
    col_names=["color","color_name","hex","R","G","B"]
    csv = pd.read_csv(csvf, names=col_names, header=None)
    return csv

def getColorName(R,G,B, csv):
    """
    calculate minimum distance from all colors and get the most matching color betwin the color in chosen point to colors in csv file.
    R,G,B: RGB in clicked point on image
    csv: pandas object holding csv content of various colors
    return: color name of the most matching color
    """
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

def draw_function(event, x,y,flags,param):
    """
    get x,y coordinates of mouse double click
    """
    if event == cv2.EVENT_LBUTTONDBLCLK: #verify the event is a double click
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x] #the value of the image in this point (=RGB in point)
        b = int(b)
        g = int(g)
        r = int(r)


if __name__ == "__main__":
    #argument parser to take image path from command line: python color_detect.py -i img.jpg
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', required=True, help="Image Path")
    args = vars(ap.parse_args())
    img_path = args['image']

    #Read the image with opencv
    img = cv2.imread(img_path)
    #read the CSV file into a pandas structure
    csv = read_csv('colors.csv')

    #global parameters
    clicked = False
    r = g = b = xpos = ypos = 0

    cv2.namedWindow('image') #title of window
    cv2.setMouseCallback('image',draw_function)

    while(1):
        cv2.imshow("image",img)
        if (clicked):
            cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)

            #Text string to display( Color name and RGB values )
            text = getColorName(r,g,b, csv) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
            
            #Display text in white (over darker colors)
            cv2.putText(img, text,(50,50),2,0.8,(255,255,255),1,cv2.LINE_AA)

            #Display text in black (over lighter colors)
            if(r+g+b>=600):
                cv2.putText(img, text,(50,50),2,0.8,(0,0,0),1,cv2.LINE_AA)
                
            clicked=False

        #Break the loop when user hits 'esc' key    
        if cv2.waitKey(20) & 0xFF ==27:
            break
        # Check if the window is closed by the user (clicking the "X" button)
        if cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) < 1:
            break
        
    cv2.destroyAllWindows()
