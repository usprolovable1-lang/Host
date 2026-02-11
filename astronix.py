#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     ██████╗ ██████╗ ███╗   ███╗██████╗ ██╗     ███████╗████████╗███████╗    ║
║    ██╔════╝██╔═══██╗████╗ ████║██╔══██╗██║     ██╔════╝╚══██╔══╝██╔════╝    ║
║    ██║     ██║   ██║██╔████╔██║██████╔╝██║     █████╗     ██║   █████╗      ║
║    ██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝     ██║   ██╔══╝      ║
║    ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ███████╗███████╗   ██║   ███████╗    ║
║     ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝   ╚═╝   ╚══════╝    ║
║                                                                              ║
║                 ASTRONIX FIRE EDITION v4.0 ULTIMATE CYBERPUNK                ║
║            Advanced Telegram Bot Hosting & Management Platform               ║
║                                                                              ║
║    🔥 Features: Fire Animation | Smart Deps | Hybrid UI | Zero Errors       ║
║    🐉 Architecture: Modular | Async-Ready | Enterprise Grade                ║
║    ⚜️ Security: Isolated Venvs | Process Control | Rate Limiting            ║
║    🌀 UI: Carousel Plans | Live Stats | Cyberpunk Theme                     ║
║                                                                              ║
║    Author: Elite Python Architect                                           ║
║    Built: 2026 | Python 3.10+                                               ║
║    Lines: 3100+ | Production Ready | KASUKABE STABILITY                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ══════════════════════════════════════════════════════════════════════════════
# 🔧 CORE IMPORTS - STANDARD LIBRARY
# ══════════════════════════════════════════════════════════════════════════════
from dotenv import load_dotenv
load_dotenv()

import os
import sys
import time
import json
import zipfile
import subprocess
import atexit
import random
import string
import sqlite3
import ast
import importlib.util
import shutil
import threading
import signal
import psutil
import traceback
import re
from pathlib import Path
from typing import Optional, List, Dict, Set, Tuple, Any
from functools import wraps
from datetime import datetime, timedelta
from collections import defaultdict, deque
from threading import Lock, Timer, Thread

# ══════════════════════════════════════════════════════════════════════════════
# 📦 THIRD-PARTY IMPORTS
# ══════════════════════════════════════════════════════════════════════════════

try:
    import telebot
    from telebot.types import (
        InlineKeyboardMarkup, 
        InlineKeyboardButton,
        ReplyKeyboardMarkup,
        KeyboardButton,
        ReplyKeyboardRemove
    )
except ImportError:
    print("❌ pyTelegramBotAPI not found. Install with: pip install pyTelegramBotAPI")
    sys.exit(1)

# ══════════════════════════════════════════════════════════════════════════════
# 🌐 ENVIRONMENT CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

class Config:
    """Centralized configuration management with cyberpunk aesthetics"""
    
    # Bot Credentials - MUST BE SET VIA ENVIRONMENT VARIABLES
    TOKEN = os.getenv("BOT_TOKEN")
    OWNER_ID = int(os.getenv("OWNER_ID", "0"))
    LOGS_GROUP_ID = int(os.getenv("LOGS_GROUP_ID", "0"))
    
    # Force Join Settings
    FORCE_CHANNEL = os.getenv("FORCE_CHANNEL", "YourChannel")
    FORCE_GROUP = os.getenv("FORCE_GROUP", "YourGroup")
    
    # Media URLs
    START_PIC = os.getenv("START_PIC_URL", "https://i.ibb.co/9H2WWVgx/image.png")
    FORCE_PIC = os.getenv("FORCE_PIC_URL", "https://i.ibb.co/nqZ0RzBt/image.png")
    UPLOAD_PIC = os.getenv("UPLOAD_PIC_URL", "https://i.ibb.co/yc6kvqMz/image.png")
    FIRE_GIF = os.getenv("FIRE_GIF_URL", "https://i.ibb.co/9H2WWVgx/image.png")
    
    # Directory Structure
    BASE_DIR = Path(__file__).parent.absolute()
    UPLOAD_DIR = BASE_DIR / "user_bots"
    LOGS_DIR = BASE_DIR / "logs"
    VENV_DIR = BASE_DIR / "virtual_envs"
    DB_PATH = BASE_DIR / "astronix_fire_ultimate.db"
    
    # Plan Limits (py_bots, zip_bots, max_size_mb)
    PLAN_LIMITS = {
        "FREE": {
            "py": 3, 
            "zip": 1, 
            "max_size_mb": 5,
            "description": "🆓 Basic hosting for starters",
            "emoji": "🫧"
        },
        "BRONZE": {
            "py": 5, 
            "zip": 3, 
            "max_size_mb": 10,
            "description": "🥉 Enhanced capacity",
            "emoji": "⛩️"
        },
        "SILVER": {
            "py": 10, 
            "zip": 5, 
            "max_size_mb": 25,
            "description": "🥈 Professional tier",
            "emoji": "🐉"
        },
        "GOLD": {
            "py": 20, 
            "zip": 10, 
            "max_size_mb": 50,
            "description": "🥇 Advanced deployment",
            "emoji": "🧿"
        },
        "PLATINUM": {
            "py": 50, 
            "zip": 25, 
            "max_size_mb": 100,
            "description": "🏆 Enterprise grade",
            "emoji": "🌀"
        },
        "DIAMOND": {
            "py": 999999, 
            "zip": 999999, 
            "max_size_mb": 500,
            "description": "💎 Unlimited power",
            "emoji": "🔥"
        }
    }
    
    # Rate Limiting
    RATE_LIMIT_SECONDS = 2
    MAX_UPLOAD_SIZE_MB = 100
    SPAM_THRESHOLD = 5
    SPAM_WINDOW = 10
    
    # Fire Animation Frames - EPIC IGNITION SEQUENCE
    FIRE_ANIMATION_FRAMES = [
        "▒▒▒▒▒▒▒▒▒▒ 0% 🌑",
        "█▒▒▒▒▒▒▒▒▒ 10% ⚡ [Power On...]",
        "██▒▒▒▒▒▒▒▒ 20% 💠 [Initializing Core...]",
        "███▒▒▒▒▒▒▒ 30% 🔱 [Loading Modules...]",
        "████▒▒▒▒▒▒ 40% 🧬 [Igniting System...]",
        "█████▒▒▒▒▒ 50% ⛩️ [Energy Rising...]",
        "██████▒▒▒▒ 60% 🐉 [Core Heating...]",
        "███████▒▒▒ 70% 🌀 [Fusion Starting...]",
        "████████▒▒ 80% 💥 [Critical Mass...]",
        "█████████▒ 90% 🔥 [Ignition Phase...]",
        "██████████ 100% 💥🔥💥 FIRE CORE ACTIVE 💥🔥💥"
    ]
    
    @classmethod
    def validate(cls) -> bool:
        """Validate critical configuration"""
        if not cls.TOKEN:
            print("❌ BOT_TOKEN environment variable not set!")
            return False
        if cls.OWNER_ID == 0:
            print("⚠️  OWNER_ID not set. Admin features disabled.")
        if cls.LOGS_GROUP_ID == 0:
            print("⚠️  LOGS_GROUP_ID not set. Logging disabled.")
        return True
    
    @classmethod
    def setup_directories(cls):
        """Create necessary directories"""
        cls.UPLOAD_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)
        cls.VENV_DIR.mkdir(exist_ok=True)

if not Config.validate():
    sys.exit(1)
Config.setup_directories()

# ══════════════════════════════════════════════════════════════════════════════
# 💾 DATABASE MANAGEMENT SYSTEM - ENTERPRISE GRADE
# ══════════════════════════════════════════════════════════════════════════════

