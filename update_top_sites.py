import pandas as pd
import requests, zipfile, io

# Télécharge le Top 10k mondial (Tranco List)
url = "https://tranco-list.eu/top-1m.csv.zip"
r = requests.get(url)
with zipfile.ZipFile(io.BytesIO(r.content)) as z:
    df = pd.read_csv(z.open('top-1m.csv'), names=['rank', 'domain'], nrows=10000)
    df['domain'].to_csv('top_10k.txt', index=False, header=False)
print("✅ Fichier 'top_10k.txt' généré.")