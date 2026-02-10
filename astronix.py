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
║                 ASTRONIX FIRE EDITION v3.0 ULTIMATE                          ║
║            Advanced Telegram Bot Hosting & Management Platform               ║
║                                                                              ║
║    🔥 Features: Fire Animation | Smart Deps | Hybrid UI | Zero Errors       ║
║    🐉 Architecture: Modular | Async-Ready | Enterprise Grade                ║
║    ⚜️ Security: Isolated Venvs | Process Control | Rate Limiting            ║
║                                                                              ║
║    Author: @offx_sahil                                                       ║
║    Rebuilt: 2026 | Python 3.10+                                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ══════════════════════════════════════════════════════════════════════════════
# 🔧 CORE IMPORTS - STANDARD LIBRARY
# ══════════════════════════════════════════════════════════════════════════════

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
from pathlib import Path
from typing import Optional, List, Dict, Set, Tuple, Any
from functools import wraps
from datetime import datetime, timedelta
from collections import defaultdict
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
    """Centralized configuration management"""
    
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
    DB_PATH = BASE_DIR / "astronix_fire.db"
    
    # Plan Limits (py_bots, zip_bots)
    PLAN_LIMITS = {
        "FREE": {"py": 3, "zip": 1, "max_size_mb": 5},
        "BRONZE": {"py": 5, "zip": 3, "max_size_mb": 10},
        "SILVER": {"py": 10, "zip": 5, "max_size_mb": 25},
        "GOLD": {"py": 20, "zip": 10, "max_size_mb": 50},
        "PLATINUM": {"py": 50, "zip": 25, "max_size_mb": 100},
        "DIAMOND": {"py": 999999, "zip": 999999, "max_size_mb": 500}
    }
    
    # Rate Limiting
    RATE_LIMIT_SECONDS = 3
    MAX_UPLOAD_SIZE_MB = 100
    
    # Animation Settings
    FIRE_ANIMATION_FRAMES = [
        "▒▒▒▒▒▒▒▒▒▒ 0%",
        "██▒▒▒▒▒▒▒▒ 20% ⛩️ [Initializing...]",
        "████▒▒▒▒▒▒ 40% 🌀 [System Heating...]",
        "██████▒▒▒▒ 60% 🔱 [Core Loading...]",
        "███████▒▒▒ 70% 💠 [Ignition Phase...]",
        "█████████▒ 90% 🐉 [Almost There...]",
        "██████████ 100% 🔥 FIRE DETECTED 🔥"
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

# Validate and setup
if not Config.validate():
    sys.exit(1)
Config.setup_directories()

# ══════════════════════════════════════════════════════════════════════════════
# 💾 DATABASE MANAGEMENT SYSTEM
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
    
    def _initialize_connection(self):
        """Initialize database connection"""
        self.connection = sqlite3.connect(
            str(self.db_path),
            check_same_thread=False,
            timeout=30.0
        )
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
    
    def _create_tables(self):
        """Create all necessary tables"""
        with self.lock:
            # Users table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    uid INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    joined_at INTEGER,
                    last_seen INTEGER
                )
            """)
            
            # Plans table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS plans (
                    uid INTEGER PRIMARY KEY,
                    plan TEXT DEFAULT 'FREE',
                    upgraded_at INTEGER,
                    expires_at INTEGER,
                    FOREIGN KEY (uid) REFERENCES users(uid)
                )
            """)
            
            # Banned users table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS banned (
                    uid INTEGER PRIMARY KEY,
                    banned_at INTEGER,
                    reason TEXT,
                    banned_by INTEGER
                )
            """)
            
            # Giveaway codes table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS giveaway (
                    code TEXT PRIMARY KEY,
                    plan TEXT,
                    created_at INTEGER,
                    created_by INTEGER,
                    used_by INTEGER,
                    used_at INTEGER
                )
            """)
            
            # Bot processes table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS bot_processes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    uid INTEGER,
                    bot_name TEXT,
                    file_type TEXT,
                    pid INTEGER,
                    started_at INTEGER,
                    stopped_at INTEGER,
                    status TEXT DEFAULT 'running'
                )
            """)
            
            # Statistics table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS statistics (
                    key TEXT PRIMARY KEY,
                    value INTEGER DEFAULT 0
                )
            """)
            
            # Settings table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)
            
            # User activity log
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    uid INTEGER,
                    action TEXT,
                    details TEXT,
                    timestamp INTEGER
                )
            """)
            
            # Initialize default settings
            self.cursor.execute(
                "INSERT OR IGNORE INTO settings VALUES ('locked', '0')"
            )
            self.cursor.execute(
                "INSERT OR IGNORE INTO settings VALUES ('maintenance_message', 'Bot is under maintenance')"
            )
            
            # Initialize statistics
            for key in ['total_starts', 'total_uploads', 'total_bot_runs', 'total_commands']:
                self.cursor.execute(
                    "INSERT OR IGNORE INTO statistics VALUES (?, 0)",
                    (key,)
                )
            
            self.connection.commit()
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute a query with locking"""
        with self.lock:
            return self.cursor.execute(query, params)
    
    def executemany(self, query: str, params_list: list) -> sqlite3.Cursor:
        """Execute many queries with locking"""
        with self.lock:
            return self.cursor.executemany(query, params_list)
    
    def commit(self):
        """Commit changes"""
        with self.lock:
            self.connection.commit()
    
    def close(self):
        """Close database connection"""
        with self.lock:
            if self.connection:
                self.connection.close()
    
    # User Management Methods
    def add_user(self, uid: int, username: str = None, first_name: str = None):
        """Add or update user"""
        now = int(time.time())
        self.execute(
            """INSERT OR REPLACE INTO users (uid, username, first_name, joined_at, last_seen)
               VALUES (?, ?, ?, COALESCE((SELECT joined_at FROM users WHERE uid=?), ?), ?)""",
            (uid, username, first_name, uid, now, now)
        )
        self.commit()
    
    def update_last_seen(self, uid: int):
        """Update user's last seen timestamp"""
        self.execute(
            "UPDATE users SET last_seen=? WHERE uid=?",
            (int(time.time()), uid)
        )
        self.commit()
    
    def get_user_plan(self, uid: int) -> str:
        """Get user's plan"""
        if uid == Config.OWNER_ID:
            return "DIAMOND"
        
        result = self.execute(
            "SELECT plan FROM plans WHERE uid=?",
            (uid,)
        ).fetchone()
        
        return result['plan'] if result else "FREE"
    
    def set_user_plan(self, uid: int, plan: str, duration_days: int = None):
        """Set user's plan"""
        now = int(time.time())
        expires_at = None
        if duration_days:
            expires_at = now + (duration_days * 86400)
        
        self.execute(
            """INSERT OR REPLACE INTO plans (uid, plan, upgraded_at, expires_at)
               VALUES (?, ?, ?, ?)""",
            (uid, plan, now, expires_at)
        )
        self.commit()
    
    def is_banned(self, uid: int) -> bool:
        """Check if user is banned"""
        result = self.execute(
            "SELECT 1 FROM banned WHERE uid=?",
            (uid,)
        ).fetchone()
        return result is not None
    
    def ban_user(self, uid: int, reason: str = "No reason provided", banned_by: int = None):
        """Ban a user"""
        self.execute(
            "INSERT OR REPLACE INTO banned VALUES (?, ?, ?, ?)",
            (uid, int(time.time()), reason, banned_by)
        )
        self.commit()
    
    def unban_user(self, uid: int):
        """Unban a user"""
        self.execute("DELETE FROM banned WHERE uid=?", (uid,))
        self.commit()
    
    def get_setting(self, key: str) -> Optional[str]:
        """Get a setting value"""
        result = self.execute(
            "SELECT value FROM settings WHERE key=?",
            (key,)
        ).fetchone()
        return result['value'] if result else None
    
    def set_setting(self, key: str, value: str):
        """Set a setting value"""
        self.execute(
            "INSERT OR REPLACE INTO settings VALUES (?, ?)",
            (key, value)
        )
        self.commit()
    
    def increment_stat(self, key: str, amount: int = 1):
        """Increment a statistic"""
        self.execute(
            "UPDATE statistics SET value = value + ? WHERE key = ?",
            (amount, key)
        )
        self.commit()
    
    def get_stat(self, key: str) -> int:
        """Get a statistic value"""
        result = self.execute(
            "SELECT value FROM statistics WHERE key=?",
            (key,)
        ).fetchone()
        return result['value'] if result else 0
    
    def log_activity(self, uid: int, action: str, details: str = ""):
        """Log user activity"""
        self.execute(
            "INSERT INTO activity_log (uid, action, details, timestamp) VALUES (?, ?, ?, ?)",
            (uid, action, details, int(time.time()))
        )
        self.commit()
    
    def get_total_users(self) -> int:
        """Get total user count"""
        result = self.execute("SELECT COUNT(*) as count FROM users").fetchone()
        return result['count']
    
    def get_premium_users(self) -> int:
        """Get premium user count"""
        result = self.execute(
            "SELECT COUNT(*) as count FROM plans WHERE plan != 'FREE'"
        ).fetchone()
        return result['count']
    
    def get_banned_count(self) -> int:
        """Get banned user count"""
        result = self.execute("SELECT COUNT(*) as count FROM banned").fetchone()
        return result['count']
    
    def create_giveaway_code(self, code: str, plan: str, created_by: int):
        """Create a giveaway code"""
        self.execute(
            "INSERT INTO giveaway (code, plan, created_at, created_by) VALUES (?, ?, ?, ?)",
            (code, plan, int(time.time()), created_by)
        )
        self.commit()
    
    def redeem_code(self, code: str, uid: int) -> Tuple[bool, str, str]:
        """
        Redeem a giveaway code
        Returns: (success, plan, message)
        """
        result = self.execute(
            "SELECT plan, used_by FROM giveaway WHERE code=?",
            (code,)
        ).fetchone()
        
        if not result:
            return False, "", "Invalid code"
        
        if result['used_by']:
            return False, "", "Code already used"
        
        plan = result['plan']
        
        # Mark code as used
        self.execute(
            "UPDATE giveaway SET used_by=?, used_at=? WHERE code=?",
            (uid, int(time.time()), code)
        )
        
        # Upgrade user
        self.set_user_plan(uid, plan)
        
        self.commit()
        return True, plan, "Code redeemed successfully"
    
    def add_bot_process(self, uid: int, bot_name: str, file_type: str, pid: int):
        """Record bot process start"""
        self.execute(
            """INSERT INTO bot_processes (uid, bot_name, file_type, pid, started_at, status)
               VALUES (?, ?, ?, ?, ?, 'running')""",
            (uid, bot_name, file_type, pid, int(time.time()))
        )
        self.commit()
    
    def stop_bot_process(self, uid: int, bot_name: str):
        """Record bot process stop"""
        self.execute(
            """UPDATE bot_processes 
               SET stopped_at=?, status='stopped' 
               WHERE uid=? AND bot_name=? AND status='running'""",
            (int(time.time()), uid, bot_name)
        )
        self.commit()
    
    def get_user_bot_count(self, uid: int, file_type: str = None) -> int:
        """Get count of user's running bots"""
        if file_type:
            result = self.execute(
                """SELECT COUNT(*) as count FROM bot_processes 
                   WHERE uid=? AND file_type=? AND status='running'""",
                (uid, file_type)
            ).fetchone()
        else:
            result = self.execute(
                """SELECT COUNT(*) as count FROM bot_processes 
                   WHERE uid=? AND status='running'""",
                (uid,)
            ).fetchone()
        
        return result['count']