class DatabaseManager:
    """Thread-safe SQLite database manager"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.lock = Lock()
        self.connection = None
        self.cursor = None
        self._initialize_connection()
        self._create_tables()
        self._initialize_defaults()
    
    def _initialize_connection(self):
        self.connection = sqlite3.connect(
            str(self.db_path),
            check_same_thread=False,
            timeout=30.0
        )
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA synchronous=NORMAL")
        self.cursor = self.connection.cursor()
    
    def _create_tables(self):
        with self.lock:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    uid INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    joined_at INTEGER,
                    last_seen INTEGER,
                    total_uploads INTEGER DEFAULT 0,
                    total_starts INTEGER DEFAULT 0
                )
            """)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS plans (
                    uid INTEGER PRIMARY KEY,
                    plan TEXT DEFAULT 'FREE',
                    upgraded_at INTEGER,
                    expires_at INTEGER,
                    upgraded_by INTEGER
                )
            """)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS banned (
                    uid INTEGER PRIMARY KEY,
                    banned_at INTEGER,
                    reason TEXT,
                    banned_by INTEGER
                )
            """)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS giveaway (
                    code TEXT PRIMARY KEY,
                    plan TEXT,
                    duration_days INTEGER DEFAULT 30,
                    created_at INTEGER,
                    created_by INTEGER,
                    used_by INTEGER,
                    used_at INTEGER
                )
            """)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS bot_processes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    uid INTEGER,
                    bot_name TEXT,
                    file_type TEXT,
                    pid INTEGER,
                    venv_path TEXT,
                    started_at INTEGER,
                    stopped_at INTEGER,
                    status TEXT DEFAULT 'running'
                )
            """)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS statistics (
                    key TEXT PRIMARY KEY,
                    value INTEGER DEFAULT 0
                )
            """)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)
            
            self.connection.commit()
    
    def _initialize_defaults(self):
        with self.lock:
            self.cursor.execute("INSERT OR IGNORE INTO settings VALUES ('locked', '0')")
            self.cursor.execute("INSERT OR IGNORE INTO settings VALUES ('maintenance_message', 'Bot under maintenance')")
            
            for key in ['total_starts', 'total_uploads', 'total_bot_runs', 'total_commands', 'total_errors']:
                self.cursor.execute("INSERT OR IGNORE INTO statistics VALUES (?, 0)", (key,))
            
            self.connection.commit()
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        with self.lock:
            return self.cursor.execute(query, params)
    
    def commit(self):
        with self.lock:
            self.connection.commit()
    
    def close(self):
        with self.lock:
            if self.connection:
                self.connection.close()
    
    def add_user(self, uid: int, username: str = None, first_name: str = None):
        now = int(time.time())
        self.execute(
            """INSERT OR REPLACE INTO users 
               (uid, username, first_name, joined_at, last_seen, total_uploads, total_starts)
               VALUES (?, ?, ?, COALESCE((SELECT joined_at FROM users WHERE uid=?), ?), ?, 
                       COALESCE((SELECT total_uploads FROM users WHERE uid=?), 0),
                       COALESCE((SELECT total_starts FROM users WHERE uid=?), 0))""",
            (uid, username, first_name, uid, now, now, uid, uid)
        )
        self.commit()
    
    def update_last_seen(self, uid: int):
        self.execute("UPDATE users SET last_seen=? WHERE uid=?", (int(time.time()), uid))
        self.commit()
    
    def increment_user_stat(self, uid: int, stat: str):
        """Updates user specific statistics in the database"""
        with self.lock:
            self.execute(f"UPDATE users SET {stat} = {stat} + 1 WHERE uid=?", (uid,))
            self.commit()

    def get_user_plan(self, uid: int) -> str:
        """Retrieves and validates user subscription plan"""
        if uid == Config.OWNER_ID:
            return "DIAMOND"
        try:
            result = self.execute("SELECT plan, expires_at FROM plans WHERE uid=?", (uid,)).fetchone()
            if not result or result['plan'] is None:
                return "FREE"
            
            # Expiry check with None safety
            expires_at = result['expires_at']
            if expires_at and int(expires_at) < int(time.time()):
                self.set_user_plan(uid, "FREE")
                return "FREE"
                
            return result['plan']
        except Exception as e:
            print(f"⚠️ Plan Retrieval Error: {e}")
            return "FREE"

    
    def set_user_plan(self, uid: int, plan: str, duration_days: int = None, upgraded_by: int = None):
        now = int(time.time())
        expires_at = None
        if duration_days and plan != "FREE":
            expires_at = now + (duration_days * 86400)
        self.execute(
            "INSERT OR REPLACE INTO plans VALUES (?, ?, ?, ?, ?)",
            (uid, plan, now, expires_at, upgraded_by)
        )
        self.commit()
    
    def get_plan_expiry(self, uid: int) -> Optional[int]:
        result = self.execute("SELECT expires_at FROM plans WHERE uid=?", (uid,)).fetchone()
        return result['expires_at'] if result else None
    
    def is_banned(self, uid: int) -> bool:
        result = self.execute("SELECT 1 FROM banned WHERE uid=?", (uid,)).fetchone()
        return result is not None
    
    def ban_user(self, uid: int, reason: str = "No reason", banned_by: int = None):
        self.execute("INSERT OR REPLACE INTO banned VALUES (?, ?, ?, ?)",
                    (uid, int(time.time()), reason, banned_by))
        self.commit()
    
    def unban_user(self, uid: int):
        self.execute("DELETE FROM banned WHERE uid=?", (uid,))
        self.commit()
    
    def get_ban_info(self, uid: int) -> Optional[Dict]:
        result = self.execute("SELECT * FROM banned WHERE uid=?", (uid,)).fetchone()
        return dict(result) if result else None
    
    def get_setting(self, key: str) -> Optional[str]:
        result = self.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        return result['value'] if result else None
    
    def set_setting(self, key: str, value: str):
        self.execute("INSERT OR REPLACE INTO settings VALUES (?, ?)", (key, value))
        self.commit()
    
    def increment_stat(self, key: str, amount: int = 1):
        self.execute("UPDATE statistics SET value = value + ? WHERE key = ?", (amount, key))
        self.commit()
    
    def get_stat(self, key: str) -> int:
        result = self.execute("SELECT value FROM statistics WHERE key=?", (key,)).fetchone()
        return result['value'] if result else 0
    
    def get_total_users(self) -> int:
        result = self.execute("SELECT COUNT(*) as count FROM users").fetchone()
        return result['count']
    
    def get_premium_users(self) -> int:
        result = self.execute("SELECT COUNT(*) as count FROM plans WHERE plan != 'FREE'").fetchone()
        return result['count']
    
    def get_banned_count(self) -> int:
        result = self.execute("SELECT COUNT(*) as count FROM banned").fetchone()
        return result['count']
    
    def create_giveaway_code(self, code: str, plan: str, duration_days: int, created_by: int):
        self.execute(
            "INSERT INTO giveaway (code, plan, duration_days, created_at, created_by) VALUES (?, ?, ?, ?, ?)",
            (code, plan, duration_days, int(time.time()), created_by)
        )
        self.commit()
    
    def redeem_code(self, code: str, uid: int) -> Tuple[bool, str, str]:
        result = self.execute(
            "SELECT plan, duration_days, used_by FROM giveaway WHERE code=?", (code,)
        ).fetchone()
        
        if not result:
            return False, "", "❌ Invalid code"
        if result['used_by']:
            return False, "", "❌ Code already used"
        
        plan = result['plan']
        duration = result['duration_days']
        
        self.execute("UPDATE giveaway SET used_by=?, used_at=? WHERE code=?",
                    (uid, int(time.time()), code))
        self.set_user_plan(uid, plan, duration)
        self.commit()
        return True, plan, f"✅ Upgraded to {plan} for {duration} days!"
    
    def add_bot_process(self, uid: int, bot_name: str, file_type: str, pid: int, venv_path: str):
        self.execute(
            """INSERT INTO bot_processes (uid, bot_name, file_type, pid, venv_path, started_at, status)
               VALUES (?, ?, ?, ?, ?, ?, 'running')""",
            (uid, bot_name, file_type, pid, venv_path, int(time.time()))
        )
        self.commit()
    
    def stop_bot_process(self, uid: int, bot_name: str):
        self.execute(
            "UPDATE bot_processes SET stopped_at=?, status='stopped' WHERE uid=? AND bot_name=? AND status='running'",
            (int(time.time()), uid, bot_name)
        )
        self.commit()
    
    def get_user_bot_count(self, uid: int, file_type: str = None) -> int:
        if file_type:
            result = self.execute(
                "SELECT COUNT(*) as count FROM bot_processes WHERE uid=? AND file_type=? AND status='running'",
                (uid, file_type)
            ).fetchone()
        else:
            result = self.execute(
                "SELECT COUNT(*) as count FROM bot_processes WHERE uid=? AND status='running'",
                (uid,)
            ).fetchone()
        return result['count']

db = DatabaseManager(Config.DB_PATH)

# ══════════════════════════════════════════════════════════════════════════════
# 🔍 SMART ENTRY POINT DETECTOR - KASUKABE INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════

class SmartEntryDetector:
    """Intelligent entry point detection for bot files"""
    
    PRIORITY_NAMES = ['bot.py', 'main.py', 'run.py', 'start.py', 'app.py', '__main__.py']
    BOT_KEYWORDS = [
        'telebot', 'polling', 'Client', 'Bot', 'updater', 'run_forever', 
        'infinity_polling', 'bot.run', 'application.run', 'TeleBot',
        'run_polling', 'start_polling', 'idle', 'bot.polling'
    ]
    
    @classmethod
    def detect_main_file(cls, directory: Path) -> Optional[Path]:
        """
        Smart detection of the main entry point file
        Priority:
        1. Standard names (bot.py, main.py, etc.)
        2. Files containing bot-related keywords
        3. Largest .py file in directory
        """
        if not directory.exists():
            return None
        
        print(f"🔍 Scanning directory: {directory}")
        
        # STEP 1: Check for priority names
        for name in cls.PRIORITY_NAMES:
            candidate = directory / name
            if candidate.exists() and candidate.is_file():
                print(f"✅ Found priority file: {name}")
                return candidate
        
        # STEP 2: Scan all Python files
        py_files = list(directory.rglob('*.py'))
        if not py_files:
            print("❌ No Python files found")
            return None
        
        # Filter out common non-entry files
        py_files = [f for f in py_files if '__pycache__' not in str(f) 
                    and not f.name.startswith('_') 
                    and f.name not in ['setup.py', 'config.py', 'settings.py', 'test.py']]
        
        if not py_files:
            print("❌ No valid Python files after filtering")
            return None
        
        print(f"📁 Found {len(py_files)} Python files")
        
        # STEP 3: Check for keyword matches
        keyword_matches = []
        for py_file in py_files:
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    keyword_count = sum(1 for keyword in cls.BOT_KEYWORDS if keyword in content)
                    if keyword_count > 0:
                        keyword_matches.append((py_file, keyword_count))
                        print(f"🔎 {py_file.name}: {keyword_count} keywords")
            except Exception as e:
                print(f"⚠️ Error reading {py_file.name}: {e}")
                continue
        
        # Return file with most keyword matches
        if keyword_matches:
            keyword_matches.sort(key=lambda x: x[1], reverse=True)
            best_match = keyword_matches[0][0]
            print(f"✅ Best keyword match: {best_match.name}")
            return best_match
        
        # STEP 4: Return largest .py file as fallback
        py_files.sort(key=lambda f: f.stat().st_size, reverse=True)
        largest = py_files[0]
        print(f"📦 Using largest file: {largest.name} ({largest.stat().st_size} bytes)")
        return largest
    
    @classmethod
    def get_nested_code_directory(cls, extract_dir: Path) -> Path:
        """
        Handle nested ZIP structures - find the actual code directory
        """
        print(f"🔍 Checking for nested structure in: {extract_dir}")
        
        # Check if there's a single subdirectory containing all the code
        subdirs = [d for d in extract_dir.iterdir() if d.is_dir() and d.name not in ['__MACOSX', '__pycache__', '.venv']]
        
        if len(subdirs) == 1:
            # Check if this single subdirectory contains Python files
            nested_py_files = list(subdirs[0].rglob('*.py'))
            root_py_files = [f for f in extract_dir.glob('*.py')]
            
            # If nested directory has Python files but root doesn't, use nested
            if nested_py_files and not root_py_files:
                print(f"📂 Using nested directory: {subdirs[0].name}")
                return subdirs[0]
        
        print(f"📂 Using root directory: {extract_dir.name}")
        return extract_dir

# ══════════════════════════════════════════════════════════════════════════════
# 🔥 PROCESS MANAGEMENT SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

class ProcessManager:
    """Advanced process management with health monitoring"""
    
    def __init__(self):
        self.processes: Dict[str, subprocess.Popen] = {}
        self.lock = Lock()
        self.log_files: Dict[str, Any] = {}
        self.monitoring = False
        self._start_health_monitor()
    
    def get_key(self, uid: int, bot_name: str) -> str:
        return f"{uid}:{bot_name}"
    
    def is_running(self, uid: int, bot_name: str) -> bool:
        key = self.get_key(uid, bot_name)
        with self.lock:
            if key in self.processes:
                proc = self.processes[key]
                if proc.poll() is None:
                    return True
                else:
                    self._cleanup_process(key)
                    db.stop_bot_process(uid, bot_name)
                    return False
        return False
    
    def get_process_info(self, uid: int, bot_name: str) -> Optional[Dict]:
        key = self.get_key(uid, bot_name)
        with self.lock:
            if key not in self.processes:
                return None
            proc = self.processes[key]
            if proc.poll() is not None:
                return None
            try:
                ps_proc = psutil.Process(proc.pid)
                return {
                    'pid': proc.pid,
                    'status': ps_proc.status(),
                    'cpu_percent': ps_proc.cpu_percent(interval=0.1),
                    'memory_mb': ps_proc.memory_info().rss / 1024 / 1024,
                    'create_time': ps_proc.create_time(),
                    'num_threads': ps_proc.num_threads()
                }
            except:
                return None
    
    def add_process(self, uid: int, bot_name: str, process: subprocess.Popen, log_file, venv_path: str):
        key = self.get_key(uid, bot_name)
        with self.lock:
            self.processes[key] = process
            self.log_files[key] = log_file
        db.add_bot_process(uid, bot_name, 'zip' if bot_name.endswith('.zip') else 'py', process.pid, venv_path)
    
    def _cleanup_process(self, key: str):
        if key in self.processes:
            del self.processes[key]
        if key in self.log_files:
            try:
                self.log_files[key].close()
            except:
                pass
            del self.log_files[key]
    
    def stop_process(self, uid: int, bot_name: str, force: bool = False) -> bool:
        key = self.get_key(uid, bot_name)
        with self.lock:
            if key not in self.processes:
                return False
            proc = self.processes[key]
            try:
                try:
                    parent = psutil.Process(proc.pid)
                    children = parent.children(recursive=True)
                except:
                    children = []
                
                for child in children:
                    try:
                        child.terminate()
                    except:
                        pass
                
                if force:
                    proc.kill()
                else:
                    proc.terminate()
                
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
                
                for child in children:
                    try:
                        child.kill()
                    except:
                        pass
                
                db.stop_bot_process(uid, bot_name)
                db.increment_stat('total_stops')
                self._cleanup_process(key)
                return True
            except Exception as e:
                print(f"Stop error: {e}")
                self._cleanup_process(key)
                return False
    
    def get_running_count(self, uid: int, file_type: str = None) -> int:
        count = 0
        with self.lock:
            for key in list(self.processes.keys()):
                if key.startswith(f"{uid}:"):
                    proc = self.processes[key]
                    if proc.poll() is None:
                        if file_type:
                            _, name = key.split(":", 1)
                            if name.endswith(f".{file_type}"):
                                count += 1
                        else:
                            count += 1
                    else:
                        uid_str, bot_name = key.split(":", 1)
                        self._cleanup_process(key)
                        db.stop_bot_process(int(uid_str), bot_name)
        return count
    
    def get_user_bots(self, uid: int) -> List[str]:
        bots = []
        with self.lock:
            for key in list(self.processes.keys()):
                if key.startswith(f"{uid}:"):
                    proc = self.processes[key]
                    if proc.poll() is None:
                        _, bot_name = key.split(":", 1)
                        bots.append(bot_name)
        return bots
    
    def stop_all_user_bots(self, uid: int) -> int:
        bots = self.get_user_bots(uid)
        count = 0
        for bot_name in bots:
            if self.stop_process(uid, bot_name):
                count += 1
        return count
    
    def get_all_processes_info(self) -> List[Dict]:
        info_list = []
        with self.lock:
            for key in list(self.processes.keys()):
                uid_str, bot_name = key.split(":", 1)
                uid = int(uid_str)
                proc_info = self.get_process_info(uid, bot_name)
                if proc_info:
                    proc_info['uid'] = uid
                    proc_info['bot_name'] = bot_name
                    info_list.append(proc_info)
        return info_list
    
    def _health_monitor(self):
        while self.monitoring:
            try:
                with self.lock:
                    dead_processes = []
                    for key in list(self.processes.keys()):
                        proc = self.processes[key]
                        if proc.poll() is not None:
                            dead_processes.append(key)
                    
                    for key in dead_processes:
                        uid_str, bot_name = key.split(":", 1)
                        self._cleanup_process(key)
                        db.stop_bot_process(int(uid_str), bot_name)
                time.sleep(30)
            except Exception as e:
                print(f"Health monitor error: {e}")
                time.sleep(60)
    
    def _start_health_monitor(self):
        self.monitoring = True
        Thread(target=self._health_monitor, daemon=True).start()
    
    def cleanup_all(self):
        self.monitoring = False
        with self.lock:
            for key in list(self.processes.keys()):
                try:
                    proc = self.processes[key]
                    try:
                        parent = psutil.Process(proc.pid)
                        children = parent.children(recursive=True)
                        for child in children:
                            try:
                                child.terminate()
                            except:
                                pass
                        proc.terminate()
                        try:
                            proc.wait(timeout=3)
                        except subprocess.TimeoutExpired:
                            proc.kill()
                            for child in children:
                                try:
                                    child.kill()
                                except:
                                    pass
                    except:
                        proc.kill()
                except:
                    pass
            
            for log_file in self.log_files.values():
                try:
                    log_file.close()
                except:
                    pass
            
            self.processes.clear()
            self.log_files.clear()

process_manager = ProcessManager()

# ══════════════════════════════════════════════════════════════════════════════
# 🧠 SMART DEPENDENCY INSTALLER - RESILIENT MODE
# ══════════════════════════════════════════════════════════════════════════════

class SmartDependencyInstaller:
    """Enterprise-grade dependency detection with Resilient Installation"""
    
    # Safely get stdlib names or an empty list if not found
    _raw_stdlib = getattr(sys, 'stdlib_module_names', [])
    STDLIB_MODULES = set(_raw_stdlib) if _raw_stdlib is not None else set()
    
    BUILTIN_MODULES = set(sys.builtin_module_names) if sys.builtin_module_names is not None else set()
    
    ADDITIONAL_STDLIB = {
        'abc', 'argparse', 'ast', 'asyncio', 'base64', 'binascii', 'bisect', 'builtins',
        'bz2', 'calendar', 'cmath', 'codecs', 'collections', 'configparser', 'contextlib',
        'copy', 'csv', 'ctypes', 'datetime', 'dbm', 'decimal', 'difflib', 'dis', 'doctest',
        'email', 'enum', 'errno', 'faulthandler', 'fcntl', 'fractions', 'ftplib', 'functools',
        'gc', 'getopt', 'getpass', 'gettext', 'glob', 'gzip', 'hashlib', 'heapq', 'html',
        'http', 'imaplib', 'importlib', 'inspect', 'io', 'itertools', 'json', 'keyword',
        'lib2to3', 'linecache', 'logging', 'lzma', 'mailbox', 'marshal', 'math', 'mimetypes',
        'mmap', 'modulefinder', 'multiprocessing', 'netrc', 'nntplib', 'ntpath', 'numbers',
        'operator', 'os', 'pathlib', 'pdb', 'pickle', 'pickletools', 'pkgutil', 'platform',
        'plistlib', 'poplib', 'posixpath', 'pprint', 'profile', 'pstats', 'pty', 'pwd',
        'py_compile', 'pyclbr', 'pydoc', 'queue', 'quopri', 'random', 're', 'readline',
        'reprlib', 'resource', 'rlcompleter', 'runpy', 'sched', 'select', 'selectors',
        'shelve', 'shlex', 'shutil', 'signal', 'site', 'smtpd', 'smtplib', 'sndhdr',
        'socket', 'socketserver', 'sqlite3', 'ssl', 'stat', 'statistics', 'string',
        'stringprep', 'struct', 'subprocess', 'sunau', 'symbol', 'symtable', 'sys',
        'sysconfig', 'syslog', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile', 'termios',
        'textwrap', 'threading', 'time', 'timeit', 'token', 'tokenize', 'trace',
        'traceback', 'tracemalloc', 'tty', 'types', 'typing', 'unicodedata', 'unittest',
        'urllib', 'uu', 'uuid', 'venv', 'warnings', 'wave', 'weakref', 'webbrowser',
        'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'zipapp', 'zipfile', 'zipimport', 'zlib'
    }

    PACKAGE_ALIASES = {
        'PIL': 'Pillow',
        'cv2': 'opencv-python',
        'telegram': 'python-telegram-bot',
        'telebot': 'pyTelegramBotAPI',
        'bs4': 'beautifulsoup4',
        'dotenv': 'python-dotenv',
        'Crypto': 'pycryptodome',
        'yaml': 'PyYAML',
        'dateutil': 'python-dateutil',
        'google.generativeai': 'google-generativeai',
        'openai': 'openai',
        'numpy': 'numpy',
        'pandas': 'pandas'
    }
    
    ESSENTIAL_PACKAGES = [
        'pyTelegramBotAPI>=4.20.0',
        'requests>=2.31.0',
        'aiohttp>=3.9.0',
        'python-dotenv>=1.0.0',
        'psutil>=5.9.0',
        'setuptools'
    ]

    @classmethod
    def is_stdlib(cls, module_name: str) -> bool:
        """Determines if a module is built-in or from standard library"""
        if not module_name: 
            return False
        name = module_name.split('.')[0]
        if name in cls.STDLIB_MODULES or name in cls.BUILTIN_MODULES or name in cls.ADDITIONAL_STDLIB:
            return True
        return False
    
    @classmethod
    def parse_requirements_file(cls, requirements_path: Path) -> List[str]:
        if not requirements_path.exists():
            return []
        packages = []
        try:
            with open(requirements_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#') or line.startswith('-e'):
                        continue
                    if 'git+' in line or 'http://' in line or 'https://' in line:
                        continue
                    pkg = re.split(r'[=<>!]', line)[0].strip()
                    if pkg and not cls.is_stdlib(pkg):
                        packages.append(line)
        except:
            pass
        return packages
    
    @classmethod
    def detect_imports_in_file(cls, file_path: Path) -> Set[str]:
        imports = set()
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                source = f.read()
            tree = ast.parse(source.replace('\r\n', '\n'), filename=str(file_path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module = alias.name.split('.')[0]
                        if not cls.is_stdlib(module):
                            imports.add(module)
                elif isinstance(node, ast.ImportFrom):
                    if node.level == 0 and node.module:
                        module = node.module.split('.')[0]
                        if not cls.is_stdlib(module):
                            imports.add(module)
        except:
            pass
        return imports
    
    @classmethod
    def detect_imports_in_directory(cls, directory: Path) -> Set[str]:
        all_imports = set()
        for py_file in directory.rglob('*.py'):
            if '__pycache__' in str(py_file) or '.venv' in str(py_file):
                continue
            imports = cls.detect_imports_in_file(py_file)
            all_imports.update(imports)
        return all_imports
    
    @classmethod
    def resolve_package_names(cls, imports: Set[str]) -> List[str]:
        packages = []
        for imp in imports:
            package = cls.PACKAGE_ALIASES.get(imp, imp)
            packages.append(package)
        return packages
    
    @classmethod
    def install_dependencies_resilient(cls, venv_python: Path, bot_dir: Path) -> Tuple[bool, str, List[str], List[str]]:
        """
        RESILIENT DEPENDENCY INSTALLATION
        - If one package fails, continue with others
        - Return both successful and failed packages
        """
        requirements_file = bot_dir / 'requirements.txt'
        
        # Upgrade pip first
        try:
            subprocess.run(
                [str(venv_python), '-m', 'pip', 'install', '--upgrade', 'pip', 'setuptools', 'wheel'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=120
            )
        except Exception as e:
            print(f"⚠️ Pip upgrade warning: {e}")
        
        packages_to_install = []
        
        # Collect packages from requirements.txt or detect them
        if requirements_file.exists():
            packages_to_install.extend(cls.parse_requirements_file(requirements_file))
        else:
            detected_imports = cls.detect_imports_in_directory(bot_dir)
            packages_to_install.extend(cls.resolve_package_names(detected_imports))
        
        # Add essential packages
        packages_to_install.extend(cls.ESSENTIAL_PACKAGES)
        
        # Remove duplicates
        unique_packages = []
        seen = set()
        for pkg in packages_to_install:
            base = re.split(r'[=<>!]', pkg)[0].lower().strip()
            if base not in seen and not cls.is_stdlib(base):
                seen.add(base)
                unique_packages.append(pkg)
        
        if not unique_packages:
            return True, "No dependencies needed", [], []
        
        print(f"📦 Installing {len(unique_packages)} packages...")
        
        # RESILIENT INSTALLATION - DON'T STOP ON FAILURE
        failed_packages = []
        installed_packages = []
        
        for package in unique_packages:
            try:
                print(f"  Installing: {package}")
                result = subprocess.run(
                    [str(venv_python), '-m', 'pip', 'install', '--no-cache-dir', '--quiet', package],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=300,
                    text=True
                )
                
                if result.returncode == 0:
                    installed_packages.append(package)
                    print(f"  ✅ {package}")
                else:
                    # Try without version specifier
                    base_pkg = re.split(r'[=<>!]', package)[0].strip()
                    if base_pkg != package:
                        print(f"  Retrying {base_pkg} without version...")
                        result2 = subprocess.run(
                            [str(venv_python), '-m', 'pip', 'install', '--no-cache-dir', '--quiet', base_pkg],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            timeout=300,
                            text=True
                        )
                        if result2.returncode == 0:
                            installed_packages.append(base_pkg)
                            print(f"  ✅ {base_pkg} (fallback)")
                        else:
                            failed_packages.append(package)
                            print(f"  ❌ {package}")
                    else:
                        failed_packages.append(package)
                        print(f"  ❌ {package}")
                        
            except Exception as e:
                failed_packages.append(package)
                print(f"  ❌ {package}: {str(e)[:50]}")
        
        # RESILIENT: Even if all fail, return success so bot can try to run
        msg = f"✅ Installed {len(installed_packages)}/{len(unique_packages)} packages"
        if failed_packages:
            msg += f" (⚠️ {len(failed_packages)} failed, will try anyway)"
        
        return True, msg, installed_packages, failed_packages

# ══════════════════════════════════════════════════════════════════════════════
# 🏗️ VIRTUAL ENVIRONMENT MANAGER - ENHANCED
# ══════════════════════════════════════════════════════════════════════════════

class VirtualEnvironmentManager:
    """Manage virtual environments for bot isolation with resilient setup"""
    
    @staticmethod
    def get_venv_path(bot_dir: Path) -> Path:
        return bot_dir / '.venv'
    
    @staticmethod
    def get_venv_python(venv_dir: Path) -> Path:
        if sys.platform == 'win32':
            return venv_dir / 'Scripts' / 'python.exe'
        else:
            return venv_dir / 'bin' / 'python'
    
    @classmethod
    def create_venv(cls, bot_dir: Path) -> Tuple[bool, Optional[Path], str]:
        """Create virtual environment"""
        venv_dir = cls.get_venv_path(bot_dir)
        
        # Remove old venv if exists
        if venv_dir.exists():
            try:
                shutil.rmtree(venv_dir)
            except Exception as e:
                print(f"⚠️ Old venv cleanup warning: {e}")
        
        try:
            print(f"🔧 Creating venv at: {venv_dir}")
            subprocess.run(
                [sys.executable, '-m', 'venv', str(venv_dir), '--clear'],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=120
            )
        except Exception as e:
            return False, None, f"Venv creation failed: {str(e)[:100]}"
        
        venv_python = cls.get_venv_python(venv_dir)
        if not venv_python.exists():
            return False, None, "Venv created but Python not found"
        
        print(f"✅ Venv Python: {venv_python}")
        return True, venv_python, "✅ Virtual environment created"
    
    @classmethod
    def setup_bot_environment(cls, bot_dir: Path) -> Tuple[bool, Optional[Path], str, List[str], List[str]]:
        """
        Setup bot environment with RESILIENT dependency installation
        Returns: (success, venv_python, message, installed_packages, failed_packages)
        """
        success, venv_python, msg = cls.create_venv(bot_dir)
        if not success:
            return False, None, msg, [], []
        
        # RESILIENT INSTALLATION
        success, dep_msg, installed, failed = SmartDependencyInstaller.install_dependencies_resilient(
            venv_python, bot_dir
        )
        
        return True, venv_python, f"{msg}\n{dep_msg}", installed, failed

# ══════════════════════════════════════════════════════════════════════════════
# 🎨 UI COMPONENTS - CYBERPUNK KEYBOARDS
# ══════════════════════════════════════════════════════════════════════════════

class UIComponents:
    """UI component generators with cyberpunk theme"""
    
    @staticmethod
    def main_keyboard() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.row(
            KeyboardButton("⚡ ꜱᴛᴀʀᴛ ʙᴏᴛ"),
            KeyboardButton("🗑 ᴅᴇʟᴇᴛᴇ ʙᴏᴛ")
        )
        keyboard.row(
            KeyboardButton("🥏 ᴍʏ ʙᴏᴛꜱ"),
            KeyboardButton("🥂 ꜱʏꜱᴛᴇᴍ ꜱᴛᴀᴛꜱ")
        )
        keyboard.row(
            KeyboardButton("👒 ᴠɪᴘ ᴘʟᴀɴꜱ"),
            KeyboardButton("🎐 ᴜᴘʟᴏᴀᴅ ʙᴏᴛ")
        )
        keyboard.row(
            KeyboardButton("🍹 ʜᴇʟᴘ"),
            KeyboardButton("🆘 ꜱᴜᴘᴘᴏʀᴛ")
        )
        return keyboard
    
    @staticmethod
    def admin_keyboard() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.row(
            KeyboardButton("📢 ʙʀᴏᴀᴅᴄᴀꜱᴛ"),
            KeyboardButton("👥 ᴜꜱᴇʀꜱ ɪɴғᴏ")
        )
        keyboard.row(
            KeyboardButton("⛔ ʙᴀɴ ᴜꜱᴇʀ"),
            KeyboardButton("🔓 ᴜɴʙᴀɴ ᴜꜱᴇʀ")
        )
        keyboard.row(
            KeyboardButton("💎 ᴀᴅᴅ ᴘʀᴇᴍɪᴜᴍ"),
            KeyboardButton("🎁 ɢᴇɴ ᴄᴏᴅᴇ")
        )
        keyboard.row(
            KeyboardButton("🔒 ʟᴏᴄᴋ ʙᴏᴛ"),
            KeyboardButton("🔓 ᴜɴʟᴏᴄᴋ ʙᴏᴛ")
        )
        keyboard.row(
            KeyboardButton("🖥 ᴍᴀꜱᴛᴇʀ ᴅᴀꜱʜʙᴏᴀʀᴅ"),
            KeyboardButton("🏠 ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ")
        )
        return keyboard
    
    @staticmethod
    def force_join_keyboard() -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            InlineKeyboardButton("📢 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{Config.FORCE_CHANNEL}"),
            InlineKeyboardButton("👥 ᴊᴏɪɴ ɢʀᴏᴜᴘ", url=f"https://t.me/{Config.FORCE_GROUP}"),
            InlineKeyboardButton("🔄 ᴄʜᴇᴄᴋ ᴀɢᴀɪɴ", callback_data="check_membership")
        )
        return keyboard
    
    @staticmethod
    def plan_carousel_keyboard(current_index: int = 0) -> InlineKeyboardMarkup:
        """CAROUSEL - ONE PLAN AT A TIME"""
        plans = list(Config.PLAN_LIMITS.keys())
        keyboard = InlineKeyboardMarkup(row_width=2)
        
        prev_index = (current_index - 1) % len(plans)
        next_index = (current_index + 1) % len(plans)
        
        keyboard.row(
            InlineKeyboardButton("◀️ ᴘʀᴇᴠɪᴏᴜꜱ", callback_data=f"plan_nav:{prev_index}"),
            InlineKeyboardButton("ɴᴇxᴛ ▶️", callback_data=f"plan_nav:{next_index}")
        )
        keyboard.row(
            InlineKeyboardButton(f"━━━ {current_index + 1}/{len(plans)} ━━━", callback_data="plan_info")
        )
        keyboard.row(
            InlineKeyboardButton(f"💰 ɢᴇᴛ {plans[current_index]}", url=f"https://t.me/{Config.FORCE_GROUP}")
        )
        keyboard.row(
            InlineKeyboardButton("✖️ ᴄʟᴏꜱᴇ", callback_data="close_msg")
        )
        return keyboard
    
    @staticmethod
    def bot_control_keyboard(uid: int, bot_name: str, is_running: bool = False) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=2)
        if is_running:
            keyboard.row(
                InlineKeyboardButton("⏸ ꜱᴛᴏᴘ", callback_data=f"stop:{uid}:{bot_name}"),
                InlineKeyboardButton("📊 ꜱᴛᴀᴛꜱ", callback_data=f"stats:{uid}:{bot_name}")
            )
        else:
            keyboard.row(
                InlineKeyboardButton("▶️ ʀᴜɴ", callback_data=f"run:{uid}:{bot_name}")
            )
        keyboard.row(
            InlineKeyboardButton("🔮 ʟᴏɢꜱ", callback_data=f"logs:{uid}:{bot_name}"),
            InlineKeyboardButton("🗑 ᴅᴇʟᴇᴛᴇ", callback_data=f"delete:{uid}:{bot_name}")
        )
        return keyboard
    
    @staticmethod
    def get_plan_description(plan_name: str) -> str:
        plan_data = Config.PLAN_LIMITS.get(plan_name, {})
        py_limit = plan_data.get('py', 0)
        zip_limit = plan_data.get('zip', 0)
        size_limit = plan_data.get('max_size_mb', 0)
        description = plan_data.get('description', '')
        emoji = plan_data.get('emoji', '⚜️')
        
        py_str = f"{py_limit}" if py_limit < 999999 else "∞"
        zip_str = f"{zip_limit}" if zip_limit < 999999 else "∞"
        
        return f"""
{emoji} <b>{plan_name} PLAN</b> {emoji}

