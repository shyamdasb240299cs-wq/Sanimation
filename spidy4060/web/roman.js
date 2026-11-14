// Cast v2 — sculpted 2D characters for the Elon what-if story.
// Design space 600 × 1000, soles y=975. Concatenate after toonbase.js.
// Original bean/stick construction, continuous head turns, smooth painted volume.
// All surfaces, hair, face features and props are drawn live; no sprite/image dependencies.
export const EXPRESSIONS = ['neutral','happy','sad','angry','shock','smirk','wink','worried','snore','stubborn','squint','exhausted','hyped','laugh'];
const STEEL='#aeb6bf', BRASS='#d9a845', GOLD='#eac563', CYAN='#49deea', CARBON='#20252c';
// Keep the base film's face vocabulary available to legacy helper calls.
Object.assign(FACE,{
 happy:{eye:['happy','happy'],brow:[-3,-3],mouth:'grin'},sad:{eye:['small','small'],brow:[-4,3],mouth:'frown'},
 angry:{eye:['slit','slit'],brow:[5,-4],mouth:'frown'},wink:{eye:['dash','dot'],brow:[-2,-3],mouth:'smirk'},
 worried:{eye:['small','small'],brow:[-4,3],mouth:'wave'},snore:{eye:['dash','dash'],brow:[0,-1],mouth:'o'},
 stubborn:{eye:['lid','lid'],brow:[4,-3],mouth:'frown'},squint:{eye:['slit','slit'],brow:[3,-2],mouth:'dash'},
 smirk:{eye:['lid','dot'],brow:[-2,3],mouth:'smirk'},exhausted:{eye:['lid','lid'],brow:[-3,3],mouth:'frown'},hyped:{eye:['shock','shock'],brow:[-4,-4],mouth:'grin'}
});
export const OUTFITS={
 elon:{identity:'elon',tunic:'#30333d',inner:'#151c26',skin:'#f3dac8',hair:'#49392f',hairStyle:'elon',blazer:true,marsTee:true,pants:'#282d37',shoes:'#22252d',R:'tablet'},
 elonBeach:{identity:'elon',tunic:'#239ca6',inner:'#f1e6cc',skin:'#edc8ac',hair:'#49392f',hairStyle:'elon',hawaiian:true,strawHat:true,glasses:'beach',pants:'#c5b38f',shoes:'#74583c',R:'coconut'},
 heroBroke:{identity:'hero',tunic:'#6c7d88',hoodCol:'#53616d',skin:'#e7ba94',hair:'#302b2d',hairStyle:'messy',hoodie:true,eyeBags:true,worn:true,pants:'#384854',shoes:'#e3dcca',R:'phone'},
 heroCEO:{identity:'hero',tunic:'#9c3044',inner:'#252632',lapel:'#6e2338',skin:'#e7ba94',hair:'#302b2d',hairStyle:'slick',blazer:true,goldChain:true,glasses:'gold',pants:'#30303c',shoes:'#b39651',R:'cash'},
 heroBurnout:{identity:'hero',tunic:'#773646',inner:'#dfd8cb',skin:'#dfb493',hair:'#302b2d',hairStyle:'frazzled',blazer:true,tie:'#b75355',looseTie:true,eyeBags:true,stubble:true,pants:'#37323c',shoes:'#4a3e3d',R:'phone'},
 spacexEng:{identity:'engineer',tunic:'#e9e9e2',inner:'#334454',skin:'#f0c6a6',hair:'#925a3c',hairStyle:'parted',labCoat:true,headset:true,badge:'#427995',pants:'#3c4d5b',shoes:'#33404a',R:'tablet'},
 teslaExec:{identity:'exec',tunic:'#46565b',inner:'#26343c',skin:'#bd8f74',hair:'#272b2e',hairStyle:'quiff',vest:true,glasses:'smart',headset:true,badge:'#c95252',pants:'#303d43',shoes:'#283039'},
 xMod:{identity:'mod',tunic:'#363341',hoodCol:'#252630',skin:'#e9ccb2',hair:'#665143',hairStyle:'messy',hoodie:true,xLogo:true,beanie:'#75618f',glasses:'nerd',pants:'#414052',shoes:'#dbd7cf'},
 bodyguard:{identity:'guard',tunic:'#292b36',inner:'#e5e2d8',skin:'#b78364',hair:'#2b2c30',hairStyle:'buzz',blazer:true,tie:'#34343e',glasses:'dark',earpiece:true,stout:true,pants:'#292934',shoes:'#24232c',L:'cross',R:'cross'},
 senator:{identity:'senator',tunic:'#30486a',inner:'#ece6dc',skin:'#e4bda4',hair:'#c3c5c0',hairStyle:'silver',blazer:true,tie:'#a84e52',brows:'#8c8f8c',pants:'#34435a',shoes:'#493c3b',R:'subpoena'}
};
for(const [alias,key] of Object.entries({legion:'elon',old:'heroBurnout',toga:'senator',civA:'spacexEng',civB:'teslaExec',civC:'xMod',workA:'spacexEng',workB:'teslaExec'}))OUTFITS[alias]=OUTFITS[key];
// Identity stays constant across wardrobe changes. Body variations communicate role and fatigue.
export const CHARACTER_PROFILES={
 elon:{a:130,b:129,jaw:.85,chin:.65,cheek:1.03,forehead:.91,eyes:21,eyeH:8,eyeY:0,eyeGap:42,iris:'#839599',nose:1.13,mouth:1.1,shoulders:99,waist:79,body:1,neck:30},
 hero:{a:110,b:133,jaw:.67,chin:.48,cheek:.93,forehead:.92,eyes:20,eyeH:11,eyeY:0,eyeGap:36,iris:'#685348',nose:.82,mouth:.93,shoulders:89,waist:74,body:1,neck:24},
 engineer:{a:105,b:142,jaw:.77,chin:.56,cheek:.90,forehead:.91,eyes:18,eyeH:11,eyeY:2,eyeGap:35,iris:'#667568',nose:.96,mouth:.9,shoulders:87,waist:67,body:1.02,neck:25},
 exec:{a:103,b:147,jaw:.70,chin:.47,cheek:.87,forehead:.92,eyes:17,eyeH:9,eyeY:1,eyeGap:34,iris:'#675343',nose:1.07,mouth:.91,shoulders:87,waist:66,body:1.02,neck:25},
 mod:{a:117,b:130,jaw:.77,chin:.57,cheek:1.02,forehead:.94,eyes:21,eyeH:11,eyeY:4,eyeGap:38,iris:'#6f726a',nose:.76,mouth:.89,shoulders:92,waist:86,body:.98,neck:25},
 guard:{a:128,b:133,jaw:.92,chin:.76,cheek:.99,forehead:.90,eyes:17,eyeH:7,eyeY:0,eyeGap:42,iris:'#4a4542',nose:1.08,mouth:.97,shoulders:121,waist:92,body:1.02,neck:39},
 senator:{a:106,b:148,jaw:.69,chin:.52,cheek:.93,forehead:.88,eyes:18,eyeH:8,eyeY:6,eyeGap:34,iris:'#798b8d',nose:1.12,mouth:.92,shoulders:85,waist:70,body:1.02,neck:25}
};
const C2={ink:'#302331',soft:'#6b4b48',cream:'#fff9ed'};
// Every head layer uses this one ellipsoid projection. No independent hair/hat drift.
let cvHeadPose=null;
export const headPoseAt=(key='elon',facing=0)=>{
 const O=(typeof key==='string'?OUTFITS[key]:key)||OUTFITS.elon,P=CHARACTER_PROFILES[O.identity]||CHARACTER_PROFILES.hero;
 const yaw=Math.max(-1,Math.min(1,facing))*.62;
 return {a:P.a*1.06,b:P.b*1.035,depth:P.a*.63,sin:Math.sin(yaw),scale:Math.sqrt(Math.cos(yaw)**2+.86**2*Math.sin(yaw)**2),yOffset:0,depthBias:0};
};
const cvHeadPoint=(x,y)=>{
 if(!cvHeadPose)return [x,y];const H=cvHeadPose,yy=y+(H.yOffset||0);
 const z=H.depth*Math.sqrt(Math.max(0,1-(x/H.a)**2-(yy/H.b)**2))+(H.depthBias||0);
 return [x*H.scale+z*H.sin,yy];
};
const cvPath=(g,commands)=>{
 g.beginPath();if(!cvHeadPose){for(const [op,...v] of commands)g[op](...v);return;}
 let x=0,y=0,sx=0,sy=0;
 for(const [op,...v] of commands){
  if(op==='moveTo'){[x,y]=v;[sx,sy]=v;g.moveTo(...cvHeadPoint(x,y));}
  else if(op==='lineTo'){[x,y]=v;g.lineTo(...cvHeadPoint(x,y));}
  else if(op==='quadraticCurveTo'||op==='bezierCurveTo'){
   const ox=x,oy=y,n=24;
   for(let i=1;i<=n;i++){const t=i/n,u=1-t;let px,py;
    if(op==='quadraticCurveTo'){px=u*u*ox+2*u*t*v[0]+t*t*v[2];py=u*u*oy+2*u*t*v[1]+t*t*v[3];}
    else {px=u*u*u*ox+3*u*u*t*v[0]+3*u*t*t*v[2]+t*t*t*v[4];py=u*u*u*oy+3*u*u*t*v[1]+3*u*t*t*v[3]+t*t*t*v[5];}
    g.lineTo(...cvHeadPoint(px,py));
   }
   x=v[v.length-2];y=v[v.length-1];
  }else if(op==='closePath'){g.closePath();x=sx;y=sy;}
 }
};
const cvShape=(g,commands,fill,stroke=C2.ink,width=6.8)=>{cvPath(g,commands);if(fill){g.fillStyle=fill;g.fill()}if(stroke&&width){g.strokeStyle=stroke;g.lineWidth=width;g.lineJoin='round';g.lineCap='round';g.stroke()}};
const cvLine=(g,commands,color=C2.ink,width=3)=>cvShape(g,commands,null,color,width);
const cvEllipse=(g,x,y,rx,ry,fill,stroke=null,width=0,rotation=0)=>{
 rx=Math.max(.1,rx);ry=Math.max(.1,ry);
 if(cvHeadPose){const pts=[];for(let i=0;i<=64;i++){const t=i/64*Math.PI*2,dx=Math.cos(t)*rx,dy=Math.sin(t)*ry;pts.push([i?'lineTo':'moveTo',x+dx*Math.cos(rotation)-dy*Math.sin(rotation),y+dx*Math.sin(rotation)+dy*Math.cos(rotation)]);}pts.push(['closePath']);cvShape(g,pts,fill,stroke,width);return;}
 g.beginPath();g.ellipse(x,y,rx,ry,rotation,0,Math.PI*2);if(fill){g.fillStyle=fill;g.fill()}if(stroke&&width){g.strokeStyle=stroke;g.lineWidth=width;g.stroke()}
};
const cvRound=(g,x,y,w,h,r,fill,stroke=C2.ink,lw=3)=>{
 if(cvHeadPose){const pts=rrect(x,y,x+w,y+h,Math.min(r,w/2,h/2),10).map(([px,py],i)=>[i?'lineTo':'moveTo',px,py]);pts.push(['closePath']);cvShape(g,pts,fill,stroke,lw);return;}
 g.beginPath();g.roundRect(x,y,w,h,r);if(fill){g.fillStyle=fill;g.fill()}if(stroke&&lw){g.strokeStyle=stroke;g.lineWidth=lw;g.stroke()}
};
const cvGrad=(g,x0,y0,x1,y1,stops)=>{const a=cvHeadPoint(x0,y0),b=cvHeadPoint(x1,y1),gr=g.createLinearGradient(...a,...b);for(const [t,c] of stops)gr.addColorStop(t,c);return gr};
const cvRadial=(g,x,y,r,stops)=>{const [px,py]=cvHeadPoint(x,y),gr=g.createRadialGradient(px,py,0,px,py,r*(cvHeadPose?.scale||1));for(const [t,c] of stops)gr.addColorStop(t,c);return gr};
const cvText=(g,s,x,y,size,col,weight=600)=>{g.font=`${weight} ${size}px Arial, sans-serif`;g.textAlign='center';g.fillStyle=col;g.fillText(s,x,y)};
const skinPaint=(g,col,x,y,r)=>cvRadial(g,x-r*.4,y-r*.55,r*1.8,[[0,mix(col,'#fff8eb',.22)],[.57,col],[.86,mul(col,[.93,.88,.86])],[1,mul(col,[.83,.77,.78])]]);
const clothPaint=(g,col,x,y,w,h)=>cvGrad(g,x-w,y-h*.3,x+w,y+h*.3,[[0,mul(col,[.74,.76,.85])],[.28,mix(col,'#fff8e9',.10)],[.53,col],[1,mul(col,[.58,.62,.73])]]);
function profileFor(O){return CHARACTER_PROFILES[O.identity]||CHARACTER_PROFILES.hero;}
export const headCenter=(seed=3,key='elon')=>294;
export const headBounds=(key='elon')=>{const O=(typeof key==='string'?OUTFITS[key]:key)||OUTFITS.elon;const P=profileFor(O);return {x:300,y:269,rx:O.strawHat?P.a*1.6:P.a+25,ry:P.b+60};};
function headContour(P,f){const a=P.a,b=P.b,shift=f*7,narrow=1-Math.abs(f)*.055;return [
 ['moveTo',shift,-b],['bezierCurveTo',a*.58+shift,-b*1.04,a*P.forehead*narrow,-b*.77,a*.97,-b*.35],
 ['bezierCurveTo',a*1.025,-b*.06,a*P.cheek,b*.29,a*P.jaw,b*.67],
 ['bezierCurveTo',a*P.chin,b*.96,a*.28,b*1.045,0,b*1.035],
 ['bezierCurveTo',-a*.34,b*1.035,-a*P.chin,b*.94,-a*P.jaw,b*.65],
 ['bezierCurveTo',-a*P.cheek,b*.30,-a*1.025,-b*.05,-a*.97,-b*.35],
 ['bezierCurveTo',-a*P.forehead*narrow,-b*.77,-a*.58+shift,-b*1.04,shift,-b],['closePath']];}