# Initialize database
db = DatabaseManager(Config.DB_PATH)

# ══════════════════════════════════════════════════════════════════════════════
# 🔥 PROCESS MANAGEMENT SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

class ProcessManager:
    """Advanced process management with PID tracking"""
    
    def __init__(self):
        self.processes: Dict[str, subprocess.Popen] = {}
        self.lock = Lock()
        self.log_files: Dict[str, Any] = {}
    
    def get_key(self, uid: int, bot_name: str) -> str:
        """Generate process key"""
        return f"{uid}:{bot_name}"
    
    def is_running(self, uid: int, bot_name: str) -> bool:
        """Check if bot is running"""
        key = self.get_key(uid, bot_name)
        with self.lock:
            if key in self.processes:
                proc = self.processes[key]
                return proc.poll() is None
        return False
    
    def get_process(self, uid: int, bot_name: str) -> Optional[subprocess.Popen]:
        """Get process object"""
        key = self.get_key(uid, bot_name)
        with self.lock:
            return self.processes.get(key)
    
    def add_process(self, uid: int, bot_name: str, process: subprocess.Popen, log_file):
        """Register a new process"""
        key = self.get_key(uid, bot_name)
        with self.lock:
            self.processes[key] = process
            self.log_files[key] = log_file
    
    def remove_process(self, uid: int, bot_name: str):
        """Remove process from tracking"""
        key = self.get_key(uid, bot_name)
        with self.lock:
            if key in self.processes:
                del self.processes[key]
            if key in self.log_files:
                try:
                    self.log_files[key].close()
                except:
                    pass
                del self.log_files[key]
    
    def stop_process(self, uid: int, bot_name: str) -> bool:
        """Stop a running process"""
        key = self.get_key(uid, bot_name)
        
        with self.lock:
            if key not in self.processes:
                return False
            
            proc = self.processes[key]
            
            try:
                # Try graceful termination first
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if didn't terminate
                    proc.kill()
                    proc.wait()
                
                # Close log file
                if key in self.log_files:
                    try:
                        self.log_files[key].close()
                    except:
                        pass
                
                # Update database
                db.stop_bot_process(uid, bot_name)
                
                # Remove from tracking
                del self.processes[key]
                if key in self.log_files:
                    del self.log_files[key]
                
                return True
            
            except Exception as e:
                print(f"Error stopping process {key}: {e}")
                return False
    
    def get_running_count(self, uid: int, file_type: str = None) -> int:
        """Get count of user's running processes"""
        count = 0
        with self.lock:
            for key in self.processes:
                if key.startswith(f"{uid}:"):
                    if file_type:
                        _, name = key.split(":", 1)
                        if name.endswith(f".{file_type}"):
                            count += 1
                    else:
                        count += 1
        return count
    
    def get_user_bots(self, uid: int) -> List[str]:
        """Get list of user's running bots"""
        bots = []
        with self.lock:
            for key in self.processes:
                if key.startswith(f"{uid}:"):
                    _, bot_name = key.split(":", 1)
                    bots.append(bot_name)
        return bots
    
    def stop_all_user_bots(self, uid: int) -> int:
        """Stop all bots for a user"""
        bots = self.get_user_bots(uid)
        count = 0
        for bot_name in bots:
            if self.stop_process(uid, bot_name):
                count += 1
        return count
    
    def cleanup_all(self):
        """Stop all processes (for shutdown)"""
        with self.lock:
            for key in list(self.processes.keys()):
                uid, bot_name = key.split(":", 1)
                try:
                    proc = self.processes[key]
                    proc.terminate()
                    try:
                        proc.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                except:
                    pass
            
            # Close all log files
            for log_file in self.log_files.values():
                try:
                    log_file.close()
                except:
                    pass
            
            self.processes.clear()
            self.log_files.clear()

# Initialize process manager
process_manager = ProcessManager()

# ══════════════════════════════════════════════════════════════════════════════
# 🧠 SMART DEPENDENCY INSTALLER - THE FIX
# ══════════════════════════════════════════════════════════════════════════════

