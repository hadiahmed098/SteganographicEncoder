# SteganographicEncoder
Program to steganographically encode a txt file into a png file. New image can also be decoded to retrieve the original message.

# Methodology
Uses Least Significant Bit (LSB) encoding. Since an image is made up of pixels, each made up of 3 sub-pixel color channels, each pixel can store 3 bits of information.
Color is stored as an 8 bit number, so changing the LSB will not make a noticable difference to the encoded image visually. A program could see the difference, however it must have the original file to compare against.
Using this method, each byte of a text file can be turned into 8 bits and encoded into an image.

# Roadmap
Project can currently save and read an encoded image. Currently, I am working on adding a commandline and gui interface.
