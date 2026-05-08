import os
import time
import requests
from DrissionPage import ChromiumPage, ChromiumOptions

# --- CONFIGURATION GITHUB ---
# Place ton APK dans le même dossier que ton script sur GitHub
APK_PATH = "Digiminer.apk" 
USER_IDS = ["2306000103", "2306000104", "2306000105", "2306000106", "2306000107", "2306000108", "2306000109", "2306000110", "2306000111", "2306000112", "2306000113", "2306000114", "2306000115", "2306000116", "2306000117", "2306000118", "2306000119", "2306000120", "2306000121", "2306000122", "2306000123", "2306000124", "2306000125", "2306000126", "2306000127", "2306000128", "2306000129", "2306000130", "2306000131", "2306000132", "2306000133", "2306000134", "2306000135", "2306000136", "2306000137", "2306000138", "2306000139", "2306000140", "2306000141", "2306000142", "2306000143", "2306000144", "2306000145", "2306000146", "2306000147", "2306000148", "2306000149", "2306000150", "2306000151", "2306000152", "2306000153", "2306000154", "2306000155", "2306000156", "2306000157", "2306000158", "2306000160", "2306000161", "2306000162", "2306000163", "2306000164", "2306000165", "2306000166", "2306000167", "2306000168", "2306000169", "2306000170", "2306000171", "2306000172", "2306000173", "2306000174", "2306000175", "2306000177", "2306000178", "2306000179", "2306000180", "2306000181", "2306000182", "2306000183", "2306000184", "2306000185", "2306000186", "2306000187", "2306000188", "2306000189", "2306000190", "2306000191", "2306000192", "2306000193", "2306000194", "2306000195", "2306000196", "2306000197", "2306000198", "2306000199", "2306000200", "2306000201", "2306000202", "2306000203", "2306000204", "2306000159", "2306000176",]

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