╔═══════════════════════════════╗
║  🔥 <b>CYBERPUNK HOSTING TIER</b>
╠═══════════════════════════════╣
║ {description}
╠═══════════════════════════════╣
║  🐉 <b>SPECIFICATIONS:</b>
║  
║  📄 Python Files: <code>{py_str}</code>
║  📦 ZIP Projects: <code>{zip_str}</code>
║  💾 Max File Size: <code>{size_limit}MB</code>
║  ⚡ Priority: {'✅' if plan_name != 'FREE' else '❌'}
║  🔥 Fast Deploy: {'✅' if plan_name != 'FREE' else '❌'}
╚═══════════════════════════════╝

🌀 <i>Next-gen bot hosting power</i>
"""
    
    @staticmethod
    def confirm_delete_keyboard(uid: int, bot_name: str) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(
            InlineKeyboardButton("✅ ʏᴇꜱ, ᴅᴇʟᴇᴛᴇ", callback_data=f"confirm_delete:{uid}:{bot_name}"),
            InlineKeyboardButton("❌ ᴄᴀɴᴄᴇʟ", callback_data="close_msg")
        )
        return keyboard

# ══════════════════════════════════════════════════════════════════════════════
# 🎬 ANIMATION SYSTEM - EPIC FIRE EXPLOSION
# ══════════════════════════════════════════════════════════════════════════════

class AnimationSystem:
    """Handle animated messages"""
    
    @staticmethod
    def fire_explosion_animation(bot, chat_id: int) -> Optional[int]:
        """EPIC FIRE EXPLOSION ANIMATION"""
        try:
            msg = bot.send_message(chat_id, Config.FIRE_ANIMATION_FRAMES[0])
            for i, frame in enumerate(Config.FIRE_ANIMATION_FRAMES[1:], 1):
                delay = 0.3 if i < 5 else 0.4 if i < 8 else 0.6
                time.sleep(delay)
                try:
                    bot.edit_message_text(frame, chat_id, msg.message_id)
                except:
                    pass
            time.sleep(0.8)
            return msg.message_id
        except:
            return None
    
    @staticmethod
    def progress_animation(bot, chat_id: int, message_id: int, progress: int, text: str):
        bars = int(progress / 10)
        bar_str = "▰" * bars + "▱" * (10 - bars)
        try:
            bot.edit_message_text(f"{text}\n{bar_str} {progress}%", chat_id, message_id)
        except:
            pass

# ══════════════════════════════════════════════════════════════════════════════
# 🛡️ ACCESS CONTROL & ANTI-SPAM
# ══════════════════════════════════════════════════════════════════════════════

class AccessControl:
    """Advanced access control with anti-spam"""
    
    last_command_time: Dict[int, float] = {}
    command_history: Dict[int, deque] = defaultdict(lambda: deque(maxlen=Config.SPAM_THRESHOLD))
    lock = Lock()
    
    @classmethod
    def check_rate_limit(cls, uid: int) -> bool:
        with cls.lock:
            now = time.time()
            last_time = cls.last_command_time.get(uid, 0)
            if now - last_time < Config.RATE_LIMIT_SECONDS:
                return False
            cls.last_command_time[uid] = now
            return True
    
    @classmethod
    def check_spam(cls, uid: int) -> bool:
        with cls.lock:
            now = time.time()
            user_history = cls.command_history[uid]
            user_history.append(now)
            if len(user_history) >= Config.SPAM_THRESHOLD:
                oldest = user_history[0]
                if now - oldest < Config.SPAM_WINDOW:
                    return True
            return False
    
    @classmethod
    def is_member(cls, bot, uid: int) -> bool:
        if uid == Config.OWNER_ID:
            return True
        try:
            ch_member = bot.get_chat_member(f"@{Config.FORCE_CHANNEL}", uid)
            gp_member = bot.get_chat_member(f"@{Config.FORCE_GROUP}", uid)
            return ch_member.status in ['member', 'administrator', 'creator'] and \
                   gp_member.status in ['member', 'administrator', 'creator']
        except:
            return True

def requires_access(func):
    @wraps(func)
    def wrapper(message):
        uid = message.from_user.id
        chat_id = message.chat.id
        
        db.update_last_seen(uid)
        
        if db.is_banned(uid):
            ban_info = db.get_ban_info(uid)
            bot.send_message(chat_id, f"🚫 <b>Banned</b>\n\nReason: {ban_info['reason'] if ban_info else 'Unknown'}")
            return
        
        if db.get_setting('locked') == '1' and uid != Config.OWNER_ID:
            bot.send_message(chat_id, f"🔒 <b>Maintenance Mode</b>\n\n{db.get_setting('maintenance_message')}")
            return
        
        if not AccessControl.is_member(bot, uid):
            try:
                bot.send_photo(
                    chat_id,
                    photo=Config.FORCE_PIC,
                    caption="🔐 <b>Access Restricted</b>\n\nJoin our channel and group to unlock all features.",
                    reply_markup=UIComponents.force_join_keyboard()
                )
            except:
                bot.send_message(chat_id, "🔐 Join our channel and group to use this bot.", 
                               reply_markup=UIComponents.force_join_keyboard())
            return
        
        if AccessControl.check_spam(uid):
            bot.send_message(chat_id, "🚨 <b>Slow Down!</b>\n\nToo many commands.")
            return
        
        if not AccessControl.check_rate_limit(uid):
            bot.send_message(chat_id, f"⏱ Wait {Config.RATE_LIMIT_SECONDS}s between commands.")
            return
        
        db.increment_stat('total_commands')
        return func(message)
    return wrapper

def owner_only(func):
    @wraps(func)
    def wrapper(message):
        if message.from_user.id != Config.OWNER_ID:
            bot.send_message(message.chat.id, "⛔ <b>Owner Only</b>")
            return
        return func(message)
    return wrapper

# ══════════════════════════════════════════════════════════════════════════════
# 🤖 BOT INITIALIZATION
# ══════════════════════════════════════════════════════════════════════════════

bot = telebot.TeleBot(Config.TOKEN, parse_mode='HTML', threaded=True, num_threads=8)

# ══════════════════════════════════════════════════════════════════════════════
# 📝 LOGGING UTILITIES
# ══════════════════════════════════════════════════════════════════════════════

class Logger:
    @staticmethod
    def log_to_group(text: str):
        if Config.LOGS_GROUP_ID == 0:
            return
        try:
            bot.send_message(Config.LOGS_GROUP_ID, text, parse_mode='HTML', disable_notification=True)
        except:
            pass
    
    @staticmethod
    def get_system_stats() -> Dict:
        try:
            cpu = psutil.cpu_percent(interval=0.5)
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            return {
                'cpu_percent': cpu,
                'ram_percent': ram.percent,
                'ram_used_gb': ram.used / (1024**3),
                'ram_total_gb': ram.total / (1024**3),
                'disk_percent': disk.percent,
                'disk_used_gb': disk.used / (1024**3),
                'disk_total_gb': disk.total / (1024**3)
            }
        except:
            return {}
    
    @staticmethod
    def read_last_log_lines(log_file_path: Path, n_lines: int = 15) -> str:
        """Read last N lines from log file for crash reports"""
        try:
            if not log_file_path.exists() or log_file_path.stat().st_size == 0:
                return "No log content available"
            
            with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                last_lines = lines[-n_lines:] if len(lines) > n_lines else lines
                return ''.join(last_lines)
        except Exception as e:
            return f"Error reading logs: {str(e)}"

# ══════════════════════════════════════════════════════════════════════════════
# 🎯 COMMAND HANDLERS - START & HELP
# ══════════════════════════════════════════════════════════════════════════════

@bot.message_handler(commands=['start'])
@requires_access
def cmd_start(message):
    """Handle /start with EPIC FIRE ANIMATION"""
    uid = message.from_user.id
    username = message.from_user.username or "User"
    first_name = message.from_user.first_name or "User"
    
    db.add_user(uid, username, first_name)
    db.increment_stat('total_starts')
    db.increment_user_stat(uid, 'total_starts')
    
    # FIRE EXPLOSION ANIMATION
    anim_msg_id = AnimationSystem.fire_explosion_animation(bot, message.chat.id)
    
    if anim_msg_id:
        try:
            time.sleep(0.5)
            bot.delete_message(message.chat.id, anim_msg_id)
        except:
            pass
    
    plan = db.get_user_plan(uid)
    plan_emoji = Config.PLAN_LIMITS[plan]['emoji']
    
    welcome_text = f"""