class SmartDependencyInstaller:
    """Intelligent dependency detection and installation"""
    
    # Python 3.10+ has sys.stdlib_module_names
    STDLIB_MODULES = set(sys.stdlib_module_names) if hasattr(sys, 'stdlib_module_names') else set()
    
    # Fallback for Python < 3.10
    BUILTIN_MODULES = set(sys.builtin_module_names)
    
    # Common package name mappings
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
    }
    
    # Force install these for bot compatibility
    ESSENTIAL_PACKAGES = [
        'pyTelegramBotAPI>=4.14.0',
        'requests>=2.31.0',
        'aiohttp>=3.9.0',
        'python-dotenv>=1.0.0',
    ]
    
    @classmethod
    def is_stdlib(cls, module_name: str) -> bool:
        """Check if module is part of standard library"""
        # Remove any version specifiers
        clean_name = module_name.split('==')[0].split('>=')[0].split('<=')[0].strip()
        
        # Check stdlib
        if clean_name in cls.STDLIB_MODULES:
            return True
        
        # Check builtins
        if clean_name in cls.BUILTIN_MODULES:
            return True
        
        # Check if starts with underscore (internal modules)
        if clean_name.startswith('_'):
            return True
        
        # Additional stdlib modules not in sys.stdlib_module_names
        additional_stdlib = {
            'typing', 'collections', 'itertools', 'functools', 
            'operator', 'pathlib', 'dataclasses', 'enum',
            'contextlib', 'abc', 'asyncio', 'concurrent',
        }
        
        if clean_name in additional_stdlib:
            return True
        
        return False
    
    @classmethod
    def parse_requirements_file(cls, requirements_path: Path) -> List[str]:
        """Parse requirements.txt file"""
        if not requirements_path.exists():
            return []
        
        packages = []
        with open(requirements_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                # Extract package name
                pkg = line.split('==')[0].split('>=')[0].split('<=')[0].split('[')[0].strip()
                
                if pkg and not cls.is_stdlib(pkg):
                    packages.append(line)  # Keep full spec
        
        return packages
    
    @classmethod
    def detect_imports_in_file(cls, file_path: Path) -> Set[str]:
        """Detect imports in a Python file using AST"""
        imports = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                source = f.read()
            
            tree = ast.parse(source, filename=str(file_path))
            
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
        
        except (SyntaxError, UnicodeDecodeError) as e:
            print(f"⚠️  Error parsing {file_path}: {e}")
        
        return imports
    
    @classmethod
    def detect_imports_in_directory(cls, directory: Path) -> Set[str]:
        """Recursively detect all imports in a directory"""
        all_imports = set()
        
        for py_file in directory.rglob('*.py'):
            imports = cls.detect_imports_in_file(py_file)
            all_imports.update(imports)
        
        return all_imports
    
    @classmethod
    def resolve_package_names(cls, imports: Set[str]) -> List[str]:
        """Convert import names to pip package names"""
        packages = []
        
        for imp in imports:
            # Use alias if available
            package = cls.PACKAGE_ALIASES.get(imp, imp)
            packages.append(package)
        
        return packages
    
    @classmethod
    def install_dependencies(cls, venv_python: Path, bot_dir: Path) -> Tuple[bool, str]:
        """
        Install dependencies for a bot
        Returns: (success, message)
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
            return False, f"Failed to upgrade pip: {e}"
        
        # Collect all packages to install
        packages_to_install = []
        
        # Check requirements.txt
        if requirements_file.exists():
            packages_to_install.extend(cls.parse_requirements_file(requirements_file))
        else:
            # Auto-detect imports
            detected_imports = cls.detect_imports_in_directory(bot_dir)
            packages_to_install.extend(cls.resolve_package_names(detected_imports))
        
        # Add essential packages
        packages_to_install.extend(cls.ESSENTIAL_PACKAGES)
        
        # Remove duplicates
        unique_packages = []
        seen = set()
        for pkg in packages_to_install:
            base = pkg.split('==')[0].split('>=')[0].split('<=')[0].lower().strip()
            if base not in seen and not cls.is_stdlib(base):
                seen.add(base)
                unique_packages.append(pkg)
        
        if not unique_packages:
            return True, "No third-party dependencies needed"
        
        # Install packages one by one for better error handling
        failed_packages = []
        installed_packages = []
        
        for package in unique_packages:
            try:
                result = subprocess.run(
                    [
                        str(venv_python), '-m', 'pip', 'install',
                        '--no-cache-dir',
                        '--disable-pip-version-check',
                        package
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=300,
                    text=True
                )
                
                if result.returncode == 0:
                    installed_packages.append(package)
                else:
                    failed_packages.append(package)
            
            except subprocess.TimeoutExpired:
                failed_packages.append(f"{package} (timeout)")
            except Exception as e:
                failed_packages.append(f"{package} ({str(e)})")
        
        if failed_packages:
            return False, f"Failed: {', '.join(failed_packages[:3])}"
        
        return True, f"Installed {len(installed_packages)} packages"

# ══════════════════════════════════════════════════════════════════════════════
# 🏗️ VIRTUAL ENVIRONMENT MANAGER
# ══════════════════════════════════════════════════════════════════════════════

class VirtualEnvironmentManager:
    """Manage virtual environments for bot isolation"""
    
    @staticmethod
    def get_venv_path(bot_dir: Path) -> Path:
        """Get virtual environment directory path"""
        return bot_dir / '.venv'
    
    @staticmethod
    def get_venv_python(venv_dir: Path) -> Path:
        """Get path to virtual environment's Python executable"""
        if sys.platform == 'win32':
            return venv_dir / 'Scripts' / 'python.exe'
        else:
            return venv_dir / 'bin' / 'python'
    
    @classmethod
    def create_venv(cls, bot_dir: Path) -> Tuple[bool, Optional[Path], str]:
        """
        Create virtual environment
        Returns: (success, venv_python_path, message)
        """
        venv_dir = cls.get_venv_path(bot_dir)
        
        # Remove existing venv if present
        if venv_dir.exists():
            try:
                shutil.rmtree(venv_dir)
            except Exception as e:
                return False, None, f"Failed to remove old venv: {e}"
        
        # Create new venv
        try:
            subprocess.run(
                [sys.executable, '-m', 'venv', str(venv_dir)],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=120
            )
        except subprocess.CalledProcessError as e:
            return False, None, f"Venv creation failed: {e.stderr.decode()}"
        except subprocess.TimeoutExpired:
            return False, None, "Venv creation timed out"
        except Exception as e:
            return False, None, f"Unexpected error: {e}"
        
        venv_python = cls.get_venv_python(venv_dir)
        
        if not venv_python.exists():
            return False, None, "Venv created but Python not found"
        
        return True, venv_python, "Virtual environment created"
    
    @classmethod
    def setup_bot_environment(cls, bot_dir: Path) -> Tuple[bool, Optional[Path], str]:
        """
        Complete setup: create venv + install dependencies
        Returns: (success, venv_python_path, message)
        """
        # Create venv
        success, venv_python, msg = cls.create_venv(bot_dir)
        if not success:
            return False, None, msg
        
        # Install dependencies
        success, dep_msg = SmartDependencyInstaller.install_dependencies(venv_python, bot_dir)
        
        if not success:
            return False, venv_python, f"Dependency error: {dep_msg}"
        
        return True, venv_python, f"Setup complete. {dep_msg}"

# ══════════════════════════════════════════════════════════════════════════════
# 🎨 UI COMPONENTS - KEYBOARDS & ANIMATIONS
# ══════════════════════════════════════════════════════════════════════════════

class UIComponents:
    """UI component generators"""
    
    @staticmethod
    def main_keyboard() -> ReplyKeyboardMarkup:
        """Create main reply keyboard (permanent bottom keyboard)"""
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        
        # Row 1: Start & Delete
        keyboard.row(
            KeyboardButton("⚡ ꜱᴛᴀʀᴛ ʙᴏᴛ"),
            KeyboardButton("🗑 ᴅᴇʟᴇᴛᴇ")
        )
        
        # Row 2: My Files & Stats
        keyboard.row(
            KeyboardButton("📂 ᴍʏ ғɪʟᴇꜱ"),
            KeyboardButton("📊 ꜱʏꜱᴛᴇᴍ ꜱᴛᴀᴛꜱ")
        )
        
        # Row 3: VIP & Support
        keyboard.row(
            KeyboardButton("💎 ᴠɪᴘ ᴘʟᴀɴꜱ"),
            KeyboardButton("🆘 ꜱᴜᴘᴘᴏʀᴛ")
        )
        
        return keyboard
    
    @staticmethod
    def admin_keyboard() -> ReplyKeyboardMarkup:
        """Create admin reply keyboard"""
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        
        keyboard.row(
            KeyboardButton("📢 ʙʀᴏᴀᴅᴄᴀꜱᴛ"),
            KeyboardButton("👥 ᴜꜱᴇʀꜱ")
        )
        keyboard.row(
            KeyboardButton("⛔ ʙᴀɴ"),
            KeyboardButton("🔓 ᴜɴʙᴀɴ")
        )
        keyboard.row(
            KeyboardButton("💎 ᴀᴅᴅ ᴘʀᴇᴍɪᴜᴍ"),
            KeyboardButton("🎁 ɢᴇɴ ᴄᴏᴅᴇ")
        )
        keyboard.row(
            KeyboardButton("🔒 ʟᴏᴄᴋ"),
            KeyboardButton("🔓 ᴜɴʟᴏᴄᴋ")
        )
        keyboard.row(
            KeyboardButton("🏠 ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ")
        )
        
        return keyboard
    
    @staticmethod
    def force_join_keyboard() -> InlineKeyboardMarkup:
        """Create force join inline keyboard"""
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            InlineKeyboardButton(
                "📢 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ",
                url=f"https://t.me/{Config.FORCE_CHANNEL}"
            ),
            InlineKeyboardButton(
                "👥 ᴊᴏɪɴ ɢʀᴏᴜᴘ",
                url=f"https://t.me/{Config.FORCE_GROUP}"
            ),
            InlineKeyboardButton(
                "🔄 ᴄʜᴇᴄᴋ ᴀɢᴀɪɴ",
                callback_data="check_membership"
            )
        )
        return keyboard
    
    @staticmethod
    def plan_carousel_keyboard(current_index: int = 0) -> InlineKeyboardMarkup:
        """Create plan carousel inline keyboard"""
        plans = list(Config.PLAN_LIMITS.keys())
        current_plan = plans[current_index]
        
        keyboard = InlineKeyboardMarkup(row_width=2)
        
        # Navigation buttons
        prev_index = (current_index - 1) % len(plans)
        next_index = (current_index + 1) % len(plans)
        
        keyboard.row(
            InlineKeyboardButton(
                "◀️ ᴘʀᴇᴠ",
                callback_data=f"plan_nav:{prev_index}"
            ),
            InlineKeyboardButton(
                "ɴᴇxᴛ ▶️",
                callback_data=f"plan_nav:{next_index}"
            )
        )
        
        # Purchase button
        keyboard.row(
            InlineKeyboardButton(
                f"💰 ɢᴇᴛ {current_plan}",
                url=f"https://t.me/{Config.FORCE_GROUP}"
            )
        )
        
        # Close button
        keyboard.row(
            InlineKeyboardButton(
                "✖️ ᴄʟᴏꜱᴇ",
                callback_data="close_msg"
            )
        )
        
        return keyboard
    
    @staticmethod
    def bot_control_keyboard(uid: int, bot_name: str) -> InlineKeyboardMarkup:
        """Create bot control inline keyboard"""
        keyboard = InlineKeyboardMarkup(row_width=2)
        
        keyboard.row(
            InlineKeyboardButton(
                "⚡ ʀᴜɴ",
                callback_data=f"run:{uid}:{bot_name}"
            ),
            InlineKeyboardButton(
                "⏸ ꜱᴛᴏᴘ",
                callback_data=f"stop:{uid}:{bot_name}"
            )
        )
        
        keyboard.row(
            InlineKeyboardButton(
                "📋 ʟᴏɢꜱ",
                callback_data=f"logs:{uid}:{bot_name}"
            ),
            InlineKeyboardButton(
                "🗑 ᴅᴇʟᴇᴛᴇ",
                callback_data=f"delete:{uid}:{bot_name}"
            )
        )
        
        return keyboard
    
    @staticmethod
    def get_plan_description(plan_name: str) -> str:
        """Get formatted plan description"""
        limits = Config.PLAN_LIMITS.get(plan_name, {})
        py_limit = limits.get('py', 0)
        zip_limit = limits.get('zip', 0)
        size_limit = limits.get('max_size_mb', 0)
        
        emojis = {
            'FREE': '🆓',
            'BRONZE': '🥉',
            'SILVER': '🥈',
            'GOLD': '🥇',
            'PLATINUM': '🏆',
            'DIAMOND': '💎'
        }
        
        emoji = emojis.get(plan_name, '⚜️')
        
        # Format limits
        py_str = f"{py_limit}" if py_limit < 999999 else "∞"
        zip_str = f"{zip_limit}" if zip_limit < 999999 else "∞"
        
        description = f"""
{emoji} <b>{plan_name} PLAN</b> {emoji}

╭─────────────────╮
│ 🐉 <b>Features:</b>
├─ 📄 .py bots: <code>{py_str}</code>
├─ 📦 .zip bots: <code>{zip_str}</code>
├─ 💾 Max size: <code>{size_limit}MB</code>
├─ ⚡ Priority queue
├─ 🔥 Fast deployment
╰─────────────────╯

🌀 <i>Cyberpunk-grade hosting power</i>
"""
        
        return description

# ══════════════════════════════════════════════════════════════════════════════
# 🎬 ANIMATION SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

class AnimationSystem:
    """Handle animated messages"""
    
    @staticmethod
    def fire_animation(bot, chat_id: int) -> int:
        """
        Execute fire animation sequence
        Returns: message_id of final message
        """
        try:
            # Send initial frame
            msg = bot.send_message(chat_id, Config.FIRE_ANIMATION_FRAMES[0])
            
            # Animate through frames
            for frame in Config.FIRE_ANIMATION_FRAMES[1:]:
                time.sleep(0.4)
                try:
                    bot.edit_message_text(
                        frame,
                        chat_id,
                        msg.message_id
                    )
                except:
                    pass
            
            time.sleep(0.5)
            return msg.message_id
        
        except Exception as e:
            print(f"Animation error: {e}")
            return None
    
    @staticmethod
    def loading_animation(bot, chat_id: int, base_text: str, duration: int = 3) -> int:
        """
        Show loading animation
        Returns: message_id
        """
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        
        try:
            msg = bot.send_message(chat_id, f"{frames[0]} {base_text}")
            
            cycles = duration * 2  # ~2 frames per second
            for i in range(cycles):
                frame = frames[i % len(frames)]
                time.sleep(0.5)
                try:
                    bot.edit_message_text(
                        f"{frame} {base_text}",
                        chat_id,
                        msg.message_id
                    )
                except:
                    pass
            
            return msg.message_id
        
        except Exception as e:
            print(f"Loading animation error: {e}")
            return None

# ══════════════════════════════════════════════════════════════════════════════
# 🛡️ ACCESS CONTROL & DECORATORS
# ══════════════════════════════════════════════════════════════════════════════

class AccessControl:
    """Access control and rate limiting"""
    
    last_command_time: Dict[int, float] = {}
    lock = Lock()
    
    @classmethod
    def check_rate_limit(cls, uid: int) -> bool:
        """Check if user is rate limited"""
        with cls.lock:
            now = time.time()
            last_time = cls.last_command_time.get(uid, 0)
            
            if now - last_time < Config.RATE_LIMIT_SECONDS:
                return False
            
            cls.last_command_time[uid] = now
            return True
    
    @classmethod
    def is_member(cls, bot, uid: int) -> bool:
        """Check if user is member of required channels"""
        if uid == Config.OWNER_ID:
            return True
        
        try:
            # Check channel
            ch_member = bot.get_chat_member(f"@{Config.FORCE_CHANNEL}", uid)
            ch_ok = ch_member.status in ['member', 'administrator', 'creator']
            
            # Check group
            gp_member = bot.get_chat_member(f"@{Config.FORCE_GROUP}", uid)
            gp_ok = gp_member.status in ['member', 'administrator', 'creator']
            
            return ch_ok and gp_ok
        
        except Exception as e:
            print(f"Membership check error: {e}")
            return False