function drawSculptedFace(g,O,P,f,opts){
 const a=P.a,b=P.b,fx=f*23,skin=O.skin,expr=EXPRESSIONS.includes(opts.expr)?opts.expr:'neutral';
 const lid=Math.max(0,Math.min(1,Number(opts.blink)||0)),happy=['happy','laugh'].includes(expr),shocked=['shock','hyped'].includes(expr);
 const eyeY=P.eyeY+1,spacing=P.eyeGap*(1-Math.abs(f)*.12);
 // The chin carries a translucent stubble wash, with a clear mouth plane above it.
 if(O.stubble){g.save();cvPath(g,headContour(P,f));g.clip();g.globalAlpha=.15;cvEllipse(g,fx,b*.72,a*.7,b*.33,'#54464a');g.globalAlpha=.42;for(let i=0;i<35;i++){const x=fx+Math.sin(i*2.399)*a*.66,y=b*.69+Math.cos(i*3.1)*b*.19;cvLine(g,[['moveTo',x,y],['lineTo',x+1,y+3]],'#776063',1.25)}g.restore();}
 if(O.identity==='elon'||O.identity==='senator'){
  const lineCol=mix(skin,'#8e6663',.35);
  for(const s of [-1,1]){const x=fx+s*a*.63;cvLine(g,[['moveTo',x,36],['bezierCurveTo',x+s*7,49,x+s*3,66,x-s*5,74]],lineCol,1.55);}
 }
 for(const s of [-1,1]){
  const far=s*f>0,depth=1-(far?.24:.02)*Math.abs(f),x=fx+s*spacing,y=eyeY+(s*f)*1.8;
  let eh=P.eyeH*(shocked?2.03:expr==='worried'?1.2:expr==='exhausted'?.63:expr==='squint'?.27:expr==='angry'?.58:1);
  const wink=expr==='wink'&&s===-1,closed=lid>=.97||wink||expr==='snore'||happy;
  const ew=P.eyes*depth;
  eh=Math.max(.7,eh*(1-lid));
  // Soft socket planes are drawn under the features; the eyelids stay legible at phone size.
  cvEllipse(g,x,y+4,ew+5,11,cvRadial(g,x,y+4,ew*1.5,[[0,mix(skin,'#a17173',.25)],[1,skin]]));
  if(closed){
   cvLine(g,[['moveTo',x-ew,y+1],['quadraticCurveTo',x,y+(happy?-10:6),x+ew,y+1]],C2.ink,3.5);
  }else{
   const top=shocked?eh:eh*.72;
   const eyePath=[['moveTo',x-ew,y],['bezierCurveTo',x-ew*.53,y-top*1.3,x+ew*.53,y-top*1.3,x+ew,y],['bezierCurveTo',x+ew*.56,y+eh*.86,x-ew*.56,y+eh*.86,x-ew,y],['closePath']];
   cvShape(g,eyePath,'#fff9ee',null,0);g.save();cvPath(g,eyePath);g.clip();
   const irisX=x+(Number(opts.look)||0)*4+f*2;
   cvEllipse(g,irisX,y,shocked?5.8:6.4,shocked?8.7:8.4,P.iris);cvEllipse(g,irisX,y,2.8,5.5,'#32303a');g.restore();
   cvLine(g,[['moveTo',x-ew,y],['bezierCurveTo',x-ew*.52,y-top*1.3,x+ew*.53,y-top*1.3,x+ew,y]],C2.ink,3.4);
   cvLine(g,[['moveTo',x-ew*.9,y+1],['quadraticCurveTo',x,y+eh*1.3,x+ew*.9,y+1]],mix(skin,C2.ink,.51),1.65);
  }
  let inner=-27,outer=-30;
  if(shocked){inner=-43;outer=-44;}if(expr==='sad'||expr==='worried'){inner=-39;outer=-24;}
  if(expr==='angry'||expr==='stubborn'){inner=-18;outer=-34;}if(happy){inner=-34;outer=-37;}
  if(expr==='smirk'||expr==='wink'){inner=s===1?-35:-24;outer=s===1?-40:-29;}
  if(expr==='exhausted'){inner=-26;outer=-22;}if(expr==='squint'){inner=-23;outer=-29;}
  const browCol=O.brows||mix(O.hair,'#76605b',.23);
  cvLine(g,[['moveTo',x-s*ew*.82,inner],['quadraticCurveTo',x,Math.min(inner,outer)-3,x+s*ew*.94,outer]],browCol,O.identity==='senator'?4.1:5.0);
  if(O.eyeBags||expr==='exhausted'){
   cvLine(g,[['moveTo',x-ew*.9,y+13],['quadraticCurveTo',x,y+22,x+ew*.84,y+11]],mix(skin,'#715965',.50),2);
   cvLine(g,[['moveTo',x-ew*.7,y+19],['quadraticCurveTo',x,y+25,x+ew*.57,y+19]],mix(skin,'#846674',.28),1.4);
  }
  if(O.identity==='senator'){for(let i=0;i<2;i++)cvLine(g,[['moveTo',x+s*(ew+4),y+3+i*5],['lineTo',x+s*(ew+12),y+4+i*8]],mix(skin,'#956e67',.5),1.4)}
 }
 // A shaded bridge and near nostril move across the face plane on turns.
 if(cvHeadPose)cvHeadPose.depthBias=11;
 const nx=fx+f*12,ny=27,n=P.nose;
 const nose=[['moveTo',fx-4*n,-10],['bezierCurveTo',fx-9*n,6,nx-13*n,25,nx-9*n,34],['quadraticCurveTo',nx+2,42,nx+12*n,33],['quadraticCurveTo',nx+11,26,nx+8,24]];
 cvShape(g,nose,cvGrad(g,nx-14,12,nx+15,28,[[0,mix(skin,'#fff4dc',.17)],[.58,skin],[1,mix(skin,'#a4786d',.43)]]),null,0);
 cvLine(g,[['moveTo',nx-10*n,33],['quadraticCurveTo',nx,39,nx+10*n,32]],mix(skin,C2.ink,.61),1.8);
 cvLine(g,[['moveTo',nx+11*n,24],['quadraticCurveTo',nx+15*n,31,nx+10*n,33]],mix(skin,C2.ink,.4),1.5);
 if(cvHeadPose)cvHeadPose.depthBias=0;
 const mx=fx+f*3,my=71,ms=P.mouth,w=30*ms;
 const talk=Math.max(0,Math.min(1,opts.talk||0));
 const clench=expr==='angry'&&O.identity==='guard';
 const open=shocked||expr==='laugh'||expr==='happy'||clench||talk>.12;
 if(expr==='snore'||expr==='shock'){
  cvEllipse(g,mx,my,expr==='shock'?12:7,expr==='shock'?18:9,'#643a40',C2.ink,2.7);
 }else if(open){
  const h=clench?11:expr==='laugh'?24:expr==='hyped'?20:expr==='happy'?14:5+talk*16;
  const mw=w*(clench?.76:expr==='laugh'?1.14:1);
  const mouthP=[['moveTo',mx-mw,my-4],['quadraticCurveTo',mx,my+2,mx+mw,my-4],['bezierCurveTo',mx+mw*.84,my+h,mx-mw*.78,my+h*1.2,mx-mw,my-4],['closePath']];
  cvShape(g,mouthP,'#58333b',C2.ink,2.6);g.save();cvPath(g,mouthP);g.clip();
  cvRound(g,mx-mw,my-5,mw*2,10,2,'#fff9e9',null,0);if(h>16)cvEllipse(g,mx+4,my+h*.85,mw*.48,6,'#bd7981');g.restore();
 }else{
  const down=['sad','angry','stubborn','exhausted'].includes(expr),smirk=expr==='smirk'||expr==='wink';
  cvEllipse(g,mx,my+7,w*.65,4,mix(skin,'#98635f',.20));
  if(expr==='worried')cvLine(g,[['moveTo',mx-w*.72,my+2],['bezierCurveTo',mx-w*.25,my-7,mx+w*.13,my+7,mx+w*.75,my]],C2.ink,2.8);
  else cvLine(g,[['moveTo',mx-w*.81,my+(smirk?5:0)],['quadraticCurveTo',mx,my+(down?-8:expr==='wink'?14:smirk?10:4),mx+w*.81,my+(expr==='wink'?-10:smirk?-4:0)]],C2.ink,2.8);
  if(smirk)cvLine(g,[['moveTo',mx+w*.91,my-7],['lineTo',mx+w*.97,my-2]],mix(skin,C2.ink,.4),1.7);
 }
 if(O.identity==='engineer')for(const [x,y] of [[-68,24],[-61,30],[-53,25],[57,26],[66,30],[72,23]])cvEllipse(g,fx+x,y,1.4,1.4,'#b08770');
 if(O.identity==='senator'){
  for(const yy of [-67,-58])cvLine(g,[['moveTo',fx-24,yy],['quadraticCurveTo',fx,yy-4,fx+25,yy]],mix(skin,'#987c76',.37),1.4);
  cvLine(g,[['moveTo',mx-22,97],['quadraticCurveTo',mx,101,mx+22,95]],mix(skin,'#94766e',.34),1.5);
 }
}
function drawHair(g,O,P,f,opts){
 const a=P.a,b=P.b,hair=O.hair,shift=0,sway=Math.sin((opts.hairPhase||0))*2;
 const H=coords=>coords.map(([op,...v])=>[op,...v.map((n,i)=>i%2===0?n+shift:n)]);
 let commands;
 if(O.hairStyle==='elon')commands=H([
  ['moveTo',-a*.98,-20],['bezierCurveTo',-a*1.06,-75,-a*.80,-128,-a*.36,-142],
  ['bezierCurveTo',-a*.04,-164,a*.42,-162,a*.78,-128],['bezierCurveTo',a*1.04,-109,a*1.03,-61,a*.97,-24],
  ['lineTo',a*.88,-47],['bezierCurveTo',a*.91,-79,a*.73,-109,a*.42,-112],
  ['bezierCurveTo',a*.12,-94,-a*.10,-96,-a*.40,-108],['bezierCurveTo',-a*.66,-111,-a*.79,-76,-a*.84,-46],['closePath']]);
 else if(O.hairStyle==='buzz')commands=H([['moveTo',-a*.98,-32],['bezierCurveTo',-a*1.01,-101,-a*.70,-147,0,-146],['bezierCurveTo',a*.80,-147,a*1.01,-99,a*.98,-32],['lineTo',a*.85,-58],['lineTo',a*.78,-82],['quadraticCurveTo',0,-96,-a*.81,-82],['closePath']]);
 else if(O.hairStyle==='bald')commands=H([['moveTo',-a*.98,-20],['quadraticCurveTo',-a*1.01,-66,-a*.83,-99],['lineTo',-a*.80,-61],['lineTo',-a*.88,-24],['closePath'],['moveTo',a*.98,-20],['quadraticCurveTo',a*1.01,-66,a*.83,-99],['lineTo',a*.80,-61],['lineTo',a*.88,-24],['closePath']]);
 else if(['bob','long','wavy','bun'].includes(O.hairStyle))commands=H([['moveTo',-a*.99,-18],['bezierCurveTo',-a*1.08,-92,-a*.85,-159,-a*.19,-157],['bezierCurveTo',a*.39,-171,a*1.05,-123,a*.99,-18],['lineTo',a*.83,-55],['quadraticCurveTo',a*.77,-112,a*.30,-117],['quadraticCurveTo',-a*.05,-86,-a*.51,-94],['quadraticCurveTo',-a*.76,-81,-a*.84,-39],['closePath']]);
 else if(O.hairStyle==='curly'){
  commands=[['moveTo',-a*.97,-17]];
  for(let i=0;i<=12;i++){const t=Math.PI+i/12*Math.PI,x=Math.cos(t)*a*1.1,y=-40+Math.sin(t)*138;commands.push(['quadraticCurveTo',x+Math.cos(t)*12,y+Math.sin(t)*13,x,y]);}
  commands.push(['lineTo',a*.96,-18],['lineTo',a*.83,-55],['quadraticCurveTo',a*.44,-91,0,-91],['quadraticCurveTo',-a*.46,-107,-a*.82,-51],['closePath']);
 }
 else if(O.hairStyle==='silver'||O.hairStyle==='parted')commands=H([['moveTo',-a*.98,-20],['bezierCurveTo',-a*1.07,-83,-a*.85,-145,-a*.25,-151],['bezierCurveTo',a*.20,-164,a*.79,-138,a*.97,-99],['quadraticCurveTo',a*1.07,-58,a*.96,-19],['lineTo',a*.82,-55],['quadraticCurveTo',a*.84,-102,a*.47,-113],['quadraticCurveTo',a*.05,-86,-a*.40,-101],['quadraticCurveTo',-a*.78,-91,-a*.83,-39],['closePath']]);
 else if(O.hairStyle==='slick'||O.hairStyle==='quiff')commands=H([['moveTo',-a*.98,-18],['quadraticCurveTo',-a*1.12,-87,-a*.78,-127],['bezierCurveTo',-a*.55,-180,a*.28,-174,a*.67,-153],['quadraticCurveTo',a*.55,-135,a*.83,-119],['quadraticCurveTo',a*1.06,-82,a*.96,-18],['lineTo',a*.81,-59],['quadraticCurveTo',a*.75,-107,a*.4,-112],['quadraticCurveTo',-.0,-105,-a*.42,-112],['quadraticCurveTo',-a*.80,-98,-a*.82,-40],['closePath']]);
 else {const frazzled=O.hairStyle==='frazzled',dy=frazzled?11:0;commands=H([['moveTo',-a*.98,-20],['lineTo',-a*1.05,-79],['lineTo',-a*1.14,-104-dy],['lineTo',-a*.86,-98],['quadraticCurveTo',-a*.90,-145-dy,-a*.46,-147],['lineTo',-a*.45,-168-dy+sway],['quadraticCurveTo',-a*.03,-146,a*.13,-161-dy],['lineTo',a*.22,-179-dy+sway],['quadraticCurveTo',a*.55,-162,a*.70,-137],['lineTo',a*.96,-147-dy],['lineTo',a*.95,-121],['lineTo',a*1.13,-97],['lineTo',a*.98,-74],['lineTo',a*.95,-18],['lineTo',a*.81,-55],['lineTo',a*.52,-86],['lineTo',a*.33,-72],['lineTo',a*.10,-93],['lineTo',-a*.30,-77],['lineTo',-a*.48,-97],['lineTo',-a*.79,-63],['closePath']]);}
 cvShape(g,commands,cvGrad(g,-90,-150,100,-15,[[0,mix(hair,'#b5a08a',.17)],[.35,hair],[1,mul(hair,[.57,.61,.71])]]),C2.ink,6.2);
 g.save();cvPath(g,commands);g.clip();
 if(!['buzz','bald','curly'].includes(O.hairStyle))for(let i=0;i<6;i++){
  const x=-a*.65+i*a*.22;
  cvLine(g,[['moveTo',x+shift,-128-i%2*8],['bezierCurveTo',x+shift+8,-146,x+shift+28,-117,x+shift+31,-106]],mix(hair,'#c8b18c',O.hairStyle==='silver'?.38:.17),2.1);
 }
 g.restore();
 if(O.beanie){
  const hat=[['moveTo',-a*1.03,-76],['bezierCurveTo',-a*1.05,-162,-a*.47,-190,8,-177],['bezierCurveTo',a*.87,-184,a*1.06,-138,a*1.05,-75],['closePath']];
  cvShape(g,hat,clothPaint(g,O.beanie,0,-130,a,110),C2.ink,6.5);cvRound(g,-a*1.04,-91,a*2.08,30,9,mix(O.beanie,'#3b3048',.17),C2.ink,4);
  for(let x=-a*.91;x<a*.95;x+=12)cvLine(g,[['moveTo',x,-87],['lineTo',x+1,-65]],mix(O.beanie,'#c0a9c6',.23),1.7);
  cvRound(g,a*.4,-84,19,16,2,'#ba8668',null,0);
 }
 if(O.strawHat){
  const oldOffset=cvHeadPose?.yOffset||0;if(cvHeadPose)cvHeadPose.yOffset=28;
  cvEllipse(g,-f*7,-132,a*1.47,23,cvGrad(g,-120,-152,140,-110,[[0,'#f1d89e'],[.5,'#dcc089'],[1,'#aa884f']]),C2.ink,5.5);
  const hat=[['moveTo',-a*.95,-135],['lineTo',-a*.81,-192],['quadraticCurveTo',-20,-204,a*.70,-191],['lineTo',a*.95,-135],['closePath']];
  cvShape(g,hat,cvGrad(g,-100,-180,110,-137,[[0,'#f5dc9e'],[.5,'#e6c78c'],[1,'#b99258']]),C2.ink,5.5);
  for(let x=-75;x<85;x+=15)cvLine(g,[['moveTo',x,-187],['lineTo',x+9,-142]],'#bc9b624d',1.6);
  cvShape(g,[['moveTo',-a*.92,-151],['quadraticCurveTo',0,-143,a*.91,-151],['lineTo',a*.95,-135],['quadraticCurveTo',0,-127,-a*.95,-135],['closePath']],'#3b665f',null,0);
  if(cvHeadPose)cvHeadPose.yOffset=oldOffset;
 }
}
function drawAccessories(g,O,P,f){
 if(O.identity==='gwen')cvLine(g,[['moveTo',-P.a*.91,-88],['quadraticCurveTo',0,-181,P.a*.89,-88]],'#253445',8);
 const a=P.a,fx=f*23;
 if(O.headset){
  cvRound(g,-a-8,-10,20,41,8,cvGrad(g,-a-8,0,-a+12,0,[[0,'#59616a'],[.5,'#303945'],[1,'#202631']]),C2.ink,3.5);
  cvLine(g,[['moveTo',-a,25],['quadraticCurveTo',-a+16,64,fx-24,52]],'#3c424b',3.7);
  cvEllipse(g,fx-22,52,7,4.5,'#66b4b4',C2.ink,2);
 }
 if(O.earrings){for(const side of [-1,1])cvEllipse(g,side*(P.a*.99),42,5,7,null,'#b99b62',2.8);}
 if(O.earpiece){cvEllipse(g,-a-3,17,5,9,'#333641',C2.ink,2);cvLine(g,[['moveTo',-a-1,22],['bezierCurveTo',-a-16,60,-59,97,-46,150]],'#9e9994',2);}
 if(!O.glasses)return;
 const raised=O.glasses==='beach',gy=raised?-100:P.eyeY;
 const frame=O.glasses==='gold'?'#cfb474':O.glasses==='smart'?'#9aa7a4':'#35313b';
 for(const s of [-1,1]){
  const x=fx+s*P.eyeGap*(1-Math.abs(f)*.12),depth=1-(s*f>0?.23:.02)*Math.abs(f),w=(O.glasses==='nerd'?31:30)*depth;
  const lens=O.glasses==='dark'||raised?'#222f39':O.glasses==='gold'?'#bda16925':'#bfd3d312';
  cvRound(g,x-w,gy-19,w*2,36,O.glasses==='nerd'?12:O.glasses==='gold'?10:7,lens,frame,4.3);
  if(O.glasses==='dark'||raised){cvLine(g,[['moveTo',x-w*.62,gy-13],['lineTo',x-w*.1,gy+9]],'#697179',2.1);}
 }
 cvLine(g,[['moveTo',fx-9,gy-8],['quadraticCurveTo',fx,gy-13,fx+9,gy-8]],frame,3.2);
 cvLine(g,[['moveTo',fx-P.eyeGap-29,gy-8],['lineTo',-a*.92,gy-15]],frame,3.2);
 cvLine(g,[['moveTo',fx+P.eyeGap+29,gy-8],['lineTo',a*.92,gy-15]],frame,3.2);
}
function drawHead(g,O,P,f,opts,chin){
 if(O.faceSkin)O={...O,skin:O.faceSkin};
 g.save();const px=300+f*7;g.translate(px,chin);g.rotate(rad(opts.tilt||0));g.translate(-px,-chin);g.translate(300,294-(opts.bob||0)*250);g.rotate(rad(opts.headTilt||0));
 const a=P.a,b=P.b;cvHeadPose=headPoseAt(O,f);
 // Long styles sit behind the skull; their front hairline is projected with the face.
 if(['bob','long','wavy'].includes(O.hairStyle)){
  const end=O.hairStyle==='bob'?b*.77:b+53;
  let back;
  if(O.hairStyle==='wavy')back=[['moveTo',-a*.9,-98],['bezierCurveTo',-a*1.23,-74,-a*1.23,-24,-a*1.12,5],['bezierCurveTo',-a*.98,38,-a*1.24,69,-a*1.13,104],['bezierCurveTo',-a*1.02,133,-a*1.17,end-10,-a*.94,end],['quadraticCurveTo',-a*.75,end+9,-a*.54,end-3],['lineTo',-a*.55,b*.55],['lineTo',a*.55,b*.55],['lineTo',a*.54,end-3],['quadraticCurveTo',a*.86,end+10,a*1.03,end-4],['bezierCurveTo',a*1.18,end-14,a*1.00,131,a*1.13,101],['bezierCurveTo',a*1.26,67,a*.98,35,a*1.13,3],['bezierCurveTo',a*1.24,-35,a*1.15,-91,a*.79,-112],['closePath']];
  else back=[['moveTo',-a*.9,-98],['bezierCurveTo',-a*1.20,-69,-a*1.12,end-30,-a*1.09,end],['quadraticCurveTo',-a*.69,end+15,-a*.54,end-3],['lineTo',-a*.55,b*.55],['lineTo',a*.55,b*.55],['lineTo',a*.54,end-3],['quadraticCurveTo',a*.88,end+15,a*1.1,end-9],['bezierCurveTo',a*1.2,end-49,a*1.17,-85,a*.79,-112],['closePath']];
  cvShape(g,back,clothPaint(g,O.hair,0,0,a,250),C2.ink,6);
  g.save();cvPath(g,back);g.clip();
  for(const side of [-1,1])for(let k=0;k<3;k++)cvLine(g,[['moveTo',side*a*(.88+k*.06),-47],['bezierCurveTo',side*a*(1.12-k*.03),27,side*a*(.91+k*.02),end-66,side*a*(.94+k*.05),end-9]],mix(O.hair,'#d0ac8f',.20),2.1);
  g.restore();
 }
 if(O.hairStyle==='bun')cvEllipse(g,a*.51,-146,37,34,clothPaint(g,O.hair,0,-146,80,90),C2.ink,5.2);
 // The headset bridge sits behind the scalp and hair, rather than across the forehead.
 if(O.headset)cvLine(g,[['moveTo',-a-5,14],['bezierCurveTo',-a*1.12,-210,a*1.12,-210,a+5,14]],'#454951',7);
 // Far ear occludes smoothly during a turn instead of popping out of the outline.
 for(const s of (O.masked?[]:[-1,1])){const vis=Math.max(.08,1-s*f*.83),x=s*a*.975;
  cvEllipse(g,x,15,13*vis,22,skinPaint(g,O.skin,x-4,7,27),C2.ink,4.1);
  cvLine(g,[['moveTo',x-s*3,5],['quadraticCurveTo',x+s*7*vis,8,x-s*1,23]],mix(O.skin,'#885b5a',.48),2);
 }
 const contour=headContour(P,0);
 cvShape(g,contour,skinPaint(g,O.faceSkin||O.skin,-25,-39,Math.max(a,b)),C2.ink,7.2);
 g.save();cvPath(g,contour);g.clip();
 // Broad, low-opacity edge shading gives a sculpted surface with no noisy texture.
 cvEllipse(g,a*.86,38,a*.40,b*.98,cvRadial(g,a*1.3,30,a*.91,[[0,mix(O.skin,'#715b67',.33)],[1,O.skin+'00']]));
 cvEllipse(g,-a*.40,-b*.40,a*.51,b*.42,cvRadial(g,-a*.4,-b*.4,a*.7,[[0,'#fff9ec16'],[1,'#fff9ec00']]));
 g.restore();
 if(O.masked)drawMask(g,O,P,opts);else {drawSculptedFace(g,{...O,skin:O.faceSkin||O.skin},P,0,opts);drawHair(g,O,P,0,opts);drawAccessories(g,O,P,0);}cvHeadPose=null;g.restore();
}
function drawProp(g,prop,x,y,side,O,opts){
 g.save();g.translate(x+side*5,y-22);g.rotate(rad(side*5+(opts.propTilt||0)));
 if(prop==='phone'){
  cvRound(g,-19,-43,38,67,7,cvGrad(g,-19,0,19,0,[[0,'#7c8a91'],[.3,'#27323b'],[1,'#161e29']]),C2.ink,3.4);
  cvRound(g,-15,-38,30,55,4,cvGrad(g,-12,-38,14,17,[[0,'#1c394d'],[.5,'#4e9ca6'],[1,'#92d0c6']]),null,0);
  cvRound(g,-6,-37,12,4,2,'#1c2938',null,0);
  for(let i=0;i<3;i++)cvRound(g,-10,-24+i*10,20-i*3,4,1,'#deede4b3',null,0);
  if(O.worn)cvLine(g,[['moveTo',5,-35],['lineTo',-4,-9],['lineTo',6,1],['lineTo',-5,16]],'#ffffffaa',1.4);
  if(O.looseTie){for(const s of [-1,1])cvLine(g,[['moveTo',s*24,-30],['quadraticCurveTo',s*33,-16,s*24,-5]],'#aa6b66',1.7);}
 }else if(prop==='tablet'){
  cvRound(g,-33,-52,66,83,8,cvGrad(g,-30,0,30,0,[[0,'#abb8bd'],[.4,'#677e8c'],[1,'#3b5262']]),C2.ink,3.8);
  cvRound(g,-27,-45,54,67,4,cvGrad(g,-25,-45,25,22,[[0,'#203949'],[1,'#122734']]),'#a1b8ba',1);
  cvLine(g,[['moveTo',-21,-31],['lineTo',21,-31]],'#749ca5',1.5);
  for(let i=0;i<4;i++)cvRound(g,-20+i*11,11-i*6,6,6+i*6,1,['#7bb5b0','#82bfc1','#d8bf7b','#6e9daa'][i],null,0);
  cvEllipse(g,0,-10,9,11,null,'#7bc5c0',2);cvLine(g,[['moveTo',-4,-10],['lineTo',0,-5],['lineTo',7,-16]],'#d6e7dc',1.5);
 }else if(prop==='cash'){
  for(let i=3;i>=0;i--)cvRound(g,-31+i,-21-i*4,61,31,3,['#4a6c5d','#78997a','#a8b993','#bdc8a2'][i],C2.ink,2.2);
  cvRound(g,-7,-32,14,42,1,'#e0c78f',null,0);cvEllipse(g,0,-11,7,10,null,'#6a795f',1.6);
 }else if(prop==='coconut'){
  cvLine(g,[['moveTo',6,-13],['lineTo',22,-51],['lineTo',31,-54]],'#cc8a8b',3.2);
  cvLine(g,[['moveTo',-10,-9],['lineTo',-12,-64]],'#8e7353',1.6);
  cvShape(g,[['moveTo',-34,-48],['quadraticCurveTo',-12,-79,13,-49],['closePath']],'#d5858e',C2.ink,2.2);
  cvLine(g,[['moveTo',-12,-66],['lineTo',-13,-49]],'#f0bdaf',1.3);
  cvEllipse(g,0,0,28,26,cvRadial(g,-9,-7,45,[[0,'#a97e53'],[.5,'#79543b'],[1,'#45362f']]),C2.ink,3.6);
  cvEllipse(g,0,-16,22,8,'#e3d7b5',C2.ink,2);cvEllipse(g,0,-17,16,4,'#bfb89d');
 }else if(prop==='subpoena'){
  cvShape(g,[['moveTo',-26,-45],['lineTo',15,-45],['lineTo',28,-31],['lineTo',28,25],['lineTo',-26,25],['closePath']],cvGrad(g,-26,-45,28,25,[[0,'#fff8e5'],[1,'#c9c5ae']]),C2.ink,2.8);
  cvShape(g,[['moveTo',15,-45],['lineTo',15,-31],['lineTo',28,-31]],'#ded8bf',C2.ink,1.5);
  cvText(g,'NOTICE',0,-20,7,'#7a5a5a',700);for(let i=0;i<3;i++)cvLine(g,[['moveTo',-15,-10+i*7],['lineTo',15,-10+i*7]],'#9a9583',1.3);
  cvEllipse(g,5,16,7,7,'#a65558',C2.ink,1.2);
 }
 g.restore();
}
function drawClothing(g,O,P,f,top,bottom){
 const s=P.shoulders,w=P.waist,center=300+f*7,neck=P.neck;
 const body=[['moveTo',center-neck-5,top],['bezierCurveTo',center-s*.66,top+2,center-s,top+12,center-s,top+50],['bezierCurveTo',center-s-4,top+116,center-s*1.08,bottom-12,center-w,bottom],['quadraticCurveTo',center,bottom+23,center+w,bottom],['bezierCurveTo',center+s*1.08,bottom-12,center+s+4,top+116,center+s,top+50],['bezierCurveTo',center+s,top+12,center+s*.66,top+2,center+neck+5,top],['closePath']];
 cvShape(g,body,clothPaint(g,O.tunic,center,top,s,bottom-top),C2.ink,6.8);
 g.save();cvPath(g,body);g.clip();
 const sx=center+f*13;
 if(O.spiderSuit)drawSuit(g,O,center,top,bottom,s);
 if(O.raincoat){for(const side of [-1,1])cvLine(g,[['moveTo',center+side*40,top+5],['lineTo',center+side*48,bottom-25]],'#238e90',11);cvLine(g,[['moveTo',center,top+10],['lineTo',center,bottom]],'#b47d26',3);for(let y=top+40;y<bottom;y+=38)cvEllipse(g,center+6,y,3,3,'#fff0aa');}
 if(O.inner){
  cvShape(g,[['moveTo',sx-37,top],['lineTo',sx+37,top],['lineTo',sx+27,bottom+20],['lineTo',sx-24,bottom+20],['closePath']],clothPaint(g,O.inner,sx,top,40,200),null,0);
 }
 if(O.blazer||O.labCoat){
  const lap=O.lapel||mix(O.tunic,'#a6ada6',.11);
  for(const side of [-1,1]){
   cvShape(g,[['moveTo',sx+side*30,top-2],['lineTo',sx+side*65,top+26],['lineTo',sx+side*48,top+45],['lineTo',sx+side*60,top+60],['lineTo',sx+side*12,top+134],['lineTo',sx+side*27,top+40],['closePath']],clothPaint(g,lap,sx,top,50,150),mix(O.tunic,C2.ink,.35),2.1);
   cvLine(g,[['moveTo',sx+side*63,bottom-60],['lineTo',sx+side*36,bottom-55]],mix(O.tunic,'#d6d8cc',.22),2.1);
  }
  for(const y of [top+155,top+190])cvEllipse(g,sx+15,y,3.8,4,mul(O.tunic,[.6,.6,.72]),'#b2a69b',.7);
 }
 if(O.marsTee){
  cvEllipse(g,sx,top+78,18,18,cvRadial(g,sx-5,top+72,30,[[0,'#d69468'],[.5,'#b9614a'],[1,'#783c3b']]));
  g.save();g.translate(sx,top+78);g.rotate(-.23);g.beginPath();g.ellipse(0,0,27,7,0,.1,Math.PI);g.strokeStyle='#bca46a';g.lineWidth=2.5;g.stroke();g.restore();
  cvText(g,'OCCUPY',sx,top+113,6.6,'#c1baad',700);cvText(g,'MARS',sx,top+122,7.8,'#c1baad',700);
 }
 if(O.tie){
  // Collar, knot and blade are one attachment: a loose tie rotates as a whole.
  for(const side of [-1,1])cvShape(g,[['moveTo',sx+side*4,top+10],['lineTo',sx+side*28,top],['lineTo',sx+side*26,top+33],['lineTo',sx+side*9,top+22],['closePath']],'#e6ded0',mix(O.inner||'#eeeeee',C2.ink,.25),1.1);
  g.save();g.translate(sx+(O.looseTie?5:0),top+(O.looseTie?38:14));g.rotate(rad(O.looseTie?10:0));
  cvShape(g,[['moveTo',1,10],['lineTo',6,11],['lineTo',10,93],['lineTo',4,103],['lineTo',1,93],['closePath']],mul(O.tie,[.71,.72,.78]),C2.ink,1.4);
  cvShape(g,[['moveTo',-4,12],['lineTo',4,12],['lineTo',12,101],['lineTo',0,116],['lineTo',-12,101],['closePath']],clothPaint(g,O.tie,0,36,16,100),C2.ink,1.8);
  cvShape(g,[['moveTo',-7,0],['lineTo',7,0],['lineTo',9,8],['lineTo',0,16],['lineTo',-9,8],['closePath']],clothPaint(g,O.tie,0,5,12,16),C2.ink,1.7);
  cvLine(g,[['moveTo',1,16],['quadraticCurveTo',-2,31,0,48]],mix(O.tie,'#f0c8af',.23),1.3);g.restore();
 }
 if(O.hoodie){
  cvShape(g,[['moveTo',sx-35,top],['quadraticCurveTo',sx,top+36,sx+35,top]],null,mix(O.hoodCol,'#c1c0b4',.27),3);
  for(const side of [-1,1]){cvLine(g,[['moveTo',sx+side*18,top+19],['quadraticCurveTo',sx+side*19,top+42,sx+side*17,top+63]],'#d6d0bb',2.5);cvRound(g,sx+side*17-2,top+62,4,7,1,'#b9b6a4',null,0);}
  const pocket=[['moveTo',sx-42,bottom-69],['lineTo',sx+42,bottom-69],['lineTo',sx+55,bottom-28],['quadraticCurveTo',sx,bottom-16,sx-55,bottom-28],['closePath']];
  cvShape(g,pocket,clothPaint(g,O.hoodCol,sx,bottom-50,55,45),mix(O.hoodCol,C2.ink,.29),2.6);
  cvLine(g,[['moveTo',sx-39,bottom-62],['lineTo',sx-26,bottom-35]],mix(O.hoodCol,'#d9d8c8',.17),1.6);cvLine(g,[['moveTo',sx+39,bottom-62],['lineTo',sx+26,bottom-35]],mix(O.hoodCol,'#d9d8c8',.17),1.6);
  cvLine(g,[['moveTo',sx-w,bottom-7],['quadraticCurveTo',sx,bottom+7,sx+w,bottom-7]],mix(O.tunic,C2.ink,.19),5);
 }
 if(O.xLogo){cvLine(g,[['moveTo',sx-13,top+74],['lineTo',sx+13,top+108]],'#deded4',3.7);cvLine(g,[['moveTo',sx+13,top+74],['lineTo',sx-13,top+108]],'#deded4',2.4);}
 if(O.vest){
  for(let y=top+68;y<bottom-20;y+=28)cvLine(g,[['moveTo',center-s+10,y],['quadraticCurveTo',center,y+14,center+s-10,y]],mix(O.tunic,'#a6b7b1',.25),1.8);
  cvLine(g,[['moveTo',sx,top+22],['lineTo',sx,bottom]],'#9daba3',2.3);
  if(!O.identity.startsWith('civilian')){cvLine(g,[['moveTo',sx-9,top+71],['quadraticCurveTo',sx+3,top+64,sx+15,top+71]],'#c66161',3);cvLine(g,[['moveTo',sx+3,top+70],['lineTo',sx+3,top+90]],'#c66161',3);}
 }
 if(O.hawaiian){
  for(const [dx,dy,r] of [[-55,46,11],[49,61,12],[-39,115,10],[60,151,11],[-47,196,10],[12,179,10]]){
   for(let i=0;i<5;i++){const t=i*Math.PI*2/5;cvEllipse(g,sx+dx+Math.cos(t)*r*.7,top+dy+Math.sin(t)*r*.7,r*.62,r*.42,'#d38f96',null,0,t);}
   cvEllipse(g,sx+dx,top+dy,3.2,3.2,'#e8cf8e');
  }
  cvLine(g,[['moveTo',sx,top+24],['lineTo',sx,bottom]],'#104f5c55',2);for(let y=top+50;y<bottom;y+=39)cvEllipse(g,sx+4,y,2.6,2.6,'#d6cba9');
 }
 if(O.cardigan){
  for(const side of [-1,1]){
   cvLine(g,[['moveTo',sx+side*33,top+3],['quadraticCurveTo',sx+side*29,top+113,sx+side*31,bottom+6]],mix(O.tunic,'#c6c6b1',.15),7);
   cvRound(g,sx+side*59-15,bottom-70,30,37,5,mul(O.tunic,[.87,.89,.92]),mix(O.tunic,C2.ink,.2),1.5);
  }
  for(const dy of [87,130,173])cvEllipse(g,sx+31,top+dy,3,3,'#b6b9a0',C2.ink,.7);
 }
 if(O.casual&&!O.cardigan&&!O.hoodie)cvLine(g,[['moveTo',sx-24,top+4],['quadraticCurveTo',sx,top+28,sx+24,top+4]],mix(O.tunic,C2.ink,.35),3);
 if(O.goldChain){
  cvLine(g,[['moveTo',sx-26,top+8],['bezierCurveTo',sx-32,top+81,sx+32,top+81,sx+26,top+8]],'#7b633e',6.6);
  cvLine(g,[['moveTo',sx-26,top+8],['bezierCurveTo',sx-32,top+81,sx+32,top+81,sx+26,top+8]],'#dcc58c',3.4);
  cvEllipse(g,sx,top+65,12,15,cvGrad(g,sx-12,top+50,sx+12,top+80,[[0,'#f8e6ac'],[.5,'#d3b775'],[1,'#9b783e']]),'#725740',1.8);cvText(g,'$',sx,top+71,17,'#8a6c40',600);
 }
 if(O.badge){
  const bx=sx+52,by=top+83;cvLine(g,[['moveTo',bx,by-17],['lineTo',bx,by-1]],'#8f9d9a',2);
  cvRound(g,bx-11,by,22,33,3,'#e5e5d9',C2.ink,1.5);cvRound(g,bx-10,by+1,20,8,1,O.badge,null,0);cvEllipse(g,bx-3,by+17,4,5,'#a0b5b5');cvLine(g,[['moveTo',bx-6,by+26],['lineTo',bx+6,by+26]],'#7d8c8b',1.3);
 }
 if(O.looseTie)for(const [dx,dy,side] of [[-64,60,1],[54,118,-1],[-45,170,-1]])cvLine(g,[['moveTo',sx+dx,top+dy],['lineTo',sx+dx+side*17,top+dy+8],['lineTo',sx+dx+side*8,top+dy+11]],mix(O.tunic,'#c79591',.28),1.5);
 g.restore();
}
export const romanFront=(p,key,opts={})=>{
 const O=(typeof key==='string'?OUTFITS[key]:key)||OUTFITS.heroBroke,P=profileFor(O),g=p.g;
 const f=Math.max(-1,Math.min(1,opts.facing||0)),bob=opts.bob||0,tilt=opts.tilt||0;
 const top=294+P.b+17-bob*250,bottom=720-bob*200+(O.stout?9:0),cx=300+f*7;
 const phase=(opts.step||0)*Math.PI*2,stride=opts.stride??(opts.step?1:0),jump=opts.jump||0;
 g.save();g.translate(0,-jump);p.rot=null;
 // Feet are anchored at y=975 in rest; knees and heel lift follow an actual two-leg cycle.
 for(const side of [-1,1]){
  const cycle=phase+(side>0?Math.PI:0),swing=Math.sin(cycle)*stride,lift=Math.max(0,Math.cos(cycle))*24*stride;
  const hx=cx+side*(P.waist*.41),hy=bottom-4,fx=300+side*42+swing*27+f*8,fy=963-lift;
  const kneeX=(hx+fx)*.5+swing*15,legColor=side*f>0?mul(O.pants,[.83,.84,.91]):O.pants;
  const line=[['moveTo',hx,hy],['quadraticCurveTo',kneeX,846-lift*.3,fx,fy]];
  cvLine(g,line,C2.ink,O.stout?25:22);cvLine(g,line,clothPaint(g,legColor,fx,hy,15,250),O.stout?17:14);
  cvLine(g,[['moveTo',fx-6,fy-5],['lineTo',fx+6,fy-5]],mix(legColor,'#a3a5a0',.2),2);
  if(O.worn)cvLine(g,[['moveTo',kneeX-5,846],['lineTo',kneeX+6,845]],'#a7b2a24d',2);
  if(O.spiderSuit){cvLine(g,[['moveTo',fx-swing*5,fy-80],['lineTo',fx,fy]],C2.ink,21);cvLine(g,[['moveTo',fx-swing*5,fy-80],['lineTo',fx,fy]],'#b82b43',15);for(let k=15;k<76;k+=17)cvLine(g,[['moveTo',fx-7,fy-k],['lineTo',fx+7,fy-k-2]],'#54293d',1.4);}
  const toe=side*(1-Math.abs(f))+f;
  const shoe=[['moveTo',fx-9,fy-3],['quadraticCurveTo',fx,fy-8,fx+10+Math.max(0,toe)*13,fy+1],['quadraticCurveTo',fx+17+Math.max(0,toe)*10,fy+12,fx-11+Math.min(0,toe)*13,fy+10],['quadraticCurveTo',fx-17+Math.min(0,toe)*8,fy+4,fx-9,fy-3],['closePath']];
  cvShape(g,shoe,clothPaint(g,O.shoes,fx,fy,30,15),C2.ink,3.5);cvLine(g,[['moveTo',fx-9,fy+8],['lineTo',fx+10+toe*10,fy+8]],mix(O.shoes,'#ece9d9',.26),1.6);
 }
 g.save();g.translate(cx,bottom);g.rotate(rad(tilt));g.translate(-cx,-bottom);
 if(O.hoodie){cvEllipse(g,cx,top+3,P.shoulders*.73,42,clothPaint(g,O.hoodCol,cx,top,70,50),C2.ink,5);}
 // Neck is visible above the clothes, linking the face to the torso volume.
 cvRound(g,cx-P.neck,top-30,P.neck*2,56,10,skinPaint(g,O.skin,cx-8,top-22,55),C2.ink,4.5);
 const defaultL=opts.L??O.L??'hang',defaultR=opts.R??O.R??'hang';
 function arm(side,pose){
  const sx=cx+side*(P.shoulders-9),sy=top+33,rest=[[sx,sy],[sx+side*16,sy+81],[sx+side*10,sy+155]];
  let points=rest.map(v=>[...v]),front=false,prop=null,finger=false,thumb=false;
  const X=k=>cx+side*(P.shoulders+k);
  const spec={
   point:[[X(36),sy-4],[X(129),sy-25]],up:[[X(32),sy-73],[X(26),sy-159]],wave:[[X(43),sy-48],[X(47),sy-146]],
   hip:[[X(47),sy+85],[cx+side*P.waist,sy+133]],belly:[[X(20),sy+112],[cx+side*21,sy+147]],temple:[[X(41),sy+9],[300+side*(P.a+15),294-20]],
   lift:[[X(39),sy-65],[X(3),sy-160]],reach:[[X(56),sy-28-(opts.lift||0)*40],[X(146),sy-87-(opts.lift||0)*80]],
   cheek:[[X(36),sy+6],[300+side*(P.a+2),294+52]],shield:[[X(11),sy+109],[cx+side*45,sy+171]],
   cross:[[X(19),sy+101],[cx-side*35,sy+98]],thumb:[[X(29),sy+48],[X(84),sy+17]],spear:[[X(12),sy+110],[X(21),sy+48]]
  };
  if(['phone','tablet','cash','coconut','subpoena'].includes(pose)){points=[rest[0],[X(31),sy+105],[X(56),sy+53]];front=true;prop=pose;}
  else if(spec[pose])points=[rest[0],...spec[pose]];
  if(['cross','belly','shield'].includes(pose))front=true;
  if(pose==='point')finger=true;if(pose==='thumb')thumb=true;
  if(pose==='wave'){
   const angle=Math.sin(opts.wv||0)*.23,ex=points[1][0],ey=points[1][1],dx=points[2][0]-ex,dy=points[2][1]-ey;
   points[2]=[ex+dx*Math.cos(angle)-dy*Math.sin(angle),ey+dx*Math.sin(angle)+dy*Math.cos(angle)];
  }
  if(pose==='hang'&&stride){points[1][0]+=Math.sin(phase+side*Math.PI/2)*13*stride;points[2][0]+=Math.sin(phase+side*Math.PI/2)*25*stride;points[2][1]-=Math.abs(Math.sin(phase))*9*stride;}
  const blend=opts.poseBlend??1;if(['wave','up','lift'].includes(pose))points=points.map((v,i)=>v.map((n,k)=>rest[i][k]+(n-rest[i][k])*blend));
  return {points,front,prop,finger,thumb,pose,side};
 }
 const arms=[arm(-1,defaultL),arm(1,defaultR)];
 function paintArm(A){
  const {points:q,side}=A;const line=[['moveTo',...q[0]],['quadraticCurveTo',...q[1],...q[2]]];
  const sleeve=O.labCoat?'#daddd6':O.tunic,width=O.stout?21:17;
  cvLine(g,line,C2.ink,width+6);cvLine(g,line,clothPaint(g,sleeve,q[1][0],q[1][1],25,100),width);
  const [x,y]=q[2],dx=x-q[1][0],dy=y-q[1][1],ang=Math.atan2(dy,dx);
  if(O.spiderSuit){if(opts.shooters&&opts.shooters!=='none'){g.save();g.translate(x,y);g.rotate(ang);cvRound(g,-25,-12,17,24,5,'#a4b5c5',C2.ink,2);cvRound(g,-22,-5,10,10,2,opts.shooters==='empty'?'#e35d49':'#7ef0df',C2.ink,1);g.restore();}}
  // Cuff and softly shaded mitten hand share the same elbow transform as the prop.
  cvLine(g,[['moveTo',x-Math.cos(ang)*12,y-Math.sin(ang)*12],['lineTo',x-Math.cos(ang)*5,y-Math.sin(ang)*5]],mix(sleeve,'#dadbd0',.18),width+1);
  cvEllipse(g,x,y,9,12,skinPaint(g,O.skin,x-3,y-5,18),C2.ink,2.8,ang-Math.PI/2);
  if(O.spiderSuit&&A.pose==='reach'){g.save();g.translate(x,y);g.rotate(ang);for(const offset of [-7,7]){cvLine(g,[['moveTo',0,offset],['lineTo',22,offset*1.6]],C2.ink,7);cvLine(g,[['moveTo',0,offset],['lineTo',22,offset*1.6]],'#bf3049',3.5);}cvLine(g,[['moveTo',1,-2],['quadraticCurveTo',9,0,1,4]],'#632d40',2);g.restore();}
  if(A.finger)cvLine(g,[['moveTo',x,y],['lineTo',x+Math.cos(ang)*23,y+Math.sin(ang)*23]],C2.ink,7.5),cvLine(g,[['moveTo',x,y],['lineTo',x+Math.cos(ang)*23,y+Math.sin(ang)*23]],O.skin,4);
  if(A.thumb)cvLine(g,[['moveTo',x-side*3,y-3],['quadraticCurveTo',x-side*1,y-14,x+side*3,y-19]],C2.ink,8),cvLine(g,[['moveTo',x-side*3,y-3],['quadraticCurveTo',x-side*1,y-14,x+side*3,y-19]],O.skin,4.5);
  if(A.prop){drawProp(g,A.prop,x,y,side,O,opts);cvEllipse(g,x-side*8,y-8,5.5,10,skinPaint(g,O.skin,x-10,y-12,15),C2.ink,2,side*.35);}
 }
 for(const arm of arms)if(!arm.front)paintArm(arm);
 drawClothing(g,O,P,f,top,bottom);for(const arm of arms)if(arm.front)paintArm(arm);
 g.restore();drawHead(g,O,P,f,opts,bottom);g.restore();p.rot=null;
};
export const actorFront=romanFront;
// ---------------- Detached 2D Prop & UI Cards for the 4-Part Elon Story ----------------

