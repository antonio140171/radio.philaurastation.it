import feedparser
import re

# === CONFIGURAZIONE ===
rss_url = "https://www.ansa.it/sito/ansait_rss.xml" # Cambialo se vuoi un altro feed
html_path = "index.html" # File da aggiornare
output_path = "index.html" # Sovrascrive lo stesso file
immagine_default = "news.jpg" # Immagine da mostrare se il feed non ne ha
# =======================

# 1. Legge il feed RSS
feed = feedparser.parse(rss_url)
notizia = feed.entries[0] # Prende la prima notizia

titolo = notizia.title
testo = notizia.summary if hasattr(notizia, "summary") else "Leggi di più sul sito."
link = notizia.link

# 2. Prova a estrarre immagine (se esiste)
immagine = immagine_default
if 'media_content' in notizia and len(notizia.media_content) > 0:
immagine = notizia.media_content[0]['url']
elif 'links' in notizia:
for l in notizia.links:
if l.type.startswith("image/"):
immagine = l.href
break

# 3. Costruisci il nuovo blocco HTML
nuovo_blocco = f"""
<div class="news-section">
<h3>Notizia del giorno</h3>
<img src="{immagine}" alt="Notizia immagine">
<p><strong>{titolo}</strong><br>{testo} <a href="{link}" target="_blank">Leggi di più</a></p>
</div>
"""

# 4. Carica l'HTML e sostituisci la sezione notizie
with open(html_path, "r", encoding="utf-8") as f:
html = f.read()

html = re.sub(r'<div class="news-section">.*?</div>', nuovo_blocco, html, flags=re.DOTALL)

# 5. Scrive il nuovo HTML nel file
with open(output_path, "w", encoding="utf-8") as f:
f.write(html)

print("✅ Notizia aggiornata con successo!")