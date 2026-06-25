def calculate_capacity(width, height):
    """
    Calculate the maximum number of characters (bytes) that can be hidden.
    Assumes 3 color channels (RGB) and 1 bit modification per channel (LSB).
    """
    total_pixels = width * height
    total_bits = total_pixels * 3  # 3 bits per pixel
    total_bytes = total_bits // 8
    
    # Subtract 4 bytes for overhead (e.g., storing the message length)
    max_capacity = total_bytes - 4 
    return max_capacity if max_capacity > 0 else 0

def check_capacity(max_capacity, message_length):
    """
    Checks if the message length exceeds the maximum capacity.
    Returns a tuple (is_valid, remaining_capacity).
    """
    remaining = max_capacity - message_length
    if remaining < 0:
        return False, 0
    return True, remaining
