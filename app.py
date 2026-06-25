import streamlit as st
import pandas as pd

def home_page():
    st.header("🕵️ Steganography Tool - Home Dashboard")
    st.markdown("---")
    
    st.subheader("Project Overview")
    st.write("Welcome to the **Steganography Tool**. This cybersecurity application allows you to securely hide and reveal secret messages inside image files using the Least Significant Bit (LSB) steganography technique.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**Supported Image Formats**\n\n- PNG (Portable Network Graphics)\n- BMP (Bitmap)\n\n*Note: Lossless formats are required to ensure the hidden data is not corrupted during compression.*")
        
    with col2:
        st.success("**Quick Statistics**\n\n- Maximum Capacity: Dependent on image resolution\n- Encryption: Optional AES (Coming soon)\n- Architecture: LSB substitution")

    st.markdown("---")
    st.subheader("What is LSB Steganography?")
    st.write("Least Significant Bit (LSB) steganography is a technique in which the last bit of each pixel is modified and replaced with the secret data's bit. Because it only changes the least significant bit, the alteration to the image's color is practically imperceptible to the human eye.")

    st.markdown("---")
    st.subheader("Navigation")
    st.write("Use the **sidebar** to navigate between:")
    st.markdown("- **Encode Secret Message:** Hide a message inside an image.")
    st.markdown("- **Decode Secret Message:** Extract a hidden message from an image.")

from utils.image_utils import get_image_info, format_size
from utils.capacity import calculate_capacity, check_capacity

def encode_page():
    st.header("🔒 Encode Secret Message")
    st.markdown("---")
    st.write("Upload an image and enter a secret message to hide it within the image.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1. Upload Image")
        uploaded_file = st.file_uploader("Choose a PNG or BMP image", type=["png", "bmp"], key="encode_upload")
        
        if uploaded_file is not None:
            from utils.validator import validate_image_for_steganography
            is_valid_img, img_msg = validate_image_for_steganography(uploaded_file)
            
            if not is_valid_img:
                st.error(img_msg)
            else:
                if "Warning:" in img_msg:
                    st.warning(img_msg)
                    
                st.image(uploaded_file, caption="Original Image Preview", use_container_width=True)
            
            img_info = get_image_info(uploaded_file)
            max_cap = calculate_capacity(img_info['width'], img_info['height'])
            
            with st.expander("Image Information", expanded=True):
                st.write(f"**File Name:** {img_info['filename']}")
                st.write(f"**Format:** {img_info['format']} | **Mode:** {img_info['mode']}")
                st.write(f"**Resolution:** {img_info['width']} x {img_info['height']} pixels")
                st.write(f"**File Size:** {format_size(img_info['size_bytes'])}")
                st.write(f"**Max Capacity:** {max_cap} characters")
                
            if img_info['format'].lower() not in ['png', 'bmp']:
                st.warning("Warning: Uploaded image format is not lossless. Encoding may fail or get corrupted.")
            
    with col2:
        st.subheader("2. Message Details")
        secret_message = st.text_area("Enter your secret message here", height=150)
        
        if uploaded_file is not None:
            msg_length = len(secret_message)
            is_valid, remaining = check_capacity(max_cap, msg_length)
            
            if msg_length > 0:
                if is_valid:
                    st.success(f"Message length: {msg_length} characters. Remaining capacity: {remaining} characters.")
                else:
                    st.error(f"Message is too long! Exceeds capacity by {abs(remaining)} characters.")
                    
        password = st.text_input("Encryption Password (Optional)", type="password", help="Add an extra layer of security.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Encode Message", type="primary", use_container_width=True):
            if uploaded_file is None:
                st.error("Please upload an image first.")
            elif not secret_message:
                st.error("Please enter a secret message.")
            elif uploaded_file is not None and not is_valid:
                st.error("Message is too long for this image. Please shorten it or use a larger image.")
            else:
                from utils.encoder import encode_image
                from utils.encryption import encrypt_message
                with st.spinner("Encoding message into image..."):
                    try:
                        # Encrypt if password is provided
                        final_message = encrypt_message(secret_message, password) if password else secret_message
                        
                        encoded_image_bytes = encode_image(uploaded_file, final_message)
                        st.success("Message encoded successfully! You can download it below.")
                        st.download_button(
                            label="⬇️ Download Encoded Image",
                            data=encoded_image_bytes,
                            file_name="encoded_image.png",
                            mime="image/png",
                            use_container_width=True
                        )
                        
                        st.markdown("---")
                        st.subheader("🛡️ Security Analysis Panel")
                        
                        efficiency = (len(final_message) / max_cap) * 100 if max_cap > 0 else 0
                        
                        if efficiency < 10:
                            detectability = "Low (Very safe)"
                            det_color = "green"
                        elif efficiency < 50:
                            detectability = "Medium (Moderate risk)"
                            det_color = "orange"
                        else:
                            detectability = "High (Prone to steganalysis)"
                            det_color = "red"
                            
                        enc_status = "AES Encryption Enabled" if password else "Disabled (Plaintext)"
                        pwd_status = "Protected" if password else "Unprotected"
                        
                        col_s1, col_s2, col_s3 = st.columns(3)
                        with col_s1:
                            st.metric("Capacity Used", f"{efficiency:.2f}%")
                            st.caption(f"{len(final_message)} / {max_cap} chars")
                        with col_s2:
                            st.markdown(f"**Detectability:** <span style='color:{det_color}'>{detectability}</span>", unsafe_allow_html=True)
                            st.caption("Based on LSB saturation")
                        with col_s3:
                            st.write(f"**Encryption:** {enc_status}")
                            st.write(f"**Password:** {pwd_status}")
                            
                    except Exception as e:
                        st.error(f"An error occurred during encoding: {str(e)}")

