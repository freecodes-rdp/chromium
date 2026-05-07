const puppeteer = require('puppeteer');
const path = require('path');

// Utilise le chemin absolu pour éviter l'erreur "file not found"
const APK_PATH = path.resolve(process.env.HOME, '/home/codespace/chromium/Digiminer.apk');
const USER_ID = "230600080";"230600081";

async function upload() {
    console.log(`🚀 Démarrage pour l'ID ${USER_ID}...`);

    const browser = await puppeteer.launch({
        headless: "new",
        args: [
            '--no-sandbox',             // OBLIGATOIRE sur Codespaces/Linux
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',  // Évite les crashs mémoire
            '--disable-gpu'
        ]
    });

    try {
        const page = await browser.newPage();
        
        console.log("🔗 Connexion à UptoPlay...");
        await page.goto(`https://www.uptoplay.net/filemanager.php?username={USER_ID}`, {
            waitUntil: 'networkidle2'
        });

        // Attente pour Cloudflare
        console.log("⏳ Attente validation Cloudflare (10s)...");
        await new Promise(r => setTimeout(r, 10000));

        const inputUpload = await page.$('input[type="file"]');
        if (inputUpload) {
            console.log("📤 Envoi du fichier APK...");
            await inputUpload.uploadFile(APK_PATH);
            
            // Attente pour que l'upload se termine (ajuster selon la taille)
            console.log("🔄 Transfert en cours...");
            await new Promise(r => setTimeout(r, 20000));
            console.log("✅ Opération terminée !");
        } else {
            console.log("❌ Erreur : Champ d'upload introuvable.");
        }

    } catch (error) {
        console.error("❌ Erreur pendant l'upload :", error);
    } finally {
        await browser.close();
    }
}

upload();
