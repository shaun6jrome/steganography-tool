from PIL import Image

def validate_image_for_steganography(uploaded_file):
    """
    Validates if the uploaded file is suitable for steganography.
    Checks file integrity and ensures the format is lossless.
    """
    if uploaded_file is None:
        return False, "No file uploaded."
        
    try:
        img = Image.open(uploaded_file)
        img.verify()  # Verify that it is, in fact, an image
        
        # Reset file pointer after verify
        uploaded_file.seek(0)
        
        # Determine format
        img = Image.open(uploaded_file)
        format_ = img.format if img.format else uploaded_file.name.split('.')[-1].upper()
        
        uploaded_file.seek(0)
        
        if format_.lower() not in ['png', 'bmp']:
            return False, "Warning: For reliable steganography, use a lossless format like PNG or BMP. JPEG compression will destroy the hidden message."
            
        return True, "Image is valid."
    except Exception as e:
        return False, f"Invalid or corrupted image file: {str(e)}"
