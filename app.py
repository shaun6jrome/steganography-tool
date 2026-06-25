import streamlit as st

def main():
    st.set_page_config(
        page_title="Steganography Tool",
        page_icon="🕵️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("Steganography Tool")
    st.markdown("---")
    st.write("Welcome to the Steganography Tool. This application allows you to securely hide and reveal secret messages inside image files using the Least Significant Bit (LSB) technique.")

if __name__ == "__main__":
    main()
