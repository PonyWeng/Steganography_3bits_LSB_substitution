# Steganography_3bits_LSB_substitution

## Introduction
Given the Embedding.py and Extraction.py, you can put your secret data into secret.txt, then embed it into your own image.
At the receiver side, they can use extraction.py to extract the secret data that you already embedded in the stego-image, finally, the extracted.txt will be the output.

It should be noticed that the "colour image" will be converted into "grayscale" in this program. Then, it will output the "stego-image" in grayscale.

---

## **Steganography for NCU電腦攻擊與防禦 Project2**

**組員：**
* 翁浩宇111522091
* 洪仁傑111522119
* 楊淑君111522120

---

Before running this program, please CHECK your python environment has been installed the following packages and librarys.

* PILLOW
* numpy
* math
* base64
* pathlib
* os

---

## How to hide your secret in the image?

* **Step1.**  Put the "embedding.py", "your own image" and the "secret.txt" in the same directory.
* **Step2.**  Open the embedding.py, then edit the variable "cover_image_file_name" to your own image name.
* **Step3.**  Open secret.txt, then input your data into it.
* **Step4.**  Execute the program embedding.py, then you will get a stego-image with your secret data has already embedded in it.

It can be noticed that your stego-image and cover-image are almost the same and you cannot use your eyes to detect or found if it has hidden some secret or not.
This is the goal of "Steganography".

## How to extract the secret data from the stego-image?

* **Step1.**  Put the "extraction.py", "stego-image" in the same directory.
* **Step2.**  Open the extraction.py, then edit the variable "stego_img_filename" to your own stego-image name.
* **Step3.**  Execute the program extraction.py, then you will get the extracted.txt and your secret data can be extracted in this file. 
