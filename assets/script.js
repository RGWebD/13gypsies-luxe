(()=>{
const d=document,RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
const $=(s,c=d)=>c.querySelector(s),$$=(s,c=d)=>[...c.querySelectorAll(s)];

/* Live open/closed (America/New_York). Tue–Thu 5–9 PM, Fri–Sat 5–10 PM, closed Sun–Mon.
   Google flags Thanksgiving (Nov 26) and Black Friday (Nov 27) 2026: "hours might differ". */
const H={2:[1020,1260],3:[1020,1260],4:[1020,1260],5:[1020,1320],6:[1020,1320]};
const FLAG={'2026-11-26':'Thanksgiving','2026-11-27':'Black Friday','2026-12-24':'Christmas Eve','2026-12-31':'New Year’s Eve'};
const DN=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
function et(t=new Date()){const p=new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',year:'numeric',month:'2-digit',day:'2-digit',weekday:'long',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(t);const o={};p.forEach(x=>o[x.type]=x.value);return{day:DN.indexOf(o.weekday),min:(+o.hour%24)*60+(+o.minute),date:`${o.year}-${o.month}-${o.day}`}}
const fmt=m=>(Math.floor(m/60)%12||12)+' PM';
function status(){const n=et(),h=H[n.day];let st,t;
 if(h&&n.min>=h[0]&&n.min<h[1]){st='open';t='Open now · until '+fmt(h[1])}
 else if(h&&n.min<h[0]){st='closed';t='Opens today at 5 PM'}
 else{let k=1;while(!H[(n.day+k)%7])k++;st='closed';t='Closed now · opens '+(k===1?'tomorrow':DN[(n.day+k)%7])+' at 5 PM';const fd=et(new Date(Date.now()+k*864e5)).date;if(FLAG[fd])t+=' ('+FLAG[fd]+': hours may differ)'}
 if(FLAG[n.date]&&h){st='unk';t=FLAG[n.date]+': hours may differ, please call'}
 $$('[data-status]').forEach(el=>{['open','closed','unk'].forEach(c=>el.classList.toggle(c,c===st));$('span',el).textContent=t});
 $$('.hours tr').forEach(tr=>tr.classList.toggle('today',+tr.dataset.d===n.day))}
status();setInterval(status,60000);

/* header over hero -> solid; mobile bar after hero */
const hdr=$('[data-hdr]'),mbar=$('[data-mbar]'),hero=$('.hero');
function onScroll(){const y=scrollY,lim=hero?hero.offsetHeight-90:0;
 if(hero&&hdr){const s=y>lim;hdr.classList.toggle('solid',s);hdr.classList.toggle('over',!s)}
 if(mbar)mbar.classList.toggle('show',hero?y>hero.offsetHeight*.7:y>200)}
addEventListener('scroll',onScroll,{passive:true});onScroll();

/* quiet fade-up reveals */
const targets=$$('.intro>*,.pt-head,.atable>*,.house>*,.pv-tx,.reviews>*,.rs-in>*:not(.otw),.visit>*,.mn-hero>*,.mn-sec,.mn-cta>*');
if(!RM&&'IntersectionObserver' in window){targets.forEach(e=>e.classList.add('rv-up'));
 const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{rootMargin:'0px 0px -8% 0px'});
 targets.forEach(e=>io.observe(e))}

/* SIGNATURE: house-made pantry. Sticky arch; each step's photo rises in from below and settles. */
const pt=$('[data-pantry]');
if(pt&&!RM&&'IntersectionObserver' in window){pt.classList.add('live');
 const shots=$$('.pt-shot',pt),ticks=$$('.pt-ticks li',pt),steps=$$('.pt-step',pt);let cur=0;
 const set=i=>{if(i===cur)return;shots.forEach((s,j)=>{s.classList.toggle('was',j===cur);s.classList.toggle('on',j===i)});ticks.forEach((t,j)=>t.classList.toggle('on',j===i));
  steps.forEach((s,j)=>s.classList.toggle('on',j===i));const nw=$('.pt-now',pt);if(nw)nw.innerHTML=$('.pt-h',steps[i]).innerHTML;cur=i};
 steps[0].classList.add('on');
 const mob=()=>innerWidth<=980;
 let io;const mk=()=>{io&&io.disconnect();io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)set(+e.target.dataset.i)}),{rootMargin:mob()?'-66% 0px -26% 0px':'-48% 0px -48% 0px'});steps.forEach(s=>io.observe(s))};
 mk();let rw;addEventListener('resize',()=>{clearTimeout(rw);rw=setTimeout(mk,200)});
}

/* menu filter chips */
const chips=$$('.chip');chips.forEach(c=>c.addEventListener('click',()=>{const f=c.dataset.f;chips.forEach(x=>{const on=x===c;x.classList.toggle('on',on);x.setAttribute('aria-pressed',on)});
 $$('.mn-sec').forEach(s=>s.classList.toggle('off',f!=='all'&&s.dataset.k!==f))}));

/* OpenTable widget (official loader); theme by card width. Link buttons stay as fallback. */
$$('.otw[data-rid]').forEach(box=>{const w=box.clientWidth;const theme=w>=860?'wide':'tall';
 const s=d.createElement('script');s.async=true;s.src=`https://www.opentable.com/widget/reservation/loader?rid=${box.dataset.rid}&type=standard&theme=${theme}&color=1&dark=false&iframe=true&domain=com&lang=en-US&newtab=false&ot_source=Restaurant%20website`;
 s.onerror=()=>{const l=$('.otload',box);if(l)l.textContent='Use the button below to reserve on OpenTable.'};
 const mo=new MutationObserver(()=>{if($('iframe',box)){const l=$('.otload',box);l&&l.remove();mo.disconnect()}});mo.observe(box,{childList:true,subtree:true});
 box.appendChild(s)});

/* demo pill */
const dm=$('.demo');if(dm){try{if(sessionStorage.getItem('g13l-demo'))dm.remove()}catch(e){}
 const x=$('button',dm);x&&x.addEventListener('click',()=>{dm.remove();try{sessionStorage.setItem('g13l-demo','1')}catch(e){}})}
})();
