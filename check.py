# -*- coding: utf-8 -*-
"""Controle van een gebouwde dist-map: links, meta, ankerteksten, aanspreekvormen, dashes."""
import os, re, sys, html
from html.parser import HTMLParser

ROOT = sys.argv[1]
ALLOWED_HOSTS = set(sys.argv[2].split(",")) if len(sys.argv) > 2 else set()
ALLOWED_ANCHORS_LOWER = set(a.lower() for a in sys.argv[3].split("|")) if len(sys.argv) > 3 else set()

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.titles=[]; self.descs=[]; self.h1=0; self.canon=[]; self.ids=[]; self.imgs_noalt=0; self.text=[]; self._a=None
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if "id" in a: self.ids.append(a["id"])
        if tag=="a":
            self._a=[a.get("href",""),a.get("rel",""),a.get("target",""),""]
        if tag=="meta" and a.get("name")=="description": self.descs.append(a.get("content",""))
        if tag=="link" and a.get("rel")=="canonical": self.canon.append(a.get("href",""))
        if tag=="h1": self.h1+=1
        if tag=="img" and not a.get("alt"): self.imgs_noalt+=1
        if tag=="title": self._t=True
    def handle_endtag(self, tag):
        if tag=="a" and self._a: self.links.append(tuple(self._a)); self._a=None
        if tag=="title": self._t=False
    def handle_data(self, d):
        if getattr(self,"_t",False): self.titles.append(d)
        if self._a: self._a[3]+=d
        self.text.append(d)

pages={}
for dp,_,fs in os.walk(ROOT):
    for f in fs:
        if f.endswith(".html"):
            p=os.path.join(dp,f); rel="/"+os.path.relpath(p,ROOT).replace("index.html","").replace("\\","/")
            pages[rel]=open(p,encoding="utf-8").read()

errs=[]; titles={}; descs={}
inbound={k:0 for k in pages}
for rel,src in pages.items():
    p=P(); p.feed(src)
    t="".join(p.titles).strip()
    if not t: errs.append((rel,"geen title"))
    if t in titles: errs.append((rel,"dubbele title met "+titles[t]))
    titles[t]=rel
    if len(p.descs)!=1: errs.append((rel,"aantal descriptions %d"%len(p.descs)))
    else:
        d=p.descs[0]
        if d in descs: errs.append((rel,"dubbele description met "+descs[d]))
        descs[d]=rel
        if rel!="/404.html" and not 70<=len(d)<=165: errs.append((rel,"description lengte %d"%len(d)))
    if not 20<=len(t)<=70: errs.append((rel,"title lengte %d"%len(t)))
    if p.h1!=1: errs.append((rel,"h1 aantal %d"%p.h1))
    if len(p.canon)!=1 and rel!="/404.html": errs.append((rel,"canonical aantal %d"%len(p.canon)))
    if len(p.ids)!=len(set(p.ids)): errs.append((rel,"dubbele id's"))
    if p.imgs_noalt: errs.append((rel,"img zonder alt"))
    for href,relattr,target,anchor in p.links:
        anchor=anchor.strip()
        if not href: errs.append((rel,"lege href")); continue
        if href.startswith("http"):
            host=re.sub(r"^https?://([^/]+).*$",r"\1",href)
            if ALLOWED_HOSTS and host not in ALLOWED_HOSTS: errs.append((rel,"host niet toegestaan: "+href))
            if "noopener" not in relattr: errs.append((rel,"geen noopener: "+href))
            if anchor!=href and anchor.lower() not in ALLOWED_ANCHORS_LOWER: errs.append((rel,"ankertekst afwijkend: %s -> %s"%(anchor,href)))
        elif href.startswith("mailto:"): pass
        elif href.startswith("#"):
            if href[1:] not in p.ids: errs.append((rel,"anker ontbreekt "+href))
        else:
            path=href.split("#")[0]
            if path.endswith(".xml") or path.endswith(".svg"):
                if not os.path.exists(os.path.join(ROOT,path.strip("/"))): errs.append((rel,"bestand ontbreekt "+href))
            elif path not in pages: errs.append((rel,"interne link kapot "+href))
            else: inbound[path]+=1
    txt=html.unescape(re.sub(r"<[^>]+>"," ",re.sub(r"<(script|style)[^>]*>.*?</\1>"," ",src,flags=re.S)))
    for ch,name in (("\u2014","em-dash"),("\u2013","en-dash")):
        if ch in txt: errs.append((rel,name))
    for w in ("lorem","dummy","placeholder","TODO"):
        if re.search(r"\b"+w+r"\b",txt,re.I): errs.append((rel,"dummytekst "+w))
    for m in ([] if rel.startswith("/blog/") and rel!="/blog/" else re.finditer(r"\b(je|jij|jouw|jullie|u|uw|wij|we|ons|onze)\b",txt)):
        errs.append((rel,"aanspreekvorm/wij-vorm: '%s' bij '%s'"%(m.group(1),txt[max(0,m.start()-40):m.end()+20].replace("\n"," "))))
for k,v in inbound.items():
    if v==0 and k not in ("/404.html",): errs.append((k,"verweesd"))
sm=os.path.join(ROOT,"sitemap.xml")
if os.path.exists(sm):
    locs=set(re.findall(r"<loc>https?://[^/]+(/[^<]*)</loc>",open(sm,encoding="utf-8").read()))
    for k in pages:
        if k!="/404.html" and k not in locs: errs.append((k,"niet in sitemap"))
    for l in locs:
        if l not in pages: errs.append((l,"sitemap wijst naar onbekende pagina"))
for e in sorted(set(errs)): print("%-40s %s"%e)
print("pagina's: %d, meldingen: %d"%(len(pages),len(set(errs))))
sys.exit(1 if errs else 0)
