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
* sys

---

## How to hide your secret in the image?

* **Step1.**  Put the "Embedding.py", "{XXX.bmp/png/jpg} (Your own image)" and the "secret.txt" in the same directory.
* **Step2.**  Open secret.txt and input the data that you want to embed into image.
* **Step3.**  Execute ``` python Embedding.py XXX.bmp secret.txt ```   <-- Two arugments includes the image and secret.txt
* **Step4.**  Finally, you will get a "stego.bmp" and "gray_img.bmp" in the same directory, and the secret has already embedded into the "stego.bmp".
* **Step5.**  In the program, you can read some detail information of your image, the sizes, secret.data. PSNR value ..., etc.

It can be noticed that your stego-image and cover-image are almost the same and you cannot use your eyes to detect or found if it has hidden some secret or not.
This is the goal of "Steganography".

## How to extract the secret data from the stego-image?

* **Step1.**  Put the "Extraction.py", "{stego-image}.bmp/png" in the same directory.
* **Step2.**  Execute ``` python Extraction.py stego.bmp ```  <-- An arugment included, it is the stego-image.
* **Step3.**  Finally, you will get an "extracted.txt" as your secret are shown in this file, and then some information will be listed.