/** Floating Net-Worth Hologram Banner (`$340,000,000,000`) */
export const netWorthCard = (p, text = "$340,000,000,000", col = "#38e8ff") => {
  const box = rrect(70, 410, 530, 550, 22);
  p.gradFill(box, "#0d1b2a", "#071018", rad(-90));
  p.inkRing(box, 10, rad(-90));
  p.poly(rrect(82, 422, 518, 538, 16), null, 4);
  const g = p.g; g.save();
  g.font = "900 44px Arial Black, Arial"; g.textAlign = "center"; g.textBaseline = "middle";
  g.lineWidth = 10; g.strokeStyle = INK; g.strokeText(text, 300, 480);
  g.fillStyle = col; g.fillText(text, 300, 480);
  g.restore();
};

/** Glowing Biometric Transfer Tablet Close-Up Card */
export const tabletCard = (p, signed = false) => {
  const pad = rrect(130, 280, 470, 740, 28);
  p.gradFill(pad, "#9aa5b4", "#5c6675", rad(-120));
  p.inkRing(pad, 12, rad(-120));
  const scr = rrect(155, 315, 445, 705, 16);
  p.poly(scr, "#0a1520", 6);
  const ringCol = signed ? "#38ff8e" : "#38e8ff";
  p.ell(300, 540, 68, 86, ringCol, 8);
  p.ell(300, 540, 42, 56, "#0a1520", 5);
  const g = p.g; g.save();
  g.font = "900 34px Arial Black, Arial"; g.textAlign = "center";
  g.fillStyle = "#f5c242"; g.fillText("TRANSFER ALL ASSETS", 300, 380);
  g.font = "800 26px Arial, sans-serif";
  g.fillStyle = ringCol; g.fillText(signed ? "APPROVED: $340B" : "TOUCH TO SIGN", 300, 665);
  g.restore();
};

