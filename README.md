# Daniele D’Orazio — sito professionale in verifica

Sito statico HTML/CSS pubblicato con GitHub Pages su https://danieledorazio.it/. Nessun framework, JavaScript eseguibile, analytics o modulo di raccolta dati. DNS, dominio e HTTPS sono già configurati: l’audit tecnico non li modifica.

## Anteprima e verifiche

```sh
python3 -m http.server 8080
python3 scripts/check_site.py
```

Il controllo usa solo la libreria standard Python e verifica collegamenti, frammenti, sitemap, canonical, metadati, JSON-LD, immagini e assenza di collegamenti WhatsApp attivi. Le verifiche Lighthouse e HTML dell’audit sono documentate in [docs/audit/2026-10-31.md](docs/audit/2026-10-31.md).

Il sito non richiede installazione di pacchetti né build. Gli strumenti dell’audit sono stati installati fuori dal repository e non sono dipendenze di produzione.

## Pagine e indicizzazione

La sitemap elenca la homepage e le sei pagine dei servizi attuali. `consulenza-ambientale.html` ed `efficienza-energetica.html` sono vecchie pagine dimostrative, non collegate dalla homepage: restano raggiungibili per non interrompere vecchi URL, ma sono `noindex,follow` ed escluse dalla sitemap fino alla conferma del loro futuro editoriale.

Il file `robots.txt` consente la scansione: non bloccare le vecchie pagine, altrimenti il motore non può leggere il loro `noindex`. I dati strutturati descrivono solo le pagine (`WebPage`), senza inventare qualifiche, recensioni, iscrizioni o dati aziendali.

## Fotografie e attribuzioni

Le fotografie esistenti di Isola del Liri sono servite dallo stesso sito, in WebP responsive. Non vengono effettuate richieste automatiche a Wikimedia. Autori, fonti, licenze e trasformazioni sono documentati in [assets/images/ATTRIBUTION.md](assets/images/ATTRIBUTION.md) e nei crediti visibili della homepage. L’immagine Open Graph è una versione 1200 × 630 della prima foto, sotto la stessa licenza.

## Prima del lancio definitivo

- Verificare effettiva ricezione e inoltro di `info@danieledorazio.it`: i collegamenti `mailto:` sono sintatticamente corretti, ma la consegna non è stata testata e il sito la indica ancora in attivazione.
- Sostituire il numero dimostrativo con il numero reale autorizzato; WhatsApp resta un collegamento interno ai contatti, senza invii esterni né link al numero fittizio.
- Confermare dati di albo, fiscali e professionali, e l’informativa privacy necessaria per l’attività reale. Non aggiungere un cookie banner senza una necessità effettiva.
- Confermare se mantenere, integrare o rimuovere le due pagine dimostrative escluse dall’indice.

## Google Search Console: predisposizione, non verifica completata

Canonical, sitemap e robots sono già riferiti al dominio finale. Il proprietario può aggiungere la proprietà in Search Console e completare la verifica tramite un metodo scelto da lui. Dopo la verifica, inviare `https://danieledorazio.it/sitemap.xml` e controllare le sette pagine attive tramite Controllo URL. Non sono stati creati account, aggiunti record DNS o inseriti token di verifica. Indicizzazione e posizionamento non sono garantiti.

GitHub Pages gestisce gli header HTTP e la cache. I punteggi Lighthouse sono misure di laboratorio: consultare il report per ambiente, limiti e distinzione da Core Web Vitals sul campo.
