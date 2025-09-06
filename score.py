# --------------------------- Example Health Scoring --------------------------- #
# Uses normalized product dict from normal.py:
# {
#   "name": str,
#   "ingredients": list,
#   "nutrients": {
#       "energy_kcal": float,
#       "fat_g": float,
#       "saturates_g": float,
#       "carbohydrate_g": float,
#       "sugars_g": float,
#       "fiber_g": float,
#       "salt_g": float
#   }
# }

def compute_score(product: dict):
    """
    Compute a health score (0–100), band, and drivers from normalized product.
    Returns:
        score (int), band (str), drivers (list of dict)
    """
    nutrients = product.get("nutrients", {})
    drivers = []

    score = 100  # Start with perfect score

    # ---------------- Energy ---------------- #
    energy = nutrients.get("energy_kcal")
    if energy is not None:
        if energy > 400:
            score -= 10
            drivers.append({"rule": "High Energy", "value": energy, "threshold": ">400 kcal/100g", "impact": -10})
        elif energy < 50:
            score -= 2
            drivers.append({"rule": "Very Low Energy", "value": energy, "threshold": "<50 kcal/100g", "impact": -2})

    # ---------------- Fat ---------------- #
    fat = nutrients.get("fat_g")
    if fat is not None:
        if fat > 17.5:  # per 100g (UK traffic light)
            score -= 15
            drivers.append({"rule": "High Fat", "value": fat, "threshold": ">17.5g/100g", "impact": -15})
        elif fat < 3:
            score += 2
            drivers.append({"rule": "Low Fat", "value": fat, "threshold": "<3g/100g", "impact": +2})

    # ---------------- Saturates ---------------- #
    sat = nutrients.get("saturates_g")
    if sat is not None:
        if sat > 5:
            score -= 10
            drivers.append({"rule": "High Saturated Fat", "value": sat, "threshold": ">5g/100g", "impact": -10})

    # ---------------- Sugars ---------------- #
    sugars = nutrients.get("sugars_g")
    if sugars is not None:
        if sugars > 22.5:
            score -= 10
            drivers.append({"rule": "High Sugars", "value": sugars, "threshold": ">22.5g/100g", "impact": -10})

    # ---------------- Salt ---------------- #
    salt = nutrients.get("salt_g")
    if salt is not None:
        if salt > 1.5:
            score -= 10
            drivers.append({"rule": "High Salt", "value": salt, "threshold": ">1.5g/100g", "impact": -10})

    # ---------------- Ingredients ---------------- #
    ingredients = product.get("ingredients", [])
    if "palm oil" in ingredients:
        score -= 5
        drivers.append({"rule": "Contains Palm Oil", "impact": -5})
    if "sugar" in ingredients and sugars is None:
        score -= 3
        drivers.append({"rule": "Contains Sugar", "impact": -3})

    # Clamp score between 0–100
    score = max(0, min(100, score))

    # Assign Band
    if score >= 75:
        band = "Green"
    elif score >= 50:
        band = "Yellow"
    else:
        band = "Red"

    return score, band, drivers
