def rank_apartments(
    apartments,
    budget=None,
    bedrooms=None,
    pet_friendly=None
):
    ranked = []

    for apartment in apartments:
        score = 0
        reasons = []

        # Budget
        if budget is not None:
            if apartment["price"] <= budget:
                score += 20
                reasons.append("Under your budget")

        # Bedrooms
        if bedrooms is not None:
            if apartment["bedrooms"] == bedrooms:
                score += 15
                reasons.append(f"Matches {bedrooms}-bedroom preference")

        # Pet Friendly
        if pet_friendly == "Yes":
            if apartment["pet_friendly"] == "Yes":
                score += 20
                reasons.append("Matches pet preference")

        # Amenities
        if apartment["gym"] == "Yes":
            score += 5

        if apartment["pool"] == "Yes":
            score += 5

        if apartment["parking"] == "Yes":
            score += 5

        apartment_copy = apartment.copy()
        apartment_copy["score"] = score
        apartment_copy["reasons"] = reasons

        ranked.append(apartment_copy)

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked