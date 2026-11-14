import fs from 'node:fs';
fs.writeFileSync(new URL('./web/toon.js',import.meta.url),fs.readFileSync(new URL('./web/toonbase.js',import.meta.url),'utf8')+fs.readFileSync(new URL('./web/roman.js',import.meta.url),'utf8'));