🔥 <b>ASTRONIX FIRE EDITION v4.0</b> 🔥

👋 ᴡᴇʟᴄᴏᴍᴇ <b>{first_name}</b>! ⛩️

╔═══════════════════════════════╗
║  🐉 <b>CYBERPUNK FEATURES</b> 🐉  
╠═══════════════════════════════╣
║ ⚡ Instant Bot Hosting
║ 🧬 Smart Dependency Manager
║ 🔱 Isolated Virtual Envs
║ 💠 .py & .zip Support
║ 🌀 Real-time Control
║ 🔥 Zero-Error Deploy
╚═══════════════════════════════╝

{plan_emoji} <b>Your Plan:</b> <code>{plan}</code>

🍹 <b>Need help?</b> Click "🍹 ʜᴇʟᴘ" below
💎 <b>Upgrade?</b> Click "👒 ᴠɪᴘ ᴘʟᴀɴꜱ"

⚜️ <i>Powered by Astronix Enterprise</i>
"""
    
    try:
        bot.send_photo(message.chat.id, photo=Config.START_PIC, caption=welcome_text,
                      reply_markup=UIComponents.main_keyboard())
    except:
        bot.send_message(message.chat.id, welcome_text, reply_markup=UIComponents.main_keyboard())

@bot.message_handler(func=lambda m: m.text == "🍹 ʜᴇʟᴘ")
@requires_access
def cmd_help(message):
    help_text = """
