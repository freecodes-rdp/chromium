const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

// --- CONFIGURATION ---
const START_TIME = Date.now();
const MAX_RUN_TIME = 5.5 * 60 * 60 * 1000; // 5h30 pour laisser le YAML nettoyer la RAM

// Remplacez ou ajoutez vos liens YouTube ici
const videoUrls = [
    'https://www.youtube.com/watch?v=rsRT4aDVKlU',
    // Ajoutez d'autres liens ici si vous le souhaitez
];

(async () => {
    const browser = await puppeteer.launch({
        headless: "new",
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--autoplay-policy=no-user-gesture-required', // Permet de forcer la lecture sans interaction
            '--window-size=1280,800'
        ]
    });

    const runInstance = async (id, urls) => {
        console.log(`[Instance ${id}] Initialisée.`);
        
        while (true) {
            // Vérification du temps restant : on ferme TOUT si dépassement
            if (Date.now() - START_TIME > MAX_RUN_TIME) {
                console.log(`[Instance ${id}] Limite de temps atteinte. Fermeture complète.`);
                await browser.close();
                process.exit(0);
            }

            let context;
            try {
                context = await browser.createBrowserContext();
                const page = await context.newPage();
                
                await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36');

                // Boucle sur chaque lien de la liste en boucle infinie
                for (let i = 0; i < urls.length; i++) {
                    const currentUrl = urls[i];
                    console.log(`[Instance ${id}] --- ${new Date().toLocaleTimeString()} : Navigation vers la vidéo ${i + 1} ---`);
                    
                    // Navigation vers la vidéo
                    await page.goto(currentUrl, { waitUntil: 'networkidle2', timeout: 60000 });

                    // Attente de 1 minute (60 000 ms) sur la page de la vidéo
                    console.log(`[Instance ${id}] Patient 1 minute sur la vidéo...`);
                    await new Promise(r => setTimeout(r, 60000));
                }

            } catch (err) {
                console.error(`[Instance ${id}] Erreur: ${err.message}`);
                await new Promise(r => setTimeout(r, 30000));
            } finally {
                if (context) await context.close();
            }
        }
    };

    // Lancement de l'instance avec la liste des liens
    runInstance(1, videoUrls);
})();