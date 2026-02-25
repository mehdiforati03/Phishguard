# PhishGuard : Système Hybride de Détection de Phishing (IA NLP)



PhishGuard est une solution de cybersécurité conçue pour détecter les tentatives de phishing en temps réel via une architecture hybride combinant réputation de domaine et intelligence artificielle.

##  Architecture du Système
Le système repose sur deux couches de défense complémentaires :
* **Filtrage de Réputation (Whitelist)** : Utilisation de la liste **Tranco (Top 10k)** pour identifier les domaines de confiance comme Google ou Azure. Cela réduit les faux positifs de 98% à 0% sur les services cloud légitimes.
* **Moteur NLP (Machine Learning)** : Pour les URLs inconnues, un modèle **Random Forest** analyse les motifs textuels via une vectorisation **TF-IDF** et des **N-grams**.

##  Spécifications Techniques
Le cœur du projet utilise le **Natural Language Processing (NLP)** pour comprendre la sémantique des URLs malveillantes.
* **Algorithme** : Random Forest Classifier.
* **Logiciel** : Flask (API), Scikit-learn (IA), Extension Chrome (Frontend).
* **Formule de Score** :
$$Score = P(\text{Phishing} \mid \text{N-grams}_{3 \dots 5})$$

##  Installation
1. **Entraînement** : `python train_model.py` (Génère `phishguard_model.pkl`).
2. **Serveur** : `python app.py` (Lancement de l'API Flask sur le port 5000).
3. **Extension** : Charger le dossier `extension/` dans `chrome://extensions/`.

##  Résultats
* **Détection du Phishing** : Identification des sites malveillants avec un score de **89%**.
* **Amélioration** : Correction des échecs de détection (passage de 5% à 89%) grâce à l'analyse sémantique.