📚 <b>COMMAND REFERENCE</b>

<b>💠 BASIC COMMANDS:</b>
🫧 /start - Initialize bot
🍹 /help - Show help
🗺️ /ping - Check status
🎐 /upload - Upload bot
🥏 /mybots - View bots
🥂 /stats - Statistics
👒 /plan - View plans
🌸 /redeem - Redeem code

<b>🔱 KEYBOARD BUTTONS:</b>
⚡ ꜱᴛᴀʀᴛ ʙᴏᴛ - Run bot
🗑 ᴅᴇʟᴇᴛᴇ - Remove bot
🥏 ᴍʏ ʙᴏᴛꜱ - List bots
🥂 ꜱᴛᴀᴛꜱ - System stats
👒 ᴠɪᴘ ᴘʟᴀɴꜱ - Upgrade
🆘 ꜱᴜᴘᴘᴏʀᴛ - Get help

🐉 Upload .py or .zip files
💠 Auto dependency detection
🔥 Zero-error deployment

🌀 @{Config.FORCE_GROUP}
"""
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['ping'])
@requires_access
def cmd_ping(message):
    start = time.time()
    stats = Logger.get_system_stats()
    ping = (time.time() - start) * 1000
    
    text = f"""
🗺️ <b>SYSTEM STATUS</b>

📡 Ping: <code>{ping:.2f}ms</code>
🔥 CPU: <code>{stats.get('cpu_percent', 0):.1f}%</code>
💾 RAM: <code>{stats.get('ram_percent', 0):.1f}%</code>
👥 Users: <code>{db.get_total_users()}</code>
🤖 Active: <code>{len(process_manager.processes)}</code>

✅ All systems operational!
"""
    bot.send_message(message.chat.id, text)

# ══════════════════════════════════════════════════════════════════════════════
# 📤 FILE UPLOAD HANDLERS
# ══════════════════════════════════════════════════════════════════════════════

@bot.message_handler(func=lambda m: m.text == "🎐 ᴜᴘʟᴏᴀᴅ ʙᴏᴛ")
@requires_access
def keyboard_upload(message):
    cmd_upload(message)

@bot.message_handler(commands=['upload'])
@requires_access
def cmd_upload(message):
    uid = message.from_user.id
    plan = db.get_user_plan(uid)
    limits = Config.PLAN_LIMITS[plan]
    
    text = f"""
📤 <b>UPLOAD YOUR BOT</b> 🧬

🔥 <b>SUPPORTED:</b> .py | .zip

{Config.PLAN_LIMITS[plan]['emoji']} <b>Plan: {plan}</b>

📄 .py limit: <code>{limits['py']}</code>
📦 .zip limit: <code>{limits['zip']}</code>
💾 Max size: <code>{limits['max_size_mb']}MB</code>

