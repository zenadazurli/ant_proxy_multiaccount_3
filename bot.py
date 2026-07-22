#!/usr/bin/env python3
# bot.py - Multi-Account con Proxy Fissi (100 proxy)
# Proxy da ProxyScrape - 3qy2whd9kpkf

import os
import time
import sys
import json
import re
import requests
import asyncio
import random
import string
from playwright.async_api import async_playwright
from urllib.parse import unquote
from datetime import datetime
import imagehash
from PIL import Image
import io

# ============================================================
# CONFIGURAZIONE
# ============================================================
HEADLESS = os.environ.get("HEADLESS", "True").lower() == "true"
MAX_CONCURRENT = int(os.environ.get("MAX_CONCURRENT", "5"))
NUM_ACCOUNTS = int(os.environ.get("NUM_ACCOUNTS", "100"))

# ============================================================
# LISTA PROXY FISSI (DA PROXYSCRAPE)
# ============================================================
PROXY_LIST = [
    "3qy2whd9kpkf:exs0gc9mhv6jag0@209.50.180.147:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@216.26.238.93:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@216.26.253.103:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@209.50.163.25:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@209.50.168.163:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@209.50.172.154:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@209.50.176.204:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@216.26.224.34:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.54.173:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@216.26.226.119:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.41.96:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@45.3.34.191:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@216.26.236.23:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@216.26.254.64:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@209.50.167.49:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.37.212:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@45.3.32.26:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@65.111.22.109:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@216.26.226.84:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@216.26.225.140:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@45.3.32.188:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@216.26.234.5:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.35.180:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@216.26.232.130:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@65.111.31.98:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@209.50.175.47:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@45.3.44.208:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@216.26.243.109:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.42.209:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@209.50.163.206:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.167.19.188:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.49.7:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@209.50.166.81:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@45.3.38.249:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@45.3.33.127:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.40.83:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@217.181.90.152:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@65.111.20.101:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@65.111.3.146:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@216.26.241.57:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.52.120:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.33.196:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.46.105:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@209.50.178.107:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@217.181.91.242:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@45.3.41.74:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@151.123.178.114:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@65.111.25.54:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@65.111.29.133:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@209.50.185.97:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@209.50.175.14:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@209.50.163.241:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@45.3.44.204:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@45.3.43.27:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@209.50.161.203:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@65.111.26.250:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@209.50.181.86:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@216.26.251.54:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@209.50.170.80:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@209.50.163.7:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@217.181.90.251:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@45.3.46.66:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.34.223:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.167.25.235:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@65.111.15.236:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@45.3.55.164:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.61.51:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@45.3.38.125:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@216.26.244.79:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@65.111.21.2:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.57.198:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.61.91:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@65.111.5.163:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@151.123.176.222:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@65.111.10.170:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.59.53:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.61.10:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@45.3.38.3:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@65.111.13.225:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.56.189:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@209.50.191.255:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@45.3.54.74:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@216.26.250.37:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.56.254:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.46.246:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.42.9:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.52.78:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.43.231:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@216.26.253.254:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@65.111.22.176:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.53.100:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@45.3.35.63:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@209.50.171.106:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@216.26.237.237:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.48.129:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@193.56.28.26:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.49.80:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@104.207.47.70:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@216.26.248.133:3129",
    "3qy2whd9kpkf:exs0gc9mhv6jag0@209.50.174.237:3129",
]

