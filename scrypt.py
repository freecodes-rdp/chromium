import os
import time
import requests
from DrissionPage import ChromiumPage, ChromiumOptions

# --- CONFIGURATION ---
# Assure-toi que l'APK est bien dans ton dossier Codespace
APK_PATH = "~/./chromium/Digiminer.apk" 
USER_IDS = ["230600080", "230600081"]

def upload_in_codespaces(uid):
    print(f"\n--- [ID {uid}] Démarrage sur Codespaces ---")
    
    if not os.path.exists(APK_PATH):
        print(f"❌ Erreur : Le fichier est introuvable à l'adresse : {APK_PATH}")
        return

    # RÉGLAGES SPÉCIFIQUES POUR ÉVITER L'ERREUR BrowserConnectError
    co = ChromiumOptions()
    
    # Chercher le binaire Chromium automatiquement
    for path in ['/usr/bin/chromium-browser', '/usr/bin/chromium', '/usr/bin/google-chrome']:
        if os.path.exists(path):
            co.set_browser_path(path)
            break

    # Arguments cruciaux pour Codespaces (Docker)
    co.set_argument('--headless=new')          # Mode sans écran (obligatoire)
    co.set_argument('--no-sandbox')            # Obligatoire dans Codespaces
    co.set_argument('--disable-dev-shm-usage') # Évite les crashs mémoire
    co.set_argument('--disable-gpu')           # Désactive l'accélération graphique
    co.set_argument('--remote-debugging-port=9222')

    try:
        print(f"[{uid}] Lancement du navigateur...")
        page = ChromiumPage(co)
        
        print(f"[{uid}] Connexion à UptoPlay et passage Cloudflare...")
        page.get(f'https://www.uptoplay.net/filemanager.php?username={uid}')
        
        # On attend que Cloudflare valide la session
        time.sleep(10)
        
        # Récupération des cookies
        cookies = {c['name']: c['value'] for c in page.cookies()}
        ua = page.user_agent
        page.quit()

        if '_sharedID' not in cookies:
            print(f"❌ [{uid}] Échec : Session Cloudflare non validée (Cookies manquants).")
            return

        # ENVOI DU FICHIER
        print(f"[{uid}] Envoi de l'APK via tunnel direct...")
        url = "https://uptoplay.net"
        params = {'service': 'apkonserver01', 'username': uid}
        data = {'api': 'upload', 'dir': ''}
        headers = {'User-Agent': ua}
        
        with open(APK_PATH, 'rb') as f:
            files = {'file': (os.path.basename(APK_PATH), f, 'application/vnd.android.package-archive')}
            response = requests.post(url, params=params, cookies=cookies, data=data, files=files, headers=headers)

        if response.status_code == 200 and ("filemanager" in response.text or "success" in response.text.lower()):
            print(f"✅ [{uid}] Upload RÉUSSI !")
        else:
            print(f"❌ [{uid}] Échec serveur (Code {response.status_code})")

    except Exception as e:
        print(f"❌ Erreur critique : {e}")
        try: page.quit()
        except: pass

# Boucle sur les IDs
for user_id in USER_IDS:
    upload_in_codespaces(user_id)
    time.sleep(2)

print("\n--- Opération terminée ---")
