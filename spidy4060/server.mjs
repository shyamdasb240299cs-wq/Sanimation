import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
export function serve(root, port = 0) {
  root = path.resolve(root);
  const mime = {'.js':'text/javascript', '.mjs':'text/javascript', '.css':'text/css', '.html':'text/html', '.json':'application/json', '.png':'image/png', '.jpg':'image/jpeg', '.mp4':'video/mp4'};
  return http.createServer((req,res) => {
    try {
      const pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
      const file = path.resolve(root, '.' + (pathname === '/' ? '/index.html' : pathname));
      if (!file.startsWith(root + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) { res.writeHead(404); res.end('Not found'); return; }
      res.writeHead(200, {'Content-Type': mime[path.extname(file)] || 'application/octet-stream', 'Cache-Control':'no-store'});
      const stream = fs.createReadStream(file);
      stream.on('error', () => res.destroy()); stream.pipe(res);
    } catch { res.writeHead(400); res.end('Bad request'); }
  }).listen(port, '127.0.0.1');
}
