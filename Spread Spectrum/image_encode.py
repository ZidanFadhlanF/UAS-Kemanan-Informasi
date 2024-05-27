import cv2
import os
from cryptography.fernet import Fernet
import sys

def encode(image_path, secret_data, new_image_path):
    image = cv2.imread(image_path)
    max_bytes = (image.shape[0] * image.shape[1]) // 8

    key = Fernet.generate_key()
    f = Fernet(key)
    secret_data = f.encrypt(secret_data.encode())
    secret_data = str(secret_data.decode()) + "e1g0l"
    secret_data = "SdfD1" + secret_data + str(key.decode())
    secret_data = secret_data + "m1Ku1"

    if len(secret_data) > max_bytes:
        raise ValueError("Secret message is too big for the carrier")

    size_of_message = sys.getsizeof(secret_data)
    length_message = max_bytes // size_of_message
    new_secret_data = secret_data * length_message

    bank_secret_message = 0
    b_secret_message = ''.join([format(ord(i), "08b") for i in new_secret_data])
    len_secret_message = len(b_secret_message)

    for row in image:
        for pixel in row:
            r, g, b = [format(i, "08b") for i in pixel]
            if bank_secret_message < len_secret_message:
                pixel[0] = int(r[:-1] + b_secret_message[bank_secret_message], 2)
                bank_secret_message += 1
            if bank_secret_message < len_secret_message:
                pixel[1] = int(g[:-1] + b_secret_message[bank_secret_message], 2)
                bank_secret_message += 1
            if bank_secret_message < len_secret_message:
                pixel[2] = int(b[:-1] + b_secret_message[bank_secret_message], 2)
                bank_secret_message += 1
            if bank_secret_message >= len_secret_message:
                break

    cv2.imwrite(new_image_path, image)