# ============================================================
# GENERATORE DI ACCOUNT REALISTICI
# ============================================================
def genera_email_realistica():
    nomi = [
        "mario", "luca", "marco", "giuseppe", "antonio", "giovanni", 
        "francesco", "andrea", "alessandro", "roberto", "stefano", 
        "paolo", "simone", "davide", "matteo", "federico", "valentina",
        "chiara", "sara", "elena", "martina", "silvia", "alessia",
        "sabrina", "paola", "giulia", "francesca", "anna", "laura"
    ]
    cognomi = [
        "rossi", "russo", "ferrari", "esposito", "bianchi", "romano",
        "colombo", "ricci", "marino", "greco", "bruno", "gallo",
        "conti", "de luca", "mancini", "giordano", "rizzo", "lombardi",
        "barbieri", "fontana", "santoro", "mariani", "conte", "moretti"
    ]
    domini = ["libero.it", "gmail.com", "outlook.it", "yahoo.it", "tiscali.it"]
    
    nome = random.choice(nomi)
    cognome = random.choice(cognomi)
    dominio = random.choice(domini)
    anno = random.randint(1970, 2005)
    
    patterns = [
        f"{nome}.{cognome}@{dominio}",
        f"{nome}.{cognome}.{anno}@{dominio}",
        f"{nome}_{cognome}_{anno}@{dominio}",
        f"{nome}{cognome}{anno}@{dominio}",
        f"{nome[0]}.{cognome}@{dominio}",
    ]
    
    return random.choice(patterns).lower()

def genera_password_realistica():
    parole = [
        "sole", "luna", "stella", "cielo", "mare", "monte", 
        "fiore", "rosa", "amore", "vita", "pace", "gioia",
        "libertà", "sogno", "cuore", "anima", "falco", "aquila",
        "tigre", "leone", "lupo", "drago", "fenice"
    ]
    anni_comuni = ["1985", "1990", "1992", "1995", "2000", "2001", "2002", "2003", "2005"]
    speciali = ['!', '$', '#', '@', '&']
    
    parola = random.choice(parole)
    anno = random.choice(anni_comuni)
    speciale = random.choice(speciali)
    
    pattern = random.choice([
        f"{parola}{anno}",
        f"{parola}{anno}{speciale}",
        f"{parola}{speciale}{anno}",
        f"{parola.capitalize()}{anno}{speciale}",
    ])
    
    return pattern

def genera_account():
    email = genera_email_realistica()
    password = genera_password_realistica()
    return {
        "email": email,
        "password": password,
        "created": False,
        "balance": 0
    }

