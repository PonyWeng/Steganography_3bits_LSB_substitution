# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 18:46:28 2022

@author: PonyWeng
"""

from PIL import Image
# import matplotlib.pyplot as plt
import numpy as np
import math
import base64
from pathlib import Path
import os
import sys


def main():
    cover_image_file_name = sys.argv[1]
    secret_file = sys.argv[2]

    #input
    img_original = Image.open(cover_image_file_name)

    file_type = cover_image_file_name.split(".")[1]
    grayscale_img_filename= "gray_img."+file_type


    #轉成灰階，儲存灰階影像
    img = img_original.convert('L')
    img.save(grayscale_img_filename)

    #複製一份作為待藏入資訊的偽裝影像
    stego_img= img.copy()

    #影像的size
    height, width=img.size


    #收input， secret data
    with open(secret_file, 'r',encoding="utf-8") as f:
        secret_str= f.read()
    # img.show()

    # 取得原始影像大小
    cover_img_file_size =Path(cover_image_file_name).stat().st_size
    gray_img_file_size =Path(grayscale_img_filename).stat().st_size

    ##計算PSNR
    def psnr(target, ref, scale):
        # target:目标图像  ref:参考图像  scale:尺寸大小
        # assume RGB image
        target_data = np.array(target)
        #target_data = target_data[scale:-scale,scale:-scale]
    
        ref_data = np.array(ref)
        #ref_data = ref_data[scale:-scale,scale:-scale]
    
        diff = ref_data - target_data
        diff = diff.flatten('C')
        mse = np.mean((target_data/1.0 - ref_data/1.0) ** 2 )
        #rmse = math.sqrt( np.mean(diff ** 2.) )
        #return 20*math.log10(1.0/rmse)
        return 10 * math.log10(255.0**2/mse)

    ##轉換原始的secret到Base64
    def transform_secret_to_base64(secret_string):
        secret_in_Byte=secret_string.encode("UTF-8")
        secret_in_Base64=base64.b64encode(secret_in_Byte)
        secret_in_Base64=secret_in_Base64.decode("UTF-8")
        return secret_in_Base64
        
    #轉換Base64到ascii
    def transform_base64_to_ascii(secret_in_base64):
        secret_in_ascii=""
        for i in secret_in_Base64:
            secret_in_ascii+=str(ord(i))+" "
            
        return secret_in_ascii

    #讓secret data未滿8位補0
    def add_zero_to_head(str1):
        
        if len(str1)!=8:
            zero_should_be_added= 8-len(str1)
            new_str=""
            for i in range(zero_should_be_added):
                new_str+="0"
            
            new_str+=str1
            return new_str

    #轉換secret為ascii的list
    def trasform_secret_in_ascii_to_list(secret_in_ascii):
        secret_in_ascii_list=[]
        secret_in_ascii_list=secret_in_ascii.split(" ")
        
        secret_in_ascii_list.pop()
        return secret_in_ascii_list

    #轉換ascii list 為binary
    def trasform_secret_in_ascii_list_to_binary(secret_in_ascii_list):
        secret_in_ascii_binary=[]
        for i in secret_in_ascii_list:
            secret_in_ascii_binary.append(bin(int(i))[2:])
    
        return secret_in_ascii_binary


    #資料標頭，前六位會顯示總secret的長度需要用多少位元
    #藏入資料的mark 紀錄我們要保留多少個位置bits來藏額外資訊
    def add_zero_to_head_6bits(str1):    
        if len(str1)!=6:
            zero_should_be_added= 6-len(str1)
            new_str=""
            for i in range(zero_should_be_added):
                new_str+="0"
            new_str+=str1
            return new_str
        else:
            return str1
        
    def generate_length_data_mark(length_of_secret):
        length_should_be_recorded = math.floor(math.log(length_of_secret,2))+1
        length_data =  bin(length_should_be_recorded)[2:]
        length_data_mark = add_zero_to_head_6bits(length_data)
        return length_data_mark


    #收input， secret data
    secret_file = 'secret.txt'

    with open(secret_file, 'r',encoding="utf-8") as f:
        secret_str= f.read()

    secret_in_ascii_list=[]
    secret_in_ascii_binary=[]
    secret_in_Base64 = transform_secret_to_base64(secret_str)
    secret_in_ascii  = transform_base64_to_ascii(secret_in_Base64)
    secret_in_ascii_list = trasform_secret_in_ascii_to_list(secret_in_ascii)
    secret_in_ascii_binary= trasform_secret_in_ascii_list_to_binary(secret_in_ascii_list)

    #完整的secret
    secret_str_complete=""

    #add_zero_to_head，當secret不滿8位時，開頭會自動補0
    for i in secret_in_ascii_binary:
        secret_str_complete+=add_zero_to_head(i)
        
    #計算secret長度
    length_of_secret=len(secret_str_complete)

    EC= height * width *3

    if length_of_secret>EC:
        try:
            print("Secret Data長度(bits)：",length_of_secret ,"bits")
            print("Secret Data容量(bytes):",length_of_secret/8,"Bytes")
            print('secret的大小超過可嵌入的容量，請重新輸入secret')
            os._exit(0) 
        except:
            print('os.exit')


    # 額外的標頭訊息處理=========================================
    length_data_mark= generate_length_data_mark(length_of_secret)
    length_data = bin(length_of_secret)[2:]
    extra_information= length_data_mark+length_data

    number_of_blcok_to_record_extra_information = math.ceil(len(extra_information)/3)
    length_of_extra_information = len(extra_information)


    extra_information_list=[]
    for i in range(0,length_of_extra_information,3):
        extra_information_list.append(extra_information[i:i+3])
        
    count=0
    for i in range(height):
        for j in range(width):
            if count>=number_of_blcok_to_record_extra_information:
                break
            else:
                cover_pixel=img.getpixel((i,j))
                stego_pixel=(cover_pixel>>3<<3)+int(extra_information_list[count],2)
                stego_img.putpixel((i,j),stego_pixel)
                count+=1
    # 額外訊息處理結束=========================================

    # 主要的機密訊息藏匿部分

    #secret_list 切成三個bits一組
    secret_list=[]
    for i in range(0,length_of_secret,3):
        secret_list.append(secret_str_complete[i:i+3])

    number_of_pixel_should_be_modified=len(secret_list)
    
    print("機密訊息的內容：")
    print("-------------------------------------------------------")
    print(secret_str)
    print("-------------------------------------------------------", end="\n\n")

    print("其他資訊：")
    print("=======================================================")
    print("原始影像的檔案大小：",float(cover_img_file_size),"Bytes", "-->" ,cover_img_file_size/1000,"KBytes") 
    print("灰階影像的檔案大小：",float(gray_img_file_size),"Bytes", "-->" ,gray_img_file_size/1000,"KBytes") 
    print("可用的藏入資訊容量：",EC/8,"Bytes" , "-->", EC/8/1000,"KBytes")
    print("=======================================================")
    print()
    print("機密訊息資訊：")
    print("=======================================================")
    #主要藏匿的步驟 3bits LSB
    count= 0
    count_secret_list=0
    for i in range(height):
        for j in range(width):
            if count>=number_of_pixel_should_be_modified+number_of_blcok_to_record_extra_information:
                break
            elif count>=number_of_blcok_to_record_extra_information:
                cover_pixel=img.getpixel((i,j))
                stego_pixel=(cover_pixel>>3<<3)+int(secret_list[count_secret_list],2)
                
                stego_img.putpixel((i,j),stego_pixel)
                count_secret_list+=1
            count+=1

    print("Secret Data的長度(bits)：",length_of_secret ,"bits","; 容量大小為",length_of_secret/8,"Bytes","(以轉換Base64後的長度計算)")
    print("與原始圖片計算峰值訊噪比 PSNR (越高代表越接近原始圖片，PSNR>30 為可接受範圍):")
    print("PSNR=",psnr(img,stego_img,512))
    print("=======================================================")




    if file_type =="jpg" or file_type=="jpeg":
        output_type = "png"    
    else:
        output_type =file_type

    stego_file_name= "stego."+output_type
    stego_img.save(stego_file_name)
    print("藏入訊息完成，輸出圖片：",stego_file_name,"。")
    stego_img_file_size =Path(stego_file_name).stat().st_size



    print("=======================================================")
    print("偽裝影像的檔案大小：",float(stego_img_file_size),"Bytes", "-->" ,stego_img_file_size/1000,"KBytes","(灰階影像)")
    print("=======================================================")

if __name__ == "__main__":
    main()