/** Backwards-compatible alias for helmetCard */
export const helmetCard = tabletCard;

/** Floating Cash Bill Particle (`fxCash`) */
export const fxCash = (p) => {
  const b = rrect(190, 440, 410, 550, 12);
  p.gradFill(b, "#52b768", "#2d7a40", rad(-110));
  p.inkRing(b, 10, rad(-110));
  p.ell(300, 495, 36, 32, "#95e0a6", 5);
  const g = p.g; g.save();
  g.font = "900 42px Arial Black, Arial"; g.textAlign = "center"; g.textBaseline = "middle";
  g.fillStyle = "#1b4d27"; g.fillText("$", 300, 497);
  g.restore();
};

/** Pop-up Notification / Alert Bubble (`fxNotif`) */
export const fxNotif = (p, label = "!") => {
  const b = rrect(200, 420, 400, 560, 28);
  p.gradFill(b, "#ff3b4e", "#b81d2d", rad(-110));
  p.inkRing(b, 11, rad(-110));
  const g = p.g; g.save();
  g.font = "900 72px Arial Black, Arial"; g.textAlign = "center"; g.textBaseline = "middle";
  g.lineWidth = 12; g.strokeStyle = INK; g.strokeText(label, 300, 492);
  g.fillStyle = "#ffffff"; g.fillText(label, 300, 492);
  g.restore();
};

