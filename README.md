#  Steganography Tool INTERN ID _ CITS4449

A modern, complete cybersecurity application built with Python and Streamlit that securely hides and reveals secret messages inside image files using the **Least Significant Bit (LSB)** steganography technique. 

## Project Overview
This project is designed for cybersecurity students, digital forensic investigators, ethical hackers, and security researchers. It provides a beginner-friendly architecture yet implements real-world data hiding techniques, complete with AES symmetric encryption and a security analysis dashboard.

## ore Features
* **Encode Secret Messages:** Seamlessly hide text within PNG or BMP images.
* **Decode Secret Messages:** Extract hidden text from encoded images.
* **Optional Encryption:** Encrypt your text message with a password using AES (Fernet) before embedding it into the image.
* **Security Analysis Panel:** Dynamically calculate image capacity, encoding efficiency, and detectability risk.
* **Modern Interface:** A sleek, cybersecurity-inspired UI with dark mode, glassmorphism aesthetics, and responsive layout.

## Installation Guide

1. **Clone the repository**
   ```bash
   git clone https://github.com/shaun6jrome/steganography-tool.git
   cd steganography-tool
   ```

2. **Create a virtual environment (Optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage Instructions

To launch the application, simply run:
```bash
streamlit run app.py
```

1. **Home Dashboard:** Read about the supported formats and LSB steganography.
2. **Encode Secret Message:** 
   * Upload a lossless image (`.png` or `.bmp`).
   * Enter your secret message.
   * (Optional) Enter a password for AES encryption.
   * Click **Encode Message** and download your new image.
3. **Decode Secret Message:**
   * Upload the previously encoded image.
   * Enter the password if you encrypted the message.
   * Click **Decode Message** to reveal the hidden text.

## 🏗️ Project Architecture

The application is structured modularly for maintainability and scalability:

```text
steganography-tool/
│
├── app.py                  # Main Streamlit application entry point
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── assets/                 
│   └── style.css           # Custom CSS for UI enhancements
│
├── outputs/                # Directory for locally saved outputs
│
└── utils/
    ├── __init__.py
    ├── encoder.py          # LSB encoding logic
    ├── decoder.py          # LSB decoding logic
    ├── capacity.py         # Image capacity calculation math
    ├── encryption.py       # Password-based AES encryption (Fernet)
    ├── image_utils.py      # Image metadata extraction
    └── validator.py        # File integrity and format validation
```

## Algorithm Explanation

### What is Steganography?
Steganography is the practice of concealing a file, message, image, or video within another file, message, image, or video. Unlike cryptography, which scrambles a message to make it unreadable, steganography hides the very existence of the message.

### Least Significant Bit (LSB) Technique
Digital images are made up of pixels. In standard RGB images, each pixel has three color channels: Red, Green, and Blue. Each channel is represented by an 8-bit integer (values from 0 to 255). 

The LSB algorithm works by altering the **last bit** (the least significant bit) of these color channels to store the binary data of our secret message.
* Because only the final bit is changed, the pixel's color value fluctuates by at most `1` (e.g., from 255 to 254). 
* This microscopic change is virtually undetectable to the human eye, keeping the secret message hidden in plain sight.

## Future Enhancements
* **Audio & Video Steganography:** Expand support beyond images.
* **Steganalysis Detection:** Build tools to detect if an image has been manipulated.
* **Batch Encoding:** Process multiple images simultaneously.

---
*Developed as part of a Cybersecurity Internship Task.*
