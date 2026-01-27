def recommend_actions(risk):
    if risk == "High":
        return [
            "Offer 10-15% discount",
            "Convert to yearly contract",
            "Optional: Add tech support"
        ]
    elif risk == "Medium":
        return [
            "Upsell bundles or add-ons",
            "Encourage auto-pay or loyalty program"
        ]
    else:
        return [
            "Maintain satisfaction and rewards"
        ]