def requires_access(func):
    """Decorator for access control"""
    @wraps(func)
    def wrapper(message):
        uid = message.from_user.id
        chat_id = message.chat.id
        
        # Update last seen
        db.update_last_seen(uid)
        
        # Check if banned
        if db.is_banned(uid):
            bot.send_message(
                chat_id,
                "🚫 <b>Access Denied</b>\n\n"
                "You are banned from using this bot.\n"
                "Contact owner if you believe this is a mistake.",
                parse_mode='HTML'
            )
            return
        
        # Check maintenance mode
        if db.get_setting('locked') == '1' and uid != Config.OWNER_ID:
            maintenance_msg = db.get_setting('maintenance_message') or "Bot under maintenance"
            bot.send_message(
                chat_id,
                f"🔒 <b>Maintenance Mode</b>\n\n{maintenance_msg}",
                parse_mode='HTML'
            )
            return
        
        # Check membership
        if not AccessControl.is_member(bot, uid):
            try:
                bot.send_photo(
                    chat_id,
                    photo=Config.FORCE_PIC,
                    caption=(
                        "🔐 <b>Access Restricted</b>\n\n"
                        "Join our channel and group to use this bot.\n\n"
                        "⛩️ After joining, click <b>Check Again</b>"
                    ),
                    reply_markup=UIComponents.force_join_keyboard(),
                    parse_mode='HTML'
                )
            except:
                bot.send_message(
                    chat_id,
                    "🔐 <b>Access Restricted</b>\n\n"
                    "Join our channel and group to use this bot.",
                    reply_markup=UIComponents.force_join_keyboard(),
                    parse_mode='HTML'
                )
            return
        
        # Check rate limit
        if not AccessControl.check_rate_limit(uid):
            bot.send_message(
                chat_id,
                "⏱ <b>Slow Down</b>\n\n"
                f"Please wait {Config.RATE_LIMIT_SECONDS} seconds between commands.",
                parse_mode='HTML'
            )
            return
        
        # All checks passed
        return func(message)
    
    return wrapper

def owner_only(func):
    """Decorator for owner-only commands"""
    @wraps(func)
    def wrapper(message):
        if message.from_user.id != Config.OWNER_ID:
            bot.send_message(
                message.chat.id,
                "⛔ <b>Owner Only</b>\n\nThis command is restricted to bot owner.",
                parse_mode='HTML'
            )
            return
        return func(message)
    
    return wrapper

# ══════════════════════════════════════════════════════════════════════════════
# 🤖 BOT INITIALIZATION
# ══════════════════════════════════════════════════════════════════════════════

bot = telebot.TeleBot(Config.TOKEN, parse_mode='HTML', threaded=True)

# ══════════════════════════════════════════════════════════════════════════════
# 📝 LOGGING UTILITIES
# ══════════════════════════════════════════════════════════════════════════════

class Logger:
    """Centralized logging system"""
    
    @staticmethod
    def log_to_group(text: str):
        """Send log to logs group"""
        if Config.LOGS_GROUP_ID == 0:
            return
        
        try:
            bot.send_message(Config.LOGS_GROUP_ID, text, parse_mode='HTML')
        except Exception as e:
            print(f"Failed to log to group: {e}")
    
    @staticmethod
    def log_file_to_group(file_path: Path, caption: str):
        """Send file log to logs group"""
        if Config.LOGS_GROUP_ID == 0:
            return
        
        try:
            with open(file_path, 'rb') as f:
                bot.send_document(Config.LOGS_GROUP_ID, f, caption=caption)
        except Exception as e:
            print(f"Failed to send file log: {e}")
    
    @staticmethod
    def log_user_action(uid: int, action: str, details: str = ""):
        """Log user action"""
        db.log_activity(uid, action, details)
        
        # Also log to group for important actions
        if action in ['bot_start', 'bot_stop', 'upload', 'redeem']:
            Logger.log_to_group(
                f"🔔 <b>Action:</b> {action}\n"
                f"👤 <b>User:</b> <code>{uid}</code>\n"
                f"📝 <b>Details:</b> {details}"
            )

# ══════════════════════════════════════════════════════════════════════════════
# 🎯 COMMAND HANDLERS - START & HELP
# ══════════════════════════════════════════════════════════════════════════════

@bot.message_handler(commands=['start'])
@requires_access
def cmd_start(message):
    """Handle /start command with fire animation"""
    uid = message.from_user.id
    username = message.from_user.username or "User"
    first_name = message.from_user.first_name or "User"
    
    # Add user to database
    db.add_user(uid, username, first_name)
    db.increment_stat('total_starts')
    
    Logger.log_user_action(uid, 'start', f"Username: @{username}")
    
    # Execute fire animation
    anim_msg_id = AnimationSystem.fire_animation(bot, message.chat.id)
    
    # Delete animation message
    if anim_msg_id:
        try:
            bot.delete_message(message.chat.id, anim_msg_id)
        except:
            pass
    
    # Send welcome message with image
    welcome_text = f"""
🔥 <b>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴀꜱᴛʀᴏɴɪx ғɪʀᴇ ᴇᴅɪᴛɪᴏɴ</b> 🔥

👋 ʜᴇʏ <b>{first_name}</b>! ⛩️

╔═══════════════════════╗
║  🐉 <b>ᴘᴏᴡᴇʀ ғᴇᴀᴛᴜʀᴇꜱ</b> 🐉  
╠═══════════════════════╣
║ ⚡ ɪɴꜱᴛᴀɴᴛ ʙᴏᴛ ʜᴏꜱᴛɪɴɢ
║ 🧬 ꜱᴍᴀʀᴛ ᴅᴇᴘᴇɴᴅᴇɴᴄʏ ᴍɢᴍᴛ
║ 🔱 ɪꜱᴏʟᴀᴛᴇᴅ ᴠɪʀᴛᴜᴀʟ ᴇɴᴠꜱ
║ 💠 .ᴘʏ & .ᴢɪᴘ ꜱᴜᴘᴘᴏʀᴛ
║ 🌀 ʀᴇᴀʟ-ᴛɪᴍᴇ ᴘʀᴏᴄᴇꜱꜱ ᴄᴏɴᴛʀᴏʟ
║ 🧿 ᴄʏʙᴇʀᴘᴜɴᴋ ᴜɪ
╚═══════════════════════╝

💎 <b>ʏᴏᴜʀ ᴘʟᴀɴ:</b> <code>{db.get_user_plan(uid)}</code>

🎯 <b>Qᴜɪᴄᴋ ꜱᴛᴀʀᴛ:</b>
<code>1.</code> ᴜᴘʟᴏᴀᴅ ʏᴏᴜʀ ʙᴏᴛ (.ᴘʏ ᴏʀ .ᴢɪᴘ)
<code>2.</code> ᴄʟɪᴄᴋ ⚡ ꜱᴛᴀʀᴛ ʙᴏᴛ
<code>3.</code> ᴇɴᴊᴏʏ 24/7 ʜᴏꜱᴛɪɴɢ

🆘 <b>ɴᴇᴇᴅ ʜᴇʟᴘ?</b> /help
💎 <b>ᴜᴘɢʀᴀᴅᴇ?</b> ᴄʟɪᴄᴋ "💎 ᴠɪᴘ ᴘʟᴀɴꜱ" ʙᴇʟᴏᴡ

⚜️ <i>ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴀꜱᴛʀᴏɴɪx ᴇɴᴛᴇʀᴘʀɪꜱᴇ</i> ⚜️
"""
    
    try:
        bot.send_photo(
            message.chat.id,
            photo=Config.START_PIC,
            caption=welcome_text,
            reply_markup=UIComponents.main_keyboard()
        )
    except:
        bot.send_message(
            message.chat.id,
            welcome_text,
            reply_markup=UIComponents.main_keyboard()
        )

@bot.message_handler(commands=['help'])
@requires_access
def cmd_help(message):
    """Handle /help command"""
    help_text = """
📚 <b>ᴄᴏᴍᴍᴀɴᴅ ʀᴇғᴇʀᴇɴᴄᴇ</b> 🧪

╔════════════════════════╗
║  <b>💠 ʙᴀꜱɪᴄ ᴄᴏᴍᴍᴀɴᴅꜱ</b>
╠════════════════════════╣
║ /start - 🔥 ɪɴɪᴛɪᴀʟɪᴢᴇ ʙᴏᴛ
║ /help - 📖 ꜱʜᴏᴡ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ
║ /upload - 📤 ᴜᴘʟᴏᴀᴅ ʙᴏᴛ ғɪʟᴇ
║ /mybots - 🤖 ᴠɪᴇᴡ ʀᴜɴɴɪɴɢ ʙᴏᴛꜱ
║ /stats - 📊 ʏᴏᴜʀ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ
║ /plan - 💎 ᴠɪᴇᴡ ᴘʟᴀɴꜱ
║ /redeem - 🎁 ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ
╚════════════════════════╝

╔════════════════════════╗
║  <b>🔱 ᴋᴇʏʙᴏᴀʀᴅ ʙᴜᴛᴛᴏɴꜱ</b>
╠════════════════════════╣
║ ⚡ ꜱᴛᴀʀᴛ ʙᴏᴛ - ʀᴜɴ ʙᴏᴛ
║ 🗑 ᴅᴇʟᴇᴛᴇ - ʀᴇᴍᴏᴠᴇ ʙᴏᴛ
║ 📂 ᴍʏ ғɪʟᴇꜱ - ʟɪꜱᴛ ʙᴏᴛꜱ
║ 📊 ꜱᴛᴀᴛꜱ - ꜱᴇᴇ ᴜꜱᴀɢᴇ
║ 💎 ᴠɪᴘ ᴘʟᴀɴꜱ - ᴜᴘɢʀᴀᴅᴇ
║ 🆘 ꜱᴜᴘᴘᴏʀᴛ - ɢᴇᴛ ʜᴇʟᴘ
╚════════════════════════╝

🐉 <b>ʜᴏᴡ ᴛᴏ ᴜᴘʟᴏᴀᴅ:</b>
<code>1.</code> ꜱᴇɴᴅ .ᴘʏ ғɪʟᴇ ᴏʀ .ᴢɪᴘ
<code>2.</code> ᴡᴀɪᴛ ғᴏʀ ᴜᴘʟᴏᴀᴅ ᴄᴏɴғɪʀᴍᴀᴛɪᴏɴ
<code>3.</code> ᴜꜱᴇ ᴄᴏɴᴛʀᴏʟ ʙᴜᴛᴛᴏɴꜱ

💠 <b>ꜰᴏʀ .ᴢɪᴘ ғɪʟᴇꜱ:</b>
• ɪɴᴄʟᴜᴅᴇ ʀᴇQᴜɪʀᴇᴍᴇɴᴛꜱ.ᴛxᴛ (ᴏᴘᴛɪᴏɴᴀʟ)
• ᴍᴀɪɴ ғɪʟᴇ: ʙᴏᴛ.ᴘʏ ᴏʀ ᴍᴀɪɴ.ᴘʏ
• ᴀᴜᴛᴏ ᴅᴇᴘᴇɴᴅᴇɴᴄʏ ɪɴꜱᴛᴀʟʟ

🌀 <b>ɴᴇᴇᴅ ʜᴇʟᴘ?</b> @{Config.FORCE_GROUP}
"""
    
    bot.send_message(message.chat.id, help_text)

# ══════════════════════════════════════════════════════════════════════════════
# 📤 FILE UPLOAD HANDLERS
# ══════════════════════════════════════════════════════════════════════════════

