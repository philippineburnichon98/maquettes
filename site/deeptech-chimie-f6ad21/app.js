(function(){
/* réseau moléculaire animé */
document.querySelectorAll('canvas[data-mol]').forEach(function(cv){
  var ctx=cv.getContext('2d'),W,H,dpr=Math.min(window.devicePixelRatio||1,2),pts=[],rings=[],mx=-1e4,my=-1e4,reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  function size(){var r=cv.getBoundingClientRect();W=r.width;H=r.height;cv.width=W*dpr;cv.height=H*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);
    var n=Math.round(W*H/16000);pts=[];for(var i=0;i<n;i++)pts.push({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.25,vy:(Math.random()-.5)*.25,r:Math.random()*1.6+1,c:Math.random()<.12});
    rings=[];for(var j=0;j<Math.max(3,Math.round(W/320));j++)rings.push({x:W*(.45+Math.random()*.55),y:Math.random()*H*.8,s:18+Math.random()*22,a:Math.random()*6,v:(Math.random()-.5)*.002});}
  function hex(x,y,s,a){ctx.beginPath();for(var k=0;k<6;k++){var t=a+k*Math.PI/3;ctx.lineTo(x+s*Math.cos(t),y+s*Math.sin(t));}ctx.closePath();ctx.stroke();
    ctx.beginPath();ctx.arc(x,y,s*.55,0,6.283);ctx.stroke();}
  function frame(){ctx.clearRect(0,0,W,H);var d=130;
    for(var i=0;i<pts.length;i++){var p=pts[i];if(!reduce){p.x+=p.vx;p.y+=p.vy;}if(p.x<0||p.x>W)p.vx*=-1;if(p.y<0||p.y>H)p.vy*=-1;
      var dx=p.x-mx,dy=p.y-my,dm=Math.sqrt(dx*dx+dy*dy);if(dm<140){p.x+=dx/dm*.6;p.y+=dy/dm*.6;}
      for(var j=i+1;j<pts.length;j++){var q=pts[j],ex=p.x-q.x,ey=p.y-q.y,dd=ex*ex+ey*ey;if(dd<d*d){var o=1-Math.sqrt(dd)/d;ctx.strokeStyle='rgba(120,220,210,'+(o*.28)+')';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(q.x,q.y);ctx.stroke();}}}
    for(i=0;i<pts.length;i++){p=pts[i];ctx.fillStyle=p.c?'rgba(242,169,59,.95)':'rgba(140,240,230,.8)';ctx.beginPath();ctx.arc(p.x,p.y,p.c?p.r+1.2:p.r,0,6.283);ctx.fill();}
    ctx.strokeStyle='rgba(21,195,180,.35)';ctx.lineWidth=1.2;rings.forEach(function(r){if(!reduce)r.a+=r.v*10;hex(r.x,r.y,r.s,r.a);});
    if(!reduce)requestAnimationFrame(frame);}
  size();addEventListener('resize',size);cv.parentElement.addEventListener('mousemove',function(e){var r=cv.getBoundingClientRect();mx=e.clientX-r.left;my=e.clientY-r.top;});
  cv.parentElement.addEventListener('mouseleave',function(){mx=my=-1e4;});frame();
});
/* nav */
var top=document.querySelector('.top');function sc(){top.classList.toggle('solid',scrollY>30||document.body.dataset.solid==='1');}addEventListener('scroll',sc);sc();
var b=document.querySelector('.burger');if(b)b.onclick=function(){document.querySelector('.drawer').classList.toggle('on');top.classList.add('solid');};
/* apparition */
var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}});},{threshold:.15});
document.querySelectorAll('.rv,.chart').forEach(function(el){io.observe(el);});
/* compteurs */
var co=new IntersectionObserver(function(es){es.forEach(function(x){if(!x.isIntersecting)return;var el=x.target,t=+el.dataset.to,suf=el.dataset.suf||'',s=performance.now();co.unobserve(el);
  (function f(n){var k=Math.min(1,(n-s)/1400),v=Math.round(t*(1-Math.pow(1-k,3)));el.textContent=v+suf;if(k<1)requestAnimationFrame(f);})(s);});},{threshold:.5});
document.querySelectorAll('[data-to]').forEach(function(el){co.observe(el);});
/* accordéon */
document.querySelectorAll('.faq button').forEach(function(bt){bt.onclick=function(){var o=bt.getAttribute('aria-expanded')==='true';bt.setAttribute('aria-expanded',!o);bt.nextElementSibling.hidden=o;};});
})();
(function(){try{var q=location.search;if(/[?&]moi\b/.test(q))localStorage.setItem('fyce_moi','1');if(/[?&]pasmoi\b/.test(q))localStorage.removeItem('fyce_moi');if(localStorage.getItem('fyce_moi')==='1')return}catch(e){}
var s=document.createElement('script');s.defer=true;s.src='https://static.cloudflareinsights.com/beacon.min.js';s.setAttribute('data-cf-beacon','{"token": "d97afe693f1b460f8a964b23ec19fe6d"}');document.head.appendChild(s)})();
