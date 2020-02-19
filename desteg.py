import cv2
import binascii as bas
import argparse
import os.path

# Function will take an image file and return the color bytes of each pixel in a 1D array
# input: image file name
# output: 1xN numpy array
def load_image_bytes(file_name):
    image_bytes = cv2.imread(file_name, cv2.IMREAD_COLOR)
    return image_bytes.flatten()

# Function will take image bytes and return the bits from the least significan bit of each byte
# input: np array of image pixel bytes
# output: list of strings where each string is a single bit
def decode_from_bytes(image_bytes):
    text_bits = []
    for byte in image_bytes:
        # Turn the byte into a binary string and index only the last bit
        text_bits.append(bin(int(byte))[len(bin(int(byte)))-1])
    return text_bits

# Function will take an array of bits and turn it into an array of bytes using a string join
# input: list of strings where each string is a single bit
# output: list of strings where each string is a single byte
def bits_to_bytes(text_bits):
    text_bytes = []
    pointer = 0  # Used to point to where each byte starts
    while pointer < len(text_bits):
        # Joins each bit with an empty string in between, effectively converting every 8 bits to a byte
        text_bytes.append(''.join(text_bits[pointer:pointer+8]))
        pointer += 8
    return text_bytes

# Function will take a list of text bytes and convert them to binary ascii strings. These strings are then
#   written to a file
# input: byte list, filename
def save_text(text_bytes, filename):
    hex_bytes = []
    for byte in text_bytes:
        # Turns each byte into a decimal number, then to a hex number
        # Chops off the first 2 characters (0x) and verifies a length of 2
        hex_bytes.append(hex(int(byte, 2))[2:].zfill(2))

    output_bytes = []
    for hex_b in hex_bytes:
        output_bytes.append(bas.unhexlify(hex_b))

    with open(filename, 'wb') as file:
        file.writelines(output_bytes)

def main():
    try:
        # Error checking on files
        if not os.path.isfile(args.input):
            raise FileNotFoundError("input file must exist and be a valid file")
        elif args.input.split('.')[1] != 'png':
            raise ValueError("input file must be a .png")

        if args.output.split('.')[1] != 'txt':
            raise ValueError("output file must be a .txt")

        i_bytes = load_image_bytes(args.input)
        t_bits = decode_from_bytes(i_bytes)

        t_bytes = bits_to_bytes(t_bits)
        save_text(t_bytes, args.output)
    except Exception as e:
        print('%s: %s' % (type(e).__name__, e))

# Setup commandline parser
parser = argparse.ArgumentParser(description='Decode an image using steganography', allow_abbrev=True,
                                 usage='desteg.py [-h] <inputfile> '
                                       '[-output <outputfile>]')

# Add commandline arguments
parser.add_argument('input', help="image input file, .png")
parser.add_argument('-output', default='message_decoded.txt', help='message output file, .txt')

args = parser.parse_args()

# Establish main method
if __name__ == '__main__':
    main()