@bot.message_handler(commands=['upload'])
@requires_access
def cmd_upload(message):
    """Handle /upload command"""
    upload_text = """
📤 <b>ᴜᴘʟᴏᴀᴅ ʏᴏᴜʀ ʙᴏᴛ</b> 🧬

╔═══════════════════════════╗
║  🔥 <b>ꜱᴜᴘᴘᴏʀᴛᴇᴅ ғᴏʀᴍᴀᴛꜱ</b>  
╠═══════════════════════════╣
║ 📄 <b>.py</b> - ꜱɪɴɢʟᴇ ғɪʟᴇ ʙᴏᴛ
║ 📦 <b>.zip</b> - ᴍᴜʟᴛɪ-ғɪʟᴇ ᴘʀᴏᴊᴇᴄᴛ
╚═══════════════════════════╝

🌀 <b>ᴊᴜꜱᴛ ꜱᴇɴᴅ ʏᴏᴜʀ ғɪʟᴇ ʜᴇʀᴇ!</b>

💡 <b>ᴛɪᴘꜱ:</b>
• ꜰᴏʀ .ᴢɪᴘ: ɪɴᴄʟᴜᴅᴇ ᴀʟʟ ғɪʟᴇꜱ
• ᴀᴅᴅ ʀᴇQᴜɪʀᴇᴍᴇɴᴛꜱ.ᴛxᴛ ғᴏʀ ᴅᴇᴘꜱ
• ᴍᴀx ꜱɪᴢᴇ ʙᴀꜱᴇᴅ ᴏɴ ʏᴏᴜʀ ᴘʟᴀɴ

⚜️ <i>ᴀᴜᴛᴏ-ᴅᴇᴛᴇᴄᴛɪᴏɴ ᴇɴᴀʙʟᴇᴅ</i>
"""
    
    try:
        bot.send_photo(
            message.chat.id,
            photo=Config.UPLOAD_PIC,
            caption=upload_text
        )
    except:
        bot.send_message(message.chat.id, upload_text)

@bot.message_handler(content_types=['document'])
@requires_access
def handle_document_upload(message):
    """Handle file uploads"""
    uid = message.from_user.id
    document = message.document
    file_name = document.file_name
    file_size_mb = document.file_size / (1024 * 1024)
    
    # Validate file type
    if not (file_name.endswith('.py') or file_name.endswith('.zip')):
        bot.send_message(
            message.chat.id,
            "❌ <b>Invalid File Type</b>\n\n"
            "Only <code>.py</code> and <code>.zip</code> files are supported."
        )
        return
    
    file_type = 'zip' if file_name.endswith('.zip') else 'py'
    
    # Check plan limits
    plan = db.get_user_plan(uid)
    limits = Config.PLAN_LIMITS.get(plan, Config.PLAN_LIMITS['FREE'])
    max_size = limits['max_size_mb']
    max_bots = limits[file_type]
    
    # Check file size
    if file_size_mb > max_size:
        bot.send_message(
            message.chat.id,
            f"❌ <b>File Too Large</b>\n\n"
            f"Your plan: <code>{plan}</code>\n"
            f"Max size: <code>{max_size}MB</code>\n"
            f"Your file: <code>{file_size_mb:.2f}MB</code>\n\n"
            f"💎 Upgrade your plan with /plan"
        )
        return
    
    # Check bot count limit
    current_count = process_manager.get_running_count(uid, file_type)
    
    if current_count >= max_bots:
        bot.send_message(
            message.chat.id,
            f"🚫 <b>Limit Reached</b>\n\n"
            f"Plan: <code>{plan}</code>\n"
            f"{file_type.upper()} bots: <code>{current_count}/{max_bots}</code>\n\n"
            f"💡 Stop some bots or upgrade: /plan"
        )
        return
    
    # Show loading animation
    loading_msg = bot.send_message(
        message.chat.id,
        "⏳ <b>Uploading...</b>\n\n"
        "🔥 Please wait while we process your bot..."
    )
    
    try:
        # Create user directory
        user_dir = Config.UPLOAD_DIR / str(uid)
        user_dir.mkdir(exist_ok=True)
        
        # Download file
        file_info = bot.get_file(document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Save file
        file_path = user_dir / file_name
        with open(file_path, 'wb') as f:
            f.write(downloaded_file)
        
        # Delete loading message
        bot.delete_message(message.chat.id, loading_msg.message_id)
        
        # Increment stats
        db.increment_stat('total_uploads')
        Logger.log_user_action(uid, 'upload', f"File: {file_name} ({file_size_mb:.2f}MB)")
        
        # Send success message with controls
        success_text = f"""
✅ <b>Upload Successful!</b> 🔥

📁 <b>File:</b> <code>{file_name}</code>
💾 <b>Size:</b> <code>{file_size_mb:.2f}MB</code>
📊 <b>Type:</b> <code>.{file_type}</code>

🎯 <b>Usage:</b>
<code>{current_count + 1}/{max_bots}</code> {file_type.upper()} bots

🌀 <i>Use controls below to manage</i>
"""
        
        bot.send_message(
            message.chat.id,
            success_text,
            reply_markup=UIComponents.bot_control_keyboard(uid, file_name)
        )
        
        # Log to group
        Logger.log_file_to_group(
            file_path,
            f"📦 <b>Upload</b>\nUser: <code>{uid}</code>\nFile: <code>{file_name}</code>"
        )
    
    except Exception as e:
        bot.delete_message(message.chat.id, loading_msg.message_id)
        bot.send_message(
            message.chat.id,
            f"❌ <b>Upload Failed</b>\n\n<code>{str(e)}</code>"
        )
        Logger.log_to_group(f"❌ Upload failed for {uid}: {str(e)}")

# ══════════════════════════════════════════════════════════════════════════════
# 🎮 BOT CONTROL HANDLERS
# ══════════════════════════════════════════════════════════════════════════════

def start_bot_process(uid: int, bot_name: str, chat_id: int) -> bool:
    """Start a bot process"""
    
    # Check if already running
    if process_manager.is_running(uid, bot_name):
        bot.send_message(
            chat_id,
            "⚠️ <b>Already Running</b>\n\n"
            f"<code>{bot_name}</code> is already active."
        )
        return False
    
    # Get file path
    file_path = Config.UPLOAD_DIR / str(uid) / bot_name
    
    if not file_path.exists():
        bot.send_message(
            chat_id,
            "❌ <b>File Not Found</b>\n\n"
            f"<code>{bot_name}</code> doesn't exist."
        )
        return False
    
    # Show progress
    progress_msg = bot.send_message(
        chat_id,
        "🔥 <b>Starting Bot...</b>\n\n"
        "⚡ Initializing environment...\n"
        "🧬 Installing dependencies...\n"
        "🌀 Launching process..."
    )
    
    try:
        bot_dir = file_path.parent
        
        # Handle ZIP files
        if bot_name.endswith('.zip'):
            extract_dir = bot_dir / bot_name.replace('.zip', '')
            
            # Remove old extraction
            if extract_dir.exists():
                shutil.rmtree(extract_dir)
            
            extract_dir.mkdir(exist_ok=True)
            
            # Extract ZIP
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Find main Python file
            main_file = None
            for candidate in ['bot.py', 'main.py']:
                candidate_path = extract_dir / candidate
                if candidate_path.exists():
                    main_file = candidate_path
                    break
            
            if not main_file:
                # Search recursively
                for py_file in extract_dir.rglob('*.py'):
                    main_file = py_file
                    break
            
            if not main_file:
                bot.delete_message(chat_id, progress_msg.message_id)
                bot.send_message(
                    chat_id,
                    "❌ <b>No Python File Found</b>\n\n"
                    "ZIP must contain a .py file."
                )
                return False
            
            work_dir = extract_dir
            script_path = main_file
        
        else:
            work_dir = bot_dir
            script_path = file_path
        
        # Create virtual environment
        success, venv_python, msg = VirtualEnvironmentManager.setup_bot_environment(work_dir)
        
        if not success:
            bot.delete_message(chat_id, progress_msg.message_id)
            bot.send_message(
                chat_id,
                f"❌ <b>Setup Failed</b>\n\n{msg}"
            )
            return False
        
        # Prepare log file
        log_file_path = work_dir / f"{bot_name}.log"
        log_file = open(log_file_path, 'a', buffering=1)
        
        # Start process
        process = subprocess.Popen(
            [str(venv_python), '-u', str(script_path)],
            cwd=str(work_dir),
            stdout=log_file,
            stderr=log_file,
            text=False
        )
        
        # Wait a moment to check if it started
        time.sleep(2)
        
        if process.poll() is not None:
            bot.delete_message(chat_id, progress_msg.message_id)
            log_file.close()
            bot.send_message(
                chat_id,
                "❌ <b>Start Failed</b>\n\n"
                "Bot crashed immediately. Check logs."
            )
            return False
        
        # Register process
        process_manager.add_process(uid, bot_name, process, log_file)
        db.add_bot_process(uid, bot_name, 'zip' if bot_name.endswith('.zip') else 'py', process.pid)
        
        # Delete progress message
        bot.delete_message(chat_id, progress_msg.message_id)
        
        # Send success message
        file_type = 'zip' if bot_name.endswith('.zip') else 'py'
        current_count = process_manager.get_running_count(uid, file_type)
        plan = db.get_user_plan(uid)
        max_count = Config.PLAN_LIMITS[plan][file_type]
        
        success_text = f"""
✅ <b>Bot Started Successfully!</b> 🔥

🤖 <b>Name:</b> <code>{bot_name}</code>
🆔 <b>PID:</b> <code>{process.pid}</code>
⚡ <b>Status:</b> Running

📊 <b>Usage:</b> <code>{current_count}/{max_count}</code> {file_type.upper()} bots

🌀 <i>Your bot is now live!</i>
"""
        
        bot.send_message(chat_id, success_text)
        
        Logger.log_user_action(uid, 'bot_start', f"{bot_name} (PID: {process.pid})")
        
        return True
    
    except Exception as e:
        bot.delete_message(chat_id, progress_msg.message_id)
        bot.send_message(
            chat_id,
            f"❌ <b>Error</b>\n\n<code>{str(e)}</code>"
        )
        Logger.log_to_group(f"❌ Start error for {uid}/{bot_name}: {str(e)}")
        return False

def stop_bot_process(uid: int, bot_name: str, chat_id: int) -> bool:
    """Stop a bot process"""
    
    if not process_manager.is_running(uid, bot_name):
        bot.send_message(
            chat_id,
            "⚠️ <b>Not Running</b>\n\n"
            f"<code>{bot_name}</code> is not active."
        )
        return False
    
    success = process_manager.stop_process(uid, bot_name)
    
    if success:
        bot.send_message(
            chat_id,
            f"⏸ <b>Bot Stopped</b>\n\n"
            f"🤖 <code>{bot_name}</code>\n\n"
            f"🌀 <i>You can restart it anytime</i>"
        )
        Logger.log_user_action(uid, 'bot_stop', bot_name)
        return True
    else:
        bot.send_message(
            chat_id,
            "❌ <b>Stop Failed</b>\n\n"
            "Unable to stop the bot."
        )
        return False

def delete_bot_files(uid: int, bot_name: str, chat_id: int) -> bool:
    """Delete bot files"""
    
    # Stop if running
    if process_manager.is_running(uid, bot_name):
        process_manager.stop_process(uid, bot_name)
    
    try:
        file_path = Config.UPLOAD_DIR / str(uid) / bot_name
        
        # Delete main file
        if file_path.exists():
            file_path.unlink()
        
        # Delete extracted directory if ZIP
        if bot_name.endswith('.zip'):
            extract_dir = file_path.parent / bot_name.replace('.zip', '')
            if extract_dir.exists():
                shutil.rmtree(extract_dir)
        
        # Delete log file
        log_file = file_path.parent / f"{bot_name}.log"
        if log_file.exists():
            log_file.unlink()
        
        bot.send_message(
            chat_id,
            f"🗑 <b>Deleted</b>\n\n"
            f"<code>{bot_name}</code> and all related files removed."
        )
        
        Logger.log_user_action(uid, 'delete', bot_name)
        return True
    
    except Exception as e:
        bot.send_message(
            chat_id,
            f"❌ <b>Delete Failed</b>\n\n<code>{str(e)}</code>"
        )
        return False

def send_bot_logs(uid: int, bot_name: str, chat_id: int):
    """Send bot logs"""
    
    log_file_path = Config.UPLOAD_DIR / str(uid) / f"{bot_name}.log"
    
    # Also check in extracted directory for ZIP files
    if bot_name.endswith('.zip'):
        extract_dir = Config.UPLOAD_DIR / str(uid) / bot_name.replace('.zip', '')
        alt_log_path = extract_dir / f"{bot_name}.log"
        if alt_log_path.exists():
            log_file_path = alt_log_path
    
    if not log_file_path.exists() or log_file_path.stat().st_size == 0:
        bot.send_message(
            chat_id,
            "📭 <b>No Logs Available</b>\n\n"
            "The bot hasn't generated any logs yet."
        )
        return
    
    try:
        with open(log_file_path, 'rb') as f:
            bot.send_document(
                chat_id,
                f,
                caption=f"📋 <b>Logs:</b> <code>{bot_name}</code>"
            )
    except Exception as e:
        bot.send_message(
            chat_id,
            f"❌ <b>Failed to send logs</b>\n\n<code>{str(e)}</code>"
        )

# ══════════════════════════════════════════════════════════════════════════════
# ⌨️ KEYBOARD BUTTON HANDLERS
# ══════════════════════════════════════════════════════════════════════════════

@bot.message_handler(func=lambda m: m.text == "⚡ ꜱᴛᴀʀᴛ ʙᴏᴛ")
@requires_access
def keyboard_start_bot(message):
    """Handle start bot keyboard button"""
    uid = message.from_user.id
    user_dir = Config.UPLOAD_DIR / str(uid)
    
    if not user_dir.exists():
        bot.send_message(
            message.chat.id,
            "📭 <b>No Bots Found</b>\n\n"
            "Upload a bot first using /upload"
        )
        return
    
    # List all bot files
    bots = [f.name for f in user_dir.iterdir() if f.is_file() and (f.name.endswith('.py') or f.name.endswith('.zip'))]
    
    if not bots:
        bot.send_message(
            message.chat.id,
            "📭 <b>No Bots Found</b>\n\n"
            "Upload a bot first using /upload"
        )
        return
    
    # Create inline keyboard with bot list
    keyboard = InlineKeyboardMarkup()
    for bot_name in bots:
        keyboard.add(
            InlineKeyboardButton(
                f"▶️ {bot_name}",
                callback_data=f"run:{uid}:{bot_name}"
            )
        )
    
    bot.send_message(
        message.chat.id,
        "⚡ <b>Select Bot to Start</b>",
        reply_markup=keyboard
    )

@bot.message_handler(func=lambda m: m.text == "🗑 ᴅᴇʟᴇᴛᴇ")
@requires_access
def keyboard_delete_bot(message):
    """Handle delete keyboard button"""
    uid = message.from_user.id
    user_dir = Config.UPLOAD_DIR / str(uid)
    
    if not user_dir.exists():
        bot.send_message(
            message.chat.id,
            "📭 <b>No Bots Found</b>"
        )
        return
    
    bots = [f.name for f in user_dir.iterdir() if f.is_file() and (f.name.endswith('.py') or f.name.endswith('.zip'))]
    
    if not bots:
        bot.send_message(
            message.chat.id,
            "📭 <b>No Bots Found</b>"
        )
        return
    
    keyboard = InlineKeyboardMarkup()
    for bot_name in bots:
        keyboard.add(
            InlineKeyboardButton(
                f"🗑 {bot_name}",
                callback_data=f"delete:{uid}:{bot_name}"
            )
        )
    
    bot.send_message(
        message.chat.id,
        "🗑 <b>Select Bot to Delete</b>",
        reply_markup=keyboard
    )

@bot.message_handler(func=lambda m: m.text == "📂 ᴍʏ ғɪʟᴇꜱ")
@requires_access
def keyboard_my_files(message):
    """Handle my files keyboard button"""
    cmd_mybots(message)

@bot.message_handler(func=lambda m: m.text == "📊 ꜱʏꜱᴛᴇᴍ ꜱᴛᴀᴛꜱ")
@requires_access
def keyboard_stats(message):
    """Handle stats keyboard button"""
    cmd_stats(message)

@bot.message_handler(func=lambda m: m.text == "💎 ᴠɪᴘ ᴘʟᴀɴꜱ")
@requires_access
def keyboard_vip_plans(message):
    """Handle VIP plans keyboard button"""
    # Show plan carousel starting at index 0
    plan_name = list(Config.PLAN_LIMITS.keys())[0]
    description = UIComponents.get_plan_description(plan_name)
    
    bot.send_message(
        message.chat.id,
        description,
        reply_markup=UIComponents.plan_carousel_keyboard(0)
    )

@bot.message_handler(func=lambda m: m.text == "🆘 ꜱᴜᴘᴘᴏʀᴛ")
@requires_access
def keyboard_support(message):
    """Handle support keyboard button"""
    support_text = f"""
🆘 <b>Support & Help</b>

╔══════════════════════╗
║  🌀 <b>Get Assistance</b>
╠══════════════════════╣
║ 💬 Join our support group
║ 🐉 Ask questions
║ 💡 Get help from community
║ 🔥 Report issues
╚══════════════════════╝

<b>📢 Support Group:</b>
@{Config.FORCE_GROUP}

<b>📣 Updates Channel:</b>
@{Config.FORCE_CHANNEL}

⚜️ <i>We're here to help!</i>
"""
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            "💬 Join Support Group",
            url=f"https://t.me/{Config.FORCE_GROUP}"
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            "📢 Join Channel",
            url=f"https://t.me/{Config.FORCE_CHANNEL}"
        )
    )
    
    bot.send_message(
        message.chat.id,
        support_text,
        reply_markup=keyboard
    )

