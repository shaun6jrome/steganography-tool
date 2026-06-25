import numpy as np
from PIL import Image
import io

def message_to_binary(message):
    """
    Converts a string message into a binary string representation.
    """
    return ''.join([format(ord(char), "08b") for char in message])

def encode_image(image_file, secret_message):
    """
    Encodes a secret message into an image using LSB steganography.
    Returns a BytesIO object containing the encoded PNG image.
    """
    # Append a delimiter to indicate the end of the message during decoding
    delimiter = "====="
    secret_message += delimiter
    
    binary_message = message_to_binary(secret_message)
    message_len = len(binary_message)
    
    # Read the image and ensure it is in RGB format for consistent processing
    img = Image.open(image_file)
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    img_array = np.array(img)
    
    # Flatten the array to iterate over all pixel channels (R, G, B sequentially)
    flat_array = img_array.flatten()
    
    if message_len > len(flat_array):
        raise ValueError("Message is too large for the image capacity.")
    
    # Modify the least significant bit (LSB) of each channel
    for i in range(message_len):
        # flat_array[i] & 254 clears the LSB (e.g., 255 -> 254, 254 -> 254)
        # | int(binary_message[i]) sets the LSB to the message bit
        flat_array[i] = (flat_array[i] & 254) | int(binary_message[i])
        
    # Reshape back to the original image dimensions
    encoded_array = flat_array.reshape(img_array.shape)
    
    # Create the new image object
    encoded_img = Image.fromarray(encoded_array.astype('uint8'), 'RGB')
    
    # Save the new image to an in-memory bytes buffer
    img_byte_arr = io.BytesIO()
    encoded_img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return img_byte_arr
