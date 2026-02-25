from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import tldextract

app = Flask(__name__)
CORS(app)

# --- 1. CHARGEMENT DU MODÈLE NLP (PIPELINE) ---
# Ce modèle contient à la fois le Vectorizer (pour les mots) et le Random Forest
MODEL_PATH = 'phishguard_model.pkl'
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    print("✅ Modèle PhishGuard NLP chargé avec succès.")
else:
    print("⚠️ Erreur : 'phishguard_model.pkl' introuvable. Relance ton train_model.py !")

# --- 2. CHARGEMENT DE LA RÉPUTATION (TOP 10K) ---
def load_trusted_domains():
    """Charge la liste Tranco générée par ton script update_top_sites.py"""
    if os.path.exists('top_10k.txt'):
        with open('top_10k.txt', 'r') as f:
            # On utilise un set pour une recherche ultra-rapide en O(1)
            return set(line.strip() for line in f)
    return set()

TRUSTED_DOMAINS = load_trusted_domains()

def is_reputable(url):
    """Vérifie si le domaine appartient au Top 10 000 mondial pour éviter les faux positifs."""
    ext = tldextract.extract(url)
    domain_full = f"{ext.domain}.{ext.suffix}" # Récupère 'google.com' ou 'azure.com'
    
    return domain_full in TRUSTED_DOMAINS

# --- 3. ROUTE API ---
@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    try:
        data = request.json
        url = data.get("url", "")
        if not url:
            return jsonify({"error": "URL manquante"}), 400

        print(f"🔍 Analyse demandée pour : {url}")

        # ÉTAPE A : Filtre de Réputation (Règle le cas Gemini/Azure/Netflix)
        if is_reputable(url):
            print(f"🛡️  Réputation : {url} est un domaine certifié.")
            return jsonify({
                "score": 0,
                "verdict": "SÛR",
                "reasons": ["Domaine reconnu mondialement (Top 10k)"]
            })

        # ÉTAPE B : Analyse IA (Détection des motifs de phishing)
        # On passe l'URL brute, le pipeline s'occupe du découpage en N-grams
        prediction_proba = model.predict_proba([url])[0]
        
        # Le score de risque est la probabilité de la classe 1 (phishing)
        # Probabilité P(Phishing | URL)
        risk_score = int(prediction_proba[1] * 100)
        
        if risk_score >= 75:
            verdict = "DANGEREUX"
        elif risk_score >= 40:
            verdict = "SUSPECT"
        else:
            verdict = "SÛR"

        print(f"📊 Résultat IA : {risk_score}% | Verdict : {verdict}")

        return jsonify({
            "score": risk_score,
            "verdict": verdict,
            "reasons": ["Analyse statistique des motifs textuels (NLP)"]
        })

    except Exception as e:
        print(f"❌ Erreur serveur : {str(e)}")
        return jsonify({"error": "Erreur interne du serveur"}), 500

@app.route("/")
def home():
    return "<h1>PhishGuard API - Master Security Edition</h1>"

if __name__ == "__main__":
    # On tourne sur le port 5000, compatible avec ton extension popup.js
    app.run(debug=True, port=5000)