# ══════════════════════════════════════════════════════════════════════════════
# 📊 INFO COMMANDS
# ══════════════════════════════════════════════════════════════════════════════

@bot.message_handler(commands=['mybots'])
@requires_access
def cmd_mybots(message):
    """List user's bots"""
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

╔═══════════════════════╗
║  📊 <b>Status Overview</b>
╠═══════════════════════╣
║ 💎 Plan: <code>{plan}</code>
║ 📄 .py: <code>{py_running}/{limits['py']}</code>
║ 📦 .zip: <code>{zip_running}/{limits['zip']}</code>
╚═══════════════════════╝

🟢 <b>Running ({len(running_bots)}):</b>
"""
    
    if running_bots:
        for i, bot_name in enumerate(running_bots, 1):
            status_icon = "🔥" if process_manager.is_running(uid, bot_name) else "⚠️"
            text += f"{i}. {status_icon} <code>{bot_name}</code>\n"
    else:
        text += "<i>No running bots</i>\n"
    
    stopped_bots = [b for b in all_bots if b not in running_bots]
    
    if stopped_bots:
        text += f"\n⚪ <b>Stopped ({len(stopped_bots)}):</b>\n"
        for i, bot_name in enumerate(stopped_bots, 1):
            text += f"{i}. ⏸ <code>{bot_name}</code>\n"
    
    text += "\n🌀 <i>Use keyboard buttons to control</i>"
    
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['stats'])
@requires_access
def cmd_stats(message):
    """Show user statistics"""
    uid = message.from_user.id
    plan = db.get_user_plan(uid)
    
    # Get user data
    user_data = db.execute(
        "SELECT joined_at, last_seen FROM users WHERE uid=?",
        (uid,)
    ).fetchone()
    
    if user_data:
        joined_date = datetime.fromtimestamp(user_data['joined_at']).strftime('%Y-%m-%d')
        last_seen = datetime.fromtimestamp(user_data['last_seen']).strftime('%Y-%m-%d %H:%M')
    else:
        joined_date = "Unknown"
        last_seen = "Now"
    
    # Count total bot runs
    total_runs = db.execute(
        "SELECT COUNT(*) as count FROM bot_processes WHERE uid=?",
        (uid,)
    ).fetchone()['count']
    
    # Current usage
    py_running = process_manager.get_running_count(uid, 'py')
    zip_running = process_manager.get_running_count(uid, 'zip')
    
    limits = Config.PLAN_LIMITS[plan]
    
    stats_text = f"""
📊 <b>Your Statistics</b> 🧬

╔═══════════════════════════╗
║  👤 <b>User Info</b>
╠═══════════════════════════╣
║ 🆔 ID: <code>{uid}</code>
║ 💎 Plan: <code>{plan}</code>
║ 📅 Joined: <code>{joined_date}</code>
║ 🕐 Last Seen: <code>{last_seen}</code>
╚═══════════════════════════╝

╔═══════════════════════════╗
║  🤖 <b>Bot Usage</b>
╠═══════════════════════════╣
║ 📄 .py: <code>{py_running}/{limits['py']}</code>
║ 📦 .zip: <code>{zip_running}/{limits['zip']}</code>
║ 🔢 Total Runs: <code>{total_runs}</code>
╚═══════════════════════════╝

╔═══════════════════════════╗
║  💾 <b>Storage</b>
╠═══════════════════════════╣
║ 📊 Max Size: <code>{limits['max_size_mb']}MB</code>
╚═══════════════════════════╝

🌀 <i>Upgrade for more power!</i>
"""
    
    bot.send_message(message.chat.id, stats_text)

@bot.message_handler(commands=['plan'])
@requires_access
def cmd_plan(message):
    """Show all plans"""
    uid = message.from_user.id
    current_plan = db.get_user_plan(uid)
    
    plan_text = f"""
💎 <b>VIP Plans</b> 🔥

<b>Your Current Plan:</b> <code>{current_plan}</code>

