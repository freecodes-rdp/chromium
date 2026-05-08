import os
import time
import requests
from DrissionPage import ChromiumPage, ChromiumOptions

# --- CONFIGURATION GITHUB ---
# Place ton APK dans le même dossier que ton script sur GitHub
APK_PATH = "Digiminer.apk" 
USER_IDS = ["2306000205", "2306000206", "2306000207", "2306000208", "2306000209", "2306000210", "2306000211", "2306000212", "2306000213", "2306000214", "2306000215", "2306000216", "2306000217", "2306000218", "2306000219", "2306000220", "2306000221", "2306000222", "2306000223", "2306000224", "2306000225", "2306000226", "2306000227", "2306000228", "2306000229", "2306000230", "2306000231", "2306000232", "2306000233", "2306000234", "2306000235", "2306000236", "2306000237", "2306000238", "2306000239", "2306000240", "2306000241", "2306000242", "2306000243", "2306000244", "2306000245", "2306000246", "2306000247", "2306000248", "2306000249", "2306000260", "2306000261", "2306000262", "2306000263", "2306000264", "2306000265", "2306000266", "2306000267", "2306000268", "2306000269", "2306000270", "2306000271", "2306000272", "2306000273", "2306000274", "2306000275", "2306000277", "2306000278", "2306000279", "2306000280", "2306000281", "2306000282", "2306000283", "2306000284", "2306000285", "2306000286", "2306000287", "2306000288", "2306000289", "2306000290", "2306000291", "2306000292", "2306000293", "2306000294", "2306000295", "2306000296", "2306000297", "2306000298", "2306000299", "2306000300", "2306000301", "2306000302", "2306000303", "2306000304", "2306000305", "2306000306", "2306000250", "2306000251", "2306000252", "2306000253", "2306000254", "2306000255", "2306000256", "2306000257", "2306000258", "2306000259", "2306000276",]

def upload_apk_final(uid):
    print(f"\n--- [ID {uid}] Démarrage ---")
    
    if not os.path.exists(APK_PATH):
        print(f"❌ Erreur : Fichier {APK_PATH} introuvable dans le dépôt.")
        return

    # --- CONFIGURATION SANS GRAPHIQUE (HEADLESS) ---
    co = ChromiumOptions()
    co.set_argument('--headless')  # Pas d'interface graphique
    co.set_argument('--no-sandbox') # Nécessaire pour les serveurs Linux
    co.set_argument('--disable-gpu')
    
    page = ChromiumPage(co)
    try:
        page.get(f'https://www.uptoplay.net/filemanager.php?username={uid}')
        time.sleep(10) # Temps d'attente augmenté pour Cloudflare sur serveur
        
        cookies = {c['name']: c['value'] for c in page.cookies()}
        ua = page.user_agent
        page.quit()

        print(f"[{uid}] Envoi réel du fichier...")
        url = "https://www.uptoplay.net/filemanager.php"
        params = {'service': 'apkonserver01', 'username': uid}
        data = {'api': 'upload', 'dir': ''}

        with open(APK_PATH, 'rb') as f:
            files = {'file': (os.path.basename(APK_PATH), f, 'application/vnd.android.package-archive')}
            headers = {'User-Agent': ua}
            
            response = requests.post(
                url, 
                params=params, 
                cookies=cookies, 
                data=data, 
                files=files, 
                headers=headers
            )

        if response.status_code == 200:
            if "filemanager.php" in response.text or "Digiminer.apk" in response.text:
                print(f"✅ [ID {uid}] Téléchargement REUSSI !")
            else:
                print(f"⚠️ [ID {uid}] Réponse inattendue (Cloudflare a peut-être bloqué le POST).")
        else:
            print(f"❌ [ID {uid}] Erreur serveur : {response.status_code}")

    except Exception as e:
        print(f"❌ Erreur critique : {e}")
        if 'page' in locals(): page.quit()

# Lancement
for uid in USER_IDS:
    upload_apk_final(uid)
    time.sleep(5)
