#!/usr/bin/env python3
# bot.py - Multi-Account con 200 Proxy Fissi - CON SALVATAGGIO PASSWORD

import os
import time
import sys
import json
import re
import requests
import asyncio
import random
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
# 200 PROXY DA PROXYSCRAPE
# ============================================================
PROXY_LIST = [
    # === PRIMI 100 PROXY (tahk21bkxl6k) ===
    "tahk21bkxl6k:gxb0zbaf3bviu8f@65.111.1.146:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@209.50.190.205:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@104.207.36.24:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@104.207.62.7:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.238.220:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.252.111:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@209.50.171.140:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.237.171:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@104.207.55.94:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@104.207.52.189:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.237.180:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@104.207.47.176:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.242.150:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@104.207.59.97:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@104.207.35.28:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@209.50.161.14:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@104.207.53.93:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@104.207.49.48:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@217.181.91.15:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@45.3.33.38:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@209.50.177.26:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@217.181.91.59:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@65.111.27.237:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@217.181.91.49:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@104.207.43.158:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@209.50.189.147:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@193.56.28.97:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@65.111.14.184:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@209.50.168.55:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@104.207.33.222:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@209.50.179.1:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@45.3.41.21:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.255.143:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@217.181.92.49:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.226.27:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@104.207.53.61:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.245.15:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@209.50.191.77:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@65.111.22.133:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@65.111.20.76:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.248.223:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@65.111.0.42:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@45.3.38.171:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@65.111.14.234:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@209.50.187.149:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@209.50.164.221:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@45.3.39.64:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.237.4:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@209.50.168.103:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@209.50.163.103:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.236.127:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@65.111.31.206:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@104.207.36.50:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@45.3.52.104:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@104.207.32.235:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@65.111.21.171:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@209.50.191.143:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@209.50.168.171:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.239.175:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.238.212:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@209.50.186.167:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.243.22:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.248.88:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@65.111.12.159:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@45.3.39.132:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@209.50.183.210:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.248.207:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@209.50.188.134:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.232.70:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.243.42:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@104.207.63.223:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@104.207.45.95:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.250.195:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@45.3.62.53:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@65.111.0.10:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.251.33:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.234.204:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@104.207.42.177:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.253.242:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@45.3.53.239:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@209.50.183.37:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@104.207.50.0:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@209.50.179.173:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@209.50.184.58:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@65.111.24.138:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.231.184:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@45.3.45.36:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@104.207.62.129:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@104.207.42.230:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@209.50.161.144:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@209.50.170.140:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.237.12:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@65.111.22.189:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@65.111.5.163:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@65.111.0.7:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@216.26.252.181:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@104.207.52.165:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@104.207.38.208:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@45.3.55.127:3129",
    "tahk21bkxl6k:gxb0zbaf3bviu8f@45.3.54.181:3129",
    # === SECONDI 100 PROXY (pql1ir85bjz6) ===
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.35.205:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@209.50.163.91:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@209.50.182.59:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.51.70:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@45.3.51.125:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.24.146:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@209.50.175.218:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@216.26.240.89:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.22.189:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@216.26.239.30:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.53.109:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@209.50.191.41:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.0.190:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@209.50.165.31:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.42.133:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@151.123.178.253:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.42.85:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.63.192:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@209.50.180.223:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@209.50.163.138:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@216.26.255.67:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@216.26.232.149:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@216.26.231.141:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@217.181.90.226:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.7.141:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.52.250:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@45.3.54.205:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@216.26.240.145:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@45.3.34.180:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.8.80:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@45.3.33.157:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.167.25.134:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@151.123.176.247:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@216.26.251.183:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.47.149:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.30.188:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@209.50.188.112:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.2.203:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.43.201:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@216.26.241.129:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.167.25.73:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.50.66:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.2.82:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@216.26.252.114:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@216.26.241.105:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.9.32:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@209.50.177.179:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@216.26.244.238:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.48.40:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@209.50.165.130:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@216.26.254.217:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@45.3.32.30:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@209.50.186.93:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@193.56.28.247:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@209.50.170.42:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@45.3.49.195:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.7.232:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.26.10:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.30.50:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@209.50.174.51:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.56.219:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.51.10:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.20.22:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.14.154:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.41.20:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.61.197:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@216.26.231.121:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@209.50.170.217:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@45.3.37.50:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.52.131:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.30.248:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@216.26.252.166:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@216.26.225.90:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@209.50.191.116:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@209.50.173.173:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.32.141:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.60.245:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@216.26.233.195:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.51.152:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.23.20:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@209.50.191.86:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@216.26.248.24:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.24.151:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.37.213:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@45.3.32.75:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.15.239:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.0.69:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@45.3.43.193:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.29.71:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@216.26.249.105:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.57.64:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.53.243:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@216.26.254.51:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.8.239:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.22.110:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.11.83:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@45.3.43.28:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.55.247:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@65.111.0.170:3129",
    "pql1ir85bjz6:gjf1aqzo4hsjnmj@104.207.57.105:3129",
]