╔═════════════════════════════════╗
║  🆓 <b>FREE</b>
├─────────────────────────────────┤
║ 📄 3 .py bots
║ 📦 1 .zip bot
║ 💾 5MB max size
╠═════════════════════════════════╣
║  🥉 <b>BRONZE</b>
├─────────────────────────────────┤
║ 📄 5 .py bots
║ 📦 3 .zip bots
║ 💾 10MB max size
╠═════════════════════════════════╣
║  🥈 <b>SILVER</b>
├─────────────────────────────────┤
║ 📄 10 .py bots
║ 📦 5 .zip bots
║ 💾 25MB max size
╠═════════════════════════════════╣
║  🥇 <b>GOLD</b>
├─────────────────────────────────┤
║ 📄 20 .py bots
║ 📦 10 .zip bots
║ 💾 50MB max size
╠═════════════════════════════════╣
║  🏆 <b>PLATINUM</b>
├─────────────────────────────────┤
║ 📄 50 .py bots
║ 📦 25 .zip bots
║ 💾 100MB max size
╠═════════════════════════════════╣
║  💎 <b>DIAMOND</b>
├─────────────────────────────────┤
║ 📄 ∞ .py bots
║ 📦 ∞ .zip bots
║ 💾 500MB max size
╚═════════════════════════════════╝

🌀 Contact @{Config.FORCE_GROUP} to upgrade!
🎁 Use /redeem for giveaway codes
"""
    
    bot.send_message(message.chat.id, plan_text)

@bot.message_handler(commands=['redeem'])
@requires_access
def cmd_redeem(message):
    """Handle /redeem command"""
    args = message.text.split()
    
    if len(args) < 2:
        bot.send_message(
            message.chat.id,
            "🎁 <b>Redeem Code</b>\n\n"
            "<b>Usage:</b> <code>/redeem CODE</code>\n\n"
            "Enter your premium code to upgrade."
        )
        return
    
    code = args[1].upper()
    uid = message.from_user.id
    
    success, plan, msg = db.redeem_code(code, uid)
    
    if success:
        limits = Config.PLAN_LIMITS[plan]
        
        success_text = f"""
🎉 <b>Code Redeemed!</b> 🔥

💎 <b>New Plan:</b> <code>{plan}</code>

╔═══════════════════════╗
║  🌀 <b>Your Benefits</b>
╠═══════════════════════╣
║ 📄 {limits['py']} .py bots
║ 📦 {limits['zip']} .zip bots
║ 💾 {limits['max_size_mb']}MB max size
╚═══════════════════════╝

🐉 <i>Enjoy your upgrade!</i>
"""
        
        bot.send_message(message.chat.id, success_text)
        Logger.log_user_action(uid, 'redeem', f"Code: {code}, Plan: {plan}")
    else:
        bot.send_message(
            message.chat.id,
            f"❌ <b>Redeem Failed</b>\n\n{msg}"
        )

# ══════════════════════════════════════════════════════════════════════════════
# 👑 ADMIN COMMANDS
# ══════════════════════════════════════════════════════════════════════════════

@bot.message_handler(commands=['admin'])
@owner_only
def cmd_admin(message):
    """Admin panel"""
    total_users = db.get_total_users()
    premium_users = db.get_premium_users()
    banned_count = db.get_banned_count()
    total_starts = db.get_stat('total_starts')
    total_uploads = db.get_stat('total_uploads')
    total_running = len(process_manager.processes)
    
    locked = "🔒 Locked" if db.get_setting('locked') == '1' else "🔓 Unlocked"
    
    admin_text = f"""
👑 <b>Admin Control Panel</b> 🔥

╔═══════════════════════════╗
║  📊 <b>System Stats</b>
╠═══════════════════════════╣
║ 👥 Total Users: <code>{total_users}</code>
║ 💎 Premium: <code>{premium_users}</code>
║ 🚫 Banned: <code>{banned_count}</code>
║ 🤖 Running Bots: <code>{total_running}</code>
║ 🚀 Total Starts: <code>{total_starts}</code>
║ 📦 Total Uploads: <code>{total_uploads}</code>
╚═══════════════════════════╝

🔐 <b>Status:</b> {locked}

🌀 <i>Use admin keyboard for controls</i>
"""
    
    bot.send_message(
        message.chat.id,
        admin_text,
        reply_markup=UIComponents.admin_keyboard()
    )

@bot.message_handler(func=lambda m: m.text == "🏠 ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ")
def keyboard_back_home(message):
    """Back to home keyboard"""
    bot.send_message(
        message.chat.id,
        "🏠 <b>Back to Main Menu</b>",
        reply_markup=UIComponents.main_keyboard()
    )

@bot.message_handler(func=lambda m: m.text == "📢 ʙʀᴏᴀᴅᴄᴀꜱᴛ")
@owner_only
def keyboard_broadcast(message):
    """Broadcast prompt"""
    bot.send_message(
        message.chat.id,
        "📢 <b>Broadcast Message</b>\n\n"
        "Reply to this message with your broadcast text."
    )
    bot.register_next_step_handler(message, process_broadcast)

def process_broadcast(message):
    """Process broadcast message"""
    broadcast_text = message.text
    
    users = db.execute("SELECT uid FROM users").fetchall()
    
    progress_msg = bot.send_message(
        message.chat.id,
        f"📡 <b>Broadcasting...</b>\n\nSending to {len(users)} users..."
    )
    
    success = 0
    failed = 0
    
    for user in users:
        uid = user['uid']
        try:
            bot.send_message(uid, f"📢 <b>Broadcast</b>\n\n{broadcast_text}")
            success += 1
            time.sleep(0.05)  # Rate limiting
        except:
            failed += 1
    
    bot.edit_message_text(
        f"✅ <b>Broadcast Complete</b>\n\n"
        f"📤 Sent: <code>{success}</code>\n"
        f"❌ Failed: <code>{failed}</code>",
        message.chat.id,
        progress_msg.message_id
    )

@bot.message_handler(func=lambda m: m.text == "⛔ ʙᴀɴ")
@owner_only
def keyboard_ban(message):
    """Ban user prompt"""
    bot.send_message(
        message.chat.id,
        "⛔ <b>Ban User</b>\n\n"
        "Reply with: <code>user_id reason</code>"
    )
    bot.register_next_step_handler(message, process_ban)

def process_ban(message):
    """Process ban"""
    try:
        parts = message.text.split(maxsplit=1)
        ban_uid = int(parts[0])
        reason = parts[1] if len(parts) > 1 else "No reason"
        
        db.ban_user(ban_uid, reason, message.from_user.id)
        
        # Stop all bots
        stopped = process_manager.stop_all_user_bots(ban_uid)
        
        bot.send_message(
            message.chat.id,
            f"✅ <b>User Banned</b>\n\n"
            f"🆔 UID: <code>{ban_uid}</code>\n"
            f"📝 Reason: {reason}\n"
            f"🤖 Stopped {stopped} bots"
        )
        
        Logger.log_to_group(
            f"⛔ <b>User Banned</b>\n"
            f"UID: <code>{ban_uid}</code>\n"
            f"Reason: {reason}\n"
            f"By: <code>{message.from_user.id}</code>"
        )
    
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"❌ <b>Error</b>\n\n<code>{str(e)}</code>"
        )

@bot.message_handler(func=lambda m: m.text == "🔓 ᴜɴʙᴀɴ")
@owner_only
def keyboard_unban(message):
    """Unban user prompt"""
    bot.send_message(
        message.chat.id,
        "🔓 <b>Unban User</b>\n\n"
        "Reply with user ID"
    )
    bot.register_next_step_handler(message, process_unban)

def process_unban(message):
    """Process unban"""
    try:
        unban_uid = int(message.text.strip())
        db.unban_user(unban_uid)
        
        bot.send_message(
            message.chat.id,
            f"✅ <b>User Unbanned</b>\n\n"
            f"🆔 UID: <code>{unban_uid}</code>"
        )
        
        Logger.log_to_group(f"🔓 User <code>{unban_uid}</code> unbanned")
    
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"❌ <b>Error</b>\n\n<code>{str(e)}</code>"
        )

@bot.message_handler(func=lambda m: m.text == "💎 ᴀᴅᴅ ᴘʀᴇᴍɪᴜᴍ")
@owner_only
def keyboard_add_premium(message):
    """Add premium prompt"""
    plans = ', '.join(Config.PLAN_LIMITS.keys())
    
    bot.send_message(
        message.chat.id,
        f"💎 <b>Add Premium</b>\n\n"
        f"Reply with: <code>user_id PLAN</code>\n\n"
        f"Available plans:\n<code>{plans}</code>"
    )
    bot.register_next_step_handler(message, process_add_premium)

def process_add_premium(message):
    """Process add premium"""
    try:
        parts = message.text.split()
        prem_uid = int(parts[0])
        plan = parts[1].upper()
        
        if plan not in Config.PLAN_LIMITS:
            bot.send_message(
                message.chat.id,
                f"❌ Invalid plan. Choose from: {', '.join(Config.PLAN_LIMITS.keys())}"
            )
            return
        
        db.set_user_plan(prem_uid, plan)
        
        limits = Config.PLAN_LIMITS[plan]
        
        bot.send_message(
            message.chat.id,
            f"✅ <b>Premium Added</b>\n\n"
            f"👤 UID: <code>{prem_uid}</code>\n"
            f"💎 Plan: <code>{plan}</code>\n"
            f"📄 .py: {limits['py']}\n"
            f"📦 .zip: {limits['zip']}"
        )
        
        # Notify user
        try:
            bot.send_message(
                prem_uid,
                f"🎉 <b>Congratulations!</b> 🔥\n\n"
                f"You've been upgraded to <b>{plan}</b> plan!\n\n"
                f"📄 .py bots: {limits['py']}\n"
                f"📦 .zip bots: {limits['zip']}\n"
                f"💾 Max size: {limits['max_size_mb']}MB"
            )
        except:
            pass
        
        Logger.log_to_group(
            f"💎 Premium added\n"
            f"UID: <code>{prem_uid}</code>\n"
            f"Plan: {plan}"
        )
    
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"❌ <b>Error</b>\n\n<code>{str(e)}</code>"
        )

@bot.message_handler(func=lambda m: m.text == "🎁 ɢᴇɴ ᴄᴏᴅᴇ")
@owner_only
def keyboard_gen_code(message):
    """Generate code prompt"""
    plans = ', '.join(Config.PLAN_LIMITS.keys())
    
    bot.send_message(
        message.chat.id,
        f"🎁 <b>Generate Code</b>\n\n"
        f"Reply with plan name:\n<code>{plans}</code>"
    )
    bot.register_next_step_handler(message, process_gen_code)

def process_gen_code(message):
    """Process generate code"""
    try:
        plan = message.text.upper().strip()
        
        if plan not in Config.PLAN_LIMITS:
            bot.send_message(
                message.chat.id,
                f"❌ Invalid plan. Choose from: {', '.join(Config.PLAN_LIMITS.keys())}"
            )
            return
        
        # Generate unique code
        code = f"FIRE{random.randint(1000, 9999)}{random.choice(string.ascii_uppercase)}"
        
        db.create_giveaway_code(code, plan, message.from_user.id)
        
        bot.send_message(
            message.chat.id,
            f"🎁 <b>Code Generated</b>\n\n"
            f"📋 Code: <code>{code}</code>\n"
            f"💎 Plan: <code>{plan}</code>\n\n"
            f"🌀 Share with users to redeem"
        )
        
        Logger.log_to_group(
            f"🎁 Code generated\n"
            f"Code: <code>{code}</code>\n"
            f"Plan: {plan}"
        )
    
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"❌ <b>Error</b>\n\n<code>{str(e)}</code>"
        )

@bot.message_handler(func=lambda m: m.text == "🔒 ʟᴏᴄᴋ")
@owner_only
def keyboard_lock(message):
    """Lock bot"""
    db.set_setting('locked', '1')
    bot.send_message(
        message.chat.id,
        "🔒 <b>Bot Locked</b>\n\nOnly owner can use the bot now."
    )
    Logger.log_to_group("🔒 Bot locked")

@bot.message_handler(func=lambda m: m.text == "🔓 ᴜɴʟᴏᴄᴋ")
@owner_only
def keyboard_unlock(message):
    """Unlock bot"""
    db.set_setting('locked', '0')
    bot.send_message(
        message.chat.id,
        "🔓 <b>Bot Unlocked</b>\n\nAll users can use the bot again."
    )
    Logger.log_to_group("🔓 Bot unlocked")

@bot.message_handler(func=lambda m: m.text == "👥 ᴜꜱᴇʀꜱ")
@owner_only
def keyboard_users(message):
    """Show user statistics"""
    total = db.get_total_users()
    premium = db.get_premium_users()
    banned = db.get_banned_count()
    
    # Get recent users
    recent = db.execute(
        "SELECT uid, username, joined_at FROM users ORDER BY joined_at DESC LIMIT 10"
    ).fetchall()
    
    text = f"""
