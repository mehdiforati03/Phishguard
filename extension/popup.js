document.getElementById('checkPage').addEventListener('click', async () => {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const resultDiv = document.getElementById('result');
    resultDiv.innerText = "Analyse en cours...";

    // Envoi de l'URL à ton API Python (Flask)
    fetch('http://127.0.0.1:5000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: tab.url })
    })
    .then(response => response.json())
    .then(data => {
        resultDiv.innerText = `Verdict : ${data.verdict} (${data.score}%)`;
        resultDiv.style.color = data.score >= 50 ? "#ef4444" : "#10b981";
    })
    .catch(err => {
        resultDiv.innerText = "Erreur : Lancez app.py d'abord !";
    });
});