def get_decision(message):
    if "bitcoin" in message.lower():
        return "📈 Le Bitcoin semble intéressant aujourd’hui."
    elif "or" in message.lower():
        return "💰 L'or présente une opportunité."
    else:
        return "🤖 Je n'ai pas compris, peux-tu reformuler ?"