# ============================================================
# SALVATAGGIO CREDENZIALI
# ============================================================
def salva_credenziali(accounts, filename="accounts_created.txt"):
    try:
        with open(filename, "w") as f:
            f.write("="*60 + "\n")
            f.write("📋 CREDENZIALI ACCOUNT CREATI\n")
            f.write(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")
            for i, acc in enumerate(accounts, 1):
                f.write(f"{i}. {acc['email']} : {acc['password']}\n")
        print(f"💾 Credenziali salvate in {filename}")
        return True
    except Exception as e:
        print(f"⚠️ Errore salvataggio: {e}")
        return False

# ============================================================
# PROXY ROTATOR
# ============================================================
class ProxyRotator:
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list
        self.current_index = 0
        self.lock = asyncio.Lock()
    
    def parse_proxy(self, proxy_string):
        """Parsea un proxy nel formato username:password@host:port"""
        try:
            auth, host = proxy_string.split('@')
            username, password = auth.split(':')
            host_parts = host.split(':')
            if len(host_parts) == 2:
                hostname, port = host_parts
                return {
                    "server": f"http://{hostname}:{port}",
                    "username": username,
                    "password": password,
                    "host": hostname,
                    "port": int(port),
                    "string": proxy_string
                }
        except:
            return None
    
    async def get_proxy(self):
        """Ottiene il prossimo proxy in rotazione"""
        async with self.lock:
            if not self.proxy_list:
                return None
            
            proxy_string = self.proxy_list[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.proxy_list)
            
            proxy = self.parse_proxy(proxy_string)
            if proxy:
                print(f"🌐 Proxy: {proxy['host']}:{proxy['port']}")
                return proxy
            return None
    
    async def mark_bad(self, proxy_string):
        """Segna un proxy come cattivo (lo rimuove dalla lista)"""
        async with self.lock:
            if proxy_string in self.proxy_list:
                self.proxy_list.remove(proxy_string)
                if len(self.proxy_list) > 0:
                    self.current_index = self.current_index % len(self.proxy_list)
                print(f"🗑️ Proxy {proxy_string} rimosso (cattivo)")

# ============================================================
# PROXY ROTATOR GLOBALE
# ============================================================
proxy_rotator = ProxyRotator(PROXY_LIST)

# ============================================================
# CARICA DATABASE PHASH
# ============================================================
def carica_database():
    try:
        with open("hash_phash_db.json", "r") as f:
            return json.load(f)
    except:
        return {}

phash_db = carica_database()

# ============================================================
# LOGGING
# ============================================================
def log(account, msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [{account}] {msg}", flush=True)

# ============================================================
# FUNZIONI DI PULIZIA
# ============================================================
def pulisci_url(url):
    url = re.sub(r'<[^>]+>', '', url)
    url = url.strip()
    url = unquote(url)
    url = re.sub(r'[<>\'"]', '', url)
    return url

def pulisci_ad_id(ad_id):
    ad_id = unquote(ad_id)
    ad_id = re.sub(r'<[^>]+>', '', ad_id)
    ad_id = re.sub(r'[<>\'"]', '', ad_id)
    match = re.search(r'(\d+)', ad_id)
    if match:
        return match.group(1)
    return ad_id

# ============================================================
# RISOLUZIONE CAPTCHA
# ============================================================
async def risolvi_captcha(page, account, phash_db, max_tentativi=5):
    for tentativo in range(max_tentativi):
        log(account, f"   🔄 Tentativo captcha {tentativo+1}/{max_tentativi}")
        html = await page.content()
        cap_match = re.search(r'capimg\.php\?id=(\d+)', html)
        if not cap_match:
            log(account, "   ✅ Nessun captcha rilevato")
            return True
        cap_id = cap_match.group(1)
        cids = [int(x) for x in re.findall(r'cid=(\d+)', html)]
        cids_unici = list(set(cids))
        log(account, f"   🖼️ Captcha ID: {cap_id}")
        log(account, f"   📌 CID disponibili: {cids_unici}")
        try:
            img_element = page.locator('img[src*="capimg.php"]')
            img_data = await img_element.screenshot()
            img_pil = Image.open(io.BytesIO(img_data))
            phash = imagehash.phash(img_pil)
            phash_str = str(phash)
            log(account, f"   🔑 PHASH: {phash_str}")
        except Exception as e:
            log(account, f"   ⚠️ Errore screenshot: {e}")
            await page.reload()
            await asyncio.sleep(2)
            continue
        for stored_phash, cid in phash_db.items():
            try:
                diff = imagehash.hex_to_hash(phash_str) - imagehash.hex_to_hash(stored_phash)
                if diff <= 10:
                    await page.goto(f"https://antautosurf.com/index.php?cid={cid}")
                    await asyncio.sleep(2)
                    log(account, f"   ✅ CAPTCHA RISOLTO! CID: {cid}")
                    return True
            except:
                pass
        for cid in cids_unici:
            log(account, f"   🔄 Provo CID {cid}...")
            await page.goto(f"https://antautosurf.com/index.php?cid={cid}")
            await asyncio.sleep(2)
            html_test = await page.content()
            if "Please Click Similar" not in html_test:
                phash_db[phash_str] = cid
                with open("hash_phash_db.json", "w") as f:
                    json.dump(phash_db, f, indent=2)
                log(account, f"   ✅ CAPTCHA RISOLTO! CID: {cid} (nuovo)")
                return True
        log(account, f"   ⚠️ Tentativo {tentativo+1} fallito, ricarico...")
        await page.goto("https://antautosurf.com/index.php", wait_until="domcontentloaded")
        await asyncio.sleep(3)
    log(account, f"   ❌ CAPTCHA NON RISOLTO DOPO {max_tentativi} TENTATIVI!")
    return False

# ============================================================
# CLICCA PTC
# ============================================================
async def clicca_ptc(page, account):
    log(account, "🔍 Cerco il bottone PTC...")
    
    selectors = [
        'input[value="PTC"]',
        '#button99[value="PTC"]',
        'input.submit2[value="PTC"]',
        'input[id="button99"][value="PTC"]',
    ]
    
    for selector in selectors:
        try:
            ptc_button = page.locator(selector)
            count = await ptc_button.count()
            if count > 0:
                log(account, f"✅ Bottone PTC trovato! (selector: {selector})")
                await ptc_button.first.click()
                await asyncio.sleep(2)
                log(account, "✅ PTC attivato!")
                return True
        except Exception as e:
            log(account, f"   ⚠️ Selector {selector} fallito: {e}")
    
    try:
        all_inputs = page.locator('input')
        count = await all_inputs.count()
        for i in range(count):
            elem = all_inputs.nth(i)
            value = await elem.get_attribute('value')
            if value == "PTC":
                log(account, f"✅ Bottone PTC trovato! (input index: {i})")
                await elem.click()
                await asyncio.sleep(2)
                log(account, "✅ PTC attivato!")
                return True
    except Exception as e:
        log(account, f"   ⚠️ Ricerca per testo fallita: {e}")
    
    log(account, "ℹ️ Bottone PTC non trovato (forse già attivo)")
    return False

# ============================================================
# SURF PER UN SINGOLO ACCOUNT
# ============================================================
async def surf_account(account):
    email = account['email']
    password = account['password']
    account_name = email.split('@')[0]
    
    log(account_name, f"🚀 Avvio thread... (Email: {email})")
    
    # 🔥 OTTIENI UN PROXY DAL ROTATOR
    proxy_info = await proxy_rotator.get_proxy()
    if not proxy_info:
        log(account_name, "❌ Nessun proxy disponibile!")
        return
    
    proxy_config = {
        "server": proxy_info["server"],
        "username": proxy_info["username"],
        "password": proxy_info["password"]
    }
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=HEADLESS,
                proxy=proxy_config,
                args=['--disable-blink-features=AutomationControlled']
            )
            
            context = await browser.new_context()
            page = await context.new_page()
            
            # ============================================================
            # LOGIN/REGISTRAZIONE
            # ============================================================
            log(account_name, "📝 Creazione account...")
            await page.goto("https://antautosurf.com/", wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(2)
            
            await page.fill('input[name="bitcoinwallet"]', email)
            await page.click('input[type="submit"][value*="Enter"]')
            await asyncio.sleep(3)
            
            html = await page.content()
            
            if "Set Login Password" in html:
                log(account_name, f"📝 Nuovo account: {email}")
                await page.fill('input[name="password"]', password)
                await page.fill('input[name="passwordb"]', password)
                match = re.search(r'name="confirm2" value="(\d+)"', html)
                if match:
                    confirm2 = match.group(1)
                    await page.goto(f"https://antautosurf.com/index.php?password={password}&passwordb={password}&confirm2={confirm2}", wait_until="domcontentloaded", timeout=30000)
                    await asyncio.sleep(3)
                    log(account_name, "   ✅ Password impostata!")
                    account['created'] = True
            
            html = await page.content()
            if "Please enter Password" in html:
                log(account_name, "🔑 Login con password...")
                await page.fill('input[name="password"]', password)
                await page.click('input[value="Enter"]')
                await asyncio.sleep(3)
            
            log(account_name, "✅ Account pronto!")
            
            # ============================================================
            # DASHBOARD
            # ============================================================
            log(account_name, "📊 Dashboard...")
            await page.goto(f"https://antautosurf.com/index.php?bitcoinwallet={email}&ref=", wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(3)
            html = await page.content()
            
            if "Please Click Similar" in html:
                log(account_name, "⚠️ CAPTCHA RILEVATO!")
                if not await risolvi_captcha(page, account_name, phash_db):
                    log(account_name, "❌ Captcha non risolto!")
                    return
            
            await clicca_ptc(page, account_name)
            
            log(account_name, "🔄 Ricarico la dashboard...")
            await page.goto(f"https://antautosurf.com/index.php?bitcoinwallet={email}&ref=", wait_until="networkidle", timeout=60000)
            await asyncio.sleep(3)
            html = await page.content()
            
            # Balance
            balance_match = re.search(r'btoday["\']?\s*[=:]\s*([\d.]+)', html)
            if balance_match:
                balance = float(balance_match.group(1))
                account['balance'] = balance
                log(account_name, f"💰 Balance: {balance}")
            
            # CSRF
            csrf_match = re.search(r'csrf_token=([a-f0-9]+)', html)
            if not csrf_match:
                log(account_name, "❌ CSRF non trovato!")
                return
            
            csrf = csrf_match.group(1)
            log(account_name, f"🎫 CSRF: {csrf[:16]}...")
            
            # Cookies
            cookies = await context.cookies()
            cookie_dict = {}
            for cookie in cookies:
                cookie_dict[cookie['name']] = cookie['value']
            
            await browser.close()
            
            # ============================================================
            # SURF SENZA PROXY
            # ============================================================
            log(account_name, "🚀 Avvio surf SENZA proxy...")
            
            browser_no_proxy = await p.chromium.launch(
                headless=HEADLESS,
                args=['--disable-blink-features=AutomationControlled']
            )
            
            context_no_proxy = await browser_no_proxy.new_context()
            
            for name, value in cookie_dict.items():
                await context_no_proxy.add_cookies([{
                    'name': name,
                    'value': value,
                    'domain': '.antautosurf.com',
                    'path': '/'
                }])
            
            page_no_proxy = await context_no_proxy.new_page()
            
            key = ""
            time_val = 12
            ad_id = ""
            cycle = 0
            csrf_invalidi = 0
            MAX_CSRF_INVALIDI = 5
            
            while True:
                cycle += 1
                log(account_name, f"🔄 CICLO {cycle}")
                
                if ad_id:
                    ad_id_pulito = pulisci_ad_id(ad_id)
                else:
                    ad_id_pulito = ""
                
                params = {
                    "wallet": email,
                    "key": key,
                    "time": time_val,
                    "ad_id": ad_id_pulito,
                    "isitbad": 0,
                    "csrf_token": csrf
                }
                
                url = "https://antautosurf.com/surf.php?" + "&".join([f"{k}={v}" for k, v in params.items()])
                
                await page_no_proxy.goto(url, wait_until="domcontentloaded", timeout=30000)
                page_text = await page_no_proxy.content()
                
                if "Invalid CSRF token" in page_text:
                    csrf_invalidi += 1
                    log(account_name, f"❌ CSRF invalido! ({csrf_invalidi}/{MAX_CSRF_INVALIDI})")
                    
                    if csrf_invalidi >= MAX_CSRF_INVALIDI:
                        log(account_name, "🔄 Troppi CSRF invalidi! Riavvio...")
                        return
                    
                    await page_no_proxy.goto(f"https://antautosurf.com/index.php?bitcoinwallet={email}&ref=", wait_until="networkidle", timeout=30000)
                    await asyncio.sleep(2)
                    html = await page_no_proxy.content()
                    csrf_match = re.search(r'csrf_token=([a-f0-9]+)', html)
                    if csrf_match:
                        csrf = csrf_match.group(1)
                        csrf_invalidi = 0
                        log(account_name, f"🎫 Nuovo CSRF: {csrf[:16]}...")
                    continue
                else:
                    csrf_invalidi = 0
                
                if "--_--" not in page_text:
                    await asyncio.sleep(5)
                    continue
                
                parts = page_text.split("--_--")
                if len(parts) < 4:
                    continue
                
                ad_url = pulisci_url(parts[0])
                time_val = int(parts[1])
                key = parts[2]
                ad_id = parts[3]
                
                if "connection.php" in ad_url:
                    log(account_name, "   📂 Test anti-bot...")
                    try:
                        new_page = await context_no_proxy.new_page()
                        await new_page.goto(ad_url, wait_until="domcontentloaded", timeout=30000)
                        await asyncio.sleep(2)
                    except Exception as e:
                        log(account_name, f"   ⚠️ Errore apertura: {e}")
                    
                    for i in range(time_val, 0, -1):
                        print(f"   ⏳ {i}s", end="\r")
                        await asyncio.sleep(1)
                    print("   " * 20, end="\r")
                    
                    try:
                        await new_page.close()
                    except:
                        pass
                    continue
                
                log(account_name, f"   📢 Annuncio reale! Timer: {time_val}s")
                
                try:
                    new_page = await context_no_proxy.new_page()
                    await new_page.goto(ad_url, wait_until="domcontentloaded", timeout=10000)
                    await asyncio.sleep(1)
                except Exception as e:
                    log(account_name, f"   ⚠️ Errore apertura: {e}")
                
                for i in range(time_val, 0, -1):
                    print(f"   ⏳ {i}s", end="\r")
                    await asyncio.sleep(1)
                print("   " * 20, end="\r")
                log(account_name, f"   ✅ Timer completato!")
                
                try:
                    await new_page.close()
                except:
                    pass
                
                if cycle % 3 == 0:
                    await page_no_proxy.goto(f"https://antautosurf.com/index.php?bitcoinwallet={email}&ref=", wait_until="networkidle", timeout=30000)
                    await asyncio.sleep(2)
                    html = await page_no_proxy.content()
                    csrf_match = re.search(r'csrf_token=([a-f0-9]+)', html)
                    if csrf_match:
                        csrf = csrf_match.group(1)
                        log(account_name, f"   🎫 CSRF aggiornato: {csrf[:16]}...")
    
    except Exception as e:
        log(account_name, f"❌ Errore: {e}")
        if "ERR_CONNECTION_RESET" in str(e) or "Timeout" in str(e) or "ERR_TUNNEL" in str(e):
            await proxy_rotator.mark_bad(proxy_info['string'])

# ============================================================
# MAIN
# ============================================================
async def main():
    print("=" * 60)
    print("🚀 ANTPROXY MULTIACCOUNT - PROXY FISSI")
    print(f"🔇 Headless: {HEADLESS}")
    print(f"🔄 Max concurrent: {MAX_CONCURRENT}")
    print(f"📋 Account da creare: {NUM_ACCOUNTS}")
    print(f"🌐 Proxy disponibili: {len(PROXY_LIST)}")
    print("=" * 60)
    
    phash_db = carica_database()
    print(f"📊 Database phash: {len(phash_db)} hash")
    
    # 🔥 GENERA ACCOUNT AUTOMATICAMENTE
    accounts = []
    print(f"📧 Generazione di {NUM_ACCOUNTS} account...")
    for i in range(NUM_ACCOUNTS):
        account = genera_account()
        accounts.append(account)
        print(f"   → {i+1}/{NUM_ACCOUNTS}: {account['email']} / {account['password']}")
    
    # 🔥 SALVA LE CREDENZIALI
    if accounts:
        salva_credenziali(accounts)
    
    print("\n" + "=" * 60)
    print("🚀 AVVIO THREAD MULTI-ACCOUNT...")
    print("=" * 60)
    
    try:
        while True:
            tasks = []
            for account in accounts:
                while len(tasks) >= MAX_CONCURRENT:
                    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                    tasks = list(pending)
                
                account_name = account['email'].split('@')[0]
                log(account_name, f"🔄 Avvio thread...")
                task = asyncio.create_task(surf_account(account))
                tasks.append(task)
                await asyncio.sleep(2)
            
            if tasks:
                await asyncio.gather(*tasks)
            
            # 🔥 STAMPA RIEPILOGO
            print("\n" + "=" * 60)
            print("📊 RIEPILOGO ACCOUNT")
            print("=" * 60)
            for acc in accounts:
                status = "✅" if acc.get('created') else "⏳"
                print(f"   {status} {acc['email']} → Balance: {acc.get('balance', 0)}")
            print("=" * 60)
            
            log("MAIN", "⏳ Tutti i thread completati, attesa 30 secondi...")
            await asyncio.sleep(30)
    
    except KeyboardInterrupt:
        log("MAIN", "\n⏹️ Arresto...")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