/** Flying Pizza Slice for Part 3 SpaceX Launch (`pizzaCard`) */
export const pizzaCard = (p) => {
  const tri = [[300, 370], [430, 610], [170, 610]];
  p.gradFill(tri, "#f7c548", "#d98a2b", rad(-110));
  p.inkRing(tri, 12, rad(-110));
  p.band([[165, 610], [435, 610]], "#c97a2b", 28, 8, "round");
  for (const [x, y] of [[295, 465], [255, 545], [340, 555]]) {
    p.ell(x, y, 22, 22, "#c92a2a", 5);
  }
};

/** ZZZ for sleeping/exhaustion */
export const fxZ = (p, t) => {
  const g = p.g; g.save(); g.font = "900 120px Arial Black, Arial"; g.lineJoin = "round";
  for (let i = 0; i < 3; i++) {
    const k = (t + i / 3) % 1, x = 220 + i * 70 + Math.sin(k * 6) * 20, y = 700 - k * 500, s = 0.5 + k * 0.7;
    g.save(); g.translate(x, y); g.scale(s, s); g.globalAlpha = Math.min(1, (1 - k) * 2.5);
    g.lineWidth = 16; g.strokeStyle = INK; g.strokeText("Z", 0, 0); g.fillStyle = "#ffffff"; g.fillText("Z", 0, 0); g.restore();
  }
  g.restore();
};

