import streamlit as st
import string
import random
import json
import os
import qrcode
from io import BytesIO

# Constants
BASE_URL = "https://your-app-name.streamlit.app"  # Change to your deployed URL

# Load or initialize mappings
MAPPING_FILE = "url_mappings.json"
if os.path.exists(MAPPING_FILE):
    with open(MAPPING_FILE, "r") as f:
        url_mappings = json.load(f)
else:
    url_mappings = {}

# Save mappings to file
def save_mappings():
    with open(MAPPING_FILE, "w") as f:
        json.dump(url_mappings, f)

# Generate random short code
def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Shorten URL
def shorten_url(original_url):
    code = generate_short_code()
    while code in url_mappings:
        code = generate_short_code()
    url_mappings[code] = original_url
    save_mappings()
    return code

# Get full URL
def get_full_short_url(code):
    return f"{BASE_URL}/?redirect={code}"

# Lookup original URL
def resolve_short_url(code):
    return url_mappings.get(code, None)

# Generate QR Code
def generate_qr_code(url):
    qr = qrcode.make(url)
    buf = BytesIO()
    qr.save(buf)
    return buf

# Streamlit App
st.set_page_config(page_title="🔗 URL Shortener with QR", layout="centered")
st.title("🔗 Simple URL Shortener + QR Code")

# Redirection Handler
query_params = st.query_params
if 'redirect' in query_params:
    code = query_params['redirect']
    original = resolve_short_url(code)
    if original:
        st.success("Redirect link found!")
        st.markdown(f"[👉 Click here to go to the original URL]({original})", unsafe_allow_html=True)
    else:
        st.error("Invalid short code.")
else:
    st.subheader("Paste your long URL to shorten it:")
    long_url = st.text_input("🔗 Enter full URL (e.g., https://example.com)")

    if st.button("Shorten URL"):
        if long_url:
            short_code = shorten_url(long_url)
            short_url = get_full_short_url(short_code)
            st.success("🎉 Your shortened URL is ready!")
            st.code(short_url)

            # Show QR code
            st.subheader("📱 QR Code:")
            img_buffer = generate_qr_code(short_url)
            st.image(img_buffer)

            st.download_button("⬇️ Download QR Code", img_buffer, file_name="short_url_qr.png")
        else:
            st.warning("Please enter a valid URL.")
