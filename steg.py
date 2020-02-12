import cv2

def load_image_bytes(file_name):
    image_bytes = cv2.imread(file_name, cv2.IMREAD_COLOR)
    return image_bytes.flatten()

def load_text_bytes(file_name):
    text_bytes = open(file_name, 'rb')
    int_bytes = []
    for (i,b) in enumerate(text_bytes):
        int_bytes[i] = int.from_bytes(b, "big")
    return int_bytes

def save_image_bytes(image_bytes, text_bytes, output_file_name):
    return