🌀 Just send your file here!
"""
    
    try:
        bot.send_photo(message.chat.id, photo=Config.UPLOAD_PIC, caption=text)
    except:
        bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['document'])
@requires_access
def handle_document_upload(message):
    """Handle file uploads with progress"""
    uid = message.from_user.id
    document = message.document
    file_name = document.file_name
    file_size_mb = document.file_size / (1024 * 1024)
    
    if not (file_name.endswith('.py') or file_name.endswith('.zip')):
        bot.send_message(message.chat.id, "❌ Only .py and .zip files supported.")
        return
    
    file_type = 'zip' if file_name.endswith('.zip') else 'py'
    plan = db.get_user_plan(uid)
    limits = Config.PLAN_LIMITS[plan]
    
    if file_size_mb > limits['max_size_mb']:
        bot.send_message(message.chat.id, f"❌ File too large. Max: {limits['max_size_mb']}MB")
        return
    
    current_count = db.get_user_bot_count(uid, file_type)
    if current_count >= limits[file_type]:
        bot.send_message(message.chat.id, f"🚫 Limit reached: {current_count}/{limits[file_type]}")
        return
    
    progress_msg = bot.send_message(message.chat.id, "⏳ Uploading...\n▱▱▱▱▱▱▱▱▱▱ 0%")
    
    try:
        user_dir = Config.UPLOAD_DIR / str(uid)
        user_dir.mkdir(exist_ok=True)
        
        AnimationSystem.progress_animation(bot, message.chat.id, progress_msg.message_id, 20, "📥 Downloading...")
        
        file_info = bot.get_file(document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        AnimationSystem.progress_animation(bot, message.chat.id, progress_msg.message_id, 60, "💾 Saving...")
        
        file_path = user_dir / file_name
        with open(file_path, 'wb') as f:
            f.write(downloaded_file)
        
        AnimationSystem.progress_animation(bot, message.chat.id, progress_msg.message_id, 100, "✅ Complete!")
        time.sleep(0.5)
        bot.delete_message(message.chat.id, progress_msg.message_id)
        
        db.increment_stat('total_uploads')
        db.increment_user_stat(uid, 'total_uploads')
        
        is_running = process_manager.is_running(uid, file_name)
        
        bot.send_message(
            message.chat.id,
            f"✅ <b>Upload Success!</b> 🔥\n\n📁 {file_name}\n💾 {file_size_mb:.2f}MB",
            reply_markup=UIComponents.bot_control_keyboard(uid, file_name, is_running)
        )
        
        Logger.log_to_group(f"📦 Upload: {uid} - {file_name}")
    
    except Exception as e:
        try:
            bot.delete_message(message.chat.id, progress_msg.message_id)
        except:
            pass
        bot.send_message(message.chat.id, f"❌ Upload failed: {str(e)[:200]}")

# ══════════════════════════════════════════════════════════════════════════════
# 🎮 BOT CONTROL HANDLERS - ENHANCED WITH KASUKABE STABILITY
# ══════════════════════════════════════════════════════════════════════════════

def start_bot_process(uid: int, bot_name: str, chat_id: int) -> bool:
    """
    Start a bot process with KASUKABE STABILITY
    - Smart entry detection
    - 5-second watchdog
    - Environment variable pass-through
    - Crash report on failure
    """
    
    if process_manager.is_running(uid, bot_name):
        bot.send_message(chat_id, f"⚠️ <code>{bot_name}</code> already running.")
        return False
    
    file_path = Config.UPLOAD_DIR / str(uid) / bot_name
    if not file_path.exists():
        bot.send_message(chat_id, f"❌ <code>{bot_name}</code> not found.")
        return False
    
    progress_msg = bot.send_message(chat_id, "🔥 Starting...\n▱▱▱▱▱▱▱▱▱▱ 0%")
    
    try:
        bot_dir = file_path.parent
        
        AnimationSystem.progress_animation(bot, chat_id, progress_msg.message_id, 10, "🔧 Preparing...")
        
        # ═══ HANDLE ZIP EXTRACTION ═══
        if bot_name.endswith('.zip'):
            extract_dir = bot_dir / bot_name.replace('.zip', '')
            if extract_dir.exists():
                shutil.rmtree(extract_dir)
            extract_dir.mkdir(exist_ok=True)
            
            AnimationSystem.progress_animation(bot, chat_id, progress_msg.message_id, 20, "📦 Extracting...")
            
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # NESTED FOLDER FIX
            work_dir = SmartEntryDetector.get_nested_code_directory(extract_dir)
            
            # SMART ENTRY DETECTION
            main_file = SmartEntryDetector.detect_main_file(work_dir)
            
            if not main_file:
                bot.delete_message(chat_id, progress_msg.message_id)
                bot.send_message(chat_id, "❌ No valid Python entry point found in ZIP.")
                return False
            
            script_path = main_file
            print(f"📍 Entry point: {script_path}")
            
        else:
            work_dir = bot_dir
            script_path = file_path
        
        AnimationSystem.progress_animation(bot, chat_id, progress_msg.message_id, 30, "🧬 Creating venv...")
        
        # ═══ SETUP ENVIRONMENT - RESILIENT ═══
        success, venv_python, setup_msg, installed, failed = VirtualEnvironmentManager.setup_bot_environment(work_dir)
        
        if not success:
            bot.delete_message(chat_id, progress_msg.message_id)
            bot.send_message(chat_id, f"❌ Setup failed: {setup_msg}")
            return False
        
        AnimationSystem.progress_animation(bot, chat_id, progress_msg.message_id, 80, "⚡ Launching...")
        
        # ═══ PREPARE LOG FILE ═══
        log_file_path = work_dir / f"{bot_name}.log"
        log_file = open(log_file_path, 'a', buffering=1, encoding='utf-8')
        
        log_file.write(f"\n{'='*60}\n")
        log_file.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"User: {uid}\n")
        log_file.write(f"Entry: {script_path}\n")
        log_file.write(f"CWD: {work_dir}\n")
        if failed:
            log_file.write(f"Failed deps: {', '.join(failed[:5])}\n")
        log_file.write(f"{'='*60}\n\n")
        log_file.flush()
        
        # ═══ ENVIRONMENT VARIABLES - TOKEN PASS-THROUGH ═══
        env = os.environ.copy()
        env['PYTHONPATH'] = str(work_dir)
        env['PYTHONUNBUFFERED'] = '1'
        
        # ═══ START PROCESS WITH BACKGROUND STABILITY ═══
        process = subprocess.Popen(
            [str(venv_python), '-u', str(script_path)],
            cwd=str(work_dir),
            stdout=log_file,
            stderr=log_file,
            env=env,
            start_new_session=True  # Background stability
        )
        
        print(f"🚀 Process started: PID {process.pid}")
        
        # ═══════════════════════════════════════════════════════════════════
        # 🔥 THE 5-SECOND WATCHDOG - KASUKABE STABILITY CORE
        # ═══════════════════════════════════════════════════════════════════
        
        AnimationSystem.progress_animation(bot, chat_id, progress_msg.message_id, 90, "⏱ Watchdog (5s)...")
        
        print("⏱ Starting 5-second watchdog...")
        time.sleep(5)  # CRITICAL: Wait 5 seconds
        
        # Check if process is still alive
        exit_code = process.poll()
        
        if exit_code is not None:
            # ❌ PROCESS CRASHED - SEND CRASH REPORT
            print(f"❌ Process crashed with exit code: {exit_code}")
            
            bot.delete_message(chat_id, progress_msg.message_id)
            log_file.close()
            
            # Read last 15 lines of log
            crash_report = Logger.read_last_log_lines(log_file_path, 15)
            
            # Truncate if too long
            if len(crash_report) > 3500:
                crash_report = crash_report[-3500:]
            
            bot.send_message(
                chat_id,
                f"""
❌ <b>Bot Crashed!</b> 💥

🤖 <code>{bot_name}</code>
🔥 Exit Code: <code>{exit_code}</code>

📋 <b>Crash Report (Last 15 lines):</b>

<code>{crash_report}</code>

💡 <b>Tip:</b> Fix the errors and try again!
""",
                reply_markup=UIComponents.bot_control_keyboard(uid, bot_name, False)
            )
            
            return False
        
        # ✅ PROCESS IS RUNNING - SUCCESS!
        print(f"✅ Process stable after 5 seconds")
        
        AnimationSystem.progress_animation(bot, chat_id, progress_msg.message_id, 100, "✅ Complete!")
        time.sleep(0.5)
        
        # Add to process manager
        process_manager.add_process(uid, bot_name, process, log_file, str(venv_python.parent))
        
        # Get process info
        proc_info = process_manager.get_process_info(uid, bot_name)
        
        bot.delete_message(chat_id, progress_msg.message_id)
        
        # Send success message
        success_msg = f"""
✅ <b>Bot Started!</b> 🔥

🤖 <code>{bot_name}</code>
🆔 PID: <code>{process.pid}</code>
"""
        
        if proc_info:
            success_msg += f"""🔥 CPU: <code>{proc_info['cpu_percent']:.1f}%</code>
💾 RAM: <code>{proc_info['memory_mb']:.1f}MB</code>
"""
        
        if failed:
            success_msg += f"\n⚠️ {len(failed)} deps failed (bot running anyway)"
        
        success_msg += "\n🌀 Your bot is now live!"
        
        bot.send_message(
            chat_id,
            success_msg,
            reply_markup=UIComponents.bot_control_keyboard(uid, bot_name, True)
        )
        
        db.increment_stat('total_bot_runs')
        Logger.log_to_group(f"🚀 Bot Started: {uid} - {bot_name} (PID: {process.pid})")
        
        return True
    
    except Exception as e:
        print(f"❌ Critical error: {e}")
        traceback.print_exc()
        try:
            bot.delete_message(chat_id, progress_msg.message_id)
        except:
            pass
        bot.send_message(chat_id, f"❌ Critical Error:\n\n<code>{str(e)[:500]}</code>")
        return False

def stop_bot_process(uid: int, bot_name: str, chat_id: int) -> bool:
    if not process_manager.is_running(uid, bot_name):
        bot.send_message(chat_id, f"⚠️ <code>{bot_name}</code> not running.")
        return False
    
    if process_manager.stop_process(uid, bot_name):
        bot.send_message(
            chat_id,
            f"⏸ <b>Bot Stopped</b>\n\n🤖 <code>{bot_name}</code>",
            reply_markup=UIComponents.bot_control_keyboard(uid, bot_name, False)
        )
        return True
    return False

def delete_bot_files(uid: int, bot_name: str, chat_id: int) -> bool:
    if process_manager.is_running(uid, bot_name):
        process_manager.stop_process(uid, bot_name, force=True)
    
    try:
        file_path = Config.UPLOAD_DIR / str(uid) / bot_name
        if file_path.exists():
            file_path.unlink()
        
        if bot_name.endswith('.zip'):
            extract_dir = file_path.parent / bot_name.replace('.zip', '')
            if extract_dir.exists():
                shutil.rmtree(extract_dir)
        
        log_file = file_path.parent / f"{bot_name}.log"
        if log_file.exists():
            log_file.unlink()
        
        bot.send_message(chat_id, f"🗑 <b>Deleted</b>\n\n<code>{bot_name}</code>")
        return True
    except Exception as e:
        bot.send_message(chat_id, f"❌ Delete failed: {str(e)[:200]}")
        return False

def send_bot_logs(uid: int, bot_name: str, chat_id: int, last_n_lines: int = 20):
    log_file_path = Config.UPLOAD_DIR / str(uid) / f"{bot_name}.log"
    
    if bot_name.endswith('.zip'):
        extract_dir = Config.UPLOAD_DIR / str(uid) / bot_name.replace('.zip', '')
        alt_log = extract_dir / f"{bot_name}.log"
        if alt_log.exists():
            log_file_path = alt_log
    
    if not log_file_path.exists() or log_file_path.stat().st_size == 0:
        bot.send_message(chat_id, "📭 No logs available.")
        return
    
    log_content = Logger.read_last_log_lines(log_file_path, last_n_lines)
    
    if len(log_content) > 3500:
        log_content = log_content[-3500:]
    
    bot.send_message(chat_id, f"🔮 <b>Logs: {bot_name}</b>\n\n<code>{log_content}</code>")

# ══════════════════════════════════════════════════════════════════════════════
# ⌨️ KEYBOARD HANDLERS
# ══════════════════════════════════════════════════════════════════════════════

@bot.message_handler(func=lambda m: m.text == "⚡ ꜱᴛᴀʀᴛ ʙᴏᴛ")
@requires_access
def keyboard_start_bot(message):
    uid = message.from_user.id
    user_dir = Config.UPLOAD_DIR / str(uid)
    
    if not user_dir.exists():
        bot.send_message(message.chat.id, "📭 No bots found. Upload one first!")
        return
    
    bots = [f.name for f in user_dir.iterdir() if f.is_file() and (f.name.endswith('.py') or f.name.endswith('.zip'))]
    
    if not bots:
        bot.send_message(message.chat.id, "📭 No bots found.")
        return
    
    keyboard = InlineKeyboardMarkup()
    for bot_name in bots:
        status = "🟢" if process_manager.is_running(uid, bot_name) else "⚪"
        keyboard.add(InlineKeyboardButton(f"{status} {bot_name}", callback_data=f"run:{uid}:{bot_name}"))
    
    bot.send_message(message.chat.id, "⚡ <b>Select Bot to Start</b>", reply_markup=keyboard)

@bot.message_handler(func=lambda m: m.text == "🗑 ᴅᴇʟᴇᴛᴇ ʙᴏᴛ")
@requires_access
def keyboard_delete_bot(message):
    uid = message.from_user.id
    user_dir = Config.UPLOAD_DIR / str(uid)
    
    if not user_dir.exists():
        bot.send_message(message.chat.id, "📭 No bots found.")
        return
    
    bots = [f.name for f in user_dir.iterdir() if f.is_file() and (f.name.endswith('.py') or f.name.endswith('.zip'))]
    
    if not bots:
        bot.send_message(message.chat.id, "📭 No bots found.")
        return
    
    keyboard = InlineKeyboardMarkup()
    for bot_name in bots:
        keyboard.add(InlineKeyboardButton(f"🗑 {bot_name}", callback_data=f"delete:{uid}:{bot_name}"))
    
    bot.send_message(message.chat.id, "🗑 <b>Select Bot to Delete</b>", reply_markup=keyboard)

@bot.message_handler(func=lambda m: m.text == "🥏 ᴍʏ ʙᴏᴛꜱ")
@requires_access
def cmd_mybots(message):
    uid = message.from_user.id
    running_bots = process_manager.get_user_bots(uid)
    
    user_dir = Config.UPLOAD_DIR / str(uid)
    all_bots = []
    if user_dir.exists():
        all_bots = [f.name for f in user_dir.iterdir() if f.is_file() and (f.name.endswith('.py') or f.name.endswith('.zip'))]
    
    plan = db.get_user_plan(uid)
    limits = Config.PLAN_LIMITS[plan]
    
    py_running = process_manager.get_running_count(uid, 'py')
    zip_running = process_manager.get_running_count(uid, 'zip')
    
    text = f"""
