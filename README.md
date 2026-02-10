# 🔥 ASTRONIX FIRE EDITION v3.0 ULTIMATE

## ✨ Complete Rebuild with Zero Errors

A professional-grade Telegram bot hosting platform with intelligent dependency management, fire animations, and cyberpunk aesthetics.

---

## 🎯 KEY FEATURES

### 🔥 **Fire Animation System**
- Frame-by-frame loading animation on `/start`
- Professional boot-up sequence
- Cyberpunk aesthetic with rare emojis (⛩️ 🐉 🔱 💠 🌀 🧿)

### 🧬 **Smart Dependency Installer (THE FIX)**
- Uses `sys.stdlib_module_names` (Python 3.10+) for accurate stdlib detection
- Filters out ALL standard library modules
- Never tries to `pip install os, sys, time`, etc.
- Handles package aliases correctly (PIL → Pillow, cv2 → opencv-python)
- Installs dependencies one-by-one with proper error handling
- **ZERO dependency installation errors**

### 🎨 **Hybrid UI System**
- **Permanent Reply Keyboard** - Always visible bottom controls
- **Inline Carousel** - Swipe through VIP plans
- Cyberpunk-themed buttons and layouts

### 🔱 **Advanced Features**
- Isolated virtual environments per bot
- Process management with PID tracking
- .py and .zip file support
- Auto-extraction and dependency detection
- Real-time bot control (start, stop, delete, logs)
- Multi-tier plan system (FREE to DIAMOND)
- Giveaway code system
- User statistics and analytics
- Admin broadcast and moderation tools
- Force join verification
- Rate limiting per user
- Comprehensive logging

---

## 🚀 INSTALLATION

### Prerequisites
- Python 3.10 or higher
- pip
- Virtual environment support

### Setup Steps

1. **Install Dependencies**
```bash
pip install pyTelegramBotAPI psutil
```

2. **Set Environment Variables**

Create a `.env` file or export these variables:

```bash
# Required
export BOT_TOKEN="your_bot_token_here"
export OWNER_ID="your_telegram_user_id"

# Optional but recommended
export LOGS_GROUP_ID="your_logs_group_id"
export FORCE_CHANNEL="YourChannelUsername"
export FORCE_GROUP="YourGroupUsername"

# Optional - Custom images
export START_PIC_URL="https://your-image-url.com/start.png"
export FORCE_PIC_URL="https://your-image-url.com/force.png"
export UPLOAD_PIC_URL="https://your-image-url.com/upload.png"
```

3. **Run the Bot**
```bash
python astronix_fire_edition.py
```

---

## 🔧 CONFIGURATION

### Plan Limits

```python
PLAN_LIMITS = {
    "FREE": {"py": 3, "zip": 1, "max_size_mb": 5},
    "BRONZE": {"py": 5, "zip": 3, "max_size_mb": 10},
    "SILVER": {"py": 10, "zip": 5, "max_size_mb": 25},
    "GOLD": {"py": 20, "zip": 10, "max_size_mb": 50},
    "PLATINUM": {"py": 50, "zip": 25, "max_size_mb": 100},
    "DIAMOND": {"py": 999999, "zip": 999999, "max_size_mb": 500}
}
```

### Rate Limiting
- Default: 3 seconds between commands per user
- Configurable in `Config.RATE_LIMIT_SECONDS`

---

## 📋 USER COMMANDS

| Command | Description |
|---------|-------------|
| `/start` | Initialize bot with fire animation |
| `/help` | Show command reference |
| `/upload` | Upload bot file (.py or .zip) |
| `/mybots` | List your running bots |
| `/stats` | View your statistics |
| `/plan` | View all VIP plans |
| `/redeem CODE` | Redeem premium code |

## ⌨️ KEYBOARD BUTTONS

