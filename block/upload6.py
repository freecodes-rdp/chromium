import os
import time
import requests
from DrissionPage import ChromiumPage, ChromiumOptions

# --- CONFIGURATION GITHUB ---
# Place ton APK dans le même dossier que ton script sur GitHub
APK_PATH = "Digiminer.apk" 
USER_IDS = ["23060001e", "23060002e", "23060003e", "23060004e", "23060005e", "23060006e", "23060007e", "23060008e", "23060009e", "230600010e", "230600011e", "230600012e", "230600013e", "230600014e", "230600015e", "230600016e", "230600017e", "230600018e", "230600019e", "230600020e", "230600021e", "230600022e", "230600023e", "230600024e", "230600025e", "230600026e", "230600027e", "230600028e", "230600029e", "230600030e", "230600031e", "230600032e", "230600033e", "230600034e", "230600035e", "230600036e", "230600037e", "230600038e", "230600039e", "230600040e", "230600041e", "230600042e", "230600043e", "230600044e", "230600045e", "230600046e", "230600047e", "230600048e", "230600049e", "230600050e", "230600051e", "230600052e", "230600053e", "230600054e", "230600055e", "230600056e", "230600057e", "230600058e", "230600059e", "230600060e","230600061e","230600062e","230600063e","230600064e",]

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
