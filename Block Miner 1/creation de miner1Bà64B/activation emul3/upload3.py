import os
import time
import requests
from DrissionPage import ChromiumPage, ChromiumOptions

# --- CONFIGURATION GITHUB ---
# Place ton APK dans le même dossier que ton script sur GitHub
APK_PATH = "Digiminer.apk" 
USER_IDS = ["23060001b", "23060002b", "23060003b", "23060004b", "23060005b", "23060006b", "23060007b", "23060008b", "23060009b", "230600010b", "230600011b", "230600012b", "230600013b", "230600014b", "230600015b", "230600016b", "230600017b", "230600018b", "230600019b", "230600020b", "230600021b", "230600022b", "230600023b", "230600024b", "230600025b", "230600026b", "230600027b", "230600028b", "230600029b", "230600030b", "230600031b", "230600032b", "230600033b", "230600034b", "230600035b", "230600036b", "230600037b", "230600038b", "230600039b", "230600040b", "230600041b", "230600042b", "230600043b", "230600044b", "230600045b", "230600046b", "230600047b", "230600048b", "230600049b", "230600050b", "230600051b", "230600052b", "230600053b", "230600054b", "230600055b", "230600056b", "230600057b", "230600058b", "230600059b", "230600060b","230600061b","230600062b","230600063b","230600064b",]

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
