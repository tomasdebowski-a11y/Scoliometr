# Skoliometr

Digitální skoliometr do telefonu: úhel rotace trupu (ATR) v Adamsově předklonu podle Bunnella. Na šířku se měří (klepnutí na displej zapíše hodnotu, SKEN se samospouští nahraje celou páteř), na výšku jsou přehledné výsledky. Posturu řeší samostatná aplikace Posturální profil. Běží jako PWA (offline, instalace na plochu), data zůstávají v telefonu.

- `index.html`, `sw.js`, `manifest.webmanifest`, ikony: publikovaná aplikace (GitHub Pages z kořene větve `main`).
- `src/app.html`: zdroj stránky, `src/build.py` z něj skládá `index.html`, `sw.js` a manifest (`cd src && python3 build.py`, výstup v `src/dist/`).

Nejde o certifikovaný zdravotnický prostředek.
