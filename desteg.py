import cv2
import binascii as bas

# Function will take an image file and return the color bytes of each pixel in a 1D array
# input: image file name
# output: 1xN numpy array, tupple with image dimensions
def load_image_bytes(file_name):
    image_bytes = cv2.imread(file_name, cv2.IMREAD_COLOR)
    return image_bytes.flatten(), image_bytes.shape

def decode_from_bytes(image_bytes):
    text_bits = []
    for byte in image_bytes:
        text_bits.append(bin(int(byte))[len(bin(int(byte)))-1])
    return text_bits

def bits_to_bytes(text_bits):
    text_bytes = []
    pointer = 0;
    while pointer < len(text_bits):
        text_bytes.append(''.join(map(str, text_bits[pointer:pointer+8])))
        pointer += 8
    return text_bytes

def save_text(text_bytes, filename):
    hex_bytes = []
    for byte in text_bytes:
        hex_bytes.append(hex(int(byte, 2))[2:].zfill(2))

    output_bytes = []
    for hex_b in hex_bytes:
        output_bytes.append(bas.unhexlify(hex_b))

    file = open(filename, 'wb')
    file.writelines(output_bytes)
    file.close()

(ibytes, size) = load_image_bytes('test.png')
tbits = decode_from_bytes(ibytes)

tbytes = bits_to_bytes(tbits)
save_text(tbytes, 'test.txt')
