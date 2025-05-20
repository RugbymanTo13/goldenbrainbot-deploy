def get_decision(text):
    # Simple example logic
    if "gold" in text.lower():
        return "Acheter de l'or 🪙"
    elif "btc" in text.lower():
        return "Vendre du Bitcoin ₿"
    else:
        return "Aucune action recommandée."