# Skoliometr

Digitální skoliometr do telefonu: úhel rotace trupu (ATR) v Adamsově předklonu podle Bunnella, sken páteře se zvukovou navigací, fotodokumentace postury s olovnicí a vývoj pacienta. Běží jako PWA (offline, instalace na plochu), data zůstávají v telefonu.

- `index.html`, `sw.js`, `manifest.webmanifest`, ikony: publikovaná aplikace (GitHub Pages z kořene větve `main`).
- `src/app.html`: zdroj stránky, `src/build.py` z něj skládá `index.html`, `sw.js` a manifest (`cd src && python3 build.py`, výstup v `src/dist/`).

Nejde o certifikovaný zdravotnický prostředek.
