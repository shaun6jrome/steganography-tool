from PIL import Image

def get_image_info(uploaded_file):
    """
    Extracts information from an uploaded image file.
    """
    img = Image.open(uploaded_file)
    width, height = img.size
    format_ = img.format if img.format else uploaded_file.name.split('.')[-1].upper()
    size_bytes = uploaded_file.size
    
    # Reset file pointer after reading so it can be used elsewhere
    uploaded_file.seek(0)
    
    return {
        "filename": uploaded_file.name,
        "size_bytes": size_bytes,
        "width": width,
        "height": height,
        "total_pixels": width * height,
        "format": format_,
        "mode": img.mode
    }

def format_size(size_bytes):
    """
    Format file size in bytes to a human-readable string.
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
