import {fileURLToPath} from 'node:url';
import {serve} from './server.mjs';
const server = serve(fileURLToPath(new URL('./web', import.meta.url)), Number(process.env.PORT || 4173));
server.on('listening', () => console.log(`Character studio: http://127.0.0.1:${server.address().port}`));
server.on('error', e => { console.error(e.message); process.exitCode=1; });
