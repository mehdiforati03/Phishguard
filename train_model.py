import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
import joblib

def train():
    print("--- Début de l'entraînement PhishGuard (Version NLP) ---")
    
    # 1. Chargement du dataset
    df = pd.read_parquet('Testing.parquet')
    
    # 2. Préparation des étiquettes
    # On transforme 'phishing' en 1 et 'legitimate' en 0
    df['target'] = df['status'].map({'phishing': 1, 'legitimate': 0})
    
    # 3. Création du Pipeline (La solution "Zéro Manuel")
    # TfidfVectorizer va découper l'URL en morceaux de 3 à 5 lettres et apprendre les motifs suspects.
    print("Configuration du pipeline d'apprentissage automatique...")
    model_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            analyzer='char',      # Analyse caractère par caractère
            ngram_range=(3, 5),   # Cherche des motifs de 3, 4 et 5 lettres
            max_features=5000     # Garde les 5000 motifs les plus fréquents
        )),
        ('rf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    # 4. Division des données
    # Plus besoin de la fonction extract_features ! On donne l'URL brute.
    X = df['url']
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 5. Entraînement
    print("L'IA analyse le dataset pour découvrir les mots et motifs dangereux...")
    model_pipeline.fit(X_train, y_train)
    
    # 6. Sauvegarde du pipeline complet
    # On sauvegarde le "cerveau" ET sa capacité à analyser le texte ensemble
    joblib.dump(model_pipeline, 'phishguard_model.pkl')
    print("✅ Succès ! Le modèle 'phishguard_model.pkl' est maintenant beaucoup plus intelligent.")

if __name__ == "__main__":
    train()