# ============================================================
# PROXY ROTATOR (SOLO PER IL LOGIN)
# ============================================================
class ProxyRotator:
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list
        self.current_index = 0
        self.lock = asyncio.Lock()
        self.used_proxies = set()
    
    def parse_proxy(self, proxy_string):
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
    
    async def get_proxy_for_login(self):
        async with self.lock:
            for i in range(len(self.proxy_list)):
                proxy_string = self.proxy_list[i]
                if proxy_string not in self.used_proxies:
                    self.used_proxies.add(proxy_string)
                    proxy = self.parse_proxy(proxy_string)
                    if proxy:
                        print(f"🌐 Proxy per login: {proxy['host']}:{proxy['port']}")
                        return proxy
            print("❌ Nessun proxy disponibile per il login!")
            return None
    
    async def get_proxy_for_surf(self):
        return None
    
    async def mark_bad(self, proxy_string):
        async with self.lock:
            if proxy_string in self.used_proxies:
                self.used_proxies.remove(proxy_string)
            if proxy_string in self.proxy_list:
                self.proxy_list.remove(proxy_string)
                if len(self.proxy_list) > 0:
                    self.current_index = self.current_index % len(self.proxy_list)
                print(f"🗑️ Proxy {proxy_string} rimosso (cattivo)")

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
# SURF PER UN SINGOLO ACCOUNT (SENZA PTC)
# ============================================================
async def surf_account(account, proxy_rotator):
    email = account['email']
    password = account['password']
    account_name = email.split('@')[0]
    
    log(account_name, f"🚀 Avvio thread... (Email: {email})")
    
    # 🔥 OTTIENI UN PROXY PER IL LOGIN
    proxy_info = await proxy_rotator.get_proxy_for_login()
    if not proxy_info:
        log(account_name, "❌ Nessun proxy disponibile per il login!")
        return
    
    proxy_config = {
        "server": proxy_info["server"],
        "username": proxy_info["username"],
        "password": proxy_info["password"]
    }
    
    try:
        async with async_playwright() as p:
            # ============================================================
            # BROWSER CON PROXY PER IL LOGIN
            # ============================================================
            browser = await p.chromium.launch(
                headless=HEADLESS,
                proxy=proxy_config,
                args=['--disable-blink-features=AutomationControlled']
            )
            
            context = await browser.new_context()
            page = await context.new_page()
            
            log(account_name, "📝 Login/Registrazione...")
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
            # DASHBOARD CON PROXY
            # ============================================================
            log(account_name, "📊 Dashboard...")
            await page.goto(f"https://antautosurf.com/index.php?bitcoinwallet={email}&ref=", wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(3)
            html = await page.content()
            
            # 🔥 RISOLVI IL CAPTCHA SE PRESENTE
            if "Please Click Similar" in html:
                log(account_name, "⚠️ CAPTCHA RILEVATO!")
                if not await risolvi_captcha(page, account_name, phash_db):
                    log(account_name, "❌ Captcha non risolto!")
                    return
            
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
            
            # ============================================================
            # CHIUDI BROWSER CON PROXY
            # ============================================================
            log(account_name, "🔄 Chiudo browser con proxy...")
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
    print("🚀 ANTPROXY MULTIACCOUNT - 200 PROXY")
    print(f"🔇 Headless: {HEADLESS}")
    print(f"🔄 Max concurrent: {MAX_CONCURRENT}")
    print(f"📋 Account da creare: {NUM_ACCOUNTS}")
    print(f"🌐 Proxy disponibili: {len(PROXY_LIST)}")
    print("=" * 60)
    
    phash_db = carica_database()
    print(f"📊 Database phash: {len(phash_db)} hash")
    
    # 🔥 PROXY ROTATOR
    proxy_rotator = ProxyRotator(PROXY_LIST)
    
    # 🔥 GENERA ACCOUNT
    accounts = []
    print(f"📧 Generazione di {NUM_ACCOUNTS} account...")
    for i in range(NUM_ACCOUNTS):
        account = genera_account()
        accounts.append(account)
        # 🔥 STAMPA EMAIL E PASSWORD
        print(f"   → {i+1}/{NUM_ACCOUNTS}: {account['email']} / {account['password']}")
    
    # 🔥 SALVA LE CREDENZIALI
    if accounts:
        salva_credenziali(accounts)
        print("\n" + "="*60)
        print("📋 CREDENZIALI ACCOUNT (SALVATE)")
        print("="*60)
        for i, acc in enumerate(accounts, 1):
            print(f"   {i}. {acc['email']} : {acc['password']}")
        print("="*60)
        print(f"💾 Salvate in: accounts_created.txt")
    
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
                task = asyncio.create_task(surf_account(account, proxy_rotator))
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