export const fxLeaf = (p, col = "#48b868") => {
  p.poly([[300, 380], [420, 470], [300, 620], [180, 470]], col, 14);
  p.stroke([[300, 400], [300, 600]], 8);
};

export const fxDust = (p, k, col = "#e8dcc4") => {
  const g = p.g; g.save(); g.globalAlpha = Math.max(0, 1 - k * k);
  for (let i = 0; i < 7; i++) {
    const a = i / 7 * Math.PI * 2, r = 90 + 150 * k;
    p.ell(300 + Math.cos(a) * r, 520 + Math.sin(a) * r * 0.6, 120 + 60 * k, 100 + 50 * k, col, 12);
  }
  p.ell(300, 520, 170 + 110 * k, 140 + 80 * k, col, 0);
  g.restore();
};

export const fxDrip = (p) => p.ell(300, 500, 40, 64, "#9fd4ff", 10);
export const fxSweat = fxDrip;
export const fxWood = (p) => {
  p.poly([[200, 420], [400, 400], [420, 560], [230, 600]], "#5b3d22", 14);
  p.stroke([[240, 450], [380, 440]], 6, "#3a2614");
};


// Ensemble casting for the Elon film. Concatenate after roman.js.
// Each identity has its own head construction; wardrobe colors are not the only difference.
// Head, hair and accessories use the same continuous turn rig as the principal cast.
export const EXTRA_PROFILES = {
  board01: {...CHARACTER_PROFILES.senator, a:108, b:136, jaw:.67, chin:.45, cheek:.95, forehead:.93, eyes:20, eyeH:9, eyeY:2, eyeGap:36, iris:'#696a5c', nose:.91, mouth:.98, shoulders:87, waist:72, body:1, neck:24},
  board02: {...CHARACTER_PROFILES.guard, a:118, b:141, jaw:.85, chin:.68, cheek:.97, forehead:.92, eyes:18, eyeH:8, eyeY:3, eyeGap:39, iris:'#493d35', nose:1.08, mouth:1.04, shoulders:108, waist:86, body:1.02, neck:32},
  board03: {...CHARACTER_PROFILES.exec, a:100, b:148, jaw:.63, chin:.43, cheek:.87, forehead:.93, eyes:17, eyeH:9, eyeY:0, eyeGap:33, iris:'#72513d', nose:1.12, mouth:.87, shoulders:82, waist:65, body:1.03, neck:22},
  board04: {...CHARACTER_PROFILES.hero, a:104, b:131, jaw:.69, chin:.49, cheek:.93, forehead:.95, eyes:20, eyeH:10, eyeY:0, eyeGap:35, iris:'#5b4938', nose:.83, mouth:.94, shoulders:88, waist:69, body:.99, neck:24},
  board05: {...CHARACTER_PROFILES.mod, a:123, b:133, jaw:.82, chin:.61, cheek:1.04, forehead:.92, eyes:19, eyeH:7.5, eyeY:4, eyeGap:40, iris:'#5a594d', nose:1.14, mouth:1.06, shoulders:106, waist:94, body:.99, neck:33},
  board06: {...CHARACTER_PROFILES.exec, a:101, b:144, jaw:.66, chin:.44, cheek:.91, forehead:.94, eyes:21, eyeH:10, eyeY:1, eyeGap:34, iris:'#6d4b38', nose:.86, mouth:.96, shoulders:85, waist:68, body:1.02, neck:23},
  board07: {...CHARACTER_PROFILES.engineer, a:108, b:146, jaw:.78, chin:.59, cheek:.91, forehead:.91, eyes:18.5, eyeH:9, eyeY:3, eyeGap:36, iris:'#627271', nose:1.04, mouth:.92, shoulders:94, waist:73, body:1.03, neck:27},
  board08: {...CHARACTER_PROFILES.senator, a:103, b:143, jaw:.64, chin:.46, cheek:.98, forehead:.90, eyes:19, eyeH:8, eyeY:5, eyeGap:35, iris:'#748481', nose:.98, mouth:.96, shoulders:84, waist:75, body:1, neck:23},
  board09: {...CHARACTER_PROFILES.guard, a:116, b:130, jaw:.91, chin:.72, cheek:.95, forehead:.94, eyes:18, eyeH:8.5, eyeY:-1, eyeGap:38, iris:'#574434', nose:.98, mouth:1.01, shoulders:103, waist:78, body:1, neck:31},
  board10: {...CHARACTER_PROFILES.senator, a:99, b:151, jaw:.72, chin:.53, cheek:.88, forehead:.91, eyes:17, eyeH:7.5, eyeY:6, eyeGap:33, iris:'#685444', nose:1.16, mouth:.88, shoulders:83, waist:67, body:1.04, neck:24},

  office01: {...CHARACTER_PROFILES.hero, a:107, b:137, jaw:.74, chin:.53, cheek:.95, forehead:.94, eyes:21, eyeH:10.5, eyeY:1, eyeGap:36, iris:'#5c4d3d', nose:.89, mouth:.97, shoulders:91, waist:72, body:1.01, neck:25},
  office02: {...CHARACTER_PROFILES.exec, a:101, b:136, jaw:.62, chin:.42, cheek:.94, forehead:.94, eyes:21, eyeH:11, eyeY:1, eyeGap:34, iris:'#57402e', nose:.81, mouth:.98, shoulders:83, waist:67, body:.99, neck:22},
  office03: {...CHARACTER_PROFILES.guard, a:122, b:136, jaw:.88, chin:.69, cheek:1.01, forehead:.91, eyes:18, eyeH:8, eyeY:3, eyeGap:40, iris:'#554b3f', nose:1.06, mouth:1.03, shoulders:111, waist:89, body:1, neck:34},
  office04: {...CHARACTER_PROFILES.engineer, a:97, b:144, jaw:.66, chin:.47, cheek:.87, forehead:.92, eyes:19, eyeH:10, eyeY:0, eyeGap:32, iris:'#56726c', nose:.91, mouth:.88, shoulders:80, waist:64, body:1.03, neck:22},
  office05: {...CHARACTER_PROFILES.mod, a:114, b:129, jaw:.68, chin:.46, cheek:1.04, forehead:.94, eyes:21, eyeH:10, eyeY:3, eyeGap:37, iris:'#654c38', nose:.85, mouth:1.02, shoulders:91, waist:82, body:.98, neck:25},

  everyday01: {...CHARACTER_PROFILES.hero, a:102, b:135, jaw:.71, chin:.51, cheek:.93, forehead:.95, eyes:20, eyeH:11, eyeY:0, eyeGap:34, iris:'#614532', nose:.88, mouth:.95, shoulders:89, waist:68, body:1, neck:24},
  everyday02: {...CHARACTER_PROFILES.engineer, a:99, b:140, jaw:.63, chin:.43, cheek:.95, forehead:.94, eyes:21, eyeH:10.5, eyeY:2, eyeGap:33, iris:'#6f7464', nose:.85, mouth:.98, shoulders:82, waist:70, body:1.01, neck:22},
  everyday03: {...CHARACTER_PROFILES.guard, a:120, b:134, jaw:.87, chin:.68, cheek:1.03, forehead:.92, eyes:19, eyeH:8.5, eyeY:2, eyeGap:39, iris:'#594836', nose:1.1, mouth:1.05, shoulders:107, waist:91, body:1, neck:32},
  everyday04: {...CHARACTER_PROFILES.senator, a:106, b:146, jaw:.71, chin:.54, cheek:.97, forehead:.89, eyes:18, eyeH:8, eyeY:5, eyeGap:35, iris:'#84938d', nose:1.11, mouth:.93, shoulders:87, waist:77, body:1.02, neck:26},
  everyday05: {...CHARACTER_PROFILES.mod, a:111, b:132, jaw:.65, chin:.44, cheek:1.02, forehead:.94, eyes:21, eyeH:11, eyeY:2, eyeGap:36, iris:'#624b36', nose:.82, mouth:1, shoulders:86, waist:76, body:.99, neck:23},

  mom: {...CHARACTER_PROFILES.hero, a:112, b:135, jaw:.64, chin:.45, cheek:1.03, forehead:.94, eyes:21, eyeH:9.5, eyeY:4, eyeGap:37, iris:'#6a7b68', nose:.91, mouth:1.02, shoulders:91, waist:83, body:.99, neck:25}
};

