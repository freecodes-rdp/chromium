import time
import random
from DrissionPage import ChromiumPage, ChromiumOptions

# --- CONFIGURATION ---
USER_IDS = [
    "23060001", "23060002", "23060003", "23060004", 
    "23060005", "23060006", "23060007", "23060008"
]

# Lien de la vidéo à visionner
YOUTUBE_URL = "https://www.youtube.com/watch?v=rsRT4aDVKlU"

# --- CONFIGURATION DE VOTRE PROXY SOCKS5 ---
PROXY_HOST = "Scallwinn-vpnjantil.com"  # Votre nom d'hôte
PROXY_PORT = "2086"                   # Votre port proxy SOCKS
PROXY_USER = "51.91.248.209"          # Votre identifiant (ou l'adresse IP si elle sert de login)
PROXY_PASS = "Cynthia92"              # Votre mot de passe

def view_youtube_with_proxy(uid):
    print(f"\n--- [ID {uid}] Démarrage avec le proxy SOCKS5 ---")

    # --- CONFIGURATION CHROMIUM ---
    co = ChromiumOptions()
    co.set_argument('--headless')
    co.set_argument('--no-sandbox')
    co.set_argument('--disable-dev-shm-usage')
    co.set_argument('--autoplay-policy=no-user-gesture-required')
    co.set_argument('--window-size=1280,800')

    # ==========================================
    # FORMATAGE DE LA CHAÎNE SOCKS5 AVEC AUTHENTIFICATION :
    # ==========================================
    proxy_string = f"socks5://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
    co.set_argument(f'--proxy-server={proxy_string}')
    # ==========================================

    page = ChromiumPage(co)
    
    try:
        # Simuler un faux User-Agent réaliste de bureau
        page.set.user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')

        print(f"[{uid}] Navigation vers YouTube via {PROXY_HOST}...")
        page.get(YOUTUBE_URL)
        
        # Attente du chargement complet de la page
        time.sleep(5)

        # Simulation d'un mouvement de souris
        try:
            page.actions.move(random.randint(100, 500), random.randint(100, 400))
        except:
            pass

        # Temps de visionnage simulé
        watch_time = random.randint(60, 80)
        print(f"[{uid}] Visionnage en cours pendant {watch_time} secondes...")
        time.sleep(watch_time)

        print(f"✅ [ID {uid}] Session terminée avec succès.")

    except Exception as e:
        print(f"❌ [ID {uid}] Erreur de connexion au proxy : {e}")
    finally:
        page.quit()

# --- BOUCLE PRINCIPALE ---
for uid in USER_IDS:
    view_youtube_with_proxy(uid)
    pause = random.randint(10, 20)
    print(f"Attente de {pause} secondes avant le profil suivant...\n")
    time.sleep(pause)