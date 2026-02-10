# 🚀 QUICK START GUIDE - ASTRONIX FIRE EDITION

Get your bot running in 5 minutes!

## ⚡ FASTEST SETUP (3 Steps)

### Step 1: Install Dependencies
```bash
pip install pyTelegramBotAPI psutil
```

### Step 2: Set Environment Variables

**Linux/Mac:**
```bash
export BOT_TOKEN="your_bot_token_from_botfather"
export OWNER_ID="your_telegram_user_id"
```

**Windows:**
```cmd
set BOT_TOKEN=your_bot_token_from_botfather
set OWNER_ID=your_telegram_user_id
```

### Step 3: Run
```bash
python astronix_fire_edition.py
```

✅ **Done!** Your bot is now live!

---

## 🎯 GET YOUR CREDENTIALS

### 1. Bot Token
1. Open Telegram
2. Message [@BotFather](https://t.me/BotFather)
3. Send `/newbot`
4. Follow instructions
5. Copy your token (looks like: `1234567890:ABCdefGHI...`)

### 2. Owner ID
1. Open Telegram
2. Message [@userinfobot](https://t.me/userinfobot)
3. Your ID will be shown (looks like: `123456789`)

### 3. Logs Group ID (Optional but recommended)
1. Create a new Telegram group
2. Add your bot to the group
3. Make bot an admin
4. Message [@myidbot](https://t.me/myidbot) in the group
5. It will show the group ID (negative number like: `-1001234567890`)

---

## 🔥 USING .ENV FILE (Recommended)

### Step 1: Install python-dotenv
```bash
pip install python-dotenv
```

### Step 2: Create .env file
Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

Edit `.env`:
```
BOT_TOKEN=1234567890:ABCdefGHI...
OWNER_ID=123456789
LOGS_GROUP_ID=-1001234567890
FORCE_CHANNEL=YourChannel
FORCE_GROUP=YourGroup
```

### Step 3: Update bot code
Add these lines at the top of `astronix_fire_edition.py` (after the imports):

```python
from dotenv import load_dotenv
load_dotenv()
```

### Step 4: Run
```bash
python astronix_fire_edition.py
```

---

## 📋 CHECKLIST

Before running, make sure you have:

- [ ] Python 3.10 or higher installed
- [ ] Bot token from @BotFather
- [ ] Your Telegram user ID
- [ ] Installed dependencies (`pip install -r requirements.txt`)
- [ ] Set BOT_TOKEN environment variable
- [ ] Set OWNER_ID environment variable
- [ ] (Optional) Created logs group and set LOGS_GROUP_ID
- [ ] (Optional) Created channel/group for force join

---

## 🧪 TEST YOUR BOT

1. Start the bot: `python astronix_fire_edition.py`
2. Look for this output:
   ```
   ✅ All systems operational
   🔥 Bot is now running...
   ```
3. Open Telegram and message your bot with `/start`
4. You should see the fire animation! 🔥

---

## 🎨 FIRST COMMANDS TO TRY

1. `/start` - See the fire animation
2. `/help` - View all commands
3. `/admin` - Access admin panel (owner only)
4. Upload a simple bot.py file to test
5. Click "⚡ ꜱᴛᴀʀᴛ ʙᴏᴛ" to run it

---

## 🐛 TROUBLESHOOTING

### Bot doesn't start
- **Check:** Is BOT_TOKEN correct?
- **Check:** Is Python 3.10+ installed? (`python --version`)
- **Check:** Are dependencies installed? (`pip list | grep telegram`)

### Can't find bot on Telegram
- **Check:** Did you create it with @BotFather?
- **Check:** Is the bot token valid?
- **Try:** Search by exact username

### "Owner only" errors
- **Check:** Is OWNER_ID set to your ID (not bot ID)?
- **Check:** Did you get ID from @userinfobot?
- **Try:** Print your ID in code to verify

### Fire animation doesn't show
- **Normal:** First message might be slow
- **Try:** Send `/start` again
- **Check:** Internet connection

---

## 💡 TIPS

1. **Run in background:**
   ```bash
   nohup python astronix_fire_edition.py > bot.log 2>&1 &
   ```

2. **Auto-restart on crash:**
   ```bash
   while true; do python astronix_fire_edition.py; sleep 5; done
   ```

3. **View logs:**
   ```bash
   tail -f bot.log
   ```

4. **Stop bot:**
   ```bash
   pkill -f astronix_fire_edition.py
   ```

---

## 🚀 NEXT STEPS

Once your bot is running:

1. **Set up Force Join** (channel/group)
2. **Configure custom images** (START_PIC, etc.)
3. **Create premium plans** with `/gen CODE`
4. **Test bot hosting** by uploading a simple bot
5. **Share with users!**

---

## 📞 NEED HELP?

- **Check:** README.md for full documentation
- **Read:** Error messages carefully
- **Test:** Each component separately
- **Ask:** In your support group

---

## 🔥 YOU'RE READY!

Your Astronix Fire Edition bot is ready to host unlimited bots!

**Happy Hosting! 🚀**

---

*Made with 🔥 by Astronix Enterprise*
