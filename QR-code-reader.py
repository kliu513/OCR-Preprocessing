import os
import requests 
from io import BytesIO
from pyzbar import pyzbar
from PIL import Image, ImageEnhance  

def get_qrcode(img_path):    
    """ 
    Read QR code
    img_path：path to an image of QR code
    """          
    img = Image.open(img_path)    
    img = ImageEnhance.Color(img).enhance(2.0)   
    img.show()     
    txt = pyzbar.decode(img)
    for elem in txt:     
        code_data = elem.data.decode('utf-8').split(',')
        print(code_data)
    return code_data

def write_xml(code_data):
    """
    Write code data to a .xml file
    code_data: a list of code data
    """
    f = open('invoice_info.xml', 'w', encoding='utf-8')
    f.write("<?xml encoding='utf-8'?>\n")
    f.write("<invoice>\n")
    f.write("\t<type>" + code_data[1] + "</type>\n")
    f.write("\t<invoiceCode>" + code_data[2] + "</invoiceCode>\n")
    f.write("\t<invoiceNo.>" + code_data[3] + "</invoiceNo.>\n")
    f.write("\t<value>" + code_data[4] + "</value>\n")
    f.write("\t<date>" + code_data[5] + "</date>\n")
    f.write("\t<checkCode>" + code_data[6] + "</checkCode>\n")
    f.write("</invoice>")
    f.close()

if __name__ == '__main__':    
    code_data = get_qrcode('sample.png') # add an image path here
    write_xml(code_data)
