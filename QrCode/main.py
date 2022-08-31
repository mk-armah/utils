import pandas as pd
import argparse
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
import os
import qrcode
import numpy as np
import cv2



def make_qr(text:str,embedded_image_path:str | None = None):
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

    qr_img = qr_img.convert("RGB")

    pos = ((outer_frame.size[0] - qr_img.size[0]) // 2, (outer_frame.size[1] - qr_img.size[1]) // 2)
    
    outer_frame.paste(qr_img, pos)
    
    return outer_frame





if __name__ == "__main__":
    
    def tuple_type(strings):
        strings = strings.replace("(", "").replace(")", "")
        mapped_int = map(int, strings.split(","))
        return tuple(mapped_int)

    
    parser = argparse.ArgumentParser(description = 'Generate QR Codes Via the Command Line')

    parser.add_argument('--outer_image','-o', type=str,default = "./designs/qr-code-frame6.png",
                    help='an image for the qrcode outermost design | specify full path to the image')
    
    parser.add_argument('--enc_ratio','-r',default= 1.82, type = int,
                        help='size ratio of the enclosure to code | Optional')
    
    parser.add_argument('--inner_image','-i',default= "./designs/embedded_logo.png",type = str,help='an optional embedding image for the inner part of the QrCode')

    parser.add_argument('--embedding','-e',type = str,help = 'document to embedding',default = 'github.com/mk-armah')

    parser.add_argument('--filedir','-f',default= "./samples",type = str,
                        help='provided directory to save png image | Optional')

    parser.add_argument('--qrcode_name','-n',default= "/mk-codes",type = str,
                        help='Name of the qrcode image | Optional')

    parser.add_argument('--size','-s',default = (512,512),type = tuple_type,help = "Size of the qrcode image")


    args = parser.parse_args()

    img = make_qr(text = args.embedding,embedded_image_path = args.inner_image)
        
    img = add_enclosure(img,enc_img_path = args.outer_image,ratio = 1.82) 

    img = img.resize(args.size,resample= Image.Resampling.NEAREST)

    img.save(fp = r"{filedir}{qrcode_name}.png".format(filedir = args.filedir,qrcode_name = args.qrcode_name),format = 'png')

    img.show()