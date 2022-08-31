import pandas as pd
import argparse
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
import os
import qrcode
import numpy as np
import matplotlib.pyplot as plt
import cv2



def make_qr(text,embedded_image_path:str | None = None):
    qr = qrcode.QRCode(version= 15)
    
    qr.add_data(text)
    
    if embedded_image_path is not None:
        img = qr.make_image(image_factory=StyledPilImage, embeded_image_path=embedded_image_path)
    else:
        img = qr.make_image()

    return img


def show_image(img):
    """Display image with Open cv
    Args:
        img : the image to display
    Return:
        None, just a image frame will be displayed to the screen"""

    cv2.imshow("image",cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    
    cv2.waitKey(0)
    
    cv2.destroyAllWindows()


def add_enclosure(qr_img, enc_img_path:str, ratio:float = 1.8):
    """"
    Enclose Generated QR-code image in a frame.

    Args :
              ratio -> int|float, default is 1.8, increases the size of the frame 1.8 times the 
              embedded image size

        Returns :
                PILImage, a qrcode image enclosed in a frame.
    """

    outer_frame = Image.open(enc_img_path).resize(
        (np.array(img.size)*ratio).astype(int)
        )

    outer_frame = outer_frame.convert("RGB")

    # size = (np.array(img.size)*2.2).astype(int)
    # print(size)

    qr_img = qr_img.convert("RGB")

    pos = ((outer_frame.size[0] - qr_img.size[0]) // 2, (outer_frame.size[1] - qr_img.size[1]) // 2)
    
    outer_frame.paste(qr_img, pos)
    
    return outer_frame





if __name__ == "__main__":
    # df = pd.read_excel("C:\\Users\\User\\Desktop\\newlinks.xlsx")
    # print(df.head()) 

    # for i in range(len(df)):

    #     img = make_qr(text = df["LINK"][i],embedded_image_path = "C:/Users/User/Desktop/embedded_logo.png")
        
    #     img = add_enclosure(img,enc_img_path = "C:/Users/User/Desktop/qr-code-frame6.png",ratio = 1.82)
        
    #     img.resize((800,800),resample= Image.Resampling.NEAREST)
    
    #     img = np.array(img)

    #     cv2.putText(img = img, text= df["PROGRAM"][i], org=(270, 120),fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(100, 55, 100),thickness=2)
        
    #     img = Image.fromarray(img)

    #     img.save(fp = r"C:/Users/User/Desktop/e-learning-codes/{}.png".format(df["PROGRAM"][i]),format = 'png')

    img = make_qr(text = "https://drive.google.com/file/d/16yEDItTCPUPWdJbwOWeimayxNzTmrN8b/view?usp=sharing",embedded_image_path = "D:/Users/mk-armah/OneDrive/Documents/embedded_logo.png")
        
    img = add_enclosure(img,enc_img_path = "D:/Users/mk-armah/OneDrive/Documents/qr-code-frame6.png",ratio = 1.82) 
    img.resize((800,800),resample= Image.Resampling.NEAREST)
    img.save(fp = r"./{}.png".format("pdf_document"),format = 'png')
    
        
    img.show()
    
    # img = make_qr("https://drive.google.com/file/d/16yEDItTCPUPWdJbwOWeimayxNzTmrN8b/view?usp=sharing")
    
    
    # img.show()