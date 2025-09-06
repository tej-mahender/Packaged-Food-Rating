import os
import logging
from datetime import datetime
from acquire import get_product_by_barcode, search_product_name, extract_text_from_image_url, extract_text_from_local
from normal import normalize_product
from score import compute_score  # Assume score.py exists

# ------------------- Setup ------------------- #
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/app.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def log_action(action_type, details):
    logging.info(f"{action_type}: {details}")

# ------------------- Input Section ------------------- #
def main():
    print("=== Product Health Lookup ===")
    print("Select input method:")
    print("1. Enter Barcode")
    print("2. Enter Product Name")
    print("3. Provide Image URL")
    print("4. Provide Local Image Path")

    choice = input("Enter option number: ").strip()

    raw_data = None
    input_type = None

    if choice == "1":
        barcode = input("Enter barcode: ").strip()
        log_action("Barcode Input", barcode)
        raw_data = get_product_by_barcode(barcode)
        input_type = "barcode"

    elif choice == "2":
        name = input("Enter product name: ").strip()
        log_action("Product Name Input", name)
        raw_data = search_product_name(name)
        input_type = "name"

    elif choice == "3":
        url = input("Enter image URL: ").strip()
        log_action("OCR Image URL Input", url)
        raw_data = extract_text_from_image_url(url)
        input_type = "image_url"

    elif choice == "4":
        path = input("Enter local image path: ").strip()
        if os.path.exists(path):
            log_action("OCR Local Image Input", path)
            raw_data = extract_text_from_local(path)
            input_type = "image_local"
        else:
            print("File not found.")
            return
    else:
        print("Invalid choice. Exiting.")
        return

    print("\n--- Raw Data ---")
    print(raw_data)

    # Normalize
    normalized = normalize_product(raw_data)
    print("\n--- Normalized Product ---")
    print(normalized)

    # Compute score
    score, band, drivers = compute_score(normalized)
    print("\n--- Health Score ---")
    print(f"Score: {score} | Band: {band}")
    print("Drivers / Rules Triggered:", drivers)

if __name__ == "__main__":
    main()
