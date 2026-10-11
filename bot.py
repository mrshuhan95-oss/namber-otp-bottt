import subprocess
import sys
import time
import re
import json
import os
import html
import random
import uuid
import pickle
import cloudscraper
import requests
import phonenumbers
from phonenumbers import geocoder
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
from threading import Thread, Event
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote_plus
import shutil

BOT_TOKEN = os.environ["BOT_TOKEN"]
MAIN_ADMIN_ID = int(os.environ.get("MAIN_ADMIN_ID", "7963559629"))
def create_backup(source_files, backup_dir="backups"):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    current_backup_dir = os.path.join(backup_dir, f"backup_{timestamp}")
    os.makedirs(current_backup_dir, exist_ok=True)
    
    for file in source_files:
        if file and os.path.exists(file):
            try:
                dest_path = os.path.join(current_backup_dir, os.path.basename(file))
                if os.path.isdir(file):
                    if os.path.exists(dest_path):
                        shutil.rmtree(dest_path)
                    shutil.copytree(file, dest_path)
                else:
                    shutil.copy2(file, current_backup_dir)
            except Exception as e:
                print(f"Error backing up {file}: {e}")
    
    
    zip_name = f"{current_backup_dir}.zip"
    try:
        shutil.make_archive(current_backup_dir, 'zip', current_backup_dir)
       
        shutil.rmtree(current_backup_dir)
        return zip_name
    except Exception as e:
        print(f"Error zipping backup: {e}")
        return current_backup_dir

class BackupManager:
    def create_backup(self):
        
        files_to_backup = []
        for var in ['SETTINGS_FILE', 'SESSIONS_FILE', 'USERS_FILE', 'ADMINS_FILE', 'GROUPS_FILE', 'COUNTRIES_FILE', 'CHANNELS_FILE']:
            val = globals().get(var)
            if val: files_to_backup.append(val)
        
        
        if os.path.exists("database"): files_to_backup.append("database")
        
        return create_backup(files_to_backup)
    
    def restore_backup(self, zip_path):
        return False

backup_manager = BackupManager()

def list_backups(backup_dir="backups"):
   
    if not os.path.exists(backup_dir):
        return []
    return sorted([d for d in os.listdir(backup_dir) if os.path.isdir(os.path.join(backup_dir, d))], reverse=True)


import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

SETTINGS_FILE = "ii287.json"
SESSIONS_FILE = "limogpt.json"
def get_country_flags(country_name):
    
    country_name_lower = country_name.lower()
    flags = {
        "egypt": "<tg-emoji emoji-id='5976310790381115423'>🇪🇬</tg-emoji>", "libya": "🇱🇾", "syria": "🇸🇾", "iraq": "<tg-emoji emoji-id='5976458232313420307'>🇮🇶</tg-emoji>", "saudi": "<tg-emoji emoji-id='5976726495970729818'>🇸🇦</tg-emoji>",
        "yemen": "<tg-emoji emoji-id='5976685311529327157'>🇾🇪</tg-emoji>", "jordan": "🇯🇴", "uae": "🇦🇪", "kuwait": "🇰🇼", "qatar": "🇶🇦",
        "oman": "🇴🇲", "bahrain": "🇧🇭", "lebanon": "🇱🇧", "palestine": "🇵🇸", "algeria": "🇩🇿",
        "morocco": "🇲🇦", "tunisia": "🇹🇳", "sudan": "🇸🇩", "somalia": "🇸🇴", "djibouti": "🇩🇯",
        "mauritania": "🇲🇷", "liber": "🇱🇾", "مصر": "<tg-emoji emoji-id='5976310790381115423'>🇪🇬</tg-emoji>", "ليبيا": "🇱🇾", "سوريا": "🇸🇾",
        "العراق": "<tg-emoji emoji-id='5976458232313420307'>🇮🇶</tg-emoji>", "السعودية": "<tg-emoji emoji-id='5976726495970729818'>🇸🇦</tg-emoji>", "اليمن": "<tg-emoji emoji-id='5976685311529327157'>🇾🇪</tg-emoji>", "الأردن": "🇯🇴", "الإمارات": "🇦🇪",
        "الكويت": "🇰🇼", "قطر": "🇶🇦", "عمان": "🇴🇲", "البحرين": "🇧🇭", "لبنان": "🇱🇧",
        "فلسطين": "🇵🇸", "الجزائر": "🇩🇿", "المغرب": "🇲🇦", "تونس": "🇹🇳", "السودان": "🇸🇩",
        "الصومال": "🇸🇴", "جيبوتي": "🇩🇯", "موريتانيا": "🇲🇷"
    }
    for name, flag in flags.items():
        if name in country_name_lower:
            return flag
    return "🌐"

def load_env():
    
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env()



DEFAULT_SETTINGS = {
    "GROUP": {
        "name": "GROUP",
        "accounts": [
            {
                "id": str(uuid.uuid4()),
                "username": "Yousseffh123",
                "password": "Yousseffh123"
            }
        ],
        "base_url": "http://139.99.63.204",
        "login_page_url": "http://139.99.63.204/ints/login",
        "login_post_url": "http://139.99.63.204/ints/signin",
        "ajax_path": "/ints/agent/res/data_smscdr.php",
        "check_interval": 5,
        "timeout": 30,
        "enabled": True
    },
    "Fly sms": {
        "name": "Fly sms",
        "accounts": [
            {
                "id": str(uuid.uuid4()),
                "username": "ud08",
                "password": "aud$$"
            }
        ],
        "base_url": "http://193.70.33.154",
        "login_page_url": "http://193.70.33.154/ints/login",
        "login_post_url": "http://193.70.33.154/ints/signin",
        "ajax_path": "/ints/agent/res/data_smscdr.php",
        "check_interval": 1,
        "timeout": 60,
        "enabled": True
    },
    "Number_Panel": {
        "name": "Number Panel",
        "accounts": [
            {
                "id": "SFBTR0ZBUzRWkE9Xd2GRVIeViIVBk3BpXnCTiElodkFhVWFYdYOLZA==",
                "api_token": "SFBTR0ZBUzRWkE9Xd2GRVIeViIVBk3BpXnCTiElodkFhVWFYdYOLZA=="
            }
        ],
        "base_url": "http://147.135.212.197/crapi/st/viewstats",
        "check_interval": 5,
        "timeout": 30,
        "enabled": True
    },
    "Bolt": {
        "name": "Bolt",
        "accounts": [
            {
                "id": str(uuid.uuid4()),
                "username": "abuar113",
                "password": "abuun_Z113"
            }
        ],
        "base_url": "http://93.190.143.35/ints",
        "login_page_url": "http://93.190.143.35/ints/Login",
        "login_post_url": "http://93.190.143.35/ints/signin",
        "ajax_path": "/agent/res/data_smscdr.php",
        "check_interval": 5,
        "timeout": 30,
        "enabled": True
    },
    "iVASMS": {
        "name": "iVAS SMS",
        "accounts": [
            {
                "id": str(uuid.uuid4()),
                "username": "mdsdxn500@gmail.com",
                "password": "12011",
                "api_key": "sk_4b5ff02b42635e4c4891bd5d2f8fcb7aff2f7af6d5daecf8498ba91092dfcbb6"
            }
        ],
        "api_url": "https://maroon-wombat-183778.hostingersite.com/apiivasms/api.php",
        "check_interval": 5,
        "timeout": 15,
        "enabled": True
    },
    "MSI": {
        "name": "MSI",
        "accounts": [
            {
                "id": str(uuid.uuid4()),
                "username": "Yo123X",
                "password": "ef64"
            }
        ],
        "base_url": "http://145.239.130.45/ints",
        "login_page_url": "http://145.239.130.45/ints/login",
        "login_post_url": "http://145.239.130.45/ints/signin",
        "ajax_path": "/agent/res/data_smscdr.php",
        "check_interval": 5,
        "timeout": 30,
        "enabled": True
    },
    "proton SMS": {
        "name": "proton SMS",
        "accounts": [
            {
                "id": str(uuid.uuid4()),
                "username": "LLL",
                "password": "ELL"
            }
        ],
        "base_url": "http://109.236.84.81/ints",
        "login_page_url": "http://109.236.84.81/ints/login",
        "login_post_url": "http://109.236.84.81/ints/signin",
        "ajax_path": "/agent/res/data_smscdr.php",
        "check_interval": 5,
        "timeout": 60,
        "enabled": True
    },
    "IMS": {
        "name": "IMS",
        "accounts": [
            {
                "id": str(uuid.uuid4()),
                "username": "Ahmone",
                "password": "98"
            }
        ],
        "base_url": "http://45.82.67.20",
        "login_page_url": "http://45.82.67.20/ints/login",
        "login_post_url": "http://45.82.67.20/ints/signin",
        "ajax_path": "/ints/agent/res/data_smscdr.php",
        "check_interval": 16,
        "timeout": 30,
        "enabled": True
    },
    "Roxy SMS": {
        "name": "Roxy SMS",
        "accounts": [
            {
                "id": str(uuid.uuid4()),
                "username": "sool",
                "password": "Yo123"
            }
        ],
        "base_url": "http://www.roxysms.net",
        "login_page_url": "http://www.roxysms.net/Login",
        "login_post_url": "http://www.roxysms.net/signin",
        "ajax_path": "/agent/res/data_smscdr.php",
        "check_interval": 5,
        "timeout": 30,
        "enabled": True,
        "use_scraper": True
    },
    "TimeSMS": {
        "name": "TimeSMS",
        "accounts": [
            {
                "id": str(uuid.uuid4()),
                "username": "a",
                "password": "7"
            }
        ],
        "base_url": "https://timesms.org",
        "login_page_url": "https://timesms.org/login",
        "login_post_url": "http://timesms.org/signin",
        "ajax_path": "/agent/res/data_smscdr.php",
        "check_interval": 5,
        "timeout": 30,
        "enabled": True
    }
}

def migrate_old_settings(settings):
    migrated = False
    for site_key in ["GROUP", "Fly sms", "Number_Panel", "Bolt", "iVASMS", "MSI", "proton SMS", "IMS", "Roxy SMS", "TimeSMS"]:
        if site_key in settings:
            if "username" in settings[site_key] and "accounts" not in settings[site_key]:
                old_username = settings[site_key]["username"]
                old_password = settings[site_key]["password"]
                settings[site_key]["accounts"] = [
                    {
                        "id": str(uuid.uuid4()),
                        "username": old_username,
                        "password": old_password
                    }
                ]
                del settings[site_key]["username"]
                del settings[site_key]["password"]
                migrated = True
            
            if settings[site_key].get("check_interval", 5) == 7:
                settings[site_key]["check_interval"] = 5
                migrated = True
                print(f"✅ স্পিড আপডেট {site_key} 7 থেকে 5 সেকেন্ডে")
    
    if "iVASMS" not in settings:
        settings["iVASMS"] = DEFAULT_SETTINGS["iVASMS"].copy()
        migrated = True
        print("✅ সাইট যোগ করা হয়েছে iVASMS সেটিংসে")
    
    if "MSI" not in settings:
        settings["MSI"] = DEFAULT_SETTINGS["MSI"].copy()
        migrated = True
    
    if "proton SMS" not in settings:
        settings["proton SMS"] = DEFAULT_SETTINGS["proton SMS"].copy()
        migrated = True
    
    if "IMS" not in settings:
        settings["IMS"] = DEFAULT_SETTINGS["IMS"].copy()
        migrated = True

    if "Roxy SMS" not in settings:
        settings["Roxy SMS"] = DEFAULT_SETTINGS["Roxy SMS"].copy()
        migrated = True

    if "TimeSMS" not in settings:
        settings["TimeSMS"] = DEFAULT_SETTINGS["TimeSMS"].copy()
        migrated = True
    
    if "Share" in settings and "proton SMS" not in settings:
        settings["proton SMS"] = settings["Share"].copy()
        settings["proton SMS"]["name"] = "proton SMS"
        del settings["Share"]
        migrated = True
    elif "Share" in settings:
        del settings["Share"]
        migrated = True
    
    return settings, migrated

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                settings, migrated = migrate_old_settings(settings)
                if migrated:
                    save_settings(settings)
                return settings
        except:
            pass
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)

def get_site_accounts(site_key):
    return SETTINGS.get(site_key, {}).get("accounts", [])

def add_account(site_key, username, password):
    if site_key not in SETTINGS:
        return False
    account = {
        "id": str(uuid.uuid4()),
        "username": username,
        "password": password
    }
    if "accounts" not in SETTINGS[site_key]:
        SETTINGS[site_key]["accounts"] = []
    SETTINGS[site_key]["accounts"].append(account)
    save_settings(SETTINGS)
    return account

def delete_account(site_key, account_id):
    global account_stop_events
    if site_key not in SETTINGS or "accounts" not in SETTINGS[site_key]:
        return False
    accounts = SETTINGS[site_key]["accounts"]
    initial_count = len(accounts)
    SETTINGS[site_key]["accounts"] = [acc for acc in accounts if acc["id"] != account_id]
    if len(SETTINGS[site_key]["accounts"]) < initial_count:
        stop_key = f"{site_key}_{account_id}"
        if stop_key in account_stop_events:
            account_stop_events[stop_key].set()
            print(f"🛑 অ্যাকাউন্টের মনিটরিং বন্ধ করা হয়েছে: {stop_key}")
            del account_stop_events[stop_key]
        
        cookies_file = f"cookies_{site_key}_{account_id}.pkl"
        last_message_file = f"last_message_{site_key}_{account_id}.txt"
        sent_messages_file = f"sent_messages_{site_key}_{account_id}.json"
        
        for file_path in [cookies_file, last_message_file, sent_messages_file]:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"🗑️ ফাইল মুছে ফেলা হয়েছে: {file_path}")
                except Exception as e:
                    print(f"⚠️ মুছতে ত্রুটি: {file_path}: {e}")
        
        if stop_key in account_sessions:
            del account_sessions[stop_key]
        if stop_key in account_last_seen:
            del account_last_seen[stop_key]
        
        save_settings(SETTINGS)
        return True
    return False

def get_account_by_id(site_key, account_id):
    accounts = get_site_accounts(site_key)
    for acc in accounts:
        if acc["id"] == account_id or acc["id"].startswith(account_id):
            return acc
    return None

def load_sessions():
    if os.path.exists(SESSIONS_FILE):
        try:
            with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {}

def save_sessions(sessions):
    with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(sessions, f, indent=2, ensure_ascii=False)

SETTINGS = load_settings()
SESSIONS = load_sessions()

def get_first_account(site_key):
    accounts = get_site_accounts(site_key)
    return accounts[0] if accounts else {"username": "", "password": ""}

USERNAME = get_first_account("GROUP").get("username", "")
PASSWORD = get_first_account("GROUP").get("password", "")
BASE_URL = SETTINGS["GROUP"]["base_url"]
LOGIN_PAGE_URL = SETTINGS["GROUP"]["login_page_url"]
LOGIN_POST_URL = SETTINGS["GROUP"]["login_post_url"]
AJAX_PATH = SETTINGS["GROUP"]["ajax_path"]
HTTP_TIMEOUT = SETTINGS["GROUP"]["timeout"]
CHECK_INTERVAL = SETTINGS["GROUP"]["check_interval"]

USERNAME2 = get_first_account("Fly sms").get("username", "")
PASSWORD2 = get_first_account("Fly sms").get("password", "")
BASE_URL2 = SETTINGS["Fly sms"]["base_url"]
LOGIN_PAGE_URL2 = SETTINGS["Fly sms"]["login_page_url"]
LOGIN_POST_URL2 = SETTINGS["Fly sms"]["login_post_url"]
AJAX_PATH2 = SETTINGS["Fly sms"]["ajax_path"]
HTTP_TIMEOUT2 = SETTINGS["Fly sms"]["timeout"]
CHECK_INTERVAL2 = SETTINGS["Fly sms"]["check_interval"]

USERNAME3 = get_first_account("Number_Panel").get("username", "")
PASSWORD3 = get_first_account("Number_Panel").get("password", "")
BASE_URL3 = SETTINGS["Number_Panel"]["base_url"]
LOGIN_PAGE_URL3 = SETTINGS["Number_Panel"].get("login_page_url", "")
LOGIN_POST_URL3 = SETTINGS["Number_Panel"].get("login_post_url", "")
AJAX_PATH3 = SETTINGS["Number_Panel"].get("ajax_path", "")
HTTP_TIMEOUT3 = SETTINGS["Number_Panel"]["timeout"]
CHECK_INTERVAL3 = SETTINGS["Number_Panel"]["check_interval"]

USERNAME4 = get_first_account("Bolt").get("username", "")
PASSWORD4 = get_first_account("Bolt").get("password", "")
BASE_URL4 = SETTINGS["Bolt"]["base_url"]
LOGIN_PAGE_URL4 = SETTINGS["Bolt"]["login_page_url"]
LOGIN_POST_URL4 = SETTINGS["Bolt"]["login_post_url"]
AJAX_PATH4 = SETTINGS["Bolt"]["ajax_path"]
HTTP_TIMEOUT4 = SETTINGS["Bolt"]["timeout"]
CHECK_INTERVAL4 = SETTINGS["Bolt"]["check_interval"]

USERNAME5 = get_first_account("iVASMS").get("username", "")
PASSWORD5 = get_first_account("iVASMS").get("password", "")
IVASMS_API_URL = SETTINGS["iVASMS"].get("api_url", "https://maroon-wombat-183778.hostingersite.com/apiivasms/api.php")
IVASMS_API_KEY = get_first_account("iVASMS").get("api_key", "")
HTTP_TIMEOUT5 = SETTINGS["iVASMS"]["timeout"]
CHECK_INTERVAL5 = SETTINGS["iVASMS"]["check_interval"]
LOGIN_PAGE_URL5 = ""
LOGIN_POST_URL5 = ""
SMS_RECEIVED_URL5 = ""
GET_SMS_URL5 = ""
GET_SMS_NUMBER_URL5 = ""
GET_SMS_MESSAGE_URL5 = ""

USERNAME6 = get_first_account("MSI").get("username", "")
PASSWORD6 = get_first_account("MSI").get("password", "")
BASE_URL6 = SETTINGS["MSI"]["base_url"]
LOGIN_PAGE_URL6 = SETTINGS["MSI"]["login_page_url"]
LOGIN_POST_URL6 = SETTINGS["MSI"]["login_post_url"]
AJAX_PATH6 = SETTINGS["MSI"]["ajax_path"]
HTTP_TIMEOUT6 = SETTINGS["MSI"]["timeout"]
CHECK_INTERVAL6 = SETTINGS["MSI"]["check_interval"]

USERNAME7 = get_first_account("proton SMS").get("username", "")
PASSWORD7 = get_first_account("proton SMS").get("password", "")
BASE_URL7 = SETTINGS["proton SMS"]["base_url"]
LOGIN_PAGE_URL7 = SETTINGS["proton SMS"]["login_page_url"]
LOGIN_POST_URL7 = SETTINGS["proton SMS"]["login_post_url"]
AJAX_PATH7 = SETTINGS["proton SMS"]["ajax_path"]
HTTP_TIMEOUT7 = SETTINGS["proton SMS"]["timeout"]
CHECK_INTERVAL7 = SETTINGS["proton SMS"]["check_interval"]

USERNAME8 = get_first_account("IMS").get("username", "")
PASSWORD8 = get_first_account("IMS").get("password", "")
BASE_URL8 = SETTINGS["IMS"]["base_url"]
LOGIN_PAGE_URL8 = SETTINGS["IMS"]["login_page_url"]
LOGIN_POST_URL8 = SETTINGS["IMS"]["login_post_url"]
AJAX_PATH8 = SETTINGS["IMS"]["ajax_path"]
HTTP_TIMEOUT8 = SETTINGS["IMS"]["timeout"]
CHECK_INTERVAL8 = SETTINGS["IMS"]["check_interval"]

USERNAME9 = get_first_account("Roxy SMS").get("username", "")
PASSWORD9 = get_first_account("Roxy SMS").get("password", "")
BASE_URL9 = SETTINGS["Roxy SMS"]["base_url"]
LOGIN_PAGE_URL9 = SETTINGS["Roxy SMS"]["login_page_url"]
LOGIN_POST_URL9 = SETTINGS["Roxy SMS"]["login_post_url"]
AJAX_PATH9 = SETTINGS["Roxy SMS"]["ajax_path"]
HTTP_TIMEOUT9 = SETTINGS["Roxy SMS"]["timeout"]
CHECK_INTERVAL9 = SETTINGS["Roxy SMS"]["check_interval"]

USERNAME10 = get_first_account("TimeSMS").get("username", "")
PASSWORD10 = get_first_account("TimeSMS").get("password", "")
BASE_URL10 = SETTINGS["TimeSMS"]["base_url"]
LOGIN_PAGE_URL10 = SETTINGS["TimeSMS"]["login_page_url"]
LOGIN_POST_URL10 = SETTINGS["TimeSMS"]["login_post_url"]
AJAX_PATH10 = SETTINGS["TimeSMS"]["ajax_path"]
HTTP_TIMEOUT10 = SETTINGS["TimeSMS"]["timeout"]
CHECK_INTERVAL10 = SETTINGS["TimeSMS"]["check_interval"]

COOKIES_FILE = "cookies.pkl"
COOKIES_FILE_SITE3 = "cookies_site3.pkl"
COOKIES_FILE_SITE4 = "cookies_site4.pkl"
COOKIES_FILE_SITE5 = "cookies_ivasms.json"
COOKIES_FILE_SITE6 = "cookies_msi.pkl"
COOKIES_FILE_SITE7 = "cookies_share.pkl"
COOKIES_FILE_SITE8 = "cookies_ims.pkl"
COOKIES_FILE_SITE9 = "cookies_roxy.pkl"
COOKIES_FILE_SITE10 = "cookies_timesms.pkl"
LAST_MESSAGE_FILE = "last_message.txt"
LAST_MESSAGE_FILE_SITE2 = "last_message_site2.txt"
LAST_MESSAGE_FILE_SITE3 = "last_message_site3.txt"
LAST_MESSAGE_FILE_SITE4 = "last_message_site4.txt"
LAST_MESSAGE_FILE_SITE5 = "last_message_ivasms.txt"
LAST_MESSAGE_FILE_SITE6 = "last_message_msi.txt"
LAST_MESSAGE_FILE_SITE7 = "last_message_share.txt"
LAST_MESSAGE_FILE_SITE8 = "last_message_ims.txt"
LAST_MESSAGE_FILE_SITE9 = "last_message_roxy.txt"
LAST_MESSAGE_FILE_SITE10 = "last_message_timesms.txt"

account_scrapers = {}
account_sessions = {}
account_last_seen = {}
account_stop_events = {}

IDX_DATE_SITE3 = 0
IDX_NUMBER_SITE3 = 2
IDX_SMS_SITE3 = 5

def create_session_group():
    
    sess = requests.Session()
    sess.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    })
    return sess

session1 = create_session_group()
is_logged_in_site1 = False
bot = telebot.TeleBot(BOT_TOKEN)
last_seen_key = ""
last_seen_key_site2 = ""
last_seen_key_site3 = ""
last_seen_key_site4 = ""

account_sessions = {}

session2 = requests.Session()
session2.headers.update({
    "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": BASE_URL2 + "/ints/agent/SMSCDRReports",
    "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8"
})
is_logged_in_site2 = False

session3 = requests.Session()
session3.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9,ar;q=0.8"
})
is_logged_in_site3 = False

session4 = requests.Session()
session4.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9,ar;q=0.8"
})
is_logged_in_site4 = False

session6 = requests.Session()
session6.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": BASE_URL6 + "/agent/SMSCDRReports",
    "Accept-Language": "en-US,en;q=0.9,ar;q=0.8"
})
is_logged_in_site6 = False
last_seen_key_site6 = ""

session7 = requests.Session()
session7.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": BASE_URL7 + "/agent/SMSCDRReports",
    "Accept-Language": "en-US,en;q=0.9,ar;q=0.8"
})
is_logged_in_site7 = False
last_seen_key_site7 = ""

session8 = requests.Session()
session8.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
})
is_logged_in_site8 = False
last_seen_key_site8 = ""

session9 = requests.Session()
session9.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
})
is_logged_in_site9 = False
last_seen_key_site9 = ""

session10 = requests.Session()
session10.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
})
is_logged_in_site10 = False
last_seen_key_site10 = ""

session5 = requests.Session()
session5.verify = False
session5.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive"
})
is_logged_in_site5 = False
csrf_token_site5 = None
last_seen_key_site5 = ""

COUNTRIES_FILE = "countriesi.json"
CHANNELS_FILE = "channelsi.json"
USERS_FILE = "usersi.json"
ADMINS_FILE = "admins.ijson"
BANNED_FILE = "bannedi.json"
OTP_GROUP_FILE = "otp_groupi.json"
GROUPS_FILE = "groupsi.json"
STATISTICS_FILE = "statisticsi.json"
REFERRALS_FILE = "referralsi.json"
REFERRAL_SETTINGS_FILE = "referral_settings.json"
WITHDRAWAL_REQUESTS_FILE = "withdrawal_requests.json"
WITHDRAWAL_METHODS_FILE = "withdrawal_methods.json"
WELCOME_MESSAGES_FILE = "welcome_messages.json"
NUMBERS_ADMINS_FILE = "numbers_admins.json"
COUNTRIES = {}
CHANNELS = []
USERS = {}
ADMINS = []
BANNED = []
OTP_GROUP = -1003852565392
GROUPS = [-1003852565392]
REFERRALS = {}
NUMBERS_ADMINS = []

def load_numbers_admins():
    global NUMBERS_ADMINS
    if os.path.exists(NUMBERS_ADMINS_FILE):
        try:
            with open(NUMBERS_ADMINS_FILE, "r", encoding="utf-8") as f:
                NUMBERS_ADMINS = json.load(f)
        except:
            NUMBERS_ADMINS = []
    return NUMBERS_ADMINS

def save_numbers_admins():
    with open(NUMBERS_ADMINS_FILE, "w", encoding="utf-8") as f:
        json.dump(NUMBERS_ADMINS, f, indent=2, ensure_ascii=False)

def is_numbers_admin(user_id):
    return user_id in NUMBERS_ADMINS or is_admin(user_id)

DEFAULT_REFERRAL_SETTINGS = {
    "codes_required_for_referral": 10,
    "referral_bonus": 0.05,
    "code_bonus": 0.002,
    "min_withdrawal": 5.0,
    "enabled": True
}

DEFAULT_WELCOME_MESSAGES = {
    "ar": "🌐 <b>অস্থায়ী নম্বর বটে স্বাগতম!</b>\n\n📱 সাথে সাথে অস্থায়ী নম্বর নিন\n🔒 নিরাপদ ও দ্রুত\n💰 রেফারেল ও কোড থেকে আয় করুন\n\nমেনু থেকে বেছে নিন:",
    "en": "🌐 <b>Welcome to Temporary Numbers Bot!</b>\n\n📱 Get a temporary number instantly\n🔒 Secure and fast\n💰 Earn from referrals and codes\n\nChoose from the menu:"
}

DEFAULT_BUTTON_LINKS = {
    "group_link": "https://t.me/alorhawa",
    "channel_link": "https://t.me/alorhawa",
    "developer_link": "https://t.me/alorhawa"
}

BUTTON_LINKS_FILE = "button_links.json"
OTP_BUTTONS_FILE = "otp_buttons.json"

DEFAULT_OTP_BUTTONS = [
    {"name": "𝙂𝙍𝙊𝙐𝙋", "url": "https://t.me/alorhawa"},
    {"name": "𝘽𝙊𝙏", "url": "https://t.me/alorhawabot "}, 
        {"name": "𝙊𝙏𝙋", "url": "https://t.me/alorhawa"}, 
           {"name": "❍𓏺 𝗨𝗻𝗖𝗹𝗘 | 𝗗𝟕 𓏺 𝗕𝗘𝗣𝗢↬", "url": "https://t.me/alorhawa"}
]

def load_otp_buttons():
    if os.path.exists(OTP_BUTTONS_FILE):
        try:
            with open(OTP_BUTTONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return DEFAULT_OTP_BUTTONS.copy()

def save_otp_buttons(buttons):
    with open(OTP_BUTTONS_FILE, "w", encoding="utf-8") as f:
        json.dump(buttons, f, indent=2, ensure_ascii=False)

OTP_BUTTONS = load_otp_buttons()

def format_decimal(value):
    
    if value == 0:
        return "0"
    
    formatted = f"{value:.10f}".rstrip('0').rstrip('.')
    
    if '.' in formatted:
        integer_part, decimal_part = formatted.split('.')
        if len(decimal_part) > 5:
            decimal_part = decimal_part[:5]
        return f"{integer_part}.{decimal_part}"
    return formatted

def load_button_links():
    if os.path.exists(BUTTON_LINKS_FILE):
        try:
            with open(BUTTON_LINKS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return DEFAULT_BUTTON_LINKS.copy()

def save_button_links(links):
    with open(BUTTON_LINKS_FILE, "w", encoding="utf-8") as f:
        json.dump(links, f, indent=2, ensure_ascii=False)

BUTTON_LINKS = load_button_links()
STATISTICS = {
    "total_codes": 0,
    "codes_today": 0,
    "codes_this_week": 0,
    "codes_this_month": 0,
    "last_reset_day": None,
    "last_reset_week": None,
    "last_reset_month": None,
    "daily_history": {}
}

user_states = {}
broadcast_state = {}

TEXTS = {
    "ar": {
        "welcome": "🌐 <b>নম্বর বটে স্বাগতম!</b>",
        "instructions": "📖 <b>বট গাইড</b>\n\n<b>📱 কোড গ্রহণ:</b>\n1️⃣ চাপুন Get Number\n2️⃣ দেশ ও নম্বর বেছে নিন\n3️⃣ রেজিস্ট্রেশনে নম্বরটি ব্যবহার করুন\n4️⃣ কোড স্বয়ংক্রিয়ভাবে আসবে\n\n<b>💰 আয়:</b>\n• প্রতিটি কোডের বোনাস\n• বন্ধু রেফারেল বোনাস\n\n<b>💵 উত্তোলন:</b>\nভোডাফোন ক্যাশ - USDT - Binance",
        "subscription_locked": "🔒 <b>প্রবেশ বন্ধ। চ্যানেলে জয়েন করে যাচাই করুন।</b>",
        "subscription_verified": "✅ <b>সাবস্ক্রিপশন যাচাই হয়েছে!</b>\n\n🌐 <b>নম্বর বটে স্বাগতম!</b>",
        "subscription_not_verified": "❌ আপনি এখনো সব চ্যানেলে জয়েন করেননি!",
        "choose_country": "📲 𝗚𝗲𝘁 𝗡𝘂𝗺𝗯𝗲𝗿",
        "my_account": "👤 𝗠𝘆 𝗔𝗰𝗰𝗼𝘂𝗻𝘁",
        "admin_panel": "🎛 অ্যাডমিন প্যানেল",
        "help": "❓ সাহায্য",
        "verify_subscription": "✅ সাবস্ক্রিপশন যাচাই করুন",
        "banned": "🚫 আপনাকে এই বট ব্যবহারে ব্যান করা হয়েছে।",
        "unauthorized": "❌ আপনার অনুমতি নেই!",
        "select_country": "📱 <b>প্ল্যাটফর্ম বেছে নিন:</b>",
        "back": "🔙 ফিরে যান",
        "select_number": "📞 <b>নম্বর বেছে নিন: {country}:</b>",
        "number_locked": "⚠️ এই নম্বরটি এখন অন্য কেউ ব্যবহার করছে। অন্য নম্বর বেছে নিন।",
        "your_number": "📞 <b>আপনার নম্বর: {country}:</b>\n<code>+{number}</code>\n\n⏳ <b>কোডের অপেক্ষায়...</b> 📱\n\n💬 কোড সরাসরি এখানে পাঠানো হবে!",
        "change_number": "🔄 নম্বর পরিবর্তন",
        "change_country": "🌍 দেশ পরিবর্তন",
        "account_info": "👤 <b>আপনার অ্যাকাউন্টের তথ্য:</b>\n\n🆔 <b>আপনার আইডি:</b> <code>{user_id_value}</code>\n📅 <b>যোগদানের তারিখ:</b> {join_date}\n📊 <b>প্রাপ্ত কোড:</b> {activations}\n🌐 <b>ভাষা:</b> {language}\n\n💡 <b>আপনার নম্বরের অবস্থা:</b>\n{number_status}",
        "no_number": "❌ এখন কোনো নম্বর নেই",
        "has_number": "✅ সক্রিয় নম্বর: {country}",
        "change_language": "🌐 ভাষা পরিবর্তন",
        "language_changed": "✅ ভাষা বাংলায় পরিবর্তন করা হয়েছে",
        "add_channel": "➕ সাবস্ক্রিপশন চ্যানেল যোগ",
        "remove_channel": "🗑 চ্যানেল মুছুন",
        "statistics": "📊 পরিসংখ্যান",
        "broadcast": "📣 ব্রডকাস্ট",
        "add_admin": "🔧 অ্যাডমিন যোগ করুন",
        "remove_admin": "🗑 অ্যাডমিন মুছুন",
        "ban_user": "🚫 ইউজার ব্যান",
        "unban_user": "✅ আনব্যান",
        "set_otp_group": "📱 গ্রুপ সেট করুন OTP",
        "close": "❌ বন্ধ করুন",
        "new_code": "🔔 <b>নতুন কোড!</b>\n\n📞 <b>নম্বর:</b> <code>+{number}</code>\n💬 <b>কোড:</b> <code>{code}</code>\n\n⏰ <b>সময়:</b> {time}",
        "no_countries_available": "❌ এখন কোনো দেশ উপলব্ধ নেই!",
        "country_not_available": "❌ দেশটি উপলব্ধ নয়!",
        "no_numbers_available": "❌ কোনো নম্বর উপলব্ধ নেই!",
        "number_reserved": "❌ এই নম্বরটি এখন সংরক্ষিত!",
        "select_country_first": "❌ আগে প্ল্যাটফর্ম বেছে নিন!",
        "number_changed": "✅ নম্বর পরিবর্তন হয়েছে!",
        "admin_panel_title": "🎛 <b>অ্যাডমিন প্যানেল</b>",
        "statistics_title": "📊 <b>বটের পরিসংখ্যান</b>\n\n👥 <b>মোট ইউজার:</b> {users_count}\n🔢 <b>মোট কোড:</b> {total_codes}\n\n📅 <b>আজকের কোড:</b> {codes_today}\n📆 <b>এই সপ্তাহের কোড:</b> {codes_this_week}\n📊 <b>এই মাসের কোড:</b> {codes_this_month}",
        "broadcast_prompt": "📣 <b>মেসেজ ব্রডকাস্ট</b>\n\nসব ইউজারকে যে মেসেজ ব্রডকাস্ট করতে চান তা পাঠান:",
        "broadcast_sent": "✅ <b>পাঠানো হয়েছে!</b>\n\n📤 সফল: {success}\n❌ ব্যর্থ: {failed}",
        "set_otp_group_prompt": "📱 <b>গ্রুপ সেট করুন OTP</b>\n\nগ্রুপের আইডি পাঠান (Group ID) যেখানে কোড পাঠাতে চান:",
        "otp_group_set": "✅ <b>গ্রুপ সেট করা হয়েছে OTP!</b>\n\n🆔 Group ID: <code>{group_id}</code>",
        "invalid_id": "❌ আইডি ভুল! সংখ্যা পাঠান ID সঠিক",
        "add_channel_id_prompt": "➕ <b>বাধ্যতামূলক সাবস্ক্রিপশন চ্যানেল যোগ</b>\n\n⚠️ শুধু চ্যানেল গ্রহণযোগ্য (গ্রুপ নয়)\n\nচ্যানেলের আইডি বা লিংক পাঠান:\n• @channel_name\n• https://t.me/channel_name",
        "add_channel_name_prompt": "",
        "add_channel_url_prompt": "",
        "channel_added": "✅ <b>চ্যানেল যোগ হয়েছে!</b>\n\n📢 চ্যানেল: {channel_name}\n🔗 লিংক: {channel_url}",
        "user_banned": "✅ <b>ইউজারকে ব্যান করা হয়েছে!</b>\n\n🆔 User ID: <code>{target_user_id}</code>",
        "user_unbanned": "✅ <b>ইউজার আনব্যান করা হয়েছে!</b>\n\n🆔 User ID: <code>{target_user_id}</code>",
        "admin_added": "✅ <b>অ্যাডমিন যোগ হয়েছে!</b>\n\n🆔 User ID: <code>{target_user_id}</code>",
        "admin_removed": "✅ <b>অ্যাডমিন মুছে ফেলা হয়েছে!</b>\n\n🆔 User ID: <code>{target_user_id}</code>",
        "channel_removed": "✅ <b>চ্যানেল মুছে ফেলা হয়েছে!</b>\n\n📢 চ্যানেল: {channel_name}",
        "no_channels": "⚠️ কোনো চ্যানেল নেই!",
        "no_banned_users": "⚠️ কোনো ব্যান করা ইউজার নেই!",
        "no_admins": "⚠️ কোনো অ্যাডমিন নেই!",
        "owner_only": "❌ এই ফিচার শুধু মালিকের জন্য!",
        "ban_user_prompt": "🚫 <b>ইউজার ব্যান</b>\n\nইউজারের আইডি পাঠান (User ID) যাকে ব্যান করতে চান:",
        "unban_user_prompt": "✅ <b>ইউজার আনব্যান</b>\n\n📋 <b>ব্যান করা ইউজার:</b>\n{banned_list}\n\nআনব্যান করতে ইউজারের আইডি পাঠান:",
        "add_moderator_prompt": "🔧 <b>অ্যাডমিন যোগ করুন</b>\n\nইউজারের আইডি পাঠান (User ID) যাকে অ্যাডমিন বানাতে চান:",
        "remove_moderator_prompt": "🗑 <b>অ্যাডমিন মুছুন</b>\n\n📋 <b>বর্তমান অ্যাডমিনরা:</b>\n{admins_list}\n\nমুছতে অ্যাডমিনের আইডি পাঠান:",
        "remove_channel_prompt": "🗑 <b>চ্যানেল মুছুন</b>\n\n📋 <b>বর্তমান চ্যানেল:</b>\n{channels_list}\n\nমুছতে চ্যানেলের নম্বর বা আইডি পাঠান:",
        "channel_not_found": "❌ চ্যানেল পাওয়া যায়নি!",
        "otp_group_status": "📱 <b>কোড গ্রুপ:</b>\n{status}",
        "otp_group_set_status": "✅ নির্ধারিত গ্রুপ: <code>{group_id}</code>",
        "otp_group_not_set": "❌ কোনো গ্রুপ নির্ধারণ করা হয়নি",
        "delete_otp_group": "🗑 গ্রুপ মুছুন",
        "otp_group_deleted": "✅ কোড গ্রুপ মুছে ফেলা হয়েছে!",
        "top_users": "👥 সেরা 10 ইউজার",
        "top_users_title": "👥 <b>সেরা 10 ইউজার</b>\n<i>প্রাপ্ত কোডের সংখ্যা অনুযায়ী</i>\n\n",
        "no_users_yet": "⚠️ এখনো কোনো ইউজার নেই!",
        "user_joined": "🎉 <b>নতুন ইউজার জয়েন করেছে!</b>\n\n👤 নাম: {name}\n🆔 ID: <code>{user_id}</code>\n📅 সময়: {time}",
        "edit_button_labels_ar": "🇧🇩 বাংলা বাটন এডিট",
        "edit_button_labels_en": "🇬🇧 ইংরেজি বাটন এডিট",
        "edit_button_labels_lang": "🏷️ <b>বাটনের নাম এডিট</b>\n\nভাষা বেছে নিন:",
        "edit_labels_ar_menu": "🇧🇩 <b>বাংলা বাটন এডিট</b>\n\nযে বাটন এডিট করতে চান সেটি বেছে নিন:",
        "edit_labels_en_menu": "🇬🇧 <b>Edit Button Labels (English)</b>\n\nChoose the button you want to edit:",
        "edit_choose_country_ar": "এডিট \"দেশ বেছে নিন\"",
        "edit_my_account_ar": "এডিট \"আমার অ্যাকাউন্ট\"",
        "edit_help_ar": "এডিট \"𝗛𝗲𝗹𝗽❓\"",
        "edit_choose_country_en": "Edit \"Choose Country\"",
        "edit_my_account_en": "Edit \"My Account\"",
        "edit_help_en": "Edit \"Help\"",
        "send_new_label": "📝 বাটনের নতুন নাম পাঠান:",
        "label_updated": "✅ বাটনের নাম সফলভাবে আপডেট হয়েছে!",
        "manage_otp_group": "📱 কোড গ্রুপ ম্যানেজমেন্ট",
        "welcome_admin": "🌐 <b>স্বাগতম এই বটে: OTP!</b>\n\nনম্বর পেতে একটি দেশ বেছে নিন এবং কোডের অপেক্ষা করুন।\n\nঅ্যাডমিন হিসেবে আপনি অ্যাডমিন প্যানেলেও যেতে পারবেন।",
        "choose_language": "🌍 <b>ভাষা বেছে নিন / Choose Language</b>",
        "group_hello_admin": "👋 হ্যালো! আমি একটি বট OTP.\n\n⚠️ <b>নোট:</b> গ্রুপ স্বয়ংক্রিয়ভাবে যোগ করা যায় না।\nঅ্যাডমিনকে অ্যাডমিন প্যানেল থেকে এই গ্রুপ যোগ করতে হবে।",
        "group_hello": "👋 হ্যালো! আমি একটি বট OTP.\n\nব্যবহারের জন্য আমার সাথে প্রাইভেটে যোগাযোগ করুন।",
        "total_users": "👥 <b>মোট ইউজার:</b>",
        "total_codes": "🔢 <b>মোট কোড:</b>",
        "codes_today": "📅 <b>আজকের কোড:</b>",
        "codes_week": "📆 <b>এই সপ্তাহের কোড:</b>",
        "codes_month": "📊 <b>এই মাসের কোড:</b>",
        "users_text": "users / ইউজার",
        "developer_btn": "🆘 ডেভেলপার",
        "verify_btn": "✅ যাচাই",
        "select_server_title": "🖥️ <b>সার্ভার বেছে নিন</b>",
        "select_server_desc": "📌 প্রতিটি সার্ভারে আলাদা দেশ ও নম্বর আছে:",
        "select_server_hint": "🔻 <i>উপলব্ধ দেশ দেখতে সার্ভার বেছে নিন</i>",
        "select_platform_title": "📱 <b>প্ল্যাটফর্ম বেছে নিন: {server}</b>",
        "select_platform_hint": "🔻 <i>যে প্ল্যাটফর্মের কোড পেতে চান সেটি বেছে নিন</i>",
        "no_numbers_here": "❌ <b>এখানে কোনো নম্বর নেই</b>",
        "no_countries_title": "❌ <b>কোনো দেশ উপলব্ধ নেই</b>",
        "server_label": "🖥️ <b>সার্ভার:</b>",
        "platform_label": "📱 <b>প্ল্যাটফর্ম:</b>",
        "no_countries_hint": "🔻 <i>এই সার্ভারে এই প্ল্যাটফর্মের জন্য এখন কোনো দেশ উপলব্ধ নেই</i>",
        "available_countries_title": "🌍 <b>উপলব্ধ দেশসমূহ</b>",
        "select_country_hint": "🔻 <i>যে দেশের কোড পেতে চান সেটি বেছে নিন</i>",
        "number_selected_success": "✅ <b>নম্বর সফলভাবে বাছাই হয়েছে!</b>",
        "waiting_for_code": "⏳ 𝓦𝓪𝓲𝓽𝓲𝓷𝓰 𝓯𝓸𝓻 𝓽𝓱𝓮 𝓬𝓸𝓭𝓮... 📱",
        "code_will_be_sent": "কোড আসামাত্র আপনাকে সরাসরি পাঠানো হবে!",
        "change_number_btn": "🔄 নম্বর পরিবর্তন",
        "change_country_btn": "🌍 দেশ পরিবর্তন",
        "back_to_servers": "𝗕𝗮𝗰𝗸 𝘁𝗼 𝘀𝗲𝗿𝘃𝗲𝗿𝘀",
        "error_msg": "❌ ত্রুটি: {error}",
        "referral_success": "🎉 <b>রেফারেল লিংকের মাধ্যমে আপনি সফলভাবে নিবন্ধিত হয়েছেন!</b>\n\nবট ব্যবহার উপভোগ করুন!"
    },
    "en": {
        "welcome": "╔════✦  𝓑𝓞𝓣𝓟  ✦════╗\n\n❖  𝗚𝗿𝗮𝗯 𝗮 𝘁𝗲𝗺𝗽𝗼𝗿𝗮𝗿𝘆 𝗻𝘂𝗺𝗯𝗲𝗿 𝗶𝗻𝘀𝘁𝗮𝗻𝘁𝗹𝘆\n❖  𝗟𝗶𝗴𝗵𝘁𝗻𝗶𝗻𝗴-𝗳𝗮𝘀𝘁 & 𝗳𝘂𝗹𝗹𝘆 𝘀𝗲𝗰𝘂𝗿𝗲\n❖  𝗪𝗼𝗿𝗸𝘀 𝗳𝗼𝗿 𝗮𝗹𝗹 𝗰𝗼𝘂𝗻𝘁𝗿𝗶𝗲𝘀\n\n•  𝗦𝗲𝗹𝗲𝗰𝘁 𝘆𝗼𝘂𝗿 𝗰𝗼𝘂𝗻𝘁𝗿𝘆\n•  𝗚𝗲𝘁 𝘆𝗼𝘂𝗿 𝗻𝘂𝗺𝗯𝗲𝗿 𝗶𝗺𝗺𝗲𝗱𝗶𝗮𝘁𝗲𝗹𝘆\n\n╚════✦  𝓑𝓞𝓣𝓟  ✦════╝",
        "instructions": "📖 <b>Bot Guide</b>\n\n<b>📱 Receiving Codes:</b>\n1️⃣ Click Get Number\n2️⃣ Choose country and number\n3️⃣ Use number to register\n4️⃣ Code arrives automatically\n\n<b>💰 Earnings:</b>\n• Bonus for each code\n• Referral bonus for friends\n\n<b>💵 Withdrawal:</b>\nVodafone Cash - USDT - Binance",
        "subscription_locked": "🔒 <b>Access locked. Join channels then verify.</b>",
        "subscription_verified": "✅ <b>Subscription verified!</b>\n\n🌐 <b>Welcome to Numbers Bot!</b>",
        "subscription_not_verified": "❌ You haven't joined all channels yet!",
        "choose_country": "📲 𝗚𝗲𝘁 𝗡𝘂𝗺𝗯𝗲𝗿",
        "my_account": "👤 𝗠𝘆 𝗔𝗰𝗰𝗼𝘂𝗻𝘁",
        "admin_panel": "🎛 Admin Panel",
        "help": "❓ Help",
        "verify_subscription": "✅ Verify Subscription",
        "banned": "🚫 You are banned from using this bot.",
        "unauthorized": "❌ Unauthorized!",
        "select_country": "🌍 <b>Select Country:</b>",
        "back": "🔙 Back",
        "select_number": "📞 <b>Select a number for {country}:</b>",
        "number_locked": "⚠️ This number is currently used by someone else. Choose another number.",
        "your_number": "📞 <b>Your number for {country}:</b>\n<code>+{number}</code>\n\n⏳ <b>Waiting for code...</b> 📱\n\n💬 Code will be sent here directly!",
        "change_number": "🔄 Change Number",
        "change_country": "🌍 Change Country",
        "account_info": "👤 <b>Your Account Info:</b>\n\n🆔 <b>ID:</b> <code>{user_id_value}</code>\n📅 <b>Join Date:</b> {join_date}\n📊 <b>Codes Received:</b> {activations}\n🌐 <b>Language:</b> {language}\n\n💡 <b>Number Status:</b>\n{number_status}",
        "no_number": "❌ No number currently",
        "has_number": "✅ Active number for {country}",
        "change_language": "🌐 Change Language",
        "language_changed": "✅ Language changed to English",
        "add_channel": "➕ Add Channel",
        "remove_channel": "🗑 Remove Channel",
        "statistics": "📊 Statistics",
        "broadcast": "📣 Broadcast",
        "add_admin": "🔧 Add Admin",
        "remove_admin": "🗑 Remove Admin",
        "ban_user": "🚫 Ban User",
        "unban_user": "✅ Unban User",
        "set_otp_group": "📱 Set OTP Group",
        "close": "❌ Close",
        "new_code": "🔔 <b>New Code!</b>\n\n📞 <b>Number:</b> <code>+{number}</code>\n💬 <b>Code:</b> <code>{code}</code>\n\n⏰ <b>Time:</b> {time}",
        "no_countries_available": "❌ No countries available!",
        "country_not_available": "❌ Country not available!",
        "no_numbers_available": "❌ No numbers available!",
        "number_reserved": "❌ This number is reserved!",
        "select_country_first": "❌ Select a country first!",
        "number_changed": "✅ Number changed!",
        "admin_panel_title": "🎛 <b>Admin Panel</b>",
        "statistics_title": "📊 <b>Bot Statistics</b>\n\n👥 <b>Total Users:</b> {users_count}\n🔢 <b>Total Codes:</b> {total_codes}\n\n📅 <b>Today's Codes:</b> {codes_today}\n📆 <b>This Week's Codes:</b> {codes_this_week}\n📊 <b>This Month's Codes:</b> {codes_this_month}",
        "broadcast_prompt": "📣 <b>Broadcast Message</b>\n\nSend the message you want to broadcast to all users:",
        "broadcast_sent": "✅ <b>Sent!</b>\n\n📤 Success: {success}\n❌ Failed: {failed}",
        "set_otp_group_prompt": "📱 <b>Set OTP Group</b>\n\nSend the Group ID where you want to receive OTP codes:",
        "otp_group_set": "✅ <b>OTP Group set!</b>\n\n🆔 Group ID: <code>{group_id}</code>",
        "invalid_id": "❌ Invalid ID! Send a valid ID number",
        "add_channel_id_prompt": "➕ <b>Add Subscription Channel</b>\n\nSend the channel ID (example: @channelname or -100...):",
        "add_channel_name_prompt": "✅ <b>Channel ID saved!</b>\n\nNow send the channel name:",
        "add_channel_url_prompt": "✅ <b>Channel name saved!</b>\n\nNow send the channel link (https://t.me/...):",
        "channel_added": "✅ <b>Channel added!</b>\n\n📢 Channel: {channel_name}\n🔗 Link: {channel_url}",
        "user_banned": "✅ <b>User banned!</b>\n\n🆔 User ID: <code>{target_user_id}</code>",
        "user_unbanned": "✅ <b>User unbanned!</b>\n\n🆔 User ID: <code>{target_user_id}</code>",
        "admin_added": "✅ <b>Admin added!</b>\n\n🆔 User ID: <code>{target_user_id}</code>",
        "admin_removed": "✅ <b>Admin removed!</b>\n\n🆔 User ID: <code>{target_user_id}</code>",
        "channel_removed": "✅ <b>Channel removed!</b>\n\n📢 Channel: {channel_name}",
        "no_channels": "⚠️ No channels!",
        "no_banned_users": "⚠️ No banned users!",
        "no_admins": "⚠️ No admins!",
        "owner_only": "❌ This feature is for owner only!",
        "ban_user_prompt": "🚫 <b>Ban User</b>\n\nSend the User ID you want to ban:",
        "unban_user_prompt": "✅ <b>Unban User</b>\n\n📋 <b>Banned Users:</b>\n{banned_list}\n\nSend the User ID to unban:",
        "add_moderator_prompt": "🔧 <b>Add Admin</b>\n\nSend the User ID you want to make admin:",
        "remove_moderator_prompt": "🗑 <b>Remove Admin</b>\n\n📋 <b>Current Admins:</b>\n{admins_list}\n\nSend the admin ID to remove:",
        "remove_channel_prompt": "🗑 <b>Remove Channel</b>\n\n📋 <b>Current Channels:</b>\n{channels_list}\n\nSend the channel number or ID to remove it:",
        "channel_not_found": "❌ Channel not found!",
        "otp_group_status": "📱 <b>OTP Group:</b>\n{status}",
        "otp_group_set_status": "✅ Group set: <code>{group_id}</code>",
        "otp_group_not_set": "❌ No group set",
        "delete_otp_group": "🗑 Delete Group",
        "otp_group_deleted": "✅ OTP group deleted!",
        "top_users": "👥 Top 10 Users",
        "top_users_title": "👥 <b>Top 10 Users</b>\n<i>By codes received</i>\n\n",
        "no_users_yet": "⚠️ No users yet!",
        "user_joined": "🎉 <b>New User Joined!</b>\n\n👤 Name: {name}\n🆔 ID: <code>{user_id}</code>\n📅 Time: {time}",
        "edit_button_labels_ar": "🇸🇦 Edit Arabic Buttons",
        "edit_button_labels_en": "🇬🇧 Edit English Buttons",
        "edit_button_labels_lang": "🏷️ <b>Edit Button Labels</b>\n\nChoose language:",
        "edit_labels_ar_menu": "🇧🇩 <b>বাংলা বাটন এডিট</b>\n\nযে বাটন এডিট করতে চান সেটি বেছে নিন:",
        "edit_labels_en_menu": "🇬🇧 <b>Edit Button Labels (English)</b>\n\nChoose the button you want to edit:",
        "edit_choose_country_ar": "এডিট \"দেশ বেছে নিন\"",
        "edit_my_account_ar": "এডিট \"আমার অ্যাকাউন্ট\"",
        "edit_help_ar": "এডিট \"𝗛𝗲𝗹𝗽❓\"",
        "edit_choose_country_en": "Edit \"Choose Country\"",
        "edit_my_account_en": "Edit \"My Account\"",
        "edit_help_en": "Edit \"Help\"",
        "send_new_label": "📝 Send the new button name:",
        "label_updated": "✅ Button label updated successfully!",
        "manage_otp_group": "📱 Manage OTP Group",
        "welcome_admin": "🌐 <b>Welcome to OTP Bot!</b>\n\nChoose a country to receive a number and wait for OTP.\n\nAs an admin, you can also access the Admin Panel.",
        "choose_language": "🌍 <b>ভাষা বেছে নিন / Choose Language</b>",
        "group_hello_admin": "👋 Hello! I'm the OTP Bot.\n\n⚠️ <b>Note:</b> Groups cannot be added automatically.\nThe admin must add this group from the admin panel.",
        "group_hello": "👋 Hello! I'm the OTP Bot.\n\nTo use me, contact me privately.",
        "total_users": "👥 <b>Total Users:</b>",
        "total_codes": "🔢 <b>Total Codes:</b>",
        "codes_today": "📅 <b>Codes Today:</b>",
        "codes_week": "📆 <b>Codes This Week:</b>",
        "codes_month": "📊 <b>Codes This Month:</b>",
        "users_text": "users",
        "developer_btn": "🆘 Developer",
        "verify_btn": "✅ Verify",
        "select_server_title": "🖥️ <b>Select Server</b>",
        "select_server_desc": "📌 Each server contains a different set of countries and numbers:",
        "select_server_hint": "🔻 <i>Select a server to view available countries</i>",
        "select_platform_title": "📱 <b>Select Platform in {server}</b>",
        "select_platform_hint": "🔻 <i>Select the platform you want to receive codes for</i>",
        "no_numbers_here": "❌ <b>No numbers available here</b>",
        "no_countries_title": "❌ <b>No countries available</b>",
        "server_label": "🖥️ <b>Server:</b>",
        "platform_label": "📱 <b>Platform:</b>",
        "no_countries_hint": "🔻 <i>No countries available for this platform in this server currently</i>",
        "available_countries_title": "🌍 <b>Available Countries</b>",
        "select_country_hint": "🔻 <i>Select the country you want to receive codes for</i>",
        "number_selected_success": "✅ <b>Number selected successfully!</b>",
        "waiting_for_code": "⏳ 𝓦𝓪𝓲𝓽𝓲𝓷𝓰 𝓯𝓸𝓻 𝓽𝓱𝓮 𝓬𝓸𝓭𝓮... 📱",
        "code_will_be_sent": "The code will be sent to you directly when it arrives!",
        "change_number_btn": "🔄 Change Number",
        "change_country_btn": "🌍 Change Country",
        "back_to_servers": "𝗕𝗮𝗰𝗸 𝘁𝗼 𝘀𝗲𝗿𝘃𝗲𝗿𝘀",
        "sticker_duration_error": "❌ Duration must be between 0.1 and 30 seconds!",
        "sticker_duration_set": "✅ <b>Sticker display duration set!</b>\n\n⏱ New duration: {duration} seconds",
        "invalid_number": "❌ Please send a valid number!\n\nExample: 0.5 or 1 or 2.5",
        "error_msg": "❌ Error: {error}",
        "referral_success": "🎉 <b>You've registered successfully via referral link!</b>\n\nEnjoy using the bot!"
    }
}

def get_user_language(user_id):
    user_data = USERS.get(str(user_id), {})
    return user_data.get("language", "ar")

def set_user_language(user_id, lang):
    if str(user_id) not in USERS:
        USERS[str(user_id)] = {}
    USERS[str(user_id)]["language"] = lang
    save_users()

def t(user_id, key):
    lang = get_user_language(user_id)
    return TEXTS.get(lang, TEXTS["ar"]).get(key, key)

def save_pickle(path, obj):
    with open(path, "wb") as f:
        pickle.dump(obj, f)

def load_pickle(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None

def save_cookies():
    cookies_dict = session1.cookies.get_dict()
    save_pickle(COOKIES_FILE, cookies_dict)

def load_cookies():
    d = load_pickle(COOKIES_FILE)
    if isinstance(d, dict) and d:
        session1.cookies.update(d)
        return True
    return False

def clear_cookies():
    session1.cookies.clear()
    if os.path.exists(COOKIES_FILE):
        try:
            os.remove(COOKIES_FILE)
            return True
        except:
            return False
    return True

def save_cookies_site3():
    cookies_dict = session3.cookies.get_dict()
    save_pickle(COOKIES_FILE_SITE3, cookies_dict)
    print("[Site3/Number_Panel] 💾 সেশন সেভ হয়েছে")

def load_cookies_site3():
    d = load_pickle(COOKIES_FILE_SITE3)
    if isinstance(d, dict) and d:
        session3.cookies.update(d)
        print("[Site3/Number_Panel] 📥 সেভ করা সেশন লোড হয়েছে")
        return True
    print("[Site3/Number_Panel] ⚠️ কোনো সেভ করা সেশন নেই")
    return False

def save_cookies_site4():
    cookies_dict = session4.cookies.get_dict()
    save_pickle(COOKIES_FILE_SITE4, cookies_dict)
    print("[Site4/Bolt] 💾 সেশন সেভ হয়েছে")

def load_cookies_site4():
    d = load_pickle(COOKIES_FILE_SITE4)
    if isinstance(d, dict) and d:
        session4.cookies.update(d)
        print("[Site4/Bolt] 📥 সেভ করা সেশন লোড হয়েছে")
        return True
    print("[Site4/Bolt] ⚠️ কোনো সেভ করা সেশন নেই")
    return False

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ]
    return random.choice(user_agents)

def login_attempt_group():
    
    global session1, is_logged_in_site1
    
    try:
        print(f"[GROUP] 🔄 লগইন পেজ আনা হচ্ছে...")
        resp = session1.get(LOGIN_PAGE_URL, timeout=HTTP_TIMEOUT)
        
        if resp.status_code != 200:
            print(f"[GROUP] ⚠️ লগইন পেজ খুলতে ব্যর্থ: {resp.status_code}")
            return False
        
        match = re.search(r'What is (\d+) \+ (\d+)', resp.text)
        if not match:
            print("[GROUP] ❌ খুঁজে পাওয়া যায়নি captcha লগইন পেজে")
            return False
        
        num1, num2 = int(match.group(1)), int(match.group(2))
        captcha_answer = num1 + num2
        print(f"[GROUP] 🧮 সমাধান captcha: {num1} + {num2} = {captcha_answer}")
        
        payload = {
            "username": USERNAME,
            "password": PASSWORD,
            "capt": str(captcha_answer)
        }
        
        headers = {
            "Content-Type": "application/x-www-fencoded",
            "Referer": LOGIN_PAGE_URL,
            "Origin": BASE_URL,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        
        print(f"[GROUP] 📤 লগইন অনুরোধ পাঠানো হচ্ছে: {USERNAME}")
        
        resp = session1.post(LOGIN_POST_URL, data=payload, headers=headers, timeout=HTTP_TIMEOUT, allow_redirects=True)
        
        print(f"[GROUP] 📊 রেসপন্স স্ট্যাটাস: {resp.status_code}")
        
        if ("dashboard" in resp.text.lower() or 
            "logout" in resp.text.lower() or 
            "agent" in resp.url.lower() or
            "/ints/agent" in resp.url or
            resp.url != LOGIN_PAGE_URL):
            print("[GROUP] ✅ লগইন সফল হয়েছে")
            is_logged_in_site1 = True
            save_cookies()
            
            print("[GROUP] 🔄 পেজ ভিজিট SMSCDRReports লগইনের পরে...")
            try:
                session1.get(BASE_URL + "/ints/agent/SMSCDRReports", timeout=HTTP_TIMEOUT)
                print("[GROUP] ✅ পেজ ভিজিট করা হয়েছে SMSCDRReports সফলভাবে")
                time.sleep(1)
            except Exception as e:
                print(f"[GROUP] ⚠️ পেজ ভিজিটে ত্রুটি SMSCDRReports: {e}")
            
            return True
        else:
            print("[GROUP] ❌ লগইন ব্যর্থ")
            if "incorrect" in resp.text.lower() or "invalid" in resp.text.lower():
                print("[GROUP] ⚠️ ইউজারনেম বা পাসওয়ার্ড ভুল")
            return False
            
    except requests.exceptions.Timeout:
        print(f"[GROUP] ⏱️ সংযোগের সময় শেষ")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"[GROUP] 🔌 সংযোগে ত্রুটি: {e}")
        return False
    except Exception as e:
        print(f"[GROUP] ❌ লগইনে ত্রুটি: {e}")
        return False

def login(max_retries=10):
    
    global session1, is_logged_in_site1
    print(f"🔐 GROUP: লগইন শুরু হচ্ছে...")
    
    for attempt in range(1, max_retries + 1):
        try:
            print(f"\n🔄 GROUP: চেষ্টা {attempt}/{max_retries}")
            
            if attempt > 1:
                print(f"🔄 GROUP: সেশন নবায়ন হচ্ছে...")
                session1 = create_session_group()
                time.sleep(2)
            
            if login_attempt_group():
                print(f"✅ GROUP: লগইন সফল হয়েছে চেষ্টা {attempt}")
                return True
            
            backoff_time = min(30, 5 * attempt)
            print(f"⏳ GROUP: অপেক্ষা {backoff_time}s পরের চেষ্টার আগে...")
            time.sleep(backoff_time)
            
        except Exception as e:
            print(f"❌ GROUP (চেষ্টা {attempt}): ত্রুটি - {str(e)}")
            time.sleep(5)
    
    print(f"❌ GROUP: লগইন ব্যর্থ হয়েছে {max_retries} চেষ্টার পর")
    return False

def check_login_valid():
    try:
        test_url = BASE_URL + "/ints/agent/res/data_smscdr.php?per-page=10"
        ajax_headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": BASE_URL + "/ints/agent/SMSCDRReports"
        }
        r = session1.get(test_url, headers=ajax_headers, timeout=15)
        if r.status_code == 200:
            if "login" in r.text.lower() or "sign in" in r.text.lower():
                return False
            if "direct script access not allowed" in r.text.lower():
                return False
            return True
        return False
    except Exception as e:
        return False

def test_bolt_type_login(site_key, account):
    username = account.get("username")
    password = account.get("password")
    
   
    if site_key == "MSI":
        session_obj = session6
        base_url = BASE_URL6
        login_page = LOGIN_PAGE_URL6
        login_post = LOGIN_POST_URL6
        timeout = HTTP_TIMEOUT6
    elif site_key == "proton SMS":
        session_obj = session7
        base_url = BASE_URL7
        login_page = LOGIN_PAGE_URL7
        login_post = LOGIN_POST_URL7
        timeout = HTTP_TIMEOUT7
    elif site_key == "IMS":
        session_obj = session8
        base_url = BASE_URL8
        login_page = LOGIN_PAGE_URL8
        login_post = LOGIN_POST_URL8
        timeout = HTTP_TIMEOUT8
    elif site_key == "Roxy SMS":
        try:
            scraper = cloudscraper.create_scraper()
            login_url = "http://www.roxysms.net/signin"
            payload = {"username": username, "password": password}
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "http://www.roxysms.net/Login"
            }
            resp = scraper.post(login_url, data=payload, headers=headers, timeout=20)
            if resp.status_code == 200 and ("success" in resp.text.lower() or "logout" in resp.text.lower()):
                print(f"[{site_key}] ({username}) ✅ লগইন সফল হয়েছে")
                return True
            else:
                print(f"[{site_key}] ({username}) ❌ লগইন ব্যর্থ")
                return False
        except Exception as e:
            print(f"[{site_key}] ({username}) ❌ লগইনে ত্রুটি: {e}")
            return False
    else:
        return False

    print(f"[{site_key}] ({username}) 🔐 লগইনের চেষ্টা (Bolt-type)...")
    
    try:
        session_obj.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,ar;q=0.8"
        })
        
        resp = session_obj.get(login_page, timeout=timeout)
        
        match = re.search(r'What is (\d+) \+ (\d+)', resp.text)
        if not match:
            print(f"[{site_key}] ({username}) ⚠️ খুঁজে পাওয়া যায়নি captcha")
            return False
        
        num1, num2 = int(match.group(1)), int(match.group(2))
        captcha_answer = num1 + num2
        
        crlf_match = re.search(r"name=['\"]crlf['\"].*?value=['\"]([^'\"]+)['\"]", resp.text)
        
        payload = {
            "username": username,
            "password": password,
            "capt": str(captcha_answer)
        }
        
        if crlf_match:
            payload["crlf"] = crlf_match.group(1)
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": login_page,
            "Origin": base_url
        }
        
        resp = session_obj.post(login_post, data=payload, headers=headers, timeout=timeout, allow_redirects=True)
        
        if ("dashboard" in resp.text.lower() or 
            "logout" in resp.text.lower() or 
            "agent" in resp.url.lower() or 
            "reports" in resp.url.lower()):
            print(f"[{site_key}] ({username}) ✅ লগইন সফল হয়েছে")
            return True
        else:
            print(f"[{site_key}] ({username}) ❌ লগইন ব্যর্থ")
            return False
            
    except Exception as e:
        print(f"[{site_key}] ({username}) ❌ লগইনে ত্রুটি: {e}")
        return False

def extract_sms(html_text, debug_mode=False):
    try:
        test_session = requests.Session()
        test_session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,ar;q=0.8"
        })
        
        resp = test_session.get(login_page_url, timeout=timeout)
        print(f"[{site_key}] 📄 স্ট্যাটাস GET: {resp.status_code}")
        
        match = re.search(r'What is (\d+) \+ (\d+)', resp.text)
        if not match:
            print(f"[{site_key}] ⚠️ খুঁজে পাওয়া যায়নি captcha পেজে")
            return False
        
        num1, num2 = int(match.group(1)), int(match.group(2))
        captcha_answer = num1 + num2
        print(f"[{site_key}] 🧮 সমাধান captcha: {num1} + {num2} = {captcha_answer}")
        
        crlf_match = re.search(r"name='crlf' value='([^']+)'", resp.text)
        
        payload = {
            "username": username,
            "password": password,
            "capt": str(captcha_answer)
        }
        
        if crlf_match:
            payload["crlf"] = crlf_match.group(1)
            print(f"[{site_key}] 🔑 বের করা crlf token")
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": login_page_url,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Origin": base_url
        }
        
        print(f"[{site_key}] 📤 লগইন অনুরোধ পাঠানো হচ্ছে: {username}")
        resp = test_session.post(login_post_url, data=payload, headers=headers, timeout=timeout, allow_redirects=True)
        
        print(f"[{site_key}] 📊 স্ট্যাটাস POST: {resp.status_code}")
        print(f"[{site_key}] 🔗 URL চূড়ান্ত: {resp.url}")
        
        if ("dashboard" in resp.text.lower() or 
            "logout" in resp.text.lower() or 
            "agent" in resp.url.lower() or 
            "reports" in resp.url.lower() or
            resp.url != login_page_url):
            print(f"[{site_key}] ✅ লগইন সফল হয়েছে")
            return True
        else:
            print(f"[{site_key}] ❌ লগইন ব্যর্থ")
            return False
            
    except Exception as e:
        print(f"[{site_key}] ❌ লগইনে ত্রুটি: {e}")
        return False

def test_site_login(chat_id, site_key, account_id=None):
    global is_logged_in_site2, is_logged_in_site3, is_logged_in_site4, is_logged_in_site5, USERNAME, PASSWORD, USERNAME2, PASSWORD2, USERNAME3, PASSWORD3, USERNAME4, PASSWORD4, USERNAME5, PASSWORD5
    
    site_name = SETTINGS[site_key]["name"]
    account = get_account_by_id(site_key, account_id) if account_id else get_site_accounts(site_key)[0]
    
    if not account:
        bot.send_message(chat_id, "❌ অ্যাকাউন্ট পাওয়া যায়নি!", parse_mode="HTML")
        return
    
    try:
        if site_key == "IMS":
            success, _ = login_site8(account)
            if success:
                bot.send_message(
                    chat_id,
                    f"✅ <b>লগইন সফল - {site_name}</b>\n\n"
                    f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                    f"🔓 লগইন সফল হয়েছে\n"
                    f"⏰ সময়: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    parse_mode="HTML"
                )
            else:
                bot.send_message(
                    chat_id,
                    f"❌ <b>লগইন ব্যর্থ - {site_name}</b>\n\n"
                    f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                    f"⚠️ তথ্য ঠিক আছে কিনা নিশ্চিত করুন (Username, Password, Captcha)",
                    parse_mode="HTML"
                )
            return

        if site_key == "GROUP":
            old_username, old_password = USERNAME, PASSWORD
            try:
                USERNAME = account.get("username")
                PASSWORD = account.get("password")
                
                result = login()
                
                if result:
                    SESSIONS[site_key] = {"logged_in": True, "time": datetime.now().isoformat()}
                    save_sessions(SESSIONS)
                    bot.send_message(
                        chat_id,
                        f"✅ <b>লগইন সফল - {site_name}</b>\n\n"
                        f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                        f"🔓 লগইন সফল হয়েছে\n"
                        f"⏰ সময়: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                        parse_mode="HTML"
                    )
                else:
                    bot.send_message(
                        chat_id,
                        f"❌ <b>লগইন ব্যর্থ - {site_name}</b>\n\n"
                        f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                        f"⚠️ ইউজারনেম ও পাসওয়ার্ড চেক করুন",
                        parse_mode="HTML"
                    )
            finally:
                USERNAME, PASSWORD = old_username, old_password
        
        elif site_key == "Roxy SMS":
            try:
                scraper = cloudscraper.create_scraper()
                login_url = "http://www.roxysms.net/signin"
                payload = {"username": account["username"], "password": account["password"]}
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Referer": "http://www.roxysms.net/Login"
                }
                resp = scraper.post(login_url, data=payload, headers=headers, timeout=20)
                if resp.status_code == 200 and ("success" in resp.text.lower() or "logout" in resp.text.lower()):
                    SESSIONS[site_key] = {"logged_in": True, "time": datetime.now().isoformat()}
                    save_sessions(SESSIONS)
                    bot.send_message(
                        chat_id,
                        f"✅ <b>লগইন সফল - {site_name}</b>\n\n"
                        f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                        f"🔓 লগইন সফল হয়েছে\n"
                        f"⏰ সময়: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                        parse_mode="HTML"
                    )
                else:
                    bot.send_message(
                        chat_id,
                        f"❌ <b>লগইন ব্যর্থ - {site_name}</b>\n\n"
                        f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                        f"⚠️ ইউজারনেম ও পাসওয়ার্ড চেক করুন",
                        parse_mode="HTML"
                    )
            except Exception as e:
                bot.send_message(chat_id, f"❌ লগইনে ত্রুটি: {e}")
            return
        
        elif site_key == "Fly sms":
            old_username, old_password = USERNAME2, PASSWORD2
            try:
                USERNAME2 = account.get("username")
                PASSWORD2 = account.get("password")
                
                is_logged_in_site2 = False
                result = login_site2()
                
                if result:
                    SESSIONS[site_key] = {"logged_in": True, "time": datetime.now().isoformat()}
                    save_sessions(SESSIONS)
                    bot.send_message(
                        chat_id,
                        f"✅ <b>লগইন সফল - {site_name}</b>\n\n"
                        f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                        f"🔓 লগইন সফল হয়েছে\n"
                        f"⏰ সময়: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                        parse_mode="HTML"
                    )
                else:
                    bot.send_message(
                        chat_id,
                        f"❌ <b>লগইন ব্যর্থ - {site_name}</b>\n\n"
                        f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                        f"⚠️ ইউজারনেম ও পাসওয়ার্ড চেক করুন",
                        parse_mode="HTML"
                    )
            finally:
                USERNAME2, PASSWORD2 = old_username, old_password
        
        elif site_key == "Number_Panel":
            old_username, old_password = USERNAME3, PASSWORD3
            try:
                USERNAME3 = account.get("username")
                PASSWORD3 = account.get("password")
                
                is_logged_in_site3 = False
                result = login_site3()
                
                if result:
                    SESSIONS[site_key] = {"logged_in": True, "time": datetime.now().isoformat()}
                    save_sessions(SESSIONS)
                    bot.send_message(
                        chat_id,
                        f"✅ <b>লগইন সফল - {site_name}</b>\n\n"
                        f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                        f"🔓 লগইন সফল হয়েছে\n"
                        f"⏰ সময়: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                        parse_mode="HTML"
                    )
                else:
                    bot.send_message(
                        chat_id,
                        f"❌ <b>লগইন ব্যর্থ - {site_name}</b>\n\n"
                        f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                        f"⚠️ ইউজারনেম ও পাসওয়ার্ড চেক করুন",
                        parse_mode="HTML"
                    )
            finally:
                USERNAME3, PASSWORD3 = old_username, old_password
        
        elif site_key == "Bolt":
            old_username, old_password = USERNAME4, PASSWORD4
            try:
                USERNAME4 = account.get("username")
                PASSWORD4 = account.get("password")
                
                is_logged_in_site4 = False
                result = login_site4()
                
                if result:
                    SESSIONS[site_key] = {"logged_in": True, "time": datetime.now().isoformat()}
                    save_sessions(SESSIONS)
                    bot.send_message(
                        chat_id,
                        f"✅ <b>লগইন সফল - {site_name}</b>\n\n"
                        f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                        f"🔓 লগইন সফল হয়েছে\n"
                        f"⏰ সময়: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                        parse_mode="HTML"
                    )
                else:
                    bot.send_message(
                        chat_id,
                        f"❌ <b>লগইন ব্যর্থ - {site_name}</b>\n\n"
                        f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                        f"⚠️ ইউজারনেম ও পাসওয়ার্ড চেক করুন",
                        parse_mode="HTML"
                    )
            finally:
                USERNAME4, PASSWORD4 = old_username, old_password
        
        elif site_key == "iVASMS":
            old_username, old_password = USERNAME5, PASSWORD5
            try:
                USERNAME5 = account.get("username")
                PASSWORD5 = account.get("password")
                
                is_logged_in_site5 = False
                result = login_site5()
                
                if result:
                    SESSIONS[site_key] = {"logged_in": True, "time": datetime.now().isoformat()}
                    save_sessions(SESSIONS)
                    bot.send_message(
                        chat_id,
                        f"✅ <b>লগইন সফল - {site_name}</b>\n\n"
                        f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                        f"🔓 লগইন সফল হয়েছে\n"
                        f"⏰ সময়: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                        parse_mode="HTML"
                    )
                else:
                    bot.send_message(
                        chat_id,
                        f"❌ <b>লগইন ব্যর্থ - {site_name}</b>\n\n"
                        f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                        f"⚠️ ইউজারনেম ও পাসওয়ার্ড চেক করুন",
                        parse_mode="HTML"
                    )
            finally:
                USERNAME5, PASSWORD5 = old_username, old_password
        
        elif site_key in ["MSI", "proton SMS", "IMS", "Roxy SMS"]:
            result = test_bolt_type_login(site_key, account)
            if result:
                SESSIONS[site_key] = {"logged_in": True, "time": datetime.now().isoformat()}
                save_sessions(SESSIONS)
                bot.send_message(
                    chat_id,
                    f"✅ <b>লগইন সফল - {site_name}</b>\n\n"
                    f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                    f"🔓 লগইন সফল হয়েছে\n"
                    f"⏰ সময়: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    parse_mode="HTML"
                )
            else:
                bot.send_message(
                    chat_id,
                    f"❌ <b>লগইন ব্যর্থ - {site_name}</b>\n\n"
                    f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                    f"⚠️ ইউজারনেম ও পাসওয়ার্ড চেক করুন",
                    parse_mode="HTML"
                )
    
    except Exception as e:
        bot.send_message(
            chat_id,
            f"❌ <b>লগইন টেস্টের সময় ত্রুটি - {site_name}</b>\n\n"
            f"⚠️ ত্রুটি: {str(e)}",
            parse_mode="HTML"
        )

def test_site_fetch(chat_id, site_key, account_id=None):
    global is_logged_in_site2, is_logged_in_site3, is_logged_in_site4, is_logged_in_site5, USERNAME, PASSWORD, USERNAME2, PASSWORD2, USERNAME3, PASSWORD3, USERNAME4, PASSWORD4, USERNAME5, PASSWORD5
    site_name = SETTINGS[site_key]["name"]
    account = get_account_by_id(site_key, account_id) if account_id else get_site_accounts(site_key)[0]
    
    if not account:
        bot.send_message(chat_id, "❌ অ্যাকাউন্ট পাওয়া যায়নি!", parse_mode="HTML")
        return
    
    try:
        if site_key == "GROUP":
            old_username, old_password = USERNAME, PASSWORD
            try:
                USERNAME = account.get("username")
                PASSWORD = account.get("password")
                
                if not check_login_valid():
                    print(f"[GROUP] সেশন বৈধ নয়: {account.get('username')}, লগইনের চেষ্টা চলছে...")
                    if not login():
                        bot.send_message(
                            chat_id,
                            f"❌ <b>লগইন ব্যর্থ - {site_name}</b>\n\n"
                            f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                            f"⚠️ কোড আনা টেস্ট করার আগে লগইন করতে হবে",
                            parse_mode="HTML"
                        )
                        return
                    time.sleep(2)
            
                sms_url = BASE_URL + AJAX_PATH
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "X-Requested-With": "XMLHttpRequest",
                    "Referer": BASE_URL + "/ints/agent/SMSCDRReports"
                }
                
                r = session1.get(sms_url, headers=headers, timeout=HTTP_TIMEOUT)
                
                if r.status_code == 200:
                    messages = extract_sms(r.text)
                    if messages:
                        last_msg = messages[0]
                        otp, decoded_text = extract_from_message(last_msg.get('raw', ''))
                        
                        bot.send_message(
                            chat_id,
                            f"✅ <b>কোড আনা সফল - {site_name}</b>\n\n"
                            f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                            f"📱 নম্বর: <code>{last_msg.get('source', 'N/A')}</code>\n"
                            f"📝 মেসেজ: {decoded_text[:100] if decoded_text else 'N/A'}...\n"
                            f"⏰ সময়: {last_msg.get('date', 'N/A')}",
                            parse_mode="HTML"
                        )
                    else:
                        bot.send_message(
                            chat_id,
                            f"⚠️ <b>কোনো মেসেজ নেই - {site_name}</b>\n\n"
                            f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>",
                            parse_mode="HTML"
                        )
                else:
                    bot.send_message(
                        chat_id,
                        f"❌ <b>ডাটা আনতে ত্রুটি - {site_name}</b>\n\n"
                        f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                        f"HTTP Status: {r.status_code}",
                        parse_mode="HTML"
                    )
            finally:
                USERNAME, PASSWORD = old_username, old_password
        
        elif site_key == "Fly sms":
            old_username, old_password = USERNAME2, PASSWORD2
            try:
                USERNAME2 = account.get("username")
                PASSWORD2 = account.get("password")
                
                if not is_logged_in_site2:
                    print(f"[Fly sms] লগইন করা নেই: {account.get('username')}, লগইনের চেষ্টা চলছে...")
                    if not login_site2():
                        bot.send_message(
                            chat_id,
                            f"❌ <b>লগইন ব্যর্থ - {site_name}</b>\n\n"
                            f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                            f"⚠️ কোড আনা টেস্ট করার আগে লগইন করতে হবে",
                            parse_mode="HTML"
                        )
                        return
                    time.sleep(2)
                
                url = build_ajax_url_site2()
                
                data = None
                max_retries = 5
                for attempt in range(1, max_retries + 1):
                    try:
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                            "Accept": "application/json, text/javascript, */*; q=0.01",
                            "X-Requested-With": "XMLHttpRequest",
                            "Referer": BASE_URL2 + "/ints/agent/SMSCDRReports"
                        }
                        r = session2.get(url, timeout=HTTP_TIMEOUT2, headers=headers)
                        
                        if r.status_code in [502, 503, 504]:
                            print(f"[Fly sms] ⚠️ সার্ভার ব্যস্ত ({r.status_code}) - চেষ্টা {attempt}/{max_retries}")
                            if attempt < max_retries:
                                time.sleep(15 * attempt)
                                continue
                            else:
                                bot.send_message(
                                    chat_id,
                                    f"⚠️ <b>সার্ভার ব্যস্ত - {site_name}</b>\n\n"
                                    f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                                    f"⏳ ত্রুটি: {r.status_code} - সার্ভারে চাপ বেশি\n"
                                    f"💡 এক মিনিট পরে আবার চেষ্টা করুন",
                                    parse_mode="HTML"
                                )
                                return
                        
                        if r.status_code == 200:
                            data = r.json()
                            break
                        else:
                            if attempt < max_retries:
                                time.sleep(10)
                                continue
                    except Exception as e:
                        print(f"[Fly sms] ⚠️ চেষ্টায় ত্রুটি {attempt}: {e}")
                        if attempt < max_retries:
                            time.sleep(10)
                            continue
                
                if data:
                    messages = data.get("data", [])
                    if messages:
                        last_msg = messages[0]
                        sms_text = last_msg[5] if len(last_msg) > 5 else "N/A"
                        number = last_msg[2] if len(last_msg) > 2 else "N/A"
                        date_str = last_msg[0] if len(last_msg) > 0 else "N/A"
                        
                        otp, decoded_text = extract_from_message(sms_text)
                        
                        bot.send_message(
                            chat_id,
                            f"✅ <b>কোড আনা সফল - {site_name}</b>\n\n"
                            f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                            f"📱 নম্বর: <code>{number}</code>\n"
                            f"📝 মেসেজ: {decoded_text[:100] if decoded_text else sms_text[:100]}...\n"
                            f"⏰ সময়: {date_str}",
                            parse_mode="HTML"
                        )
                    else:
                        bot.send_message(
                            chat_id,
                            f"⚠️ <b>কোনো মেসেজ নেই - {site_name}</b>\n\n"
                            f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>",
                            parse_mode="HTML"
                        )
                else:
                    bot.send_message(
                        chat_id,
                        f"❌ <b>ডাটা আনতে ত্রুটি - {site_name}</b>\n\n"
                        f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                        f"⚠️ সার্ভারে সংযোগ ব্যর্থ",
                        parse_mode="HTML"
                    )
            except Exception as e:
                bot.send_message(
                    chat_id,
                    f"❌ <b>ডাটা প্রসেসে ত্রুটি - {site_name}</b>\n\n"
                    f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                    f"⚠️ বিবরণ: {str(e)}",
                    parse_mode="HTML"
                )
            finally:
                USERNAME2, PASSWORD2 = old_username, old_password
        
        elif site_key == "Number_Panel":
            old_username, old_password = USERNAME3, PASSWORD3
            try:
                USERNAME3 = account.get("username")
                PASSWORD3 = account.get("password")
                api_token = account.get("api_token") or SETTINGS[site_key].get("api_token")
                
                if api_token:
                    api_url = "http://147.135.212.197/crapi/st/viewstats"
                    r = session3.get(api_url, params={"token": api_token, "records": 10}, timeout=HTTP_TIMEOUT3)
                    if r.status_code == 200:
                        try:
                            data = r.json()
                            if isinstance(data, list) and data:
                                last_msg = data[0]
                                sms_text = last_msg[2]
                                number = last_msg[1]
                                date_str = last_msg[3]
                                
                                otp, decoded_text = extract_from_message(sms_text)
                                
                                bot.send_message(
                                    chat_id,
                                    f"✅ <b>কোড আনা সফল - {site_name} (API)</b>\n\n"
                                    f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                                    f"📱 নম্বর: <code>{number}</code>\n"
                                    f"📝 মেসেজ: {decoded_text[:100] if decoded_text else sms_text[:100]}...\n"
                                    
                                    f"⏰ সময়: {date_str}",
                                    parse_mode="HTML"
                                )
                                return
                        except Exception as e:
                            print(f"API parse error: {e}")

                if not is_logged_in_site3:
                    print(f"[Number_Panel] লগইন করা নেই: {account.get('username')}, লগইনের চেষ্টা চলছে...")
                    if not login_site3():
                        bot.send_message(
                            chat_id,
                            f"❌ <b>লগইন ব্যর্থ - {site_name}</b>\n\n"
                            f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                            f"⚠️ কোড আনা টেস্ট করার আগে লগইন করতে হবে",
                            parse_mode="HTML"
                        )
                        return
                    time.sleep(2)
                
                url = BASE_URL3 + AJAX_PATH3
                params = {
                    "draw": 1,
                    "start": 0,
                    "length": 10
                }
                
                r = session3.get(url, params=params, timeout=HTTP_TIMEOUT3)
                
                if r.status_code == 200:
                    try:
                        data = r.json()
                        messages = data.get("data", []) or data.get("aaData", [])
                        if messages:
                            last_msg = messages[0]
                            sms_text = last_msg[IDX_SMS_SITE3] if len(last_msg) > IDX_SMS_SITE3 else "N/A"
                            number = last_msg[IDX_NUMBER_SITE3] if len(last_msg) > IDX_NUMBER_SITE3 else "N/A"
                            date_str = last_msg[IDX_DATE_SITE3] if len(last_msg) > IDX_DATE_SITE3 else "N/A"
                            
                            otp, decoded_text = extract_from_message(sms_text)
                            
                            bot.send_message(
                                chat_id,
                                f"✅ <b>কোড আনা সফল - {site_name}</b>\n\n"
                                f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                                f"📱 নম্বর: <code>{number}</code>\n"
                                f"📝 মেসেজ: {decoded_text[:100] if decoded_text else sms_text[:100]}...\n"
                                f"⏰ সময়: {date_str}",
                                parse_mode="HTML"
                            )
                        else:
                            bot.send_message(
                                chat_id,
                                f"⚠️ <b>কোনো মেসেজ নেই - {site_name}</b>\n\n"
                                f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>",
                                parse_mode="HTML"
                            )
                    except Exception as e:
                        bot.send_message(
                            chat_id,
                            f"❌ <b>ডাটা প্রসেসে ত্রুটি - {site_name}</b>\n\n"
                            f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                            f"⚠️ বিবরণ: {str(e)}",
                            parse_mode="HTML"
                        )
                else:
                    bot.send_message(
                        chat_id,
                        f"❌ <b>ডাটা আনতে ত্রুটি - {site_name}</b>\n\n"
                        f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                        f"HTTP Status: {r.status_code}",
                        parse_mode="HTML"
                    )
            finally:
                USERNAME3, PASSWORD3 = old_username, old_password
        
        elif site_key == "Bolt":
            bot.send_message(
                chat_id,
                f"⚠️ <b>কোড আনা টেস্ট এখন সমর্থিত নয় - {site_name}</b>\n\n"
                f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                f"📝 অ্যাকাউন্ট যাচাই করতে লগইন টেস্ট ব্যবহার করতে পারেন",
                parse_mode="HTML"
            )
        
        elif site_key == "iVASMS":
            old_username, old_password = USERNAME5, PASSWORD5
            try:
                USERNAME5 = account.get("username")
                PASSWORD5 = account.get("password")
                
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                
                test_session = requests.Session()
                test_session.verify = False
                test_session.headers.update({
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Connection": "keep-alive"
                })
                
                resp = test_session.get(LOGIN_PAGE_URL5, timeout=HTTP_TIMEOUT5)
                soup = BeautifulSoup(resp.text, 'html.parser')
                csrf_input = soup.find('input', {'name': '_token'})
                if not csrf_input:
                    bot.send_message(chat_id, f"❌ <b>সংযোগ ব্যর্থ - {site_name}</b>\n\n⚠️ খুঁজে পাওয়া যায়নি CSRF token", parse_mode="HTML")
                    return
                
                csrf = csrf_input.get('value')
                payload = {'_token': csrf, 'email': USERNAME5, 'password': PASSWORD5}
                headers = {"Content-Type": "application/x-www-form-urlencoded", "Referer": LOGIN_PAGE_URL5}
                
                resp = test_session.post(LOGIN_POST_URL5, data=payload, headers=headers, timeout=HTTP_TIMEOUT5, allow_redirects=True)
                
                if 'portal' not in resp.url and 'login' in resp.url:
                    bot.send_message(chat_id, f"❌ <b>লগইন ব্যর্থ - {site_name}</b>\n\n👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>", parse_mode="HTML")
                    return
                
                soup = BeautifulSoup(resp.text, 'html.parser')
                csrf_input = soup.find('input', {'name': '_token'})
                if csrf_input:
                    csrf = csrf_input.get('value')
                
                today = date.today()
                from_date = (today - timedelta(days=7)).strftime("%d/%m/%Y")
                to_date = today.strftime("%d/%m/%Y")
                
                payload = {'from': from_date, 'to': to_date, '_token': csrf}
                headers = {'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Referer': SMS_RECEIVED_URL5}
                
                resp = test_session.post(GET_SMS_URL5, data=payload, headers=headers, timeout=HTTP_TIMEOUT5)
                
                if resp.status_code != 200:
                    bot.send_message(chat_id, f"❌ <b>ডাটা আনতে ত্রুটি - {site_name}</b>\n\nHTTP Status: {resp.status_code}", parse_mode="HTML")
                    return
                
                soup = BeautifulSoup(resp.text, 'html.parser')
                items = soup.select("div.item div.card.card-body")
                ranges = []
                for item in items:
                    onclick = item.get('onclick', '')
                    match = re.search(r"getDetials\s*\(\s*['\"]([^'\"]+)['\"]\s*\)", str(onclick) if onclick else "")
                    if match:
                        ranges.append(match.group(1))
                
                if not ranges:
                    bot.send_message(chat_id, f"⚠️ <b>কোনো মেসেজ নেই - {site_name}</b>\n\n👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>", parse_mode="HTML")
                    return
                
                first_range = ranges[0]
                start_datetime = f"{today.strftime('%Y-%m-%d')} 00:00:00"
                end_datetime = f"{today.strftime('%Y-%m-%d')} 23:59:59"
                
                payload = {'_token': csrf, 'start': start_datetime, 'end': end_datetime, 'range': first_range}
                resp = test_session.post(GET_SMS_NUMBER_URL5, data=payload, headers=headers, timeout=HTTP_TIMEOUT5)
                
                numbers = []
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    for item in soup.select("[onclick]"):
                        onclick = item.get('onclick', '')
                        phone_match = re.search(r"getNumber[^\(]*\(['\"]([^'\"]+)['\"]", str(onclick) if onclick else "")
                        if phone_match:
                            phone = phone_match.group(1)
                            if phone and len(phone) > 5:
                                numbers.append(phone)
                    if not numbers:
                        all_numbers = re.findall(r'["\']?(\d{10,15})["\']?', resp.text)
                        numbers.extend(all_numbers[:10])
                
                if not numbers:
                    bot.send_message(chat_id, f"⚠️ <b>কোনো নম্বর নেই - {site_name}</b>\n\n👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\nRange: {first_range}", parse_mode="HTML")
                    return
                
                first_phone = numbers[0]
                payload = {'_token': csrf, 'start': start_datetime, 'end': end_datetime, 'Number': first_phone, 'Range': first_range}
                resp = test_session.post(GET_SMS_MESSAGE_URL5, data=payload, headers=headers, timeout=HTTP_TIMEOUT5)
                
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    message = None
                    for selector in [".col-9.col-sm-6 p", ".col-sm-6 p"]:
                        el = soup.select_one(selector)
                        if el:
                            message = el.text.strip()
                            break
                    if not message:
                        for p in soup.find_all('p'):
                            text = p.text.strip()
                            if len(text) > 15:
                                message = text
                                break
                    
                    if message:
                        otp, decoded_text = extract_from_message(message)
                        bot.send_message(
                            chat_id,
                            f"✅ <b>কোড আনা সফল - {site_name}</b>\n\n"
                            f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                            f"📱 নম্বর: <code>{first_phone}</code>\n"
                            f"📝 মেসেজ: {(decoded_text[:100] if decoded_text else message[:100])}...\n"
                            
                            f"📊 Ranges: {len(ranges)} | Numbers: {len(numbers)}",
                            parse_mode="HTML"
                        )
                    else:
                        bot.send_message(chat_id, f"⚠️ <b>কোনো মেসেজ নেই - {site_name}</b>\n\n📱 নম্বর: {first_phone}", parse_mode="HTML")
                else:
                    bot.send_message(chat_id, f"❌ <b>মেসেজ আনতে ত্রুটি - {site_name}</b>\n\nHTTP Status: {resp.status_code}", parse_mode="HTML")
                    
            except Exception as e:
                bot.send_message(chat_id, f"❌ <b>ত্রুটি - {site_name}</b>\n\n⚠️ {str(e)}", parse_mode="HTML")
            finally:
                USERNAME5, PASSWORD5 = old_username, old_password
        
        elif site_key in ["MSI", "proton SMS", "IMS", "Roxy SMS"]:
            session_obj = session6 if site_key == "MSI" else (session7 if site_key == "proton SMS" else (session8 if site_key == "IMS" else session9))
            base_url = BASE_URL6 if site_key == "MSI" else (BASE_URL7 if site_key == "proton SMS" else (BASE_URL8 if site_key == "IMS" else BASE_URL9))
            ajax_path = AJAX_PATH6 if site_key == "MSI" else (AJAX_PATH7 if site_key == "proton SMS" else (AJAX_PATH8 if site_key == "IMS" else AJAX_PATH9))
            timeout = HTTP_TIMEOUT6 if site_key == "MSI" else (HTTP_TIMEOUT7 if site_key == "proton SMS" else (HTTP_TIMEOUT8 if site_key == "IMS" else HTTP_TIMEOUT9))
            
            result = test_bolt_type_login(site_key, account)
            if not result:
                bot.send_message(
                    chat_id,
                    f"❌ <b>লগইন ব্যর্থ - {site_name}</b>\n\n"
                    f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                    f"⚠️ কোড আনা টেস্ট করার আগে লগইন করতে হবে",
                    parse_mode="HTML"
                )
                return
            
            time.sleep(2)
            url = base_url + ajax_path
            params = {
                "draw": 1,
                "start": 0,
                "length": 10
            }
            
            try:
                
                for attempt in range(3):
                    try:
                        r = session_obj.get(url, params=params, timeout=timeout)
                        break
                    except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError) as e:
                        if attempt == 2: raise
                        time.sleep(2)
                
                if r.status_code == 200:
                    try:
                        data = r.json()
                        messages = data.get("data", [])
                        if messages:
                            last_msg = messages[0]
                            sms_text = last_msg[5] if len(last_msg) > 5 else "N/A"
                            number = last_msg[2] if len(last_msg) > 2 else "N/A"
                            date_str = last_msg[0] if len(last_msg) > 0 else "N/A"
                            
                            otp, decoded_text = extract_from_message(sms_text)
                            
                            bot.send_message(
                                chat_id,
                                f"✅ <b>কোড আনা সফল - {site_name}</b>\n\n"
                                f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                                f"📱 নম্বর: <code>{number}</code>\n"
                                f"📝 মেসেজ: {decoded_text[:100] if decoded_text else sms_text[:100]}...\n"
                                
                                f"⏰ সময়: {date_str}",
                                parse_mode="HTML"
                            )
                        else:
                            bot.send_message(
                                chat_id,
                                f"⚠️ <b>কোনো মেসেজ নেই - {site_name}</b>\n\n"
                                f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>",
                                parse_mode="HTML"
                            )
                    except Exception as e:
                        bot.send_message(
                            chat_id,
                            f"❌ <b>ডাটা প্রসেসে ত্রুটি - {site_name}</b>\n\n"
                            f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                            f"⚠️ বিবরণ: {str(e)}",
                            parse_mode="HTML"
                        )
                else:
                    bot.send_message(
                        chat_id,
                        f"❌ <b>ডাটা আনতে ত্রুটি - {site_name}</b>\n\n"
                        f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                        f"HTTP Status: {r.status_code}",
                        parse_mode="HTML"
                    )
            except Exception as e:
                bot.send_message(
                    chat_id,
                    f"❌ <b>সংযোগে ত্রুটি - {site_name}</b>\n\n"
                    f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n"
                    f"⚠️ বিবরণ: {str(e)}",
                    parse_mode="HTML"
                )
    
    except Exception as e:
        bot.send_message(
            chat_id,
            f"❌ <b>কোড আনা টেস্টের সময় ত্রুটি - {site_name}</b>\n\n"
            f"⚠️ ত্রুটি: {str(e)}",
            parse_mode="HTML"
        )

def extract_sms(html_text, debug_mode=False):
    soup = BeautifulSoup(html_text, "html.parser")
    messages = []
    
    table = soup.find("table", class_="table")
    if not table:
        all_tables = soup.find_all("table")
        if all_tables:
            table = all_tables[0]
        else:
            return []
        
    tbody = table.find("tbody")
    if not tbody:
        rows = table.find_all("tr")
    else:
        rows = tbody.find_all("tr")
    
    row_count = 0
    for row in rows:
        tds = row.find_all("td")
        if not tds:
            continue
        
        row_count += 1
        cols = [td.get_text(separator=" ", strip=True) for td in tds]
        
        if debug_mode and row_count <= 3:
            print(f"  সারি {row_count}: {len(cols)} কলাম - {cols[:8] if len(cols) > 7 else cols}")
        
        if not cols or len(cols) < 5:
            continue
        
        msg = {
            "date": cols[0] if len(cols) > 0 else "",
            "ref": cols[1] if len(cols) > 1 else "",
            "source": cols[2] if len(cols) > 2 else "",
            "client": cols[3] if len(cols) > 3 else "",
            "destination": cols[4] if len(cols) > 4 else "",
            "raw": cols[5] if len(cols) > 5 else (cols[4] if len(cols) > 4 else "")
        }
        
        if msg["date"] and msg["raw"] and len(msg["raw"]) > 3:
            messages.append(msg)
    
    return messages

def normalize_otp_from_text(text):
    if not text: 
        return None
    
    candidates = []
    
    telegram_pattern = r'(?:telegram|تيليجرام|تلجرام)\s*(?:code|كود)?\s*[:\s]*(\d{4,6})'
    match = re.search(telegram_pattern, text, re.IGNORECASE)
    if match:
        digits = match.group(1)
        candidates.append({
            'otp': digits,
            'position': match.start(),
            'confidence': 100
        })
    
    instagram_pattern = r'(\d{3})\s+(\d{3})\s+is\s+your\s+Instagram\s+code'
    match = re.search(instagram_pattern, text, re.IGNORECASE)
    if match:
        digits = match.group(1) + match.group(2)
        candidates.append({
            'otp': f"{digits[:3]} {digits[3:]}",
            'position': match.start(),
            'confidence': 99
        })
    
    code_keyword_pattern = r'(?:code|كود|رمز|verification|تحقق)[:\s]*(\d{4,8})'
    for match in re.finditer(code_keyword_pattern, text, re.IGNORECASE):
        digits = match.group(1)
        if 4 <= len(digits) <= 8:
            candidates.append({
                'otp': digits,
                'position': match.start(),
                'confidence': 95
            })
    
    spaced_triple_pattern = r'(\d{3})\s+(\d{3})'
    for match in re.finditer(spaced_triple_pattern, text):
        digits = match.group(1) + match.group(2)
        if len(digits) == 6:
            candidates.append({
                'otp': f"{digits[:3]} {digits[3:]}",
                'position': match.start(),
                'confidence': 90
            })
    
    high_confidence_pattern = r'(\d)\s+(\d)\s+(\d)\s*-\s*(\d)\s+(\d)\s+(\d)'
    for match in re.finditer(high_confidence_pattern, text):
        digits = re.sub(r'\D', '', match.group(0))
        if len(digits) == 6:
            candidates.append({
                'otp': f"{digits[:3]} {digits[3:]}",
                'position': match.start(),
                'confidence': 85
            })
    
    spaced_digits_pattern = r'(\d)\s+(\d)\s+(\d)\s+(\d)\s+(\d)\s+(\d)'
    for match in re.finditer(spaced_digits_pattern, text):
        digits = re.sub(r'\D', '', match.group(0))
        if len(digits) == 6:
            candidates.append({
                'otp': f"{digits[:3]} {digits[3:]}",
                'position': match.start(),
                'confidence': 80
            })
    
    hyphen_pattern = r'(\d{3})\s*-\s*(\d{3})'
    for match in re.finditer(hyphen_pattern, text):
        digits = re.sub(r'\D', '', match.group(0))
        if len(digits) == 6:
            candidates.append({
                'otp': f"{digits[:3]}-{digits[3:]}",
                'position': match.start(),
                'confidence': 98
            })
    
    
    rtl_whatsapp_pattern = r'[\u200e\u200f\u202a-\u202e]?(\d{3})\s*-\s*(\d{3})'
    for match in re.finditer(rtl_whatsapp_pattern, text):
        digits = match.group(1) + match.group(2)
        if len(digits) == 6:
            candidates.append({
                'otp': f"{match.group(1)}-{match.group(2)}",
                'position': match.start(),
                'confidence': 110
            })

    six_digits_pattern = r'\b\d{6}\b'
    for match in re.finditer(six_digits_pattern, text):
        digits = match.group(0)
        candidates.append({
            'otp': f"{digits[:3]} {digits[3:]}",
            'position': match.start(),
            'confidence': 70
        })
    
    five_digits_pattern = r'\b\d{5}\b'
    for match in re.finditer(five_digits_pattern, text):
        digits = match.group(0)
        candidates.append({
            'otp': digits,
            'position': match.start(),
            'confidence': 65
        })
    
    four_digits_pattern = r'\b\d{4}\b'
    for match in re.finditer(four_digits_pattern, text):
        digits = match.group(0)
        candidates.append({
            'otp': digits,
            'position': match.start(),
            'confidence': 60
        })
    
    if candidates:
        candidates.sort(key=lambda x: (-x['confidence'], x['position']))
        return candidates[0]['otp']
    
    all_digits = re.findall(r'\d+', text)
    for digit_group in reversed(all_digits):
        if len(digit_group) >= 4:
            return digit_group
    
    return None

def extract_from_message(raw_text):
    if not raw_text: 
        return None, None
    
    decoded_text = try_decode(raw_text)
    text = html.unescape(decoded_text)
    otp = normalize_otp_from_text(text)
    
    return otp, text

def clean_number(num_str: str) -> str:
    if num_str is None:
        return ""
    if isinstance(num_str, (int, float)):
        return str(int(num_str))
    return re.sub(r'\D', '', str(num_str))

IDX_DATE_SITE2 = 0
IDX_NUMBER_SITE2 = 2
IDX_SMS_SITE2 = 5

def retry_request_site2(func, max_retries=5, retry_delay=10):
    attempt = 0
    last_error = None
    while attempt < max_retries:
        attempt += 1
        try:
            return func()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            last_error = e
            backoff = min(60, retry_delay * attempt)
            print(f"⚠️ [Fly sms] চেষ্টা {attempt}/{max_retries} ব্যর্থ হয়েছে: {type(e).__name__}")
            print(f"⏳ [Fly sms] অপেক্ষা {backoff} সেকেন্ড, আবার চেষ্টার আগে...")
            time.sleep(backoff)
        except requests.exceptions.HTTPError as e:
            last_error = e
            status_code = e.response.status_code if e.response else 0
            if status_code in [502, 503, 504]:
                backoff = min(60, 10 + (attempt * 5))
                print(f"⚠️ [Fly sms] ত্রুটি {status_code} - চেষ্টা {attempt}/{max_retries}")
                print(f"⏳ [Fly sms] সার্ভার ব্যস্ত, অপেক্ষা {backoff} সেকেন্ড...")
                time.sleep(backoff)
            elif status_code == 404:
                backoff = min(60, 15 + (attempt * 5))
                print(f"⚠️ [Fly sms] ত্রুটি 404 - চেষ্টা {attempt}/{max_retries}")
                print(f"⏳ [Fly sms] অপেক্ষা {backoff} সেকেন্ড...")
                time.sleep(backoff)
            else:
                print(f"❌ [Fly sms] ত্রুটি HTTP {status_code}: {e}")
                raise
        except Exception as e:
            error_str = str(e)
            if "503" in error_str or "502" in error_str or "504" in error_str or "Service" in error_str:
                last_error = e
                backoff = min(60, 10 + (attempt * 5))
                print(f"⚠️ [Fly sms] সার্ভার ত্রুটি - চেষ্টা {attempt}/{max_retries}: {error_str[:100]}")
                print(f"⏳ [Fly sms] অপেক্ষা {backoff} সেকেন্ড...")
                time.sleep(backoff)
            elif "404" in error_str or "Not Found" in error_str:
                last_error = e
                backoff = min(60, 15 + (attempt * 5))
                print(f"⚠️ [Fly sms] ত্রুটি 404 - চেষ্টা {attempt}/{max_retries}")
                print(f"⏳ [Fly sms] অপেক্ষা {backoff} সেকেন্ড...")
                time.sleep(backoff)
            else:
                print(f"❌ [Fly sms] অপ্রত্যাশিত ত্রুটি: {e}")
                raise
    
    print(f"❌ [Fly sms] সব চেষ্টা শেষ ({max_retries})")
    if last_error:
        raise last_error
    raise Exception("Max retries exceeded")

def try_decode_site2(raw):
    if raw is None:
        return ""
    
    if isinstance(raw, str):
        cleaned = raw.replace('\x00', '').strip()
        if cleaned:
            return cleaned
        return ""
    
    if isinstance(raw, bytes):
        b = raw
    else:
        text_str = str(raw)
        cleaned = text_str.replace('\x00', '').strip()
        if cleaned:
            return cleaned
        return ""
    
    for enc in ("utf-8", "cp1256", "windows-1256", "iso-8859-6", "utf-16-be", "utf-16-le", "latin-1"):
        try:
            s = b.decode(enc, errors='ignore')
            cleaned = s.replace('\x00', '').strip()
            if cleaned:
                return cleaned
        except:
            continue
    
    return b.decode('utf-8', errors='replace').replace('\x00', '').strip()

def clean_html_site2(text):
    if text is None or text == "":
        return ""
    try:
        text = str(text) if not isinstance(text, str) else text
        text = re.sub(r'<[^>]+>', '', text)
        text = html.unescape(text)
        text = text.replace('\x00', '').strip()
        return text
    except Exception as e:
        print(f"[Site2] ⚠️ ত্রুটি: clean_html: {e} - মান: {repr(text)}")
        try:
            return str(text) if text else ""
        except:
            return ""


def solve_captcha_timesms(html_content):
    match = re.search(r'(\d+)\s*([+\-*/])\s*(\d+)\s*=?\s*\?', html_content)
    if match:
        n1, op, n2 = int(match.group(1)), match.group(2), int(match.group(3))
        if op == '+': return str(n1 + n2)
        elif op == '-': return str(n1 - n2)
        elif op == '*': return str(n1 * n2)
        elif op == '/': return str(n1 // n2) if n2 else '0'
    return None

def login_site10(account=None):
    global is_logged_in_site10, session10
    print("[TimeSMS] 🔄 লগইনের চেষ্টা চলছে...")
    
    site_key = "TimeSMS"
    if account:
        user = account.get("username")
        pw = account.get("password")
        sess = requests.Session()
        sess.headers.update(session10.headers)
    else:
        user = USERNAME10
        pw = PASSWORD10
        sess = session10

    login_url = SETTINGS[site_key]["login_page_url"]
    submit_url = SETTINGS[site_key]["login_post_url"]

    try:
        resp = sess.get(login_url, timeout=15)
        captcha = solve_captcha_timesms(resp.text)
        if not captcha:
            print("[TimeSMS] ❌ ক্যাপচা সমাধান ব্যর্থ")
            return False
        
        data = {'username': user, 'password': pw, 'capt': captcha}
        login_resp = sess.post(submit_url, data=data, headers={'Referer': login_url}, timeout=15, allow_redirects=True)
        
        if 'login' not in str(login_resp.url).lower():
            if not account: is_logged_in_site10 = True
            print("[TimeSMS] ✅ লগইন সফল হয়েছে")
            return sess if account else True
    except Exception as e:
        print(f"[TimeSMS] ❌ লগইনে ত্রুটি: {e}")
    return False

def login_site2():
    global is_logged_in_site2
    print("[Fly sms] 🔄 লগইনের চেষ্টা চলছে...")
    
    session2.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive"
    })
    
    def do_login():
        try:
            resp = session2.get(LOGIN_PAGE_URL2, timeout=HTTP_TIMEOUT2)
            
            if resp.status_code in [502, 503, 504]:
                print(f"[Fly sms] ⚠️ সার্ভার ব্যস্ত ({resp.status_code})")
                raise requests.exceptions.HTTPError(f"{resp.status_code} Server Error", response=resp)
            
            match = re.search(r'What is (\d+) \+ (\d+)', resp.text)
            if not match:
                print("[Fly sms] ⚠️ খুঁজে পাওয়া যায়নি captcha লগইন পেজে")
                if resp.status_code != 200:
                    raise Exception(f"HTTP {resp.status_code}")
                return False
            
            num1, num2 = int(match.group(1)), int(match.group(2))
            captcha_answer = num1 + num2
            print(f"[Fly sms] 🧮 সমাধান captcha: {num1} + {num2} = {captcha_answer}")
            
            payload = {
                "username": USERNAME2,
                "password": PASSWORD2,
                "capt": str(captcha_answer)
            }
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": LOGIN_PAGE_URL2,
                "Origin": BASE_URL2,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            }
            
            print(f"[Fly sms] 📤 লগইন অনুরোধ পাঠানো হচ্ছে: {USERNAME2}")
            
            resp = session2.post(LOGIN_POST_URL2, data=payload, headers=headers, timeout=HTTP_TIMEOUT2, allow_redirects=True)
            
            print(f"[Fly sms] 📊 রেসপন্স স্ট্যাটাস: {resp.status_code}")
            
            if resp.status_code in [502, 503, 504]:
                print(f"[Fly sms] ⚠️ সার্ভার ব্যস্ত ({resp.status_code})")
                raise requests.exceptions.HTTPError(f"{resp.status_code} Server Error", response=resp)
            
            if ("dashboard" in resp.text.lower() or 
                "logout" in resp.text.lower() or 
                "agent" in resp.url.lower() or
                "/ints/agent" in resp.url or
                resp.url != LOGIN_PAGE_URL2):
                print("[Fly sms] ✅ লগইন সফল হয়েছে")
                is_logged_in_site2 = True
                
                try:
                    session2.get(BASE_URL2 + "/ints/agent/SMSCDRReports", timeout=HTTP_TIMEOUT2)
                    print("[Fly sms] ✅ পেজ ভিজিট করা হয়েছে SMSCDRReports")
                except:
                    pass
                
                return True
            else:
                print("[Fly sms] ❌ লগইন ব্যর্থ")
                if "incorrect" in resp.text.lower() or "invalid" in resp.text.lower():
                    print("[Fly sms] ⚠️ ইউজারনেম বা পাসওয়ার্ড ভুল")
                return False
                
        except requests.exceptions.HTTPError as e:
            print(f"[Fly sms] ⚠️ ত্রুটি HTTP: {e}")
            raise
        except Exception as e:
            print(f"[Fly sms] ❌ লগইনে ত্রুটি: {e}")
            raise
    
    try:
        return retry_request_site2(do_login, max_retries=5, retry_delay=15)
    except:
        return False

def build_ajax_url_site2(wide_range=False):
    if wide_range:
        start_date = date.today() - timedelta(days=5)
        end_date = date.today() + timedelta(days=1)
    else:
        start_date = date.today()
        end_date = date.today() + timedelta(days=1)
    
    fdate1 = f"{start_date.strftime('%Y-%m-%d')} 00:00:00"
    fdate2 = f"{end_date.strftime('%Y-%m-%d')} 23:59:59"
    q = (
        f"fdate1={quote_plus(fdate1)}&fdate2={quote_plus(fdate2)}&frange=&fclient=&fnum=&fcli=&fgdate=&fgmonth=&fgrange="
        f"&fgclient=&fgnumber=&fgcli=&fg=0&sEcho=1&iColumns=9&sColumns=%2C%2C%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=50000"
        f"&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&mDataProp_4=4&mDataProp_5=5&mDataProp_6=6&mDataProp_7=7&mDataProp_8=8"
        f"&sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=desc&iSortingCols=1&_={int(time.time()*1000)}"
    )
    return BASE_URL2 + AJAX_PATH2 + "?" + q

def fetch_ajax_json_site2(url):
    global is_logged_in_site2
    
    def do_fetch():
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": BASE_URL2 + "/ints/agent/SMSCDRReports"
        }
        r = session2.get(url, timeout=HTTP_TIMEOUT2, headers=headers)
        
        if r.status_code == 403:
            raise Exception("Session expired")
        
        if r.status_code in [502, 503, 504]:
            raise requests.exceptions.HTTPError(f"{r.status_code} Server Error", response=r)
        
        if r.status_code == 401:
            raise Exception("Session expired")
        
        r.raise_for_status()
        
        try:
            data = r.json()
            if not isinstance(data, (dict, list)):
                raise Exception("Invalid JSON response")
            return data
        except (json.JSONDecodeError, ValueError) as e:
            if "login" in r.text.lower() and r.url and "login" in r.url.lower():
                raise Exception("Session expired")
            raise
    
    try:
        return retry_request_site2(do_fetch, max_retries=5, retry_delay=10)
    except Exception as e:
        error_str = str(e)
        if "Session expired" in error_str:
            print("[Fly sms] ⚠️ সেশনের মেয়াদ শেষ। আবার লগইন হচ্ছে...")
            is_logged_in_site2 = False
            if login_site2():
                is_logged_in_site2 = True
                try:
                    return retry_request_site2(do_fetch, max_retries=5, retry_delay=10)
                except:
                    return None
            else:
                return None
        if "503" in error_str or "502" in error_str or "504" in error_str:
            print(f"[Fly sms] ⚠️ সার্ভার ব্যস্ত, কিছুক্ষণ পরে আবার চেষ্টা...")
            time.sleep(30)
            try:
                return retry_request_site2(do_fetch, max_retries=3, retry_delay=15)
            except:
                return None
        print(f"[Fly sms] ❌ আনা/বিশ্লেষণে ত্রুটি AJAX: {e}")
        return None

def extract_rows_from_json_site2(j):
    if j is None:
        return []
    for key in ("data", "aaData", "rows", "aa_data"):
        if isinstance(j, dict) and key in j:
            return j[key]
    if isinstance(j, list):
        return j
    if isinstance(j, dict):
        for v in j.values():
            if isinstance(v, list):
                return v
    return []

def row_to_tuple_site2(row):
    date_str = ""
    number_str = ""
    sms_str = ""
    try:
        if isinstance(row, (list, tuple)):
            if len(row) > IDX_DATE_SITE2:
                val = row[IDX_DATE_SITE2]
                date_str = clean_html_site2(str(val) if val is not None else "")
            if len(row) > IDX_NUMBER_SITE2:
                val = row[IDX_NUMBER_SITE2]
                number_str = clean_number(str(val) if val is not None else "")
            if len(row) > IDX_SMS_SITE2:
                val = row[IDX_SMS_SITE2]
                sms_str = try_decode_site2(val) if val is not None else ""
                sms_str = clean_html_site2(sms_str)
        elif isinstance(row, dict):
            for k in ("date","time","datetime","dt","created_at"):
                if k in row and not date_str:
                    val = row[k]
                    date_str = clean_html_site2(str(val) if val is not None else "")
            for k in ("number","msisdn","cli","from","sender"):
                if k in row and not number_str:
                    val = row[k]
                    number_str = clean_number(str(val) if val is not None else "")
            for k in ("sms","message","msg","body","text"):
                if k in row and not sms_str:
                    val = row[k]
                    sms_str = try_decode_site2(val) if val is not None else ""
                    sms_str = clean_html_site2(sms_str)
            if not sms_str:
                vals = list(row.values())
                if len(vals) > IDX_SMS_SITE2:
                    val = vals[IDX_SMS_SITE2]
                    sms_str = try_decode_site2(val) if val is not None else ""
                    sms_str = clean_html_site2(sms_str)
                elif vals:
                    val = vals[-1]
                    sms_str = try_decode_site2(val) if val is not None else ""
                    sms_str = clean_html_site2(sms_str)
    except Exception as e:
        print(f"[Site2] ⚠️ ত্রুটি: row_to_tuple: {e}")
        print(f"[Site2] Row data: {row}")
    
    unique_key = f"{date_str}|{number_str}|{sms_str}"
    return date_str, number_str, sms_str, unique_key

def load_last_seen_key_site2():
    global last_seen_key_site2
    if os.path.exists(LAST_MESSAGE_FILE_SITE2):
        try:
            with open(LAST_MESSAGE_FILE_SITE2, "r", encoding="utf-8") as f:
                last_seen_key_site2 = f.read().strip()
                print(f"[Site2] 📋 সর্বশেষ দেখা মেসেজ লোড হয়েছে: {last_seen_key_site2[:50]}..." if last_seen_key_site2 else "[Site2] 📋 আগের কোনো মেসেজ নেই")
        except:
            last_seen_key_site2 = ""
    else:
        last_seen_key_site2 = ""

def save_last_seen_key_site2():
    try:
        with open(LAST_MESSAGE_FILE_SITE2, "w", encoding="utf-8") as f:
            f.write(last_seen_key_site2)
        print(f"[Site2] 💾 সর্বশেষ দেখা মেসেজ সেভ হয়েছে")
    except Exception as e:
        print(f"[Site2] ❌ সর্বশেষ মেসেজ সেভে ত্রুটি: {str(e)}")

def load_data():
    global COUNTRIES, CHANNELS, USERS, ADMINS, BANNED, OTP_GROUP, GROUPS, REFERRALS, NUMBERS_ADMINS

    if os.path.exists(COUNTRIES_FILE):
        with open(COUNTRIES_FILE, "r", encoding="utf-8") as f:
            COUNTRIES = json.load(f)

    if os.path.exists(CHANNELS_FILE):
        with open(CHANNELS_FILE, "r", encoding="utf-8") as f:
            CHANNELS = json.load(f)

    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            USERS = json.load(f)

    if os.path.exists(ADMINS_FILE):
        with open(ADMINS_FILE, "r", encoding="utf-8") as f:
            ADMINS = json.load(f)

    if MAIN_ADMIN_ID != 0 and MAIN_ADMIN_ID not in ADMINS:
        ADMINS.append(MAIN_ADMIN_ID)
        save_admins()

    if os.path.exists(BANNED_FILE):
        with open(BANNED_FILE, "r", encoding="utf-8") as f:
            BANNED = json.load(f)

    if os.path.exists(OTP_GROUP_FILE):
        with open(OTP_GROUP_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            OTP_GROUP = data.get("group_id")

    if os.path.exists(GROUPS_FILE):
        with open(GROUPS_FILE, "r", encoding="utf-8") as f:
            GROUPS = json.load(f)
    
    if os.path.exists(REFERRALS_FILE):
        with open(REFERRALS_FILE, "r", encoding="utf-8") as f:
            REFERRALS = json.load(f)
    
    load_numbers_admins()
    load_statistics()


def save_countries():
    with open(COUNTRIES_FILE, "w", encoding="utf-8") as f:
        json.dump(COUNTRIES, f, indent=2, ensure_ascii=False)

def save_channels():
    with open(CHANNELS_FILE, "w", encoding="utf-8") as f:
        json.dump(CHANNELS, f, indent=2, ensure_ascii=False)

def save_users():
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(USERS, f, indent=2, ensure_ascii=False)

def save_admins():
    with open(ADMINS_FILE, "w", encoding="utf-8") as f:
        json.dump(ADMINS, f, indent=2, ensure_ascii=False)

def save_banned():
    with open(BANNED_FILE, "w", encoding="utf-8") as f:
        json.dump(BANNED, f, indent=2, ensure_ascii=False)

def save_otp_group():
    with open(OTP_GROUP_FILE, "w", encoding="utf-8") as f:
        json.dump({"group_id": OTP_GROUP}, f, indent=2)

def save_groups():
    with open(GROUPS_FILE, "w", encoding="utf-8") as f:
        json.dump(GROUPS, f, indent=2)

def cleanup_old_numbers_files(country_code):
   
    pass

def load_referrals():
    global REFERRALS
    if os.path.exists(REFERRALS_FILE):
        try:
            with open(REFERRALS_FILE, "r", encoding="utf-8") as f:
                REFERRALS = json.load(f)
        except:
            REFERRALS = {}
    return REFERRALS

def save_referrals(data=None):
    global REFERRALS
    if data:
        REFERRALS = data
    with open(REFERRALS_FILE, "w", encoding="utf-8") as f:
        json.dump(REFERRALS, f, indent=2, ensure_ascii=False)

def load_referral_settings():
    if os.path.exists(REFERRAL_SETTINGS_FILE):
        try:
            with open(REFERRAL_SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return DEFAULT_REFERRAL_SETTINGS.copy()

def save_referral_settings(settings):
    with open(REFERRAL_SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)

def load_withdrawal_requests():
    if os.path.exists(WITHDRAWAL_REQUESTS_FILE):
        try:
            with open(WITHDRAWAL_REQUESTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return []

def save_withdrawal_requests(requests):
    with open(WITHDRAWAL_REQUESTS_FILE, "w", encoding="utf-8") as f:
        json.dump(requests, f, indent=2, ensure_ascii=False)

DEFAULT_WITHDRAWAL_METHODS = {
    "vodafone": {"name_ar": "ভোডাফোন ক্যাশ", "name_en": "Vodafone Cash", "enabled": True, "details_ar": "ফোন নম্বর", "details_en": "Phone number"},
    "usdt_trc20": {"name_ar": "USDT (TRC20)", "name_en": "USDT (TRC20)", "enabled": True, "details_ar": "ওয়ালেট ঠিকানা TRC20", "details_en": "TRC20 wallet address"},
    "usdt_bep20": {"name_ar": "USDT (BEP20)", "name_en": "USDT (BEP20)", "enabled": True, "details_ar": "ওয়ালেট ঠিকানা BEP20", "details_en": "BEP20 wallet address"},
    "binance_id": {"name_ar": "Binance ID", "name_en": "Binance ID", "enabled": True, "details_ar": "Binance Pay ID অথবা Email", "details_en": "Binance Pay ID or Email"}
}

def load_withdrawal_methods():
    if os.path.exists(WITHDRAWAL_METHODS_FILE):
        try:
            with open(WITHDRAWAL_METHODS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return DEFAULT_WITHDRAWAL_METHODS.copy()

def save_withdrawal_methods(methods):
    with open(WITHDRAWAL_METHODS_FILE, "w", encoding="utf-8") as f:
        json.dump(methods, f, indent=2, ensure_ascii=False)

def load_welcome_messages():
    if os.path.exists(WELCOME_MESSAGES_FILE):
        try:
            with open(WELCOME_MESSAGES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return DEFAULT_WELCOME_MESSAGES.copy()

def save_welcome_messages(messages):
    with open(WELCOME_MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)

def generate_referral_code(user_id):
    
    import hashlib
    hash_input = f"{user_id}_{datetime.now().timestamp()}"
    return hashlib.md5(hash_input.encode()).hexdigest()[:8].upper()

def get_user_referral_data(user_id):
    
    global REFERRALS
    REFERRALS = load_referrals()
    user_key = str(user_id)
    if user_key not in REFERRALS:
        REFERRALS[user_key] = {
            "referral_code": generate_referral_code(user_id),
            "referred_by": None,
            "referrals": [],
            "referred_users_codes": {},
            "active_referrals": 0,
            "active_referrals_list": [],
            "codes_received": 0,
            "balance": 0.0,
            "total_earned": 0.0,
            "referral_used": False
        }
        save_referrals(REFERRALS)
    else:
        if "referral_code" not in REFERRALS[user_key]:
            REFERRALS[user_key]["referral_code"] = generate_referral_code(user_id)
            save_referrals(REFERRALS)
        if "referred_users_codes" not in REFERRALS[user_key]:
            REFERRALS[user_key]["referred_users_codes"] = {}
            save_referrals(REFERRALS)
        if "active_referrals_list" not in REFERRALS[user_key]:
            REFERRALS[user_key]["active_referrals_list"] = []
            save_referrals(REFERRALS)
    return REFERRALS[user_key]

def process_referral(user_id, referrer_id):
    
    global REFERRALS
    REFERRALS = load_referrals()
    settings = load_referral_settings()
    
    user_key = str(user_id)
    referrer_key = str(referrer_id)
    
    if user_key not in REFERRALS:
        REFERRALS[user_key] = {
            "referred_by": referrer_key,
            "referrals": [],
            "active_referrals": 0,
            "codes_received": 0,
            "balance": 0.0,
            "total_earned": 0.0
        }
    else:
        if REFERRALS[user_key].get("referred_by"):
            return False
        REFERRALS[user_key]["referred_by"] = referrer_key
    
    if referrer_key not in REFERRALS:
        REFERRALS[referrer_key] = {
            "referred_by": None,
            "referrals": [],
            "active_referrals": 0,
            "codes_received": 0,
            "balance": 0.0,
            "total_earned": 0.0
        }
    
    if user_key not in REFERRALS[referrer_key]["referrals"]:
        REFERRALS[referrer_key]["referrals"].append(user_key)
    
    save_referrals(REFERRALS)
    return True

def add_code_bonus(user_id):
    
    global REFERRALS
    REFERRALS = load_referrals()
    settings = load_referral_settings()
    
    user_key = str(user_id)
    if user_key not in REFERRALS:
        REFERRALS[user_key] = {
            "referred_by": None,
            "referrals": [],
            "active_referrals": 0,
            "codes_received": 0,
            "balance": 0.0,
            "total_earned": 0.0
        }
    
    REFERRALS[user_key]["codes_received"] += 1
    code_bonus = settings.get("code_bonus", 0.01)
    REFERRALS[user_key]["balance"] += code_bonus
    REFERRALS[user_key]["total_earned"] += code_bonus
    
    referrer_key = REFERRALS[user_key].get("referred_by")
    if referrer_key and referrer_key in REFERRALS:
        codes_required = settings.get("codes_required_for_referral", 3)
        user_codes = REFERRALS[user_key]["codes_received"]
        
        if user_codes == codes_required:
            REFERRALS[referrer_key]["active_referrals"] += 1
            referral_bonus = settings.get("referral_bonus", 0.50)
            REFERRALS[referrer_key]["balance"] += referral_bonus
            REFERRALS[referrer_key]["total_earned"] += referral_bonus
            
            try:
                referrer_lang = get_user_language(int(referrer_key))
                if referrer_lang == "ar":
                    notify_msg = (
                        f"🎉 <b>অভিনন্দন! নতুন রেফারেল সক্রিয় হয়েছে!</b>\n\n"
                        f"👤 ইউজার <code>{user_id}</code> সক্রিয় রেফারেল হয়ে গেছে!\n"
                        f"💰 যোগ করা হয়েছে <b>${referral_bonus:.2f}</b> আপনার ব্যালেন্সে!\n\n"
                        f"📊 মোট সক্রিয় রেফারেল: <b>{REFERRALS[referrer_key]['active_referrals']}</b>\n"
                        f"💵 আপনার বর্তমান ব্যালেন্স: <b>${REFERRALS[referrer_key]['balance']:.2f}</b>"
                    )
                else:
                    notify_msg = (
                        f"🎉 <b>Congratulations! New Active Referral!</b>\n\n"
                        f"👤 User <code>{user_id}</code> became an active referral!\n"
                        f"💰 <b>${referral_bonus:.2f}</b> added to your balance!\n\n"
                        f"📊 Total active referrals: <b>{REFERRALS[referrer_key]['active_referrals']}</b>\n"
                        f"💵 Your current balance: <b>${REFERRALS[referrer_key]['balance']:.2f}</b>"
                    )
                bot.send_message(int(referrer_key), notify_msg, parse_mode="HTML")
            except Exception as notify_err:
                print(f"⚠️ রেফারেল নোটিফিকেশন পাঠাতে ত্রুটি: {notify_err}")
    
    save_referrals(REFERRALS)

REFERRAL_SETTINGS = load_referral_settings()
WELCOME_MESSAGES = load_welcome_messages()

def load_statistics():
    global STATISTICS
    if os.path.exists(STATISTICS_FILE):
        try:
            with open(STATISTICS_FILE, 'r', encoding='utf-8') as f:
                STATISTICS = json.load(f)
        except:
            pass

def save_statistics():
    with open(STATISTICS_FILE, 'w', encoding='utf-8') as f:
        json.dump(STATISTICS, f, indent=2, ensure_ascii=False)

def update_statistics():
    global STATISTICS
    today = datetime.now().date().isoformat()
    week_num = datetime.now().isocalendar()[1]
    month = datetime.now().strftime('%Y-%m')
    
    if STATISTICS.get("last_reset_day") != today:
        STATISTICS["codes_today"] = 0
        STATISTICS["last_reset_day"] = today
    
    if STATISTICS.get("last_reset_week") != week_num:
        STATISTICS["codes_this_week"] = 0
        STATISTICS["last_reset_week"] = week_num
    
    if STATISTICS.get("last_reset_month") != month:
        STATISTICS["codes_this_month"] = 0
        STATISTICS["last_reset_month"] = month
    
    STATISTICS["total_codes"] += 1
    STATISTICS["codes_today"] += 1
    STATISTICS["codes_this_week"] += 1
    STATISTICS["codes_this_month"] += 1
    
    if today not in STATISTICS.get("daily_history", {}):
        if "daily_history" not in STATISTICS:
            STATISTICS["daily_history"] = {}
        STATISTICS["daily_history"][today] = 0
    STATISTICS["daily_history"][today] += 1
    
    save_statistics()

def get_statistics_text():
    total_users = len(USERS)
    total_codes = STATISTICS.get("total_codes", 0)
    codes_today = STATISTICS.get("codes_today", 0)
    codes_week = STATISTICS.get("codes_this_week", 0)
    codes_month = STATISTICS.get("codes_this_month", 0)
    
    text = f"📊 <b>বটের পরিসংখ্যান</b>\n\n"
    text += f"👥 <b>মোট ইউজার:</b> {total_users}\n"
    text += f"🔢 <b>মোট কোড:</b> {total_codes}\n\n"
    text += f"📅 <b>আজকের কোড:</b> {codes_today}\n"
    text += f"📆 <b>এই সপ্তাহের কোড:</b> {codes_week}\n"
    text += f"📊 <b>এই মাসের কোড:</b> {codes_month}\n"
    
    return text

def is_admin(user_id):
    return user_id in ADMINS

def is_banned(user_id):
    return user_id in BANNED

def check_subscription(user_id):
    if not CHANNELS: return True
    for channel in CHANNELS:
        try:
            member = bot.get_chat_member(channel['id'], user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception as e:
            
            err_msg = str(e).lower()
            if "member list is inaccessible" in err_msg or "chat not found" in err_msg:
                
                print(f"⚠️ Warning: Channel {channel['id']} inaccessible for sub check: {e}")
                continue
            return False
    return True

def get_subscription_message(user_id):
    lang = get_user_language(user_id)
    text = "⚠️ <b>চ্যানেলগুলোতে সাবস্ক্রাইব করতে হবে:</b>\n\n" if lang == "ar" else "⚠️ <b>Subscribe to channels:</b>\n\n"
    for idx, ch in enumerate(CHANNELS, 1): text += f"{idx}. {ch['name']}\n"
    return text

def get_full_subscription_keyboard(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    for ch in CHANNELS:
        try:
            chat = bot.get_chat(ch['id'])
        
            url = None
            if chat.invite_link:
                url = chat.invite_link
            elif chat.username:
                url = f"https://t.me/{chat.username}"
            
            if url:
                markup.add(InlineKeyboardButton(ch['name'], url=url))
        except Exception as e:
            print(f"Error getting channel link: {e}")
            continue
    markup.add(InlineKeyboardButton("✅ সাবস্ক্রাইব করা হয়েছে" if get_user_language(user_id) == "ar" else "✅ Subscribed", callback_data="check_sub"))
    return markup

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_sub_callback(call):
    user_id = call.from_user.id
    if check_subscription(user_id):
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass
        start(call.message)
    else: 
        bot.answer_callback_query(call.id, "⚠️ আপনি এখনো সব চ্যানেলে সাবস্ক্রাইব করেননি!", show_alert=True)
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=get_subscription_message(user_id),
                parse_mode="HTML",
                reply_markup=get_full_subscription_keyboard(user_id)
            )
        except: pass

def get_first_unjoined_channel(user_id):
    if not CHANNELS: return None
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel['id'], user_id).status
            if status not in ['member', 'administrator', 'creator']: return channel
        except: return channel
    return None

def get_subscription_keyboard():

    markup = InlineKeyboardMarkup(row_width=1)

    for channel in CHANNELS:
        channel_name = channel.get("name", "Channel")
        channel_url = channel.get("url", "")
        btn = InlineKeyboardButton(f"🔗 Join {channel_name}", url=channel_url)
        markup.add(btn)

    verify_btn = InlineKeyboardButton("✅ যাচাই / Verify", callback_data="verify_subscription", style="success")
    markup.add(verify_btn)

    return markup

def get_all_channels_keyboard(user_id=None):
    markup = InlineKeyboardMarkup(row_width=1)
    lang = get_user_language(user_id) if user_id else "ar"
    
    for channel in CHANNELS:
        channel_name = channel.get(f"name_{lang}", channel.get("name", "Channel"))
        channel_url = channel.get("url", "")
        markup.add(InlineKeyboardButton(f"📢 {channel_name}", url=channel_url))
    
    if lang == "ar":
        verify_text = "✅ সাবস্ক্রিপশন যাচাই করুন"
    else:
        verify_text = "✅ Verify Subscription"
        
    markup.add(InlineKeyboardButton(verify_text, callback_data="verify_subscription"))
    
    return markup

def get_single_channel_keyboard(channel, user_id=None):
    lang = get_user_language(user_id) if user_id else "ar"
    markup = InlineKeyboardMarkup()
    btn_name = channel.get(f"name_{lang}", channel.get("name", "Join 🔗"))
    markup.add(InlineKeyboardButton(btn_name, url=channel['url']))
    
    if lang == "ar":
        verify_text = "✅ সাবস্ক্রিপশন যাচাই করুন"
    else:
        verify_text = "✅ Verify Subscription"
        
    markup.add(InlineKeyboardButton(verify_text, callback_data="verify_subscription"))
    return markup

def get_all_channels_message(user_id):
    lang = get_user_language(user_id)
    
    if lang == "ar":
        text = "🔒 <b>চালিয়ে যেতে নিচের চ্যানেলগুলোতে জয়েন করুন</b>\n\n"
        for i, channel in enumerate(CHANNELS, 1):
            channel_name = channel.get("name_ar", channel.get("name", "Channel"))
            text += f"{i}. 📢 <b>{channel_name}</b>\n"
        return text
    else:
        text = "🔒 <b>Join the following channels to continue</b>\n\n"
        for i, channel in enumerate(CHANNELS, 1):
            channel_name = channel.get("name_en", channel.get("name", "Channel"))
            text += f"{i}. 📢 <b>{channel_name}</b>\n"
        return text

def get_subscription_message(user_id):
    lang = get_user_language(user_id)
    text = "⚠️ <b>চ্যানেলগুলোতে সাবস্ক্রাইব করতে হবে:</b>\n\n" if lang == "ar" else "⚠️ <b>Subscribe to channels:</b>\n\n"
    for idx, ch in enumerate(CHANNELS, 1): text += f"{idx}. {ch['name']}\n"
    return text

def get_main_menu_lang(user_id):
    lang = get_user_language(user_id)
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(t(user_id, "choose_country"), callback_data="choose_country"),
        InlineKeyboardButton(t(user_id, "my_account"), callback_data="my_account")
    )
    
    withdraw_text = "💰 ব্যালেন্স উত্তোলন" if lang == "ar" else "💰 Withdraw"
    help_text = "❓ সাহায্য" if lang == "ar" else "❓ Help"
    markup.add(
        InlineKeyboardButton(withdraw_text, callback_data="withdraw_balance"),
        InlineKeyboardButton(help_text, callback_data="show_instructions")
    )
    
    links = load_button_links()
    dev_text = "👨‍💻 ডেভেলপার" if lang == "ar" else "👨‍💻 Developer"
    markup.add(
        InlineKeyboardButton(dev_text, url=links.get("developer_link", f"tg://user?id={MAIN_ADMIN_ID}"))
    )
    return markup

def get_admin_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("⚙️ সাইট সেটিংস", callback_data="admin_sites_menu", style="primary"),
        InlineKeyboardButton("👥 অ্যাকাউন্ট ম্যানেজমেন্ট", callback_data="admin_accounts_menu", style="primary")
    )
    markup.add(
        InlineKeyboardButton("➕ দেশ যোগ করুন", callback_data="admin_add_country", style="success"),
        InlineKeyboardButton("➖ দেশ মুছুন", callback_data="admin_remove_country", style="danger")
    )
    markup.add(
        InlineKeyboardButton("📋 উপলব্ধ দেশসমূহ", callback_data="admin_list_countries", style="primary")
    )
    markup.add(
        InlineKeyboardButton("📢 চ্যানেল যোগ করুন", callback_data="admin_add_channel", style="success"),
        InlineKeyboardButton("🗑 চ্যানেল মুছুন", callback_data="admin_remove_channel", style="danger")
    )
    markup.add(
        InlineKeyboardButton("📊 যোগ করা চ্যানেল", callback_data="admin_list_channels", style="primary"),
        InlineKeyboardButton("📱 গ্রুপ ম্যানেজমেন্ট", callback_data="admin_groups_menu", style="primary")
    )
    markup.add(
        InlineKeyboardButton("📈 পরিসংখ্যান", callback_data="admin_statistics", style="primary")
    )
    markup.add(
        InlineKeyboardButton("📣 ব্রডকাস্ট", callback_data="admin_broadcast_menu", style="success")
    )
    markup.add(
        InlineKeyboardButton("🔧 অ্যাডমিন যোগ করুন", callback_data="admin_add_admin", style="success"),
        InlineKeyboardButton("🗑 অ্যাডমিন মুছুন", callback_data="admin_remove_admin", style="danger")
    )
    markup.add(
        InlineKeyboardButton("🚫 ইউজার ব্যান", callback_data="admin_ban_user", style="danger"),
        InlineKeyboardButton("✅ আনব্যান", callback_data="admin_unban_user", style="success")
    )
    markup.add(
        InlineKeyboardButton("💰 রেফারেল সিস্টেম", callback_data="admin_referral_settings", style="primary"),
        InlineKeyboardButton("📝 স্বাগত বার্তা", callback_data="admin_welcome_messages", style="primary")
    )
    markup.add(
        InlineKeyboardButton("🔗 বাটনের লিংক", callback_data="admin_button_links", style="primary"),
        InlineKeyboardButton("🔘 মেসেজ বাটন OTP", callback_data="admin_otp_buttons", style="success")
    )
    markup.add(
        InlineKeyboardButton("📥 ব্যাকআপ তৈরি", callback_data="admin_create_backup", style="success"),
        InlineKeyboardButton("📤 ব্যাকআপ পুনরুদ্ধার", callback_data="admin_restore_backup", style="primary")
    )
    markup.add(InlineKeyboardButton("🔙 মূল মেনুতে ফিরুন", callback_data="back_to_main", style="danger"))
    return markup

def get_sites_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🏢 GROUP", callback_data="site_config_GROUP", style="primary"),
        InlineKeyboardButton("🔷 Fly sms", callback_data="site_config_Fly sms", style="primary")
    )
    markup.add(
        InlineKeyboardButton("📱 Number Panel", callback_data="site_config_Number_Panel", style="success"),
        InlineKeyboardButton("⚡ Bolt", callback_data="site_config_Bolt", style="danger"),
        InlineKeyboardButton("🌐 IMS", callback_data="site_config_IMS", style="primary"),
        InlineKeyboardButton("🌸 Roxy SMS", callback_data="site_config_Roxy SMS", style="success")
    )
    markup.add(
        InlineKeyboardButton("🌐 iVAS SMS", callback_data="site_config_iVASMS", style="primary")
    )
    markup.add(
        InlineKeyboardButton("🔵 MSI", callback_data="site_config_MSI", style="success"),
        InlineKeyboardButton(" proton SMS", callback_data="site_config_proton SMS", style="danger")
    )
    markup.add(
        InlineKeyboardButton("🆕 TimeSMS", callback_data="site_config_TimeSMS", style="danger")
    )
    markup.add(InlineKeyboardButton("🔙 অ্যাডমিন প্যানেলে ফিরুন", callback_data="admin", style="primary"))
    return markup

def get_site_config_menu(site_key, account_id=None):
    site_name = SETTINGS[site_key]["name"]
    short_id = account_id[:8] if account_id else ""
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("👤 ইউজারনেম পরিবর্তন", callback_data=f"site_change_user_{site_key}_{short_id}"),
        InlineKeyboardButton("🔑 পাসওয়ার্ড পরিবর্তন", callback_data=f"site_change_pass_{site_key}_{short_id}")
    )
    markup.add(
        InlineKeyboardButton("⏱ অনুসন্ধানের বিরতি", callback_data=f"site_change_interval_{site_key}"),
        InlineKeyboardButton("⏳ অপেক্ষার সময়", callback_data=f"site_change_timeout_{site_key}")
    )
    markup.add(
        InlineKeyboardButton("🔓 লগইন টেস্ট", callback_data=f"site_test_login_{site_key}_{short_id}"),
        InlineKeyboardButton("📥 কোড আনা টেস্ট", callback_data=f"site_test_fetch_{site_key}_{short_id}")
    )
    markup.add(
        InlineKeyboardButton("🆕 TimeSMS", callback_data="site_config_TimeSMS", style="success")
    )
    markup.add(InlineKeyboardButton("🔙 সাইটের তালিকায় ফিরুন", callback_data="admin_sites_menu", style="danger"))
    return markup

def get_site_accounts_selection_menu(site_key):
    site_name = SETTINGS[site_key]["name"]
    accounts = get_site_accounts(site_key)
    
    markup = InlineKeyboardMarkup(row_width=2)
    
    buttons = []
    for idx, account in enumerate(accounts, 1):
        username = account.get("username", "N/A")
        account_id = account.get("id", "")
        short_id = account_id[:8] if account_id else ""
        buttons.append(
            InlineKeyboardButton(
                f"👤 {idx}. {username[:15]}",
                callback_data=f"select_account_config_{site_key}_{short_id}"
            )
        )
    
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.add(buttons[i], buttons[i+1])
        else:
            markup.add(buttons[i])
    
    markup.add(InlineKeyboardButton("🔙 সাইটের তালিকায় ফিরুন", callback_data="admin_sites_menu", style="danger"))
    return markup

def get_accounts_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🏢 GROUP", callback_data="accounts_site_GROUP", style="primary"),
        InlineKeyboardButton("🔷 Fly sms", callback_data="accounts_site_Fly sms", style="success")
    )
    markup.add(
        InlineKeyboardButton("📱 Number Panel", callback_data="accounts_site_Number_Panel", style="primary"),
        InlineKeyboardButton("⚡ Bolt", callback_data="accounts_site_Bolt", style="success"),
        InlineKeyboardButton("🌐 IMS", callback_data="accounts_site_IMS", style="primary"),
        InlineKeyboardButton("🌸 Roxy SMS", callback_data="accounts_site_Roxy SMS", style="success")
    )
    markup.add(
        InlineKeyboardButton("🌐 iVAS SMS", callback_data="accounts_site_iVASMS", style="danger")
    )
    markup.add(
        InlineKeyboardButton("🔵 MSI", callback_data="accounts_site_MSI", style="primary"),
        InlineKeyboardButton("proton SMS", callback_data="accounts_site_proton SMS", style="success")
    )
    markup.add(
        InlineKeyboardButton("🆕 TimeSMS", callback_data="accounts_site_TimeSMS", style="danger")
    )
    markup.add(InlineKeyboardButton("🔙 অ্যাডমিন প্যানেলে ফিরুন", callback_data="admin_panel", style="danger"))
    return markup

def get_site_accounts_menu(site_key):
    site_name = SETTINGS[site_key]["name"]
    accounts = get_site_accounts(site_key)
    
    markup = InlineKeyboardMarkup(row_width=2)
    
    if accounts:
        buttons = []
        for idx, account in enumerate(accounts, 1):
            username = account.get("username", "N/A")
            account_id = account.get("id", "")
            short_id = account_id[:8] if account_id else ""
            buttons.append(
                InlineKeyboardButton(
                    f"👤 {idx}. {username[:15]}",
                    callback_data=f"view_account_{site_key}_{short_id}"
                )
            )
        
        for i in range(0, len(buttons), 2):
            if i + 1 < len(buttons):
                markup.add(buttons[i], buttons[i+1])
            else:
                markup.add(buttons[i])
    
    markup.add(
        InlineKeyboardButton("➕ নতুন অ্যাকাউন্ট যোগ", callback_data=f"add_account_{site_key}")
    )
    markup.add(InlineKeyboardButton("🔙 সাইটের তালিকায় ফিরুন", callback_data="admin_accounts_menu", style="danger"))
    return markup

def get_account_details_menu(site_key, account_id):
    short_id = account_id[:8] if account_id else ""
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🗑 অ্যাকাউন্ট মুছুন", callback_data=f"delete_account_{site_key}_{short_id}"),
        InlineKeyboardButton("🔙 অ্যাকাউন্টে ফিরুন", callback_data=f"accounts_site_{site_key}")
    )
    return markup

def try_decode(raw):
    if raw is None:
        return ""
    
    if isinstance(raw, str):
        
        return raw.replace('\x00', '').strip()
    
    if not isinstance(raw, bytes):
        try:
            
            return str(raw).replace('\x00', '').strip()
        except:
            return ""

  
    encodings = (
        "utf-8", 
        "utf-16", "utf-16-be", "utf-16-le",
        "cp1256", "windows-1256", "iso-8859-6", 
        "cp1251", "windows-1251", "koi8-r",    
        "latin-1", "iso-8859-1"
    )
    
    for enc in encodings:
        try:
            s = raw.decode(enc)
            
            return s.replace('\x00', '').strip()
        except:
            continue
    
    return raw.decode('utf-8', errors='replace').replace('\x00', '').strip()

def mask_number(num):
    s = str(num)
    digits = re.sub(r'\D', '', s)
    if len(digits) <= 6:
        return s
    
    if len(digits) >= 11:
        return digits[:2] + "••••••" + digits[-3:]
    return digits[:2] + "•••" + digits[-2:]

import phonenumbers
from phonenumbers.phonenumberutil import region_code_for_number
import pycountry

def get_flag(country_code):
    if not country_code: return "🌍"
    return ''.join([chr(0x1F1E6 + ord(c) - ord('A')) for c in country_code.upper()])

def detect_country_from_number(number, user_id=None):
    try:
        s = str(number).strip()
        if not s.startswith('+'):
            s = '+' + s
        
       
        try:
            parsed = phonenumbers.parse(s)
        except phonenumbers.NumberParseException:
            
            parsed = phonenumbers.parse(s + "00000000")
            
        region = phonenumbers.region_code_for_number(parsed)
        if not region:
            return "Unknown", "🌍", "UN"
        
        lang = get_user_language(user_id) if user_id else "ar"
        
       
        country_name = geocoder.description_for_number(parsed, lang)
        
       
        if not country_name or country_name == "Unknown":
            try:
                py_country = pycountry.countries.get(alpha_2=region)
                if py_country:
                    
                    country_name = py_country.name
            except:
                pass

       
        if not country_name or country_name == "Unknown":
            country_name = geocoder.description_for_number(parsed, "en")
            
        if not country_name or country_name == "Unknown":
            country_name = region

        flag = get_flag(region)
        return country_name, flag, region
    except Exception as e:
        print(f"Error detecting country: {e}")
        return "Unknown", "🌍", "UN"

def format_otp_message(number, sms_text, service_name="[TG]", otp_code=None, user_id=None):
    country_name, flag, region_code = detect_country_from_number(number, user_id)
    masked = mask_number(number)
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    header = f"──────────────╖ \n↠ {flag} #{region_code} {service_name} {masked} ┨<tg-emoji emoji-id='6084757039567868626'>👆</tg-emoji>\n──────────────╛"
    
    body = f"<blockquote>{sms_text}</blockquote>"
    time_footer = f"<blockquote>• <tg-emoji emoji-id='5413704112220949842'>⏰</tg-emoji> ~ {now_str}</blockquote>"
    
    return f"{header}\n{body}\n{time_footer}"


def detect_service(text, source_addr=None):
    if not text:
        return "Unknown 🌐"
    t = text.lower()
    source_lower = source_addr.lower() if source_addr else ""
    
   
    if any(k in t for k in ["whatsapp", "واتساب", "واتس"]):
        return "<tg-emoji emoji-id='5188683998125106802'>📞</tg-emoji>"
    if any(k in t for k in ["telegram", "تيليجرام", "تلجرام"]):
        return "<tg-emoji emoji-id='5471949924658588235'>👉</tg-emoji>"
    if any(k in t for k in ["facebook", "فيسبوك", "meta"]):
        return "FB"
    if any(k in t for k in ["instagram", "انستقرام", "انستا"]):
        return "IG"
    if any(k in t for k in ["tiktok", "تيك توك", "تيكتوك"]):
        return "TK"
    if any(k in t for k in ["google", "جوجل", "gmail"]):
        return "GG"
    if any(k in t for k in ["imo", "ايمو"]):
        return "IM"
    if any(k in t for k in ["viber", "فايبر"]):
        return "VB"
    if any(k in t for k in ["snapchat", "سناب"]):
        return "SC"

    services = {
        "whatsapp": "<tg-emoji emoji-id='5188683998125106802'>📞</tg-emoji>",
        "واتساب": "WS",
        "واتس": "WS",
        "facebook": "FB",
        "فيسبوك": "FB",
        "meta": "FB",
        "instagram": "IG",
        "انستقرام": "IG",
        "انستا": "IG",
        "telegram": "<tg-emoji emoji-id='5471949924658588235'>👉</tg-emoji>",
        "تيليجرام": "<tg-emoji emoji-id='5471949924658588235'>👉</tg-emoji>",
        "تلجرام": "<tg-emoji emoji-id='5471949924658588235'>👉</tg-emoji>",
        "twitter": "TW",
        "تويتر": "TW",
        "x.com": "TW",
        "snapchat": "SC",
        "سناب": "SC",
        "tiktok": "TK",
        "تيك توك": "TK",
        "google": "GG",
        "جوجل": "GG",
        "gmail": "GG",
        "linkedin": "LN",
        "لينكد": "LN",
        "discord": "DC",
        "ديسكورد": "DC",
        "uber": "UB",
        "bolt": "BT",
        "careem": "CR",
        "amazon": "AZ",
        "netflix": "NF",
        "spotify": "SP",
        "apple": "AP",
        "microsoft": "MS",
        "paypal": "PP",
        "binance": "BN",
        "coinbase": "CB",
    }

    for keyword, service in services.items():
        if keyword in t:
            return service
    
    for keyword, service in services.items():
        if keyword in source_lower:
            return service

    if source_addr and source_addr.strip():
        cleaned_source = source_addr.replace('#', '').strip()
        if cleaned_source:
            return cleaned_source.upper()
    return "Unknown 🌐"

def get_country_flags(country_name):
    
    flags = {
        "مصر": "<tg-emoji emoji-id='5976310790381115423'>🇪🇬</tg-emoji>", "Egypt": "<tg-emoji emoji-id='5976310790381115423'>🇪🇬</tg-emoji>",
        "السعودية": "<tg-emoji emoji-id='5976726495970729818'>🇸🇦</tg-emoji>", "Saudi Arabia": "<tg-emoji emoji-id='5976726495970729818'>🇸🇦</tg-emoji>",
        "ليبيا": "🇱🇾", "Libya": "🇱🇾",
        "الجزائر": "🇩🇿", "Algeria": "🇩🇿",
        "زيبمبابوي":"<tg-emoji emoji-id='5357255314099943456'>🇿🇼</tg-emoji>"," Zimbabwe": "<tg-emoji emoji-id='5357255314099943456'>🇿🇼</tg-emoji>", 
        "المغرب": "🇲🇦", "Morocco": "🇲🇦",
        "تونس": "🇹🇳", "Tunisia": "🇹🇳",
        "العراق": "<tg-emoji emoji-id='5976458232313420307'>🇮🇶</tg-emoji>", "Iraq": "<tg-emoji emoji-id='5976458232313420307'>🇮🇶</tg-emoji>",
        "الأردن": "🇯🇴", "Jordan": "🇯🇴",
        "فينزويلا":"<tg-emoji emoji-id='5228751795274136090'>🇻🇪</tg-emoji>", "Venezuela": "<tg-emoji emoji-id='5228751795274136090'>🇻🇪</tg-emoji>" ,
        "الإمارات": "🇦🇪", "UAE": "🇦🇪",
        "الكويت": "🇰🇼", "Kuwait": "🇰🇼",
        "قطر": "🇶🇦", "Qatar": "🇶🇦",
        "لبنان": "🇱🇧", "Lebanon": "🇱🇧",
        "سوريا": "🇸🇾", "Syria": "🇸🇾",
        "روسيا": "🇷🇺", "Russia": "🇷🇺",
        "أمريكا": "🇺🇸", "USA": "🇺🇸",
        "فرنسا": "🇫🇷", "France": "🇫🇷",
        "ألمانيا": "<tg-emoji emoji-id='5976493356555968244'>🇩🇪</tg-emoji>", "Germany": "<tg-emoji emoji-id='5976493356555968244'>🇩🇪</tg-emoji>",
        "تركيا": "🇹🇷", "Turkey": "🇹🇷"
    }
    return flags.get(country_name, "🌍")

def detect_country_code_from_file(file_path):
   
    try:
        prefixes = {}
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if not line: continue
            first_part = line.split()[0] if line.split() else line
            digits = ''.join(c for c in first_part if c.isdigit())
            
            if len(digits) >= 8:
               
                for i in range(1, 4):
                    prefix = digits[:i]
                    prefixes[prefix] = prefixes.get(prefix, 0) + 1
        
        if not prefixes:
            return None
            
        
        sorted_prefixes = sorted(prefixes.items(), key=lambda x: (x[1], len(x[0])), reverse=True)
        return sorted_prefixes[0][0] 
    except Exception as e:
        print(f"Error detecting country code: {e}")
        return None

def clean_and_filter_numbers(file_path, country_code):
    
    cleaned_numbers = []
    total_lines = 0
    rejected_lines = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue

            total_lines += 1

            parts = re.split(r'\s+', line)
            if not parts:
                rejected_lines += 1
                continue

            first_part = parts[0].strip()
            digits = re.sub(r'\D', '', first_part)

            if not digits:
                rejected_lines += 1
                continue

            if digits.startswith(country_code):
                cleaned_numbers.append(digits)
            else:
                rejected_lines += 1

        with open(file_path, 'w', encoding='utf-8') as f:
            for number in cleaned_numbers:
                f.write(number + '\n')

        return (len(cleaned_numbers), total_lines, rejected_lines)

    except Exception as e:
        print(f"❌ ফাইল পরিষ্কারে ত্রুটি: {e}")
        return (0, 0, 0)

def get_platform_buttons(country_name):
   
    markup = InlineKeyboardMarkup(row_width=2)
    buttons_found = False
    
    
    if country_name in COUNTRIES:
        info = COUNTRIES[country_name]
        platforms = info.get('platforms', [])
        platform_icons = {
            "Facebook": "📘 Facebook",
            "WhatsApp": "💬 WhatsApp",
            "Telegram": "✈️ Telegram",
            "Instagram": "📸 Instagram",
            "Twitter": "🐦 Twitter/X",
            "TikTok": "📱 TikTok",
            "Discord": "🎮 Discord",
            "Gmail": "📧 Gmail"
        }
        for platform in platforms:
            display_name = platform_icons.get(platform, f"📱 {platform}")
            markup.add(InlineKeyboardButton(display_name, callback_data=f"platform_{country_name}_{platform}"))
            buttons_found = True
    else:
        
        platform_icons = {
            "Facebook": "📘 Facebook",
            "WhatsApp": "💬 WhatsApp",
            "Telegram": "✈️ Telegram",
            "Instagram": "📸 Instagram",
            "Twitter": "🐦 Twitter/X",
            "TikTok": "📱 TikTok",
            "Discord": "🎮 Discord",
            "Gmail": "📧 Gmail"
        }
        for cid, info in COUNTRIES.items():
            if info.get("display_name") == country_name or cid == country_name:
                platforms = info.get('platforms', [])
                for platform in platforms:
                    display_name = platform_icons.get(platform, f"📱 {platform}")
                    markup.add(InlineKeyboardButton(display_name, callback_data=f"platform_{cid}_{platform}"))
                    buttons_found = True

    if not buttons_found:
        return None
    
    markup.add(InlineKeyboardButton("𝗕𝗮𝗰𝗸", callback_data="choose_country", style="danger"))
    return markup

def get_platforms_list(user_id=None):
    
    platform_stats = {}
    for country_id, info in COUNTRIES.items():
        platforms = info.get("platforms", [])
        count = info.get("numbers_count", 0)
        
        filename = info.get("file", "")
        if count == 0 and filename and os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    count = sum(1 for line in f if line.strip())
            except:
                pass
        
        for p in platforms:
            platform_stats[p] = platform_stats.get(p, 0) + count

    platform_icons = {
        "Facebook": "📘 Facebook",
        "WhatsApp": "💬 WhatsApp",
        "Telegram": "✈️ Telegram",
        "Instagram": "📸 Instagram",
        "Twitter": "🐦 Twitter/X",
        "TikTok": "📱 TikTok",
        "Discord": "🎮 Discord",
        "Gmail": "📧 Gmail"
    }

    markup = InlineKeyboardMarkup(row_width=1)
    for platform, count in platform_stats.items():
        if count > 0:
            display_name = platform_icons.get(platform, f"📱 {platform}")
            markup.add(InlineKeyboardButton(f"{display_name} ({count})", callback_data=f"select_plt_{platform}"))
    
    return markup

def get_countries_for_platform(platform, user_id=None):
    
    lang = get_user_language(user_id)
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = []
    
    
    display_name_counts = {}
    
    
    total_counts = {}
    for info in COUNTRIES.values():
        if platform in info.get("platforms", []):
            dname = info.get("display_name")
            total_counts[dname] = total_counts.get(dname, 0) + 1

    for cid, info in COUNTRIES.items():
        if platform in info.get("platforms", []):
            display_name = info.get("display_name", cid)
            flag = info.get("flag", "🌍")
            count = info.get("numbers_count", 0)
            code = info.get("code", "")
            
            display_name_counts[display_name] = display_name_counts.get(display_name, 0) + 1
            entry_number = display_name_counts[display_name]
            
            label = f"{flag} {display_name}"
            
            if total_counts.get(display_name, 0) > 1:
                label += f" {entry_number}"
            
            if code:
                label += f" (+{code})"

            markup.add(InlineKeyboardButton(f"{label} ({count})", callback_data=f"country_{cid}"))
    
    markup.add(InlineKeyboardButton("🔙 Back" if lang != "ar" else "🔙 ফিরে যান", callback_data="choose_country"))
    return markup

def get_countries_list(user_id=None):
    
    lang = get_user_language(user_id)
    markup = InlineKeyboardMarkup(row_width=2)
    found = False
    
    
    display_name_counts = {}
    total_counts = {}
    for info in COUNTRIES.values():
        dname = info.get("display_name")
        total_counts[dname] = total_counts.get(dname, 0) + 1

    for cid, info in COUNTRIES.items():
        display_name = info.get("display_name", cid)
        flag = info.get("flag", "🌍")
        code = info.get("code", "??")
        count = info.get("numbers_count", 0)
        
        display_name_counts[display_name] = display_name_counts.get(display_name, 0) + 1
        entry_number = display_name_counts[display_name]
        
        label = f"{flag} {display_name}"
        if total_counts.get(display_name, 0) > 1:
            label += f" {entry_number}"
            
        markup.add(InlineKeyboardButton(f"{label} (+{code}) ({count})", callback_data=f"country_{cid}"))
        found = True
    
    markup.add(InlineKeyboardButton("🔙 Back" if lang != "ar" else "🔙 ফিরে যান", callback_data="choose_country"))
    return markup if found else None

def get_country_buttons(user_id=None):
    return get_platforms_list(user_id)

def get_random_number(country_name):
    if country_name not in COUNTRIES:
        return None

    filename = COUNTRIES[country_name]["file"]

    if not os.path.exists(filename):
        return None

    with open(filename, "r", encoding="utf-8") as f:
        numbers = [line.strip() for line in f if line.strip()]

    if not numbers:
        return None

    return random.choice(numbers)

def create_message_buttons(user_id=None):
    user_id = user_id or telebot.types.User(0, False, "Dummy").id
    lang = get_user_language(user_id)
    links = load_button_links()
    markup = InlineKeyboardMarkup(row_width=1)
    
    change_number_text = "🔄 নম্বর পরিবর্তন" if lang == "ar" else "🔄 Change Number"
    change_country_text = "🌍 দেশ পরিবর্তন" if lang == "ar" else "🌍 Change Country"
    group_link_text = "📢 বটের গ্রুপ" if lang == "ar" else "📢 Group Link"
    back_text = "🔙 মূল মেনু" if lang == "ar" else "🔙 Back to Main"
    
    markup.add(InlineKeyboardButton(change_number_text, callback_data="change_number"))
    markup.add(InlineKeyboardButton(change_country_text, callback_data="choose_country"))
    markup.add(InlineKeyboardButton(group_link_text, url=links.get("group_link", "https://t.me/alorhawa")))
    markup.add(InlineKeyboardButton(back_text, callback_data="back_to_main"))
    
    return markup

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_group_otp_keyboard(otp_code=None):
    otp_buttons = load_otp_buttons()  # ধরে নিন এটি বাটনের তালিকা ফেরত দেয়
    
    markup = InlineKeyboardMarkup(row_width=2)
    
    # ────────────── ইমোজি সেটআপ ──────────────
    OTP_EMOJI_ID = "5454386656628991407"       # বাটনের ইমোজি OTP
    DEFAULT_EMOJI_LEFT = "5974337549261347177" # সারির প্রথম বাটন
    DEFAULT_EMOJI_RIGHT = "5368324170671202286"# সারির দ্বিতীয় বাটন
    
    # ────────────── বাটন OTP ──────────────
    if otp_code and otp_code != "N/A":
        try:
            markup.add(
                InlineKeyboardButton(
                    text=f"🔑 {otp_code}",
                    callback_data=f"copy_{otp_code}"
                )
            )
        except Exception as e:
            print(f"বাটন তৈরিতে ত্রুটি OTP: {e}")
            markup.add(
                InlineKeyboardButton(
                    text=f"🔑 {otp_code}",
                    callback_data=f"copy_{otp_code}"
                )
            )
    
    # ────────────── অন্য বাটন (otp_buttons) ──────────────
    if otp_buttons:
        row_buttons = []
        button_index = 0
        
        for btn in otp_buttons:
            emoji_id = btn.get("emoji_id")
            
            if not emoji_id:
                # ডিফল্টগুলো ক্রম অনুযায়ী ভাগ করুন
                emoji_id = DEFAULT_EMOJI_LEFT if button_index % 2 == 0 else DEFAULT_EMOJI_RIGHT
            
            try:
                # বাটনের রং: প্রথমটি নীল, দ্বিতীয়টি সবুজ
                btn_style = "primary" if button_index % 2 == 0 else "primary"
                
                button = InlineKeyboardButton(
                    text=f" {btn['name']}",
                    url=btn["url"],
                    icon_custom_emoji_id=emoji_id,
                    style=btn_style
                )
                row_buttons.append(button)
            except Exception as e:
                print(f"ত্রুটি: custom emoji বাটনের জন্য {btn['name']}: {e}")
                row_buttons.append(
                    InlineKeyboardButton(
                        text=btn["name"],
                        url=btn["url"]
                    )
                )
            
            button_index += 1
        
        # প্রতি সারিতে 2টি বাটন
        for i in range(0, len(row_buttons), 2):
            chunk = row_buttons[i:i+2]
            markup.add(*chunk)
    
    # ────────────── চতুর্থ বাটন (আলাদা সারিতে) ──────────────
    FOURTH_BUTTON_TEXT = "𝗗𝗘𝗩𝗘𝗟𝗢𝗣𝗘𝗥"
    FOURTH_BUTTON_URL = "https://t.me/alorhawa"
    FOURTH_EMOJI_ID = "5203916679460953989"
    
    markup.add(
        InlineKeyboardButton(
            text=f" {FOURTH_BUTTON_TEXT}",
            url=FOURTH_BUTTON_URL,
            icon_custom_emoji_id=FOURTH_EMOJI_ID,
            style="danger"   # লাল রং
        )
    )
    
    return markup if (otp_code or otp_buttons) else None

@bot.callback_query_handler(func=lambda call: call.data.startswith("copy_"))
def handle_copy_callback(call):
    otp = call.data.split("_", 1)[1]
    
    bot.answer_callback_query(call.id, f"{otp}", show_alert=True)

def create_otp_message_keyboard(otp_code):
    global OTP_BUTTONS
    OTP_BUTTONS = load_otp_buttons()
    
    markup = InlineKeyboardMarkup(row_width=2)
    
    
    for btn in OTP_BUTTONS:
        markup.add(InlineKeyboardButton(btn["name"], url=btn["url"]))
    
    
    markup.add(InlineKeyboardButton("📋 Copy OTP", callback_data=f"copy_otp_{otp_code}"))
    
    return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith("copy_otp_"))
def copy_otp_callback(call):
    otp_code = call.data.replace("copy_otp_", "")
    bot.answer_callback_query(call.id, f"✅ Code: {otp_code}\n(Long press to copy if your client supports it)", show_alert=True)

def auto_delete_message(chat_id, message_id, delay=300):
    def delete():
        time.sleep(delay)
        try: bot.delete_message(chat_id, message_id)
        except: pass
    threading.Thread(target=delete, daemon=True).start()

def safe_send_message(chat_id, text, **kwargs):
    msg = bot.send_message(chat_id, text, **kwargs)
    if isinstance(chat_id, (int, str)) and (int(chat_id) < 0 or str(chat_id).startswith("-100")):
        auto_delete_message(int(chat_id), msg.message_id)
    return msg


original_send = bot.send_message
def hooked_send(chat_id, *args, **kwargs):
    msg = original_send(chat_id, *args, **kwargs)
    if isinstance(chat_id, (int, str)) and (int(chat_id) < 0 or str(chat_id).startswith("-100")):
        auto_delete_message(int(chat_id), msg.message_id)
    return msg
bot.send_message = hooked_send

def format_otp_message(country_name, country_flag, service_detected, number, otp, message_text, server_key="GROUP", is_group=False, show_full_number=True, user_id=None):
    
    use_shorthand = is_group or (OTP_GROUP and str(user_id) == str(OTP_GROUP))
    
    service_upper = str(service_detected).upper()
    shorthand = service_upper
    
    if use_shorthand:
        SHORTHANDS = {
            "WHATSAPP": "<tg-emoji emoji-id='5188683998125106802'>📞</tg-emoji>",
            "TELEGRAM": "<tg-emoji emoji-id='5471949924658588235'>👉</tg-emoji>",
            "FACEBOOK": "FB",
            "INSTAGRAM": "IG",
            "TIKTOK": "TK",
            "TWITTER": "TW",
            "GOOGLE": "GG",
            "MICROSOFT": "MS",
            "NETFLIX": "NF",
            "STEAM": "ST",
            "SNAPCHAT": "SC",
            "VIBER": "VB",
            "IMO": "IM",
            "WECHAT": "WC",
            "LINE": "LN",
            "DISCORD": "DC",
            "PAYPAL": "PP",
            "AMAZON": "AZ",
            "EBAY": "EB",
            "APPLE": "AP"
        }

        
        found = False
        for key, val in SHORTHANDS.items():
            if key in service_upper:
                shorthand = val
                found = True
                break
                
        if not found:
        
            shorthand = service_upper[:2] if len(service_upper) > 2 else service_upper
            
    service_name = f"[{shorthand}]"
    formatted = format_otp_message_v2(number, message_text, service_name, otp)
    
    if OTP_GROUP:
        try:
            
            if not use_shorthand:
               
                group_shorthand = service_upper
                SHORTHANDS = {"WHATSAPP": "<tg-emoji emoji-id='5188683998125106802'>📞</tg-emoji>", "TELEGRAM": "<tg-emoji emoji-id='5471949924658588235'>👉</tg-emoji>", "FACEBOOK": "FB", "INSTAGRAM": "IG", "TIKTOK": "TK", "TWITTER": "TW"}
                for key, val in SHORTHANDS.items():
                    if key in service_upper:
                        group_shorthand = val
                        break
                if group_shorthand == service_upper: 
                    group_shorthand = service_upper[:2]
                
                group_service_name = f"[{group_shorthand}]"
                group_formatted = format_otp_message_v2(number, message_text, group_service_name, otp, is_group=True)
            else:
                group_formatted = formatted
            
            msg = original_send(OTP_GROUP, group_formatted, parse_mode="HTML", reply_markup=create_group_otp_keyboard(otp))
            auto_delete_message(OTP_GROUP, msg.message_id)
        except: pass
    return formatted

def format_otp_message_v2(number, sms_text, service_name="[TG]", otp_code=None, is_group=False):
    country_name, flag, region_code = detect_country_from_number(number)
    masked = mask_number(number)
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    display_service = service_name
    if is_group:
        service_clean = str(service_name).replace("[", "").replace("]", "").upper()
        SHORTHANDS = {
            "WHATSAPP": "<tg-emoji emoji-id='5188683998125106802'>📞</tg-emoji>", "TELEGRAM": "TG", "FACEBOOK": "FB", "INSTAGRAM": "IG", 
            "TIKTOK": "TK", "TWITTER": "TW", "GOOGLE": "GG", "MICROSOFT": "MS"
        }
        found_sh = service_clean
        for k, v in SHORTHANDS.items():
            if k in service_clean:
                found_sh = v
                break
        if found_sh == service_clean and len(found_sh) > 3:
            found_sh = found_sh[:2]
        display_service = f"[{found_sh}]"
    
    otp_display = ""
    if otp_code:
        otp_display = "" 

    line_content = f"↠ {flag} #{region_code} {display_service} {masked} ┨<tg-emoji emoji-id='6084757039567868626'>👆</tg-emoji>"
   
    top_bottom_line = "──────────────"
    
    header = f"{top_bottom_line}╖ \n{line_content}\n{top_bottom_line}╛"
    
    body = f"<blockquote><tg-emoji emoji-id='5971844011508372946'>☠</tg-emoji>{sms_text}</blockquote>"
    time_footer = f"<blockquote>• <tg-emoji emoji-id='5413704112220949842'>⏰</tg-emoji> ~ {now_str}</blockquote>"
    
    return f"{header}\n{otp_display}\n{body}\n{time_footer}"

@bot.message_handler(commands=["start"])
def start(msg):
    user_id = msg.from_user.id

    if is_banned(user_id):
        bot.reply_to(msg, t(user_id, "banned"))
        return

    if msg.chat.type == "private":
        referrer_id = None
        if msg.text and len(msg.text.split()) > 1:
            param = msg.text.split()[1]
            if param.startswith("ref_"):
                try:
                    referrer_id = int(param.replace("ref_", ""))
                    if referrer_id == user_id:
                        referrer_id = None
                except:
                    referrer_id = None
        
        is_new_user = str(user_id) not in USERS
        
        if is_new_user or "language" not in USERS.get(str(user_id), {}):
            if is_new_user and referrer_id:
                USERS[str(user_id)] = {
                    "selected_country": None, 
                    "selected_number": None, 
                    "join_date": datetime.now().strftime('%Y-%m-%d'),
                    "activations": 0,
                    "pending_referrer": referrer_id
                }
                save_users()
            
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("🇧🇩 বাংলা", callback_data="set_lang_ar", style="success"),
                InlineKeyboardButton("🇬🇧 English", callback_data="set_lang_en", style="primary")
            )
            bot.send_message(
                msg.chat.id,
                "🌍 <b>ভাষা বেছে নিন / Choose Language</b>",
                parse_mode="HTML",
                reply_markup=markup
            )
            return
        
        if not check_subscription(user_id):
            bot.send_message(
                msg.chat.id,
                get_subscription_message(user_id),
                parse_mode="HTML",
                reply_markup=get_full_subscription_keyboard(user_id)
            )
            return

        if str(user_id) not in USERS:
            USERS[str(user_id)] = {"selected_country": None, "selected_number": None, "language": "ar", "join_date": datetime.now().strftime('%Y-%m-%d'), "activations": 0}
            save_users()
        
        if referrer_id and is_new_user:
            process_referral(user_id, referrer_id)
            lang = get_user_language(user_id)
            try:
                bot.send_message(user_id, t(user_id, "referral_success"))
            except:
                pass

        if is_admin(user_id):
            admin_markup = get_admin_menu()
            bot.send_message(
                msg.chat.id,
                "🎛 <b>অ্যাডমিন প্যানেল</b>\n\nপ্রয়োজনীয় অপশন বেছে নিন:",
                parse_mode="HTML",
                reply_markup=admin_markup
            )
            return
        
        lang = get_user_language(user_id)
        settings = load_referral_settings()
        code_bonus = settings.get("code_bonus", 0.01)
        
        markup = get_platforms_list(user_id)
        if markup:
            if lang == "ar":
                title = f"<tg-emoji emoji-id='5972277098830634724'>🚨</tg-emoji> <b>প্ল্যাটফর্ম বেছে নিন</b>\n\n<tg-emoji emoji-id='6046356449938905522'>💰</tg-emoji> আপনি পাবেন <b>${format_decimal(code_bonus)}</b> প্রতিটি কোড পেলে!"
            else:
                title = f"<tg-emoji emoji-id='5972277098830634724'>🚨</tg-emoji> <b>Select Platform</b>\n\n<tg-emoji emoji-id='6046356449938905522'>💰</tg-emoji> You'll earn <b>${format_decimal(code_bonus)}</b> for each code received!"
            
            bot.send_message(
                msg.chat.id,
                title,
                parse_mode="HTML",
                reply_markup=markup
            )
        else:
            text = t(user_id, "welcome")
            if not text: text = "🌐 <b>স্বাগতম!</b>"
            bot.send_message(
                msg.chat.id,
                text,
                parse_mode="HTML",
                reply_markup=get_main_menu_lang(user_id)
            )
    else:
        if is_admin(user_id):
            bot.send_message(
                msg.chat.id,
                t(user_id, "group_hello_admin"),
                parse_mode="HTML"
            )
        else:
            bot.send_message(
                msg.chat.id,
                t(user_id, "group_hello"),
                parse_mode="HTML"
            )

@bot.message_handler(commands=["getnumber"])
def getnumber_command(msg):
    user_id = msg.from_user.id
    
    if is_banned(user_id):
        bot.reply_to(msg, t(user_id, "banned"))
        return
    
    if msg.chat.type != "private":
        return
    
    if not check_subscription(user_id):
        unjoined_channel = get_first_unjoined_channel(user_id)
        if unjoined_channel:
            bot.send_message(
                msg.chat.id,
                get_subscription_message_for_channel(unjoined_channel, user_id),
                parse_mode="HTML",
                reply_markup=get_single_channel_keyboard(unjoined_channel, user_id)
            )
        return
    
    lang = get_user_language(user_id)
    settings = load_referral_settings()
    code_bonus = settings.get("code_bonus", 0.01)
    
    markup = get_country_buttons(user_id)
    if markup:
        if lang == "ar":
            title = f"<tg-emoji emoji-id='5972277098830634724'>🚨</tg-emoji> <b>প্ল্যাটফর্ম বেছে নিন</b>\n\n<tg-emoji emoji-id='6046356449938905522'>💰</tg-emoji> আপনি পাবেন <b>${format_decimal(code_bonus)}</b> প্রতিটি কোড পেলে!"
        else:
            title = f"<tg-emoji emoji-id='5972277098830634724'>🚨</tg-emoji> <b>Select Country</b>\n\n💰 You'll earn <b>${format_decimal(code_bonus)}</b> for each code received!"
        
        bot.send_message(msg.chat.id, title, parse_mode="HTML", reply_markup=markup)

@bot.message_handler(commands=["account"])
def account_command(msg):
    user_id = msg.from_user.id
    
    if is_banned(user_id):
        bot.reply_to(msg, t(user_id, "banned"))
        return
    
    if msg.chat.type != "private":
        return
    
    if not check_subscription(user_id):
        unjoined_channel = get_first_unjoined_channel(user_id)
        if unjoined_channel:
            bot.send_message(
                msg.chat.id,
                get_subscription_message_for_channel(unjoined_channel, user_id),
                parse_mode="HTML",
                reply_markup=get_single_channel_keyboard(unjoined_channel, user_id)
            )
        return
    
    user_data = USERS.get(str(user_id), {})
    activations = user_data.get("activations", 0)
    join_date = user_data.get("join_date", datetime.now().strftime('%Y-%m-%d'))
    lang = get_user_language(user_id)
    
    referral_data = get_user_referral_data(user_id)
    balance = referral_data.get("balance", 0.0)
    total_earned = referral_data.get("total_earned", 0.0)
    referrals_count = len(referral_data.get("referrals", []))
    active_referrals = referral_data.get("active_referrals", 0)
    
    selected_country = user_data.get("selected_country")
    selected_number = user_data.get("selected_number")
    
    if selected_number and selected_country:
        number_status = f"✅ সক্রিয় নম্বর: {selected_country}" if lang == "ar" else f"✅ Active number for {selected_country}"
    else:
        number_status = "❌ এখন কোনো নম্বর নেই" if lang == "ar" else "❌ No number currently"
    
    bot_info = bot.get_me()
    referral_link = f"https://t.me/{bot_info.username}?start=ref_{user_id}"
    
    if lang == "ar":
        account_text = (
            f"👤 <b>আপনার অ্যাকাউন্টের তথ্য:</b>\n\n"
            f"🆔 <b>আপনার আইডি:</b> <code>{user_id}</code>\n"
            f"📅 <b>যোগদানের তারিখ:</b> {join_date}\n"
            f"📊 <b>প্রাপ্ত কোড:</b> {activations}\n"
            f"🌐 <b>ভাষা:</b> বাংলা\n\n"
            f"💰 <b>আয়ের তথ্য:</b>\n"
            f"├ 💵 বর্তমান ব্যালেন্স: <b>${format_decimal(balance)}</b>\n"
            f"├ 📈 মোট আয়: <b>${format_decimal(total_earned)}</b>\n"
            f"├ 👥 রেফারেল সংখ্যা: <b>{referrals_count}</b>\n"
            f"└ ✅ সক্রিয় রেফারেল: <b>{active_referrals}</b>\n\n"
            f"🔗 <b>রেফারেল লিংক:</b>\n<code>{referral_link}</code>\n\n"
            f"💡 <b>আপনার নম্বরের অবস্থা:</b>\n{number_status}"
        )
    else:
        account_text = (
            f"👤 <b>Your Account Info:</b>\n\n"
            f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
            f"📅 <b>Join Date:</b> {join_date}\n"
            f"📊 <b>Codes Received:</b> {activations}\n"
            f"🌐 <b>Language:</b> English\n\n"
            f"💰 <b>Earnings Info:</b>\n"
            f"├ 💵 Current Balance: <b>${format_decimal(balance)}</b>\n"
            f"├ 📈 Total Earned: <b>${format_decimal(total_earned)}</b>\n"
            f"├ 👥 Total Referrals: <b>{referrals_count}</b>\n"
            f"└ ✅ Active Referrals: <b>{active_referrals}</b>\n\n"
            f"🔗 <b>Referral Link:</b>\n<code>{referral_link}</code>\n\n"
            f"💡 <b>Number Status:</b>\n{number_status}"
        )
    
    markup = InlineKeyboardMarkup(row_width=1)
    if balance >= load_referral_settings().get("min_withdrawal", 5.0):
        withdraw_text = "💰 ব্যালেন্স উত্তোলন" if lang == "ar" else "💰 Withdraw"
        markup.add(InlineKeyboardButton(withdraw_text, callback_data="withdraw_balance"))
    
    back_text = "🔙 ফিরে যান" if lang == "ar" else "🔙 Back"
    markup.add(InlineKeyboardButton(back_text, callback_data="back_to_main"))
    
    bot.send_message(msg.chat.id, account_text, parse_mode="HTML", reply_markup=markup)

@bot.message_handler(commands=["help"])
def help_command(msg):
    user_id = msg.from_user.id
    
    if is_banned(user_id):
        bot.reply_to(msg, t(user_id, "banned"))
        return
    
    if msg.chat.type != "private":
        return
    
    lang = get_user_language(user_id)
    settings = load_referral_settings()
    code_bonus = settings.get("code_bonus", 0.01)
    referral_bonus = settings.get("referral_bonus", 0.50)
    codes_required = settings.get("codes_required_for_referral", 3)
    min_withdrawal = settings.get("min_withdrawal", 5.0)
    
    if lang == 'ar':
        instructions_text = f"""📖 <b>বট ব্যবহারের গাইড</b>

━━━━━━ <b>📱 কোড গ্রহণ</b> ━━━━━━

1️⃣ <b>দেশ বাছাই:</b>
   • চাপুন "Get Number"
   • আপনার পছন্দের দেশ বেছে নিন

2️⃣ <b>নম্বর বাছাই:</b>
   • উপলব্ধ নম্বরগুলো দেখানো হবে
   • উপযুক্ত নম্বর বেছে নিন

3️⃣ <b>কোড গ্রহণ:</b>
   • যেকোনো সাইট/অ্যাপে রেজিস্ট্রেশনে নম্বরটি ব্যবহার করুন
   • কোড স্বয়ংক্রিয়ভাবে এই বটে আসবে

━━━━━━ <b>💰 আয়ের সিস্টেম</b> ━━━━━━

💎 <b>কোড বোনাস:</b>
   • আপনি পাবেন <b>${format_decimal(code_bonus)}</b> প্রতিটি কোড পেলে

👥 <b>রেফারেল বোনাস:</b>
   • রেফারেল লিংক বন্ধুদের সাথে শেয়ার করুন
   • যখন আপনার বন্ধু পাবে <b>{codes_required} কোড</b>
   • আপনি পাবেন <b>${format_decimal(referral_bonus)}</b> সরাসরি!

━━━━━━ <b>💵 উত্তোলন</b> ━━━━━━

💰 <b>সর্বনিম্ন:</b> ${format_decimal(min_withdrawal)}
📝 <b>উত্তোলনের পদ্ধতি:</b>
   • ভোডাফোন ক্যাশ
   • USDT (TRC20/BEP20)
   • Binance ID

━━━━━━ আপনার বিশ্বাসের জন্য ধন্যবাদ ━━━━━━

🆘 সাহায্যের জন্য ডেভেলপারের সাথে যোগাযোগ করুন"""
    else:
        instructions_text = f"""📖 <b>Bot Guide</b>

━━━━━━ <b>📱 Receiving Codes</b> ━━━━━━

1️⃣ <b>Choose Country:</b>
   • Click on "Get Number"
   • Select your desired country

2️⃣ <b>Choose Number:</b>
   • Available numbers will appear
   • Select the number you want

3️⃣ <b>Receive Code:</b>
   • Use the number to register on any site/app
   • The code will arrive automatically here in the bot

━━━━━━ <b>💰 Earning System</b> ━━━━━━

💎 <b>Code Bonus:</b>
   • Earn <b>${format_decimal(code_bonus)}</b> for each code you receive

👥 <b>Referral Bonus:</b>
   • Share your referral link with friends
   • When your friend receives <b>{codes_required} codes</b>
   • You get <b>${format_decimal(referral_bonus)}</b> instantly!

━━━━━━ <b>💵 Withdrawal</b> ━━━━━━

💰 <b>Minimum:</b> ${format_decimal(min_withdrawal)}
📝 <b>Withdrawal Methods:</b>
   • Vodafone Cash
   • USDT (TRC20/BEP20)
   • Binance ID

━━━━━━ Thanks for your trust ━━━━━━

🆘 For help, contact the developer"""
    
    markup = InlineKeyboardMarkup(row_width=1)
    developer_btn_text = "🆘 Contact eloper" if lang == "en" else "🆘 ডেভেলপারের সাথে যোগাযোগ"
    markup.add(InlineKeyboardButton(developer_btn_text, url="https://t.me/alorhawa"))
    markup.add(InlineKeyboardButton(t(user_id, "back"), callback_data="back_to_main_user"))
    
    bot.send_message(msg.chat.id, instructions_text, parse_mode="HTML", reply_markup=markup)

@bot.message_handler(commands=["withdraw"])
def withdraw_command(msg):
    user_id = msg.from_user.id
    
    if is_banned(user_id):
        bot.reply_to(msg, t(user_id, "banned"))
        return
    
    if msg.chat.type != "private":
        return
    
    if not check_subscription(user_id):
        unjoined_channel = get_first_unjoined_channel(user_id)
        if unjoined_channel:
            bot.send_message(
                msg.chat.id,
                get_subscription_message_for_channel(unjoined_channel, user_id),
                parse_mode="HTML",
                reply_markup=get_single_channel_keyboard(unjoined_channel, user_id)
            )
        return
    
    lang = get_user_language(user_id)
    referral_data = get_user_referral_data(user_id)
    balance = referral_data.get("balance", 0.0)
    settings = load_referral_settings()
    min_withdrawal = settings.get("min_withdrawal", 5.0)
    
    if balance < min_withdrawal:
        if lang == "ar":
            msg_text = f"❌ আপনার ব্যালেন্স (${format_decimal(balance)}) সর্বনিম্ন উত্তোলনের চেয়ে কম (${format_decimal(min_withdrawal)})"
        else:
            msg_text = f"❌ Your balance (${format_decimal(balance)}) is below minimum withdrawal (${format_decimal(min_withdrawal)})"
        bot.send_message(msg.chat.id, msg_text, parse_mode="HTML")
        return
    
    user_states[user_id] = {"action": "withdraw_method"}
    
    methods = load_withdrawal_methods()
    markup = InlineKeyboardMarkup(row_width=2)
    
    method_icons = {"vodafone": "💳", "usdt_trc20": "📱", "usdt_bep20": "🔗", "binance_id": "🅱️"}
    
    for method_key, method_data in methods.items():
        if method_data.get("enabled", True):
            name = method_data.get(f"name_{lang}", method_data.get("name_en", method_key))
            icon = method_icons.get(method_key, "💰")
            markup.add(InlineKeyboardButton(f"{icon} {name}", callback_data=f"wd_method_{method_key}"))
    
    back_text = "🔙 ফিরে যান" if lang == "ar" else "🔙 Back"
    markup.add(InlineKeyboardButton(back_text, callback_data="my_account"))
    
    if lang == "ar":
        text = f"💰 <b>ব্যালেন্স উত্তোলন</b>\n\n💵 আপনার বর্তমান ব্যালেন্স: <b>${format_decimal(balance)}</b>\n\nউত্তোলনের পদ্ধতি বেছে নিন:"
    else:
        text = f"💰 <b>Withdraw Balance</b>\n\n💵 Your balance: <b>${format_decimal(balance)}</b>\n\nChoose withdrawal method:"
    
    bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=markup)

@bot.message_handler(commands=["hom"])
def hom_command(msg):
    user_id = msg.from_user.id
    
    if is_banned(user_id):
        bot.reply_to(msg, t(user_id, "banned"))
        return
    
    if msg.chat.type != "private":
        return
    
    text = t(user_id, "welcome")
    if not text: text = "🌐 <b>স্বাগতম!</b>"
    bot.send_message(
        msg.chat.id,
        text,
        parse_mode="HTML",
        reply_markup=get_main_menu_lang(user_id)
    )

@bot.message_handler(commands=["language"])
def language_command(msg):
    user_id = msg.from_user.id
    
    if is_banned(user_id):
        bot.reply_to(msg, t(user_id, "banned"))
        return
    
    if msg.chat.type != "private":
        return
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🇧🇩 বাংলা", callback_data="set_lang_ar", style="success"),
        InlineKeyboardButton("🇬🇧 English", callback_data="set_lang_en", style="primary")
    )
    
    bot.send_message(
        msg.chat.id,
        "🌍 <b>Choose Language / ভাষা বেছে নিন</b>",
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.message_handler(commands=["bonus"])
def bonus_command(msg):
    user_id = msg.from_user.id
    
    if is_banned(user_id):
        bot.reply_to(msg, t(user_id, "banned"))
        return
    
    if msg.chat.type != "private":
        return
    
    lang = get_user_language(user_id)
    settings = load_referral_settings()
    code_bonus = settings.get("code_bonus", 0.01)
    referral_bonus = settings.get("referral_bonus", 0.50)
    codes_required = settings.get("codes_required_for_referral", 3)
    min_withdrawal = settings.get("min_withdrawal", 5.0)
    
    referral_data = get_user_referral_data(user_id)
    balance = referral_data.get("balance", 0.0)
    total_earned = referral_data.get("total_earned", 0.0)
    referrals_count = len(referral_data.get("referrals", []))
    active_referrals = referral_data.get("active_referrals", 0)
    
    bot_info = bot.get_me()
    referral_link = f"https://t.me/{bot_info.username}?start=ref_{user_id}"
    
    if lang == "ar":
        bonus_text = f"""💰 <b>বোনাস সিস্টেম</b>

━━━━━━ <b>📊 আপনার পরিসংখ্যান</b> ━━━━━━

💵 বর্তমান ব্যালেন্স: <b>${format_decimal(balance)}</b>
📈 মোট আয়: <b>${format_decimal(total_earned)}</b>
👥 রেফারেল সংখ্যা: <b>{referrals_count}</b>
✅ সক্রিয় রেফারেল: <b>{active_referrals}</b>

━━━━━━ <b>🎁 বোনাসের হার</b> ━━━━━━

💎 কোড বোনাস: <b>${format_decimal(code_bonus)}</b> প্রতি কোডে
👥 রেফারেল বোনাস: <b>${format_decimal(referral_bonus)}</b> যখন {codes_required} কোড
💰 সর্বনিম্ন উত্তোলন: <b>${format_decimal(min_withdrawal)}</b>

━━━━━━ <b>🔗 রেফারেল লিংক</b> ━━━━━━

<code>{referral_link}</code>

বোনাস পেতে লিংক বন্ধুদের সাথে শেয়ার করুন!"""
    else:
        bonus_text = f"""💰 <b>Bonus System</b>

━━━━━━ <b>📊 Your Stats</b> ━━━━━━

💵 Current Balance: <b>${format_decimal(balance)}</b>
📈 Total Earned: <b>${format_decimal(total_earned)}</b>
👥 Total Referrals: <b>{referrals_count}</b>
✅ Active Referrals: <b>{active_referrals}</b>

━━━━━━ <b>🎁 Bonus Rates</b> ━━━━━━

💎 Code Bonus: <b>${format_decimal(code_bonus)}</b> per code
👥 Referral Bonus: <b>${format_decimal(referral_bonus)}</b> after {codes_required} codes
💰 Min Withdrawal: <b>${format_decimal(min_withdrawal)}</b>

━━━━━━ <b>🔗 Referral Link</b> ━━━━━━

<code>{referral_link}</code>

Share this link with friends to earn bonus!"""
    
    markup = InlineKeyboardMarkup(row_width=1)
    share_text = "📤 Share Link" if lang == "en" else "📤 লিংক শেয়ার"
    share_url = f"https://t.me/share/url?url={referral_link}"
    markup.add(InlineKeyboardButton(share_text, url=share_url))
    
    bot.send_message(msg.chat.id, bonus_text, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("set_lang_"))
def set_language_callback(call):
    user_id = call.from_user.id
    lang = call.data.replace("set_lang_", "")
    
    set_user_language(user_id, lang)
    
    pending_referrer = None
    if str(user_id) not in USERS:
        USERS[str(user_id)] = {"selected_country": None, "selected_number": None, "language": lang, "activations": 0, "join_date": datetime.now().strftime('%Y-%m-%d')}
    else:
        pending_referrer = USERS[str(user_id)].get("pending_referrer")
        USERS[str(user_id)]["language"] = lang
        if "activations" not in USERS[str(user_id)]:
            USERS[str(user_id)]["activations"] = 0
        if "join_date" not in USERS[str(user_id)]:
            USERS[str(user_id)]["join_date"] = datetime.now().strftime('%Y-%m-%d')
        if pending_referrer:
            del USERS[str(user_id)]["pending_referrer"]
    save_users()
    
    if pending_referrer:
        if process_referral(user_id, pending_referrer):
            try:
                referrer_lang = get_user_language(pending_referrer)
                settings = load_referral_settings()
                referral_bonus = settings.get("referral_bonus", 0.50)
                codes_required = settings.get("codes_required_for_referral", 3)
                
                user_name = call.from_user.first_name or "ইউজার"
                
                if referrer_lang == "ar":
                    notify_msg = (
                        f"🎉 <b>নতুন রেফারেল!</b>\n\n"
                        f"👤 ইউজার: <b>{user_name}</b>\n"
                        f"🆔 ID: <code>{user_id}</code>\n\n"
                        f"💰 <b>সম্ভাব্য আয়:</b> ${referral_bonus:.2f}\n"
                        f"📊 পৌঁছালে {codes_required} কোড হলে রেফারেল সক্রিয় হবে!"
                    )
                else:
                    notify_msg = (
                        f"🎉 <b>New Referral!</b>\n\n"
                        f"👤 User: <b>{user_name}</b>\n"
                        f"🆔 ID: <code>{user_id}</code>\n\n"
                        f"💰 <b>Expected Profit:</b> ${referral_bonus:.2f}\n"
                        f"📊 Referral becomes active after {codes_required} codes!"
                    )
                bot.send_message(pending_referrer, notify_msg, parse_mode="HTML")
            except Exception as e:
                print(f"Error sending referral notification: {e}")
            try:
                bot.send_message(user_id, t(user_id, "referral_success"), parse_mode="HTML")
            except:
                pass
    
    bot.delete_message(call.message.chat.id, call.message.message_id)
    
    if not check_subscription(user_id):
        unjoined_channel = get_first_unjoined_channel(user_id)
        if unjoined_channel:
            bot.send_message(
                call.message.chat.id,
                get_subscription_message(unjoined_channel, user_id),
                parse_mode="HTML",
                reply_markup=get_single_channel_keyboard(unjoined_channel)
            )
        return
    
    if is_admin(user_id):
        admin_markup = get_admin_menu()
        bot.send_message(
            call.message.chat.id,
            "🎛 <b>অ্যাডমিন প্যানেল</b>\n\nপ্রয়োজনীয় অপশন বেছে নিন:",
            parse_mode="HTML",
            reply_markup=admin_markup
        )
    
    settings = load_referral_settings()
    code_bonus = settings.get("code_bonus", 0.01)
    
    markup = get_country_buttons(user_id)
    if markup:
        if lang == "ar":
            title = f"<tg-emoji emoji-id='5972277098830634724'>🚨</tg-emoji> <b>প্ল্যাটফর্ম বেছে নিন</b>\n\n<tg-emoji emoji-id='6046356449938905522'>💰</tg-emoji> আপনি পাবেন <b>${format_decimal(code_bonus)}</b> প্রতিটি কোড পেলে!"
        else:
            title = f"<tg-emoji emoji-id='5972277098830634724'>🚨</tg-emoji> <b>Select Country</b>\n\n💰 You'll earn <b>${format_decimal(code_bonus)}</b> for each code received!"
        
        bot.send_message(
            call.message.chat.id,
            title,
            parse_mode="HTML",
            reply_markup=markup
        )
    else:
        text = t(user_id, "welcome")
        if not text: text = "🌐 <b>স্বাগতম!</b>"
        bot.send_message(
            call.message.chat.id,
            text,
            parse_mode="HTML",
            reply_markup=get_main_menu_lang(user_id)
        )

@bot.callback_query_handler(func=lambda call: call.data == "show_instructions")
def show_instructions_callback(call):
    user_id = call.from_user.id
    lang = get_user_language(user_id)
    
    settings = load_referral_settings()
    code_bonus = settings.get("code_bonus", 0.01)
    referral_bonus = settings.get("referral_bonus", 0.50)
    codes_required = settings.get("codes_required_for_referral", 3)
    min_withdrawal = settings.get("min_withdrawal", 5.0)
    
    if lang == 'ar':
        instructions_text = f"""📖 <b>বট ব্যবহারের গাইড</b>

━━━━━━ <b>📱 কোড গ্রহণ</b> ━━━━━━

1️⃣ <b>দেশ বাছাই:</b>
   • চাপুন "Get Number"
   • আপনার পছন্দের দেশ বেছে নিন

2️⃣ <b>নম্বর বাছাই:</b>
   • উপলব্ধ নম্বরগুলো দেখানো হবে
   • উপযুক্ত নম্বর বেছে নিন

3️⃣ <b>কোড গ্রহণ:</b>
   • যেকোনো সাইট/অ্যাপে রেজিস্ট্রেশনে নম্বরটি ব্যবহার করুন
   • কোড স্বয়ংক্রিয়ভাবে এই বটে আসবে

━━━━━━ <b>💰 আয়ের সিস্টেম</b> ━━━━━━

💎 <b>কোড বোনাস:</b>
   • আপনি পাবেন <b>${format_decimal(code_bonus)}</b> প্রতিটি কোড পেলে

👥 <b>রেফারেল বোনাস:</b>
   • রেফারেল লিংক বন্ধুদের সাথে শেয়ার করুন
   • যখন আপনার বন্ধু পাবে <b>{codes_required} কোড</b>
   • আপনি পাবেন <b>${referral_bonus:.2f}</b> সরাসরি!

━━━━━━ <b>💵 উত্তোলন</b> ━━━━━━

💰 <b>সর্বনিম্ন:</b> ${min_withdrawal:.2f}
📝 <b>উত্তোলনের পদ্ধতি:</b>
   • ভোডাফোন ক্যাশ
   • USDT (TRC20/BEP20)
   • Binance ID

⚡ <b>উত্তোলনের ধাপ:</b>
   1. যান "আমার অ্যাকাউন্ট"
   2. চাপুন "ব্যালেন্স উত্তোলন"
   3. উত্তোলনের পদ্ধতি বেছে নিন
   4. আপনার তথ্য দিন
   5. 24 ঘণ্টার মধ্যে পাঠানো হবে

━━━━━━ <b>📋 নোট</b> ━━━━━━

⏰ সাইটে যাচাই চাওয়ার পর কোডের অপেক্ষা করুন
🔄 আপনি যেকোনো সময় নম্বর বদলাতে পারেন
✅ আয় স্বয়ংক্রিয়ভাবে ব্যালেন্সে যোগ হয়

━━━━━━ আপনার বিশ্বাসের জন্য ধন্যবাদ ━━━━━━

🆘 সাহায্যের জন্য ডেভেলপারের সাথে যোগাযোগ করুন"""
    else:
        instructions_text = f"""📖 <b>Bot Guide</b>

━━━━━━ <b>📱 Receiving Codes</b> ━━━━━━

1️⃣ <b>Choose Country:</b>
   • Click on "Get Number"
   • Select your desired country

2️⃣ <b>Choose Number:</b>
   • Available numbers will appear
   • Select the number you want

3️⃣ <b>Receive Code:</b>
   • Use the number to register on any site/app
   • The code will arrive automatically here in the bot

━━━━━━ <b>💰 Earning System</b> ━━━━━━

💎 <b>Code Bonus:</b>
   • Earn <b>${format_decimal(code_bonus)}</b> for each code you receive

👥 <b>Referral Bonus:</b>
   • Share your referral link with friends
   • When your friend receives <b>{codes_required} codes</b>
   • You get <b>${referral_bonus:.2f}</b> instantly!

━━━━━━ <b>💵 Withdrawal</b> ━━━━━━

💰 <b>Minimum:</b> ${min_withdrawal:.2f}
📝 <b>Withdrawal Methods:</b>
   • Vodafone Cash
   • USDT (TRC20/BEP20)
   • Binance ID

⚡ <b>How to Withdraw:</b>
   1. Go to "My Account"
   2. Click "Withdraw Balance"
   3. Choose withdrawal method
   4. Enter your details
   5. Transfer within 24 hours

━━━━━━ <b>📋 Notes</b> ━━━━━━

⏰ Wait for code after verification request from the site
🔄 You can change the number anytime
✅ Earnings are added automatically

━━━━━━ Thanks for your trust ━━━━━━

🆘 For help, contact the developer"""
    
    markup = InlineKeyboardMarkup(row_width=1)
    eloper_btn_text = "🆘 Contact eloper" if get_user_language(user_id) == "en" else "🆘 ডেভেলপারের সাথে যোগাযোগ"
    markup.add(
        InlineKeyboardButton(eloper_btn_text, url="https://t.me/alorhawa")
    )
    markup.add(
        InlineKeyboardButton(t(user_id, "back"), callback_data="back_to_main_user")
    )
    
    bot.edit_message_text(
        instructions_text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "my_account")
def my_account_callback(call):
    user_id = call.from_user.id
    
    user_data = USERS.get(str(user_id), {})
    activations = user_data.get("activations", 0)
    join_date = user_data.get("join_date", datetime.now().strftime('%Y-%m-%d'))
    lang = get_user_language(user_id)
    
    referral_data = get_user_referral_data(user_id)
    balance = referral_data.get("balance", 0.0)
    total_earned = referral_data.get("total_earned", 0.0)
    referrals_count = len(referral_data.get("referrals", []))
    active_referrals = referral_data.get("active_referrals", 0)
    codes_received_bonus = referral_data.get("codes_received", 0)
    
    selected_country = user_data.get("selected_country")
    selected_number = user_data.get("selected_number")
    
    if selected_number and selected_country:
        number_status = f"✅ সক্রিয় নম্বর: {selected_country}" if lang == "ar" else f"✅ Active number for {selected_country}"
    else:
        number_status = "❌ এখন কোনো নম্বর নেই" if lang == "ar" else "❌ No number currently"
    
    bot_info = bot.get_me()
    referral_link = f"https://t.me/{bot_info.username}?start=ref_{user_id}"
    
    if lang == "ar":
        account_text = (
            f"👤 <b>আপনার অ্যাকাউন্টের তথ্য:</b>\n\n"
            f"🆔 <b>আপনার আইডি:</b> <code>{user_id}</code>\n"
            f"📅 <b>যোগদানের তারিখ:</b> {join_date}\n"
            f"📊 <b>প্রাপ্ত কোড:</b> {activations}\n"
            f"🌐 <b>ভাষা:</b> বাংলা\n\n"
            f"💰 <b>আয়ের তথ্য:</b>\n"
            f"├ 💵 বর্তমান ব্যালেন্স: <b>${balance:.2f}</b>\n"
            f"├ 📈 মোট আয়: <b>${total_earned:.2f}</b>\n"
            f"├ 👥 রেফারেল সংখ্যা: <b>{referrals_count}</b>\n"
            f"└ ✅ সক্রিয় রেফারেল: <b>{active_referrals}</b>\n\n"
            f"🔗 <b>রেফারেল লিংক:</b>\n<code>{referral_link}</code>\n\n"
            f"💡 <b>আপনার নম্বরের অবস্থা:</b>\n{number_status}"
        )
    else:
        account_text = (
            f"👤 <b>Your Account Info:</b>\n\n"
            f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
            f"📅 <b>Join Date:</b> {join_date}\n"
            f"📊 <b>Codes Received:</b> {activations}\n"
            f"🌐 <b>Language:</b> English\n\n"
            f"💰 <b>Earnings Info:</b>\n"
            f"├ 💵 Current Balance: <b>${balance:.2f}</b>\n"
            f"├ 📈 Total Earned: <b>${total_earned:.2f}</b>\n"
            f"├ 👥 Total Referrals: <b>{referrals_count}</b>\n"
            f"└ ✅ Active Referrals: <b>{active_referrals}</b>\n\n"
            f"🔗 <b>Referral Link:</b>\n<code>{referral_link}</code>\n\n"
            f"💡 <b>Number Status:</b>\n{number_status}"
        )
    
    copy_link_text = " রেফারেল লিংক কপি" if lang == "ar" else " Copy Referral Link"
    share_link_text = "📤 লিংক শেয়ার" if lang == "ar" else "📤 Share Link"
    share_url = f"https://t.me/share/url?url={referral_link}&text={'রেফারেল লিংকের মাধ্যমে জয়েন করুন!' if lang == 'ar' else 'Join via my referral link!'}"
    
    keyboard_rows = []
    
    if balance >= load_referral_settings().get("min_withdrawal", 5.0):
        withdraw_text = "💰 ব্যালেন্স উত্তোলন" if lang == "ar" else "💰 Withdraw"
        keyboard_rows.append([{"text": withdraw_text, "callback_data": "withdraw_balance"}])
    
    bonus_info_text = "📖 বোনাস ও রেফারেল সিস্টেম" if lang == "ar" else "📖 Bonus & Referral System"
    keyboard_rows.append([{"text": bonus_info_text, "callback_data": "bonus_info"}])
    
    keyboard_rows.append([
        {"text": copy_link_text, "copy_text": {"text": referral_link}},
        {"text": share_link_text, "url": share_url}
    ])
    
    keyboard_rows.append([{"text": t(user_id, "change_language"), "callback_data": "change_lang"}])
    keyboard_rows.append([{"text": t(user_id, "back"), "callback_data": "back_to_main_user"}])
    
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
        resp = requests.post(url, json={
            "chat_id": call.message.chat.id,
            "message_id": call.message.message_id,
            "text": account_text,
            "parse_mode": "HTML",
            "reply_markup": {"inline_keyboard": keyboard_rows}
        }, timeout=10)
    except:
        markup = InlineKeyboardMarkup(row_width=2)
        if balance >= load_referral_settings().get("min_withdrawal", 5.0):
            withdraw_text = "💰 ব্যালেন্স উত্তোলন" if lang == "ar" else "💰 Withdraw"
            markup.add(InlineKeyboardButton(withdraw_text, callback_data="withdraw_balance"))
        markup.add(InlineKeyboardButton(bonus_info_text, callback_data="bonus_info"))
        markup.add(InlineKeyboardButton(t(user_id, "change_language"), callback_data="change_lang"))
        markup.add(InlineKeyboardButton(t(user_id, "back"), callback_data="back_to_main_user"))
        bot.edit_message_text(account_text, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "bonus_info")
def bonus_info_callback(call):
    user_id = call.from_user.id
    lang = get_user_language(user_id)
    settings = load_referral_settings()
    
    code_bonus = settings.get("code_bonus", 0.01)
    referral_bonus = settings.get("referral_bonus", 0.50)
    codes_required = settings.get("codes_required_for_referral", 3)
    min_withdrawal = settings.get("min_withdrawal", 5.0)
    
    if lang == "ar":
        info_text = (
            "📖 <b>বোনাস ও রেফারেল সিস্টেম</b>\n\n"
            "━━━━━━ <b>কীভাবে আয় করবেন?</b> ━━━━━━\n\n"
            f"💎 <b>কোড বোনাস:</b>\n"
            f"   • আপনি পাবেন <b>${format_decimal(code_bonus)}</b> প্রতিটি কোড পেলে\n\n"
            f"👥 <b>রেফারেল বোনাস:</b>\n"
            f"   • রেফারেল লিংক বন্ধুদের সাথে শেয়ার করুন\n"
            f"   • যখন কোনো বন্ধু আপনার লিংকে জয়েন করে\n"
            f"   • এবং পায় <b>{codes_required} কোড</b>\n"
            f"   • আপনি পাবেন <b>${referral_bonus:.2f}</b> সরাসরি!\n\n"
            "━━━━━━ <b>উত্তোলন</b> ━━━━━━\n\n"
            f"💰 <b>সর্বনিম্ন উত্তোলন:</b> ${min_withdrawal:.2f}\n"
            "📝 <b>উপলব্ধ উত্তোলনের পদ্ধতি:</b>\n"
            "   • ভোডাফোন ক্যাশ\n"
            "   • USDT (TRC20/BEP20)\n"
            "   • Binance ID\n\n"
            "━━━━━━ <b>গুরুত্বপূর্ণ নোট</b> ━━━━━━\n\n"
            "✅ আয় স্বয়ংক্রিয়ভাবে ব্যালেন্সে যোগ হয়\n"
            "✅ আপনার অ্যাকাউন্ট পেজ থেকে রেফারেল ট্র্যাক করতে পারবেন\n"
            "✅ উত্তোলনের অনুরোধ 24 ঘণ্টার মধ্যে প্রসেস হয়"
        )
    else:
        info_text = (
            "📖 <b>Bonus & Referral System</b>\n\n"
            "━━━━━━ <b>How to Earn?</b> ━━━━━━\n\n"
            f"💎 <b>Code Bonus:</b>\n"
            f"   • Get <b>${format_decimal(code_bonus)}</b> for each code you receive\n\n"
            f"👥 <b>Referral Bonus:</b>\n"
            f"   • Share your referral link with friends\n"
            f"   • When a friend joins via your link\n"
            f"   • And receives <b>{codes_required} codes</b>\n"
            f"   • You get <b>${referral_bonus:.2f}</b> instantly!\n\n"
            "━━━━━━ <b>Withdrawal</b> ━━━━━━\n\n"
            f"💰 <b>Minimum Withdrawal:</b> ${min_withdrawal:.2f}\n"
            "📝 <b>Available Methods:</b>\n"
            "   • Vodafone Cash\n"
            "   • USDT (TRC20/BEP20)\n"
            "   • Binance ID\n\n"
            "━━━━━━ <b>Important Notes</b> ━━━━━━\n\n"
            "✅ Earnings are added automatically to your balance\n"
            "✅ Track your referrals from your account page\n"
            "✅ Withdrawal requests are processed within 24 hours"
        )
    
    markup = InlineKeyboardMarkup()
    back_text = "🔙 ফিরে যান" if lang == "ar" else "🔙 Back"
    markup.add(InlineKeyboardButton(back_text, callback_data="my_account"))
    
    bot.edit_message_text(
        info_text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "change_lang")
def change_language_callback(call):
    user_id = call.from_user.id
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🇧🇩 বাংলা", callback_data="set_lang_ar", style="success"),
        InlineKeyboardButton("🇬🇧 English", callback_data="set_lang_en", style="primary")
    )
    
    bot.edit_message_text(
        "🌍 <b>ভাষা বেছে নিন / Choose Language</b>",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "back_to_main_user")
def back_to_main_user_callback(call):
    user_id = call.from_user.id
    lang = get_user_language(user_id)
    settings = load_referral_settings()
    code_bonus = settings.get("code_bonus", 0.01)
    
    markup = get_country_buttons(user_id)
    if markup:
        if lang == "ar":
            title = f"<tg-emoji emoji-id='5972277098830634724'>🚨</tg-emoji> <b>প্ল্যাটফর্ম বেছে নিন</b>\n\n<tg-emoji emoji-id='6046356449938905522'>💰</tg-emoji> আপনি পাবেন <b>${format_decimal(code_bonus)}</b> প্রতিটি কোড পেলে!"
        else:
            title = f"<tg-emoji emoji-id='5972277098830634724'>🚨</tg-emoji> <b>Select Country</b>\n\n💰 You'll earn <b>${format_decimal(code_bonus)}</b> for each code received!"
        
        try:
            bot.edit_message_text(
                title,
                call.message.chat.id,
                call.message.message_id,
                parse_mode="HTML",
                reply_markup=markup
            )
        except:
            pass
    else:
        try:
            text = t(user_id, "welcome")
            if not text: text = "🌐 <b>স্বাগতম!</b>"
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode="HTML",
                reply_markup=get_main_menu_lang(user_id)
            )
        except:
            pass

def get_single_channel_keyboard(channel, lang="ar"):
    markup = InlineKeyboardMarkup()
    btn_name = channel.get(f"name_{lang}", channel.get("name", "Join 🔗"))
    markup.add(InlineKeyboardButton(btn_name, url=channel['url']))
    
    verify_text = "✅ সাবস্ক্রিপশন যাচাই করুন"
    if lang == "en":
        verify_text = "✅ Verify Subscription"
    elif lang != "ar":
        verify_text = "✅ যাচাই / Verify"
        
    markup.add(InlineKeyboardButton(verify_text, callback_data="verify_subscription"))
    return markup

def get_subscription_message_for_channel(channel, user_id):
    lang = get_user_language(user_id)
    
    channel_name = channel.get(f"name_{lang}", channel.get("name", "Join 🔗"))
    
    if lang == "ar":
        return f"⚠️ <b>বট ব্যবহার করতে বটের চ্যানেলে সাবস্ক্রাইব করতে হবে।</b>\n\n📢 চ্যানেল: <b>{channel_name}</b>"
    else:
        return f"⚠️ <b>You must subscribe to the bot channel to use it.</b>\n\n📢 Channel: <b>{channel_name}</b>"

@bot.callback_query_handler(func=lambda call: call.data == "verify_subscription")
def verify_subscription_callback(call):
    user_id = call.from_user.id
    lang = get_user_language(user_id)
    
    unjoined_channel = get_first_unjoined_channel(user_id)
    
    if unjoined_channel:
        try:
            bot.edit_message_text(
                get_subscription_message_for_channel(unjoined_channel, user_id),
                call.message.chat.id,
                call.message.message_id,
                parse_mode="HTML",
                reply_markup=get_single_channel_keyboard(unjoined_channel, user_id)
            )
        except:
            pass
        
        if lang == "ar":
            bot.answer_callback_query(call.id, "❌ আগে চ্যানেলে জয়েন করুন!", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "❌ Join the channel first!", show_alert=True)
        return
    
    bot.delete_message(call.message.chat.id, call.message.message_id)

    if str(user_id) not in USERS:
        USERS[str(user_id)] = {"selected_country": None, "selected_number": None}
        save_users()

    settings = load_referral_settings()
    code_bonus = settings.get("code_bonus", 0.01)
    markup = get_country_buttons(user_id)
    
    if markup:
        if lang == "ar":
            title = f"📱 <b>প্ল্যাটফর্ম বেছে নিন</b>\n\n<tg-emoji emoji-id='6046356449938905522'>💰</tg-emoji> আপনি পাবেন <b>${format_decimal(code_bonus)}</b> প্রতিটি কোড পেলে!"
        else:
            title = f"🌍 <b>Select Country</b>\n\n<tg-emoji emoji-id='6046356449938905522'>💰</tg-emoji>You'll earn <b>${format_decimal(code_bonus)}</b> for each code received!"
        bot.send_message(call.message.chat.id, title, parse_mode="HTML", reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, t(user_id, "welcome"), parse_mode="HTML", reply_markup=get_main_menu_lang(user_id))

@bot.callback_query_handler(func=lambda call: call.data == "admin_panel")
def admin_panel_callback(call):
    user_id = call.from_user.id

    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "⛔️ এই প্যানেলে প্রবেশের অনুমতি আপনার নেই", show_alert=True)
        return

    bot.edit_message_text(
        "🎛 <b>অ্যাডমিন প্যানেল</b>\n\nপ্রয়োজনীয় অপশন বেছে নিন:",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=get_admin_menu()
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("na_add_country_srv_"))
def na_add_country_server_callback(call):
    user_id = call.from_user.id
    if not is_numbers_admin(user_id):
        return
    
    if user_id not in user_states or user_states[user_id].get("action") != "na_add_country_server":
        bot.answer_callback_query(call.id, "❌ সেশন শেষ হয়ে গেছে!", show_alert=True)
        return
    
    server = call.data.replace("na_add_country_srv_", "")
    state = user_states[user_id]
    
    user_states[user_id] = {
        "action": "na_add_country_platforms",
        "numbers_file": state.get("numbers_file"),
        "country_code": state.get("country_code"),
        "country_name": state.get("country_name"),
        "num_cleaned": state.get("num_cleaned"),
        "server": server,
        "selected_platforms": []
    }
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📘 Facebook", callback_data="na_add_country_plt_Facebook", style="primary"),
        InlineKeyboardButton("💬 WhatsApp", callback_data="na_add_country_plt_WhatsApp", style="success")
    )
    markup.add(
        InlineKeyboardButton("✈️ Telegram", callback_data="na_add_country_plt_Telegram", style="primary"),
        InlineKeyboardButton("📸 Instagram", callback_data="na_add_country_plt_Instagram", style="danger")
    )
    markup.add(
        InlineKeyboardButton("🐦 Twitter/X", callback_data="na_add_country_plt_Twitter", style="success"),
        InlineKeyboardButton("📱 TikTok", callback_data="na_add_country_plt_TikTok", style="danger")
    )
    markup.add(
        InlineKeyboardButton("🎮 Discord", callback_data="na_add_country_plt_Discord", style="primary"),
        InlineKeyboardButton("📧 Gmail", callback_data="na_add_country_plt_Gmail", style="success")
    )
    markup.add(
        InlineKeyboardButton("🌐 সব প্ল্যাটফর্ম", callback_data="na_add_country_plt_ALL", style="success")
    )
    markup.add(InlineKeyboardButton("✅ নিশ্চিত করুন ও শেষ করুন", callback_data="na_add_country_finish", style="success"))
    markup.add(InlineKeyboardButton("❌ বাতিল", callback_data="numbers_admin_panel", style="danger"))
    
    server_names = {
        "GROUP": "𝐒𝐞𝐫𝐯𝐞𝐫 𝟏",
        "Fly sms": "𝐒𝐞𝐫𝐯𝐞𝐫 𝟐",
        "Number_Panel": "𝐒𝐞𝐫𝐯𝐞𝐫 𝟑",
        "Bolt": "𝐒𝐞𝐫𝐯𝐞𝐫 𝟒",
        "iVASMS": "𝐒𝐞𝐫𝐯𝐞𝐫 𝟓",
        "MSI": "𝐒𝐞𝐫𝐯𝐞𝐫 𝟔",
        "proton SMS": "𝐒𝐞𝐫𝐯𝐞𝐫 𝟕"
    }
    
    bot.edit_message_text(
        f"✅ <b>ধাপ 5/5 - প্ল্যাটফর্ম বাছাই</b>\n\n"
        f"🌍 দেশ: <b>{state.get('country_name')}</b>\n"
        f"🔢 দেশের কোড: <b>{state.get('country_code')}</b>\n"
        f"🖥️ সার্ভার: <b>{server_names.get(server, server)}</b>\n\n"
        f"📱 <b>বাছাই করা প্ল্যাটফর্ম:</b> নেই\n\n"
        f"এই নম্বরগুলো যে প্ল্যাটফর্মে কাজ করে সেগুলো বেছে নিন:",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "na_add_country_edit_name")
def na_add_country_edit_name_callback(call):
    user_id = call.from_user.id
    if not is_numbers_admin(user_id):
        return
    
    lang = get_user_language(user_id)
    state = user_states.get(user_id)
    if not state:
        bot.answer_callback_query(call.id, "❌ সেশন শেষ হয়ে গেছে!", show_alert=True)
        return
    
    state["action"] = "na_add_country_edit_name_input"
    text = "📝 দেশের নতুন নাম পাঠান:" if lang == "ar" else "📝 Please send the new country name:"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("na_add_country_plt_"))
def na_add_country_platform_callback(call):
    user_id = call.from_user.id
    if not is_numbers_admin(user_id):
        return
    
    if user_id not in user_states or user_states[user_id].get("action") != "na_add_country_platforms":
        bot.answer_callback_query(call.id, "❌ সেশন শেষ হয়ে গেছে!", show_alert=True)
        return
    
    platform = call.data.replace("na_add_country_plt_", "")
    state = user_states[user_id]
    selected_platforms = state.get("selected_platforms", [])
    
    if platform == "ALL":
        selected_platforms = ["Facebook", "WhatsApp", "Telegram", "Instagram", "Twitter", "TikTok", "Discord", "Gmail"]
    elif platform in selected_platforms:
        selected_platforms.remove(platform)
    else:
        selected_platforms.append(platform)
    
    user_states[user_id]["selected_platforms"] = selected_platforms
    
    platform_icons = {
        "Facebook": "📘", "WhatsApp": "💬", "Telegram": "✈️",
        "Instagram": "📸", "Twitter": "🐦", "TikTok": "📱",
        "Discord": "🎮", "Gmail": "📧"
    }
    
    def get_btn_text(name, icon):
        check = "✅" if name in selected_platforms else ""
        return f"{check} {icon} {name}"
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(get_btn_text("Facebook", "📘"), callback_data="na_add_country_plt_Facebook"),
        InlineKeyboardButton(get_btn_text("WhatsApp", "💬"), callback_data="na_add_country_plt_WhatsApp")
    )
    markup.add(
        InlineKeyboardButton(get_btn_text("Telegram", "✈️"), callback_data="na_add_country_plt_Telegram"),
        InlineKeyboardButton(get_btn_text("Instagram", "📸"), callback_data="na_add_country_plt_Instagram")
    )
    markup.add(
        InlineKeyboardButton(get_btn_text("Twitter", "🐦"), callback_data="na_add_country_plt_Twitter"),
        InlineKeyboardButton(get_btn_text("TikTok", "📱"), callback_data="na_add_country_plt_TikTok")
    )
    markup.add(
        InlineKeyboardButton(get_btn_text("Discord", "🎮"), callback_data="na_add_country_plt_Discord"),
        InlineKeyboardButton(get_btn_text("Gmail", "📧"), callback_data="na_add_country_plt_Gmail")
    )
    markup.add(
        InlineKeyboardButton("🌐 সব প্ল্যাটফর্ম", callback_data="na_add_country_plt_ALL", style="success")
    )
    markup.add(InlineKeyboardButton("✅ নিশ্চিত করুন ও শেষ করুন", callback_data="na_add_country_finish", style="success"))
    markup.add(InlineKeyboardButton("❌ বাতিল", callback_data="numbers_admin_panel", style="danger"))
    
    
    platform_icons = {
        "Facebook": "📘", "WhatsApp": "💬", "Telegram": "✈️",
        "Instagram": "📸", "Twitter": "🐦", "TikTok": "📱",
        "Discord": "🎮", "Gmail": "📧"
    }
    
    platforms_text = ", ".join([f"{platform_icons.get(p, '📱')} {p}" for p in selected_platforms]) if selected_platforms else "নেই"
    
    bot.edit_message_text(
        f"✅ <b>ধাপ 5/5 - প্ল্যাটফর্ম বাছাই</b>\n\n"
        f"🌍 দেশ: <b>{state.get('country_name')}</b>\n"
        f"🔢 দেশের কোড: <b>{state.get('country_code')}</b>\n"
        f"📱 <b>বাছাই করা প্ল্যাটফর্ম:</b> {platforms_text}\n\n"
        f"এই নম্বরগুলো যে প্ল্যাটফর্মে কাজ করে সেগুলো বেছে নিন:",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "na_add_country_finish")
def na_add_country_finish_callback(call):
    user_id = call.from_user.id
    if not is_numbers_admin(user_id):
        return
    
    if user_id not in user_states or user_states[user_id].get("action") != "na_add_country_platforms":
        bot.answer_callback_query(call.id, "❌ সেশন শেষ হয়ে গেছে!", show_alert=True)
        return
    
    state = user_states[user_id]
    country_name = state.get("country_name")
    country_code = state.get("country_code")
    numbers_file = state.get("numbers_file")
    server = state.get("server")
    selected_platforms = state.get("selected_platforms", [])
    num_cleaned = state.get("num_cleaned", 0)
    
    if not selected_platforms:
        bot.answer_callback_query(call.id, "❌ কমপক্ষে একটি প্ল্যাটফর্ম বেছে নিতে হবে!", show_alert=True)
        return
    
    flag = get_flag_for_country_code(country_code)
    
    
    country_id = f"{country_name}_{uuid.uuid4().hex[:6]}"
    
    COUNTRIES[country_id] = {
        "display_name": country_name,
        "file": numbers_file,
        "code": country_code,
        "flag": flag,
        "server": server,
        "platforms": selected_platforms,
        "numbers_count": num_cleaned,
        "added_by": user_id,
        "added_at": datetime.now().isoformat()
    }
    save_countries()
    
    del user_states[user_id]
    
    server_names = {
        "GROUP": "𝐒𝐞𝐫𝐯𝐞𝐫 𝟏",
        "Fly sms": "𝐒𝐞𝐫𝐯𝐞𝐫 𝟐",
        "Number_Panel": "𝐒𝐞𝐫𝐯𝐞𝐫 𝟑",
        "Bolt": "𝐒𝐞𝐫𝐯𝐞𝐫 𝟒",
        "iVASMS": "𝐒𝐞𝐫𝐯𝐞𝐫 𝟓",
        "MSI": "𝐒𝐞𝐫𝐯𝐞𝐫 𝟔",
        "proton SMS": "𝐒𝐞𝐫𝐯𝐞𝐫 𝟕"
    }
    
    platforms_text = ", ".join(selected_platforms)
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("➕ আরেকটি দেশ যোগ করুন", callback_data="admin_add_country", style="success"),
        InlineKeyboardButton("📄 আরেকটি ফাইল যোগ করুন", callback_data="admin_add_country", style="success")
    )
    markup.add(InlineKeyboardButton("🔙 প্যানেলে ফিরুন", callback_data="admin_panel", style="danger"))
    
    bot.edit_message_text(
        f"✅ <b>দেশ সফলভাবে যোগ হয়েছে!</b>\n\n"
        f"🌍 দেশ: <b>{flag} {country_name}</b>\n"
        f"🔢 দেশের কোড: <b>{country_code}</b>\n"
        f"📊 নম্বরের সংখ্যা: <b>{num_cleaned}</b>\n"
        f"🖥️ সার্ভার: <b>{server_names.get(server, server)}</b>\n"
        f"📱 প্ল্যাটফর্ম: <b>{platforms_text}</b>",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

def get_flag_for_country_code(country_code):
    try:
       
        code_str = str(country_code).replace('+', '').strip()
        if not code_str.isdigit():
            return "🌍"
            
        import phonenumbers
        from phonenumbers.phonenumberutil import region_code_for_country_code
        
       
        region = region_code_for_country_code(int(code_str))
        if region and region != 'ZZ':
            return get_flag(region)
    except Exception as e:
        print(f"Error getting flag for code {country_code}: {e}")
        
    return "🌍"

@bot.callback_query_handler(func=lambda call: call.data == "na_list_countries")
def na_list_countries_callback(call):
    user_id = call.from_user.id
    if not is_numbers_admin(user_id):
        return
    
    if not COUNTRIES:
        text = "📋 <b>উপলব্ধ দেশসমূহ</b>\n\n❌ এখনো কোনো দেশ যোগ করা হয়নি!"
    else:
        text = "📋 <b>উপলব্ধ দেশসমূহ</b>\n\n"
        for idx, (country_name, info) in enumerate(sorted(COUNTRIES.items()), 1):
            flag = info.get("flag", "🌍")
            server = info.get("server", "N/A")
            platforms = info.get("platforms", [])
            platforms_count = len(platforms)
            text += f"{idx}. {flag} <b>{country_name}</b> - {server} ({platforms_count} প্ল্যাটফর্ম)\n"
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 ফিরে যান", callback_data="numbers_admin_panel", style="danger"))
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "na_ban_user")
def na_ban_user_callback(call):
    user_id = call.from_user.id
    if not is_numbers_admin(user_id):
        return
    
    user_states[user_id] = {"mode": "na_ban_user"}
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("❌ বাতিল", callback_data="numbers_admin_panel", style="danger"))
    
    bot.edit_message_text(
        "🚫 <b>ইউজার ব্যান</b>\n\n"
        "📝 ইউজারের আইডি পাঠান (ID) যাকে ব্যান করতে চান:",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "na_unban_user")
def na_unban_user_callback(call):
    user_id = call.from_user.id
    if not is_numbers_admin(user_id):
        return
    
    user_states[user_id] = {"mode": "na_unban_user"}
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("❌ বাতিল", callback_data="numbers_admin_panel", style="danger"))
    
    bot.edit_message_text(
        "✅ <b>ইউজার আনব্যান</b>\n\n"
        "📝 ইউজারের আইডি পাঠান (ID) যাকে আনব্যান করতে চান:",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "na_banned_list")
def na_banned_list_callback(call):
    user_id = call.from_user.id
    if not is_numbers_admin(user_id):
        return
    
    if not BANNED:
        text = "📊 <b>ব্যান করা ইউজারের তালিকা</b>\n\n✅ কোনো ব্যান করা ইউজার নেই!"
    else:
        text = "📊 <b>ব্যান করা ইউজারের তালিকা</b>\n\n"
        for idx, banned_id in enumerate(BANNED[:50], 1):
            text += f"{idx}. <code>{banned_id}</code>\n"
        if len(BANNED) > 50:
            text += f"\n... এবং {len(BANNED) - 50} আরও"
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 ফিরে যান", callback_data="numbers_admin_panel", style="danger"))
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_manage_numbers_admins")
def admin_manage_numbers_admins_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "⛔️ আপনার অনুমতি নেই!", show_alert=True)
        return
    
    text = "🧮 <b>নম্বর অ্যাডমিন ম্যানেজমেন্ট</b>\n\n"
    text += f"👥 নম্বর অ্যাডমিনের সংখ্যা: {len(NUMBERS_ADMINS)}\n\n"
    
    if NUMBERS_ADMINS:
        text += "<b>বর্তমান তালিকা:</b>\n"
        for idx, admin_id in enumerate(NUMBERS_ADMINS, 1):
            text += f"{idx}. <code>{admin_id}</code>\n"
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("➕ নম্বর অ্যাডমিন যোগ", callback_data="add_numbers_admin", style="success"),
        InlineKeyboardButton("➖ নম্বর অ্যাডমিন মুছুন", callback_data="remove_numbers_admin", style="danger")
    )
    markup.add(InlineKeyboardButton("🔙 ফিরে যান", callback_data="admin_panel", style="danger"))
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "add_numbers_admin")
def add_numbers_admin_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    user_states[user_id] = {"mode": "add_numbers_admin"}
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("❌ বাতিল", callback_data="admin_manage_numbers_admins", style="danger"))
    
    bot.edit_message_text(
        "➕ <b>নতুন নম্বর অ্যাডমিন যোগ</b>\n\n"
        "📝 ইউজারের আইডি পাঠান (User ID) যাকে নম্বর অ্যাডমিন বানাতে চান:",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "remove_numbers_admin")
def remove_numbers_admin_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    if not NUMBERS_ADMINS:
        bot.answer_callback_query(call.id, "❌ কোনো নম্বর অ্যাডমিন নেই!", show_alert=True)
        return
    
    markup = InlineKeyboardMarkup(row_width=1)
    for admin_id in NUMBERS_ADMINS:
        markup.add(
            InlineKeyboardButton(
                f"🗑 মুছুন {admin_id}",
                callback_data=f"del_numbers_admin_{admin_id}"
            )
        )
    markup.add(InlineKeyboardButton("🔙 ফিরে যান", callback_data="admin_manage_numbers_admins", style="danger"))
    
    bot.edit_message_text(
        "➖ <b>নম্বর অ্যাডমিন মুছুন</b>\n\n"
        "যে অ্যাডমিনকে মুছতে চান তাকে বেছে নিন:",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("del_numbers_admin_"))
def del_numbers_admin_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    admin_to_remove = int(call.data.replace("del_numbers_admin_", ""))
    
    if admin_to_remove in NUMBERS_ADMINS:
        NUMBERS_ADMINS.remove(admin_to_remove)
        save_numbers_admins()
        bot.answer_callback_query(call.id, f"✅ মুছে ফেলা হয়েছে {admin_to_remove} নম্বর অ্যাডমিন থেকে!", show_alert=True)
    else:
        bot.answer_callback_query(call.id, "❌ অ্যাডমিন পাওয়া যায়নি!", show_alert=True)
    
    admin_manage_numbers_admins_callback(call)

@bot.callback_query_handler(func=lambda call: call.data == "admin_statistics")
def admin_statistics_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    stats_text = get_statistics_text()
    bot.send_message(call.message.chat.id, stats_text, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == "admin_referral_settings")
def admin_referral_settings_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    settings = load_referral_settings()
    
    text = (
        "💰 <b>রেফারেল ও বোনাস সিস্টেম সেটিংস</b>\n\n"
        f"🎁 কোড বোনাস: <b>${settings.get('code_bonus', 0.01)}</b>\n"
        f"👥 রেফারেল বোনাস: <b>${settings.get('referral_bonus', 0.50)}</b>\n"
        f"📊 সক্রিয় রেফারেলের জন্য প্রয়োজনীয় কোড সংখ্যা: <b>{settings.get('codes_required_for_referral', 3)}</b>\n"
        f"💵 সর্বনিম্ন উত্তোলন: <b>${settings.get('min_withdrawal', 5.0)}</b>\n\n"
        "যে সেটিং এডিট করতে চান সেটি বেছে নিন:"
    )
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🎁 কোড বোনাস", callback_data="edit_code_bonus", style="success"),
        InlineKeyboardButton("👥 রেফারেল বোনাস", callback_data="edit_referral_bonus", style="primary")
    )
    markup.add(
        InlineKeyboardButton("📊 রেফারেল কোড", callback_data="edit_codes_required", style="success"),
        InlineKeyboardButton("💵 উত্তোলনের সীমা", callback_data="edit_min_withdrawal", style="primary")
    )
    markup.add(
        InlineKeyboardButton("➕ ইউজারকে ব্যালেন্স যোগ", callback_data="admin_add_balance", style="success"),
        InlineKeyboardButton("➖ ইউজারের ব্যালেন্স কর্তন", callback_data="admin_subtract_balance", style="danger")
    )
    markup.add(
        InlineKeyboardButton("📋 উত্তোলনের অনুরোধ", callback_data="view_withdrawal_requests", style="success"),
        InlineKeyboardButton("⚙️ উত্তোলনের পদ্ধতি", callback_data="admin_withdrawal_methods", style="primary")
    )
    markup.add(InlineKeyboardButton("🔙 ফিরে যান", callback_data="admin", style="danger"))
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "edit_code_bonus")
def edit_code_bonus_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    user_states[user_id] = {"action": "edit_code_bonus"}
    bot.send_message(
        call.message.chat.id,
        "🎁 <b>কোড বোনাস এডিট</b>\n\n"
        "নতুন মান পাঠান (উদাহরণ: 0.01 বা 0.02):",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == "edit_referral_bonus")
def edit_referral_bonus_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    user_states[user_id] = {"action": "edit_referral_bonus"}
    bot.send_message(
        call.message.chat.id,
        "👥 <b>রেফারেল বোনাস এডিট</b>\n\n"
        "নতুন মান পাঠান (উদাহরণ: 0.50 বা 1.00):",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == "edit_codes_required")
def edit_codes_required_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    user_states[user_id] = {"action": "edit_codes_required"}
    bot.send_message(
        call.message.chat.id,
        "📊 <b>প্রয়োজনীয় কোড সংখ্যা এডিট</b>\n\n"
        "নতুন সংখ্যা পাঠান (উদাহরণ: 3 বা 5):",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == "edit_min_withdrawal")
def edit_min_withdrawal_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    user_states[user_id] = {"action": "edit_min_withdrawal"}
    bot.send_message(
        call.message.chat.id,
        "💵 <b>সর্বনিম্ন উত্তোলন এডিট</b>\n\n"
        "নতুন মান পাঠান (উদাহরণ: 5.00 বা 10.00):",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_add_balance")
def admin_add_balance_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    user_states[user_id] = {"action": "admin_add_balance"}
    bot.send_message(
        call.message.chat.id,
        "➕ <b>ইউজারকে ব্যালেন্স যোগ</b>\n\n"
        "ইউজার আইডি ও পরিমাণ এই ফরম্যাটে পাঠান:\n"
        "<code>USER_ID AMOUNT</code>\n\n"
        "উদাহরণ: <code>123456789 5.00</code>",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_subtract_balance")
def admin_subtract_balance_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    user_states[user_id] = {"action": "admin_subtract_balance"}
    bot.send_message(
        call.message.chat.id,
        "➖ <b>ইউজারের ব্যালেন্স কর্তন</b>\n\n"
        "ইউজার আইডি ও পরিমাণ এই ফরম্যাটে পাঠান:\n"
        "<code>USER_ID AMOUNT</code>\n\n"
        "উদাহরণ: <code>123456789 5.00</code>",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == "view_withdrawal_requests")
def view_withdrawal_requests_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    requests = load_withdrawal_requests()
    pending_requests = [r for r in requests if r.get("status") == "pending"]
    
    if not pending_requests:
        bot.answer_callback_query(call.id, "📭 কোনো অপেক্ষমাণ উত্তোলনের অনুরোধ নেই!", show_alert=True)
        return
    
    markup = InlineKeyboardMarkup(row_width=1)
    for req in pending_requests[:10]:
        req_id = req.get("id", "")[:8]
        user_req_id = req.get("user_id")
        amount = req.get("amount", 0)
        markup.add(
            InlineKeyboardButton(
                f"👤 {user_req_id} | ${amount:.2f}",
                callback_data=f"view_wd_req_{req_id}"
            )
        )
    markup.add(InlineKeyboardButton("🔙 ফিরে যান", callback_data="admin_referral_settings", style="danger"))
    
    bot.edit_message_text(
        f"📋 <b>অপেক্ষমাণ উত্তোলনের অনুরোধ</b>\n\nঅনুরোধের সংখ্যা: {len(pending_requests)}",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("view_wd_req_"))
def view_wd_request_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    req_id = call.data.replace("view_wd_req_", "")
    requests = load_withdrawal_requests()
    
    req = None
    for r in requests:
        if r.get("id", "").startswith(req_id):
            req = r
            break
    
    if not req:
        bot.answer_callback_query(call.id, "❌ অনুরোধ পাওয়া যায়নি!", show_alert=True)
        return
    
    target_user_id = req.get('user_id')
    target_user_data = USERS.get(str(target_user_id), {})
    target_referral_data = get_user_referral_data(target_user_id)
    
    join_date = target_user_data.get("join_date", "নির্ধারিত নয়")
    total_codes = target_user_data.get("activations", 0)
    total_referrals = len(target_referral_data.get("referrals", []))
    active_referrals = target_referral_data.get("active_referrals", 0)
    total_earned = target_referral_data.get("total_earned", 0.0)
    current_balance = target_referral_data.get("balance", 0.0)
    
    text = (
        f"📋 <b>উত্তোলনের অনুরোধের বিবরণ</b>\n\n"
        f"🆔 অনুরোধের আইডি: <code>{req.get('id', '')[:8]}</code>\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"👤 <b>ইউজারের তথ্য:</b>\n"
        f"├ 🆔 ID: <code>{target_user_id}</code>\n"
        f"├ 📅 যোগদানের তারিখ: {join_date}\n"
        f"├ 📊 মোট কোড: {total_codes}\n"
        f"├ 👥 মোট রেফারেল: {total_referrals}\n"
        f"├ ✅ সক্রিয় রেফারেল: {active_referrals}\n"
        f"├ 💰 মোট আয়: ${total_earned:.2f}\n"
        f"└ 💵 বর্তমান ব্যালেন্স: ${current_balance:.2f}\n\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"💳 <b>উত্তোলনের বিবরণ:</b>\n"
        f"├ 💵 পরিমাণ: <b>${req.get('amount', 0):.2f}</b>\n"
        f"├ 📝 পদ্ধতি: {req.get('method', 'নির্ধারিত নয়')}\n"
        f"├ 📋 বিবরণ: <code>{req.get('details', 'নির্ধারিত নয়')}</code>\n"
        f"├ 📅 তারিখ: {req.get('date', 'নির্ধারিত নয়')}\n"
        f"└ 📊 অবস্থা: {req.get('status', 'pending')}"
    )
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("✅ পেমেন্ট নিশ্চিত", callback_data=f"approve_wd_{req_id}"),
        InlineKeyboardButton("❌ প্রত্যাখ্যান", callback_data=f"reject_wd_{req_id}")
    )
    markup.add(InlineKeyboardButton("🔙 ফিরে যান", callback_data="view_withdrawal_requests", style="danger"))
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_wd_") or call.data.startswith("wd_approve_"))
def approve_withdrawal_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    if call.data.startswith("wd_approve_"):
        req_id = call.data.replace("wd_approve_", "")
    else:
        req_id = call.data.replace("approve_wd_", "")
    
    requests = load_withdrawal_requests()
    
    for i, req in enumerate(requests):
        if req.get("id", "").startswith(req_id):
            requests[i]["status"] = "approved"
            save_withdrawal_requests(requests)
            
            target_user_id = req.get("user_id")
            user_lang = get_user_language(target_user_id)
            
            try:
                if user_lang == "ar":
                    bot.send_message(
                        target_user_id,
                        f"✅ <b>টাকা সফলভাবে পাঠানো হয়েছে!</b>\n\n"
                        f"🆔 অনুরোধ নম্বর: <code>{req.get('id', '')[:8]}</code>\n"
                        f"💵 পরিমাণ: <b>${req.get('amount', 0):.2f}</b>\n"
                        f"📝 পদ্ধতি: {req.get('method', '')}\n"
                        f"📋 বিবরণ: <code>{req.get('details', '')}</code>\n\n"
                        f"💰 টাকা আপনার অ্যাকাউন্টে সফলভাবে পাঠানো হয়েছে।\n"
                        f"বট ব্যবহারের জন্য ধন্যবাদ! 🎉",
                        parse_mode="HTML"
                    )
                else:
                    bot.send_message(
                        target_user_id,
                        f"✅ <b>Payment sent successfully!</b>\n\n"
                        f"🆔 Request ID: <code>{req.get('id', '')[:8]}</code>\n"
                        f"💵 Amount: <b>${req.get('amount', 0):.2f}</b>\n"
                        f"📝 Method: {req.get('method', '')}\n"
                        f"📋 Details: <code>{req.get('details', '')}</code>\n\n"
                        f"💰 The amount has been successfully transferred to your account.\n"
                        f"Thank you for using the bot! 🎉",
                        parse_mode="HTML"
                    )
            except:
                pass
            
            try:
                bot.edit_message_text(
                    f"✅ <b>পেমেন্ট নিশ্চিত হয়েছে!</b>\n\n"
                    f"🆔 অনুরোধ নম্বর: <code>{req.get('id', '')[:8]}</code>\n"
                    f"👤 ইউজার: <code>{target_user_id}</code>\n"
                    f"💵 পরিমাণ: <b>${req.get('amount', 0):.2f}</b>\n"
                    f"📝 পদ্ধতি: {req.get('method', '')}\n"
                    f"📋 বিবরণ: <code>{req.get('details', '')}</code>\n\n"
                    f"✅ টাকা পাঠানোর বিষয়ে ইউজারকে জানানো হয়েছে",
                    call.message.chat.id,
                    call.message.message_id,
                    parse_mode="HTML"
                )
            except:
                bot.answer_callback_query(call.id, "✅ পেমেন্ট নিশ্চিত হয়েছে!", show_alert=True)
            break

@bot.callback_query_handler(func=lambda call: call.data.startswith("reject_wd_") or call.data.startswith("wd_reject_"))
def reject_withdrawal_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    if call.data.startswith("wd_reject_"):
        req_id = call.data.replace("wd_reject_", "")
    else:
        req_id = call.data.replace("reject_wd_", "")
    
    requests = load_withdrawal_requests()
    
    for i, req in enumerate(requests):
        if req.get("id", "").startswith(req_id):
            requests[i]["status"] = "rejected"
            
            global REFERRALS
            REFERRALS = load_referrals()
            target_user_id = req.get("user_id")
            user_key = str(target_user_id)
            if user_key in REFERRALS:
                REFERRALS[user_key]["balance"] += req.get("amount", 0)
                save_referrals(REFERRALS)
            
            save_withdrawal_requests(requests)
            
            user_lang = get_user_language(target_user_id)
            
            try:
                if user_lang == "ar":
                    bot.send_message(
                        target_user_id,
                        f"❌ <b>উত্তোলনের অনুরোধ প্রত্যাখ্যান করা হয়েছে</b>\n\n"
                        f"🆔 অনুরোধ নম্বর: <code>{req.get('id', '')[:8]}</code>\n"
                        f"💵 পরিমাণ: <b>${req.get('amount', 0):.2f}</b>\n\n"
                        f"টাকা আপনার ব্যালেন্সে ফেরত দেওয়া হয়েছে।",
                        parse_mode="HTML"
                    )
                else:
                    bot.send_message(
                        target_user_id,
                        f"❌ <b>Withdrawal request rejected</b>\n\n"
                        f"🆔 Request ID: <code>{req.get('id', '')[:8]}</code>\n"
                        f"💵 Amount: <b>${req.get('amount', 0):.2f}</b>\n\n"
                        f"The amount has been returned to your balance.",
                        parse_mode="HTML"
                    )
            except:
                pass
            
            try:
                bot.edit_message_text(
                    f"❌ <b>অনুরোধ প্রত্যাখ্যান করা হয়েছে!</b>\n\n"
                    f"🆔 অনুরোধ নম্বর: <code>{req.get('id', '')[:8]}</code>\n"
                    f"👤 ইউজার: <code>{target_user_id}</code>\n"
                    f"💵 পরিমাণ: <b>${req.get('amount', 0):.2f}</b>\n"
                    f"টাকা ইউজারকে ফেরত দেওয়া হয়েছে।",
                    call.message.chat.id,
                    call.message.message_id,
                    parse_mode="HTML"
                )
            except:
                bot.answer_callback_query(call.id, "❌ অনুরোধ প্রত্যাখ্যান ও টাকা ফেরত হয়েছে!", show_alert=True)
            break

@bot.callback_query_handler(func=lambda call: call.data == "admin_withdrawal_methods")
def admin_withdrawal_methods_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    methods = load_withdrawal_methods()
    
    text = "⚙️ <b>উত্তোলনের পদ্ধতি ম্যানেজমেন্ট</b>\n\n"
    text += "চালু বা বন্ধ করতে উত্তোলনের পদ্ধতিতে চাপুন:\n\n"
    
    method_icons = {"vodafone": "💳", "usdt_trc20": "📱", "usdt_bep20": "🔗", "binance_id": "🅱️"}
    
    markup = InlineKeyboardMarkup(row_width=1)
    
    for method_key, method_data in methods.items():
        enabled = method_data.get("enabled", True)
        name = method_data.get("name_ar", method_key)
        icon = method_icons.get(method_key, "💰")
        status = "✅" if enabled else "❌"
        markup.add(InlineKeyboardButton(f"{status} {icon} {name}", callback_data=f"toggle_wd_method_{method_key}"))
    
    markup.add(InlineKeyboardButton("🔙 ফিরে যান", callback_data="admin_referral_settings", style="danger"))
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("toggle_wd_method_"))
def toggle_withdrawal_method_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    method_key = call.data.replace("toggle_wd_method_", "")
    methods = load_withdrawal_methods()
    
    if method_key in methods:
        methods[method_key]["enabled"] = not methods[method_key].get("enabled", True)
        save_withdrawal_methods(methods)
        
        status = "চালু ✅" if methods[method_key]["enabled"] else "বন্ধ ❌"
        bot.answer_callback_query(call.id, f"অবস্থা পরিবর্তন করে করা হয়েছে: {status}", show_alert=True)
    
    admin_withdrawal_methods_callback(call)

@bot.callback_query_handler(func=lambda call: call.data == "admin_welcome_messages")
def admin_welcome_messages_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    messages = load_welcome_messages()
    
    text = (
        "📝 <b>স্বাগত বার্তার সেটিংস</b>\n\n"
        f"🇧🇩 <b>বাংলা:</b>\n{messages.get('ar', 'নির্ধারিত নয়')[:100]}...\n\n"
        f"🇬🇧 <b>English:</b>\n{messages.get('en', 'Not set')[:100]}...\n\n"
        "স্বাগত বার্তা এডিট করতে ভাষা বেছে নিন:"
    )
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🇧🇩 বাংলা এডিট", callback_data="edit_welcome_ar", style="success"),
        InlineKeyboardButton("🇬🇧 Edit English", callback_data="edit_welcome_en", style="primary")
    )
    markup.add(InlineKeyboardButton("🔙 ফিরে যান", callback_data="admin", style="danger"))
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "edit_welcome_ar")
def edit_welcome_ar_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    user_states[user_id] = {"action": "edit_welcome_ar"}
    messages = load_welcome_messages()
    
    bot.send_message(
        call.message.chat.id,
        f"🇧🇩 <b>বাংলা স্বাগত বার্তা এডিট</b>\n\n"
        f"বর্তমান মেসেজ:\n<code>{messages.get('ar', '')}</code>\n\n"
        f"নতুন মেসেজ পাঠান (ব্যবহার করতে পারেন HTML):",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == "edit_welcome_en")
def edit_welcome_en_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    user_states[user_id] = {"action": "edit_welcome_en"}
    messages = load_welcome_messages()
    
    bot.send_message(
        call.message.chat.id,
        f"🇬🇧 <b>Edit English Welcome Message</b>\n\n"
        f"Current message:\n<code>{messages.get('en', '')}</code>\n\n"
        f"Send the new message (HTML supported):",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_button_links")
def admin_button_links_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    links = load_button_links()
    
    text = (
        "🔗 <b>বাটনের লিংক সেটিংস</b>\n"
        "🔗 <b>Button Links Settings</b>\n\n"
        f"📢 <b>গ্রুপের লিংক / Group Link:</b>\n<code>{links.get('group_link', 'Not set')}</code>\n\n"
        f"📺 <b>চ্যানেলের লিংক / Channel Link:</b>\n<code>{links.get('channel_link', 'Not set')}</code>\n\n"
        f"👨‍💻 <b>ডেভেলপারের লিংক / Developer Link:</b>\n<code>{links.get('developer_link', 'Not set')}</code>\n\n"
        "এডিট করতে লিংক বেছে নিন:\nChoose a link to edit:"
    )
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("📢 গ্রুপের লিংক এডিট / Edit Group Link", callback_data="edit_link_group", style="primary"),
        InlineKeyboardButton("📺 চ্যানেলের লিংক এডিট / Edit Channel Link", callback_data="edit_link_channel", style="success"),
        InlineKeyboardButton("👨‍💻 ডেভেলপারের লিংক এডিট / Edit Developer Link", callback_data="edit_link_developer", style="primary")
    )
    markup.add(InlineKeyboardButton("🔙 ফিরুন / Back", callback_data="admin", style="danger"))
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("edit_link_"))
def edit_link_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    link_type = call.data.replace("edit_link_", "")
    link_names = {
        "group": ("গ্রুপের লিংক", "Group Link", "group_link"),
        "channel": ("চ্যানেলের লিংক", "Channel Link", "channel_link"),
        "developer": ("ডেভেলপারের লিংক", "Developer Link", "developer_link")
    }
    
    ar_name, en_name, key = link_names.get(link_type, ("Link", "Link", "group_link"))
    links = load_button_links()
    current = links.get(key, "")
    
    user_states[user_id] = {"action": f"edit_button_link_{key}"}
    
    bot.send_message(
        call.message.chat.id,
        f"🔗 <b>এডিট {ar_name}</b>\n"
        f"🔗 <b>Edit {en_name}</b>\n\n"
        f"বর্তমান লিংক / Current link:\n<code>{current}</code>\n\n"
        f"নতুন লিংক পাঠান / Send the new link:",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_create_backup")
def admin_create_backup_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id): return
    bot.answer_callback_query(call.id, "ব্যাকআপ তৈরি হচ্ছে... ⏳")
    try:
        backup_file = backup_manager.create_backup()
        with open(backup_file, 'rb') as f:
            bot.send_document(call.message.chat.id, f, caption=f"✅ ব্যাকআপ সফলভাবে তৈরি হয়েছে!\n📅 তারিখ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        os.remove(backup_file)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ ব্যাকআপ তৈরির সময় ত্রুটি হয়েছে: {e}")

@bot.callback_query_handler(func=lambda call: call.data == "admin_restore_backup")
def admin_restore_backup_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id): return
    msg = bot.send_message(call.message.chat.id, "📤 অনুগ্রহ করে ব্যাকআপ ফাইল পাঠান (zip).")
    bot.register_next_step_handler(msg, process_restore_backup)

def process_restore_backup(message):
    if not is_admin(message.from_user.id): return
    if not message.document or not message.document.file_name.endswith('.zip'):
        bot.reply_to(message, "❌ দুঃখিত, ফাইল অবশ্যই এই ফরম্যাটে হতে হবে zip শুধু।")
        return
    
    bot.reply_to(message, "ব্যাকআপ পুনরুদ্ধার হচ্ছে... ⏳")
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open("restore_temp.zip", 'wb') as f:
            f.write(downloaded_file)
            
        if backup_manager.restore_backup("restore_temp.zip"):
            bot.reply_to(message, "✅ ব্যাকআপ সফলভাবে পুনরুদ্ধার হয়েছে! এখন ডাটা আবার লোড হবে।")
            load_data() 
        else:
            bot.reply_to(message, "❌ ব্যাকআপ পুনরুদ্ধার ব্যর্থ।")
        
        if os.path.exists("restore_temp.zip"):
            os.remove("restore_temp.zip")
    except Exception as e:
        bot.reply_to(message, f"❌ পুনরুদ্ধারের সময় ত্রুটি হয়েছে: {e}")

@bot.callback_query_handler(func=lambda call: call.data == "admin_otp_buttons")
def admin_otp_buttons_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    global OTP_BUTTONS
    OTP_BUTTONS = load_otp_buttons()
    
    text = "🔘 <b>মেসেজ বাটন সেটিংস OTP</b>\n\n"
    if OTP_BUTTONS:
        for i, btn in enumerate(OTP_BUTTONS, 1):
            text += f"{i}. <b>{btn['name']}</b>\n   🔗 <code>{btn['url']}</code>\n\n"
    else:
        text += "কোনো বাটন যোগ করা নেই\n\n"
    
    text += "প্রয়োজনীয় অপশন বেছে নিন:"
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("➕ নতুন বাটন যোগ করুন", callback_data="otp_btn_add", style="success"),
        InlineKeyboardButton("✏️ বাটন এডিট", callback_data="otp_btn_edit_list", style="primary"),
        InlineKeyboardButton("🗑 বাটন মুছুন", callback_data="otp_btn_delete_list", style="danger")
    )
    markup.add(InlineKeyboardButton("🔙 ফিরে যান", callback_data="admin", style="danger"))
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "otp_btn_add")
def otp_btn_add_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    user_states[user_id] = {"action": "otp_btn_add_name"}
    
    bot.send_message(
        call.message.chat.id,
        "➕ <b>নতুন বাটন যোগ করুন</b>\n\n"
        "বাটনের নাম পাঠান:\n"
        "(উদাহরণ: 𝕮𝖍𝖆𝖓𝖓𝖊𝖑 অথবা Channel)",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == "otp_btn_edit_list")
def otp_btn_edit_list_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    global OTP_BUTTONS
    OTP_BUTTONS = load_otp_buttons()
    
    if not OTP_BUTTONS:
        bot.answer_callback_query(call.id, "❌ এডিট করার মতো কোনো বাটন নেই!", show_alert=True)
        return
    
    markup = InlineKeyboardMarkup(row_width=1)
    for i, btn in enumerate(OTP_BUTTONS):
        markup.add(InlineKeyboardButton(f"✏️ {btn['name']}", callback_data=f"otp_btn_edit_{i}"))
    markup.add(InlineKeyboardButton("🔙 ফিরে যান", callback_data="admin_otp_buttons", style="danger"))
    
    bot.edit_message_text(
        "✏️ <b>এডিট করতে বাটন বেছে নিন:</b>",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("otp_btn_edit_") and not call.data.startswith("otp_btn_edit_name_") and not call.data.startswith("otp_btn_edit_url_") and not call.data.startswith("otp_btn_edit_list"))
def otp_btn_edit_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    btn_idx = int(call.data.replace("otp_btn_edit_", ""))
    global OTP_BUTTONS
    OTP_BUTTONS = load_otp_buttons()
    
    if btn_idx >= len(OTP_BUTTONS):
        bot.answer_callback_query(call.id, "❌ বাটন পাওয়া যায়নি!", show_alert=True)
        return
    
    btn = OTP_BUTTONS[btn_idx]
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("✏️ নাম পরিবর্তন", callback_data=f"otp_btn_edit_name_{btn_idx}"),
        InlineKeyboardButton("🔗 লিংক পরিবর্তন", callback_data=f"otp_btn_edit_url_{btn_idx}")
    )
    markup.add(InlineKeyboardButton("🔙 ফিরে যান", callback_data="otp_btn_edit_list", style="danger"))
    
    bot.edit_message_text(
        f"✏️ <b>বাটন এডিট:</b>\n\n"
        f"📝 <b>নাম:</b> {btn['name']}\n"
        f"🔗 <b>লিংক:</b> <code>{btn['url']}</code>\n\n"
        f"যা এডিট করতে চান তা বেছে নিন:",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("otp_btn_edit_name_"))
def otp_btn_edit_name_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    btn_idx = int(call.data.replace("otp_btn_edit_name_", ""))
    user_states[user_id] = {"action": "otp_btn_edit_name", "btn_idx": btn_idx}
    
    bot.send_message(
        call.message.chat.id,
        "✏️ বাটনের নতুন নাম পাঠান:",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("otp_btn_edit_url_"))
def otp_btn_edit_url_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    btn_idx = int(call.data.replace("otp_btn_edit_url_", ""))
    user_states[user_id] = {"action": "otp_btn_edit_url", "btn_idx": btn_idx}
    
    bot.send_message(
        call.message.chat.id,
        "🔗 বাটনের নতুন লিংক পাঠান:",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == "otp_btn_delete_list")
def otp_btn_delete_list_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    global OTP_BUTTONS
    OTP_BUTTONS = load_otp_buttons()
    
    if not OTP_BUTTONS:
        bot.answer_callback_query(call.id, "❌ মুছে ফেলার মতো কোনো বাটন নেই!", show_alert=True)
        return
    
    markup = InlineKeyboardMarkup(row_width=1)
    for i, btn in enumerate(OTP_BUTTONS):
        markup.add(InlineKeyboardButton(f"🗑 {btn['name']}", callback_data=f"otp_btn_delete_{i}"))
    markup.add(InlineKeyboardButton("🔙 ফিরে যান", callback_data="admin_otp_buttons", style="danger"))
    
    bot.edit_message_text(
        "🗑 <b>মুছতে বাটন বেছে নিন:</b>",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("otp_btn_delete_") and not call.data.startswith("otp_btn_delete_list"))
def otp_btn_delete_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    btn_idx = int(call.data.replace("otp_btn_delete_", ""))
    global OTP_BUTTONS
    OTP_BUTTONS = load_otp_buttons()
    
    if btn_idx >= len(OTP_BUTTONS):
        bot.answer_callback_query(call.id, "❌ বাটন পাওয়া যায়নি!", show_alert=True)
        return
    
    deleted_btn = OTP_BUTTONS.pop(btn_idx)
    save_otp_buttons(OTP_BUTTONS)
    
    bot.answer_callback_query(call.id, f"✅ বাটন মুছে ফেলা হয়েছে: {deleted_btn['name']}", show_alert=True)
    
    text = "🔘 <b>মেসেজ বাটন সেটিংস OTP</b>\n\n"
    if OTP_BUTTONS:
        for i, btn in enumerate(OTP_BUTTONS, 1):
            text += f"{i}. <b>{btn['name']}</b>\n   🔗 <code>{btn['url']}</code>\n\n"
    else:
        text += "কোনো বাটন যোগ করা নেই\n\n"
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("➕ নতুন বাটন যোগ করুন", callback_data="otp_btn_add", style="success"),
        InlineKeyboardButton("✏️ বাটন এডিট", callback_data="otp_btn_edit_list", style="primary"),
        InlineKeyboardButton("🗑 বাটন মুছুন", callback_data="otp_btn_delete_list", style="danger")
    )
    markup.add(InlineKeyboardButton("🔙 ফিরে যান", callback_data="admin", style="danger"))
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "withdraw_balance")
def withdraw_balance_callback(call):
    user_id = call.from_user.id
    lang = get_user_language(user_id)
    
    referral_data = get_user_referral_data(user_id)
    balance = referral_data.get("balance", 0.0)
    settings = load_referral_settings()
    min_withdrawal = settings.get("min_withdrawal", 5.0)
    
    if balance < min_withdrawal:
        msg = f"❌ আপনার ব্যালেন্স ({balance:.2f}$) সর্বনিম্ন উত্তোলনের চেয়ে কম ({min_withdrawal}$)" if lang == "ar" else f"❌ Your balance (${balance:.2f}) is below minimum withdrawal (${min_withdrawal})"
        bot.answer_callback_query(call.id, msg, show_alert=True)
        return
    
    user_states[user_id] = {"action": "withdraw_method"}
    
    methods = load_withdrawal_methods()
    markup = InlineKeyboardMarkup(row_width=2)
    
    method_icons = {"vodafone": "💳", "usdt_trc20": "📱", "usdt_bep20": "🔗", "binance_id": "🅱️"}
    
    for method_key, method_data in methods.items():
        if method_data.get("enabled", True):
            name = method_data.get(f"name_{lang}", method_data.get("name_en", method_key))
            icon = method_icons.get(method_key, "💰")
            markup.add(InlineKeyboardButton(f"{icon} {name}", callback_data=f"wd_method_{method_key}"))
    
    back_text = "🔙 ফিরে যান" if lang == "ar" else "🔙 Back"
    markup.add(InlineKeyboardButton(back_text, callback_data="my_account"))
    
    if lang == "ar":
        text = f"💰 <b>ব্যালেন্স উত্তোলন</b>\n\n💵 আপনার বর্তমান ব্যালেন্স: <b>${balance:.2f}</b>\n\nউত্তোলনের পদ্ধতি বেছে নিন:"
    else:
        text = f"💰 <b>Withdraw Balance</b>\n\n💵 Your balance: <b>${balance:.2f}</b>\n\nChoose withdrawal method:"
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("wd_method_"))
def withdraw_method_callback(call):
    user_id = call.from_user.id
    lang = get_user_language(user_id)
    method_key = call.data.replace("wd_method_", "")
    
    methods = load_withdrawal_methods()
    method_data = methods.get(method_key, {})
    
    if not method_data.get("enabled", True):
        msg = "❌ এই উত্তোলনের পদ্ধতি এখন উপলব্ধ নয়" if lang == "ar" else "❌ This withdrawal method is not available"
        bot.answer_callback_query(call.id, msg, show_alert=True)
        return
    
    method_name = method_data.get(f"name_{lang}", method_data.get("name_en", method_key))
    details_prompt = method_data.get(f"details_{lang}", method_data.get("details_en", "Account details"))
    
    user_states[user_id] = {"action": "withdraw_details", "method": method_name, "method_key": method_key}
    
    if lang == "ar":
        text = f"📝 পাঠান <b>{details_prompt}</b> আপনার জন্য: {method_name}:"
    else:
        text = f"📝 Send your <b>{details_prompt}</b> for {method_name}:"
    
    bot.send_message(call.message.chat.id, text, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == "admin_admins_menu")
def admin_admins_menu_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔧 অ্যাডমিন যোগ করুন", callback_data="admin_add_admin", style="success"),
        InlineKeyboardButton("🗑 অ্যাডমিন মুছুন", callback_data="admin_remove_admin", style="danger")
    )
    markup.add(
        InlineKeyboardButton("🚫 ইউজার ব্যান", callback_data="admin_ban_user", style="danger"),
        InlineKeyboardButton("✅ আনব্যান", callback_data="admin_unban_user", style="success")
    )
    markup.add(InlineKeyboardButton("🔙 ফিরে যান", callback_data="admin_panel", style="danger"))
    
    bot.edit_message_text(
        "👥 <b>অ্যাডমিন ও ইউজার ম্যানেজমেন্ট</b>\n\nপ্রয়োজনীয় অপশন বেছে নিন:",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_channels_menu")
def admin_channels_menu_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("➕ চ্যানেল যোগ করুন", callback_data="admin_add_channel", style="success"),
        InlineKeyboardButton("🗑 চ্যানেল মুছুন", callback_data="admin_remove_channel", style="danger")
    )
    markup.add(
        InlineKeyboardButton("📊 যোগ করা চ্যানেল", callback_data="admin_list_channels", style="primary")
    )
    markup.add(InlineKeyboardButton("🔙 ফিরে যান", callback_data="admin_panel", style="danger"))
    
    bot.edit_message_text(
        "📢 <b>চ্যানেল ম্যানেজমেন্ট</b>\n\nপ্রয়োজনীয় অপশন বেছে নিন:",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_countries_menu")
def admin_countries_menu_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("➕ দেশ যোগ করুন", callback_data="admin_add_country", style="success"),
        InlineKeyboardButton("➖ দেশ মুছুন", callback_data="admin_remove_country", style="danger")
    )
    markup.add(
        InlineKeyboardButton("📋 উপলব্ধ দেশসমূহ", callback_data="admin_list_countries", style="primary")
    )
    markup.add(InlineKeyboardButton("🔙 ফিরে যান", callback_data="admin_panel", style="danger"))
    
    bot.edit_message_text(
        "🌍 <b>দেশ ম্যানেজমেন্ট</b>\n\nপ্রয়োজনীয় অপশন বেছে নিন:",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_groups_menu")
def admin_groups_menu_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("➕ গ্রুপ যোগ করুন", callback_data="admin_add_group_start", style="success"),
        InlineKeyboardButton("➖ গ্রুপ মুছুন", callback_data="admin_remove_group", style="danger")
    )
    markup.add(
        InlineKeyboardButton("📋 গ্রুপ দেখুন", callback_data="admin_list_groups", style="primary")
    )
    markup.add(InlineKeyboardButton("🔙 ফিরে যান", callback_data="admin_panel", style="danger"))
    
    bot.edit_message_text(
        "📱 <b>গ্রুপ ম্যানেজমেন্ট</b>\n\nপ্রয়োজনীয় অপশন বেছে নিন:",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_add_group_start")
def admin_add_group_start_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    from telebot.types import ReplyKeyboardMarkup, KeyboardButton
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("🔘 গ্রুপ বেছে নিন", request_chat=telebot.types.KeyboardButtonRequestChat(request_id=1, chat_is_channel=False)))
    
    bot.send_message(
        call.message.chat.id,
        "➕ <b>নতুন গ্রুপ যোগ করুন</b>\n\n"
        "গ্রুপ বাছাই করতে নিচের বাটনে চাপুন অথবা পাঠান ID সরাসরি গ্রুপ:",
        parse_mode="HTML",
        reply_markup=markup
    )
    user_states[user_id] = {"action": "add_group"}

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get("action") == "add_group", content_types=['text', 'chat_shared'])
def handle_add_group_message(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return

    group_id = None
    if message.content_type == 'chat_shared':
        group_id = message.chat_shared.chat_id
    else:
        text = message.text.strip()
        if text.startswith('-') and text[1:].isdigit() or text.isdigit():
            group_id = int(text)
    
    if group_id:
        if group_id not in GROUPS:
            GROUPS.append(group_id)
            save_groups()
            bot.send_message(message.chat.id, f"✅ গ্রুপ সফলভাবে যোগ হয়েছে!\nID: <code>{group_id}</code>", parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
        else:
            bot.send_message(message.chat.id, "⚠️ এই গ্রুপ আগেই যোগ করা আছে।", reply_markup=ReplyKeyboardRemove())
        user_states[user_id] = {}
    else:
        bot.send_message(message.chat.id, "❌ ID অবৈধ। অনুগ্রহ করে পাঠান ID সঠিক আইডি অথবা বাটন থেকে গ্রুপ বেছে নিন।")

@bot.callback_query_handler(func=lambda call: call.data == "admin_add_group")
def admin_add_group_callback(call):
   
    admin_add_group_start_callback(call)

@bot.callback_query_handler(func=lambda call: call.data == "admin_remove_group")
def admin_remove_group_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    if not GROUPS:
        bot.answer_callback_query(call.id, "⚠️ কোনো গ্রুপ যোগ করা নেই", show_alert=True)
        return
    
    groups_list = "\n".join([f"• <code>{gid}</code>" for gid in GROUPS])
    
    user_states[user_id] = {"action": "remove_group"}
    
    bot.send_message(
        call.message.chat.id,
        f"🗑 <b>গ্রুপ মুছুন</b>\n\n"
        f"<b>যোগ করা গ্রুপ:</b>\n{groups_list}\n\n"
        f"পাঠান ID যে গ্রুপ মুছতে চান:",
        parse_mode="HTML"
    )

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get("action") == "remove_group")
def handle_remove_group_message(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return

    try:
        group_id = int(message.text.strip())
        if group_id in GROUPS:
            GROUPS.remove(group_id)
            save_groups()
            bot.send_message(message.chat.id, f"✅ গ্রুপ মুছে ফেলা হয়েছে <code>{group_id}</code> সফলভাবে!", parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, "❌ এই গ্রুপ তালিকায় নেই।")
    except ValueError:
        bot.send_message(message.chat.id, "❌ অনুগ্রহ করে পাঠান ID সঠিক আইডি (সংখ্যা)।")
    
    user_states[user_id] = {}

@bot.callback_query_handler(func=lambda call: call.data == "admin_list_groups")
def admin_list_groups_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    if not GROUPS:
        bot.answer_callback_query(call.id, "⚠️ কোনো গ্রুপ যোগ করা নেই", show_alert=True)
        return
    
    groups_text = "📋 <b>যোগ করা গ্রুপ:</b>\n\n"
    for idx, gid in enumerate(GROUPS, 1):
        try:
            chat = bot.get_chat(gid)
            groups_text += f"{idx}. <b>{chat.title}</b>\n"
            groups_text += f"   🆔 <code>{gid}</code>\n\n"
        except:
            groups_text += f"{idx}. অজানা গ্রুপ\n"
            groups_text += f"   🆔 <code>{gid}</code>\n\n"
    
    bot.send_message(call.message.chat.id, groups_text, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == "admin_broadcast_menu")
def admin_broadcast_menu_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📣 ব্রডকাস্ট", callback_data="admin_broadcast_normal", style="primary"),
        InlineKeyboardButton("📤 ফরওয়ার্ড ব্রডকাস্ট", callback_data="admin_broadcast_forward", style="primary")
    )
    markup.add(InlineKeyboardButton("🔙 ফিরে যান", callback_data="admin_panel", style="danger"))
    
    bot.edit_message_text(
        "📣 <b>ব্রডকাস্ট সিস্টেম</b>\n\n"
        "ব্রডকাস্টের ধরন বেছে নিন:\n\n"
        "• <b>ব্রডকাস্ট:</b> প্রতি ইউজারের জন্য নতুন মেসেজ\n"
        "• <b>ফরওয়ার্ড ব্রডকাস্ট:</b> আপনার মেসেজ ফরওয়ার্ড করা হবে",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_broadcast_normal")
def admin_broadcast_normal_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id): return
    broadcast_state[user_id] = {"type": "normal", "step": "waiting_message"}
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 বাতিল", callback_data="cancel_broadcast", style="danger"))
    bot.send_message(call.message.chat.id, "📣 <b>সাধারণ ব্রডকাস্ট</b>\n\nযে মেসেজ ব্রডকাস্ট করতে চান তা পাঠান:", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "admin_broadcast_forward")
def admin_broadcast_forward_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id): return
    broadcast_state[user_id] = {"type": "forward", "step": "waiting_message"}
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 বাতিল", callback_data="cancel_broadcast", style="danger"))
    bot.send_message(call.message.chat.id, "📤 <b>ফরওয়ার্ড ব্রডকাস্ট</b>\n\nযে মেসেজ ফরওয়ার্ড করতে চান তা পাঠান:", parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.from_user.id in broadcast_state and broadcast_state[msg.from_user.id].get("step") == "waiting_message", content_types=["text", "photo", "video", "document"])
def handle_broadcast_message(msg):
    user_id = msg.from_user.id
    state = broadcast_state[user_id]
    state["step"] = "confirm"
    state["message"] = msg
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅ পাঠানো নিশ্চিত", callback_data="confirm_broadcast", style="success"), InlineKeyboardButton("❌ বাতিল", callback_data="cancel_broadcast", style="danger"))
    bot.reply_to(msg, "❓ <b>আপনি কি নিশ্চিত এই মেসেজ সবাইকে পাঠাতে চান?</b>", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "confirm_broadcast")
def confirm_broadcast_callback(call):
    user_id = call.from_user.id
    if user_id not in broadcast_state: return
    state = broadcast_state[user_id]
    msg = state["message"]
    success, failed = 0, 0
    progress = bot.send_message(call.message.chat.id, "⏳ পাঠানো হচ্ছে...")
    for uid in list(USERS.keys()):
        try:
            if state["type"] == "forward":
                bot.forward_message(int(uid), msg.chat.id, msg.message_id)
            else:
                bot.copy_message(int(uid), msg.chat.id, msg.message_id)
            success += 1
        except: failed += 1
    bot.delete_message(progress.chat.id, progress.message_id)
    bot.send_message(call.message.chat.id, f"✅ <b>পাঠানো হয়েছে!</b>\n\n📊 সফল: {success}\n❌ ব্যর্থ: {failed}", parse_mode="HTML")
    del broadcast_state[user_id]

def send_saved_message(target_bot, target_uid, saved_msg):
    
    content_type = saved_msg.get("content_type")
    
    if content_type == "text":
        target_bot.send_message(target_uid, saved_msg.get("text"), parse_mode="HTML" if saved_msg.get("has_entities") else None)
    elif content_type == "photo":
        target_bot.send_photo(target_uid, saved_msg.get("file_id"), caption=saved_msg.get("caption"))
    elif content_type == "video":
        target_bot.send_video(target_uid, saved_msg.get("file_id"), caption=saved_msg.get("caption"))
    elif content_type == "document":
        target_bot.send_document(target_uid, saved_msg.get("file_id"), caption=saved_msg.get("caption"))
    elif content_type == "audio":
        target_bot.send_audio(target_uid, saved_msg.get("file_id"), caption=saved_msg.get("caption"))
    elif content_type == "voice":
        target_bot.send_voice(target_uid, saved_msg.get("file_id"), caption=saved_msg.get("caption"))
    elif content_type == "sticker":
        target_bot.send_sticker(target_uid, saved_msg.get("file_id"))

@bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
def back_to_main_callback(call):
    user_id = call.from_user.id
    lang = get_user_language(user_id)
    settings = load_referral_settings()
    code_bonus = settings.get("code_bonus", 0.01)
    
    markup = get_country_buttons(user_id)
    if markup:
        if lang == "ar":
            title = f"<tg-emoji emoji-id='5972277098830634724'>🚨</tg-emoji> <b>প্ল্যাটফর্ম বেছে নিন</b>\n\n<tg-emoji emoji-id='6046356449938905522'>💰</tg-emoji> আপনি পাবেন <b>${format_decimal(code_bonus)}</b> প্রতিটি কোড পেলে!"
        else:
            title = f"<tg-emoji emoji-id='5972277098830634724'>🚨</tg-emoji> <b>Select Country</b>\n\n💰 You'll earn <b>${format_decimal(code_bonus)}</b> for each code received!"
        
        try:
            bot.edit_message_text(
                title,
                call.message.chat.id,
                call.message.message_id,
                parse_mode="HTML",
                reply_markup=markup
            )
        except:
            pass
    else:
        try:
            text = t(user_id, "welcome")
            if not text: text = "🌐 <b>স্বাগতম!</b>"
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode="HTML",
                reply_markup=get_main_menu_lang(user_id)
            )
        except:
            pass

@bot.callback_query_handler(func=lambda call: call.data == "admin_add_country")
def admin_add_country_callback(call):
    user_id = call.from_user.id

    if not is_admin(user_id):
        return

    user_states[user_id] = {"action": "na_add_country_file"}

    bot.send_message(
        call.message.chat.id,
        "📝 <b>নতুন দেশ যোগ - ধাপ 1/3</b>\n\n"
        "📤 নম্বরের ফাইল পাঠান (.txt)\n\n"
        "<i>ফাইল স্বয়ংক্রিয়ভাবে পরিষ্কার হবে এবং প্রতি লাইন থেকে শুধু নম্বর নেওয়া হবে</i>",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_remove_country")
def admin_remove_country_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    if not COUNTRIES:
        bot.answer_callback_query(call.id, "❌ কোনো দেশ যোগ করা নেই!", show_alert=True)
        return
    
    markup = InlineKeyboardMarkup(row_width=2)
    
    for cid in sorted(COUNTRIES.keys()):
        info = COUNTRIES[cid]
        cname = info.get("display_name", cid)
        flag = info.get("flag", "🌍")
        count = info.get("numbers_count", 0)
        markup.add(InlineKeyboardButton(f"❌ {flag} {cname} ({count})", callback_data=f"delete_country_btn_{cid}"))
    
    markup.add(InlineKeyboardButton("🔙 ফিরে যান", callback_data="admin_panel", style="danger"))
    
    bot.edit_message_text(
        "🗑 <b>দেশ মুছুন</b>\n\nনিচের তালিকা থেকে যে দেশ মুছতে চান সেটি বেছে নিন:",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_country_btn_"))
def delete_country_confirm_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        return
    
    country_name = call.data.replace("delete_country_btn_", "")
    if country_name in COUNTRIES:
        
        file_path = COUNTRIES[country_name].get("file")
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
        
        del COUNTRIES[country_name]
        save_countries()
        bot.answer_callback_query(call.id, f"✅ মুছে ফেলা হয়েছে {country_name} সফলভাবে!", show_alert=True)
        
        admin_remove_country_callback(call)
    else:
        bot.answer_callback_query(call.id, "❌ এই দেশ পাওয়া যায়নি!", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "admin_list_countries")
def admin_list_countries_callback(call):
    user_id = call.from_user.id

    if not is_admin(user_id):
        return

    if not COUNTRIES:
        bot.answer_callback_query(call.id, "⚠️ এখন কোনো দেশ যোগ করা নেই", show_alert=True)
        return

    countries_text = "📋 <b>উপলব্ধ দেশ:</b>\n\n"
    for cid, info in COUNTRIES.items():
        cname = info.get("display_name", cid)
        countries_text += f"🌍 <b>{cname}</b> {info.get('flag', '🌐')}\n"
        countries_text += f"   🆔 আইডি: <code>{cid}</code>\n"
        countries_text += f"   📊 নম্বর: {info.get('numbers_count', 0)}\n"
        countries_text += f"   ⚙️ সার্ভিস: {info.get('service', 'N/A')}\n"
        countries_text += f"   📄 ফাইল: {info.get('file', 'N/A')}\n"
        if info.get('server'):
            countries_text += f"   🖥️ সার্ভার: {info.get('server')}\n"
        if info.get('platforms'):
            countries_text += f"   📱 প্ল্যাটফর্ম: {', '.join(info.get('platforms', []))}\n"
        countries_text += "\n"

    bot.send_message(call.message.chat.id, countries_text, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data.startswith("add_country_srv_"))
def add_country_server_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    if user_id not in user_states or user_states[user_id].get("action") != "add_country_server":
        bot.answer_callback_query(call.id, "❌ সেশন শেষ হয়ে গেছে!", show_alert=True)
        return
    
    server = call.data.replace("add_country_srv_", "")
    state = user_states[user_id]
    
    user_states[user_id] = {
        "action": "add_country_platforms",
        "temp_file": state.get("temp_file"),
        "country_code": state.get("country_code"),
        "country_name": state.get("country_name"),
        "num_cleaned": state.get("num_cleaned"),
        "server": server,
        "selected_platforms": []
    }
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📘 Facebook", callback_data="add_country_plt_Facebook", style="primary"),
        InlineKeyboardButton("💬 WhatsApp", callback_data="add_country_plt_WhatsApp", style="success")
    )
    markup.add(
        InlineKeyboardButton("✈️ Telegram", callback_data="add_country_plt_Telegram", style="primary"),
        InlineKeyboardButton("📸 Instagram", callback_data="add_country_plt_Instagram", style="danger")
    )
    markup.add(
        InlineKeyboardButton("🐦 Twitter/X", callback_data="add_country_plt_Twitter", style="primary"),
        InlineKeyboardButton("📱 TikTok", callback_data="add_country_plt_TikTok", style="success")
    )
    markup.add(
        InlineKeyboardButton("🎮 Discord", callback_data="add_country_plt_Discord", style="danger"),
        InlineKeyboardButton("📧 Gmail", callback_data="add_country_plt_Gmail", style="primary")
    )
    markup.add(
        InlineKeyboardButton("🌐 সব প্ল্যাটফর্ম", callback_data="add_country_plt_ALL", style="success")
    )
    markup.add(InlineKeyboardButton("✅ নিশ্চিত করুন ও শেষ করুন", callback_data="add_country_finish", style="success"))
    markup.add(InlineKeyboardButton("❌ বাতিল", callback_data="admin_countries", style="primary"))
    
    server_names = {
        "GROUP": "🏢 GROUP",
        "Fly sms": "🔷 Fly sms",
        "Number_Panel": "📱 Number Panel",
        "Bolt": "⚡ Bolt",
        "iVASMS": "🌐 iVASMS"
    }
    
    bot.edit_message_text(
        f"✅ <b>ধাপ 5/5 - প্ল্যাটফর্ম বাছাই</b>\n\n"
        f"🌍 দেশ: <b>{state.get('country_name')}</b>\n"
        f"🔢 দেশের কোড: <b>{state.get('country_code')}</b>\n"
        f"🖥️ সার্ভার: <b>{server_names.get(server, server)}</b>\n\n"
        f"📱 <b>বাছাই করা প্ল্যাটফর্ম:</b> নেই\n\n"
        f"এই নম্বরগুলো যে প্ল্যাটফর্মে কাজ করে সেগুলো বেছে নিন:",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("add_country_plt_"))
def add_country_platform_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    if user_id not in user_states or user_states[user_id].get("action") != "add_country_platforms":
        bot.answer_callback_query(call.id, "❌ সেশন শেষ হয়ে গেছে!", show_alert=True)
        return
    
    platform = call.data.replace("add_country_plt_", "")
    state = user_states[user_id]
    selected_platforms = state.get("selected_platforms", [])
    
    if platform == "ALL":
        selected_platforms = ["Facebook", "WhatsApp", "Telegram", "Instagram", "Twitter", "TikTok", "Discord", "Gmail"]
    elif platform in selected_platforms:
        selected_platforms.remove(platform)
    else:
        selected_platforms.append(platform)
    
    user_states[user_id]["selected_platforms"] = selected_platforms
    
    platform_icons = {
        "Facebook": "📘", "WhatsApp": "💬", "Telegram": "✈️",
        "Instagram": "📸", "Twitter": "🐦", "TikTok": "📱",
        "Discord": "🎮", "Gmail": "📧"
    }
    
    markup = InlineKeyboardMarkup(row_width=2)
    
    def get_btn_text(name, icon):
        check = "✅" if name in selected_platforms else ""
        return f"{check} {icon} {name}"
    
    markup.add(
        InlineKeyboardButton(get_btn_text("Facebook", "📘"), callback_data="add_country_plt_Facebook"),
        InlineKeyboardButton(get_btn_text("WhatsApp", "💬"), callback_data="add_country_plt_WhatsApp")
    )
    markup.add(
        InlineKeyboardButton(get_btn_text("Telegram", "✈️"), callback_data="add_country_plt_Telegram"),
        InlineKeyboardButton(get_btn_text("Instagram", "📸"), callback_data="add_country_plt_Instagram")
    )
    markup.add(
        InlineKeyboardButton(get_btn_text("Twitter", "🐦"), callback_data="add_country_plt_Twitter"),
        InlineKeyboardButton(get_btn_text("TikTok", "📱"), callback_data="add_country_plt_TikTok")
    )
    markup.add(
        InlineKeyboardButton(get_btn_text("Discord", "🎮"), callback_data="add_country_plt_Discord"),
        InlineKeyboardButton(get_btn_text("Gmail", "📧"), callback_data="add_country_plt_Gmail")
    )
    markup.add(
        InlineKeyboardButton("🌐 সব প্ল্যাটফর্ম", callback_data="add_country_plt_ALL", style="success")
    )
    markup.add(InlineKeyboardButton("✅ নিশ্চিত করুন ও শেষ করুন", callback_data="add_country_finish", style="success"))
    markup.add(InlineKeyboardButton("❌ বাতিল", callback_data="admin_countries", style="danger"))
    
    server_names = {
        "GROUP": "🏢 GROUP",
        "Fly sms": "🔷 Fly sms",
        "Number_Panel": "📱 Number Panel",
        "Bolt": "⚡ Bolt",
        "iVASMS": "🌐 iVASMS"
    }
    
   
    platform_icons = {
        "Facebook": "📘", "WhatsApp": "💬", "Telegram": "✈️",
        "Instagram": "📸", "Twitter": "🐦", "TikTok": "📱",
        "Discord": "🎮", "Gmail": "📧"
    }
    
    platforms_text = ", ".join([f"{platform_icons.get(p, '📱')} {p}" for p in selected_platforms]) if selected_platforms else "নেই"
    
    try:
        bot.edit_message_text(
            f"✅ <b>ধাপ 5/5 - প্ল্যাটফর্ম বাছাই</b>\n\n"
            f"🌍 দেশ: <b>{state.get('country_name')}</b>\n"
            f"🔢 দেশের কোড: <b>{state.get('country_code')}</b>\n"
            f"🖥️ সার্ভার: <b>{server_names.get(state.get('server'), state.get('server'))}</b>\n\n"
            f"📱 <b>বাছাই করা প্ল্যাটফর্ম:</b> {platforms_text}\n\n"
            f"এই নম্বরগুলো যে প্ল্যাটফর্মে কাজ করে সেগুলো বেছে নিন:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="HTML",
            reply_markup=markup
        )
    except:
        pass
    
    bot.answer_callback_query(call.id)

def format_otp_message(number, sms_text, service_name="[TG]", otp_code=None, user_id=None, is_group=False):
    country_name, flag, region_code = detect_country_from_number(number, user_id)
    masked = mask_number(number)
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
   
    service_upper = str(service_name).replace("[", "").replace("]", "").upper()
    shorthand = service_upper
    
    if is_group:
        SHORTHANDS = {
            "WHATSAPP": "<tg-emoji emoji-id='5188683998125106802'>📞</tg-emoji>",
            "TELEGRAM": "TG",
            "FACEBOOK": "FB",
            "INSTAGRAM": "IG",
            "TIKTOK": "TK",
            "TWITTER": "TW",
            "GOOGLE": "GG",
            "MICROSOFT": "MS",
            "NETFLIX": "NF",
            "STEAM": "ST",
            "SNAPCHAT": "SC",
            "VIBER": "VB",
            "IMO": "IM",
            "WECHAT": "WC",
            "LINE": "LN",
            "DISCORD": "DC",
            "PAYPAL": "PP",
            "AMAZON": "AZ",
            "EBAY": "EB",
            "APPLE": "AP"
        }

        for key, val in SHORTHANDS.items():
            if key in service_upper:
                shorthand = val
                break
                
        if shorthand == service_upper and len(shorthand) > 3:
            shorthand = shorthand[:2]
        
    service_display = f"[{shorthand}]"
    
    header = f"──────────────╖ \n↠ {flag} #{region_code} {service_display} {masked} ┨\n──────────────╛"
    
    body = f"<blockquote>{sms_text}</blockquote>"
    time_footer = f"<blockquote>• ⏰ ~ {now_str}</blockquote>"
    
    return f"{header}\n{body}\n{time_footer}"

@bot.callback_query_handler(func=lambda call: call.data == "add_country_finish")
def add_country_finish_callback(call):
    user_id = call.from_user.id
    if not is_admin(user_id): return
    if user_id not in user_states or user_states[user_id].get("action") != "add_country_platforms":
        bot.answer_callback_query(call.id, "❌ সেশন শেষ হয়ে গেছে!", show_alert=True)
        return
    
    state = user_states[user_id]
    temp_file = state.get("temp_file")
    server = state.get("server")
    selected_platforms = state.get("selected_platforms", ["WhatsApp"])
    
    bot.edit_message_text("🔍 ফাইল পরীক্ষা করে স্বয়ংক্রিয়ভাবে দেশ নির্ধারণ করা হচ্ছে...", call.message.chat.id, call.message.message_id)
    
    prefix = detect_country_code_from_file(temp_file)
    if not prefix:
        bot.send_message(call.message.chat.id, "❌ ফাইল থেকে দেশের কোড নির্ধারণ করা যায়নি।")
        return

    country_name, flag, region_code = detect_country_from_number(prefix)
    count, total, rejected = clean_and_filter_numbers(temp_file, prefix)
    
    if count == 0:
        bot.send_message(call.message.chat.id, f"❌ ফাইলে এমন কোনো নম্বর নেই যা শুরু হয় +{prefix}")
        return

    final_country_name = country_name
    if region_code == "EG": final_country_name = "مصر"
    
    final_filename = f"numbers_{prefix}_{uuid.uuid4().hex[:8]}.txt"
    if os.path.exists(temp_file):
        os.rename(temp_file, final_filename)

    
    unique_id = uuid.uuid4().hex[:12]
    country_id = f"{final_country_name}_{unique_id}"
    
    
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_filename = f"numbers_{prefix}_{timestamp_str}_{unique_id}.txt"
    
    if os.path.exists(temp_file):
        
        while os.path.exists(final_filename):
            unique_id = uuid.uuid4().hex[:12]
            final_filename = f"numbers_{prefix}_{timestamp_str}_{unique_id}.txt"
            country_id = f"{final_country_name}_{unique_id}"
            
        os.rename(temp_file, final_filename)
        print(f"✅ ফাইল ইউনিক নামে সেভ হয়েছে: {final_filename}")

    COUNTRIES[country_id] = {
        "display_name": final_country_name,
        "file": final_filename,
        "code": prefix,
        "flag": flag,
        "server": server,
        "platforms": selected_platforms,
        "numbers_count": count,
        "added_by": user_id,
        "added_at": datetime.now().isoformat()
    }
    
   
    with open(COUNTRIES_FILE, "w", encoding="utf-8") as f:
        json.dump(COUNTRIES, f, indent=2, ensure_ascii=False)
    
    del user_states[user_id]
    bot.send_message(
        call.message.chat.id,
        f"✅ <b>দেশ সফলভাবে যোগ হয়েছে!</b>\n\n"
        f"🌍 দেশ: {flag} {final_country_name} (#{region_code})\n"
        f"🔢 কোড: +{prefix}\n"
        f"📱 সংখ্যা: {count} নম্বর\n"
        f"🖥 সার্ভার: {server}\n"
        f"✨ ফাইলের কন্টেন্ট থেকে স্বয়ংক্রিয়ভাবে নির্ধারিত",
        parse_mode="HTML"
    )


@bot.callback_query_handler(func=lambda call: call.data == "admin_add_channel")
def admin_add_channel_callback(call):
    user_id = call.from_user.id

    if not is_admin(user_id):
        return

    user_states[user_id] = {"action": "add_channel"}

    bot.send_message(
        call.message.chat.id,
        "📢 <b>বাধ্যতামূলক সাবস্ক্রিপশন চ্যানেল যোগ</b>\n\n"
        "চ্যানেলের লিংক বা আইডি পাঠান:\n\n"
        "<b>উদাহরণ:</b>\n"
        "• <code>@new_OTP_Group</code>\n"
        "• <code>https://t.me/alorhawa</code>\n"
        "• <code>-1003591777442</code> (ID)\n\n"
        "<b>নোট:</b> বটকে চ্যানেলের অ্যাডমিন হতে হবে!",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_remove_channel")
def admin_remove_channel_callback(call):
    user_id = call.from_user.id

    if not is_admin(user_id):
        return

    if not CHANNELS:
        bot.answer_callback_query(call.id, "⚠️ এখন কোনো চ্যানেল যোগ করা নেই", show_alert=True)
        return

    channels_list = "\n".join([f"{idx+1}. {ch['name']} ({ch['username']})" for idx, ch in enumerate(CHANNELS)])

    user_states[user_id] = {"action": "remove_channel"}

    bot.send_message(
        call.message.chat.id,
        f"🗑 <b>চ্যানেল মুছুন</b>\n\n"
        f"<b>যোগ করা চ্যানেল:</b>\n{channels_list}\n\n"
        f"যে চ্যানেল মুছতে চান তার নম্বর পাঠান:",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_list_channels")
def admin_list_channels_callback(call):
    user_id = call.from_user.id

    if not is_admin(user_id):
        return

    if not CHANNELS:
        bot.answer_callback_query(call.id, "⚠️ এখন কোনো চ্যানেল যোগ করা নেই", show_alert=True)
        return

    channels_text = "📊 <b>যোগ করা চ্যানেল:</b>\n\n"
    for idx, ch in enumerate(CHANNELS, 1):
        channels_text += f"{idx}. 📢 <b>{ch['name']}</b>\n"
        channels_text += f"   🔗 {ch['username']}\n"
        channels_text += f"   🆔 ID: <code>{ch['id']}</code>\n\n"

    bot.send_message(call.message.chat.id, channels_text, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == "admin_add_admin")
def admin_add_admin_callback(call):
    user_id = call.from_user.id
    if user_id != MAIN_ADMIN_ID:
        bot.answer_callback_query(call.id, "❌ দুঃখিত, শুধু মালিক অ্যাডমিন যোগ করতে পারেন!", show_alert=True)
        return
    user_states[user_id] = {"action": "add_admin"}
    bot.send_message(call.message.chat.id, "🔧 <b>নতুন অ্যাডমিন যোগ</b>\n\nইউজারের আইডি পাঠান (User ID) যাকে অ্যাডমিন বানাতে চান:", parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == "admin_remove_admin")
def admin_remove_admin_callback(call):
    user_id = call.from_user.id
    if user_id != MAIN_ADMIN_ID:
        bot.answer_callback_query(call.id, "❌ দুঃখিত, শুধু মালিক অ্যাডমিন মুছতে পারেন!", show_alert=True)
        return
    
    admins_list = ""
    for aid in ADMINS:
        status = " (মালিক 👑)" if aid == MAIN_ADMIN_ID else ""
        admins_list += f"• <code>{aid}</code>{status}\n"
    
    user_states[user_id] = {"action": "remove_admin"}
    bot.send_message(
        call.message.chat.id, 
        f"🗑 <b>অ্যাডমিন মুছুন</b>\n\n📋 <b>বর্তমান অ্যাডমিনরা:</b>\n{admins_list}\n\nযে অ্যাডমিনকে মুছতে চান তার আইডি পাঠান:", 
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_ban_user")
def admin_ban_user_callback(call):
    user_id = call.from_user.id

    if not is_admin(user_id):
        return

    user_states[user_id] = {"action": "ban_user"}

    bot.send_message(
        call.message.chat.id,
        "🚫 <b>ইউজার ব্যান</b>\n\n"
        "পাঠান ID ইউজার:",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_unban_user")
def admin_unban_user_callback(call):
    user_id = call.from_user.id

    if not is_admin(user_id):
        return

    if not BANNED:
        bot.answer_callback_query(call.id, "⚠️ কোনো ব্যান করা ইউজার নেই!", show_alert=True)
        return

    banned_list = "\n".join([f"• <code>{uid}</code>" for uid in BANNED])

    user_states[user_id] = {"action": "unban_user"}

    bot.send_message(
        call.message.chat.id,
        f"✅ <b>ইউজার আনব্যান</b>\n\n"
        f"<b>ব্যান করা ইউজার:</b>\n{banned_list}\n\n"
        f"পাঠান ID ইউজার:",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_set_otp_group")
def admin_set_otp_group_callback(call):
    user_id = call.from_user.id

    if not is_admin(user_id):
        return

    user_states[user_id] = {"action": "set_otp_group"}

    bot.send_message(
        call.message.chat.id,
        "📬 <b>গ্রুপ সেট করুন OTP</b>\n\n"
        "পাঠান ID যে গ্রুপে মেসেজ পাঠানো হবে OTP সেটি:",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_accounts_menu")
def admin_accounts_menu_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "⛔️ আপনার প্রবেশাধিকার নেই", show_alert=True)
        return
    
    bot.edit_message_text(
        "👥 <b>অ্যাকাউন্ট ম্যানেজমেন্ট</b>\n\nঅ্যাকাউন্ট ম্যানেজ করতে সাইট বেছে নিন:",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=get_accounts_menu()
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("accounts_site_"))
def accounts_site_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    site_key = call.data.replace("accounts_site_", "")
    site_name = SETTINGS[site_key]["name"]
    accounts = get_site_accounts(site_key)
    
    accounts_text = f"👥 <b>অ্যাকাউন্ট {site_name}</b>\n\n"
    if accounts:
        accounts_text += f"📊 অ্যাকাউন্ট সংখ্যা: {len(accounts)}\n\n"
        for idx, account in enumerate(accounts, 1):
            username = account.get("username", "N/A")
            accounts_text += f"{idx}. 👤 <code>{username}</code>\n"
    else:
        accounts_text += "⚠️ কোনো অ্যাকাউন্ট যোগ করা নেই\n"
    
    accounts_text += "\nবিবরণ দেখতে অ্যাকাউন্ট বেছে নিন বা নতুন যোগ করুন:"
    
    bot.edit_message_text(
        accounts_text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=get_site_accounts_menu(site_key)
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("view_account_"))
def view_account_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    data = call.data.replace("view_account_", "")
    parts = data.rsplit("_", 1)
    if len(parts) < 2:
        return
    
    site_key, account_id = parts[0], parts[1]
    account = get_account_by_id(site_key, account_id)
    
    if not account:
        bot.answer_callback_query(call.id, "❌ অ্যাকাউন্ট পাওয়া যায়নি", show_alert=True)
        return
    
    site_name = SETTINGS[site_key]["name"]
    full_id = account.get("id", "")
    
    account_text = (
        f"👤 <b>অ্যাকাউন্টের বিবরণ - {site_name}</b>\n\n"
        f"📛 <b>ইউজারনেম:</b> <code>{account.get('username', 'N/A')}</code>\n"
        f"🔑 <b>পাসওয়ার্ড:</b> <code>{account.get('password', 'N/A')}</code>\n"
        f"🆔 <b>ID:</b> <code>{full_id[:8]}...</code>\n"
    )
    
    bot.edit_message_text(
        account_text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=get_account_details_menu(site_key, full_id)
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("add_account_"))
def add_account_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    site_key = call.data.replace("add_account_", "")
    site_name = SETTINGS[site_key]["name"]
    
    user_states[user_id] = {"action": "add_account_username", "site_key": site_key}
    
    bot.send_message(
        call.message.chat.id,
        f"➕ <b>নতুন অ্যাকাউন্ট যোগ - {site_name}</b>\n\n"
        f"📝 ধাপ 1/2: ইউজারনেম পাঠান (Username):",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_account_"))
def delete_account_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    data = call.data.replace("delete_account_", "")
    parts = data.rsplit("_", 1)
    if len(parts) < 2:
        return
    
    site_key, account_id = parts[0], parts[1]
    site_name = SETTINGS[site_key]["name"]
    account = get_account_by_id(site_key, account_id)
    
    if not account:
        bot.answer_callback_query(call.id, "❌ অ্যাকাউন্ট পাওয়া যায়নি", show_alert=True)
        return
    
    accounts = get_site_accounts(site_key)
    if len(accounts) <= 1:
        bot.answer_callback_query(
            call.id, 
            "⚠️ একমাত্র অ্যাকাউন্টটি মুছে ফেলা যাবে না!\nপ্রতিটি সাইটে কমপক্ষে একটি অ্যাকাউন্ট থাকতে হবে।", 
            show_alert=True
        )
        return
    
    username = account.get("username", "N/A")
    full_id = account.get("id", "")
    success = delete_account(site_key, full_id)
    
    if success:
        bot.answer_callback_query(call.id, f"✅ অ্যাকাউন্ট মুছে ফেলা হয়েছে {username} সফলভাবে!", show_alert=True)
        
        accounts = get_site_accounts(site_key)
        accounts_text = f"👥 <b>অ্যাকাউন্ট {site_name}</b>\n\n"
        accounts_text += f"📊 অ্যাকাউন্ট সংখ্যা: {len(accounts)}\n\n"
        for idx, acc in enumerate(accounts, 1):
            acc_username = acc.get("username", "N/A")
            accounts_text += f"{idx}. 👤 <code>{acc_username}</code>\n"
        accounts_text += "\nবিবরণ দেখতে অ্যাকাউন্ট বেছে নিন বা নতুন যোগ করুন:"
        
        bot.edit_message_text(
            accounts_text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="HTML",
            reply_markup=get_site_accounts_menu(site_key)
        )
    else:
        bot.answer_callback_query(call.id, "❌ অ্যাকাউন্ট মুছতে ব্যর্থ", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "admin_sites_menu" or call.data == "admin")
def sites_menu_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "⛔️ আপনার প্রবেশাধিকার নেই", show_alert=True)
        return
    
    if call.data == "admin":
        bot.edit_message_text(
            "🎛 <b>অ্যাডমিন প্যানেল</b>\n\nপ্রয়োজনীয় অপশন বেছে নিন:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="HTML",
            reply_markup=get_admin_menu()
        )
    else:
        bot.edit_message_text(
            "⚙️ <b>সাইট সেটিংস</b>\n\nসেটিংস এডিট করতে সাইট বেছে নিন:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="HTML",
            reply_markup=get_sites_menu()
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith("site_config_"))
def site_config_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    site_key = call.data.replace("site_config_", "")
    site_config = SETTINGS.get(site_key, {})
    site_name = site_config.get("name", site_key)
    accounts = get_site_accounts(site_key)
    
    if len(accounts) > 1:
        accounts_text = f"⚙️ <b>সেটিংস {site_name}</b>\n\n"
        accounts_text += f"👥 <b>অ্যাকাউন্ট সংখ্যা:</b> {len(accounts)}\n\n"
        accounts_text += "যে অ্যাকাউন্ট নিয়ন্ত্রণ করতে চান সেটি বেছে নিন:"
        
        bot.edit_message_text(
            accounts_text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="HTML",
            reply_markup=get_site_accounts_selection_menu(site_key)
        )
    else:
        first_account = accounts[0] if accounts else {"username": "N/A", "password": "", "id": ""}
        account_id = first_account.get("id", "")
        
        info_text = (
            f"⚙️ <b>সেটিংস {site_name}</b>\n\n"
            f"👤 <b>অ্যাকাউন্ট:</b> <code>{first_account.get('username', 'N/A')}</code>\n"
            f"🔑 <b>পাসওয়ার্ড:</b> <code>{'*' * len(first_account.get('password', ''))}</code>\n"
            f"⏱ <b>অনুসন্ধানের বিরতি:</b> {site_config.get('check_interval', 0)} সেকেন্ড\n"
            f"⏳ <b>অপেক্ষার সময়:</b> {site_config.get('timeout', 0)} সেকেন্ড\n\n"
            f"প্রয়োজনীয় অপশন বেছে নিন:"
        )
        
        bot.edit_message_text(
            info_text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="HTML",
            reply_markup=get_site_config_menu(site_key, account_id)
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith("select_account_config_"))
def select_account_config_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    data = call.data.replace("select_account_config_", "")
    parts = data.rsplit("_", 1)
    if len(parts) < 2:
        return
    
    site_key, account_id = parts[0], parts[1]
    site_config = SETTINGS.get(site_key, {})
    site_name = site_config.get("name", site_key)
    account = get_account_by_id(site_key, account_id)
    
    if not account:
        bot.answer_callback_query(call.id, "❌ অ্যাকাউন্ট পাওয়া যায়নি", show_alert=True)
        return
    
    info_text = (
        f"⚙️ <b>সেটিংস {site_name}</b>\n\n"
        f"👤 <b>অ্যাকাউন্ট:</b> <code>{account.get('username', 'N/A')}</code>\n"
        f"🔑 <b>পাসওয়ার্ড:</b> <code>{'*' * len(account.get('password', ''))}</code>\n"
        f"⏱ <b>অনুসন্ধানের বিরতি:</b> {site_config.get('check_interval', 0)} সেকেন্ড\n"
        f"⏳ <b>অপেক্ষার সময়:</b> {site_config.get('timeout', 0)} সেকেন্ড\n\n"
        f"প্রয়োজনীয় অপশন বেছে নিন:"
    )
    
    bot.edit_message_text(
        info_text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=get_site_config_menu(site_key, account_id)
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("site_change_user_"))
def site_change_user_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    data_parts = call.data.replace("site_change_user_", "").rsplit("_", 1)
    site_key = data_parts[0]
    account_id = data_parts[1] if len(data_parts) > 1 else None
    
    # Handle TimeSMS special case for single account sites or direct access
    if not account_id and site_key == "TimeSMS":
        accounts = get_site_accounts(site_key)
        if accounts:
            account = accounts[0]
            account_id = account.get("id", "")[:8]
        else:
            bot.answer_callback_query(call.id, "❌ কোনো অ্যাকাউন্ট নিবন্ধিত নেই", show_alert=True)
            return

    account = get_account_by_id(site_key, account_id) if account_id else None
    
    if not account:
        bot.answer_callback_query(call.id, "❌ অ্যাকাউন্ট পাওয়া যায়নি", show_alert=True)
        return
    
    full_id = account.get("id", "")
    
    user_states[user_id] = {
        "action": "change_site_username",
        "site_key": site_key,
        "account_id": full_id
    }
    
    bot.send_message(
        call.message.chat.id,
        f"👤 <b>ইউজারনেম পরিবর্তন - {site_name}</b>\n\n"
        f"বর্তমান অ্যাকাউন্ট: <code>{account.get('username', 'N/A')}</code>\n\n"
        f"নতুন ইউজারনেম পাঠান:",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("site_change_pass_"))
def site_change_pass_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    data_parts = call.data.replace("site_change_pass_", "").rsplit("_", 1)
    # Handle TimeSMS special case for single account sites or direct access
    if not account_id and site_key == "TimeSMS":
        accounts = get_site_accounts(site_key)
        if accounts:
            account = accounts[0]
            account_id = account.get("id", "")[:8]
        else:
            bot.answer_callback_query(call.id, "❌ কোনো অ্যাকাউন্ট নিবন্ধিত নেই", show_alert=True)
            return

    account = get_account_by_id(site_key, account_id) if account_id else None
    
    if not account:
        bot.answer_callback_query(call.id, "❌ অ্যাকাউন্ট পাওয়া যায়নি", show_alert=True)
        return
    
    full_id = account.get("id", "")
    
    user_states[user_id] = {
        "action": "change_site_password",
        "site_key": site_key,
        "account_id": full_id
    }
    
    bot.send_message(
        call.message.chat.id,
        f"🔑 <b>পাসওয়ার্ড পরিবর্তন - {site_name}</b>\n\n"
        f"অ্যাকাউন্ট: <code>{account.get('username', 'N/A')}</code>\n\n"
        f"নতুন পাসওয়ার্ড পাঠান:",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("site_change_interval_"))
def site_change_interval_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    site_key = call.data.replace("site_change_interval_", "")
    site_name = SETTINGS[site_key]["name"]
    current = SETTINGS[site_key]["check_interval"]
    
    user_states[user_id] = {"action": "change_site_interval", "site_key": site_key}
    
    bot.send_message(
        call.message.chat.id,
        f"⏱ <b>অনুসন্ধানের বিরতি পরিবর্তন - {site_name}</b>\n\n"
        f"📊 বর্তমান বিরতি: {current} সেকেন্ড\n\n"
        f"নতুন বিরতি সেকেন্ডে পাঠান:",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("site_change_timeout_"))
def site_change_timeout_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    site_key = call.data.replace("site_change_timeout_", "")
    site_name = SETTINGS[site_key]["name"]
    current = SETTINGS[site_key]["timeout"]
    
    user_states[user_id] = {"action": "change_site_timeout", "site_key": site_key}
    
    bot.send_message(
        call.message.chat.id,
        f"⏳ <b>অপেক্ষার সময় পরিবর্তন - {site_name}</b>\n\n"
        f"📊 বর্তমান সময়: {current} সেকেন্ড\n\n"
        f"নতুন সময় সেকেন্ডে পাঠান:",
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("site_test_login_"))
def site_test_login_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    data_parts = call.data.replace("site_test_login_", "").rsplit("_", 1)
    # Handle TimeSMS special case for single account sites or direct access
    if not account_id and site_key == "TimeSMS":
        accounts = get_site_accounts(site_key)
        if accounts:
            account = accounts[0]
            account_id = account.get("id", "")[:8]
        else:
            bot.answer_callback_query(call.id, "❌ কোনো অ্যাকাউন্ট নিবন্ধিত নেই", show_alert=True)
            return

    account = get_account_by_id(site_key, account_id) if account_id else None
    
    if not account:
        bot.answer_callback_query(call.id, "❌ অ্যাকাউন্ট পাওয়া যায়নি", show_alert=True)
        return
    
    bot.answer_callback_query(call.id, f"🔄 লগইন টেস্ট চলছে: {account.get('username')}...")
    
    bot.send_message(
        call.message.chat.id,
        f"🔓 <b>লগইন টেস্ট - {site_name}</b>\n\n"
        f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n\n"
        f"⏳ সংযোগ ও যাচাই চলছে...",
        parse_mode="HTML"
    )
    
    Thread(target=test_site_login, args=(call.message.chat.id, site_key, account_id)).start()

@bot.callback_query_handler(func=lambda call: call.data.startswith("site_test_fetch_"))
def site_test_fetch_callback(call):
    user_id = call.from_user.id
    
    if not is_admin(user_id):
        return
    
    data_parts = call.data.replace("site_test_fetch_", "").rsplit("_", 1)
    # Handle TimeSMS special case for single account sites or direct access
    if not account_id and site_key == "TimeSMS":
        accounts = get_site_accounts(site_key)
        if accounts:
            account = accounts[0]
            account_id = account.get("id", "")[:8]
        else:
            bot.answer_callback_query(call.id, "❌ কোনো অ্যাকাউন্ট নিবন্ধিত নেই", show_alert=True)
            return

    account = get_account_by_id(site_key, account_id) if account_id else None
    
    if not account:
        bot.answer_callback_query(call.id, "❌ অ্যাকাউন্ট পাওয়া যায়নি", show_alert=True)
        return
    
    bot.answer_callback_query(call.id, f"🔄 সর্বশেষ কোড আনা হচ্ছে: {account.get('username')}...")
    
    bot.send_message(
        call.message.chat.id,
        f"📥 <b>কোড আনা টেস্ট - {site_name}</b>\n\n"
        f"👤 অ্যাকাউন্ট: <code>{account.get('username')}</code>\n\n"
        f"⏳ সর্বশেষ মেসেজ আনা হচ্ছে...",
        parse_mode="HTML"
    )
    
    Thread(target=test_site_fetch, args=(call.message.chat.id, site_key, account_id)).start()

@bot.callback_query_handler(func=lambda call: call.data.startswith("country_"))
def country_selection_callback(call):
    user_id = call.from_user.id
    lang = get_user_language(user_id)

    if not check_subscription(user_id):
        bot.answer_callback_query(call.id, "❌ Please subscribe to all channels first!", show_alert=True)
        return

    country_name = call.data.replace("country_", "")
    
    if country_name not in COUNTRIES:
        bot.answer_callback_query(call.id, "❌ Country not found!", show_alert=True)
        return

    country_info = COUNTRIES.get(country_name, {})
    flag = country_info.get("flag", "🌍")

    number = get_random_number(country_name)

    if not number:
        bot.answer_callback_query(call.id, "❌ No numbers available for this country!", show_alert=True)
        return

    service_type = country_info.get("service", "WS")

    display_number = f'+{number.lstrip("+")}'

    old_data = USERS.get(str(user_id), {})
    USERS[str(user_id)] = {
        "selected_country": country_name,
        "selected_number": number,
        "flag": flag,
        "service": service_type,
        "platform": "General",
        "joined": str(datetime.now()),
        "activations": old_data.get("activations", 0),
        "language": old_data.get("language", "ar"),
        "join_date": old_data.get("join_date", datetime.now().strftime('%Y-%m-%d'))
    }
    save_users()

    bot.delete_message(call.message.chat.id, call.message.message_id)

    links = load_button_links()
    markup = InlineKeyboardMarkup(row_width=1)
    change_number_text = "🔄 নম্বর পরিবর্তন" if lang == "ar" else "🔄 Change Number"
    change_country_text = "🌍 দেশ পরিবর্তন" if lang == "ar" else "🌍 Change Country"
    change_number = InlineKeyboardButton(change_number_text, callback_data="change_number")
    change_country = InlineKeyboardButton(change_country_text, callback_data="choose_country")
    markup.add(change_number)
    markup.add(change_country)
    
    group_link_text = "📢 বটের গ্রুপ" if lang == "ar" else "📢 Group Link"
    group_link_btn = InlineKeyboardButton(group_link_text, url=links.get("group_link", "https://t.me/alorhawa"))
    markup.add(group_link_btn)
    
    back_text = "🔙 মূল মেনু" if lang == "ar" else "🔙 Back to Main"
    markup.add(InlineKeyboardButton(back_text, callback_data="back_to_main"))

   
    user_lang = get_user_language(user_id)
    platform = USERS.get(str(user_id), {}).get("platform", "General")
    country_info = COUNTRIES.get(country_name, {})
    country_code = country_info.get("code", "")
    localized_country_name, _, _ = detect_country_from_number(country_code, user_id)
    
    if user_lang == "ar":
        msg_text = (
            f"<tg-emoji emoji-id='5972010570340112281'>😀</tg-emoji> <b>নম্বর সফলভাবে বাছাই হয়েছে!</b>\n\n"
            f"<tg-emoji emoji-id='5224450179368767019'>🌎</tg-emoji> <b>দেশ:</b> {flag} {localized_country_name}\n"
            f"<tg-emoji emoji-id='5782668844061430712'>🗣</tg-emoji> <b>প্ল্যাটফর্ম:</b> {platform}\n"
            f"<tg-emoji emoji-id='5453965363286925977'>📞</tg-emoji> <b>নম্বর:</b> <code>{display_number}</code>\n\n"
            f"<tg-emoji emoji-id='5458603043203327669'>😀</tg-emoji> মেসেজ আসলে স্বয়ংক্রিয়ভাবে পাবেন"
        )
    else:
        msg_text = (
            f"<tg-emoji emoji-id='5972010570340112281'>😀</tg-emoji> <b>Number selected successfully!</b>\n\n"
            f"<tg-emoji emoji-id='5224450179368767019'>🌎</tg-emoji> <b>Country:</b> {flag} {localized_country_name}\n"
            f"<tg-emoji emoji-id='5782668844061430712'>🗣</tg-emoji> <b>Platform:</b> {platform}\n"
            f"<tg-emoji emoji-id='5453965363286925977'>📞</tg-emoji> <b>Number:</b> <code>{display_number}</code>\n\n"
            f"🔔 You will receive messages automatically when they arrive"
        )

    bot.send_message(
        call.message.chat.id,
        msg_text,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "change_number")
def change_number_callback(call):
    user_id = call.from_user.id
    lang = get_user_language(user_id)

    if not check_subscription(user_id):
        bot.answer_callback_query(call.id, "❌ Please subscribe to all channels first!", show_alert=True)
        return

    user_data = USERS.get(str(user_id))
    if not user_data:
        bot.answer_callback_query(call.id, "❌ User data not found!", show_alert=True)
        return
        
    country_name = user_data.get("country") or user_data.get("selected_country")
    if not country_name:
        bot.answer_callback_query(call.id, "❌ No country selected!", show_alert=True)
        return
    number = get_random_number(country_name)

    if not number:
        bot.answer_callback_query(call.id, "❌ No numbers available for this country!", show_alert=True)
        return

    country_info = COUNTRIES.get(country_name, {})
    service_type = country_info.get("service", "WS")
    flag = country_info.get("flag", "🌍")

    display_number = f'+{number.lstrip("+")}'

    USERS[str(user_id)]["selected_number"] = number
    save_users()

    links = load_button_links()
    markup = InlineKeyboardMarkup(row_width=1)
    change_number_text = "🔄 নম্বর পরিবর্তন" if lang == "ar" else "🔄 Change Number"
    change_country_text = "🌍 দেশ পরিবর্তন" if lang == "ar" else "🌍 Change Country"
    change_number = InlineKeyboardButton(change_number_text, callback_data="change_number")
    change_country = InlineKeyboardButton(change_country_text, callback_data="choose_country")
    markup.add(change_number)
    markup.add(change_country)
    
    group_link_text = "📢 বটের গ্রুপ" if lang == "ar" else "📢 Group Link"
    group_link_btn = InlineKeyboardButton(group_link_text, url=links.get("group_link", "https://t.me/alorhawa"))
    markup.add(group_link_btn)
    
    back_text = "🔙 মূল মেনু" if lang == "ar" else "🔙 Back to Main"
    markup.add(InlineKeyboardButton(back_text, callback_data="back_to_main"))

    
    user_lang = get_user_language(user_id)
    platform = USERS.get(str(user_id), {}).get("platform", "General")
    country_info = COUNTRIES.get(country_name, {})
    country_code = country_info.get("code", "")
    localized_country_name, _, _ = detect_country_from_number(country_code, user_id)
    
    if user_lang == "ar":
        msg_text = (
            f"<tg-emoji emoji-id='5972010570340112281'>😀</tg-emoji> <b>নম্বর সফলভাবে বাছাই হয়েছে!</b>\n\n"
            f"<tg-emoji emoji-id='5224450179368767019'>🌎</tg-emoji> <b>দেশ:</b> {flag} {localized_country_name}\n"
            f"<tg-emoji emoji-id='5782668844061430712'>🗣</tg-emoji> <b>প্ল্যাটফর্ম:</b> {platform}\n"
            f"<tg-emoji emoji-id='5453965363286925977'>📞</tg-emoji> <b>নম্বর:</b> <code>{display_number}</code>\n\n"
            f"<tg-emoji emoji-id='5458603043203327669'>😀</tg-emoji> মেসেজ আসলে স্বয়ংক্রিয়ভাবে পাবেন"
        )
    else:
        msg_text = (
            f"✅ <b>Number selected successfully!</b>\n\n"
            f"🌍 <b>Country:</b> {flag} {localized_country_name}\n"
            f"<tg-emoji emoji-id='5782668844061430712'>🗣</tg-emoji> <b>Platform:</b> {platform}\n"
            f"<tg-emoji emoji-id='5453965363286925977'>📞</tg-emoji> <b>Number:</b> <code>{display_number}</code>\n\n"
            f"<tg-emoji emoji-id='5458603043203327669'>😀</tg-emoji> You will receive messages automatically when they arrive"
        )

    bot.edit_message_text(
        msg_text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

    changed_text = "✅ নম্বর পরিবর্তন হয়েছে!" if lang == "ar" else "✅ Number changed!"
    bot.answer_callback_query(call.id, changed_text)

@bot.callback_query_handler(func=lambda call: call.data.startswith("select_plt_"))
def select_platform_main_callback(call):
    user_id = call.from_user.id
    platform = call.data.replace("select_plt_", "")
    lang = get_user_language(user_id)
    
    markup = get_countries_for_platform(platform, user_id)
    if not markup:
        bot.answer_callback_query(call.id, "❌ No countries available for this platform!", show_alert=True)
        return
    
    title = f"🌍 <b>Choose Country for {platform}</b>" if lang != "ar" else f"🌍 <b>দেশ বেছে নিন: {platform}</b>"
    bot.edit_message_text(title, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "choose_country")
def choose_country_callback(call):
    user_id = call.from_user.id

    if not check_subscription(user_id):
        bot.answer_callback_query(call.id, "❌ Please subscribe to all channels first!", show_alert=True)
        return

    
    user_data = USERS.get(str(user_id), {})
    platform = user_data.get("platform")
    
    if platform and platform != "General":
        markup = get_countries_for_platform(platform, user_id)
        if markup:
            lang = get_user_language(user_id)
            settings = load_referral_settings()
            code_bonus = settings.get("code_bonus", 0.01)
            
            if lang == "ar":
                title = f"🌍 <b>দেশ বেছে নিন: {platform}</b>\n\n💰 আপনি পাবেন <b>${format_decimal(code_bonus)}</b> প্রতিটি কোড পেলে!"
            else:
                title = f"🌍 <b>Select Country for {platform}</b>\n\n💰 You'll earn <b>${format_decimal(code_bonus)}</b> for each code received!"

            bot.edit_message_text(title, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)
            return

    
    markup = get_platforms_list(user_id)

    if not markup:
        bot.answer_callback_query(call.id, "❌ No countries available!", show_alert=True)
        return

    lang = get_user_language(user_id)
    settings = load_referral_settings()
    code_bonus = settings.get("code_bonus", 0.01)
    
    if lang == "ar":
        title = f"🌍 <b>দেশ বেছে নিন</b>\n\n<tg-emoji emoji-id='6046356449938905522'>💰</tg-emoji> আপনি পাবেন <b>${format_decimal(code_bonus)}</b> প্রতিটি কোড পেলে!"
    else:
        title = f"🌍 <b>Select Country</b>\n\n<tg-emoji emoji-id='6046356449938905522'>💰</tg-emoji> You'll earn <b>${format_decimal(code_bonus)}</b> for each code received!"

    bot.edit_message_text(
        title,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("platform_"))
def select_platform_callback(call):
    user_id = call.from_user.id

    if not check_subscription(user_id):
        bot.answer_callback_query(call.id, "❌ Please subscribe to all channels first!", show_alert=True)
        return

    parts = call.data.split("_", 2)
    if len(parts) < 3:
        bot.answer_callback_query(call.id, "❌ Invalid selection!", show_alert=True)
        return
    
    country_name = parts[1]
    platform = parts[2]
    
    if country_name not in COUNTRIES:
        bot.answer_callback_query(call.id, "❌ Country not found!", show_alert=True)
        return
    
    country_info = COUNTRIES[country_name]
    selected_number = get_random_number(country_name)
    
    if not selected_number:
        bot.answer_callback_query(call.id, "❌ No numbers available for this country!", show_alert=True)
        return
    
    USERS[str(user_id)] = {
        "selected_number": selected_number,
        "selected_country": country_name,
        "country": country_name,
        "platform": platform,
        "joined": str(datetime.now()),
        "activations": USERS.get(str(user_id), {}).get("activations", 0),
        "language": USERS.get(str(user_id), {}).get("language", "ar")
    }
    save_users()
    
    country_flag = country_info.get("flag", "🌍")
    display_number = f'+{selected_number.lstrip("+")}'
    user_lang = get_user_language(user_id)
    localized_country_name, _, _ = detect_country_from_number(country_info.get("code", ""), user_id)
    
    if user_lang == "ar":
        msg_text = (
            f"<tg-emoji emoji-id='5972010570340112281'>😀</tg-emoji> <b>নম্বর সফলভাবে বাছাই হয়েছে!</b>\n\n"
            f"<tg-emoji emoji-id='5224450179368767019'>🌎</tg-emoji> <b>দেশ:</b> {country_flag} {localized_country_name}\n"
            f"<tg-emoji emoji-id='5782668844061430712'>🗣</tg-emoji> <b>প্ল্যাটফর্ম:</b> {platform}\n"
            f"<tg-emoji emoji-id='5453965363286925977'>📞</tg-emoji> <b>নম্বর:</b> <code>{display_number}</code>\n\n"
            f"<tg-emoji emoji-id='5458603043203327669'>😀</tg-emoji> <b>মেসেজ আসলে স্বয়ংক্রিয়ভাবে পাবেন</b>"
        )
    else:
        msg_text = (
            f"<tg-emoji emoji-id='5972010570340112281'>😀</tg-emoji> <b>Number selected successfully!</b>\n\n"
            f"<tg-emoji emoji-id='5224450179368767019'>🌎</tg-emoji> <b>Country:</b> {country_flag} {localized_country_name}\n"
            f"<tg-emoji emoji-id='5782668844061430712'>🗣</tg-emoji> <b>Platform:</b> {platform}\n"
            f"<tg-emoji emoji-id='5453965363286925977'>📞</tg-emoji> <b>Number:</b> <code>{display_number}</code>\n\n"
            f"<tg-emoji emoji-id='5458603043203327669'>😀</tg-emoji> <b>You will receive messages automatically when they arrive</b>"
        )
    
    bot.edit_message_text(
        msg_text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=create_message_buttons(user_id)
    )

@bot.message_handler(commands=["hom"])
def hom_command(msg):
    user_id = msg.from_user.id
    lang = get_user_language(user_id)
    
    
    if is_admin(user_id):
        
        settings = load_referral_settings()
        code_bonus = settings.get("code_bonus", 0.01)
        
        if lang == "ar":
            text = f"<tg-emoji emoji-id='5972277098830634724'>🚨</tg-emoji> <b>প্ল্যাটফর্ম বেছে নিন</b>\n\n<tg-emoji emoji-id='6046356449938905522'>💰</tg-emoji> আপনি পাবেন <b>${format_decimal(code_bonus)}</b> প্রতিটি কোড পেলে!"
        else:
            text = f"<tg-emoji emoji-id='5972277098830634724'>🚨</tg-emoji> <b>Choose Platform</b>\n\n<tg-emoji emoji-id='6046356449938905522'>💰</tg-emoji> You'll earn <b>${format_decimal(code_bonus)}</b> for each code received!"
            
        markup = get_platforms_list(user_id)
        bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=markup)
        return

    if is_banned(user_id):
        bot.reply_to(msg, t(user_id, "banned"))
        return

    text = t(user_id, "welcome")
    if not text: text = "🌐 <b>স্বাগতম!</b>"
    bot.send_message(
        msg.chat.id,
        text,
        parse_mode="HTML",
        reply_markup=get_main_menu_lang(user_id)
    )

def process_country_code_logic(msg, user_id, country_code, state):
    
    country_code = str(country_code).replace('+', '').strip()
    
   
    import phonenumbers
    from phonenumbers import COUNTRY_CODE_TO_REGION_CODE
    
    
    potential_code = ""
    for i in range(min(len(country_code), 4), 0, -1):
        prefix = country_code[:i]
        if int(prefix) in COUNTRY_CODE_TO_REGION_CODE:
            potential_code = prefix
            break
            
    if potential_code:
        country_code = potential_code

    if not country_code.isdigit():
        bot.reply_to(msg, "❌ দেশের কোডে শুধু সংখ্যা থাকতে হবে!")
        return

    temp_file = state.get("temp_file")
    if not temp_file or not os.path.exists(temp_file):
        bot.reply_to(msg, "❌ ফাইল পাওয়া যায়নি! অনুগ্রহ করে নতুন করে শুরু করুন।")
        if user_id in user_states: del user_states[user_id]
        return

    try:
        with open(temp_file, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception as e:
        bot.reply_to(msg, f"❌ ফাইল পড়তে ত্রুটি: {e}")
        return

    cleaned_numbers = []
    total_lines = 0
    rejected_lines = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue
        total_lines += 1
        first_part = line.split()[0] if line.split() else line
        digits_only = ''.join(c for c in first_part if c.isdigit())

        if digits_only.startswith(country_code) and len(digits_only) >= 8:
            cleaned_numbers.append(digits_only)
        else:
            rejected_lines += 1

    num_cleaned = len(cleaned_numbers)

    if num_cleaned == 0:
        bot.reply_to(
            msg,
            f"❌ <b>দেশের কোড দিয়ে শুরু হওয়া কোনো নম্বর পাওয়া যায়নি {country_code}!</b>\n\n"
            f"📊 মোট প্রসেস করা লাইন: {total_lines}\n"
            f"❌ বাতিল নম্বর: {rejected_lines}\n\n"
            f"<i>ফাইলের মান নিশ্চিত করুন</i>",
            parse_mode="HTML"
        )
        if os.path.exists(temp_file):
            os.remove(temp_file)
        if user_id in user_states: del user_states[user_id]
        return

    cleanup_old_numbers_files(country_code)
    
    cleaned_filename = f"numbers_{country_code}_{uuid.uuid4().hex[:8]}.txt"
    with open(cleaned_filename, "w", encoding="utf-8") as f:
        for num in cleaned_numbers:
            f.write(num + "\n")

    if os.path.exists(temp_file):
        os.remove(temp_file)

    user_states[user_id] = {
        "action": "na_add_country_name",
        "numbers_file": cleaned_filename,
        "country_code": country_code,
        "num_cleaned": num_cleaned,
        "total_lines": total_lines,
        "rejected_lines": rejected_lines
    }

    bot.reply_to(
        msg,
        f"✅ <b>ফাইল স্বয়ংক্রিয়ভাবে প্রসেস হয়েছে!</b>\n\n"
        f"📊 মোট লাইন: <b>{total_lines}</b>\n"
        f"✅ গ্রহণযোগ্য নম্বর: <b>{num_cleaned}</b>\n"
        f"🔢 শনাক্ত করা দেশের কোড: <b>+{country_code}</b>\n\n"
        f"🔍 <b>স্বয়ংক্রিয়ভাবে দেশ নির্ধারণ হচ্ছে...</b>",
        parse_mode="HTML"
    )

   
    country_name, flag, region_code = detect_country_from_number(country_code, user_id)
    
    
    lang = get_user_language(user_id)
    if lang == "ar":
       
        country_name_ar = geocoder.description_for_number(phonenumbers.parse("+" + country_code + "0000000"), "ar")
        if country_name_ar:
            country_name = country_name_ar

    user_states[user_id] = {
        "action": "na_add_country_platforms",
        "numbers_file": cleaned_filename,
        "country_code": country_code,
        "country_name": country_name,
        "num_cleaned": num_cleaned,
        "server": "GROUP", 
        "selected_platforms": []
    }
    
   
    lang = get_user_language(user_id)
    markup = InlineKeyboardMarkup(row_width=2)
    platforms = ["Facebook", "WhatsApp", "Telegram", "Instagram", "Twitter", "TikTok", "Discord", "Gmail"]
    for p in platforms:
        markup.add(InlineKeyboardButton(f"{p}", callback_data=f"na_add_country_plt_{p}"))
    
    edit_name_text = "✏️ নাম এডিট" if lang == "ar" else "✏️ Edit Name"
    confirm_text = "✅ সম্পন্ন" if lang == "ar" else "✅ Continue"
    
    markup.add(
        InlineKeyboardButton(edit_name_text, callback_data="na_add_country_edit_name"),
        InlineKeyboardButton(confirm_text, callback_data="na_add_country_finish")
    )
    
    bot.send_message(
        msg.chat.id,
        f"🌍 দেশ নির্ধারণ হয়েছে: <b>{flag} {country_name} (+{country_code})</b>\n\n"
        f"📱 এই নম্বরগুলো যে প্ল্যাটফর্মে কাজ করে সেগুলো বেছে নিন:",
        parse_mode="HTML",
        reply_markup=markup
    )
    return

@bot.message_handler(content_types=["text", "document", "photo", "video", "audio", "voice", "sticker"])
def handle_messages(msg):
    user_id = msg.from_user.id
    
    if msg.chat.type != "private":
        return

    if user_id not in user_states and user_id not in broadcast_state:
        return

    state = user_states.get(user_id, {})
    action = state.get("action")
    mode = state.get("mode")
    
    if mode == "add_numbers_admin":
        if msg.content_type != "text":
            bot.reply_to(msg, "❌ অনুগ্রহ করে সংখ্যার আইডি পাঠান!")
            return
        
        try:
            new_admin_id = int(msg.text.strip())
        except ValueError:
            bot.reply_to(msg, "❌ আইডি অবশ্যই সংখ্যা হতে হবে!")
            return
        
        if new_admin_id in NUMBERS_ADMINS:
            bot.reply_to(msg, "⚠️ এই ইউজার আগেই নম্বর অ্যাডমিন!")
        else:
            NUMBERS_ADMINS.append(new_admin_id)
            save_numbers_admins()
            bot.reply_to(msg, f"✅ যোগ করা হয়েছে <code>{new_admin_id}</code> নম্বর অ্যাডমিন হিসেবে!", parse_mode="HTML")
        
        del user_states[user_id]
        return
    
    elif action == "na_add_country_edit_name_input":
        new_name = msg.text.strip()
        if not new_name:
            bot.reply_to(msg, "❌ অনুগ্রহ করে সঠিক নাম পাঠান!")
            return
        
        state["country_name"] = new_name
        
        lang = get_user_language(user_id)
        markup = InlineKeyboardMarkup(row_width=2)
        platforms = ["Facebook", "WhatsApp", "Telegram", "Instagram", "Twitter", "TikTok", "Discord", "Gmail"]
        for p in platforms:
            prefix = "✅ " if p in state.get("selected_platforms", []) else ""
            markup.add(InlineKeyboardButton(f"{prefix}{p}", callback_data=f"na_add_country_plt_{p}"))
        
        edit_name_text = "✏️ নাম এডিট" if lang == "ar" else "✏️ Edit Name"
        confirm_text = "✅ সম্পন্ন" if lang == "ar" else "✅ Continue"
        
        markup.add(
            InlineKeyboardButton(edit_name_text, callback_data="na_add_country_edit_name"),
            InlineKeyboardButton(confirm_text, callback_data="na_add_country_finish")
        )
        
        bot.send_message(
            msg.chat.id,
            f"✅ নাম আপডেট হয়ে হয়েছে: <b>{new_name}</b>\n\n"
            f"📱 এই নম্বরগুলো যে প্ল্যাটফর্মে কাজ করে সেগুলো বেছে নিন:",
            parse_mode="HTML",
            reply_markup=markup
        )
        state["action"] = "na_add_country_platforms"
        return

    elif action == "na_add_country_paste":
        if msg.content_type != "text":
            bot.reply_to(msg, "❌ অনুগ্রহ করে নম্বরগুলো টেক্সট হিসেবে পাঠান!")
            return
        
        text = msg.text.strip()
        numbers_raw = re.findall(r'\d+', text)
        
        if not numbers_raw:
            bot.reply_to(msg, "❌ পাঠানো টেক্সটে কোনো নম্বর পাওয়া যায়নি!")
            return
        
        
        guessed_code = ""
        
        first_num_digits = "".join(filter(str.isdigit, numbers_raw[0])) if numbers_raw else ""
        
        if first_num_digits:
           
            for length in [3, 2, 1]:
                prefix = first_num_digits[:length]
               
                if prefix in ["966", "971", "965", "974", "973", "968", "212", "213", "216", "961", "962", "963", "964", "967", "249", "218", "222", "20", "7", "1", "44"]:
                    guessed_code = prefix
                    break
            if not guessed_code:
                guessed_code = first_num_digits[:2] 
        else:
            guessed_code = "218" 

        temp_filename = f"temp_{uuid.uuid4().hex[:8]}.txt"
        with open(temp_filename, "w", encoding="utf-8") as f:
            for num in numbers_raw:
                if len(num) >= 8:
                    f.write(num + "\n")
        
    
        state = {"temp_file": temp_filename, "paste_mode": True}
        process_country_code_logic(msg, user_id, guessed_code, state)
        return
    
    elif action == "na_add_country_file":
        if msg.content_type != "document":
            bot.reply_to(msg, "❌ অনুগ্রহ করে ফাইল পাঠান txt!")
            return

        try:
            file_info = bot.get_file(msg.document.file_id)
            if not file_info.file_path:
                bot.reply_to(msg, "❌ ফাইল লোডে ত্রুটি!")
                return
            downloaded_file = bot.download_file(file_info.file_path)
        except Exception as e:
            bot.reply_to(msg, f"❌ ফাইল লোডে ত্রুটি: {e}")
            return

        temp_filename = f"temp_{uuid.uuid4().hex[:8]}.txt"
        with open(temp_filename, "wb") as f:
            f.write(downloaded_file)

        
        try:
            with open(temp_filename, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
                all_numbers = re.findall(r'\d+', content)
                if all_numbers:
                   
                    likely_phones = [n for n in all_numbers if 8 <= len(n) <= 15]
                    if likely_phones:
                        
                        prefixes = {}
                        for num in likely_phones:
                           
                            for i in range(1, 4):
                                if len(num) > i:
                                    pref = num[:i]
                                    prefixes[pref] = prefixes.get(pref, 0) + 1
                        
                        
                        sorted_prefixes = sorted(prefixes.items(), key=lambda x: (x[1], len(x[0])), reverse=True)
                        guessed_code = sorted_prefixes[0][0] if sorted_prefixes else "20"
                    else:
                        guessed_code = "20"
                else:
                    guessed_code = "20"
        except Exception as e:
            print(f"Error guessing code: {e}")
            guessed_code = "20"

        state = {"temp_file": temp_filename}
        process_country_code_logic(msg, user_id, guessed_code, state)
        return

    elif action == "na_add_country_code":
        country_code = msg.text.strip()
        process_country_code_logic(msg, user_id, country_code, state)
        return

    elif action == "na_add_country_name":
        country_name = msg.text.strip()
        numbers_file = state.get("numbers_file")
        country_code = state.get("country_code")
        num_cleaned = state.get("num_cleaned")

        user_states[user_id] = {
            "action": "na_add_country_platforms",
            "numbers_file": numbers_file,
            "country_code": country_code,
            "country_name": country_name,
            "num_cleaned": num_cleaned,
            "server": "GROUP",
            "selected_platforms": []
        }
        
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("📘 Facebook", callback_data="na_add_country_plt_Facebook", style="primary"),
            InlineKeyboardButton("💬 WhatsApp", callback_data="na_add_country_plt_WhatsApp", style="success")
        )
        markup.add(
            InlineKeyboardButton("✈️ Telegram", callback_data="na_add_country_plt_Telegram", style="primary"),
            InlineKeyboardButton("📸 Instagram", callback_data="na_add_country_plt_Instagram", style="danger")
        )
        markup.add(
            InlineKeyboardButton("🐦 Twitter/X", callback_data="na_add_country_plt_Twitter", style="primary"),
            InlineKeyboardButton("📱 TikTok", callback_data="na_add_country_plt_TikTok", style="danger")
        )
        markup.add(
            InlineKeyboardButton("🎮 Discord", callback_data="na_add_country_plt_Discord", style="danger"),
            InlineKeyboardButton("📧 Gmail", callback_data="na_add_country_plt_Gmail", style="primary")
        )
        markup.add(
            InlineKeyboardButton("🌐 সব প্ল্যাটফর্ম", callback_data="na_add_country_plt_ALL", style="primary")
        )
        markup.add(InlineKeyboardButton("✅ নিশ্চিত করুন ও শেষ করুন", callback_data="na_add_country_finish", style="success"))
        markup.add(InlineKeyboardButton("❌ বাতিল", callback_data="numbers_admin_panel", style="danger"))

        bot.reply_to(
            msg,
            f"✅ <b>ধাপ 3/3 - প্ল্যাটফর্ম বাছাই</b>\n\n"
            f"🌍 দেশ: <b>{country_name}</b>\n"
            f"🔢 দেশের কোড: <b>{country_code}</b>\n"
            f"📊 নম্বরের সংখ্যা: <b>{num_cleaned}</b>\n\n"
            f"📱 <b>বাছাই করা প্ল্যাটফর্ম:</b> নেই\n\n"
            f"এই নম্বরগুলো যে প্ল্যাটফর্মে কাজ করে সেগুলো বেছে নিন:",
            parse_mode="HTML",
            reply_markup=markup
        )
        return
    
    elif mode == "na_ban_user":
        if msg.content_type != "text":
            bot.reply_to(msg, "❌ অনুগ্রহ করে সংখ্যার আইডি পাঠান!")
            return
        
        try:
            ban_id = int(msg.text.strip())
        except ValueError:
            bot.reply_to(msg, "❌ আইডি অবশ্যই সংখ্যা হতে হবে!")
            return
        
        if ban_id in BANNED:
            bot.reply_to(msg, "⚠️ এই ইউজার আগেই ব্যান করা!")
        else:
            BANNED.append(ban_id)
            save_banned()
            bot.reply_to(msg, f"✅ ইউজারকে ব্যান করা হয়েছে <code>{ban_id}</code>!", parse_mode="HTML")
        
        del user_states[user_id]
        return
    
    elif mode == "na_unban_user":
        if msg.content_type != "text":
            bot.reply_to(msg, "❌ অনুগ্রহ করে সংখ্যার আইডি পাঠান!")
            return
        
        try:
            unban_id = int(msg.text.strip())
        except ValueError:
            bot.reply_to(msg, "❌ আইডি অবশ্যই সংখ্যা হতে হবে!")
            return
        
        if unban_id not in BANNED:
            bot.reply_to(msg, "⚠️ এই ইউজার ব্যান করা নেই!")
        else:
            BANNED.remove(unban_id)
            save_banned()
            bot.reply_to(msg, f"✅ ইউজার আনব্যান করা হয়েছে <code>{unban_id}</code>!", parse_mode="HTML")
        
        del user_states[user_id]
        return
    
    if user_id in broadcast_state:
        bc_mode = broadcast_state[user_id].get("mode")
        
        if bc_mode == "na_global_broadcast":
            success = 0
            failed = 0
            
            for uid in USERS.keys():
                try:
                    bot.copy_message(int(uid), msg.chat.id, msg.message_id)
                    success += 1
                except:
                    failed += 1
            
            bot.reply_to(msg, f"✅ সবার কাছে ব্রডকাস্ট পাঠানো হয়েছে!\n\n📊 সফল: {success}\n❌ ব্যর্থ: {failed}")
            del broadcast_state[user_id]
            return

    elif action == "na_add_country_file":
        if msg.content_type != "document":
            bot.reply_to(msg, "❌ অনুগ্রহ করে ফাইল পাঠান txt!")
            return

        try:
            file_info = bot.get_file(msg.document.file_id)
            if not file_info.file_path:
                bot.reply_to(msg, "❌ ফাইল লোডে ত্রুটি!")
                return
            downloaded_file = bot.download_file(file_info.file_path)
        except Exception as e:
            bot.reply_to(msg, f"❌ ফাইল লোডে ত্রুটি: {e}")
            return

        temp_filename = f"temp_{uuid.uuid4().hex[:8]}.txt"

        with open(temp_filename, "wb") as f:
            f.write(downloaded_file)

        user_states[user_id] = {"action": "na_add_country_code", "temp_file": temp_filename}

        bot.reply_to(
            msg,
            "✅ <b>ফাইল সফলভাবে আপলোড হয়েছে!</b>\n\n"
            "📝 <b>ধাপ 2/4</b>\n\n"
            "দেশের কোড পাঠান (উদাহরণ: 880 বাংলাদেশ, 91 ভারত, 1 আমেরিকা)\n\n"
            "<i>শুধু এই দেশের কোড দিয়ে শুরু হওয়া নম্বরগুলো রাখা হবে</i>",
            parse_mode="HTML"
        )
        return

    elif action == "na_add_country_name":
        country_name = msg.text.strip()
        numbers_file = state.get("numbers_file")
        country_code = state.get("country_code")
        num_cleaned = state.get("num_cleaned")

        user_states[user_id] = {
            "action": "na_add_country_platforms",
            "numbers_file": numbers_file,
            "country_code": country_code,
            "country_name": country_name,
            "num_cleaned": num_cleaned,
            "server": "GROUP",
            "selected_platforms": []
        }
        
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("📘 Facebook", callback_data="na_add_country_plt_Facebook", style="primary"),
            InlineKeyboardButton("💬 WhatsApp", callback_data="na_add_country_plt_WhatsApp", style="success")
        )
        markup.add(
            InlineKeyboardButton("✈️ Telegram", callback_data="na_add_country_plt_Telegram", style="danger"),
            InlineKeyboardButton("📸 Instagram", callback_data="na_add_country_plt_Instagram", style="primary")
        )
        markup.add(
            InlineKeyboardButton("🐦 Twitter/X", callback_data="na_add_country_plt_Twitter", style="danger"),
            InlineKeyboardButton("📱 TikTok", callback_data="na_add_country_plt_TikTok", style="primary")
        )
        markup.add(
            InlineKeyboardButton("🎮 Discord", callback_data="na_add_country_plt_Discord", style="primary"),
            InlineKeyboardButton("📧 Gmail", callback_data="na_add_country_plt_Gmail", style="danger")
        )
        markup.add(
            InlineKeyboardButton("🌐 সব প্ল্যাটফর্ম", callback_data="na_add_country_plt_ALL", style="primary")
        )
        markup.add(InlineKeyboardButton("✅ নিশ্চিত করুন ও শেষ করুন", callback_data="na_add_country_finish", style="success"))
        markup.add(InlineKeyboardButton("❌ বাতিল", callback_data="numbers_admin_panel", style="danger"))

        bot.reply_to(
            msg,
            f"✅ <b>ধাপ 3/3 - প্ল্যাটফর্ম বাছাই</b>\n\n"
            f"🌍 দেশ: <b>{country_name}</b>\n"
            f"🔢 দেশের কোড: <b>{country_code}</b>\n"
            f"📊 নম্বরের সংখ্যা: <b>{num_cleaned}</b>\n\n"
            f"📱 <b>বাছাই করা প্ল্যাটফর্ম:</b> নেই\n\n"
            f"এই নম্বরগুলো যে প্ল্যাটফর্মে কাজ করে সেগুলো বেছে নিন:",
            parse_mode="HTML",
            reply_markup=markup
        )
        return

    elif action == "remove_country":
        country_name = msg.text.strip()

        if country_name in COUNTRIES:
            country_data = COUNTRIES[country_name]
            numbers_file = country_data.get("file", "")
            
            if numbers_file and os.path.exists(numbers_file):
                try:
                    os.remove(numbers_file)
                    print(f"🗑️ নম্বরের ফাইল মুছে ফেলা হয়েছে: {numbers_file}")
                except Exception as e:
                    print(f"⚠️ নম্বরের ফাইল মুছতে ত্রুটি {numbers_file}: {e}")
            
            del COUNTRIES[country_name]
            save_countries()
            del user_states[user_id]
            
            file_status = f"\n📄 নম্বরের ফাইল মুছে ফেলা হয়েছে: {numbers_file}" if numbers_file else ""
            bot.reply_to(msg, f"✅ দেশ মুছে ফেলা হয়েছে: {country_name}{file_status}")
        else:
            bot.reply_to(msg, f"❌ দেশ পাওয়া যায়নি: {country_name}")

    elif action == "add_channel":
        try:
            channel_input = msg.text.strip()
            if channel_input.startswith("https://t.me/"):
                channel_username = "@" + channel_input.replace("https://t.me/", "")
            elif channel_input.startswith("@"):
                channel_username = channel_input
            elif channel_input.startswith("-") or channel_input.isdigit():
                channel_username = channel_input
            else:
                channel_username = "@" + channel_input

            try:
                chat = bot.get_chat(channel_username)
                channel_id = chat.id
                
                if chat.username:
                    channel_url = f"https://t.me/{chat.username}"
                else:
                    channel_url = f"https://t.me/c/{str(channel_id)[4:]}/1"

                user_states[user_id] = {
                    "action": "add_channel_name_ar",
                    "channel_id": channel_id,
                    "channel_username": channel_username,
                    "channel_url": channel_url
                }
                bot.reply_to(msg, "📝 এখন বাটনে দেখানোর জন্য চ্যানেলের নাম পাঠান (বাংলায়):")
            except Exception as e:
                bot.reply_to(msg, f"❌ চ্যানেলে প্রবেশে ত্রুটি: {e}\n\nনিশ্চিত করুন যে:\n• বট চ্যানেলের অ্যাডমিন\n• লিংক বা আইডি সঠিক")
        except Exception as e:
            bot.reply_to(msg, f"❌ ত্রুটি: {e}")

    elif action == "add_channel_name_ar":
        name_ar = msg.text.strip()
        state["name_ar"] = name_ar
        user_states[user_id]["action"] = "add_channel_name_en"
        bot.reply_to(msg, "📝 এখন বাটনে দেখানোর জন্য চ্যানেলের নাম পাঠান (ইংরেজিতে):")

    elif action == "add_channel_name_en":
        name_en = msg.text.strip()
        channel_id = state.get("channel_id")
        channel_username = state.get("channel_username")
        channel_url = state.get("channel_url")
        name_ar = state.get("name_ar")

        CHANNELS.append({
            "name": name_en, 
            "name_ar": name_ar,
            "name_en": name_en,
            "id": channel_id,
            "username": channel_username,
            "url": channel_url
        })
        save_channels()
        del user_states[user_id]

        bot.reply_to(
            msg,
            f"✅ <b>চ্যানেল সফলভাবে যোগ হয়েছে!</b>\n\n"
            f"📢 নাম (বাংলা): {name_ar}\n"
            f"📢 নাম (ইংরেজি): {name_en}\n"
            f"🔗 আইডি: {channel_username}\n"
            f"🆔 ID: <code>{channel_id}</code>",
            parse_mode="HTML"
        )

    elif action == "remove_channel":
        try:
            index = int(msg.text.strip()) - 1

            if 0 <= index < len(CHANNELS):
                removed = CHANNELS.pop(index)
                save_channels()
                del user_states[user_id]
                bot.reply_to(msg, f"✅ চ্যানেল মুছে ফেলা হয়েছে: {removed['name']}")
            else:
                bot.reply_to(msg, "❌ নম্বর সঠিক নয়!")
        except ValueError:
            bot.reply_to(msg, "❌ অনুগ্রহ করে সঠিক সংখ্যা পাঠান!")

    elif action == "add_admin":
        if user_id != MAIN_ADMIN_ID:
            bot.reply_to(msg, "❌ দুঃখিত, শুধু মালিক অ্যাডমিন যোগ করতে পারেন!")
            return
        try:
            new_admin_id = int(msg.text.strip())

            if new_admin_id in ADMINS:
                bot.reply_to(msg, "⚠️ এই ইউজার আগেই অ্যাডমিন!")
                return

            ADMINS.append(new_admin_id)
            save_admins()
            del user_states[user_id]
            bot.reply_to(msg, f"✅ অ্যাডমিন সফলভাবে যোগ হয়েছে!\n\nID: <code>{new_admin_id}</code>", parse_mode="HTML")
        except ValueError:
            bot.reply_to(msg, "❌ ID সঠিক নয়!")

    elif action == "remove_admin":
        if user_id != MAIN_ADMIN_ID:
            bot.reply_to(msg, "❌ দুঃখিত, শুধু মালিক অ্যাডমিন মুছতে পারেন!")
            return
        try:
            target_id = int(msg.text.strip())
            if target_id == MAIN_ADMIN_ID:
                bot.reply_to(msg, "❌ মূল অ্যাডমিনকে (মালিক) মুছে ফেলা যাবে না!")
                return
            
            if target_id in ADMINS:
                ADMINS.remove(target_id)
                save_admins()
                del user_states[user_id]
                bot.reply_to(msg, f"✅ অ্যাডমিন সফলভাবে মুছে ফেলা হয়েছে!\n\nID: <code>{target_id}</code>", parse_mode="HTML")
            else:
                bot.reply_to(msg, "❌ এই ইউজার অ্যাডমিন নয়!")
        except ValueError:
            bot.reply_to(msg, "❌ ID সঠিক নয়!")

    elif action == "ban_user":
        try:
            ban_user_id = int(msg.text.strip())

            if ban_user_id in ADMINS:
                bot.reply_to(msg, "❌ অ্যাডমিনদের ব্যান করা যাবে না!")
                return

            if ban_user_id in BANNED:
                bot.reply_to(msg, "⚠️ এই ইউজার আগেই ব্যান করা!")
                return

            BANNED.append(ban_user_id)
            save_banned()
            del user_states[user_id]
            bot.reply_to(msg, f"✅ ইউজারকে ব্যান করা হয়েছে!\n\nID: <code>{ban_user_id}</code>", parse_mode="HTML")
        except ValueError:
            bot.reply_to(msg, "❌ ID সঠিক নয়!")

    elif action == "unban_user":
        try:
            unban_user_id = int(msg.text.strip())

            if unban_user_id in BANNED:
                BANNED.remove(unban_user_id)
                save_banned()
                del user_states[user_id]
                bot.reply_to(msg, f"✅ ইউজার আনব্যান করা হয়েছে!\n\nID: <code>{unban_user_id}</code>", parse_mode="HTML")
            else:
                bot.reply_to(msg, "❌ এই ইউজার ব্যান করা নেই!")
        except ValueError:
            bot.reply_to(msg, "❌ ID সঠিক নয়!")

    elif action == "set_otp_group":
        global OTP_GROUP
        try:
            group_id = int(msg.text.strip())
            OTP_GROUP = group_id
            save_otp_group()
            del user_states[user_id]
            bot.reply_to(msg, f"✅ গ্রুপ সেট করা হয়েছে OTP!\n\nID: <code>{group_id}</code>", parse_mode="HTML")
        except ValueError:
            bot.reply_to(msg, "❌ ID সঠিক নয়!")
    
    elif action == "edit_code_bonus":
        try:
            new_value = float(msg.text.strip())
            if new_value <= 0 or new_value > 10:
                bot.reply_to(msg, "❌ মান অবশ্যই 0.01 থেকে 10 এর মধ্যে হতে হবে!")
                return
            settings = load_referral_settings()
            settings["code_bonus"] = new_value
            save_referral_settings(settings)
            del user_states[user_id]
            bot.reply_to(msg, f"✅ কোড বোনাস আপডেট হয়েছে <b>${new_value}</b>", parse_mode="HTML")
        except ValueError:
            bot.reply_to(msg, "❌ অনুগ্রহ করে সঠিক সংখ্যা দিন!")
    
    elif action == "edit_referral_bonus":
        try:
            new_value = float(msg.text.strip())
            if new_value <= 0 or new_value > 100:
                bot.reply_to(msg, "❌ মান অবশ্যই 0.01 থেকে 100 এর মধ্যে হতে হবে!")
                return
            settings = load_referral_settings()
            settings["referral_bonus"] = new_value
            save_referral_settings(settings)
            del user_states[user_id]
            bot.reply_to(msg, f"✅ রেফারেল বোনাস আপডেট হয়েছে <b>${new_value}</b>", parse_mode="HTML")
        except ValueError:
            bot.reply_to(msg, "❌ অনুগ্রহ করে সঠিক সংখ্যা দিন!")
    
    elif action == "edit_codes_required":
        try:
            new_value = int(msg.text.strip())
            if new_value < 1 or new_value > 100:
                bot.reply_to(msg, "❌ সংখ্যা অবশ্যই 1 থেকে 100 এর মধ্যে হতে হবে!")
                return
            settings = load_referral_settings()
            settings["codes_required_for_referral"] = new_value
            save_referral_settings(settings)
            del user_states[user_id]
            bot.reply_to(msg, f"✅ প্রয়োজনীয় কোড সংখ্যা আপডেট হয়েছে <b>{new_value}</b>", parse_mode="HTML")
        except ValueError:
            bot.reply_to(msg, "❌ অনুগ্রহ করে সঠিক সংখ্যা দিন!")
    
    elif action == "edit_min_withdrawal":
        try:
            new_value = float(msg.text.strip())
            if new_value <= 0 or new_value > 1000:
                bot.reply_to(msg, "❌ মান অবশ্যই 0.01 থেকে 1000 এর মধ্যে হতে হবে!")
                return
            settings = load_referral_settings()
            settings["min_withdrawal"] = new_value
            save_referral_settings(settings)
            del user_states[user_id]
            bot.reply_to(msg, f"✅ সর্বনিম্ন উত্তোলন আপডেট হয়েছে <b>${new_value}</b>", parse_mode="HTML")
        except ValueError:
            bot.reply_to(msg, "❌ অনুগ্রহ করে সঠিক সংখ্যা দিন!")
    
    elif action == "admin_add_balance":
        try:
            parts = msg.text.strip().split()
            if len(parts) != 2:
                bot.reply_to(msg, "❌ ফরম্যাট ভুল! ব্যবহার করুন: USER_ID AMOUNT")
                return
            target_user_id = int(parts[0])
            amount = float(parts[1])
            if amount <= 0 or amount > 10000:
                bot.reply_to(msg, "❌ পরিমাণ অবশ্যই 0.01 থেকে 10000 এর মধ্যে হতে হবে!")
                return
            
            referrals_data = load_referrals()
            target_key = str(target_user_id)
            if target_key not in referrals_data:
                referrals_data[target_key] = {
                    "referred_by": None,
                    "referrals": [],
                    "active_referrals": 0,
                    "codes_received": 0,
                    "balance": 0.0,
                    "total_earned": 0.0
                }
            
            old_balance = referrals_data[target_key].get("balance", 0.0)
            referrals_data[target_key]["balance"] = old_balance + amount
            referrals_data[target_key]["total_earned"] = referrals_data[target_key].get("total_earned", 0.0) + amount
            save_referrals(referrals_data)
            del user_states[user_id]
            
            new_balance = referrals_data[target_key]["balance"]
            bot.reply_to(msg, f"✅ <b>ব্যালেন্স সফলভাবে যোগ হয়েছে!</b>\n\n👤 ইউজার: <code>{target_user_id}</code>\n💰 যোগ করা পরিমাণ: <b>${amount:.2f}</b>\n💵 আগের ব্যালেন্স: <b>${old_balance:.2f}</b>\n💵 নতুন ব্যালেন্স: <b>${new_balance:.2f}</b>", parse_mode="HTML")
            
            try:
                target_lang = get_user_language(target_user_id)
                if target_lang == "ar":
                    notify_msg = f"💰 <b>ব্যালেন্স যোগ হয়েছে!</b>\n\nযোগ করা হয়েছে <b>${amount:.2f}</b> অ্যাডমিন আপনার ব্যালেন্সে যোগ করেছেন।\n💵 আপনার বর্তমান ব্যালেন্স: <b>${new_balance:.2f}</b>"
                else:
                    notify_msg = f"💰 <b>Balance Added!</b>\n\n<b>${amount:.2f}</b> has been added to your balance by admin.\n💵 Your current balance: <b>${new_balance:.2f}</b>"
                bot.send_message(target_user_id, notify_msg, parse_mode="HTML")
            except:
                pass
        except ValueError:
            bot.reply_to(msg, "❌ ফরম্যাট ভুল! ব্যবহার করুন: USER_ID AMOUNT\n\nউদাহরণ: 123456789 5.00")
    
    elif action == "admin_subtract_balance":
        try:
            parts = msg.text.strip().split()
            if len(parts) != 2:
                bot.reply_to(msg, "❌ ফরম্যাট ভুল! ব্যবহার করুন: USER_ID AMOUNT")
                return
            target_user_id = int(parts[0])
            amount = float(parts[1])
            if amount <= 0 or amount > 10000:
                bot.reply_to(msg, "❌ পরিমাণ অবশ্যই 0.01 থেকে 10000 এর মধ্যে হতে হবে!")
                return
            
            referrals_data = load_referrals()
            target_key = str(target_user_id)
            if target_key not in referrals_data:
                bot.reply_to(msg, "❌ ইউজার রেফারেল সিস্টেমে নেই!")
                del user_states[user_id]
                return
            
            old_balance = referrals_data[target_key].get("balance", 0.0)
            if amount > old_balance:
                bot.reply_to(msg, f"❌ ইউজারের ব্যালেন্স যথেষ্ট নয়!\n💵 তার বর্তমান ব্যালেন্স: ${old_balance:.2f}")
                return
            
            referrals_data[target_key]["balance"] = old_balance - amount
            save_referrals(referrals_data)
            del user_states[user_id]
            
            new_balance = referrals_data[target_key]["balance"]
            bot.reply_to(msg, f"✅ <b>ব্যালেন্স সফলভাবে কর্তন হয়েছে!</b>\n\n👤 ইউজার: <code>{target_user_id}</code>\n💰 কর্তন করা পরিমাণ: <b>${amount:.2f}</b>\n💵 আগের ব্যালেন্স: <b>${old_balance:.2f}</b>\n💵 নতুন ব্যালেন্স: <b>${new_balance:.2f}</b>", parse_mode="HTML")
            
            try:
                target_lang = get_user_language(target_user_id)
                if target_lang == "ar":
                    notify_msg = f"⚠️ <b>ব্যালেন্স কর্তন হয়েছে!</b>\n\nকর্তন করা হয়েছে <b>${amount:.2f}</b> অ্যাডমিন আপনার ব্যালেন্স থেকে কেটেছেন।\n💵 আপনার বর্তমান ব্যালেন্স: <b>${new_balance:.2f}</b>"
                else:
                    notify_msg = f"⚠️ <b>Balance Deducted!</b>\n\n<b>${amount:.2f}</b> has been deducted from your balance by admin.\n💵 Your current balance: <b>${new_balance:.2f}</b>"
                bot.send_message(target_user_id, notify_msg, parse_mode="HTML")
            except:
                pass
        except ValueError:
            bot.reply_to(msg, "❌ ফরম্যাট ভুল! ব্যবহার করুন: USER_ID AMOUNT\n\nউদাহরণ: 123456789 5.00")
    
    elif action == "edit_welcome_ar":
        new_message = msg.text.strip()
        if len(new_message) < 10:
            bot.reply_to(msg, "❌ মেসেজ খুব ছোট!")
            return
        messages = load_welcome_messages()
        messages["ar"] = new_message
        save_welcome_messages(messages)
        del user_states[user_id]
        bot.reply_to(msg, "✅ বাংলা স্বাগত বার্তা আপডেট হয়েছে!")
    
    elif action == "edit_welcome_en":
        new_message = msg.text.strip()
        if len(new_message) < 10:
            bot.reply_to(msg, "❌ Message is too short!")
            return
        messages = load_welcome_messages()
        messages["en"] = new_message
        save_welcome_messages(messages)
        del user_states[user_id]
        bot.reply_to(msg, "✅ English welcome message updated!")
    
    elif action and action.startswith("edit_button_link_"):
        link_key = action.replace("edit_button_link_", "")
        new_link = msg.text.strip()
        if not new_link.startswith("https://"):
            bot.reply_to(msg, "❌ লিংক শুরু হতে হবে https://\n❌ Link must start with https://")
            return
        links = load_button_links()
        links[link_key] = new_link
        save_button_links(links)
        del user_states[user_id]
        bot.reply_to(msg, f"✅ লিংক সফলভাবে আপডেট হয়েছে!\n✅ Link updated successfully!\n\n🔗 {new_link}")
    
    elif action == "otp_btn_add_name":
        btn_name = msg.text.strip()
        if len(btn_name) < 1:
            bot.reply_to(msg, "❌ বাটনের নাম খুব ছোট!")
            return
        user_states[user_id] = {"action": "otp_btn_add_url", "btn_name": btn_name}
        bot.reply_to(msg, f"✅ বাটনের নাম: <b>{btn_name}</b>\n\nএখন বাটনের লিংক পাঠান:\n(উদাহরণ: https://t.me/YourChannel)", parse_mode="HTML")
    
    elif action == "otp_btn_add_url":
        btn_url = msg.text.strip()
        if not btn_url.startswith("https://"):
            bot.reply_to(msg, "❌ লিংক শুরু হতে হবে https://")
            return
        btn_name = state.get("btn_name", "Button")
        otp_buttons = load_otp_buttons()
        otp_buttons.append({"name": btn_name, "url": btn_url})
        save_otp_buttons(otp_buttons)
        del user_states[user_id]
        bot.reply_to(msg, f"✅ বাটন সফলভাবে যোগ হয়েছে!\n\n📝 নাম: <b>{btn_name}</b>\n🔗 লিংক: {btn_url}", parse_mode="HTML")
    
    elif action == "otp_btn_edit_name":
        btn_idx = state.get("btn_idx", 0)
        new_name = msg.text.strip()
        if len(new_name) < 1:
            bot.reply_to(msg, "❌ বাটনের নাম খুব ছোট!")
            return
        otp_buttons = load_otp_buttons()
        if btn_idx < len(otp_buttons):
            otp_buttons[btn_idx]["name"] = new_name
            save_otp_buttons(otp_buttons)
            del user_states[user_id]
            bot.reply_to(msg, f"✅ বাটনের নাম আপডেট হয়ে হয়েছে: <b>{new_name}</b>", parse_mode="HTML")
        else:
            bot.reply_to(msg, "❌ বাটন পাওয়া যায়নি!")
            del user_states[user_id]
    
    elif action == "otp_btn_edit_url":
        btn_idx = state.get("btn_idx", 0)
        new_url = msg.text.strip()
        if not new_url.startswith("https://"):
            bot.reply_to(msg, "❌ লিংক শুরু হতে হবে https://")
            return
        otp_buttons = load_otp_buttons()
        if btn_idx < len(otp_buttons):
            otp_buttons[btn_idx]["url"] = new_url
            save_otp_buttons(otp_buttons)
            del user_states[user_id]
            bot.reply_to(msg, f"✅ বাটনের লিংক আপডেট হয়ে হয়েছে:\n🔗 {new_url}", parse_mode="HTML")
        else:
            bot.reply_to(msg, "❌ বাটন পাওয়া যায়নি!")
            del user_states[user_id]
    
    elif action == "withdraw_details":
        method = state.get("method", "Unknown")
        method_key = state.get("method_key", "unknown")
        details = msg.text.strip()
        lang = get_user_language(user_id)
        
        if len(details) < 5:
            msg_text = "❌ বিবরণ সঠিক নয়!" if lang == "ar" else "❌ Invalid details!"
            bot.reply_to(msg, msg_text)
            return
        
        referral_data = get_user_referral_data(user_id)
        balance = referral_data.get("balance", 0.0)
        settings = load_referral_settings()
        min_withdrawal = settings.get("min_withdrawal", 5.0)
        
        if balance < min_withdrawal:
            msg_text = f"❌ আপনার ব্যালেন্স যথেষ্ট নয়! সর্বনিম্ন: ${min_withdrawal}" if lang == "ar" else f"❌ Insufficient balance! Minimum: ${min_withdrawal}"
            bot.reply_to(msg, msg_text)
            del user_states[user_id]
            return
        
        global REFERRALS
        REFERRALS = load_referrals()
        REFERRALS[str(user_id)]["balance"] = 0.0
        save_referrals(REFERRALS)
        
        request_id = str(uuid.uuid4())[:8]
        withdrawal_request = {
            "id": request_id,
            "user_id": user_id,
            "amount": balance,
            "method": method,
            "method_key": method_key,
            "details": details,
            "date": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "status": "pending"
        }
        
        requests_list = load_withdrawal_requests()
        requests_list.append(withdrawal_request)
        save_withdrawal_requests(requests_list)
        
        del user_states[user_id]
        
        if lang == "ar":
            bot.reply_to(
                msg,
                f"✅ <b>উত্তোলনের অনুরোধ পাঠানো হয়েছে!</b>\n\n"
                f"🆔 অনুরোধ নম্বর: <code>{request_id}</code>\n"
                f"💵 পরিমাণ: <b>${balance:.2f}</b>\n"
                f"📝 পদ্ধতি: {method}\n"
                f"📋 বিবরণ: <code>{details}</code>\n\n"
                f"⏳ <b>অবস্থা:</b> প্রসেসিং চলছে\n"
                f"অনুমোদন বা প্রত্যাখ্যানের সময় জানানো হবে।",
                parse_mode="HTML"
            )
        else:
            bot.reply_to(
                msg,
                f"✅ <b>Withdrawal request submitted!</b>\n\n"
                f"🆔 Request ID: <code>{request_id}</code>\n"
                f"💵 Amount: <b>${balance:.2f}</b>\n"
                f"📝 Method: {method}\n"
                f"📋 Details: <code>{details}</code>\n\n"
                f"⏳ <b>Status:</b> Processing\n"
                f"You will be notified when approved or rejected.",
                parse_mode="HTML"
            )
        
        admin_markup = InlineKeyboardMarkup(row_width=2)
        admin_markup.add(
            InlineKeyboardButton("✅ পেমেন্ট নিশ্চিত", callback_data=f"wd_approve_{request_id}"),
            InlineKeyboardButton("❌ প্রত্যাখ্যান", callback_data=f"wd_reject_{request_id}")
        )
        
        user_data_for_admin = USERS.get(str(user_id), {})
        user_referral_for_admin = get_user_referral_data(user_id)
        
        admin_join_date = user_data_for_admin.get("join_date", "নির্ধারিত নয়")
        admin_total_codes = user_data_for_admin.get("activations", 0)
        admin_total_referrals = len(user_referral_for_admin.get("referrals", []))
        admin_active_referrals = user_referral_for_admin.get("active_referrals", 0)
        admin_total_earned = user_referral_for_admin.get("total_earned", 0.0)
        
        admin_notification = (
            f"📋 <b>নতুন উত্তোলনের অনুরোধ!</b>\n\n"
            f"🆔 অনুরোধ নম্বর: <code>{request_id}</code>\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"👤 <b>ইউজারের তথ্য:</b>\n"
            f"├ 🆔 ID: <code>{user_id}</code>\n"
            f"├ 📅 যোগদানের তারিখ: {admin_join_date}\n"
            f"├ 📊 মোট কোড: {admin_total_codes}\n"
            f"├ 👥 মোট রেফারেল: {admin_total_referrals}\n"
            f"├ ✅ সক্রিয় রেফারেল: {admin_active_referrals}\n"
            f"└ 💰 মোট আয়: ${admin_total_earned:.2f}\n\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"💳 <b>উত্তোলনের বিবরণ:</b>\n"
            f"├ 💵 পরিমাণ: <b>${balance:.2f}</b>\n"
            f"├ ?? পদ্ধতি: {method}\n"
            f"└ 📋 বিবরণ: <code>{details}</code>\n\n"
            f"⏳ অবস্থা: অপেক্ষমাণ"
        )
        
        for admin_id in ADMINS:
            try:
                bot.send_message(
                    admin_id,
                    admin_notification,
                    parse_mode="HTML",
                    reply_markup=admin_markup
                )
            except:
                pass
    
    elif action == "change_site_username":
        global USERNAME, USERNAME2, USERNAME3
        site_key = state.get("site_key")
        account_id = state.get("account_id")
        new_username = msg.text.strip()
        
        accounts = get_site_accounts(site_key)
        account_found = False
        
        for idx, acc in enumerate(accounts):
            if acc.get("id") == account_id:
                accounts[idx]["username"] = new_username
                account_found = True
                
                if idx == 0:
                    if site_key == "GROUP":
                        USERNAME = new_username
                    elif site_key == "Fly sms":
                        USERNAME2 = new_username
                    elif site_key == "Number_Panel":
                        USERNAME3 = new_username
                break
        
        if account_found:
            SETTINGS[site_key]["accounts"] = accounts
            save_settings(SETTINGS)
            
            del user_states[user_id]
            site_name = SETTINGS[site_key]["name"]
            bot.reply_to(
                msg,
                f"✅ <b>ইউজারনেম আপডেট হয়েছে - {site_name}</b>\n\n"
                f"👤 নতুন ইউজারনেম: <code>{new_username}</code>",
                parse_mode="HTML"
            )
        else:
            bot.reply_to(msg, "❌ অ্যাকাউন্ট পাওয়া যায়নি!")
    
    elif action == "change_site_password":
        global PASSWORD, PASSWORD2, PASSWORD3
        site_key = state.get("site_key")
        account_id = state.get("account_id")
        new_password = msg.text.strip()
        
        accounts = get_site_accounts(site_key)
        account_found = False
        
        for idx, acc in enumerate(accounts):
            if acc.get("id") == account_id:
                accounts[idx]["password"] = new_password
                account_found = True
                
                if idx == 0:
                    if site_key == "GROUP":
                        PASSWORD = new_password
                    elif site_key == "Fly sms":
                        PASSWORD2 = new_password
                    elif site_key == "Number_Panel":
                        PASSWORD3 = new_password
                break
        
        if account_found:
            SETTINGS[site_key]["accounts"] = accounts
            save_settings(SETTINGS)
            
            del user_states[user_id]
            site_name = SETTINGS[site_key]["name"]
            bot.reply_to(
                msg,
                f"✅ <b>পাসওয়ার্ড আপডেট হয়েছে - {site_name}</b>\n\n"
                f"🔑 নতুন পাসওয়ার্ড সেভ হয়েছে",
                parse_mode="HTML"
            )
        else:
            bot.reply_to(msg, "❌ অ্যাকাউন্ট পাওয়া যায়নি!")
    
    elif action == "add_account_username":
        site_key = state.get("site_key")
        site_name = SETTINGS[site_key]["name"]
        new_username = msg.text.strip()
        
        if not new_username:
            bot.reply_to(msg, "❌ ইউজারনেম ফাঁকা রাখা যাবে না!")
            return
        
        if site_key == "iVASMS":
            user_states[user_id] = {
                "action": "add_account_password",
                "site_key": site_key,
                "username": new_username
            }
            bot.reply_to(
                msg,
                f"➕ <b>নতুন অ্যাকাউন্ট যোগ - {site_name}</b>\n\n"
                f"✅ ইউজারনেম: <code>{new_username}</code>\n\n"
                f"📝 ধাপ 2/3: পাসওয়ার্ড পাঠান (Password):",
                parse_mode="HTML"
            )
        else:
            user_states[user_id] = {
                "action": "add_account_password",
                "site_key": site_key,
                "username": new_username
            }
            bot.reply_to(
                msg,
                f"➕ <b>নতুন অ্যাকাউন্ট যোগ - {site_name}</b>\n\n"
                f"✅ ইউজারনেম: <code>{new_username}</code>\n\n"
                f"📝 ধাপ 2/2: পাসওয়ার্ড পাঠান (Password):",
                parse_mode="HTML"
            )
    
    elif action == "add_account_password":
        site_key = state.get("site_key")
        site_name = SETTINGS[site_key]["name"]
        username = state.get("username")
        password = msg.text.strip()
        
        if not password:
            bot.reply_to(msg, "❌ পাসওয়ার্ড ফাঁকা রাখা যাবে না!")
            return
        
        if site_key == "iVASMS":
            user_states[user_id] = {
                "action": "add_account_api_key",
                "site_key": site_key,
                "username": username,
                "password": password
            }
            bot.reply_to(
                msg,
                f"➕ <b>নতুন অ্যাকাউন্ট যোগ - {site_name}</b>\n\n"
                f"✅ ইউজারনেম: <code>{username}</code>\n"
                f"✅ পাসওয়ার্ড: <code>{password}</code>\n\n"
                f"📝 ধাপ 3/3: কী পাঠান API (API Key):",
                parse_mode="HTML"
            )
            return
        
        new_account = add_account(site_key, username, password)
        
        if new_account:
            del user_states[user_id]
            
            if SETTINGS[site_key]["enabled"]:
                thread = Thread(target=start_monitoring_for_account, args=(site_key, new_account), daemon=True)
                thread.start()
                print(f"🚀 নতুন অ্যাকাউন্টের তাৎক্ষণিক মনিটরিং শুরু: {username} ({site_name})")
                
                bot.reply_to(
                    msg,
                    f"✅ <b>অ্যাকাউন্ট সফলভাবে যোগ হয়েছে - {site_name}</b>\n\n"
                    f"👤 ইউজারনেম: <code>{username}</code>\n"
                    f"🔑 পাসওয়ার্ড: <code>{password}</code>\n"
                    f"🆔 ID: <code>{new_account['id'][:8]}...</code>\n\n"
                    f"🚀 <b>মনিটরিং সাথে সাথে শুরু হয়েছে!</b>",
                    parse_mode="HTML"
                )
            else:
                bot.reply_to(
                    msg,
                    f"✅ <b>অ্যাকাউন্ট সফলভাবে যোগ হয়েছে - {site_name}</b>\n\n"
                    f"👤 ইউজারনেম: <code>{username}</code>\n"
                    f"🔑 পাসওয়ার্ড: <code>{password}</code>\n"
                    f"🆔 ID: <code>{new_account['id'][:8]}...</code>\n\n"
                    f"⚠️ সাইটটি এখন চালু নেই",
                    parse_mode="HTML"
                )
        else:
            bot.reply_to(msg, "❌ অ্যাকাউন্ট যোগ ব্যর্থ!")
    
    elif action == "add_account_api_key":
        site_key = state.get("site_key")
        site_name = SETTINGS[site_key]["name"]
        username = state.get("username")
        password = state.get("password")
        api_key = msg.text.strip()
        
        if not api_key:
            bot.reply_to(msg, "❌ কী API ফাঁকা রাখা যাবে না!")
            return
        
        new_account = add_account(site_key, username, password)
        
        if new_account:
            for idx, acc in enumerate(SETTINGS[site_key]["accounts"]):
                if acc["id"] == new_account["id"]:
                    SETTINGS[site_key]["accounts"][idx]["api_key"] = api_key
                    save_settings(SETTINGS)
                    break
            
            del user_states[user_id]
            
            if SETTINGS[site_key]["enabled"]:
                new_account["api_key"] = api_key
                thread = Thread(target=start_monitoring_for_account, args=(site_key, new_account), daemon=True)
                thread.start()
                print(f"🚀 নতুন অ্যাকাউন্টের তাৎক্ষণিক মনিটরিং শুরু: {username} ({site_name})")
                
                bot.reply_to(
                    msg,
                    f"✅ <b>অ্যাকাউন্ট সফলভাবে যোগ হয়েছে - {site_name}</b>\n\n"
                    f"👤 ইউজারনেম: <code>{username}</code>\n"
                    f"🔑 পাসওয়ার্ড: <code>{password}</code>\n"
                    f"🔐 কী API: <code>{api_key[:10]}...</code>\n"
                    f"🆔 ID: <code>{new_account['id'][:8]}...</code>\n\n"
                    f"🚀 <b>মনিটরিং সাথে সাথে শুরু হয়েছে!</b>",
                    parse_mode="HTML"
                )
            else:
                bot.reply_to(
                    msg,
                    f"✅ <b>অ্যাকাউন্ট সফলভাবে যোগ হয়েছে - {site_name}</b>\n\n"
                    f"👤 ইউজারনেম: <code>{username}</code>\n"
                    f"🔑 পাসওয়ার্ড: <code>{password}</code>\n"
                    f"🔐 কী API: <code>{api_key[:10]}...</code>\n"
                    f"🆔 ID: <code>{new_account['id'][:8]}...</code>\n\n"
                    f"⚠️ সাইটটি এখন চালু নেই",
                    parse_mode="HTML"
                )
        else:
            bot.reply_to(msg, "❌ অ্যাকাউন্ট যোগ ব্যর্থ!")
    
    elif action == "change_site_interval":
        global CHECK_INTERVAL, CHECK_INTERVAL2, CHECK_INTERVAL3
        site_key = state.get("site_key")
        
        try:
            new_interval = int(msg.text.strip())
            
            if new_interval < 1 or new_interval > 300:
                bot.reply_to(msg, "❌ বিরতি অবশ্যই 1 থেকে 300 সেকেন্ডের মধ্যে হতে হবে!")
                return
            
            SETTINGS[site_key]["check_interval"] = new_interval
            save_settings(SETTINGS)
            
            if site_key == "GROUP":
                CHECK_INTERVAL = new_interval
            elif site_key == "Fly sms":
                CHECK_INTERVAL2 = new_interval
            elif site_key == "Number_Panel":
                CHECK_INTERVAL3 = new_interval
            
            del user_states[user_id]
            site_name = SETTINGS[site_key]["name"]
            bot.reply_to(
                msg,
                f"✅ <b>অনুসন্ধানের বিরতি আপডেট হয়েছে - {site_name}</b>\n\n"
                f"⏱ নতুন বিরতি: {new_interval} সেকেন্ড\n\n"
                f"⚠️ পরিবর্তন পরের চক্রে কার্যকর হবে",
                parse_mode="HTML"
            )
        except ValueError:
            bot.reply_to(msg, "❌ অনুগ্রহ করে সঠিক সংখ্যা দিন!")
    
    elif action == "change_site_timeout":
        global HTTP_TIMEOUT, HTTP_TIMEOUT2, HTTP_TIMEOUT3
        site_key = state.get("site_key")
        
        try:
            new_timeout = int(msg.text.strip())
            
            if new_timeout < 5 or new_timeout > 300:
                bot.reply_to(msg, "❌ অপেক্ষার সময় অবশ্যই 5 থেকে 300 সেকেন্ডের মধ্যে হতে হবে!")
                return
            
            SETTINGS[site_key]["timeout"] = new_timeout
            save_settings(SETTINGS)
            
            if site_key == "GROUP":
                HTTP_TIMEOUT = new_timeout
            elif site_key == "Fly sms":
                HTTP_TIMEOUT2 = new_timeout
            elif site_key == "Number_Panel":
                HTTP_TIMEOUT3 = new_timeout
            
            del user_states[user_id]
            site_name = SETTINGS[site_key]["name"]
            bot.reply_to(
                msg,
                f"✅ <b>অপেক্ষার সময় আপডেট হয়েছে - {site_name}</b>\n\n"
                f"⏳ নতুন সময়: {new_timeout} সেকেন্ড",
                parse_mode="HTML"
            )
        except ValueError:
            bot.reply_to(msg, "❌ অনুগ্রহ করে সঠিক সংখ্যা দিন!")
    
    elif action == "add_group":
        try:
            group_id = int(msg.text.strip())
            
            try:
                chat = bot.get_chat(group_id)
                admins = bot.get_chat_administrators(group_id)
                
                bot_is_admin = False
                for admin in admins:
                    if admin.user.id == bot.get_me().id:
                        bot_is_admin = True
                        break
                
                if not bot_is_admin:
                    bot.reply_to(msg, "❌ বট নয় admin এই গ্রুপে!")
                    return
                
                if group_id in GROUPS:
                    bot.reply_to(msg, "⚠️ এই গ্রুপ আগেই যোগ করা আছে!")
                    return
                
                GROUPS.append(group_id)
                save_groups()
                del user_states[user_id]
                
                bot.reply_to(
                    msg,
                    f"✅ <b>গ্রুপ সফলভাবে যোগ হয়েছে!</b>\n\n"
                    f"📱 নাম: <b>{chat.title}</b>\n"
                    f"🆔 ID: <code>{group_id}</code>",
                    parse_mode="HTML"
                )
            except Exception as e:
                bot.reply_to(msg, f"❌ ত্রুটি: {e}\n\nনিশ্চিত করুন যে:\n• বট admin গ্রুপে\n• ID গ্রুপ সঠিক")
        except ValueError:
            bot.reply_to(msg, "❌ ID সঠিক নয়!")
    
    elif action == "remove_group":
        try:
            group_id = int(msg.text.strip())
            
            if group_id in GROUPS:
                GROUPS.remove(group_id)
                save_groups()
                del user_states[user_id]
                bot.reply_to(msg, f"✅ গ্রুপ মুছে ফেলা হয়েছে!\n\nID: <code>{group_id}</code>", parse_mode="HTML")
            else:
                bot.reply_to(msg, "❌ গ্রুপ পাওয়া যায়নি!")
        except ValueError:
            bot.reply_to(msg, "❌ ID সঠিক নয়!")
    
    elif user_id in broadcast_state:
        state = broadcast_state[user_id]
        broadcast_type = state.get("type")
        step = state.get("step")
        
        if step != "waiting_message":
            return
        
        saved_msg = {
            "content_type": msg.content_type,
            "chat_id": msg.chat.id,
            "message_id": msg.message_id
        }
        
        if msg.content_type == "text":
            saved_msg["text"] = msg.text
            saved_msg["has_entities"] = bool(msg.entities)
        elif msg.content_type == "photo":
            saved_msg["file_id"] = msg.photo[-1].file_id
            saved_msg["caption"] = msg.caption
        elif msg.content_type == "video":
            saved_msg["file_id"] = msg.video.file_id
            saved_msg["caption"] = msg.caption
        elif msg.content_type == "document":
            saved_msg["file_id"] = msg.document.file_id
            saved_msg["caption"] = msg.caption
        elif msg.content_type == "audio":
            saved_msg["file_id"] = msg.audio.file_id
            saved_msg["caption"] = msg.caption
        elif msg.content_type == "voice":
            saved_msg["file_id"] = msg.voice.file_id
            saved_msg["caption"] = msg.caption
        elif msg.content_type == "sticker":
            saved_msg["file_id"] = msg.sticker.file_id
        
        broadcast_state[user_id]["message"] = saved_msg
        broadcast_state[user_id]["step"] = "confirm"
        
        if broadcast_type == "forward":
            broadcast_label = "📤 ইউজারদের কাছে ফরওয়ার্ড"
        else:
            broadcast_label = "📣 মূল বটের ইউজার"
        
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("✅ পাঠানো নিশ্চিত", callback_data="confirm_broadcast", style="success"),
            InlineKeyboardButton("🔙 বাতিল", callback_data="cancel_broadcast", style="danger")
        )
        
        bot.reply_to(
            msg,
            f"📣 <b>ব্রডকাস্ট নিশ্চিত</b>\n\n"
            f"📍 গন্তব্য: {broadcast_label}\n"
            f"📝 মেসেজের ধরন: {msg.content_type}\n\n"
            f"⚠️ আপনি কি নিশ্চিত এই মেসেজ পাঠাতে চান?",
            parse_mode="HTML",
            reply_markup=markup
        )
    
def get_country_info(number: str):
    cleaned_num = clean_number(number)
    country_codes = detect_country_from_number(number)
    if country_codes:
        return country_codes[0], country_codes[1]
    return "Unknown", "🌐"

def normalize_number(number):

    if not number:
        return ""

    cleaned = re.sub(r'\D', '', str(number))
    return cleaned

COLLECTED_CODES_FILE = "collected_codes.json"
collected_codes = []

def load_collected_codes():
    global collected_codes
    if os.path.exists(COLLECTED_CODES_FILE):
        try:
            with open(COLLECTED_CODES_FILE, 'r', encoding='utf-8') as f:
                collected_codes = json.load(f)
        except:
            collected_codes = []
    return collected_codes

def save_collected_codes():
    with open(COLLECTED_CODES_FILE, 'w', encoding='utf-8') as f:
        json.dump(collected_codes, f, indent=2, ensure_ascii=False)

def send_otp_to_user(number, otp_message, full_number, group_message=None, otp_code=None):
   
    normalized_incoming = normalize_number(number)
    
    sent_to_users = []
    users_copy = dict(USERS)
    for user_id_str, user_data in users_copy.items():
        selected_num = user_data.get("selected_number")
        if not selected_num:
            continue

        normalized_selected = normalize_number(selected_num)

        if (normalized_incoming == normalized_selected or 
            normalized_incoming.endswith(normalized_selected) or 
            normalized_selected.endswith(normalized_incoming) or
            full_number == selected_num):

            try:
                bot.send_message(
                    int(user_id_str),
                    otp_message,
                    parse_mode="HTML"
                )
                sent_to_users.append(user_id_str)
                
                if "activations" not in USERS.get(user_id_str, {}):
                    if user_id_str in USERS:
                        USERS[user_id_str]["activations"] = 0
                if user_id_str in USERS:
                    USERS[user_id_str]["activations"] = USERS[user_id_str].get("activations", 0) + 1
                save_users()
                
                try:
                    add_code_bonus(int(user_id_str))
                except Exception as bonus_err:
                    print(f"⚠️ ইউজারকে বোনাস যোগ করতে ত্রুটি {user_id_str}: {bonus_err}")
            except Exception as e:
                print(f"❌ ইউজারকে পাঠাতে ত্রুটি {user_id_str}: {str(e)}")

    update_statistics()
    
    sent_groups = set()
    msg_to_group = group_message if group_message else otp_message
    
    group_keyboard = create_group_otp_keyboard(otp_code)
    
    if OTP_GROUP and OTP_GROUP not in sent_groups:
        try:
            bot.send_message(OTP_GROUP, msg_to_group, parse_mode="HTML", disable_web_page_preview=True, reply_markup=group_keyboard)
            sent_groups.add(OTP_GROUP)
            print(f"✅ গ্রুপে পাঠানো হয়েছে OTP_GROUP: {OTP_GROUP}")
        except Exception as e:
            print(f"❌ গ্রুপে পাঠাতে ত্রুটি OTP: {str(e)}")
    
    
    if not GROUPS and os.path.exists(GROUPS_FILE):
        try:
            with open(GROUPS_FILE, "r") as f:
                loaded_groups = json.load(f)
                for g in loaded_groups:
                    if g not in GROUPS:
                        GROUPS.append(g)
        except:
            pass

    groups_copy = list(GROUPS)
    for gid in groups_copy:
        if gid not in sent_groups:
            try:
                bot.send_message(gid, msg_to_group, parse_mode="HTML", disable_web_page_preview=True, reply_markup=group_keyboard)
                sent_groups.add(gid)
                print(f"✅ তালিকার একটি গ্রুপে পাঠানো হয়েছে: {gid}")
            except Exception as e:
                print(f"❌ গ্রুপে পাঠাতে ত্রুটি {gid}: {str(e)}")
    
    return sent_to_users

def load_last_seen_key():
    global last_seen_key
    if os.path.exists(LAST_MESSAGE_FILE):
        try:
            with open(LAST_MESSAGE_FILE, "r", encoding="utf-8") as f:
                last_seen_key = f.read().strip()
                print(f"📋 সর্বশেষ দেখা মেসেজ লোড হয়েছে: {last_seen_key[:50]}..." if last_seen_key else "📋 আগের কোনো মেসেজ নেই")
        except:
            last_seen_key = ""
    else:
        last_seen_key = ""

def save_last_seen_key():
    try:
        with open(LAST_MESSAGE_FILE, "w", encoding="utf-8") as f:
            f.write(last_seen_key)
        print(f"💾 সর্বশেষ দেখা মেসেজ সেভ হয়েছে")
    except Exception as e:
        print(f"❌ সর্বশেষ মেসেজ সেভে ত্রুটি: {str(e)}")

def print_monitoring_box(site_name, username, status_icon, status_text):
    box_width = 45
    box = f"\n╔{'═' * box_width}\n  📍 {site_name}  •  👤 {username}\n  {status_icon} {status_text}\n╚{'═' * box_width}"
    print(box)

def login_site3():
    global is_logged_in_site3
    print("[Site3/Number_Panel] 🔄 লগইনের চেষ্টা চলছে...")
    
    try:
        session3.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,ar;q=0.8"
        })
        
        resp = session3.get(LOGIN_PAGE_URL3, timeout=HTTP_TIMEOUT3)
        print(f"[Site3/Number_Panel] 📄 স্ট্যাটাস GET: {resp.status_code}")
        
        match = re.search(r'What is (\d+) \+ (\d+)', resp.text)
        if not match:
            print("[Site3/Number_Panel] ⚠️ খুঁজে পাওয়া যায়নি captcha পেজে")
            print(f"[Site3/Number_Panel] 📋 কন্টেন্টের নমুনা: {resp.text[:500]}")
            return False
        
        num1, num2 = int(match.group(1)), int(match.group(2))
        captcha_answer = num1 + num2
        print(f"[Site3/Number_Panel] 🧮 সমাধান captcha: {num1} + {num2} = {captcha_answer}")
        
        payload = {
            "username": USERNAME3,
            "password": PASSWORD3,
            "capt": str(captcha_answer)
        }
        
        if "crlf" in resp.text:
            crlf_match = re.search(r"name='crlf' value='([^']+)'", resp.text)
            if crlf_match:
                payload["crlf"] = crlf_match.group(1)
                print(f"[Site3/Number_Panel] 🔑 বের করা crlf token")
        
        csrf_token = get_csrf_token_np(resp.text)
        if csrf_token:
            payload["_token"] = csrf_token
            print(f"[Site3/Number_Panel] 🔑 বের করা CSRF Token")
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": LOGIN_PAGE_URL3,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Origin": BASE_URL3
        }
        
        print(f"[Site3/Number_Panel] 📤 লগইন অনুরোধ পাঠানো হচ্ছে: {USERNAME3}")
        resp = session3.post(LOGIN_POST_URL3, data=payload, headers=headers, timeout=HTTP_TIMEOUT3, allow_redirects=True)
        
        print(f"[Site3/Number_Panel] 📊 স্ট্যাটাস POST: {resp.status_code}")
        print(f"[Site3/Number_Panel] 🔗 URL চূড়ান্ত: {resp.url}")
        
        if ("dashboard" in resp.text.lower() or 
            "logout" in resp.text.lower() or 
            "agent" in resp.url.lower() or
            "reports" in resp.url.lower() or
            "smscdr" in resp.text.lower() or
            "signin" in resp.text.lower() or
            "dashboard" in resp.url.lower() or
            resp.url != LOGIN_PAGE_URL3):
            print("[Site3/Number_Panel] ✅ লগইন সফল হয়েছে")
            is_logged_in_site3 = True
            save_cookies_site3()
            return True
        else:
            print("[Site3/Number_Panel] ❌ লগইন ব্যর্থ")
            if "incorrect" in resp.text.lower() or "invalid" in resp.text.lower():
                print("[Site3/Number_Panel] ⚠️ ইউজারনেম বা পাসওয়ার্ড ভুল")
            return False
    except Exception as e:
        print(f"[Site3/Number_Panel] ❌ লগইনে ত্রুটি: {e}")
        import traceback
        traceback.print_exc()
        return False

def build_ajax_url_site3(wide_range=False):
    if wide_range:
        start_date = date.today() - timedelta(days=5)
        end_date = date.today() + timedelta(days=1)
    else:
        start_date = date.today()
        end_date = date.today() + timedelta(days=1)
    
    fdate1 = f"{start_date.strftime('%Y-%m-%d')} 00:00:00"
    fdate2 = f"{end_date.strftime('%Y-%m-%d')} 23:59:59"
    
    return {
        'url': BASE_URL3 + AJAX_PATH3,
        'params': {
            'fdate1': fdate1,
            'fdate2': fdate2,
            'sEcho': '1',
            'iDisplayStart': '0',
            'iDisplayLength': '50000',
            'iSortCol_0': '0',
            'sSortDir_0': 'desc'
        }
    }

def extract_rows_from_json_site3(j):
    if j is None:
        return []
    for key in ("data", "aaData", "rows"):
        if isinstance(j, dict) and key in j:
            return j[key]
    return j if isinstance(j, list) else []

def row_to_tuple_site3(row):
    date_str = clean_html_site2(row[0]) if len(row) > 0 else ""
    number = clean_number(row[2]) if len(row) > 2 else ""
    sms = clean_html_site2(row[5]) if len(row) > 5 else ""
    key = f"{date_str}|{number}|{sms}"
    return date_str, number, sms, key

def fetch_ajax_data_np(account_session, site_key, account):
    try:
        api_token = account.get("api_token") or account.get("id")
        if not api_token or api_token == "Api Token":
            return {"aaData": []}, False
            
        api_url = "http://147.135.212.197/crapi/st/viewstats"
        params = {"token": api_token, "records": 50}
        
        
        r = account_session.get(api_url, params=params, timeout=30)
        
        if r.status_code == 200:
            data = r.json()
            
            if isinstance(data, list):
                formatted_rows = []
                for item in data:
                    if isinstance(item, list) and len(item) >= 4:
                        row = [None] * 6
                        row[0] = item[3] 
                        row[1] = item[0] 
                        row[2] = item[1] 
                        row[5] = item[2] 
                        formatted_rows.append(row)
                return {"aaData": formatted_rows}, False
        else:
            print(f"[Number_Panel] API Status Error: {r.status_code}")
        return {"aaData": []}, False
    except Exception as e:
        print(f"[Number_Panel] API Exception: {e}")
        return None, False

def sms_loop_for_number_panel_account(site_key, account):
    account_id = account.get("id")
    api_token = account.get("api_token") or account_id
    site_name = SETTINGS[site_key]["name"]
    check_interval = SETTINGS[site_key].get("check_interval", 5)
    
    account_session = requests.Session()
    account_session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    })
    
    safe_id = "".join(x for x in api_token if x.isalnum())[:15]
    last_message_file = f"last_message_{site_key}_{safe_id}.txt"
    last_seen_key_local = ""
    
    if os.path.exists(last_message_file):
        try:
            with open(last_message_file, "r", encoding="utf-8") as f:
                last_seen_key_local = f.read().strip()
        except: pass

    print_monitoring_box(site_name, f"TOKEN: {api_token[:10]}...", "🌐", "মনিটরিং শুরু হয়েছে মাধ্যমে API...")
    
    while True:
        try:
            j, _ = fetch_ajax_data_np(account_session, site_key, {"api_token": api_token})
            rows = extract_rows_from_json_site3(j)
            
            if rows:
                valid_rows = []
                for row in rows:
                    if isinstance(row, list) and len(row) > 5:
                        date_str = clean_html_site2(row[0])
                        number = clean_number(row[2])
                        sms = clean_html_site2(row[5])
                        service_name_api = clean_html_site2(row[1]) if row[1] else ""
                        key = f"{date_str}|{number}|{sms}"
                        if date_str and number and sms:
                            valid_rows.append((date_str, number, sms, key, service_name_api))
                
                if valid_rows:
                    def get_dt(r):
                        try: return datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S")
                        except: return datetime.min
                    
                    valid_rows.sort(key=get_dt, reverse=True)
                    
                    if not last_seen_key_local:
                        
                        r = valid_rows[0]
                        date_str, number, sms, key, s_name = r
                        otp_val, sms_text = extract_from_message(sms)
                        display_name = f"[{s_name}]" if s_name else f"[{detect_service(sms)}]"
                        formatted_msg = format_otp_message_v2(number, sms_text, display_name, otp_val)
                        
                        
                        send_otp_to_user(clean_number(number), formatted_msg, number, None, otp_val)
                        
                        last_seen_key_local = key
                        with open(last_message_file, "w", encoding="utf-8") as f:
                            f.write(last_seen_key_local)
                        print(f"[{site_name}] Initialized and sent latest code: {last_seen_key_local[:20]}...")
                    else:
                        new_msgs = []
                        for r in valid_rows:
                            if r[3] == last_seen_key_local:
                                break
                            new_msgs.append(r)
                        
                        if new_msgs:
                            new_msgs.reverse() 
                            for r in new_msgs:
                                date_str, number, sms, key, s_name = r
                                otp_val, sms_text = extract_from_message(sms)
                                display_name = f"[{s_name}]" if s_name else f"[{detect_service(sms)}]"
                                formatted_msg = format_otp_message_v2(number, sms_text, display_name, otp_val)
                                send_otp_to_user(clean_number(number), formatted_msg, number, None, otp_val)
                                last_seen_key_local = key
                            
                            with open(last_message_file, "w", encoding="utf-8") as f:
                                f.write(last_seen_key_local)
            
            time.sleep(check_interval)
        except Exception as e:
            print(f"[{site_name}] Loop Error: {e}")
            time.sleep(10)


def login_site4():
    global is_logged_in_site4
    print("[Site4/Bolt] 🔄 লগইনের চেষ্টা চলছে...")
    
    try:
        session4.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,ar;q=0.8"
        })
        
        resp = session4.get(LOGIN_PAGE_URL4, timeout=HTTP_TIMEOUT4)
        print(f"[Site4/Bolt] 📄 স্ট্যাটাস GET: {resp.status_code}")
        
        match = re.search(r'What is (\d+) \+ (\d+)', resp.text)
        if not match:
            print("[Site4/Bolt] ⚠️ খুঁজে পাওয়া যায়নি captcha পেজে")
            print(f"[Site4/Bolt] 📋 কন্টেন্টের নমুনা: {resp.text[:500]}")
            return False
        
        num1, num2 = int(match.group(1)), int(match.group(2))
        captcha_answer = num1 + num2
        print(f"[Site4/Bolt] 🧮 সমাধান captcha: {num1} + {num2} = {captcha_answer}")
        
        crlf_match = re.search(r"name='crlf' value='([^']+)'", resp.text)
        
        payload = {
            "username": USERNAME4,
            "password": PASSWORD4,
            "capt": str(captcha_answer)
        }
        
        if crlf_match:
            payload["crlf"] = crlf_match.group(1)
            print(f"[Site4/Bolt] 🔑 বের করা crlf token")
        else:
            print(f"[Site4/Bolt] ⚠️ খুঁজে পাওয়া যায়নি crlf token")
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": LOGIN_PAGE_URL4,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Origin": BASE_URL4
        }
        
        print(f"[Site4/Bolt] 📤 লগইন অনুরোধ পাঠানো হচ্ছে: {USERNAME4}")
        resp = session4.post(LOGIN_POST_URL4, data=payload, headers=headers, timeout=HTTP_TIMEOUT4, allow_redirects=True)
        
        print(f"[Site4/Bolt] 📊 স্ট্যাটাস POST: {resp.status_code}")
        print(f"[Site4/Bolt] 🔗 URL চূড়ান্ত: {resp.url}")
        
        if ("dashboard" in resp.text.lower() or 
            "logout" in resp.text.lower() or 
            "agent" in resp.url.lower() or 
            "reports" in resp.url.lower() or
            resp.url != LOGIN_PAGE_URL4):
            print("[Site4/Bolt] ✅ লগইন সফল হয়েছে")
            is_logged_in_site4 = True
            save_cookies_site4()
            return True
        else:
            print("[Site4/Bolt] ❌ লগইন ব্যর্থ")
            if "incorrect" in resp.text.lower() or "invalid" in resp.text.lower():
                print("[Site4/Bolt] ⚠️ ইউজারনেম বা পাসওয়ার্ড ভুল")
            return False
            
    except Exception as e:
        print(f"[Site4/Bolt] ❌ লগইনে ত্রুটি: {e}")
        import traceback
        traceback.print_exc()
        return False

def build_ajax_url_site4(start_date=None, end_date=None, wide_range=False):
    if wide_range:
        start_date = date.today() - timedelta(days=7)
        end_date = date.today() + timedelta(days=1)
    else:
        if start_date is None:
            start_date = date.today()
        if end_date is None:
            end_date = date.today() + timedelta(days=1)
    
    fdate1 = f"{start_date.strftime('%Y-%m-%d')} 00:00:00"
    fdate2 = f"{end_date.strftime('%Y-%m-%d')} 23:59:59"
    
    return {
        'url': BASE_URL4 + AJAX_PATH4,
        'params': {
            'fdate1': fdate1,
            'fdate2': fdate2,
            'frange': '',
            'fclient': '',
            'fnum': '',
            'fcli': '',
            'fgdate': '',
            'fgmonth': '',
            'fgrange': '',
            'fgclient': '',
            'fgnumber': '',
            'fgcli': '',
            'fg': '0',
            'sEcho': '1',
            'iColumns': '8',
            'sColumns': '',
            'iDisplayStart': '0',
            'iDisplayLength': '100',
            'mDataProp_0': '0',
            'mDataProp_1': '1',
            'mDataProp_2': '2',
            'mDataProp_3': '3',
            'mDataProp_4': '4',
            'mDataProp_5': '5',
            'mDataProp_6': '6',
            'mDataProp_7': '7',
            'sSearch': '',
            'bRegex': 'false',
            'iSortCol_0': '0',
            'sSortDir_0': 'desc',
            'iSortingCols': '1'
        }
    }

def fetch_ajax_json_site4(url_dict, retry_count=0):
    global is_logged_in_site4
    
    ajax_headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': BASE_URL4 + "/agent/SMSCDRReports"
    }
    
    try:
        print(f"[Site4/Bolt] 📡 অনুরোধ পাঠানো হচ্ছে AJAX প্রতি: {url_dict['url']}")
        r = session4.post(url_dict['url'], data=url_dict['params'], headers=ajax_headers, timeout=HTTP_TIMEOUT4)
        print(f"[Site4/Bolt] 📊 স্ট্যাটাস API: {r.status_code}, URL: {r.url[:80]}")
        
        if r.status_code == 403 or (r.status_code == 200 and 'login' in r.url.lower()):
            is_logged_in_site4 = False
            print("[Site4/Bolt] 🔄 সেশন শেষ - আবার লগইন হচ্ছে...")
            if login_site4():
                is_logged_in_site4 = True
                save_cookies_site4()
                r = session4.post(url_dict['url'], data=url_dict['params'], headers=ajax_headers, timeout=HTTP_TIMEOUT4)
                print(f"[Site4/Bolt] 📊 স্ট্যাটাস API আবার লগইনের পর: {r.status_code}")
            else:
                return None
        
        r.raise_for_status()
        data = r.json()
        print(f"[Site4/Bolt] 🔎 ডাটার ধরন: {type(data)}, আকার: {len(str(data))}")
        
        if data:
            rows_count = 0
            if isinstance(data, dict):
                print(f"[Site4/Bolt] 🔑 কী JSON: {list(data.keys())[:10]}")
                for key in ("data", "aaData", "rows"):
                    if key in data and isinstance(data[key], list):
                        rows_count = len(data[key])
                        print(f"[Site4/Bolt] ✅ পাওয়া গেছে {rows_count} মেসেজ '{key}'")
                        break
            elif isinstance(data, list):
                rows_count = len(data)
                print(f"[Site4/Bolt] ✅ তালিকায় আছে {rows_count} আইটেম")
            
            if rows_count == 0:
                print(f"[Site4/Bolt] ⚠️ রেসপন্স ফাঁকা: {str(data)[:300]}")
        else:
            print(f"[Site4/Bolt] ⚠️ ডাটা None অথবা ফাঁকা")
        
        return data if isinstance(data, (dict, list)) else None
    except Exception as e:
        print(f"[Site4/Bolt] ❌ ডাটা আনতে ত্রুটি: {e}")
        import traceback
        traceback.print_exc()
        return None

def extract_rows_from_json_site4(j):
    if j is None:
        return []
    for key in ("data", "aaData", "rows"):
        if isinstance(j, dict) and key in j:
            return j[key]
    return j if isinstance(j, list) else []

def is_hotmelo_message(message):
    message_lower = message.lower()
    hotmelo_keywords = ["hotmelo", "hot melo", "hot-melo", "hotmelon"]
    return any(keyword in message_lower for keyword in hotmelo_keywords)

def filter_hotmelo_messages_site4(rows):
    IDX_DATE_SITE4 = 0
    IDX_NUMBER_SITE4 = 2
    IDX_SMS_SITE4 = 5
    
    hotmelo_messages = []
    other_messages = []
    
    for row in rows:
        if isinstance(row, list) and len(row) > IDX_SMS_SITE4:
            date_val = clean_html_site2(row[IDX_DATE_SITE4])
            number_val = clean_number(row[IDX_NUMBER_SITE4])
            sms_val = clean_html_site2(row[IDX_SMS_SITE4]) if row[IDX_SMS_SITE4] else ""
            
            if (date_val and '-' in date_val and ':' in date_val and 
                number_val and len(number_val) >= 10 and 
                sms_val and len(sms_val) > 5):
                
                if is_hotmelo_message(sms_val):
                    hotmelo_messages.append(row)
                else:
                    other_messages.append(row)
    
    return hotmelo_messages + other_messages

def row_to_tuple_site4(row):
    IDX_DATE_SITE4 = 0
    IDX_NUMBER_SITE4 = 2
    IDX_SMS_SITE4 = 5
    
    date_str = clean_html_site2(row[IDX_DATE_SITE4]) if len(row) > IDX_DATE_SITE4 else ""
    number = clean_number(row[IDX_NUMBER_SITE4]) if len(row) > IDX_NUMBER_SITE4 else ""
    sms = clean_html_site2(row[IDX_SMS_SITE4]) if len(row) > IDX_SMS_SITE4 else ""
    key = f"{date_str}|{number}|{sms}"
    return date_str, number, sms, key

def load_last_seen_key_site4():
    global last_seen_key_site4
    if os.path.exists(LAST_MESSAGE_FILE_SITE4):
        with open(LAST_MESSAGE_FILE_SITE4, "r", encoding="utf-8") as f:
            last_seen_key_site4 = f.read().strip()
            print(f"[Site4/Bolt] 📋 সর্বশেষ মেসেজ লোড হয়েছে: {last_seen_key_site4[:50]}...")

def save_last_seen_key_site4():
    with open(LAST_MESSAGE_FILE_SITE4, "w", encoding="utf-8") as f:
        f.write(last_seen_key_site4)

def verify_session_site4():
    try:
        test_url = build_ajax_url_site4(wide_range=False)
        ajax_headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': BASE_URL4 + "/agent/SMSCDRReports"
        }
        r = session4.post(test_url['url'], data=test_url['params'], headers=ajax_headers, timeout=HTTP_TIMEOUT4)
        
        if r.status_code == 403 or 'login' in r.url.lower():
            return False
        
        r.raise_for_status()
        return True
    except:
        return False

def verify_session_site3():
    try:
        test_url = build_ajax_url_site3(wide_range=False)
        ajax_headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': BASE_URL3 + "/agent/SMSCDRReports"
        }
        r = session3.post(test_url['url'], data=test_url['params'], headers=ajax_headers, timeout=HTTP_TIMEOUT3)
        
        if r.status_code == 403 or 'login' in r.url.lower():
            return False
        
        r.raise_for_status()
        return True
    except:
        return False

def login_site5():
    
    global is_logged_in_site5, csrf_token_site5
    print("[iVASMS] 🔄 লগইনের চেষ্টা চলছে...")
    
    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        resp = session5.get(LOGIN_PAGE_URL5, timeout=HTTP_TIMEOUT5)
        print(f"[iVASMS] 📄 স্ট্যাটাস GET: {resp.status_code}")
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        csrf_input = soup.find('input', {'name': '_token'})
        if not csrf_input:
            print("[iVASMS] ⚠️ খুঁজে পাওয়া যায়নি CSRF token")
            return False
        
        csrf = csrf_input.get('value')
        if not csrf:
            print("[iVASMS] ⚠️ CSRF token ফাঁকা")
            return False
        print(f"[iVASMS] 🔑 বের করা CSRF token: {csrf[:20] if len(str(csrf)) > 20 else csrf}...")
        
        payload = {
            '_token': csrf,
            'email': USERNAME5,
            'password': PASSWORD5,
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": LOGIN_PAGE_URL5,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        
        print(f"[iVASMS] 📤 লগইন অনুরোধ পাঠানো হচ্ছে: {USERNAME5}")
        resp = session5.post(LOGIN_POST_URL5, data=payload, headers=headers, timeout=HTTP_TIMEOUT5, allow_redirects=True)
        
        print(f"[iVASMS] 📊 স্ট্যাটাস POST: {resp.status_code}")
        print(f"[iVASMS] 🔗 URL চূড়ান্ত: {resp.url}")
        
        if 'portal' in resp.url or (resp.status_code == 200 and 'login' not in resp.url):
            print("[iVASMS] ✅ লগইন সফল হয়েছে")
            is_logged_in_site5 = True
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            csrf_input = soup.find('input', {'name': '_token'})
            if csrf_input:
                csrf_token_site5 = csrf_input.get('value')
            
            return True
        else:
            print("[iVASMS] ❌ লগইন ব্যর্থ")
            return False
            
    except Exception as e:
        print(f"[iVASMS] ❌ লগইনে ত্রুটি: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_session_site5():
    
    global csrf_token_site5
    try:
        resp = session5.get(SMS_RECEIVED_URL5, timeout=HTTP_TIMEOUT5)
        if 'login' in resp.url.lower():
            return False
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        csrf_input = soup.find('input', {'name': '_token'})
        if csrf_input:
            csrf_token_site5 = csrf_input.get('value')
            return True
        return False
    except:
        return False

def get_csrf_token_site5():
    
    global csrf_token_site5
    try:
        resp = session5.get(SMS_RECEIVED_URL5, timeout=HTTP_TIMEOUT5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        csrf_input = soup.find('input', {'name': '_token'})
        if csrf_input:
            csrf_token_site5 = csrf_input.get('value')
            return True
    except Exception as e:
        print(f"[iVASMS] ❌ আনতে ত্রুটি CSRF token: {e}")
    return False

def sms_loop_for_ivasms_account(site_key, account):
    
    global account_stop_events
    account_id = account.get("id")
    username = account.get("username")
    password = account.get("password")
    api_key = account.get("api_key", "")
    site_name = SETTINGS[site_key]["name"]
    
    stop_key = f"{site_key}_{account_id}"
    account_stop_events[stop_key] = Event()
    stop_event = account_stop_events[stop_key]
    
    API_URL = SETTINGS[site_key].get("api_url", "https://maroon-wombat-183778.hostingersite.com/apiivasms/api.php")
    HTTP_TIMEOUT5 = SETTINGS[site_key]["timeout"]
    CHECK_INTERVAL5 = SETTINGS[site_key]["check_interval"]
    
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    sent_messages_local = set()
    message_lock = threading.Lock()
    
    def load_sent_messages():
        nonlocal sent_messages_local
        sent_file = f"sent_messages_{site_key}_{account_id}.json"
        if os.path.exists(sent_file):
            try:
                with open(sent_file, 'r') as f:
                    sent_messages_local = set(json.load(f))
            except:
                sent_messages_local = set()
    
    def save_sent_messages():
        sent_file = f"sent_messages_{site_key}_{account_id}.json"
        try:
            msgs = list(sent_messages_local)[-500:]
            with open(sent_file, 'w') as f:
                json.dump(msgs, f)
        except Exception as e:
            print(f"[{site_name}] ({username}) ❌ পাঠানো মেসেজ সেভে ত্রুটি: {e}")
    
    def fetch_sms_via_api():
        try:
            params = {
                'api_key': api_key,
                'username': username,
                'password': password,
                '_t': int(time.time() * 1000)
            }
            resp = requests.get(API_URL, params=params, timeout=HTTP_TIMEOUT5, verify=False)
            
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    if data.get('success') and data.get('codes'):
                        return data['codes']
                    elif data.get('success'):
                        return []
                    else:
                        error_msg = data.get('error', data.get('message', 'Unknown error'))
                        print(f"[{site_name}] ({username}) ⚠️ API ত্রুটি: {error_msg}")
                        return []
                except json.JSONDecodeError:
                    print(f"[{site_name}] ({username}) ⚠️ অবৈধ রেসপন্স JSON")
                    return []
            else:
                print(f"[{site_name}] ({username}) ❌ রেসপন্স স্ট্যাটাস: {resp.status_code}")
                return []
        except Exception as e:
            print(f"[{site_name}] ({username}) ❌ ডাটা আনতে ত্রুটি: {e}")
            return []
    
    if not api_key:
        print_monitoring_box(site_name, username, "❌", "কী API পাওয়া যায়নি!")
        return
    
    print_monitoring_box(site_name, username, "🌐", "মনিটরিং শুরু হয়েছে মাধ্যমে API...")
    load_sent_messages()
    print(f"[{site_name}] ({username}) ✅ মনিটরিং শুরু প্রতি {CHECK_INTERVAL5} সেকেন্ড... (API চালু)")
    
    while not stop_event.is_set():
        try:
            if stop_event.is_set():
                break
                
            messages = fetch_sms_via_api()
            
            if stop_event.is_set():
                break
            
            new_count = 0
            for msg in messages:
                if stop_event.is_set():
                    break
                
                phone = msg.get('phone', msg.get('number', ''))
                message_text = msg.get('message', msg.get('sms', msg.get('text', '')))
                msg_time = msg.get('time', msg.get('date', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                
                if not phone or not message_text:
                    continue
                    
                msg_key = f"{phone}|{message_text[:50]}"
                
                if msg_key not in sent_messages_local:
                    otp_val, sms_text = extract_from_message(message_text)
                    service_name = f"[{detect_service(message_text)}]"
                    formatted_msg = format_otp_message_v2(phone, sms_text, service_name, otp_val)
                    
                    send_otp_to_user(clean_number(phone), formatted_msg, phone, None, otp_val)
                    if True:
                        print(f"✅ {site_name} ({username}): কোড পাঠানো হয়েছে: {mask_number(phone)}")
                    
                    sent_messages_local.add(msg_key)
                    new_count += 1
            
            if new_count > 0:
                save_sent_messages()
                print(f"[{site_name}] ({username}) 📨 পাঠানো হয়েছে {new_count} নতুন মেসেজ")
            else:
                print_monitoring_box(site_name, username, "📭", "কোনো কোড নেই")
            
        except Exception as e:
            if stop_event.is_set():
                break
            print_monitoring_box(site_name, username, "❌", f"অপ্রত্যাশিত ত্রুটি: {str(e)}")
            time.sleep(10)
        
        if stop_event.wait(CHECK_INTERVAL5):
            break
    
    print(f"[{site_name}] ({username}) 🛑 মনিটরিং সফলভাবে বন্ধ হয়েছে")

def sms_loop_requests_based(site_key, account):
    
    global account_stop_events
    
    account_id = account.get("id")
    username = account.get("username")
    password = account.get("password")
    site_name = SETTINGS[site_key]["name"]
    
    stop_key = f"{site_key}_{account_id}"
    account_stop_events[stop_key] = Event()
    stop_event = account_stop_events[stop_key]
    
    BASE_URL = SETTINGS[site_key]["base_url"]
    if not BASE_URL.startswith("http"):
        BASE_URL = "http://" + BASE_URL.lstrip(":")
    
    LOGIN_PAGE_URL = SETTINGS[site_key]["login_page_url"]
    LOGIN_POST_URL = SETTINGS[site_key]["login_post_url"]
    AJAX_PATH = SETTINGS[site_key].get("ajax_path", "/agent/res/data_smscdr.php")
    CHECK_INTERVAL = SETTINGS[site_key]["check_interval"]
    TIMEOUT_LOCAL = SETTINGS[site_key].get("timeout", 60)
    
    if "/ints" in BASE_URL:
        AJAX_URL = BASE_URL + AJAX_PATH
    elif "/ints" in AJAX_PATH:
        AJAX_URL = BASE_URL + AJAX_PATH
    else:
        AJAX_URL = BASE_URL + AJAX_PATH
    
    print(f"[{site_name}] ({username}) 🔗 AJAX URL: {AJAX_URL}")
    
    last_message_file = f"last_message_{site_key}_{account_id}.txt"
    sent_messages_file = f"sent_messages_{site_key}_{account_id}.json"
    last_seen_key_local = ""
    sent_messages_local = set()
    session = requests.Session()
    session.verify = False
    is_logged_in = False
    
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    })
    
    def load_last_seen():
        nonlocal last_seen_key_local
        if os.path.exists(last_message_file):
            try:
                with open(last_message_file, "r", encoding="utf-8") as f:
                    last_seen_key_local = f.read().strip()
            except:
                last_seen_key_local = ""
    
    def save_last_seen():
        try:
            with open(last_message_file, "w", encoding="utf-8") as f:
                f.write(last_seen_key_local)
        except:
            pass
    
    def load_sent_messages():
        nonlocal sent_messages_local
        if os.path.exists(sent_messages_file):
            try:
                with open(sent_messages_file, 'r') as f:
                    sent_messages_local = set(json.load(f))
            except:
                sent_messages_local = set()
    
    def save_sent_messages():
        try:
            msgs = list(sent_messages_local)[-500:]
            with open(sent_messages_file, 'w') as f:
                json.dump(msgs, f)
        except:
            pass
    
    def login():
        nonlocal is_logged_in
        print(f"[{site_name}] ({username}) 🔐 লগইন হচ্ছে...")
        
        try:
            resp = session.get(LOGIN_PAGE_URL, timeout=TIMEOUT_LOCAL)
            
            if resp.status_code != 200:
                print(f"[{site_name}] ({username}) ⚠️ লগইন পেজ খুলতে ব্যর্থ: {resp.status_code}")
                return False
            
            match = re.search(r'What is (\d+) \+ (\d+)', resp.text)
            if not match:
                match = re.search(r'(\d+)\s*\+\s*(\d+)', resp.text)
            
            if not match:
                print(f"[{site_name}] ({username}) ⚠️ খুঁজে পাওয়া যায়নি Captcha, চেষ্টা ছাড়া captcha...")
                captcha_answer = ""
            else:
                captcha_answer = str(int(match.group(1)) + int(match.group(2)))
                print(f"[{site_name}] ({username}) 🧮 Captcha: {match.group(1)} + {match.group(2)} = {captcha_answer}")
            
            crlf_match = re.search(r"name=['\"]crlf['\"].*?value=['\"]([^'\"]+)['\"]", resp.text)
            if not crlf_match:
                crlf_match = re.search(r"value=['\"]([^'\"]+)['\"].*?name=['\"]crlf['\"]", resp.text)
            
            payload = {
                'username': username,
                'password': password,
            }
            if captcha_answer:
                payload['capt'] = captcha_answer
            
            if crlf_match:
                payload['crlf'] = crlf_match.group(1)
                print(f"[{site_name}] ({username}) 🔑 বের করা হয়েছে crlf token")
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': LOGIN_PAGE_URL,
                'Origin': BASE_URL.rstrip('/'),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }
            
            resp = session.post(LOGIN_POST_URL, data=payload, headers=headers, timeout=TIMEOUT_LOCAL, allow_redirects=True)
            
            print(f"[{site_name}] ({username}) 📊 Response URL: {resp.url}")
            
            if ("dashboard" in resp.text.lower() or 
                "logout" in resp.text.lower() or 
                "agent" in resp.url.lower() or 
                "reports" in resp.url.lower() or 
                "smscdr" in resp.text.lower() or
                "signin" in resp.text.lower() or
                resp.url != LOGIN_PAGE_URL):
                print(f"[{site_name}] ({username}) ✅ লগইন সফল হয়েছে")
                is_logged_in = True
                return True
            
            if 'dashboard' in resp.text.lower() or 'logout' in resp.text.lower() or 'reports' in resp.url.lower():
                print(f"[{site_name}] ({username}) ✅ লগইন সফল (dashboard detected)")
                is_logged_in = True
                return True
            
            if resp.url != LOGIN_PAGE_URL and 'login' not in resp.url.lower():
                print(f"[{site_name}] ({username}) ✅ লগইন সফল (redirected)")
                is_logged_in = True
                return True
            
            sms_page_path = "/agent/SMSCDRReports" if "/ints" in BASE_URL else "/ints/agent/SMSCDRReports"
            test_resp = session.get(BASE_URL.rstrip('/') + sms_page_path, timeout=15)
            if test_resp.status_code == 200 and 'login' not in test_resp.url.lower():
                print(f"[{site_name}] ({username}) ✅ লগইন সফল (verified)")
                is_logged_in = True
                return True
            
            print(f"[{site_name}] ({username}) ❌ লগইন ব্যর্থ")
            return False
            
        except Exception as e:
            print(f"[{site_name}] ({username}) ❌ লগইনে ত্রুটি: {e}")
            return False
    
    def get_sesskey_from_page(html_text):
        match = re.search(r'sesskey=([A-Za-z0-9=]+)', html_text)
        if match:
            return match.group(1)
        return None
    
    current_sesskey = None
    
    def fetch_sms_data():
        nonlocal is_logged_in, current_sesskey
        
        sms_page_path = "/agent/SMSCDRReports" if "/ints" in BASE_URL else "/ints/agent/SMSCDRReports"
        referer_url = BASE_URL.rstrip('/') + sms_page_path
        
        if site_key == "GROUP":
            for retry in range(3):
                try:
                    page_resp = session.get(referer_url, timeout=TIMEOUT_LOCAL)
                    
                    if page_resp.status_code == 200:
                        if 'login' in page_resp.text.lower() and 'password' in page_resp.text.lower():
                            soup = BeautifulSoup(page_resp.text, 'html.parser')
                            login_form = soup.find('input', {'name': 'password'})
                            if login_form:
                                is_logged_in = False
                                print(f"[{site_name}] ({username}) ⚠️ সেশন শেষ, আবার লগইন হচ্ছে...")
                                return []
                        
                        sesskey = get_sesskey_from_page(page_resp.text)
                        if sesskey:
                            current_sesskey = sesskey
                            print(f"[{site_name}] ({username}) 🔑 বের করা হয়েছে sesskey")
                            
                            today = datetime.now().strftime('%Y-%m-%d')
                            ajax_url = BASE_URL + AJAX_PATH
                            params = {
                                'fdate1': f'{today} 00:00:00',
                                'fdate2': f'{today} 23:59:59',
                                'frange': '',
                                'fclient': '',
                                'fnum': '',
                                'fcli': '',
                                'fgdate': '',
                                'fgmonth': '',
                                'fgrange': '',
                                'fgclient': '',
                                'fgnumber': '',
                                'fgcli': '',
                                'fg': '0',
                                'sesskey': sesskey
                            }
                            
                            ajax_headers = {
                                'Accept': 'application/json, text/javascript, */*; q=0.01',
                                'X-Requested-With': 'XMLHttpRequest',
                                'Referer': referer_url
                            }
                            
                            ajax_resp = session.get(ajax_url, params=params, headers=ajax_headers, timeout=TIMEOUT_LOCAL)
                            
                            if ajax_resp.status_code == 200:
                                try:
                                    data = ajax_resp.json()
                                    if 'aaData' in data:
                                        rows = data['aaData']
                                        if rows:
                                            print(f"[{site_name}] ({username}) ✅ আনা হয়েছে {len(rows)} মেসেজ মাধ্যমে AJAX")
                                            return rows
                                    elif isinstance(data, list):
                                        if data:
                                            print(f"[{site_name}] ({username}) ✅ আনা হয়েছে {len(data)} মেসেজ মাধ্যমে AJAX")
                                            return data
                                except:
                                    pass
                        
                        soup = BeautifulSoup(page_resp.text, 'html.parser')
                        table = soup.find('table')
                        if table:
                            tbody = table.find('tbody')
                            rows = tbody.find_all('tr') if tbody else table.find_all('tr')[1:]
                            data_rows = []
                            for row in rows:
                                cells = row.find_all('td')
                                if len(cells) >= 6:
                                    data_rows.append([cell.get_text(strip=True) for cell in cells])
                            if data_rows:
                                print(f"[{site_name}] ({username}) 📄 ব্যবহার HTML parsing বিকল্প হিসেবে")
                                return data_rows
                        return []
                        
                    elif page_resp.status_code in [502, 503, 504]:
                        if retry < 2:
                            print(f"[{site_name}] ({username}) ⚠️ সার্ভার ব্যস্ত ({page_resp.status_code}) - চেষ্টা {retry+1}/3...")
                            time.sleep(3 + retry * 2)
                            continue
                        print(f"[{site_name}] ({username}) ⚠️ সার্ভার ব্যস্ত ({page_resp.status_code})")
                        return []
                    else:
                        print(f"[{site_name}] ({username}) ⚠️ HTTP {page_resp.status_code}")
                        return []
                    
                except Exception as e:
                    if retry < 2 and ('Connection' in str(e) or 'Timeout' in str(e)):
                        time.sleep(2)
                        continue
                    print(f"[{site_name}] ({username}) ❌ ডাটা আনতে ত্রুটি: {e}")
                    is_logged_in = False
                    return []
            return []
        
        for retry in range(3):
            try:
                headers = {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Referer': referer_url,
                    'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
                }
                
                today = datetime.now()
                start_date = (today - timedelta(days=1)).strftime('%Y-%m-%d')
                end_date = (today + timedelta(days=1)).strftime('%Y-%m-%d')
                
                payload = {
                    'fdate1': f'{start_date} 00:00:00',
                    'fdate2': f'{end_date} 23:59:59',
                    'frange': '',
                    'fclient': '',
                    'fnum': '',
                    'fcli': '',
                    'fgdate': '',
                    'fgmonth': '',
                    'fgrange': '',
                    'fgclient': '',
                    'fgnumber': '',
                    'fgcli': '',
                    'fg': '0',
                    'sEcho': '1',
                    'iColumns': '8',
                    'sColumns': '',
                    'iDisplayStart': '0',
                    'iDisplayLength': '100',
                    'mDataProp_0': '0',
                    'mDataProp_1': '1',
                    'mDataProp_2': '2',
                    'mDataProp_3': '3',
                    'mDataProp_4': '4',
                    'mDataProp_5': '5',
                    'mDataProp_6': '6',
                    'mDataProp_7': '7',
                    'sSearch': '',
                    'bRegex': 'false',
                    'iSortCol_0': '0',
                    'sSortDir_0': 'desc',
                    'iSortingCols': '1'
                }
                
                resp = session.post(AJAX_URL, data=payload, headers=headers, timeout=TIMEOUT_LOCAL)
                
                if resp.status_code == 200:
                    try:
                        data = resp.json()
                        for key in ['data', 'aaData', 'rows']:
                            if key in data and isinstance(data[key], list):
                                return data[key]
                        is_logged_in = False
                    except Exception as je:
                        if 'login' in resp.text.lower() or 'signin' in resp.text.lower():
                            is_logged_in = False
                            print(f"[{site_name}] ({username}) ⚠️ সেশন শেষ, আবার লগইন হচ্ছে...")
                        else:
                            try:
                                soup = BeautifulSoup(resp.text, 'html.parser')
                                table = soup.find('table')
                                if table:
                                    tbody = table.find('tbody')
                                    rows = tbody.find_all('tr') if tbody else table.find_all('tr')[1:]
                                    data_rows = []
                                    for row in rows:
                                        cells = row.find_all('td')
                                        if len(cells) >= 6:
                                            data_rows.append([cell.get_text(strip=True) for cell in cells])
                                    if data_rows:
                                        print(f"[{site_name}] ({username}) 📄 ব্যবহার HTML parsing")
                                        return data_rows
                            except:
                                pass
                elif resp.status_code == 503:
                    if retry < 2:
                        time.sleep(3 + retry * 2)
                        continue
                    print(f"[{site_name}] ({username}) ⚠️ সার্ভার ব্যস্ত (503) - বিকল্প পদ্ধতিতে চেষ্টা চলছে...")
                    try:
                        page_resp = session.get(referer_url, timeout=TIMEOUT_LOCAL)
                        if page_resp.status_code == 200:
                            soup = BeautifulSoup(page_resp.text, 'html.parser')
                            table = soup.find('table')
                            if table:
                                tbody = table.find('tbody')
                                rows = tbody.find_all('tr') if tbody else table.find_all('tr')[1:]
                                data_rows = []
                                for row in rows:
                                    cells = row.find_all('td')
                                    if len(cells) >= 6:
                                        data_rows.append([cell.get_text(strip=True) for cell in cells])
                                if data_rows:
                                    print(f"[{site_name}] ({username}) 📄 ব্যবহার HTML parsing (বিকল্প)")
                                    return data_rows
                    except Exception as html_e:
                        print(f"[{site_name}] ({username}) ⚠️ ব্যর্থ HTML parsing: {html_e}")
                else:
                    print(f"[{site_name}] ({username}) ⚠️ HTTP {resp.status_code}")
                
                return []
                
            except Exception as e:
                if retry < 2 and ('Connection' in str(e) or 'Timeout' in str(e)):
                    time.sleep(2)
                    continue
                print(f"[{site_name}] ({username}) ❌ ডাটা আনতে ত্রুটি: {e}")
                is_logged_in = False
                return []
        return []
    
    print_monitoring_box(site_name, username, "🚀", "মনিটরিং শুরু হয়েছে Requests (হালকা ও দ্রুত)...")
    
    load_last_seen()
    load_sent_messages()
    
    if not login():
        print_monitoring_box(site_name, username, "❌", "প্রথম লগইন ব্যর্থ")
        return
    
    errors = 0
    print(f"[{site_name}] ({username}) ✅ মনিটরিং শুরু প্রতি {CHECK_INTERVAL} সেকেন্ড...")
    
    while not stop_event.is_set():
        try:
            if stop_event.is_set():
                break
            
            if not is_logged_in:
                if not login():
                    time.sleep(30)
                    continue
            
            raw_data = fetch_sms_data()
            
            if not raw_data:
                print_monitoring_box(site_name, username, "📭", "কোনো কোড নেই")
            else:
                data = []
                for row in raw_data:
                    if isinstance(row, list) and len(row) >= 6:
                        date_str = str(row[0]).strip() if row[0] else ""
                        number = re.sub(r'\D', '', str(row[2])) if row[2] else ""
                        sms = str(row[5]).strip() if row[5] else ""
                        
                        if date_str and number and len(number) >= 7 and sms:
                            
                            if any(x in sms.lower() for x in ["currency", "payout", "nan%", "100%", "0.008", "my payout", "client payout", "range", "number", "cli", "client"]):
                                continue
                            
                            
                            if sms.count(',') >= 5 and ('%' in sms or 'nan' in sms.lower()):
                                continue

                            
                            otp_val, _ = extract_from_message(sms)
                            if not otp_val and len(sms) < 5: 
                                continue
                                
                            data.append({'date': date_str, 'number': number, 'sms': sms})
                
                if not data:
                    print_monitoring_box(site_name, username, "📭", "কোনো কোড নেই")
                else:
                    data.sort(key=lambda x: x['date'], reverse=False) 
                    
                    new_messages = []
                    for msg in data:
                        key = f"{msg['date']}|{msg['number']}"
                        if key == last_seen_key_local:
                            new_messages = [] 
                            continue
                        if key not in sent_messages_local:
                            new_messages.append(msg)
                    
                    if new_messages:
                        print(f"[{site_name}] ({username}) 📨 {len(new_messages)} নতুন মেসেজ")
                        
                        
                        for msg in new_messages:
                            date_str = msg['date']
                            number = msg['number']
                            sms = msg['sms']
                            
                            otp_val, sms_text = extract_from_message(sms)
                            service_name = f"[{detect_service(sms)}]"
                            formatted_msg = format_otp_message_v2(number, sms_text, service_name, otp_val)
                            
                            if otp_val:
                                print(f"🔑 {site_name} ({username}): কোড পাওয়া গেছে {otp_val}")
                            
                            send_otp_to_user(clean_number(number), formatted_msg, number, None, otp_val)
                            
                           
                            key = f"{date_str}|{number}"
                            sent_messages_local.add(key)
                            last_seen_key_local = key
                        
                        save_last_seen()
                        save_sent_messages()
                    else:
                        print_monitoring_box(site_name, username, "📭", "কোনো কোড নেই")
            
            errors = 0
            
        except Exception as e:
            errors += 1
            print_monitoring_box(site_name, username, "❌", f"ত্রুটি ({errors}/5): {str(e)[:40]}")
            if errors >= 5:
                print(f"[{site_name}] ({username}) 🔄 আবার লগইন হচ্ছে...")
                if login():
                    errors = 0
                else:
                    time.sleep(30)
            time.sleep(5)
        
        if stop_event.wait(CHECK_INTERVAL):
            break
    
    print(f"[{site_name}] ({username}) 🛑 মনিটরিং বন্ধ করা হয়েছে")

def login_site8(account):
    username = account.get("username")
    password = account.get("password")
    
    
    session = requests.Session()
    session.verify = False
    
    print(f"[Site8/IMS] ({username}) 🔄 লগইন হচ্ছে...")
    try:
       
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive"
        })
        
        response = session.get(LOGIN_PAGE_URL8, timeout=HTTP_TIMEOUT8)
        if response.status_code == 403:
            
            response = session.get(LOGIN_PAGE_URL8, timeout=HTTP_TIMEOUT8, headers={"User-Agent": "Mozilla/5.0"})
        
        if response.status_code != 200:
            print(f"[Site8/IMS] ({username}) [!] লগইন পেজ খুলতে ব্যর্থ: {response.status_code}")
            return False, None
        
        html_content = response.text
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        csrf_token = None
        csrf_input = soup.find('input', {'name': '_token'})
        if csrf_input:
            csrf_token = str(csrf_input.get('value'))
        if not csrf_token:
            csrf_input = soup.find('input', {'name': 'csrf_token'})
            if csrf_input:
                csrf_token = str(csrf_input.get('value'))
        if not csrf_token:
            csrf_meta = soup.find('meta', {'name': 'csrf-token'})
            if csrf_meta:
                csrf_token = str(csrf_meta.get('content'))
        if not csrf_token:
            match = re.search(r'name=["\']_token["\'].*?value=["\']([^"\']+)["\']', html_content)
            if match:
                csrf_token = match.group(1)
        
        if csrf_token:
            print(f"[Site8/IMS] ({username}) [*] CSRF Token: {csrf_token[:20]}...")
        
        
        captcha_answer = None
        
        patterns = [
            r'(\d+)\s*\+\s*(\d+)\s*=', 
            r'What is (\d+) \+ (\d+)', 
            r'(\d+)\s*plus\s*(\d+)'
        ]
        
        
        for pattern in patterns:
            match = re.search(pattern, html_content, re.IGNORECASE)
            if match:
                captcha_answer = str(int(match.group(1)) + int(match.group(2)))
                break
        
        
        if not captcha_answer:
            b_tags = soup.find_all('b')
            nums = []
            for b in b_tags:
                text = b.get_text().strip()
                if text.isdigit():
                    nums.append(int(text))
            if len(nums) >= 2:
                captcha_answer = str(nums[0] + nums[1])
        
        if not captcha_answer:
            
            text = soup.get_text()
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    captcha_answer = str(int(match.group(1)) + int(match.group(2)))
                    break
        
        if not captcha_answer:
            print(f"[Site8/IMS] ({username}) [!] ক্যাপচা পাওয়া যায়নি")
            return False, None
        
        print(f"[Site8/IMS] ({username}) [*] Captcha: {captcha_answer}")
        
        login_data = {
            "username": username,
            "password": password,
            "capt": captcha_answer,
        }
        
        if csrf_token:
            login_data["_token"] = csrf_token
        
        form = soup.find('form')
        if form:
            for hidden in form.find_all('input', type='hidden'):
                name = hidden.get('name')
                value = hidden.get('value')
                if name and isinstance(name, str) and name not in login_data:
                    login_data[name] = str(value) if value is not None else ''

        
        login_headers = {
            "Referer": LOGIN_PAGE_URL8,
            "Origin": BASE_URL8,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = session.post(
            LOGIN_POST_URL8,
            data=login_data,
            headers=login_headers,
            timeout=HTTP_TIMEOUT8,
            allow_redirects=True
        )
        
        print(f"[Site8/IMS] ({username}) [DEBUG] Final URL: {response.url}")
        
        if any(x in response.url.lower() for x in ["/agent", "/dashboard", "/home"]) or \
           (response.status_code == 200 and "login" not in response.url.lower() and "signin" not in response.url.lower()):
            print(f"[Site8/IMS] ({username}) [+] লগইন সফল (Landed on: {response.url})")
            return True, session
        
        content_lower = response.text.lower()
        if "logout" in content_lower or "smscdr" in content_lower or "agent" in content_lower:
            print(f"[Site8/IMS] ({username}) [+] লগইন সফল (Detected via content)")
            return True, session

        print(f"[Site8/IMS] ({username}) [!] লগইন ব্যর্থ")
        return False, None
    except Exception as e:
        print(f"[Site8/IMS] ({username}) [!] লগইনে ত্রুটি: {e}")
        return False, None

def sms_loop_for_ims_account(site_key, account):
    site_name = SETTINGS[site_key]["name"]
    username = account.get("username")
    password = account.get("password")
    account_id = account.get("id")
    stop_event = account_stop_events.get(f"{site_key}_{account_id}", Event())
    
    session = requests.Session()
    session.verify = False
    is_logged_in = False
    
    last_message_file = f"last_message_{site_key}_{account_id}.txt"
    last_seen_key_local = ""
    
    def load_last_seen():
        nonlocal last_seen_key_local
        if os.path.exists(last_message_file):
            try:
                with open(last_message_file, "r", encoding="utf-8") as f:
                    last_seen_key_local = f.read().strip()
            except: pass
    def save_last_seen():
        try:
            with open(last_message_file, "w", encoding="utf-8") as f:
                f.write(last_seen_key_local)
        except: pass

    print_monitoring_box(site_name, username, "🚀", "মনিটরিং শুরু হচ্ছে...")
    
    success, new_session = login_site8(account)
    if success:
        session = new_session
        is_logged_in = True
    else:
        print_monitoring_box(site_name, username, "❌", "লগইন ব্যর্থ")
    
    load_last_seen()
    errors = 0
    
    while not stop_event.is_set():
        try:
            
            current_account = get_account_by_id(site_key, account_id)
            if current_account and current_account.get("password") != password:
                print(f"[Site8/IMS] ({username}) 🔑 পাসওয়ার্ড পরিবর্তন শনাক্ত হয়েছে, আবার লগইন হচ্ছে...")
                password = current_account.get("password")
                success, new_session = login_site8(current_account)
                if success:
                    session = new_session
                    is_logged_in = True
                else:
                    is_logged_in = False
                    time.sleep(30)
                    continue

            if not is_logged_in:
                success, new_session = login_site8(current_account or account)
                if success:
                    session = new_session
                    is_logged_in = True
                else:
                    time.sleep(30)
                    continue

            today = datetime.now().strftime('%Y-%m-%d')
            
            codes_html = ""
            try:
                resp_codes = session.get(BASE_URL8 + "/ints/agent/SMSCDRReports", timeout=HTTP_TIMEOUT8)
                codes_html = resp_codes.text
                if 'login' in resp_codes.url.lower():
                    is_logged_in = False
                    continue
            except Exception as e:
                print(f"[Site8/IMS] ({username}) [!] Error loading codes page: {e}")
                is_logged_in = False
                continue

            sesskey = ""
            sesskey_match = re.search(r'sesskey=([A-Za-z0-9=]+)', codes_html)
            if sesskey_match:
                sesskey = sesskey_match.group(1)
            else:
                is_logged_in = False
                continue

            params = {
                'fdate1': f'{today} 00:00:00',
                'fdate2': f'{today} 23:59:59',
                'frange': '', 'fclient': '', 'fnum': '', 'fcli': '',
                'fgdate': '', 'fgmonth': '', 'fgrange': '', 'fgclient': '',
                'fgnumber': '', 'fgcli': '', 'fg': '0', 'sesskey': sesskey
            }

            ajax_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': BASE_URL8 + "/ints/agent/SMSCDRReports"
            }
            
            r = session.get("http://45.82.67.20/ints/agent/res/data_smscdr.php", params=params, headers=ajax_headers, timeout=HTTP_TIMEOUT8)
            
            if r.status_code != 200 or 'login' in r.url.lower():
                is_logged_in = False
                continue

            data_json = r.json()
            if data_json.get('aaData'):
                rows = data_json['aaData']
            else:
                rows = data_json if isinstance(data_json, list) else []
            
            if not rows:
                print_monitoring_box(site_name, username, "📭", "কোনো কোড নেই")
            else:
                
                try:
                    rows.sort(key=lambda x: str(x[0]) if isinstance(x, list) and len(x) > 0 else "", reverse=True)
                except:
                    pass

                new_messages = []
                for row in rows:
                    if isinstance(row, list) and len(row) >= 6:
                        date_str = str(row[0]).strip()
                        number = re.sub(r'\D', '', str(row[2]))
                        sms = str(row[5]).strip()
                        
                        
                        if sms.count(',') > 3 or sms.count('%') > 1 or 'NAN%' in sms:
                            continue
                        
                        
                        if re.match(r'^[\d.,%|NAN/]+$', sms):
                            continue
                            
                        key = f"{date_str}|{number}"
                        if key == last_seen_key_local: break
                        new_messages.append({'date': date_str, 'number': number, 'sms': sms})
                
                if new_messages:
                    
                    last_seen_key_local = f"{new_messages[0]['date']}|{new_messages[0]['number']}"
                    save_last_seen()
                    
                    print(f"[{site_name}] ({username}) 📨 {len(new_messages)} নতুন মেসেজ")
                   
                    
                    for msg in reversed(new_messages):
                        otp_val, sms_text = extract_from_message(msg['sms'])
                        
                        
                        service_name = f"[{detect_service(sms_text)}]"
                        formatted_msg = format_otp_message_v2(msg['number'], sms_text, service_name, otp_val)
                        
                        print(f"🔑 {site_name} ({username}): কোড পাওয়া গেছে {otp_val}")
                        
                        success = False
                        for retry in range(3):
                            try:
                                send_otp_to_user(clean_number(msg['number']), formatted_msg, msg['number'], None, otp_val)
                                success = True
                                break
                            except Exception as e:
                                if "429" in str(e):
                                    wait_time = 35 
                                    match = re.search(r'after (\d+)', str(e))
                                    if match: wait_time = int(match.group(1)) + 2
                                    print(f"⚠️ Telegram 429 (Flood Control): Waiting {wait_time}s...")
                                    time.sleep(wait_time)
                                else:
                                    print(f"❌ Error sending: {e}")
                                    break
                else:
                    print_monitoring_box(site_name, username, "📭", "কোনো কোড নেই")
            
            errors = 0
        except Exception as e:
            errors += 1
            if errors >= 5:
                is_logged_in = False
            time.sleep(10)

        if stop_event.wait(SETTINGS[site_key].get("check_interval", 16)):
            break


def start_monitoring_for_account(site_key, account):
    
    if site_key == "Number_Panel":
        sms_loop_for_number_panel_account(site_key, account)
    elif site_key == "iVASMS":
        sms_loop_for_ivasms_account(site_key, account)
    elif site_key == "IMS":
        sms_loop_for_ims_account(site_key, account)
    elif site_key == "Roxy SMS":
        sms_loop_for_roxy_account(site_key, account)
    elif site_key == "TimeSMS":
        sms_loop_for_timesms_account(site_key, account)
    else:
        sms_loop_requests_based(site_key, account)

def sms_loop_for_timesms_account(site_key, account):
    site_name = SETTINGS[site_key]["name"]
    username = account.get("username")
    password = account.get("password")
    account_id = account.get("id")
    stop_event = account_stop_events.get(f"{site_key}_{account_id}", Event())
    
    sess = requests.Session()
    sess.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    is_logged_in = False
    
    last_message_file = f"last_message_{site_key}_{account_id}.txt"
    last_seen_key_local = ""
    
    def load_last_seen():
        nonlocal last_seen_key_local
        if os.path.exists(last_message_file):
            try:
                with open(last_message_file, "r", encoding="utf-8") as f:
                    last_seen_key_local = f.read().strip()
            except: pass
    def save_last_seen():
        try:
            with open(last_message_file, "w", encoding="utf-8") as f:
                f.write(last_seen_key_local)
        except: pass

    print_monitoring_box(site_name, username, "🚀", "মনিটরিং শুরু হচ্ছে...")
    load_last_seen()
    
    login_url = SETTINGS[site_key]["login_page_url"]
    submit_url = SETTINGS[site_key]["login_post_url"]
    ajax_url = SETTINGS[site_key]["base_url"] + "/agent/res/data_smscdr.php"
    
    while not stop_event.is_set():
        try:
            if not is_logged_in:
                resp = sess.get(login_url, timeout=15)
                captcha = solve_captcha_timesms(resp.text)
                if captcha:
                    data = {'username': username, 'password': password, 'capt': captcha}
                    login_resp = sess.post(submit_url, data=data, headers={'Referer': login_url}, timeout=15, allow_redirects=True)
                    if 'login' not in str(login_resp.url).lower():
                        is_logged_in = True
                        print_monitoring_box(site_name, username, "✅", "লগইন সফল হয়েছে")
                    else:
                        print_monitoring_box(site_name, username, "❌", "লগইন ব্যর্থ")
                        time.sleep(30); continue
                else:
                    print_monitoring_box(site_name, username, "❌", "ক্যাপচা সমাধান ব্যর্থ")
                    time.sleep(30); continue

            today = datetime.now()
            fdate1 = today.strftime('%Y-%m-%d') + " 00:00:00"
            fdate2 = today.strftime('%Y-%m-%d') + " 23:59:59"
            params = {'fdate1': fdate1, 'fdate2': fdate2, 'fg': '0', 'sEcho': '1', 'iDisplayStart': '0', 'iDisplayLength': '500', 'iSortCol_0': '0', 'sSortDir_0': 'desc'}
            
            r = sess.get(ajax_url, params=params, headers={'Referer': SETTINGS[site_key]["base_url"] + "/agent/SMSCDRReports", 'X-Requested-With': 'XMLHttpRequest'}, timeout=30)
            if r.status_code != 200 or 'login' in r.url.lower():
                is_logged_in = False; continue

            try:
                data = r.json()
            except Exception as e:
                print(f"[{site_name}] JSON Decode Error: {e}")
                is_logged_in = False; continue
                
            rows = data.get('aaData', [])
            
            if rows:
                new_messages = []
                # Ensure rows are sorted by date descending (newest first)
                try:
                    # TimeSMS date format is YYYY-MM-DD HH:MM:SS
                    rows.sort(key=lambda x: str(x[0]).strip() if len(x) > 0 else "", reverse=True)
                except:
                    pass
                
                for row in rows:
                    if len(row) >= 6:
                        msg_date, msg_num, msg_cli, msg_text = str(row[0]).strip(), str(row[2]).strip(), str(row[3]).strip(), str(row[5]).strip()
                        
                        # Skip if it's not a real date (e.g. headers or junk data)
                        if not re.match(r'\d{4}-\d{2}-\d{2}', msg_date):
                            continue

                        # Use same logic as Roxy SMS for TimeSMS to ensure we don't get empty/wrong text
                        if msg_text == "$" or len(msg_text) < 2:
                            for idx in [4, 6, 3]: 
                                if len(row) > idx:
                                    potential_msg = str(row[idx]).strip()
                                    if potential_msg and potential_msg != "$":
                                        msg_text = potential_msg
                                        break
                        
                        msg_key = f"{msg_date}_{msg_num}_{msg_text[:20]}" # More unique key
                        if msg_key == last_seen_key_local: break
                        new_messages.append({'date': msg_date, 'number': msg_num, 'cli': msg_cli, 'sms': msg_text, 'key': msg_key})
                
                if new_messages:
                    # Update last_seen_key_local with the most recent message (first in rows after sorting descending)
                    is_initial = not os.path.exists(last_message_file) or os.path.getsize(last_message_file) == 0
                    
                    last_seen_key_local = new_messages[0]['key']
                    save_last_seen()
                    
                    if is_initial:
                        print_monitoring_box(site_name, username, "🔔", "মনিটরিং শুরু হয়েছে: শুধু সর্বশেষ কোড আনা হচ্ছে")
                        messages_to_process = [new_messages[0]]
                    else:
                        print_monitoring_box(site_name, username, "🔔", f"কোড পাওয়া গেছে: {len(new_messages)} নতুন মেসেজ")
                        # Process messages in reverse order (oldest to newest among new ones)
                        messages_to_process = reversed(new_messages)
                    
                    for msg in messages_to_process:
                        otp_val, clean_sms = extract_from_message(msg['sms'])
                        service_name = f"[{detect_service(clean_sms)}]"
                        formatted = format_otp_message_v2(msg['number'], clean_sms, service_name, otp_val)
                        send_otp_to_user(clean_number(msg['number']), formatted, msg['number'], None, otp_val)
                        
                        # Save details for statistics or logs if needed
                        sent_file = f"sent_messages_{site_key}_{account_id}.json"
                        try:
                            sent_msgs = []
                            if os.path.exists(sent_file):
                                with open(sent_file, 'r', encoding='utf-8') as f:
                                    sent_msgs = json.load(f)
                            
                            sent_msgs.append({
                                'date': msg['date'],
                                'number': msg['number'],
                                'text': msg['sms'],
                                'otp': otp_val,
                                'timestamp': time.time()
                            })
                            
                            # Keep only last 100 messages
                            if len(sent_msgs) > 100:
                                sent_msgs = sent_msgs[-100:]
                                
                            with open(sent_file, 'w', encoding='utf-8') as f:
                                json.dump(sent_msgs, f, indent=2, ensure_ascii=False)
                        except Exception as e:
                            print(f"[{site_name}] Error saving sent messages: {e}")
                else:
                    print_monitoring_box(site_name, username, "🟢", "কোনো কোড নেই")
            else:
                print_monitoring_box(site_name, username, "🟢", "কোনো কোড নেই")

        except Exception as e:
            print(f"[{site_name}] Error: {e}")
            is_logged_in = False
        time.sleep(SETTINGS[site_key].get("check_interval", 5))

def sms_loop_for_roxy_account(site_key, account):
    site_name = SETTINGS[site_key]["name"]
    username = account.get("username")
    password = account.get("password")
    account_id = account.get("id")
    stop_event = account_stop_events.get(f"{site_key}_{account_id}", Event())
    
    scraper = cloudscraper.create_scraper()
    is_logged_in = False
    
    last_message_file = f"last_message_{site_key}_{account_id}.txt"
    last_seen_key_local = ""
    
    def load_last_seen():
        nonlocal last_seen_key_local
        if os.path.exists(last_message_file):
            try:
                with open(last_message_file, "r", encoding="utf-8") as f:
                    last_seen_key_local = f.read().strip()
            except: pass
    def save_last_seen():
        try:
            with open(last_message_file, "w", encoding="utf-8") as f:
                f.write(last_seen_key_local)
        except: pass

    print_monitoring_box(site_name, username, "🚀", "মনিটরিং শুরু হচ্ছে...")
    load_last_seen()
    
    login_url = "http://www.roxysms.net/signin"
    ajax_url = "http://www.roxysms.net/agent/res/data_smscdr.php"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "http://www.roxysms.net/agent/SMSCDRReports"
    }
    
    while not stop_event.is_set():
        try:
            if not is_logged_in:
                payload = {"username": username, "password": password}
                try:
                    login_resp = scraper.post(login_url, data=payload, headers=headers, timeout=30)
                    if login_resp.status_code == 200 and ("success" in login_resp.text.lower() or "logout" in login_resp.text.lower()):
                        is_logged_in = True
                        print_monitoring_box(site_name, username, "✅", "লগইন সফল হয়েছে")
                    else:
                        print_monitoring_box(site_name, username, "❌", "লগইন ব্যর্থ, আবার চেষ্টা চলছে...")
                        time.sleep(30)
                        continue
                except Exception as e:
                    print(f"[{site_name}] Login Error: {e}")
                    time.sleep(30)
                    continue

            today = datetime.now().strftime('%Y-%m-%d')
            params = {
                'fdate1': f'{today} 00:00:00',
                'fdate2': f'{today} 23:59:59',
                'fg': '0'
            }
            
            try:
                r = scraper.get(ajax_url, params=params, headers=headers, timeout=30)
                
                if r.status_code != 200 or 'login' in r.url.lower():
                    is_logged_in = False
                    continue

                data = r.json()
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                print(f"[{site_name}] Connection issue, retrying: {e}")
                is_logged_in = False
                time.sleep(10)
                continue
            except Exception as e:
                print(f"[{site_name}] Request Error: {e}")
                is_logged_in = False
                time.sleep(10)
                continue
            rows = data.get('aaData', []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
            
            if rows:
                new_messages = []
                for row in rows:
                    if isinstance(row, list) and len(row) >= 6:
                        d_str, num, msg_txt = str(row[0]), re.sub(r'\D', '', str(row[2])), str(row[5])
                        
                        if msg_txt == "$" or len(msg_txt) < 2:
                            
                            for idx in [4, 6, 3]: 
                                if len(row) > idx:
                                    potential_msg = str(row[idx]).strip()
                                    if potential_msg and potential_msg != "$":
                                        msg_txt = potential_msg
                                        break
                        
                        key = f"{d_str}|{num}"
                        if key == last_seen_key_local: break
                        new_messages.append({'date': d_str, 'number': num, 'sms': msg_txt})
                
                if new_messages:
                    last_seen_key_local = f"{new_messages[0]['date']}|{new_messages[0]['number']}"
                    save_last_seen()
                    
                    
                    for msg in reversed(new_messages):
                        otp_val, clean_sms = extract_from_message(msg['sms'])
                        service_name = f"[{detect_service(clean_sms)}]"
                        formatted = format_otp_message_v2(msg['number'], clean_sms, service_name, otp_val)
                        send_otp_to_user(clean_number(msg['number']), formatted, msg['number'], None, otp_val)
                else:
                    print_monitoring_box(site_name, username, "📭", "কোনো নতুন কোড নেই")
            else:
                print_monitoring_box(site_name, username, "📭", "কোনো কোড নেই")
                
        except Exception as e:
            print(f"[{site_name}] Error: {e}")
            is_logged_in = False
            time.sleep(10)

        if stop_event.wait(SETTINGS[site_key].get("check_interval", 5)):
            break

if __name__ == "__main__":
    # --- Render Web Service এর জন্য ছোট ওয়েব সার্ভার (পোর্ট খোলা রাখে) ---
    from http.server import BaseHTTPRequestHandler, HTTPServer

    class _PingHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Bot is running")
        def do_HEAD(self):
            self.send_response(200)
            self.end_headers()
        def log_message(self, *args):
            pass

    def _run_web_server():
        port = int(os.environ.get("PORT", "10000"))
        HTTPServer(("0.0.0.0", port), _PingHandler).serve_forever()

    Thread(target=_run_web_server, daemon=True).start()
    # --------------------------------------------------------------------

    load_data()
    
    monitoring_threads = []
    print("🚀 মাল্টি-অ্যাকাউন্ট মনিটরিং সিস্টেম চালু হচ্ছে...")
    
    for site_key in ["GROUP", "Fly sms", "Number_Panel", "Bolt", "iVASMS", "MSI", "proton SMS", "IMS", "Roxy SMS", "TimeSMS"]:
        if SETTINGS[site_key]["enabled"]:
            accounts = get_site_accounts(site_key)
            site_name = SETTINGS[site_key]["name"]
            
            if accounts:
                print(f"\n📋 {site_name}: পাওয়া গেছে {len(accounts)} অ্যাকাউন্ট")
                for account in accounts:
                    username = account.get('username', 'N/A')
                    thread = Thread(target=start_monitoring_for_account, args=(site_key, account), daemon=True)
                    monitoring_threads.append(thread)
                    thread.start()
                    print(f"  ✅ মনিটরিং শুরু: {username}")
            else:
                print(f"  ⚠️ {site_name}: কোনো অ্যাকাউন্ট নেই")
    
    print(f"\n🎯 মোট Threads সক্রিয়: {len(monitoring_threads)}")
    
    import requests
    try:
        bot_token = BOT_TOKEN
        delete_webhook_url = f"https://api.telegram.org/bot{bot_token}/deleteWebhook?drop_pending_updates=true"
        response = requests.get(delete_webhook_url)
        print(f"🔄 মুছে ফেলা হয়েছে webhook এবং অপেক্ষমাণ আপডেট পরিষ্কার: {response.json()}")
    except Exception as e:
        print(f"⚠️ মুছতে ত্রুটি: webhook: {e}")
    
    print("\n✨ বট কাজের জন্য প্রস্তুত!\n")
    
    try:
        from telebot.types import BotCommand
        commands = [
            BotCommand("start", "Start the bot"),
            BotCommand("getnumber", "Get a number"),
            BotCommand("account", "My account"),
            BotCommand("help", "Help guide"),
            BotCommand("withdraw", "Withdraw balance"),
            BotCommand("hom", "Main menu"),
            BotCommand("language", "Change language"),
            BotCommand("bonus", "Bonus system")
        ]
        bot.set_my_commands(commands)
        print("✅ কমান্ড সফলভাবে নিবন্ধিত হয়েছে!")
    except Exception as e:
        print(f"⚠️ কমান্ড নিবন্ধনে ত্রুটি: {e}")
    
    max_retries = 5
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            print(f"🚀 শুরু করার চেষ্টা polling (চেষ্টা {attempt + 1}/{max_retries})...")
            bot.infinity_polling(timeout=60, long_polling_timeout=60, skip_pending=True)
            break
        except Exception as e:
            if "409" in str(e) or "Conflict" in str(e):
                if attempt < max_retries - 1:
                    print(f"⚠️ সংঘাত polling (409) - আবার চেষ্টা হবে {retry_delay} সেকেন্ড পরে...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    print(f"❌ বট চালু করতে ব্যর্থ {max_retries} চেষ্টার পর!")
                    raise
            else:
                raise