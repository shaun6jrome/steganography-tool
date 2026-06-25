import numpy as np
from PIL import Image

def decode_image(image_file):
    """
    Decodes a hidden message from an image using LSB steganography.
    """
    delimiter = "====="
    delimiter_bytes = delimiter.encode('latin1')
    
    # Read the image and convert to RGB
    img = Image.open(image_file)
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    img_array = np.array(img)
    flat_array = img_array.flatten()
    
    # Extract the least significant bit from each color channel
    extracted_bits = flat_array & 1
    
    # Ensure the length of the bits array is a multiple of 8
    valid_bits_length = (len(extracted_bits) // 8) * 8
    extracted_bits = extracted_bits[:valid_bits_length]
    
    # Pack the extracted bits into bytes
    # np.packbits treats the first bit as the Most Significant Bit (MSB), 
    # which matches our encoding format(ord(char), "08b")
    bytes_array = np.packbits(extracted_bits)
    byte_string = bytes_array.tobytes()
    
    # Find the delimiter to know where the message ends
    delimiter_index = byte_string.find(delimiter_bytes)
    
    if delimiter_index != -1:
        message_bytes = byte_string[:delimiter_index]
        # Decode the bytes back to a string
        return message_bytes.decode('latin1')
    else:
        raise ValueError("No hidden message found, or the image is corrupted.")