def decode_page():
    st.header("🔓 Decode Secret Message")
    st.markdown("---")
    st.write("Upload an encoded image to reveal the hidden message.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1. Upload Encoded Image")
        uploaded_file = st.file_uploader("Choose a PNG or BMP image", type=["png", "bmp"], key="decode_upload")
        
        if uploaded_file is not None:
            from utils.validator import validate_image_for_steganography
            is_valid_img, img_msg = validate_image_for_steganography(uploaded_file)
            
            if not is_valid_img:
                st.error(img_msg)
            else:
                st.image(uploaded_file, caption="Encoded Image Preview", use_container_width=True)
            
    with col2:
        st.subheader("2. Decoding Details")
        password = st.text_input("Decryption Password (If encrypted)", type="password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Decode Message", type="primary", use_container_width=True):
            if uploaded_file is None:
                st.error("Please upload an encoded image first.")
            else:
                from utils.decoder import decode_image
                from utils.encryption import decrypt_message
                with st.spinner("Decoding message from image..."):
                    try:
                        extracted_message = decode_image(uploaded_file)
                        
                        # Decrypt if password is provided
                        final_message = decrypt_message(extracted_message, password) if password else extracted_message
                        
                        st.success("Message decoded successfully!")
                        st.text_area("Hidden Message:", value=final_message, height=150)
                    except Exception as e:
                        st.error(f"An error occurred during decoding: {str(e)}")


def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except Exception:
        pass

def main():
    st.set_page_config(
        page_title="Steganography Tool",
        page_icon="🕵️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load custom UI styles
    load_css("assets/style.css")
    
    # Sidebar Navigation
    st.sidebar.title("Navigation")
    st.sidebar.markdown("---")
    
    pages = {
        "Home Dashboard": home_page,
        "Encode Secret Message": encode_page,
        "Decode Secret Message": decode_page
    }
    
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    
    st.sidebar.markdown("---")
    st.sidebar.info("A Cybersecurity Application for Secure Data Hiding")
    
    # Render selected page
    pages[selection]()

if __name__ == "__main__":
    main()