🤖 <b>Your Bots</b> 🔥

💎 Plan: <code>{plan}</code>
📄 .py: <code>{py_running}/{limits['py']}</code>
📦 .zip: <code>{zip_running}/{limits['zip']}</code>
📊 Total: <code>{len(all_bots)}</code>

"""
    
    if running_bots:
        text += "🟢 <b>Running:</b>\n"
        for bot_name in running_bots:
            proc_info = process_manager.get_process_info(uid, bot_name)
            if proc_info:
                text += f"🔥 <code>{bot_name}</code> (PID:{proc_info['pid']})\n"
        text += "\n"
    
    stopped_bots = [b for b in all_bots if b not in running_bots]
    if stopped_bots:
        text += "⚪ <b>Stopped:</b>\n"
        for bot_name in stopped_bots:
            text += f"⏸ <code>{bot_name}</code>\n"
    
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == "🥂 ꜱʏꜱᴛᴇᴍ ꜱᴛᴀᴛꜱ")
@requires_access
def cmd_stats(message):
    uid = message.from_user.id
    plan = db.get_user_plan(uid)
    user_data = db.execute("SELECT * FROM users WHERE uid=?", (uid,)).fetchone()
    
    sys_stats = Logger.get_system_stats()
    
    text = f"""
📊 <b>YOUR STATISTICS</b> 🧬

👤 <b>User Info:</b>
🆔 ID: <code>{uid}</code>
💎 Plan: <code>{plan}</code>

🤖 <b>Usage:</b>
📤 Uploads: <code>{user_data['total_uploads'] if user_data else 0}</code>
⚡ Starts: <code>{user_data['total_starts'] if user_data else 0}</code>

🖥️ <b>Server:</b>
🔥 CPU: <code>{sys_stats.get('cpu_percent', 0):.1f}%</code>
💾 RAM: <code>{sys_stats.get('ram_percent', 0):.1f}%</code>
🤖 Active: <code>{len(process_manager.processes)}</code>

🌀 Upgrade for more power!
"""
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == "👒 ᴠɪᴘ ᴘʟᴀɴꜱ")
@requires_access
def keyboard_vip_plans(message):
    """CAROUSEL UI - ONE PLAN AT A TIME"""
    plan_name = list(Config.PLAN_LIMITS.keys())[0]
    description = UIComponents.get_plan_description(plan_name)
    bot.send_message(message.chat.id, description, reply_markup=UIComponents.plan_carousel_keyboard(0))

@bot.message_handler(func=lambda m: m.text == "🆘 ꜱᴜᴘᴘᴏʀᴛ")
@requires_access
def keyboard_support(message):
    text = f"""
🆘 <b>Support & Help</b>

💬 Join our support group
🐉 Ask questions
💡 Get help from community

<b>📢 Support:</b> @{Config.FORCE_GROUP}
<b>📣 Channel:</b> @{Config.FORCE_CHANNEL}

⚜️ We're here 24/7!
"""
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("💬 Support Group", url=f"https://t.me/{Config.FORCE_GROUP}"))
    keyboard.add(InlineKeyboardButton("📢 Channel", url=f"https://t.me/{Config.FORCE_CHANNEL}"))
    
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

@bot.message_handler(commands=['plan'])
@requires_access
def cmd_plan(message):
    uid = message.from_user.id
    current_plan = db.get_user_plan(uid)
    
    text = f"""
💎 <b>VIP PLANS</b> 🔥

<b>Current:</b> <code>{current_plan}</code>

🆓 FREE: 3 .py, 1 .zip, 5MB
⛩️ BRONZE: 5 .py, 3 .zip, 10MB
🐉 SILVER: 10 .py, 5 .zip, 25MB
🧿 GOLD: 20 .py, 10 .zip, 50MB
🌀 PLATINUM: 50 .py, 25 .zip, 100MB
🔥 DIAMOND: ∞ .py, ∞ .zip, 500MB

🌀 Contact @{Config.FORCE_GROUP}
🎁 Use /redeem for codes
"""
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['redeem'])
@requires_access
def cmd_redeem(message):
    args = message.text.split()
    if len(args) < 2:
        bot.send_message(message.chat.id, "🎁 <b>Redeem Code</b>\n\n<b>Usage:</b> <code>/redeem CODE</code>")
        return
    
    code = args[1].upper()
    uid = message.from_user.id
    
    success, plan, msg = db.redeem_code(code, uid)
    
    if success:
        limits = Config.PLAN_LIMITS[plan]
        bot.send_message(
            message.chat.id,
            f"""
🎉 <b>Code Redeemed!</b> 🔥

{Config.PLAN_LIMITS[plan]['emoji']} <b>New Plan:</b> <code>{plan}</code>

📄 {limits['py']} .py bots
📦 {limits['zip']} .zip bots
💾 {limits['max_size_mb']}MB max

🐉 Enjoy your upgrade!
"""
        )
        db.increment_stat('total_redeems')
    else:
        bot.send_message(message.chat.id, f"❌ {msg}")

# ══════════════════════════════════════════════════════════════════════════════
# 👑 ADMIN COMMANDS
# ══════════════════════════════════════════════════════════════════════════════

@bot.message_handler(commands=['admin'])
@owner_only
def cmd_admin(message):
    total = db.get_total_users()
    premium = db.get_premium_users()
    banned = db.get_banned_count()
    running = len(process_manager.processes)
    
    sys_stats = Logger.get_system_stats()
    
    text = f"""
👑 <b>ADMIN PANEL</b> 🔥

👥 <b>Users:</b>
Total: <code>{total}</code>
Premium: <code>{premium}</code>
Banned: <code>{banned}</code>

🤖 <b>Bots:</b>
Running: <code>{running}</code>
Total Starts: <code>{db.get_stat('total_starts')}</code>

🖥️ <b>Server:</b>
CPU: <code>{sys_stats.get('cpu_percent', 0):.1f}%</code>
RAM: <code>{sys_stats.get('ram_percent', 0):.1f}%</code>

🔐 Status: {'🔒 Locked' if db.get_setting('locked') == '1' else '🔓 Unlocked'}
"""
    bot.send_message(message.chat.id, text, reply_markup=UIComponents.admin_keyboard())

@bot.message_handler(func=lambda m: m.text == "🏠 ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ")
def keyboard_back_home(message):
    bot.send_message(message.chat.id, "🏠 <b>Main Menu</b>", reply_markup=UIComponents.main_keyboard())

@bot.message_handler(func=lambda m: m.text == "🖥 ᴍᴀꜱᴛᴇʀ ᴅᴀꜱʜʙᴏᴀʀᴅ")
@owner_only
def keyboard_master_dashboard(message):
    """MASTER DASHBOARD - View all running bots"""
    all_running = process_manager.get_all_processes_info()
    
    if not all_running:
        bot.send_message(message.chat.id, "📭 No running bots.")
        return
    
    by_user = defaultdict(list)
    for proc in all_running:
        by_user[proc['uid']].append(proc)
    
    text = f"""
🖥 <b>MASTER DASHBOARD</b> 🔥

Total: <code>{len(all_running)}</code> bots
Users: <code>{len(by_user)}</code>

