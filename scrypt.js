const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const APK_PATH = path.join(__dirname, '/home/codespace/chromium/Digiminer.apk');
const USER_ID = "230600080"; "230600081";

async function upload() {
    console.log(`Démarrage pour l'ID ${USER_ID}...`);

    const browser = await puppeteer.launch({
        headless: "new",
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu'
        ]
    });

    try {
        const page = await browser.newPage();
        
        // Passage Cloudflare
        console.log("Connexion à UptoPlay...");
        await page.goto(`https://www.uptoplay.net/filemanager.php?username={USER_ID}`, {
            waitUntil: 'networkidle2'
        });

        // Attente manuelle pour Cloudflare
        await new Promise(r => setTimeout(r, 10000));

        // Sélection du fichier via le bouton caché
        const inputUpload = await page.$('input[type="file"]');
        if (inputUpload) {
            console.log("Envoi du fichier...");
            await inputUpload.uploadFile(APK_PATH);
            
            // Attente de l'upload
            await new Promise(r => setTimeout(r, 15000));
            console.log("✅ Terminé !");
        } else {
            console.log("❌ Erreur : Bouton d'upload non trouvé.");
        }

    } catch (error) {
        console.error("❌ Erreur critique :", error);
    } finally {
        await browser.close();
    }
}

upload();
