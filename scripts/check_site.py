#!/usr/bin/env python3
"""Dependency-free regression checks for the static site's technical contract."""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://danieledorazio.it/'
LEGACY = {'consulenza-ambientale.html', 'efficienza-energetica.html'}

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.nodes, self.ids, self.headings = [], [], []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.nodes.append((tag, attrs))
        if 'id' in attrs: self.ids.append(attrs['id'])
        if re.fullmatch(r'h[1-6]', tag): self.headings.append(int(tag[1]))
    def meta(self, name):
        return [a.get('content', '') for t,a in self.nodes if t == 'meta' and name in (a.get('name'), a.get('property'))]


def check():
    errors = []
    pages = {p.name: Page(p.read_text()) for p in ROOT.glob('*.html')}
    titles, descriptions = [], []
    def require(condition, message):
        if not condition: errors.append(message)
    for name, page in pages.items():
        text = (ROOT/name).read_text()
        title = re.findall(r'<title>(.*?)</title>', text)
        require(len(title) == 1 and 0 < len(title[0]) <= 70, f'{name}: invalid or overlong title')
        titles += title
        desc = page.meta('description'); descriptions += desc
        require(len(desc) == 1 and bool(desc[0]), f'{name}: description missing')
        require(page.headings.count(1) == 1, f'{name}: must have one H1')
        require(all(b <= a+1 for a,b in zip(page.headings, page.headings[1:])), f'{name}: skipped heading level')
        require(len(page.ids) == len(set(page.ids)), f'{name}: duplicate ID')
        expected = ORIGIN + ('' if name == 'index.html' else name)
        canonical = [a.get('href') for t,a in page.nodes if t == 'link' and a.get('rel') == 'canonical']
        require(canonical == [expected], f'{name}: incorrect canonical')
        for key in ('og:title','og:description','og:url','og:image','og:image:alt','twitter:card'):
            require(len(page.meta(key)) == 1, f'{name}: {key} missing or duplicated')
        require(page.meta('og:url') == [expected], f'{name}: incorrect og:url')
        require('contenuto' in page.ids, f'{name}: skip destination missing')
        require(any(t=='a' and a.get('class')=='skip' for t,a in page.nodes), f'{name}: skip link missing')
        schemas = re.findall(r'<script type="application/ld\+json">(.*?)</script>',text)
        require(len(schemas) == 1, f'{name}: expected one WebPage schema')
        for data in schemas:
            schema=json.loads(data)
            require(schema.get('@type') == 'WebPage' and schema.get('url') == expected, f'{name}: incorrect WebPage schema')
        for tag,a in page.nodes:
            if tag=='script': require(a.get('type')=='application/ld+json', f'{name}: unexpected executable script')
            if tag=='img':
                require(bool(a.get('alt')), f'{name}: image without alt')
                require('width' in a and 'height' in a, f'{name}: image dimensions missing')
                require(not a.get('src','').startswith('http'), f'{name}: externally embedded image')
            for attr in ('href','src'):
                value=a.get(attr,'')
                if not value: continue
                require(not value.startswith(('http:','javascript:','tel:')), f'{name}: unsafe or unverified action {value}')
                require(not re.search(r'wa\.me|api\.whatsapp|whatsapp://',value), f'{name}: WhatsApp must remain inactive')
                if value.startswith('mailto:'):
                    require(urlsplit(value).path == 'info@danieledorazio.it', f'{name}: unexpected recipient')
                    continue
                parsed=urlsplit(value)
                if parsed.scheme or parsed.netloc: continue
                target=unquote(parsed.path)
                dest=ROOT/(target or name)
                if dest.is_dir(): dest=dest/'index.html'
                require(dest.is_file(), f'{name}: missing local resource {value}')
                if parsed.fragment:
                    require(dest.name in pages and unquote(parsed.fragment) in pages[dest.name].ids, f'{name}: missing fragment {value}')
            for candidate in a.get('srcset','').split(','):
                if candidate.strip(): require((ROOT/candidate.strip().split()[0]).is_file(), f'{name}: missing srcset asset')
        if name in LEGACY: require(page.meta('robots') == ['noindex,follow'], f'{name}: legacy page is indexable')
    require(len(titles)==len(set(titles)), 'Duplicate titles')
    require(len(descriptions)==len(set(descriptions)), 'Duplicate descriptions')
    urls=[n.text for n in ET.parse(ROOT/'sitemap.xml').findall('.//{*}loc')]
    expected_urls={ORIGIN+('' if n=='index.html' else n) for n in pages if n not in LEGACY}
    require(len(urls)==len(set(urls)) and set(urls)==expected_urls,'Sitemap does not match active pages')
    require('Sitemap: '+ORIGIN+'sitemap.xml' in (ROOT/'robots.txt').read_text(),'robots.txt sitemap missing')
    require((ROOT/'CNAME').read_text().strip()=='danieledorazio.it','Domain file changed')
    for error in errors: print('FAIL:',error)
    if errors: return 1
    print(f'PASS: {len(pages)} pages, {len(urls)} sitemap URLs; links, fragments, metadata, schema, images and inactive WhatsApp checked.')
    return 0

if __name__ == '__main__': sys.exit(check())
