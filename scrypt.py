import os
import time
import requests
from DrissionPage import ChromiumPage, ChromiumOptions

# --- CONFIGURATION UBUNTU ---
# /home/votre_nom/dossier/app.apk
APK_PATH = "~/./chromium/Digiminer.apk" 
USER_IDS = ["230600080", "230600081"]

def upload_terminal(uid):
    print(f"\n--- [ID {uid}] Démarrage sur Serveur ---")
    
    # RÉGLAGES POUR LE MODE TERMINAL (SANS ÉCRAN)
    co = ChromiumOptions()
    co.set_browser_path('/usr/bin/chromium-browser') # Chemin standard Ubuntu
    co.set_argument('--headless')     # OBLIGATOIRE : Pas de fenêtre visuelle
    co.set_argument('--no-sandbox')   # Recommandé pour les serveurs
    co.set_argument('--disable-gpu')  # Évite les erreurs graphiques inutiles

    page = ChromiumPage(co)
    try:
        print(f"[{uid}] Connexion et passage Cloudflare...")
        page.get(f'https://www.uptoplay.net/filemanager.php?username={uid}')
        time.sleep(10) # Un peu plus long sur serveur pour être sûr
        
        # Récupération des cookies de session
        cookies = {c['name']: c['value'] for c in page.cookies()}
        ua = page.user_agent
        page.quit()

        if not cookies.get('_sharedID'):
            print(f"❌ [{uid}] Échec : Cookies non récupérés.")
            return

        # Upload direct via Requests
        url = "https://uptoplay.net"
        params = {'service': 'apkonserver01', 'username': uid}
        data = {'api': 'upload', 'dir': ''}
        
        print(f"[{uid}] Envoi de l'APK...")
        with open(APK_PATH, 'rb') as f:
            files = {'file': (os.path.basename(APK_PATH), f, 'application/vnd.android.package-archive')}
            headers = {'User-Agent': ua}
            response = requests.post(url, params=params, cookies=cookies, data=data, files=files, headers=headers)

        if response.status_code == 200 and ("filemanager" in response.text or "success" in response.text.lower()):
            print(f"✅ [{uid}] Upload réussi !")
        else:
            print(f"❌ [{uid}] Erreur serveur (Code {response.status_code})")

    except Exception as e:
        print(f"❌ Erreur sur {uid} : {e}")
        try: page.quit()
        except: pass

# Lancement
for uid in USER_IDS:
    upload_terminal(uid)
    time.sleep(2)