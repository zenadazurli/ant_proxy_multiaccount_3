#!/usr/bin/env python3
# bot.py - V3: 100 ACCOUNT CON GENERAZIONE AUTOMATICA
# Proxy Manager potenziato con 25 fonti

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
MAX_CONCURRENT = int(os.environ.get("MAX_CONCURRENT", "10"))  # 10 thread in parallelo
NUM_ACCOUNTS = int(os.environ.get("NUM_ACCOUNTS", "100"))     # 100 account da creare

# ============================================================
# GENERATORE DI ACCOUNT REALISTICI (AUTOMATICO)
# ============================================================
def genera_email_realistica():
    """Genera un'email realistica (come un utente vero)"""
    
    nomi = [
        "mario", "luca", "marco", "giuseppe", "antonio", "giovanni", 
        "francesco", "andrea", "alessandro", "roberto", "stefano", 
        "paolo", "simone", "davide", "matteo", "federico", "valentina",
        "chiara", "sara", "elena", "martina", "silvia", "alessia",
        "sabrina", "paola", "giulia", "francesca", "anna", "laura",
        "carlo", "alberto", "emanuele", "lorenzo", "riccardo", "daniele",
        "marzia", "elisabetta", "daniela", "monica", "cristina", "veronica"
    ]
    
    cognomi = [
        "rossi", "russo", "ferrari", "esposito", "bianchi", "romano",
        "colombo", "ricci", "marino", "greco", "bruno", "gallo",
        "conti", "de luca", "mancini", "giordano", "rizzo", "lombardi",
        "barbieri", "fontana", "santoro", "mariani", "conte", "moretti",
        "gentile", "carboni", "leone", "fabbri", "palmieri", "parisi"
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
    """Genera una password realistica (come la userebbe un utente vero)"""
    
    parole = [
        "sole", "luna", "stella", "cielo", "mare", "monte", 
        "fiore", "rosa", "amore", "vita", "pace", "gioia",
        "libertà", "sogno", "cuore", "anima", "falco", "aquila",
        "tigre", "leone", "lupo", "aquila", "drago", "fenice"
    ]
    
    anni_comuni = ["1985", "1990", "1992", "1995", "2000", "2001", "2002", "2003", "2005"]
    speciali = ['!', '$', '#', '@', '&']
    
    # Combina: parola + anno + speciale
    parola = random.choice(parole)
    anno = random.choice(anni_comuni)
    speciale = random.choice(speciali)
    
    # Variazioni: parola+anno, parola+anno+!, parola+!
    pattern = random.choice([
        f"{parola}{anno}",
        f"{parola}{anno}{speciale}",
        f"{parola}{speciale}{anno}",
        f"{parola.capitalize()}{anno}{speciale}",
    ])
    
    return pattern

def genera_account(n):
    """Genera un account con numero progressivo per evitare duplicati"""
    email = genera_email_realistica()
    # Aggiungi un numero per evitare duplicati rari
    if random.random() < 0.3:
        base, dominio = email.split('@')
        email = f"{base}{random.randint(1, 99)}@{dominio}"
    password = genera_password_realistica()
    return {
        "email": email,
        "password": password,
        "created": False,
        "balance": 0
    }

# ============================================================
# PROXY MANAGER (25 FONTI - INVARIATO)
# ============================================================
class ProxyManager:
    def __init__(self):
        self.proxy_pool = []
        self.lock = asyncio.Lock()
        self.bad_proxies = set()
        self.last_refresh = None
        
        self.sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all",
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=5000&country=all",
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=5000&country=all",
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=5000&country=all",
            "https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
            "https://raw.githubusercontent.com/Argh94/Proxy-List/main/http.txt",
            "https://raw.githubusercontent.com/Ian-Lusule/Proxies/main/proxies/all_proxies.txt",
            "https://raw.githubusercontent.com/komutan234/Proxy-List-Free/main/proxies/http.txt",
            "https://free.geonix.com/it/",
            "https://nodemaven.com/free-proxy-list/",
            "https://spys.one/en/",
            "https://litport.net/free-proxy",
            "https://fineproxy.org/free-proxy/",
            "https://proxymix.net/freeproxy",
            "https://www.proxy-list.download/api/v1/get?type=http",
            "https://www.proxy-list.download/api/v1/get?type=https",
            "https://www.proxy-list.download/api/v1/get?type=socks4",
            "https://www.proxy-list.download/api/v1/get?type=socks5",
            "https://api.openproxylist.xyz/http.txt",
            "https://api.openproxylist.xyz/socks4.txt",
            "https://api.openproxylist.xyz/socks5.txt",
            "https://sockslist.us/Api?request=display&country=all&level=all&token=free",
        ]
        
        self.allowed_types = ['http', 'https']
    
    def fetch_roundproxies(self):
        """Scarica proxy da RoundProxies.com (parsing HTML base)"""
        url = "https://roundproxies.com/free-proxy-list/"
        proxies = []
        try:
            resp = requests.get(url, timeout=15)
            matches = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+)', resp.text)
            for match in matches[:1000]:
                proxy = match.strip()
                if proxy.count(':') == 1 and proxy not in self.bad_proxies:
                    proxies.append(proxy)
            print(f"✅ RoundProxies: {len(proxies)} proxy")
        except Exception as e:
            print(f"⚠️ Errore RoundProxies: {e}")
        return proxies
    
    def fetch_sockslist(self):
        """Scarica proxy da SocksList.us via API"""
        url = "https://sockslist.us/Api?request=display&country=all&level=all&token=free"
        proxies = []
        try:
            resp = requests.get(url, timeout=10)
            data = resp.json()
            for entry in data:
                proxy = f"{entry['ip']}:{entry['port']}"
                if proxy.count(':') == 1 and proxy not in self.bad_proxies:
                    proxies.append(proxy)
            print(f"✅ SocksList: {len(proxies)} proxy")
        except Exception as e:
            print(f"⚠️ Errore SocksList: {e}")
        return proxies
    
    def fetch_proxies_sync(self):
        """Scarica proxy da TUTTE le fonti"""
        all_proxies = []
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📡 Scaricamento proxy da {len(self.sources)} fonti...")
        
        for idx, url in enumerate(self.sources):
            try:
                print(f"   📥 Fonte {idx+1}/{len(self.sources)}...", end=" ")
                resp = requests.get(url, timeout=15)
                proxies_found = 0
                for line in resp.text.strip().splitlines():
                    if ':' in line:
                        proxy = line.strip()
                        if proxy.count(':') == 1 and proxy not in self.bad_proxies:
                            proxy_type = 'http'
                            if 'socks4' in url or 'socks4' in line.lower():
                                proxy_type = 'socks4'
                            elif 'socks5' in url or 'socks5' in line.lower():
                                proxy_type = 'socks5'
                            elif 'https' in url or ':443' in proxy:
                                proxy_type = 'https'
                            
                            if proxy_type in self.allowed_types:
                                all_proxies.append(proxy)
                                proxies_found += 1
                print(f"✅ {proxies_found} proxy")
            except Exception as e:
                print(f"❌ Errore: {e}")
        
        all_proxies.extend(self.fetch_roundproxies())
        all_proxies.extend(self.fetch_sockslist())
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📋 Totale proxy scaricati: {len(all_proxies)}")
        return all_proxies
    
    def test_proxy_sync(self, proxy):
        """Testa un proxy (HTTP e HTTPS)"""
        proxy_url = f"http://{proxy}"
        proxies = {"http": proxy_url, "https": proxy_url}
        try:
            start = time.time()
            resp_http = requests.get("http://ip-api.com/json", proxies=proxies, timeout=5)
            if resp_http.status_code != 200:
                return False, 0, "", ""
            delay = int((time.time() - start) * 1000)
            data = resp_http.json()
            try:
                resp_https = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=5)
                if resp_https.status_code != 200:
                    return False, 0, "", ""
            except:
                return False, 0, "", ""
            return True, delay, data.get("query", ""), data.get("countryCode", "")
        except:
            return False, 0, "", ""
    
    async def get_proxy(self):
        """Ottiene un proxy funzionante"""
        async with self.lock:
            if not self.proxy_pool:
                self.refresh_pool_sync()
            while self.proxy_pool:
                proxy = self.proxy_pool.pop(0)
                if proxy['proxy'] not in self.bad_proxies:
                    ok, delay, ip, country = self.test_proxy_sync(proxy['proxy'])
                    if ok:
                        proxy['delay'] = delay
                        proxy['ip'] = ip
                        proxy['country'] = country
                        return proxy
                    else:
                        self.bad_proxies.add(proxy['proxy'])
                        print(f"🗑️ Proxy {proxy['proxy']} fallito al test, scartato")
            self.refresh_pool_sync()
            if self.proxy_pool:
                return self.proxy_pool.pop(0)
            return None
    
    def refresh_pool_sync(self, limit=25):
        """Aggiorna il pool con proxy testati"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔄 Aggiornamento pool proxy...")
        raw_proxies = self.fetch_proxies_sync()
        if not raw_proxies:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Nessun proxy scaricato!")
            return []
        random.shuffle(raw_proxies)
        good_proxies = []
        tested = 0
        max_to_test = min(len(raw_proxies), 200)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🧪 Testo {max_to_test} proxy...")
        for proxy in raw_proxies[:max_to_test]:
            tested += 1
            ok, delay, ip, country = self.test_proxy_sync(proxy)
            if ok:
                good_proxies.append({
                    "proxy": proxy,
                    "delay": delay,
                    "ip": ip,
                    "country": country
                })
                if len(good_proxies) >= limit:
                    break
            if tested % 20 == 0:
                print(f"   Testati {tested}/{max_to_test} proxy...")
        good_proxies.sort(key=lambda x: x['delay'])
        self.proxy_pool = good_proxies
        self.last_refresh = datetime.now()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Proxy funzionanti: {len(good_proxies)}")
        if good_proxies:
            print(f"   🔥 Miglior proxy: {good_proxies[0]['proxy']} ({good_proxies[0]['delay']}ms) - {good_proxies[0].get('country', '')}")
        return good_proxies
    
    def mark_bad(self, proxy):
        """Segna un proxy come cattivo"""
        self.bad_proxies.add(proxy)
        self.proxy_pool = [p for p in self.proxy_pool if p['proxy'] != proxy]
        print(f"🗑️ Proxy {proxy} segnato come cattivo")

# ============================================================
# PROXY MANAGER GLOBALE
# ============================================================
proxy_manager = ProxyManager()

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
# RISOLUZIONE CAPTCHA (VERSIONE ASYNC)
# ============================================================
async def risolvi_captcha(page, account, phash_db, max_tentativi=5):
    """Risolvi captcha con tentativi multipli e fallback (async)"""
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
# CLICCA BOTTONE PTC
# ============================================================
async def clicca_ptc(page, account):
    """Cerca e clicca il bottone PTC se presente"""
    try:
        selectors = ['#button99', 'input[value="PTC"]', 'input.submit2[value="PTC"]']
        for selector in selectors:
            ptc_button = page.locator(selector)
            count = await ptc_button.count()
            if count > 0:
                log(account, f"✅ Bottone PTC trovato! (selector: {selector})")
                await ptc_button.click()
                await asyncio.sleep(2)
                log(account, "✅ PTC attivato!")
                return True
        log(account, "ℹ️ Bottone PTC non trovato (forse già attivo)")
        return False
    except Exception as e:
        log(account, f"⚠️ Errore clic PTC: {e}")
        return False

# ============================================================
# SURF PER UN SINGOLO ACCOUNT (VERSIONE ASYNC)
# ============================================================
async def surf_account(account):
    """Esegue il surf per un singolo account (async)"""
    email = account['email']
    password = account['password']
    account_name = email.split('@')[0]
    
    log(account_name, f"🚀 Avvio thread... (Email: {email})")
    
    max_retry = 3
    proxy_info = None
    
    for attempt in range(max_retry):
        proxy_info = await proxy_manager.get_proxy()
        if proxy_info:
            log(account_name, f"🌐 Proxy: {proxy_info['proxy']} ({proxy_info['delay']}ms) - {proxy_info.get('country', '')}")
            break
        else:
            log(account_name, f"⚠️ Tentativo {attempt+1}/{max_retry}: nessun proxy")
            proxy_manager.refresh_pool_sync()
    
    if not proxy_info:
        log(account_name, "❌ Nessun proxy disponibile!")
        return
    
    proxy_config = {"server": f"http://{proxy_info['proxy']}"}
    
    try:
        async with async_playwright() as p:
            # 🔥 FASE 1: LOGIN CON PROXY
            browser = await p.chromium.launch(
                headless=HEADLESS,
                proxy=proxy_config,
                args=['--disable-blink-features=AutomationControlled']
            )
            
            context = await browser.new_context()
            page = await context.new_page()
            
            # ============================================================
            # REGISTRAZIONE/CREAZIONE ACCOUNT
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
            
            # 🔥 CLICCA PTC (SE PRESENTE)
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
            
            # 🔥 FASE 2: CHIUDI BROWSER CON PROXY
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
            proxy_manager.mark_bad(proxy_info['proxy'])

# ============================================================
# MAIN (VERSIONE ASYNC)
# ============================================================
async def main():
    print("=" * 60)
    print("🚀 V3 - 100 ACCOUNT CON PROXY MANAGER")
    print(f"🔇 Headless: {HEADLESS}")
    print(f"🔄 Max concurrent: {MAX_CONCURRENT}")
    print(f"📋 Account da creare: {NUM_ACCOUNTS}")
    print("=" * 60)
    
    phash_db = carica_database()
    print(f"📊 Database phash: {len(phash_db)} hash")
    
    # 🔥 GENERA 100 ACCOUNT AUTOMATICAMENTE
    accounts = []
    print(f"📧 Generazione di {NUM_ACCOUNTS} account...")
    for i in range(NUM_ACCOUNTS):
        account = genera_account(i)
        accounts.append(account)
        print(f"   → {i+1}/{NUM_ACCOUNTS}: {account['email']} / {account['password']}")
    
    print("\n" + "=" * 60)
    print("🚀 AVVIO THREAD MULTI-ACCOUNT (ASYNC)...")
    print("=" * 60)
    
    try:
        while True:
            tasks = []
            for account in accounts:
                while len(tasks) >= MAX_CONCURRENT:
                    # Aspetta che qualche task finisca
                    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                    tasks = list(pending)
                
                account_name = account['email'].split('@')[0]
                log(account_name, f"🔄 Avvio thread...")
                task = asyncio.create_task(surf_account(account))
                tasks.append(task)
                await asyncio.sleep(2)
            
            # Aspetta che tutti i task finiscano
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