import time
import random
from DrissionPage import ChromiumPage, ChromiumOptions

# --- CONFIGURATION (Tous les IDs restaurés) ---
USER_IDS = [
    "23060001", "23060002", "23060003", "23060004", 
    "23060005", "23060006", "23060007", "23060008"
]

# Lien de la vidéo à visionner
YOUTUBE_URL = "https://www.youtube.com/watch?v=rsRT4aDVKlU"

def view_youtube_local(uid):
    print(f"\n--- [ID {uid}] Démarrage sur le bureau virtuel (Sans Proxy) ---")

    # --- CONFIGURATION CHROMIUM ---
    co = ChromiumOptions()
    co.set_argument('--no-sandbox')
    co.set_argument('--disable-dev-shm-usage')
    co.set_argument('--autoplay-policy=no-user-gesture-required')
    co.set_argument('--window-size=1280,800')

    page = ChromiumPage(co)
    
    try:
        page.set.user_agent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')

        print(f"[{uid}] Navigation vers YouTube...")
        page.get(YOUTUBE_URL)
        
        time.sleep(5)

        # Simulation d'un mouvement de souris humain
        try:
            page.actions.move(random.randint(100, 500), random.randint(100, 400))
        except:
            pass

        # Temps de visionnage
        watch_time = random.randint(40, 60)
        print(f"[{uid}] Visionnage en cours pendant {watch_time} secondes...")
        time.sleep(watch_time)

        print(f"✅ [ID {uid}] Session terminée avec succès.")

    except Exception as e:
        print(f"❌ [ID {uid}] Erreur : {e}")
    finally:
        page.quit()

# --- BOUCLE PRINCIPALE AVEC TOUS LES IDS ---
for uid in USER_IDS:
    view_youtube_local(uid)
    pause = random.randint(10, 20)
    print(f"Attente de {pause} secondes avant le profil suivant...\n")
    time.sleep(pause)