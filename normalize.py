import re

# Example: standardize ingredient names
COMMON_INGREDIENTS = {
    "sugar": ["sugar", "sucrose", "glucose syrup", "fructose"],
    "salt": ["salt", "sodium chloride", "NaCl"],
    "palm oil": ["palm oil", "palmolein"],
    "cocoa": ["cocoa", "cocoa solids", "cocoa butter"]
}

def normalize_ingredients(raw_ingredients: str):
    """
    Convert raw ingredient string into standardized list of ingredients.
    """
    raw_ingredients = raw_ingredients.lower()
    normalized = []
    for key, variants in COMMON_INGREDIENTS.items():
        for var in variants:
            if var in raw_ingredients:
                normalized.append(key)
                break
    return list(set(normalized))  # Remove duplicates

def normalize_product(raw_data):
    """
    Normalize product dict or raw text from OCR.
    Returns consistent dict with keys: ingredients, nutrients (per 100g)
    """
    product = {}
    if isinstance(raw_data, dict):
        # OpenFoodFacts JSON
        product["name"] = raw_data.get("product_name", "Unknown")
        ingredients_text = raw_data.get("ingredients_text", "")
        product["ingredients"] = normalize_ingredients(ingredients_text)
        nutriments = raw_data.get("nutriments", {})
        # Convert common fields to per 100g
        product["nutrients"] = {
            "energy_kcal": nutriments.get("energy-kcal_100g"),
            "fat_g": nutriments.get("fat_100g"),
            "saturates_g": nutriments.get("saturated-fat_100g"),
            "carbohydrate_g": nutriments.get("carbohydrates_100g"),
            "sugars_g": nutriments.get("sugars_100g"),
            "fiber_g": nutriments.get("fiber_100g"),
            "salt_g": nutriments.get("salt_100g")
        }
    elif isinstance(raw_data, str):
        # OCR text
        product["name"] = "Unknown"
        product["ingredients"] = normalize_ingredients(raw_data)
        # Nutrients parsing (simple example, extend as needed)
        product["nutrients"] = {}
        energy_match = re.search(r"(\d+)\s*(kcal|cal)", raw_data.lower())
        if energy_match:
            product["nutrients"]["energy_kcal"] = float(energy_match.group(1))
        fat_match = re.search(r"(\d+\.?\d*)\s*g\s*fat", raw_data.lower())
        if fat_match:
            product["nutrients"]["fat_g"] = float(fat_match.group(1))
        sugar_match = re.search(r"(\d+\.?\d*)\s*g\s*sugars?", raw_data.lower())
        if sugar_match:
            product["nutrients"]["sugars_g"] = float(sugar_match.group(1))
        # Add more parsing rules as needed
    else:
        product["name"] = "Unknown"
        product["ingredients"] = []
        product["nutrients"] = {}

    return product
