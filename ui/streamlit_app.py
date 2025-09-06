import sys
import os

# Add project root to sys.path so Python can find normal.py, acquire.py, score.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from acquire import get_product_by_barcode, search_product_name, extract_text_from_image_url, extract_text_from_local
from normalize import normalize_product, normalize_ingredients
from score import compute_score
from datetime import datetime
import json

# Setup paths
HISTORY_FILE = "outputs/history.json"
os.makedirs("outputs", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Load history
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
else:
    history = []

# ---------------- Streamlit UI ---------------- #
st.title("🍏 Product Health Lookup")
st.write("Scan barcode, enter product name, or upload label to get health score and explanation.")

tab1, tab2 = st.tabs(["Lookup Product", "History"])

with tab1:
    st.subheader("1️⃣ Enter Product Info")
    input_method = st.radio("Select Input Method", ["Barcode", "Product Name", "Image URL", "Upload Image"])

    raw_data = None
    input_type = None

    if input_method == "Barcode":
        barcode = st.text_input("Enter Barcode")
        if st.button("Lookup Barcode"):
            raw_data = get_product_by_barcode(barcode)
            input_type = "barcode"

    elif input_method == "Product Name":
        name = st.text_input("Enter Product Name")
        if st.button("Search Product"):
            raw_data = search_product_name(name)
            input_type = "name"

    elif input_method == "Image URL":
        image_url = st.text_input("Enter Image URL")
        if st.button("Extract from URL"):
            raw_data = extract_text_from_image_url(image_url)
            input_type = "image_url"

    elif input_method == "Upload Image":
        uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        if uploaded_file and st.button("Extract from Image"):
            raw_data = extract_text_from_local(uploaded_file)
            input_type = "image_local"

    if raw_data:
        st.subheader("Raw Data Retrieved")
        st.json(raw_data)

        normalized = normalize_product(raw_data)
        st.subheader("Normalized Data")
        st.json(normalized)

        score, band, drivers = compute_score(normalized)
        st.subheader("Health Score")
        st.metric(label="Score (0–100)", value=score, delta=band)
        st.subheader("Drivers / Rules Triggered")
        st.json(drivers)

        # Save to history
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "input_type": input_type,
            "raw_data": raw_data,
            "normalized": normalized,
            "score": score,
            "band": band,
            "drivers": drivers
        }
        history.append(history_entry)
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
        st.success("✅ Result saved to history")

with tab2:
    st.subheader("📜 History of Lookups")
    if history:
        for i, entry in enumerate(reversed(history[-10:]), 1):
            st.markdown(f"**{i}. {entry['timestamp']} - {entry['input_type']}**")
            st.json(entry)
    else:
        st.info("No history yet.")
