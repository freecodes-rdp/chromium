import os
import time
import requests
import shutil
from DrissionPage import ChromiumPage, ChromiumOptions

# --- CONFIGURATION ---
APK_PATH = os.path.expanduser("/home/codespace/chromium/Digiminer.apk")
USER_IDS = ["230600080", "230600081"]

def upload_in_codespaces(uid):
    print(f"\n--- [ID {uid}] Démarrage sur Codespaces ---")
    
    if not os.path.exists(APK_PATH):
        print(f"❌ Erreur : Fichier introuvable à : {APK_PATH}")
        return

    # Configuration des options
    co = ChromiumOptions()
    
    # Force un dossier utilisateur propre pour éviter le "BrowserConnectError"
    tmp_user_data = f"/tmp/chrome_profile_{uid}"
    if os.path.exists(tmp_user_data):
        shutil.rmtree(tmp_user_data)
    co.set_user_data_path(tmp_user_data)

    # Arguments de survie pour Codespaces
    co.set_argument('--headless=new')
    co.set_argument('--no-sandbox')
    co.set_argument('--disable-dev-shm-usage')
    co.set_argument('--disable-gpu')
    co.set_argument('--remote-debugging-port=9222')

    try:
        print(f"[{uid}] Lancement de Chromium...")
        page = ChromiumPage(co)
        
        print(f"[{uid}] Passage Cloudflare...")
        page.get(f'https://www.uptoplay.net/filemanager.php?username={uid}')
        time.sleep(10)
        
        cookies = {c['name']: c['value'] for c in page.cookies()}
        ua = page.user_agent
        page.quit()

        # Envoi via Requests
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
        try: page.quit()
        except: pass
        if os.path.exists(tmp_user_data):
            shutil.rmtree(tmp_user_data)

for user_id in USER_IDS:
    upload_in_codespaces(user_id)
