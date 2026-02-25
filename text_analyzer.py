import re

def analyze_text(text):
    score = 0
    reasons = []
    
    # 1. Détection des mots-clés d'urgence (Pression psychologique)
    urgency_words = ['urgent', 'immédiat', 'suspendu', 'bloqué', 'dernière chance', 'action requise']
    found_urgency = [word for word in urgency_words if word in text.lower()]
    if found_urgency:
        score += 30
        reasons.append(f"Ton alarmiste détecté ({', '.join(found_urgency)})")
        
    # 2. Détection des demandes d'argent ou de coordonnées
    finance_words = ['virement', 'facture', 'paiement', 'remboursement', 'bancaire', 'rib']
    found_finance = [word for word in finance_words if word in text.lower()]
    if found_finance:
        score += 25
        reasons.append("Sujet financier sensible")

    # 3. Détection de liens suspects dans le texte
    if "http" in text or "www." in text:
        score += 20
        reasons.append("Contient un lien externe")

    # 4. Score final (Max 100)
    final_score = min(score, 100)
    
    return {
        "text_sample": text[:50] + "...",
        "risk_score": f"{final_score}%",
        "verdict": "DANGEREUX" if final_score > 50 else "SUSPECT" if final_score > 20 else "SÛR",
        "reasons": reasons
    }

# --- Test avec un faux SMS de phishing ---
sms_test = "URGENT: Votre compte bancaire est suspendu. Cliquez ici pour valider votre identité : http://bit.ly/123fake"
print(analyze_text(sms_test))