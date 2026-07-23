#!/usr/bin/env python3
# bot.py - Multi-Account con 200 Proxy Fissi - VERSIONE COMPLETA

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
        """Ottiene un proxy per il login (lo consuma)"""
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
        """Non usa proxy per il surf"""
        return None
    
    async def mark_bad(self, proxy_string):
        """Segna un proxy come cattivo"""
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
    anno
