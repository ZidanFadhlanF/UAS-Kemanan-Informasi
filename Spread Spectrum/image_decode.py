import cv2
from cryptography.fernet import Fernet

def decode(image_path):
    image = cv2.imread(image_path)
    bank_secret_message = ""

    for row in image:
        for pixel in row:
            r, g, b = [format(i, "08b") for i in pixel]
            bank_secret_message += r[-1]
            bank_secret_message += g[-1]
            bank_secret_message += b[-1]

    all_data_secret_message = [bank_secret_message[i: i+8] for i in range(0, len(bank_secret_message), 8)]
    decoded_secret_message = ""

    for byte in all_data_secret_message:
        decoded_secret_message += chr(int(byte, 2))

    secret_message = decoded_secret_message.split("SdfD1")[1]
    split_1 = secret_message.split("e1g0l")[1][:-5]
    split_2 = secret_message.split("e1g0l")[0]

    decoded = Fernet(split_1).decrypt(split_2.encode())
    return decoded.decode()
