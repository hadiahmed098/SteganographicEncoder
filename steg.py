import cv2
import numpy as np

# Function will take an image file and return the color bytes of each pixel in a 1D array
# input: image file name
# output: 1xN numpy array, tupple with image dimensions
def load_image_bytes(file_name):
    image_bytes = cv2.imread(file_name, cv2.IMREAD_COLOR)
    return image_bytes.flatten(), image_bytes.shape

# Function will take a text file and return a string with bytes of the text
# input: text file name
# output: byte string of the text file
def load_text_bytes(file_name):
    with open(file_name, 'rb') as f:
        text_bytes = f.read()
    return text_bytes

# Function will take the text bytes and convert them into bits
# input: byte string with the text
# output: bit array
def bytes_to_bits(text_bytes):
    bits = []
    for byte in text_bytes:
        bits.append(bin(byte)[2:].zfill(8))
    return bits

# Function will take bits of a text file and bytes of an image file and use LSB encoding
# input: image bytes, text bits
# output: bytes of new image
def encode_bits_in_bytes(image_bytes, text_bits):
    # Error checking to avoid any out-of-bound errors before encoding
    if len(ibytes) < len(tbits) * 8:
        raise IndexError("size of image file is larger than size of image")

    output_bytes = []
    byte_counter = 0
    for bits in text_bits:
        for bit in bits:
            output_bytes.append((image_bytes[byte_counter] & 254) | int(bit))
            byte_counter += 1

    output_bytes = np.concatenate((np.asarray(output_bytes), image_bytes[byte_counter:]))
    return output_bytes

# Function will take bytes of an image and convert them into an image
# input: image bytes in numpy array, output image name, dimensions of the image
def save_image_bytes(image_bytes, output_file_name, image_dim):
    image_reshape = image_bytes.reshape(image_dim)
    cv2.imwrite(output_file_name, image_reshape)

tbits = bytes_to_bits(load_text_bytes('message.txt'))
(ibytes, size) = load_image_bytes('donut.png')

obytes = encode_bits_in_bytes(ibytes, tbits)
save_image_bytes(np.asarray(obytes), 'test.png', size)
