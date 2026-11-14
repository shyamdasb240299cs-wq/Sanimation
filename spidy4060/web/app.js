import {SPIDY_CAST,EXPRESSIONS,drawCharacter} from './toon.js';
const $=id=>document.getElementById(id),c=$('c'),g=c.getContext('2d');
export const actions=['idle','walk','run','wave','talk','turn','celebrate','webPose','swingPose','weary','reach'];
const state={key:'spidy',expr:'neutral',action:'idle',facing:0,shooters:'none',shot:'full',playing:!matchMedia('(prefers-reduced-motion: reduce)').matches};
export function options(frame,over={}){const s={...state,...over},t=frame/30,o={expr:s.expr,facing:s.facing,shooters:s.shooters,time:t,headTilt:Math.sin(t*1.6)*1.4,bob:Math.sin(t*2)*.004,hairPhase:t*2,blink:Math.pow(Math.max(0,Math.cos(t*1.7)),40),L:'hang',R:'hang'};
 if(s.action==='idle'&&['civilian01','civilian08'].includes(s.key))o.R='phone';
 if(s.action==='walk'||s.action==='run'){o.step=t*(s.action==='run'?2.2:1.15);o.stride=s.action==='run'?1.5:1;o.bob=Math.abs(Math.sin(t*7.22))*.008;}
 if(s.action==='wave'){o.L='wave';o.wv=t*7;}
 if(s.action==='talk')o.talk=Math.max(0,Math.sin(t*12)*.5);
 if(s.action==='turn')o.facing=Math.sin(t*1.2);
 if(s.action==='celebrate'){o.L='up';o.R='wave';o.wv=t*8;o.jump=Math.max(0,Math.sin(t*5))*22;o.expr='hyped';}
 if(s.action==='webPose'){o.R='reach';o.L='hip';o.lift=.2+Math.sin(t*2)*.1;o.expr='squint';}
 if(s.action==='swingPose'){o.L='up';o.R='reach';o.tilt=Math.sin(t*2)*7;o.jump=40+Math.sin(t*2)*20;}
 if(s.action==='weary'){o.R='temple';o.expr='exhausted';o.headTilt=5;}
 if(s.action==='reach'){o.R='reach';o.L='belly';o.expr='worried';}
 return o;
}
function render(frame=0,over={}){const s={...state,...over};g.clearRect(0,0,c.width,c.height);if(!over.transparent){let bg=g.createLinearGradient(0,0,900,1600);bg.addColorStop(0,'#f1ecdf');bg.addColorStop(1,'#ccd9dc');g.fillStyle=bg;g.fillRect(0,0,c.width,c.height);g.fillStyle='#61788522';g.beginPath();g.ellipse(540,1465,165,19,0,0,7);g.fill();}g.save();if(s.shot==='portrait'){if(s.key==='child'){g.translate(-746,-1370);g.scale(4.3,4.3);}else{g.translate(-360,-220);g.scale(3,3);}}else {g.translate(90,0);g.scale(1.5,1.5);}drawCharacter(g,s.key,options(frame,s));g.restore();return c;}
for(const a of SPIDY_CAST){let b=document.createElement('button');b.textContent=a.name;b.onclick=()=>{state.key=a.key;sync();};b.dataset.key=a.key;$('cast').append(b);}
for(const [id,values]of [['expression',EXPRESSIONS],['action',actions]])for(const x of values){let o=document.createElement('option');o.textContent=x;$(id).append(o);}
for(const [id,key]of [['expression','expr'],['action','action'],['facing','facing'],['shooters','shooters'],['shot','shot']])$(id).oninput=e=>{state[key]=id==='facing'?+e.target.value:e.target.value;render(frame);};
function sync(){const a=SPIDY_CAST.find(x=>x.key===state.key);$('name').textContent=a.name;$('role').textContent=a.role;document.querySelectorAll('nav button').forEach(b=>b.classList.toggle('active',b.dataset.key===state.key));render(frame);}
let frame=0,last=0;$('pause').onclick=()=>{state.playing=!state.playing;$('pause').textContent=state.playing?'Pause':'Play';};
$('export').onclick=()=>{render(frame,{transparent:true});let a=document.createElement('a');a.download=state.key+'.png';a.href=c.toDataURL();a.click();render(frame);};
window.renderFrame=f=>render(f);window.studio={render,cast:SPIDY_CAST,expressions:EXPRESSIONS,actions,options};window.rendererInfo={kind:'canvas2d',name:'Shared sculpted vector rig'};window.ready=true;sync();
function loop(now){if(!window.EXPORTING&&state.playing){frame+=Math.min(100,now-last)*.03;render(frame);}last=now;requestAnimationFrame(loop);}requestAnimationFrame(loop);
