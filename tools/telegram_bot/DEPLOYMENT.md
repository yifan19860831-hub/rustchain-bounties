# RustChain Telegram Bot - Deployment Guide

Quick deployment options for the RustChain Telegram Bot.

---

## 🐳 Docker Deployment (Recommended)

### Prerequisites
- Docker and Docker Compose installed
- Telegram Bot Token from @BotFather

### Quick Start

```bash
# 1. Clone and navigate to the bot directory
cd tools/telegram_bot

# 2. Set your bot token
export BOT_TOKEN="your_bot_token_here"

# 3. Build and run
docker-compose up -d

# 4. Check logs
docker-compose logs -f
```

### Build Custom Image

```bash
docker build -t rustchain-telegram-bot .
docker run -d -e BOT_TOKEN=your_token_here --name rustchain-bot rustchain-telegram-bot
```

---

## 🔧 Systemd Service (Linux)

### Setup

```bash
# 1. Copy service file
sudo cp rustchain-bot.service /etc/systemd/system/

# 2. Edit paths in service file
sudo nano /etc/systemd/system/rustchain-bot.service
# Update:
#   - User=youruser
#   - WorkingDirectory=/actual/path/to/telegram_bot
#   - ExecStart=/usr/bin/python3 /actual/path/to/telegram_bot/bot.py

# 3. Enable and start
sudo systemctl daemon-reload
sudo systemctl enable rustchain-bot
sudo systemctl start rustchain-bot

# 4. Check status
sudo systemctl status rustchain-bot
```

### Logs

```bash
# View logs
journalctl -u rustchain-bot -f

# Recent errors
journalctl -u rustchain-bot -p err -n 50
```

---

## 🖥️ Manual Installation

### Requirements
- Python 3.11+
- pip

### Steps

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Edit bot.py and set BOT_TOKEN
nano bot.py
# Replace: BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
# With your actual token

# 3. Run the bot
python bot.py
```

### Run in Background

```bash
# Using nohup
nohup python bot.py > bot.log 2>&1 &

# Using screen
screen -S rustchain-bot
python bot.py
# Ctrl+A, D to detach
```

---

## 🔍 Troubleshooting

### Bot doesn't start
```bash
# Check Python version
python --version  # Should be 3.11+

# Check dependencies
pip install -r requirements.txt --upgrade
```

### Connection errors
- Verify internet connectivity
- Check if RustChain API is accessible: `curl https://rustchain.org/health`
- Ensure bot token is valid

### Docker issues
```bash
# Rebuild image
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Check logs
docker-compose logs rustchain-bot
```

---

## 📊 Monitoring

### Health Check

```bash
# Test bot is running
docker-compose ps

# Check API connectivity
curl https://rustchain.org/health
```

### Logs Location

- **Docker**: `docker-compose logs -f`
- **Systemd**: `journalctl -u rustchain-bot -f`
- **Manual**: Check `bot.log` or console output

---

## 🔐 Security Best Practices

1. **Never commit bot token** to version control
2. Use environment variables for sensitive data
3. Keep dependencies updated: `pip install --upgrade -r requirements.txt`
4. Run with minimal privileges (systemd service hardening included)
5. Monitor logs for suspicious activity

---

## 📝 Support

For issues or feature requests:
- GitHub Issues: https://github.com/Scottcjn/rustchain-bounties/issues
- RustChain Docs: https://rustchain.org

---

**Version**: 1.0.0  
**Last Updated**: 2026-03-13
