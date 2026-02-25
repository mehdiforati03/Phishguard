import re
from urllib.parse import urlparse

def extract_features(url):
    features = {}
    
    # On nettoie l'URL pour l'analyse
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path
    
    # 1. Caractéristiques de structure
    features['url_length'] = len(url)
    features['dot_count'] = domain.count('.')
    features['has_hyphen'] = 1 if "-" in domain else 0
    
    # 2. Caractéristiques de sécurité (Technique)
    # Vérifie si l'URL commence par https (Sûr) ou http (Suspect)
    features['is_https'] = 1 if url.startswith('https') else 0
    
    # 3. Caractéristiques lexicales
    # Compte le nombre de chiffres (les pirates en utilisent beaucoup dans les URLs générées)
    features['digit_count'] = sum(c.isdigit() for c in url)
    
    # Liste de mots souvent utilisés pour tromper les gens
    suspicious_words = ['login', 'verify', 'update', 'secure', 'account', 'banking', 'netflix', 'paypal']
    features['suspicious_word_count'] = sum(1 for word in suspicious_words if word in url.lower())

    return features

# --- Test de vérification ---
test_url = "http://secure-update-netflix-login.com/check"
print(f"Analyse de : {test_url}")
print(extract_features(test_url))