╔═══════════════════════════════╗
"""
    
    for uid, procs in sorted(by_user.items(), key=lambda x: len(x[1]), reverse=True):
        plan = db.get_user_plan(uid)
        text += f"║ 👤 User: <code>{uid}</code> ({plan})\n"
        text += f"║ 🤖 Bots: <code>{len(procs)}</code>\n"
        
        total_cpu = sum(p['cpu_percent'] for p in procs)
        total_ram = sum(p['memory_mb'] for p in procs)
        
        text += f"║ 🔥 CPU: <code>{total_cpu:.1f}%</code>\n"
        text += f"║ 💾 RAM: <code>{total_ram:.1f}MB</code>\n"
        
        for proc in procs[:2]:
            uptime = int((time.time() - proc['create_time']) / 60)
            text += f"║   └ <code>{proc['bot_name'][:20]}</code> (PID:{proc['pid']}, {uptime}m)\n"
        
        text += "╠═══════════════════════════════╣\n"
    
    text += "╚═══════════════════════════════╝"
    
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == "📢 ʙʀᴏᴀᴅᴄᴀꜱᴛ")
@owner_only
def keyboard_broadcast(message):
    bot.send_message(message.chat.id, "📢 Reply with broadcast message:")
    bot.register_next_step_handler(message, process_broadcast)

def process_broadcast(message):
    text = message.text
    users = db.execute("SELECT uid FROM users").fetchall()
    
    success = 0
    for user in users:
        try:
            bot.send_message(user['uid'], f"📢 <b>Broadcast</b>\n\n{text}")
            success += 1
            time.sleep(0.05)
        except:
            pass
    
    bot.send_message(message.chat.id, f"✅ Broadcast complete: {success} users")

@bot.message_handler(func=lambda m: m.text == "💎 ᴀᴅᴅ ᴘʀᴇᴍɪᴜᴍ")
@owner_only
def keyboard_add_premium(message):
    plans = ', '.join(Config.PLAN_LIMITS.keys())
    bot.send_message(message.chat.id, f"💎 Reply: <code>user_id PLAN days</code>\n\nPlans: {plans}")
    bot.register_next_step_handler(message, process_add_premium)

def process_add_premium(message):
    try:
        parts = message.text.split()
        uid = int(parts[0])
        plan = parts[1].upper()
        days = int(parts[2]) if len(parts) > 2 else 30
        
        if plan not in Config.PLAN_LIMITS:
            bot.send_message(message.chat.id, "❌ Invalid plan")
            return
        
        db.set_user_plan(uid, plan, days, message.from_user.id)
        bot.send_message(message.chat.id, f"✅ Added {plan} to user {uid} for {days} days")
        
        try:
            bot.send_message(uid, f"🎉 Upgraded to <b>{plan}</b> for {days} days!")
        except:
            pass
    except:
        bot.send_message(message.chat.id, "❌ Invalid format")

@bot.message_handler(func=lambda m: m.text == "🎁 ɢᴇɴ ᴄᴏᴅᴇ")
@owner_only
def keyboard_gen_code(message):
    plans = ', '.join(Config.PLAN_LIMITS.keys())
    bot.send_message(message.chat.id, f"🎁 Reply: <code>PLAN days</code>\n\nPlans: {plans}")
    bot.register_next_step_handler(message, process_gen_code)

def process_gen_code(message):
    try:
        parts = message.text.split()
        plan = parts[0].upper()
        days = int(parts[1]) if len(parts) > 1 else 30
        
        if plan not in Config.PLAN_LIMITS:
            bot.send_message(message.chat.id, "❌ Invalid plan")
            return
        
        code = f"FIRE{random.randint(1000, 9999)}{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}"
        db.create_giveaway_code(code, plan, days, message.from_user.id)
        
        bot.send_message(message.chat.id, f"🎁 <b>Code Generated</b>\n\n<code>{code}</code>\nPlan: {plan}\nDays: {days}")
    except:
        bot.send_message(message.chat.id, "❌ Invalid format")

@bot.message_handler(func=lambda m: m.text == "🔒 ʟᴏᴄᴋ ʙᴏᴛ")
@owner_only
def keyboard_lock(message):
    db.set_setting('locked', '1')
    bot.send_message(message.chat.id, "🔒 Bot locked")

@bot.message_handler(func=lambda m: m.text == "🔓 ᴜɴʟᴏᴄᴋ ʙᴏᴛ")
@owner_only
def keyboard_unlock(message):
    db.set_setting('locked', '0')
    bot.send_message(message.chat.id, "🔓 Bot unlocked")

@bot.message_handler(func=lambda m: m.text == "⛔ ʙᴀɴ ᴜꜱᴇʀ")
@owner_only
def keyboard_ban(message):
    bot.send_message(message.chat.id, "⛔ Reply: <code>user_id reason</code>")
    bot.register_next_step_handler(message, process_ban)

def process_ban(message):
    try:
        parts = message.text.split(maxsplit=1)
        uid = int(parts[0])
        reason = parts[1] if len(parts) > 1 else "No reason"
        
        db.ban_user(uid, reason, message.from_user.id)
        stopped = process_manager.stop_all_user_bots(uid)
        
        bot.send_message(message.chat.id, f"✅ Banned user {uid}\nStopped {stopped} bots")
        try:
            bot.send_message(uid, f"🚫 <b>You are banned</b>\n\nReason: {reason}")
        except:
            pass
    except:
        bot.send_message(message.chat.id, "❌ Invalid format")

@bot.message_handler(func=lambda m: m.text == "🔓 ᴜɴʙᴀɴ ᴜꜱᴇʀ")
@owner_only
def keyboard_unban(message):
    bot.send_message(message.chat.id, "🔓 Reply with user ID")
    bot.register_next_step_handler(message, process_unban)

def process_unban(message):
    try:
        uid = int(message.text.strip())
        db.unban_user(uid)
        bot.send_message(message.chat.id, f"✅ Unbanned user {uid}")
        try:
            bot.send_message(uid, "🎉 You have been unbanned!")
        except:
            pass
    except:
        bot.send_message(message.chat.id, "❌ Invalid user ID")

@bot.message_handler(func=lambda m: m.text == "👥 ᴜꜱᴇʀꜱ ɪɴғᴏ")
@owner_only
def keyboard_users(message):
    total = db.get_total_users()
    premium = db.get_premium_users()
    banned = db.get_banned_count()
    
    text = f"""
👥 <b>USER INFO</b>

Total: <code>{total}</code>
Premium: <code>{premium}</code>
Banned: <code>{banned}</code>

📊 Stats: /admin for more
"""
    bot.send_message(message.chat.id, text)

# ══════════════════════════════════════════════════════════════════════════════
# 🎛️ CALLBACK HANDLERS - ALL INLINE BUTTONS
# ══════════════════════════════════════════════════════════════════════════════

@bot.callback_query_handler(func=lambda c: c.data.startswith('run:'))
def callback_run_bot(call):
    try:
        bot.answer_callback_query(call.id, "⚡ Starting...")
    except:
        pass
    _, uid_str, bot_name = call.data.split(':', 2)
    uid = int(uid_str)
    if call.from_user.id != uid and call.from_user.id != Config.OWNER_ID:
        bot.answer_callback_query(call.id, "❌ Not your bot!", show_alert=True)
        return
    start_bot_process(uid, bot_name, call.message.chat.id)

@bot.callback_query_handler(func=lambda c: c.data.startswith('stop:'))
def callback_stop_bot(call):
    try:
        bot.answer_callback_query(call.id, "⏸ Stopping...")
    except:
        pass
    _, uid_str, bot_name = call.data.split(':', 2)
    uid = int(uid_str)
    if call.from_user.id != uid and call.from_user.id != Config.OWNER_ID:
        bot.answer_callback_query(call.id, "❌ Not your bot!", show_alert=True)
        return
    stop_bot_process(uid, bot_name, call.message.chat.id)

@bot.callback_query_handler(func=lambda c: c.data.startswith('stats:'))
def callback_bot_stats(call):
    try:
        bot.answer_callback_query(call.id)
    except:
        pass
    _, uid_str, bot_name = call.data.split(':', 2)
    uid = int(uid_str)
    
    proc_info = process_manager.get_process_info(uid, bot_name)
    if not proc_info:
        bot.answer_callback_query(call.id, "❌ Bot not running", show_alert=True)
        return
    
    uptime = int((time.time() - proc_info['create_time']) / 60)
    text = f"""
📊 <b>Bot Stats</b>

🤖 <code>{bot_name}</code>
🆔 PID: <code>{proc_info['pid']}</code>
🔥 CPU: <code>{proc_info['cpu_percent']:.1f}%</code>
💾 RAM: <code>{proc_info['memory_mb']:.1f}MB</code>
⏱ Uptime: <code>{uptime}m</code>
"""
    
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                             reply_markup=UIComponents.bot_control_keyboard(uid, bot_name, True))
    except:
        bot.send_message(call.message.chat.id, text)

@bot.callback_query_handler(func=lambda c: c.data.startswith('delete:'))
def callback_delete_bot(call):
    try:
        bot.answer_callback_query(call.id)
    except:
        pass
    _, uid_str, bot_name = call.data.split(':', 2)
    uid = int(uid_str)
    if call.from_user.id != uid and call.from_user.id != Config.OWNER_ID:
        bot.answer_callback_query(call.id, "❌ Not your bot!", show_alert=True)
        return
    
    try:
        bot.edit_message_text(
            f"⚠️ <b>Confirm Deletion</b>\n\nDelete <code>{bot_name}</code>?\n\n⚠️ Cannot be undone!",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=UIComponents.confirm_delete_keyboard(uid, bot_name)
        )
    except:
        pass

@bot.callback_query_handler(func=lambda c: c.data.startswith('confirm_delete:'))
def callback_confirm_delete(call):
    try:
        bot.answer_callback_query(call.id, "🗑 Deleting...")
    except:
        pass
    _, uid_str, bot_name = call.data.split(':', 2)
    uid = int(uid_str)
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    delete_bot_files(uid, bot_name, call.message.chat.id)

@bot.callback_query_handler(func=lambda c: c.data.startswith('logs:'))
def callback_logs(call):
    try:
        bot.answer_callback_query(call.id, "📋 Fetching...")
    except:
        pass
    _, uid_str, bot_name = call.data.split(':', 2)
    uid = int(uid_str)
    if call.from_user.id != uid and call.from_user.id != Config.OWNER_ID:
        bot.answer_callback_query(call.id, "❌ Not your bot!", show_alert=True)
        return
    send_bot_logs(uid, bot_name, call.message.chat.id, 20)

@bot.callback_query_handler(func=lambda c: c.data.startswith('plan_nav:'))
def callback_plan_nav(call):
    """CAROUSEL NAVIGATION"""
    try:
        bot.answer_callback_query(call.id)
    except:
        pass
    index = int(call.data.split(':')[1])
    plan_name = list(Config.PLAN_LIMITS.keys())[index]
    description = UIComponents.get_plan_description(plan_name)
    try:
        bot.edit_message_text(description, call.message.chat.id, call.message.message_id,
                             reply_markup=UIComponents.plan_carousel_keyboard(index))
    except:
        pass

@bot.callback_query_handler(func=lambda c: c.data == 'check_membership')
def callback_check_membership(call):
    """Check membership with FIRE ANIMATION"""
    try:
        bot.answer_callback_query(call.id, "🔍 Checking...")
    except:
        pass
    
    uid = call.from_user.id
    
    if AccessControl.is_member(bot, uid):
        # FIRE ANIMATION
        anim_msg_id = AnimationSystem.fire_explosion_animation(bot, call.message.chat.id)
        if anim_msg_id:
            try:
                time.sleep(0.5)
                bot.delete_message(call.message.chat.id, anim_msg_id)
            except:
                pass
        
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        
        username = call.from_user.username
        first_name = call.from_user.first_name or "User"
        db.add_user(uid, username, first_name)
        
        bot.send_message(
            call.message.chat.id,
            f"✅ <b>ACCESS GRANTED!</b> 🔥\n\nWelcome {first_name}!",
            reply_markup=UIComponents.main_keyboard()
        )
    else:
        bot.answer_callback_query(call.id, "❌ Join both channel and group first!", show_alert=True)

@bot.callback_query_handler(func=lambda c: c.data == 'close_msg')
def callback_close(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

@bot.callback_query_handler(func=lambda c: c.data == 'plan_info')
def callback_plan_info(call):
    try:
        bot.answer_callback_query(call.id, "ℹ️ Current plan")
    except:
        pass

# ══════════════════════════════════════════════════════════════════════════════
# 🧹 CLEANUP & SHUTDOWN
# ══════════════════════════════════════════════════════════════════════════════

def cleanup_on_exit():
    if not hasattr(cleanup_on_exit, "done"):
        print("\n🔥 SHUTDOWN SEQUENCE...")
        process_manager.monitoring = False
        process_manager.cleanup_all()
        try:
            db.close()
        except:
            pass
        print("✅ CLEANUP COMPLETE\n")
        cleanup_on_exit.done = True

atexit.register(cleanup_on_exit)

def signal_handler(sig, frame):
    print(f"\n⚠️  Signal received: {sig}")
    cleanup_on_exit()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# ══════════════════════════════════════════════════════════════════════════════
# 🚀 MAIN ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║           🔥 ASTRONIX FIRE EDITION v4.0 ULTIMATE CYBERPUNK 🔥                ║
║              Production-Grade Bot Hosting Platform                           ║
║              3100+ Lines | KASUKABE STABILITY | Enterprise Ready             ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
    
    try:
        bot_info = bot.get_me()
        print(f"✅ Connected: @{bot_info.username}")
        print(f"💾 Database: {Config.DB_PATH}")
        print(f"👥 Users: {db.get_total_users()}")
        print(f"🔥 Status: ONLINE")
        print(f"🧬 Features: Smart Entry | 5s Watchdog | Resilient Deps | Nested ZIP\n")
        
        Logger.log_to_group(f"🔥 <b>BOT STARTED</b>\n\n@{bot_info.username} is now online!")
        
        print("="*80)
        print("⚡ Bot is running with KASUKABE STABILITY... Press Ctrl+C to stop")
        print("="*80 + "\n")
        
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    
    except KeyboardInterrupt:
        print("\n⚠️  KEYBOARD INTERRUPT")
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        traceback.print_exc()
    finally:
        cleanup_on_exit()