# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 18:53:38 2022

@author: PonyWeng
"""

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import math
import base64

def add_zero_to_head(str1):
    if len(str1)!=8:
        zero_should_be_added= 8-len(str1)
        new_str=""
        for i in range(zero_should_be_added):
            new_str+="0"
       
        new_str+=str1
        return new_str
    else:
        return str1
    
#載入偽裝影像

stego_img_filename="stego.png"
stego_img = Image.open(stego_img_filename)

#取得影像尺寸
height, width =stego_img.size

#讀取檔案標頭，得知嵌入的訊息長度
l1=stego_img.getpixel((0,0))
l2=stego_img.getpixel((0,1))

l1_1=(bin(l1)[2:])
l2_1=(bin(l2)[2:])
mark = l1_1[-3:]+l2_1[-3:]

length_of_data_number_of_bits = int(mark,2)

number_of_pixel_should_be_extracted=length_of_data_number_of_bits//3
number_of_bits_are_left=length_of_data_number_of_bits%3

count=-2
extra=""

for i in range(height):
    for j in range(width):
        if count < number_of_pixel_should_be_extracted and count>=0 :
            stego_pixel = stego_img.getpixel((i,j))
            stego_pixel_binary=bin(stego_pixel)[2:]
            stego_pixel_binary=add_zero_to_head(stego_pixel_binary)
            extra+=stego_pixel_binary[-3:]
        elif count==number_of_pixel_should_be_extracted:
            if number_of_bits_are_left==0:
                break
            else:    
                stego_pixel = stego_img.getpixel((i,j))
                stego_pixel_binary=bin(stego_pixel)[2:]
                stego_pixel_binary=add_zero_to_head(stego_pixel_binary)
                extra+=stego_pixel_binary[-number_of_bits_are_left:]
        count+=1

extra_information=mark+extra
length_of_secret=int(extra,2)

# print(len(extra_information))
# print(len(extra_information)%3)


if len(extra_information)%3==0:
    number_of_blcok_to_record_extra_information = len(extra_information) / 3
elif len(extra_information)%3==2:
    number_of_blcok_to_record_extra_information = math.floor(len(extra_information)/3)+1
else:
    number_of_blcok_to_record_extra_information = math.floor(len(extra_information)/3)+1
    
if length_of_secret %3 == 0:
    number_of_pixel_should_be_modified = length_of_secret /3
else:    
    number_of_pixel_should_be_modified= math.floor(length_of_secret/3)+1

## 取出機密訊息
extracted_data=""
final_part_of_secret=length_of_secret-(length_of_secret//3*3)
total_pixl_need_modify = number_of_pixel_should_be_modified+number_of_blcok_to_record_extra_information

##取出資料
count= 0
for i in range(height):
    for j in range(width):
        if count>=total_pixl_need_modify:
            break
        elif count>=number_of_blcok_to_record_extra_information:
            stego_pixel=stego_img.getpixel((i,j))
            
            stego_pixel_in_binary=bin(stego_pixel)[2:]
            
            stego_pixel_in_binary=add_zero_to_head(stego_pixel_in_binary)
            
            if count==total_pixl_need_modify-1 and final_part_of_secret!=0:
                extracted_bits =stego_pixel_in_binary[-final_part_of_secret:]
                extracted_data+=extracted_bits
            else:
                extracted_bits =stego_pixel_in_binary[-3:]
                extracted_data+=extracted_bits
        count+=1


number_of_pixel_should_be_modified= math.ceil(length_of_secret/3)
final_part_of_secret=length_of_secret-length_of_secret//3*3

recover_to_ascii=""
count1=0

for i in extracted_data:
    if count1 % 8 == 0 and count1!=0:
        recover_to_ascii+=" "+i
    else:
        recover_to_ascii+=i
    count1+=1
    
# print(number_of_blcok_to_record_extra_information)
# print(number_of_pixel_should_be_modified)

recover_to_ascii_list=recover_to_ascii.split(" ")
base64code= ""

for i in recover_to_ascii_list:
    ascii_in_decimal=int(i,2)
    plaintext=chr(ascii_in_decimal)
    base64code+=plaintext

base64code=base64code.encode("UTF-8")
base64code = base64.b64decode(base64code)
extracted_plaintext = base64code.decode("UTF-8")






print("提取出來的訊息內容：")
print("-----------------------------------------------------------------------------")
print(extracted_plaintext)
print("-----------------------------------------------------------------------------", end="\n\n")


print("=============================================================================")
print("讀入偽裝影像的檔名為",stego_img_filename,"(確認副檔名是否正確)")
print("secret data的長度(bits)：",length_of_secret ,"bits","(計算方式為轉換成Base64之後的資料長度)") 
print("secret data的容量大小為",length_of_secret/8,"Bytes","-->",length_of_secret/8/1000,"KBytes")
print("該影像的可嵌入容量為",height * width * 3/8/1000, "KBytes")
print("你使用了總容量中的",(length_of_secret)/(height * width * 3)*100,"%")
print("已取出機密訊息，輸出檔名為：extracted_data.txt")
print("=============================================================================")
stego_img.close()

path = 'extracted_data.txt'
with open(path, 'w',encoding="utf-8") as f:
    f.write(extracted_plaintext)
f.close()
    



