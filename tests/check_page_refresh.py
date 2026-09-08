"""Firefox check for advisor/initiative parity and themed secondary pages."""
from pathlib import Path
from time import sleep
from browser_check import Driver

d=Driver()
try:
 for width in (1440,390):
  d.resize(width,1000)
  d.navigate('http://127.0.0.1:8080/index.html');sleep(.5)
  for _ in range(5):
   assert d.execute("const a=document.querySelector('.advisor-card.is-active').getBoundingClientRect(),b=document.querySelector('.advisor-grid').getBoundingClientRect(),n=document.querySelector('.advisor-card.is-next').getBoundingClientRect();return Math.abs(a.x+a.width/2-b.x-b.width/2)<1&&a.width>n.width")
   assert d.execute("const a=getComputedStyle(document.querySelector('.advisor-card.is-active'));return innerWidth<=767?a.gridTemplateColumns.split(' ').length===1:a.gridTemplateColumns.split(' ').length===2")
   assert d.execute("return [...document.querySelectorAll('.advisor-card')].every(c=>{const b=c.querySelector('.advisor-body'),h=c.querySelector('h3'),i=c.querySelector('.advisor-impact');return b.scrollHeight<=b.clientHeight&&h.scrollWidth<=h.clientWidth&&i.textContent.length>=110&&i.textContent.length<=190})")
   d.execute("document.querySelector('.advisor-next').click()");sleep(.35)
  for page in ('about-us','upcoming'):
   d.navigate(f'http://127.0.0.1:8080/pages/{page}.html');sleep(.6)
   assert d.execute('return document.documentElement.scrollWidth<=innerWidth'), (width,page)
   assert d.execute("return document.querySelector('.page-hero').clientHeight>300"), (width,page)
   assert d.execute("return document.querySelectorAll('.site-footer .footer-column a').length===8 && getComputedStyle(document.querySelector('.site-footer')).backgroundColor==='rgb(25, 21, 43)'"), (width,page)
   if page=='about-us':
    assert d.execute("return document.querySelector('.founder-card img').clientHeight>250"), (width,page)
    assert d.execute("const i=[...document.querySelectorAll('.story-images img')],c=[...document.querySelectorAll('.story-images figcaption')];return i.length===4&&c.length===4&&new Set(i.map(x=>x.currentSrc)).size===4&&c.every(x=>x.textContent.trim().length>25)"), (width,page)
    assert d.execute("return !document.querySelector('.editorial-main>.closing')"), (width,page)
    if width>1000:
     assert d.execute("return document.querySelector('.page-hero').clientHeight<=570"), (width,page)
     assert d.execute("const i=[...document.querySelectorAll('.story-images img')].map(x=>x.getBoundingClientRect());return Math.abs(i[0].top-i[1].top)<2&&Math.abs(i[2].top-i[3].top)<2&&i[2].top>i[0].bottom+15&&i.every(r=>Math.abs(r.width/r.height-1)<.03)"), (width,page)
     assert d.execute("const g=document.querySelector('.story-images').getBoundingClientRect(),c=document.querySelector('.story-card').getBoundingClientRect();return g.width/c.width>=.86&&g.left>=c.left&&g.right<=c.right"), (width,page)
     assert d.execute("return Math.abs(document.querySelector('.page-hero-copy').offsetHeight-document.querySelector('.about-hero-media').offsetHeight)<2")
     assert d.execute("const h=document.querySelector('.page-hero').getBoundingClientRect(),p=document.querySelector('.page-proof').getBoundingClientRect(),imgs=[...document.querySelectorAll('.about-hero-media img')];return p.top>=h.bottom-1&&imgs.every(i=>i.getBoundingClientRect().bottom<=h.bottom+1)"), (width,page)
     assert d.execute("const i=document.querySelector('.founder-card>img').getBoundingClientRect(),c=document.querySelector('.founder-copy').getBoundingClientRect();return c.left-i.right>=20"), (width,page)
   else: assert d.execute("return document.querySelectorAll('.event-card').length===5&&[...document.querySelectorAll('details')].every(e=>e.open)"), (width,page)
   d.screenshot(Path(f'/home/kai/General/work/IYOF/{page}-clean-{width}.png'))
  print(width,'PASS: advisor structure and clean secondary pages fit')
finally:d.close()