export const EXTRA_OUTFITS = {
  // Board: ten individually cast directors, each with a complete coordinated suit.
  board01: {identity:'board01', tunic:'#354c61', lapel:'#24364c', inner:'#e8e0d1', skin:'#d8aa8b', hair:'#4c3c35', hairStyle:'bob', blazer:true, earrings:true, pants:'#354354', shoes:'#5b3939', R:'tablet'},
  board02: {identity:'board02', tunic:'#3d4149', lapel:'#30333c', inner:'#e4e3dc', tie:'#b48a44', skin:'#9b6d51', hair:'#2c2b2a', hairStyle:'buzz', blazer:true, glasses:'smart', pants:'#363a42', shoes:'#4a3530'},
  board03: {identity:'board03', tunic:'#2c3f58', lapel:'#223248', inner:'#d9d9e2', tie:'#74556b', skin:'#edc09e', hair:'#25282e', hairStyle:'slick', blazer:true, glasses:'nerd', pants:'#2a384c', shoes:'#292d38', R:'subpoena'},
  board04: {identity:'board04', tunic:'#426b65', lapel:'#31534e', inner:'#f0e6cf', skin:'#bd825e', hair:'#29272a', hairStyle:'bun', blazer:true, earrings:true, pants:'#365851', shoes:'#583e32'},
  board05: {identity:'board05', tunic:'#735e4d', lapel:'#584b41', inner:'#ede3d0', tie:'#7f3f42', skin:'#e2b699', hair:'#aaa49b', hairStyle:'bald', brows:'#777168', blazer:true, stout:true, pants:'#625143', shoes:'#4a342a'},
  board06: {identity:'board06', tunic:'#733b50', lapel:'#552b40', inner:'#e1d4c1', skin:'#925e42', hair:'#252528', hairStyle:'curly', blazer:true, earrings:true, pants:'#59313e', shoes:'#352c33', R:'tablet'},
  board07: {identity:'board07', tunic:'#4d5b50', lapel:'#39483c', inner:'#d7e0dc', tie:'#be9271', skin:'#d3a58c', hair:'#463735', hairStyle:'parted', blazer:true, stubble:true, pants:'#414f43', shoes:'#624835'},
  board08: {identity:'board08', tunic:'#6b6b78', lapel:'#50515f', inner:'#eee4da', skin:'#edcbb4', hair:'#c7c3b9', hairStyle:'wavy', brows:'#8a847d', blazer:true, glasses:'gold', earrings:true, pants:'#575867', shoes:'#51404d'},
  board09: {identity:'board09', tunic:'#273c4a', lapel:'#1d2e39', inner:'#e4d3bc', tie:'#328b8a', skin:'#b27a54', hair:'#302a29', hairStyle:'quiff', blazer:true, pants:'#24343f', shoes:'#46312c'},
  board10: {identity:'board10', tunic:'#584d66', lapel:'#40384f', inner:'#e5d7cb', tie:'#a25f47', skin:'#c19678', hair:'#b9b7af', hairStyle:'silver', brows:'#77736c', blazer:true, glasses:'smart', pants:'#493f57', shoes:'#332d38'},

  // Office/factory side actors: useful in Tesla, SpaceX, corridors and the lab.
  office01: {identity:'office01', tunic:'#53787c', inner:'#dfd6c0', skin:'#d6a576', hair:'#37302d', hairStyle:'parted', casual:true, badge:'#80a9a4', pants:'#344c58', shoes:'#7d654c', R:'tablet'},
  office02: {identity:'office02', tunic:'#b87954', inner:'#f1e4ca', skin:'#986b4d', hair:'#28272a', hairStyle:'curly', casual:true, earrings:true, badge:'#65868d', pants:'#3b4356', shoes:'#ded6bd', R:'phone'},
  office03: {identity:'office03', tunic:'#425568', inner:'#cfc9b7', skin:'#c6a17f', hair:'#443f39', hairStyle:'bald', vest:true, stubble:true, stout:true, badge:'#c18d4b', pants:'#394959', shoes:'#6a5039'},
  office04: {identity:'office04', tunic:'#dbe1dc', inner:'#647d8a', skin:'#efd0b0', hair:'#7a4b36', hairStyle:'long', labCoat:true, glasses:'smart', badge:'#5f91a2', pants:'#52616d', shoes:'#40515b', R:'tablet'},
  office05: {identity:'office05', tunic:'#6b5b88', hoodCol:'#514669', skin:'#d19f78', hair:'#3d2d2e', hairStyle:'bob', hoodie:true, glasses:'nerd', badge:'#bd9570', pants:'#42455b', shoes:'#cbbfa7'},

  // Everyday side actors: varied civilian silhouettes for street, cafe and home scenes.
  everyday01: {identity:'everyday01', tunic:'#bd7952', hoodCol:'#92583d', skin:'#bb855c', hair:'#2c2a2b', hairStyle:'messy', hoodie:true, pants:'#415b70', denim:true, shoes:'#d9d4bd', R:'phone'},
  everyday02: {identity:'everyday02', tunic:'#648682', inner:'#e6d9bd', skin:'#e5ba96', hair:'#5f3e31', hairStyle:'long', cardigan:true, earrings:true, pants:'#7d6d59', shoes:'#795144', R:'tablet'},
  everyday03: {identity:'everyday03', tunic:'#54789a', inner:'#dcd8c5', skin:'#b5805c', hair:'#40322e', hairStyle:'buzz', casual:true, denim:true, stubble:true, stout:true, pants:'#434c56', shoes:'#735239'},
  everyday04: {identity:'everyday04', tunic:'#78624b', inner:'#d5b789', skin:'#e2b79c', hair:'#c1b9aa', hairStyle:'silver', brows:'#8c8274', casual:true, glasses:'gold', pants:'#454e4b', shoes:'#594337'},
  everyday05: {identity:'everyday05', tunic:'#bd9470', inner:'#eee2c8', skin:'#aa7655', hair:'#3c2d2a', hairStyle:'bun', casual:true, earrings:true, pants:'#6d7e72', shoes:'#d9cdb5', R:'phone'},

  // A practical American middle-class mom: cardigan, tee, jeans and everyday sneakers.
  mom: {identity:'mom', tunic:'#81977c', inner:'#eee3ce', skin:'#e6bc9c', hair:'#8a5138', hairStyle:'wavy', cardigan:true, casual:true, earrings:true, pants:'#4a6479', denim:true, shoes:'#e0d8c3', R:'phone'}
};

export const EXTRA_CAST = [
  {key:'board01', name:'Evelyn — Board Chair', beat:'Calm authority', detail:'Angular chestnut bob · midnight blue suit · ivory shell', note:'A measured chairwoman who can stop the room with one raised eyebrow.', group:'board'},
  {key:'board02', name:'Marcus — Finance Director', beat:'Checks the numbers', detail:'Broad jaw · charcoal suit · muted gold tie · steel frames', note:'A solid, analytical CFO with a low, skeptical gaze and restrained gestures.', group:'board'},
  {key:'board03', name:'Daniel — General Counsel', beat:'Finds the fine print', detail:'Long narrow face · navy suit · plum tie · dark frames', note:'A precise attorney who carries the notice and reacts with dry disbelief.', group:'board'},
  {key:'board04', name:'Priya — Technology Director', beat:'Asks the hard question', detail:'High bun · compact face · deep teal suit · cream blouse', note:'A younger technical director with a direct gaze and a quick, knowing smile.', group:'board'},
  {key:'board05', name:'Walter — Lead Investor', beat:'Wants a return', detail:'Bald crown · broad build · taupe suit · wine red tie', note:'A seasoned investor with a rounder face, heavy brows and a skeptical squint.', group:'board'},
  {key:'board06', name:'Naomi — Operations Director', beat:'Keeps things moving', detail:'Rounded curls · tall cheekbones · burgundy suit · pearl studs', note:'A decisive operator whose expressions move from patient to sharply unimpressed.', group:'board'},
  {key:'board07', name:'Adrian — Strategy Director', beat:'Pitches the next move', detail:'Side part · long face · olive suit · copper tie', note:'A lean strategist with a little stubble and a carefully practiced sales smile.', group:'board'},
  {key:'board08', name:'Helen — Independent Director', beat:'Has seen this before', detail:'Silver waves · soft cheeks · slate suit · gold frames', note:'An experienced director with warm eyes and a devastatingly quiet side-eye.', group:'board'},
  {key:'board09', name:'Rafael — Commercial Director', beat:'Closes the deal', detail:'Square chin · dark quiff · ink blue suit · teal tie', note:'An energetic commercial lead with wide shoulders and a confident half-smile.', group:'board'},
  {key:'board10', name:'Victor — Founding Director', beat:'Protects the company', detail:'Silver side part · narrow face · aubergine suit · rust tie', note:'An older founding director with a thoughtful frown and a steady, deliberate delivery.', group:'board'},

  {key:'office01', name:'Owen — Product Engineer', beat:'Explains the prototype', detail:'Side part · petrol work shirt · ID badge · tablet', note:'A relaxed colleague for lab demonstrations, desk chats and technical reactions.', group:'office'},
  {key:'office02', name:'Maya — Project Coordinator', beat:'Keeps the schedule', detail:'Short curls · terracotta top · navy trousers · ID badge', note:'An expressive coordinator for office scenes, phone calls and hallway interruptions.', group:'office'},
  {key:'office03', name:'Frank — Factory Supervisor', beat:'Gets it built', detail:'Bald crown · strong jaw · blue work vest · practical shoes', note:'A broad, grounded factory veteran with a little stubble and a patient stare.', group:'office'},
  {key:'office04', name:'Claire — Lab Technician', beat:'Checks the experiment', detail:'Long copper hair · white lab coat · slim glasses · tablet', note:'A slender technician for test benches, lab discoveries and uneasy glances.', group:'office'},
  {key:'office05', name:'Jules — Design Associate', beat:'Spots the problem', detail:'Dark bob · plum hoodie · rounder face · dark glasses', note:'A comfortable, casual office colleague with a dry smile and quick reactions.', group:'office'},

  {key:'everyday01', name:'Leo — Student', beat:'Always on his phone', detail:'Tousled dark hair · rust hoodie · blue jeans · cream sneakers', note:'A younger civilian for crowds, street scenes and amused background reactions.', group:'everyday'},
  {key:'everyday02', name:'Grace — Teacher', beat:'Listens, then reacts', detail:'Long brown hair · teal cardigan · oatmeal tee · tablet', note:'A warm civilian with an oval face, useful in a cafe, at home or on the street.', group:'everyday'},
  {key:'everyday03', name:'Ben — Local Contractor', beat:'Sizes up the situation', detail:'Close cropped hair · broad build · chambray shirt · work shoes', note:'An everyday working dad with a square jaw, soft stubble and an easy grin.', group:'everyday'},
  {key:'everyday04', name:'Arthur — Retired Neighbor', beat:'Quietly unimpressed', detail:'Silver hair · long face · sand overshirt · gold frames', note:'An older neighbor with relaxed posture and a slow, skeptical eyebrow raise.', group:'everyday'},
  {key:'everyday05', name:'Nina — Cafe Regular', beat:'Hears the gossip', detail:'Dark bun · camel top · sage trousers · cream sneakers', note:'A round cheeked civilian for cafe conversations, crowds and phone reactions.', group:'everyday'},

  {key:'mom', name:'Mom — American Middle-Class', beat:'Warm, practical, perceptive', detail:'Auburn waves · sage cardigan · cream tee · blue jeans · sneakers', note:'A middle-aged American mom with soft cheeks and kind eyes, dressed for an ordinary day at home or running errands.', group:'family'}
];

