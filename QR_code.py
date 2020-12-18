import os
import requests 
from io import BytesIO
from pyzbar import pyzbar
from PIL import Image, ImageEnhance  

def get_ewm(img_path):    
    """ 
    读取二维码的内容
    img_path：二维码地址（可本地可网络） 
    """    
    if os.path.isfile(img_path):
        #从本地加载二维码图片        
        img = Image.open(img_path)    
    else:        
        #从网络下载并加载二维码图片        
        qr_img = requests.get(img_path).content        
        img = Image.open(BytesIO(qr_img))
    img = ImageEnhance.Color(img).enhance(2.0)   
    img.show()     
    txt = pyzbar.decode(img)
    for elem in txt:     
        code_data = elem.data.decode('utf-8').split(',')
        print(code_data)
    return code_data

def write_xml(code_data):
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
    code_data = get_ewm('sample.png')
    write_xml(code_data)