// Save as render.mjs beside web/. Run: node render.mjs stills "0,54,108" [step=1] [quality=0.96]
// WEB=path HASH=#nd USE_CPU=1 RESUME=1 CHROME_PATH=/path/to/chrome are optional.
// Canvas 2D previews and WebGL film scenes share ready / err / renderFrame(frame) / canvas#c.
import {chromium} from 'playwright';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

export function parseFrames(spec, step = 1) {
  if (!Number.isSafeInteger(step) || step < 1) throw new Error('step must be a positive integer');
  const result = new Set();
  for (const token of spec.split(',')) {
    if (!/^\d+(?:-\d+)?$/.test(token.trim())) throw new Error(`Invalid frame range: ${token}`);
    const [a, b = a] = token.trim().split('-').map(Number);
    if (!Number.isSafeInteger(a) || !Number.isSafeInteger(b) || b < a) throw new Error(`Invalid range: ${token}`);
    if (b > 10_000_000 || result.size + Math.floor((b-a)/step) > 1_000_000) throw new Error('Frame range is too large');
    for (let f = a; f <= b; f += step) result.add(f);
  }
  return [...result].sort((a,b)=>a-b);
}
function serve(root) {
  const types={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.json':'application/json','.png':'image/png','.jpg':'image/jpeg','.svg':'image/svg+xml','.woff2':'font/woff2'};
  return http.createServer((req,res)=>{
    try {
      const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
      const file=path.resolve(root,'.'+(pathname==='/'?'/index.html':pathname));
      if(!file.startsWith(root+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile()){res.writeHead(404);res.end('Not found');return;}
      res.writeHead(200,{'Content-Type':types[path.extname(file)]||'application/octet-stream'});
      fs.createReadStream(file).on('error',()=>res.destroy()).pipe(res);
    }catch{res.writeHead(400);res.end('Bad request');}
  }).listen(0,'127.0.0.1');
}
async function main(){
  const [outdir,spec,step='1',qual='0.96']=process.argv.slice(2);
  if(!outdir||!spec)throw new Error('Usage: node render.mjs <outdir> <frames: "a-b" or "1,2,3"> [step] [quality]');
  const frames=parseFrames(spec,Number(step)), quality=Number(qual);
  if(!Number.isFinite(quality)||quality<=0||quality>1)throw new Error('quality must be > 0 and <= 1');
  const root=path.resolve(process.env.WEB||fileURLToPath(new URL('./web',import.meta.url)));
  if(!fs.existsSync(path.join(root,'index.html')))throw new Error(`Missing ${root}/index.html`);
  fs.mkdirSync(outdir,{recursive:true});
  const srv=serve(root);let browser;
  try{
    await new Promise((resolve,reject)=>{srv.once('listening',resolve);srv.once('error',reject)});
    const url=`http://127.0.0.1:${srv.address().port}/index.html${process.env.HASH||''}`;
    async function launch(cpu){
      const args=cpu?['--use-angle=swiftshader','--enable-unsafe-swiftshader']:['--ignore-gpu-blocklist','--enable-gpu-rasterization','--enable-webgl'];
      const detectedChrome=['/opt/google/chrome/chrome','/usr/bin/chromium'].find(p=>fs.existsSync(p));
      const candidate=await chromium.launch({args,executablePath:process.env.CHROME_PATH||detectedChrome});
      try{
        const page=await candidate.newPage({viewport:{width:1080,height:1920}});
        const errors=[];
        page.on('pageerror',e=>errors.push(e.message));
        page.on('console',m=>{if(m.type()==='error')console.error('PAGE:',m.text())});
        await page.addInitScript(()=>{window.EXPORTING=true;addEventListener('error',e=>{window.err=e.message});addEventListener('unhandledrejection',e=>{window.err=String(e.reason)});});
        await page.goto(url,{waitUntil:'load',timeout:60000});
        await page.waitForFunction(()=>window.ready||window.err,null,{timeout:180000});
        const err=await page.evaluate(()=>window.err);if(err||errors.length)throw new Error(err||errors.join('\n'));
        const info=await page.evaluate(()=>{
          if(typeof window.renderFrame!=='function'||!document.getElementById('c'))throw new Error('Missing renderFrame or canvas#c');
          if(window.rendererInfo?.kind==='canvas2d')return window.rendererInfo;
          // Use a separate canvas: requesting WebGL on an existing 2D canvas always returns null.
          const c=document.createElement('canvas'),gl=c.getContext('webgl2')||c.getContext('webgl');
          if(!gl)throw new Error('No WebGL context available');
          const ext=gl.getExtension('WEBGL_debug_renderer_info');
          const name=ext?gl.getParameter(ext.UNMASKED_RENDERER_WEBGL):gl.getParameter(gl.RENDERER);
          gl.getExtension('WEBGL_lose_context')?.loseContext();return {kind:'webgl',name};
        });
        // Render the first requested frame during preparation to catch lazy shader/runtime failures.
        await page.evaluate(async f=>{await window.renderFrame(f)},frames[0]);
        if(errors.length)throw new Error(errors.join('\n'));
        console.log(`Renderer: ${info.name} (${info.kind}${cpu?', SwiftShader requested':''})`);
        return {browser:candidate,page,errors};
      }catch(err){await candidate.close();throw err;}
    }
    let session;
    try{session=await launch(process.env.USE_CPU==='1')}
    catch(e){if(process.env.USE_CPU==='1')throw e;console.warn(`Initial renderer failed: ${e.message}. Retrying with SwiftShader.`);session=await launch(true)}
    browser=session.browser;const {page,errors}=session;const start=Date.now();let count=0,skipped=0;
    for(const frame of frames){
      const dest=path.join(outdir,`f${String(frame).padStart(4,'0')}.jpg`);
      if(process.env.RESUME==='1'&&fs.existsSync(dest)&&fs.statSync(dest).size>0){skipped++;continue;}
      const data=await page.evaluate(async([f,q])=>{
        window.EXPORTING=true;
        if(location.hash==='#nd')window.DEBUG_ND=1;if(location.hash==='#e')window.DEBUG_E=1;
        await window.renderFrame(f);
        if(window.err)throw new Error(String(window.err));
        return document.getElementById('c').toDataURL('image/jpeg',q);
      },[frame,quality]);
      if(errors.length)throw new Error(errors.join('\n'));
      if(!data.startsWith('data:image/jpeg;base64,'))throw new Error(`Frame ${frame}: invalid canvas output`);
      const tmp=dest+'.tmp';fs.writeFileSync(tmp,Buffer.from(data.split(',')[1],'base64'));fs.renameSync(tmp,dest);count++;
      if(count%30===0)console.log(`${count} rendered / ${frames.length} requested`);
    }
    console.log(`Done: ${count} rendered, ${skipped} resumed; ${count?((Date.now()-start)/count/1000).toFixed(3):0} s/frame`);
  }finally{if(browser)await browser.close();await new Promise(resolve=>srv.close(resolve));}
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))main().catch(e=>{console.error(e.stack||e.message);process.exitCode=1});
