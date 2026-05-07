import os
import time
import requests
import shutil
import random
from DrissionPage import ChromiumPage, ChromiumOptions

# --- CONFIGURATION ---
APK_PATH = os.path.expanduser("/home/codespace/chromium/Digiminer.apk")
USER_IDS = ["230600080", "230600080"]

def upload_in_codespaces(uid):
    print(f"\n--- [ID {uid}] Démarrage sur Codespaces ---")
    
    if not os.path.exists(APK_PATH):
        print(f"❌ Erreur : Fichier introuvable à : {APK_PATH}")
        return

    co = ChromiumOptions()
    
    # Trouver le navigateur
    for path in ['/usr/bin/chromium-browser', '/usr/bin/chromium', '/usr/bin/google-chrome']:
        if os.path.exists(path):
            co.set_browser_path(path)
            break

    # 1. Dossier de profil UNIQUE et propre
    tmp_user_data = f"/tmp/chrome_profile_{uid}_{random.randint(100, 999)}"
    if os.path.exists(tmp_user_data):
        shutil.rmtree(tmp_user_data)
    co.set_user_data_path(tmp_user_data)

    # 2. Utiliser un PORT aléatoire pour éviter le conflit "127.0.0.1:9222"
    port = random.randint(9300, 9500)
    co.set_local_port(port)

    # 3. Arguments de survie pour Codespaces
    co.set_argument('--headless=new')
    co.set_argument('--no-sandbox')
    co.set_argument('--disable-dev-shm-usage') # Indispensable pour Codespaces
    co.set_argument('--disable-gpu')
    co.set_argument('--disable-software-rasterizer')

    try:
        print(f"[{uid}] Lancement de Chromium sur port {port}...")
        page = ChromiumPage(co)
        
        print(f"[{uid}] Passage Cloudflare...")
        page.get(f'https://www.uptoplay.net/filemanager.php?username={uid}')
        time.sleep(12) # On laisse plus de temps au serveur Codespaces
        
        cookies = {c['name']: c['value'] for c in page.cookies()}
        ua = page.user_agent
        page.quit()

        # Envoi direct
        print(f"[{uid}] Envoi de l'APK...")
        url = "https://uptoplay.net"
        params = {'service': 'apkonserver01', 'username': uid}
        data = {'api': 'upload', 'dir': ''}
        
        with open(APK_PATH, 'rb') as f:
            files = {'file': (os.path.basename(APK_PATH), f, 'application/vnd.android.package-archive')}
            headers = {'User-Agent': ua}
            response = requests.post(url, params=params, cookies=cookies, data=data, files=files, headers=headers)

        if response.status_code == 200:
            print(f"✅ [{uid}] Upload terminé !")
        else:
            print(f"❌ [{uid}] Code erreur serveur : {response.status_code}")

    except Exception as e:
        print(f"❌ Erreur critique : {e}")
    finally:
        if os.path.exists(tmp_user_data):
            shutil.rmtree(tmp_user_data)

for user_id in USER_IDS:
    upload_in_codespaces(user_id)
