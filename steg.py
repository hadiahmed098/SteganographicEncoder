import cv2
import numpy as np
import argparse
import os.path

# Function will take an image file and return the color bytes of each pixel in a 1D array
# input: image file name
# output: 1xN numpy array, tuple with image dimensions
def load_image_bytes(file_name):
    image_bytes = cv2.imread(file_name, cv2.IMREAD_COLOR)
    return image_bytes.flatten(), image_bytes.shape


# Function will take a text file and return a string with bytes of the text
# input: text file name
# output: byte string of the text file with padding
def load_text_bytes(file_name, bytes_length):

    with open(file_name, 'rb') as f:
        text_bytes = f.read()

    padding_bytes = b''

    # Pad text_bytes so no random noise is encoded into the image
    while len(padding_bytes) < (bytes_length - (len(text_bytes) * 8)) / 8:
        padding_bytes += b' '
    text_bytes += padding_bytes

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
def encode_bits_in_bytes(image_bytes, text_bits, bits_number):
    # Error checking to avoid any out-of-bound errors before encoding
    if len(image_bytes) < len(text_bits) * 8:  # TODO modify check to account for bits_number
        raise IndexError(f"size of image file ({len(image_bytes)}) is smaller than size of message ({len(text_bits) * 8})")

    output_bytes = []
    byte_counter = 0
    for bits in text_bits:
        print('2')
    # TODO modify for loops to account for each image byte having more than one encoded bit
    # (((254 << i) & 255) + (2**i) - 1) will shift the open bit spot to the ith spot
    for bit in bits:
        for i in range(bits_number):
            output_bytes.append((image_bytes[byte_counter] & (((254 << i) & 255) + (2**i) - 1) | int(bit)))
        byte_counter += 1

    output_bytes = np.concatenate((np.asarray(output_bytes), image_bytes[byte_counter:]))
    return output_bytes


# Function will take bytes of an image and convert them into an image
# input: image bytes in numpy array, output image name, dimensions of the image
def save_image_bytes(image_bytes, output_file_name, image_dim):
    image_reshape = image_bytes.reshape(image_dim)
    cv2.imwrite(output_file_name, image_reshape)

def main():
    try:
        # Error checking on files
        if not os.path.isfile(args.input):
            raise FileNotFoundError("input file must exist and be a valid file")
        elif args.input.split('.')[1] != 'png':
            raise ValueError("input file must be a .png")

        if not os.path.isfile(args.message):
            raise FileNotFoundError("message file must exist and be a valid file")
        elif args.message.split('.')[1] != 'txt':
            raise ValueError("message file must be a .txt")

        if args.output.split('.')[1] != 'png':
            raise FileNotFoundError("output file must be a .png")

        (i_bytes, size) = load_image_bytes(args.input)
        t_bits = bytes_to_bits(load_text_bytes(args.message, size[0] * size[1] * size[2]))

        o_bytes = encode_bits_in_bytes(i_bytes, t_bits, args.bitsnumber)
        save_image_bytes(np.asarray(o_bytes), args.output, size)
    except Exception as e:
        print('%s: %s' % (type(e).__name__, e))

# Setup commandline parser
parser = argparse.ArgumentParser(description='Encode an image using steganography', allow_abbrev=True,
                                 usage='steg.py [-h] <numberofbits (1-7)> <inputfilename> <messagefilename> '
                                       '[-output <outputfile>] ')

# Add commandline arguments
parser.add_argument('bitsnumber', help="the number of bits used to encode", type=int, choices=range(1, 8))
parser.add_argument('input', help="image input file, .png")
parser.add_argument('message', help='message input file, .txt')
parser.add_argument('-output', default='message_encoded.png', help='image output file, .png')

args = parser.parse_args()

# Establish main method
if __name__ == '__main__':
    main()