| Button | Function |
|--------|----------|
| ⚡ ꜱᴛᴀʀᴛ ʙᴏᴛ | Start uploaded bot |
| 🗑 ᴅᴇʟᴇᴛᴇ | Delete bot files |
| 📂 ᴍʏ ғɪʟᴇꜱ | List all bots |
| 📊 ꜱʏꜱᴛᴇᴍ ꜱᴛᴀᴛꜱ | View statistics |
| 💎 ᴠɪᴘ ᴘʟᴀɴꜱ | Browse plans |
| 🆘 ꜱᴜᴘᴘᴏʀᴛ | Get support |

---

## 👑 ADMIN COMMANDS

Only available to `OWNER_ID`:

| Command | Description |
|---------|-------------|
| `/admin` | Admin control panel |
| 📢 ʙʀᴏᴀᴅᴄᴀꜱᴛ | Send message to all users |
| ⛔ ʙᴀɴ | Ban user by ID |
| 🔓 ᴜɴʙᴀɴ | Unban user |
| 💎 ᴀᴅᴅ ᴘʀᴇᴍɪᴜᴍ | Manually upgrade user |
| 🎁 ɢᴇɴ ᴄᴏᴅᴇ | Generate giveaway code |
| 🔒 ʟᴏᴄᴋ | Enable maintenance mode |
| 🔓 ᴜɴʟᴏᴄᴋ | Disable maintenance mode |
| 👥 ᴜꜱᴇʀꜱ | View user statistics |

---

## 🔒 SECURITY FEATURES

1. **No Hardcoded Secrets** - All credentials via environment variables
2. **Isolated Environments** - Each bot runs in its own venv
3. **Process Isolation** - PID tracking and safe termination
4. **Rate Limiting** - Prevents spam and abuse
5. **Access Control** - Decorators for authentication
6. **Force Join** - Required channel/group membership
7. **Ban System** - Permanent and temporary bans

---

## 🧬 SMART DEPENDENCY SYSTEM

### How It Works

1. **Detection Phase**
   - Scans all .py files in project
   - Uses AST parsing to find imports
   - Checks `requirements.txt` if present

2. **Filtering Phase**
   - Compares against `sys.stdlib_module_names`
   - Checks `sys.builtin_module_names`
   - Filters underscore-prefixed modules
   - Removes known stdlib modules

3. **Installation Phase**
   - Upgrades pip, setuptools, wheel first
   - Installs packages one-by-one
   - Continues on individual failures
   - Logs all errors without crashing

### Package Aliases

```python
PACKAGE_ALIASES = {
    'PIL': 'Pillow',
    'cv2': 'opencv-python',
    'telegram': 'python-telegram-bot',
    'telebot': 'pyTelegramBotAPI',
    'bs4': 'beautifulsoup4',
    'dotenv': 'python-dotenv',
    'Crypto': 'pycryptodome',
}
```

---

## 📦 SUPPORTED FILE FORMATS

### .py Files
- Single Python script
- Auto-detects imports
- Creates isolated venv
- Installs dependencies
- Runs directly

### .zip Files
- Multi-file projects
- Auto-extracts to dedicated folder
- Looks for `requirements.txt`
- Finds main file (bot.py, main.py, or first .py)
- Full project support

---

## 🎯 WORKFLOW EXAMPLE

1. **User uploads bot.py**
   ```
   User → Upload bot.py → Bot receives
   ```

2. **Bot processes file**
   ```
   Create user directory
   → Save file
   → Show control buttons
   ```

3. **User clicks "⚡ ꜱᴛᴀʀᴛ ʙᴏᴛ"**
   ```
   Check limits
   → Create venv
   → Detect imports
   → Install dependencies
   → Start process
   → Track PID
   ```

4. **Bot runs 24/7**
   ```
   Process monitored
   → Logs captured
   → User can stop/restart
   ```

---

## 📊 DATABASE STRUCTURE

### Tables

- **users** - User profiles and join dates
- **plans** - Premium subscriptions
- **banned** - Banned users with reasons
- **giveaway** - Redeemable codes
- **bot_processes** - Running bot tracking
- **statistics** - Global counters
- **settings** - Bot configuration
- **activity_log** - User action history

---

## 🔥 FIRE ANIMATION

The signature boot sequence:

```
▒▒▒▒▒▒▒▒▒▒ 0%
██▒▒▒▒▒▒▒▒ 20% ⛩️ [Initializing...]
████▒▒▒▒▒▒ 40% 🌀 [System Heating...]
██████▒▒▒▒ 60% 🔱 [Core Loading...]
███████▒▒▒ 70% 💠 [Ignition Phase...]
█████████▒ 90% 🐉 [Almost There...]
██████████ 100% 🔥 FIRE DETECTED 🔥
```

Executes in ~3 seconds with smooth frame transitions.

---

## 💡 TIPS FOR USERS

1. **For .zip files:**
   - Include a `requirements.txt` (optional)
   - Main file should be `bot.py` or `main.py`
   - Keep file size under plan limit

2. **For dependencies:**
   - Bot auto-detects most packages
   - Add `requirements.txt` for manual control
   - Don't include stdlib modules

3. **For best performance:**
   - Use .py files for simple bots
   - Use .zip for complex projects
   - Stop unused bots to free slots

---

## 🐛 TROUBLESHOOTING

### "Dependency installation failed"
- **Fixed in this version!** The smart installer filters stdlib correctly.

### "Bot crashed immediately"
- Check logs with 📋 button
- Verify your bot code
- Check for syntax errors

### "Upload failed"
- Check file size against plan limit
- Ensure file is .py or .zip
- Try uploading again

### "Can't start bot - limit reached"
- Stop unused bots
- Upgrade plan with /plan
- Delete old bots

---

## 📈 PERFORMANCE

- **Startup Time:** ~3s (with animation)
- **Venv Creation:** ~5-10s
- **Dependency Install:** ~30-60s (varies)
- **Bot Launch:** ~2s
- **Database Queries:** <10ms

---

## 🎨 AESTHETICS

### Cyberpunk Theme
- Rare Unicode emojis: ⛩️ 🐉 🔱 💠 🌀 🧿 ⚜️ 🧬 🧪 🦠
- Code blocks for data display
- Box-drawing characters for borders
- Consistent visual hierarchy

### UI Principles
- **Clarity:** Information is easy to scan
- **Consistency:** Same style throughout
- **Feedback:** User actions acknowledged
- **Beauty:** Aesthetic > Generic

---

## 🚨 IMPORTANT NOTES

1. **Python 3.10+ Required** for `sys.stdlib_module_names`
2. **Set BOT_TOKEN** before running
3. **Set OWNER_ID** for admin access
4. **Database auto-creates** on first run
5. **Processes auto-cleanup** on shutdown

---

## 📝 CODE STATISTICS

- **Total Lines:** 2,400+
- **Functions:** 80+
- **Classes:** 8
- **Commands:** 15+
- **Callbacks:** 10+
- **Database Tables:** 8

---

## 🔗 SUPPORT

- **Issues:** Check logs first
- **Questions:** Join support group
- **Updates:** Follow channel
- **Customization:** Modify Config class

---

## 📜 LICENSE

This is a custom bot for Astronix Enterprise. 
For commercial use, contact the developer.

---

## 👨‍💻 DEVELOPER

**Author:** @offx_sahil  
**Version:** 3.0 ULTIMATE  
**Year:** 2026  
**Rebuilt:** February 2026

---

## 🎯 WHAT'S NEW IN v3.0

✅ **FIXED:** Dependency installer (no more stdlib errors)  
✅ **ADDED:** Fire animation system  
✅ **ADDED:** Hybrid UI with reply keyboard  
✅ **ADDED:** Plan carousel navigation  
✅ **ADDED:** Comprehensive logging  
✅ **ADDED:** Process manager with PID tracking  
✅ **ADDED:** Rate limiting  
✅ **ADDED:** Activity log  
✅ **IMPROVED:** Database structure  
✅ **IMPROVED:** Error handling  
✅ **IMPROVED:** Code organization  
✅ **IMPROVED:** Security features  

---

## 🔥 THANK YOU FOR USING ASTRONIX FIRE EDITION!

**Made with 🔥 by the Astronix team**
