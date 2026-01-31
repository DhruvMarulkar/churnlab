def revenue_at_risk(prob, monthly_charge, months=12):
    return round(prob * monthly_charge * months, 2)

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

def best_strategy(risk):
    if risk == "High":
        return "Convert to yearly contract"
    elif risk == "Medium":
        return "Upsell add-ons"
    else:
        return "Maintain rewards"