👥 <b>User Statistics</b>

╔═══════════════════════╗
║  📊 <b>Overview</b>
╠═══════════════════════╣
║ 👤 Total: <code>{total}</code>
║ 💎 Premium: <code>{premium}</code>
║ 🚫 Banned: <code>{banned}</code>
╚═══════════════════════╝

📅 <b>Recent Users:</b>
"""
    
    for user in recent:
        joined = datetime.fromtimestamp(user['joined_at']).strftime('%m/%d')
        username = f"@{user['username']}" if user['username'] else "No username"
        text += f"• {joined} - <code>{user['uid']}</code> ({username})\n"
    
    bot.send_message(message.chat.id, text)

# ══════════════════════════════════════════════════════════════════════════════
# 🎛️ CALLBACK QUERY HANDLERS
# ══════════════════════════════════════════════════════════════════════════════

@bot.callback_query_handler(func=lambda c: c.data.startswith('run:'))
def callback_run_bot(call):
    """Handle run bot callback"""
    try:
        bot.answer_callback_query(call.id)
    except:
        pass
    
    _, uid_str, bot_name = call.data.split(':', 2)
    uid = int(uid_str)
    
    # Verify ownership
    if call.from_user.id != uid and call.from_user.id != Config.OWNER_ID:
        bot.answer_callback_query(call.id, "❌ Not your bot!", show_alert=True)
        return
    
    start_bot_process(uid, bot_name, call.message.chat.id)

@bot.callback_query_handler(func=lambda c: c.data.startswith('stop:'))
def callback_stop_bot(call):
    """Handle stop bot callback"""
    try:
        bot.answer_callback_query(call.id)
    except:
        pass
    
    _, uid_str, bot_name = call.data.split(':', 2)
    uid = int(uid_str)
    
    if call.from_user.id != uid and call.from_user.id != Config.OWNER_ID:
        bot.answer_callback_query(call.id, "❌ Not your bot!", show_alert=True)
        return
    
    stop_bot_process(uid, bot_name, call.message.chat.id)

@bot.callback_query_handler(func=lambda c: c.data.startswith('delete:'))
def callback_delete_bot(call):
    """Handle delete bot callback"""
    try:
        bot.answer_callback_query(call.id)
    except:
        pass
    
    _, uid_str, bot_name = call.data.split(':', 2)
    uid = int(uid_str)
    
    if call.from_user.id != uid and call.from_user.id != Config.OWNER_ID:
        bot.answer_callback_query(call.id, "❌ Not your bot!", show_alert=True)
        return
    
    # Confirmation keyboard
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton(
            "✅ Yes, Delete",
            callback_data=f"confirm_delete:{uid}:{bot_name}"
        ),
        InlineKeyboardButton(
            "❌ Cancel",
            callback_data="close_msg"
        )
    )
    
    bot.edit_message_text(
        f"⚠️ <b>Confirm Deletion</b>\n\n"
        f"Delete <code>{bot_name}</code>?\n\n"
        f"This action cannot be undone.",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith('confirm_delete:'))
def callback_confirm_delete(call):
    """Handle confirmed deletion"""
    try:
        bot.answer_callback_query(call.id)
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
    """Handle logs callback"""
    try:
        bot.answer_callback_query(call.id)
    except:
        pass
    
    _, uid_str, bot_name = call.data.split(':', 2)
    uid = int(uid_str)
    
    if call.from_user.id != uid and call.from_user.id != Config.OWNER_ID:
        bot.answer_callback_query(call.id, "❌ Not your bot!", show_alert=True)
        return
    
    send_bot_logs(uid, bot_name, call.message.chat.id)

@bot.callback_query_handler(func=lambda c: c.data.startswith('plan_nav:'))
def callback_plan_nav(call):
    """Handle plan carousel navigation"""
    try:
        bot.answer_callback_query(call.id)
    except:
        pass
    
    index = int(call.data.split(':')[1])
    plan_name = list(Config.PLAN_LIMITS.keys())[index]
    description = UIComponents.get_plan_description(plan_name)
    
    try:
        bot.edit_message_text(
            description,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=UIComponents.plan_carousel_keyboard(index)
        )
    except:
        pass

@bot.callback_query_handler(func=lambda c: c.data == 'check_membership')
def callback_check_membership(call):
    """Handle membership check callback"""
    try:
        bot.answer_callback_query(call.id)
    except:
        pass
    
    uid = call.from_user.id
    
    if AccessControl.is_member(bot, uid):
        first_name = call.from_user.first_name or "User"
        
        welcome_text = f"""
🔥 <b>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴀꜱᴛʀᴏɴɪx ғɪʀᴇ ᴇᴅɪᴛɪᴏɴ</b> 🔥

👋 ʜᴇʏ <b>{first_name}</b>! ⛩️

╔═══════════════════════╗
║  🐉 <b>ᴘᴏᴡᴇʀ ғᴇᴀᴛᴜʀᴇꜱ</b> 🐉  
╠═══════════════════════╣
║ ⚡ ɪɴꜱᴛᴀɴᴛ ʙᴏᴛ ʜᴏꜱᴛɪɴɢ
║ 🧬 ꜱᴍᴀʀᴛ ᴅᴇᴘᴇɴᴅᴇɴᴄʏ ᴍɢᴍᴛ
║ 🔱 ɪꜱᴏʟᴀᴛᴇᴅ ᴠɪʀᴛᴜᴀʟ ᴇɴᴠꜱ
║ 💠 .ᴘʏ & .ᴢɪᴘ ꜱᴜᴘᴘᴏʀᴛ
║ 🌀 ʀᴇᴀʟ-ᴛɪᴍᴇ ᴘʀᴏᴄᴇꜱꜱ ᴄᴏɴᴛʀᴏʟ
║ 🧿 ᴄʏʙᴇʀᴘᴜɴᴋ ᴜɪ
╚═══════════════════════╝

💎 <b>ʏᴏᴜʀ ᴘʟᴀɴ:</b> <code>{db.get_user_plan(uid)}</code>

🆘 <b>ɴᴇᴇᴅ ʜᴇʟᴘ?</b> /help

⚜️ <i>ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴀꜱᴛʀᴏɴɪx ᴇɴᴛᴇʀᴘʀɪꜱᴇ</i> ⚜️
"""
        
        try:
            bot.edit_message_caption(
                caption=welcome_text,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=None
            )
        except:
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except:
                pass
            
            bot.send_message(
                call.message.chat.id,
                welcome_text,
                reply_markup=UIComponents.main_keyboard()
            )
    else:
        bot.answer_callback_query(
            call.id,
            "❌ Please join both channel and group first!",
            show_alert=True
        )

@bot.callback_query_handler(func=lambda c: c.data == 'close_msg')
def callback_close(call):
    """Handle close message callback"""
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

# ══════════════════════════════════════════════════════════════════════════════
# 🧹 CLEANUP & SHUTDOWN
# ══════════════════════════════════════════════════════════════════════════════

def cleanup_on_exit():
    """Cleanup function called on exit"""
    print("\n🔥 Initiating shutdown sequence...")
    
    # Stop all processes
    print("⏸  Stopping all bot processes...")
    process_manager.cleanup_all()
    
    # Close database
    print("💾 Closing database...")
    try:
        db.close()
    except:
        pass
    
    print("✅ Cleanup complete. Goodbye! 🔥")

# Register cleanup
atexit.register(cleanup_on_exit)

# Handle SIGTERM
def signal_handler(sig, frame):
    print("\n⚠️  Received shutdown signal")
    cleanup_on_exit()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# ══════════════════════════════════════════════════════════════════════════════
# 🚀 MAIN ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "═" * 80)
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                              ║")
    print("║             🔥 ASTRONIX FIRE EDITION v3.0 ULTIMATE 🔥                        ║")
    print("║                                                                              ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print("═" * 80)
    
    try:
        bot_info = bot.get_me()
        print(f"\n🤖 Bot Username: @{bot_info.username}")
        print(f"🆔 Bot ID: {bot_info.id}")
    except Exception as e:
        print(f"\n❌ Failed to get bot info: {e}")
        sys.exit(1)
    
    print(f"\n💾 Database: {Config.DB_PATH}")
    print(f"📁 Upload Directory: {Config.UPLOAD_DIR}")
    print(f"👑 Owner ID: {Config.OWNER_ID}")
    print(f"📊 Logs Group: {Config.LOGS_GROUP_ID}")
    
    print("\n" + "═" * 80)
    print("✅ All systems operational")
    print("🔥 Bot is now running...")
    print("⚡ Press Ctrl+C to stop")
    print("═" * 80 + "\n")
    
    # Log startup
    Logger.log_to_group(
        f"🔥 <b>ASTRONIX FIRE EDITION STARTED</b>\n\n"
        f"🤖 Bot: @{bot_info.username}\n"
        f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"🌀 Status: ✅ Online"
    )
    
    # Start polling
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except KeyboardInterrupt:
        print("\n⚠️  Keyboard interrupt detected")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        Logger.log_to_group(f"❌ <b>BOT CRASHED</b>\n\n<code>{str(e)}</code>")
    finally:
        cleanup_on_exit()