Object.assign(OUTFITS, EXTRA_OUTFITS);
Object.assign(CHARACTER_PROFILES, EXTRA_PROFILES);

function webbing(g,cx,cy,rx,ry){
 g.save();g.globalAlpha=.62;
 for(let i=0;i<12;i++){let t=i*Math.PI/6;cvLine(g,[['moveTo',cx,cy],['lineTo',cx+Math.cos(t)*rx,cy+Math.sin(t)*ry]],'#392637',1.7);}
 for(let r=.23;r<1.1;r+=.23){let a=[];for(let i=0;i<=48;i++){let t=i*Math.PI/24;a.push([i?'lineTo':'moveTo',cx+Math.cos(t)*rx*r,cy+Math.sin(t)*ry*r]);}cvLine(g,a,'#392637',1.6);}g.restore();
}
function drawMask(g,O,P,opts){
 g.save();cvPath(g,headContour(P,0));g.clip();webbing(g,0,8,P.a*1.5,P.b*1.5);g.restore();
 const narrow=['angry','squint','exhausted','stubborn'].includes(opts.expr),wide=['shock','hyped'].includes(opts.expr);
 for(const side of [-1,1]){g.save();let y=wide?-22:-8,h=wide?52:narrow?13:35;if(['happy','laugh','smirk'].includes(opts.expr))h=22;if(['sad','worried'].includes(opts.expr))y=side<0?-18:-10;if(opts.expr==='wink'&&side>0)h=3;let eye=[['moveTo',side*14,y+7],['quadraticCurveTo',side*46,y-8,side*88,y-22],['quadraticCurveTo',side*82,y+h+10,side*48,y+h],['quadraticCurveTo',side*24,y+h,side*14,y+7],['closePath']];cvShape(g,eye,'#f1f7ed','#172639',7);cvLine(g,[['moveTo',side*29,y+7],['quadraticCurveTo',side*49,y+1,side*73,y-9]],'#ffffff',3);g.restore();}
}
function drawSuit(g,O,cx,top,bottom,w){
 for(const side of [-1,1])cvShape(g,[['moveTo',cx+side*w,top+60],['lineTo',cx+side*38,top+122],['lineTo',cx+side*39,bottom-30],['lineTo',cx+side*w,bottom],['closePath']],'#153857',null,0);
 webbing(g,cx,top+67,w*1.3,200);
 cvEllipse(g,cx,top+78,7,12,'#172539');cvEllipse(g,cx,top+96,10,15,'#172539');
 for(const side of [-1,1])for(let i=0;i<4;i++)cvLine(g,[['moveTo',cx+side*5,top+80+i*6],['lineTo',cx+side*(23+i*3),top+63+i*15],['lineTo',cx+side*(28+i*3),top+44+i*25]],'#172539',3.5);
}
CHARACTER_PROFILES.peter={...CHARACTER_PROFILES.hero,a:102,b:141,jaw:.72,chin:.48,eyes:21,eyeH:10,eyeGap:36,nose:1.08,mouth:1.1,shoulders:83,waist:56,neck:23,iris:'#735137'};
CHARACTER_PROFILES.gwen={...CHARACTER_PROFILES.hero,a:103,b:132,jaw:.66,chin:.49,eyes:22,eyeGap:37,nose:.76,mouth:.92,shoulders:78,waist:64,iris:'#65928b'};
CHARACTER_PROFILES.child={...CHARACTER_PROFILES.hero,a:116,b:119,jaw:.81,chin:.66,eyes:24,eyeH:13,eyeGap:40,nose:.61,shoulders:71,waist:66,neck:22,iris:'#735136'};
const suit={identity:'peter',spiderSuit:true,tunic:'#ba2944',skin:'#ba2944',hair:'#46302b',hairStyle:'quiff',pants:'#183c61',shoes:'#b72c43'};
OUTFITS.spidy={...suit,masked:true};OUTFITS.peter={...suit,faceSkin:'#e7b798'};
OUTFITS.peterCasual={identity:'peter',tunic:'#29465b',inner:'#d4c8b5',skin:'#e7b798',hair:'#46302b',hairStyle:'quiff',cardigan:true,pants:'#3a4351',shoes:'#b5aaa0'};
OUTFITS.gwen={identity:'gwen',tunic:'#b6a18b',inner:'#273b47',skin:'#f0c7aa',hair:'#dec47d',hairStyle:'long',cardigan:true,pants:'#263744',shoes:'#413538'};
OUTFITS.child={identity:'child',tunic:'#edbd3c',skin:'#c9926b',hair:'#47312b',hairStyle:'messy',raincoat:true,hoodie:true,hoodCol:'#ce982a',pants:'#38576a',shoes:'#3688b4'};
export const SPIDY_CAST=[
 {key:'spidy',name:'Spider-Man',role:'Masked hero · bare wrists / full / empty',group:'Principals'},
 {key:'peter',name:'Peter · unmasked suit',role:'Andrew Garfield-inspired face · shared hero identity',group:'Principals'},
 {key:'peterCasual',name:'Peter · everyday',role:'Same face · civilian wardrobe',group:'Principals'},
 {key:'gwen',name:'Gwen Stacy',role:'Blonde waves · warm coat · teal eyes',group:'Principals'},
 {key:'child',name:'Milo · rescue child',role:'Age 7 · yellow raincoat · teal backpack',group:'Principals'},
 ...['everyday01','everyday02','everyday03','everyday04','everyday05','mom','office01','office02','office03','office04','office05','board02','board04','board05','board06'].map((k,i)=>({key:'civilian'+String(i+1).padStart(2,'0'),name:['Leo · selfie fan','Grace · teacher','Ben · contractor','Arthur · neighbor','Nina · café regular','Ruth · parent','Owen · commuter','Maya · photographer','Frank · delivery rider','Claire · student','Jules · music fan','Marcus · office worker','Priya · shopper','Walter · shopkeeper','Naomi · local artist'][i],role:'NYC ensemble · distinct face and silhouette',group:'City',source:k})),
 {key:'miniSpider',name:'Pip · tiny spider',role:'Eight legs · ceiling descent · lens greeting',group:'Outro'}];
for(const c of SPIDY_CAST.filter(c=>c.source)){OUTFITS[c.key]={...OUTFITS[c.source],badge:null,R:c.key==='civilian01'||c.key==='civilian08'?'phone':'hang',L:'hang',blazer:false,tie:null,casual:true};}
// Additional street ensemble: independent face proportions and wardrobe definitions.
const CITY_ADDITIONS = [
 ['Diego · bike messenger','quiff','#976344','#25272b','#cb7147','#334b58',104,144,.83,.58,22,91,68,{vest:true,inner:'#ddd2b9'}],
 ['Amara · florist','bun','#744b38','#28232b','#799566','#665345',115,125,.75,.62,23,86,77,{cardigan:true,inner:'#f0d7ab',earrings:true}],
 ['Mei · architect','bob','#e1b18d','#272731','#6d8494','#34435b',99,143,.67,.48,18,80,60,{glasses:'smart',casual:true,inner:'#eee1cb'}],
 ['Sam · skateboarder','messy','#d6a47d','#754632','#bd9a47','#425c70',111,130,.74,.55,21,89,75,{hoodie:true,hoodCol:'#917239',beanie:'#496e6a'}],
 ['Elena · bookseller','wavy','#c08a68','#9c6240','#805c80','#4b455c',108,139,.77,.61,19,83,73,{cardigan:true,inner:'#e4c9a5',glasses:'gold'}],
 ['Hassan · taxi driver','buzz','#b58158','#342a2b','#426f75','#414f50',124,132,.93,.75,17,113,93,{stout:true,stubble:true,casual:true,inner:'#d5c9b4'}],
 ['Iris · retired nurse','silver','#edc8ae','#c7c6c1','#af7482','#5a586c',114,137,.80,.63,20,85,80,{cardigan:true,inner:'#f1e2d3',glasses:'gold',brows:'#817a77'}],
 ['Andre · barista','curly','#805138','#252329','#b48c66','#4c5546',105,145,.72,.53,22,95,64,{casual:true,inner:'#f1dabb',stubble:true}],
 ['Sofia · dog walker','long','#d7a17c','#49332d','#599392','#5b6784',107,131,.70,.52,23,81,68,{hoodie:true,hoodCol:'#397676',earrings:true}],
 ['Noah · street musician','parted','#edc0a2','#a45936','#a35b43','#465465',101,151,.69,.48,18,88,63,{vest:true,inner:'#e0c9aa',glasses:'nerd'}]
];
for(const [i,entry] of CITY_ADDITIONS.entries()){
 const [name,hairStyle,skin,hair,tunic,pants,a,b,jaw,chin,eyes,shoulders,waist,details]=entry;
 const key='civilian'+String(i+16).padStart(2,'0');
 CHARACTER_PROFILES[key]={...CHARACTER_PROFILES.hero,a,b,jaw,chin,eyes,eyeGap:34+i%4*3,eyeH:9+i%3,nose:.78+i*.045,mouth:.88+i%4*.08,shoulders,waist,neck:23+i%3*3,iris:['#5c4436','#6f744d','#496675'][i%3]};
 OUTFITS[key]={identity:key,skin,hair,hairStyle,tunic,pants,shoes:['#d8cdb3','#665044','#384356'][i%3],...details};
 SPIDY_CAST.splice(SPIDY_CAST.length-1,0,{key,name,role:'NYC ensemble · '+hairStyle+' hair · independent face profile',group:'City'});
}
export function drawCharacter(g,key,opts={}){
 if(key==='miniSpider'){
  g.save();g.translate(300,610);let t=opts.time||0;g.translate(0,Math.sin(t*2)*9);
  cvLine(g,[['moveTo',0,-550],['lineTo',0,-60]],'#d1dae3',3);
  for(const side of [-1,1])for(let i=0;i<4;i++){let y=-35+i*27,a=Math.sin(t*4+i)*9;cvLine(g,[['moveTo',side*43,y],['quadraticCurveTo',side*(105+i*9),y-45+a,side*(126+i*8),y+30+a]],'#28314c',14);cvLine(g,[['moveTo',side*43,y],['quadraticCurveTo',side*(105+i*9),y-45+a,side*(126+i*8),y+30+a]],'#b72b43',8);}
  cvEllipse(g,0,10,68,74,clothPaint(g,'#b72b43',0,0,80,90),C2.ink,6);cvEllipse(g,0,49,46,27,'#254a76',C2.ink,3);
  for(const side of [-1,1]){cvEllipse(g,side*25,-16,19,25,'#f4f4e9',C2.ink,4);cvEllipse(g,side*23,-11,6,12,'#23324a');}g.restore();return;
 }
 g.save();if(key==='child'){g.translate(90,292.5);g.scale(.7,.7);cvRound(g,226,465,148,220,32,'#258b8e',C2.ink,6);}
 romanFront(new Pen(g),key,opts);g.restore();
}
