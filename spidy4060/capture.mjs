import {chromium} from 'playwright';import fs from 'node:fs';import {serve} from './server.mjs';
const srv=serve(new URL('./web',import.meta.url).pathname,4186);await new Promise(r=>srv.on('listening',r));
const browser=await chromium.launch({executablePath:process.env.CHROME_PATH||'/opt/google/chrome/chrome',args:['--no-sandbox']});
try{const page=await browser.newPage();let errors=[];page.on('pageerror',e=>errors.push(e.message));await page.addInitScript(()=>window.EXPORTING=true);await page.goto('http://127.0.0.1:4186');await page.waitForFunction(()=>window.ready);
const cast=await page.evaluate(()=>window.studio.cast);fs.writeFileSync('characters/manifest.json',JSON.stringify(cast,null,2));
async function shot(file,opts,frame=24){const data=await page.evaluate(({opts,frame})=>window.studio.render(frame,opts).toDataURL('image/png'),{opts,frame});fs.writeFileSync(file,Buffer.from(data.split(',')[1],'base64'));}
for(const a of cast){await shot(`characters/${a.key}.png`,{key:a.key,transparent:true});}
fs.mkdirSync('review/heads',{recursive:true});for(const key of ['spidy','peter','gwen','child'])for(const expr of ['neutral','happy','shock','angry','sad','exhausted'])await shot(`review/heads/${key}-${expr}.png`,{key,expr,shot:'portrait'});
fs.mkdirSync('review/turns',{recursive:true});for(const key of ['spidy','peter','gwen','child'])for(const facing of [-1,-.5,0,.5,1])await shot(`review/turns/${key}-${facing}.png`,{key,facing,shot:'portrait'});
// Every actor / expression / motion / facing boundary must produce a frame without exceptions.
let count=await page.evaluate(()=>{let n=0;for(const a of window.studio.cast)for(const expr of window.studio.expressions)for(const facing of [-1,0,1]){window.studio.render(19,{key:a.key,expr,facing});n++;}for(const key of ['spidy','peter','gwen','child','miniSpider'])for(const action of window.studio.actions)for(const f of [0,7,15,29,45,60]){window.studio.render(f,{key,action});n++;}return n;});
fs.mkdirSync('review/motion',{recursive:true});for(let f=0;f<240;f++){let part=Math.floor(f/60),key=['spidy','peter','gwen','child'][part],action=['webPose','turn','wave','walk'][part];await shot(`review/motion/f${String(f).padStart(4,'0')}.png`,{key,action,shooters:'full'},f%60);}
if(errors.length)throw Error(errors.join('\n'));fs.writeFileSync('review/checks.json',JSON.stringify({renderChecks:count,pageErrors:errors,castCount:cast.length,voiceoverDuration:81.3975},null,2));console.log({count,cast:cast.length,errors});
}finally{await browser.close();srv.close();}
