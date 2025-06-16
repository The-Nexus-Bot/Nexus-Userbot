# 🌟 Nexus Telegram Userbot v2.0

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0+-green.svg)](https://docs.pyrogram.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Heroku%20%7C%20Render%20%7C%20Railway%20%7C%20Koyeb-purple.svg)]()

A sophisticated hybrid Telegram userbot system featuring both personal automation and public assistant bot capabilities. Built with advanced plugin architecture, real-time monitoring, and comprehensive security features.

## ✨ Key Features

### 🤖 Hybrid Bot Architecture
- **Personal Userbot** - Private automation with 24+ built-in commands
- **Assistant Bot** - Public bot with commands, inline mode, and auto-profile management
- **Seamless Integration** - Shared logging, monitoring, and plugin systems

### 🔌 Advanced Plugin System
- **Real Plugin Installation** - Install .py files directly from messages or GitHub URLs
- **Hot Loading** - Plugins load instantly without restart
- **26+ Available Plugins** - Built-in commands + installable plugins
- **Custom Plugin Support** - Full API access for developers

### 🛡️ Security & Monitoring
- **PM Protection** - Auto-response with assistant bot redirection
- **Log Group Integration** - Command tracking, error monitoring, usage statistics
- **Code Protection** - Integrity verification and unauthorized usage detection
- **Environment Validation** - Secure configuration management

### 🎨 Rich Media Features
- **Text to Sticker** - Create custom stickers with multiple visual styles
- **Website Screenshots** - Full-page capture with mobile/desktop modes
- **Translation System** - Multi-language support with auto-detection
- **Group Management** - Smart leave commands and analytics

### Built-in Commands (24+ Core Plugins)

#### 📊 Information & Status
- **Alive** - Stylish status message with owner info and uptime
- **Ping** - Real-time latency testing with precise timing
- **Info** - Bot version, uptime, framework details
- **System** - CPU, memory, disk usage monitoring with real-time stats
- **Time** - Current date, time, timezone, and timestamp
- **Uptime** - How long the bot has been running

#### 👤 User Management
- **UserInfo** - Detailed user profiles (ID, username, verification status, profile photos)
- **ID** - Get user, chat, and message IDs with chat type detection
- **PM Permit** - Advanced private message protection with auto-responses

#### 🎨 Media & Stickers
- **Sticker Maker** - Create custom text stickers with multiple visual styles
- **Sticker Pack** - Manage and organize sticker collections

#### 🏢 Group Management
- **Leave** - Smart group leaving with confirmation prompts
- **Leave All** - Bulk group cleanup with safety confirmations
- **Groups** - Comprehensive group and channel listing with analytics

#### ✍️ Text Effects & Animation
- **Write** - Animated writing effect with cursor
- **Type** - Advanced typewriter effect with loading animation
- **Echo** - Simple text repetition
- **Reverse** - Text reversal utility

#### 🛠️ Utilities
- **Calculator** - Safe mathematical expression evaluation
- **Speed Test** - Network connection speed testing
- **Quote** - Format and quote replied messages with user attribution

#### 🛡️ Security & Protection
- **PM Permit** - Advanced private message protection with ASCII art display
- **Approve/Disapprove** - User management for PM protection

#### 🗑️ Message Management
- **Delete** - Remove your messages and replied messages
- **Purge** - Bulk delete messages from a specific point
- **Edit** - Edit your last sent message

#### 🔧 Development & Plugin Management
- **Update** - Check for userbot updates and changelog
- **Auto-Update** - Toggle automatic update notifications
- **Install** - Plugin installation system with URL and file support
- **Repository** - Show repository information and deployment links
- **Help** - Comprehensive command documentation with examples

## 🤖 Assistant Bot Features

The hybrid system includes a public assistant bot with these capabilities:

### Public Commands
- `/start` - Welcome message with feature overview
- `/help` - Complete command documentation
- `/ping` - Response time testing
- `/info` - Bot information and statistics
- `/webshot <url>` - Website screenshot capture
- `/translate <text>` - Text translation service

### Inline Mode
Use `@your_bot_username` in any chat for quick access:
- `webshot:url` - Instant website screenshots
- `translate:text` - Quick translation
- `ping` - Fast response test

### Auto-Profile Management
- Custom hexagonal Nexus logo
- Automatic bio and description updates
- Professional bot commands menu
- Real-time profile synchronization

### Log Group Integration
- Command usage tracking with user statistics
- Error monitoring and reporting
- Real-time performance metrics
- Professional formatted logs with timestamps

## 📦 Installable Plugins

Beyond the 24+ built-in commands, install additional plugins:

### Available Plugins
- **webshot** - Advanced website screenshot tool
- **translator** - Multi-language translation system
- **sticker_maker** - Create custom text stickers with styles
- **group_manager** - Smart group leaving and analytics
- **weather** - Weather information and forecasts
- **qrcode** - QR code generation utility

### Installation Methods
```bash
# Install from plugin repository
.install webshot

# Install from file (reply to .py file)
.install plugin_name

# List available plugins
.install list

# Check installation status
.install status
```

### Technical Features
- **Pyrogram Framework** - Fast, modern Telegram client library
- **Session Management** - Secure string session handling
- **Error Handling** - Comprehensive error logging and recovery
- **Real-time Animations** - Smooth text effects and loading indicators

## 🚀 Quick Deployment

### Prerequisites

1. **Get Telegram API Credentials:**
   - Visit [my.telegram.org/apps](https://my.telegram.org/apps)
   - Create a new application
   - Note your `API_ID` and `API_HASH`

2. **Generate Session String:**
   ```bash
   python3 -c "from pyrogram import Client; import asyncio; asyncio.run(Client(':memory:', api_id=YOUR_API_ID, api_hash='YOUR_API_HASH').start())"
   ```

3. **Create Assistant Bot (Optional):**
   - Message @BotFather on Telegram
   - Use `/newbot` command to create a new bot
   - Save the bot token for hybrid mode

### Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/nexus-userbot)

1. Click the deploy button above
2. Fork the repository when prompted
3. Set environment variables (see Configuration section below)

### Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/The-Nexus-Bot/Nexus-Userbot)

1. Fork this repository to your GitHub account
2. Click the deploy button above
3. Connect your forked repository
4. Add environment variables in Render dashboard
5. Deploy

### Deploy to Heroku

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/The-Nexus-Bot/Nexus-Userbot)

1. Fork this repository to your GitHub account
2. Click the deploy button above
3. Set the required environment variables
4. Deploy to Heroku

### Deploy to Koyeb

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&repository=github.com/The-Nexus-Bot/Nexus-Userbot&branch=main&name=nexus-userbot)

1. Fork this repository
2. Click the deploy button above
3. Connect your GitHub repository
4. Set environment variables in Koyeb console

### Local Deployment

1. **Clone and setup:**
   ```bash
   git clone https://github.com/The-Nexus-Bot/Nexus-Userbot.git
   cd Nexus-Userbot
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Run the userbot:**
   ```bash
   python main.py
   ```

## ⚙️ Configuration

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `API_ID` | Telegram API ID from my.telegram.org | `1234567` |
| `API_HASH` | Telegram API Hash from my.telegram.org | `abcdef123456...` |
| `SESSION_STRING` | Pyrogram session string | `BQC1Abc...` |

### Optional Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `COMMAND_PREFIX` | `.` | Command prefix for userbot |
| `BOT_TOKEN` | None | Assistant bot token for hybrid mode |
| `LOG_GROUP_ID` | None | Group ID for command/error logging |
| `ENABLE_ASSISTANT_BOT` | `false` | Enable public assistant bot |
| `AUTO_UPDATE_PROFILE` | `true` | Auto-update assistant bot profile |
| `ENABLE_INLINE_MODE` | `true` | Enable inline query support |
| `LOG_COMMANDS` | `true` | Log command usage to group |
| `LOG_ERRORS` | `true` | Log errors to group |
| `ENABLE_AUTO_RESPONSE` | `false` | PM auto-response system |
| `AUTO_RESPONSE_MESSAGE` | Custom | Custom PM response message |
| `BOT_NAME` | `Nexus Userbot` | Display name for the bot |
| `BOT_VERSION` | `2.0` | Version identifier |
| `OWNER_ID` | Auto-detect | Your Telegram user ID |

### Advanced Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `ENABLE_PROTECTION` | `true` | Code protection system |
| `ENVIRONMENT` | `production` | Environment mode |
| `DEBUG_MODE` | `false` | Enable debug logging |
| `PLUGIN_AUTO_LOAD` | `true` | Auto-load installed plugins |
| `COMMAND_COOLDOWN` | `2` | Cooldown between commands (seconds) |
| `MAX_MESSAGE_LENGTH` | `4096` | Maximum message length |

## 🎯 Command Categories

Use `.help` to see all available commands organized by category:

### Core Commands
- Information and status checking
- System monitoring and diagnostics
- Bot management and updates

### Media & Content
- Text effects and animations
- Sticker creation with multiple styles
- Website screenshot capture
- Translation services

### User & Group Management
- Private message protection
- Group analytics and management
- User information lookup

### Utilities
- Mathematical calculations
- Network speed testing
- Message formatting and quotes

## 🛡️ Security & Protection

### Code Integrity Verification
- Automatic detection of code modifications
- File hash verification system
- Environment validation and monitoring
- Anti-tampering protection

### PM Protection System
- Smart auto-response with assistant bot redirection
- Flood protection and rate limiting
- User approval/disapproval system
- Custom response messages

### Log Group Integration
- Real-time command usage tracking
- Error monitoring and reporting
- User activity analytics
- Professional formatted logs with timestamps

## 🔧 Development

### Plugin Development
Create custom plugins with full API access:

```python
# Example plugin structure
async def my_command(client, message):
    """Custom command implementation"""
    await message.edit("Hello from my plugin!")

# Plugin metadata
__plugin_name__ = "My Plugin"
__version__ = "1.0"
__commands__ = ["mycommand"]
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📊 Statistics & Analytics

### Usage Tracking
- Command usage statistics
- User engagement metrics
- System performance monitoring
- Error rate analysis

### Performance Metrics
- Response time tracking
- Memory usage monitoring
- CPU utilization stats
- Network performance data

## 🆘 Support & Community

### Getting Help
- Check the comprehensive `.help` command
- Review configuration documentation
- Join our community for support

### Troubleshooting
- Verify environment variables are set correctly
- Check session string validity
- Ensure proper permissions for bot operations
- Review logs for error details

## 📜 License

This project is licensed under the MIT License with attribution requirements. See the [LICENSE](LICENSE) file for details.

### Attribution Requirements
- Maintain original copyright notices
- Include attribution to @nexustech_dev
- Link back to the original repository

## ⚠️ Disclaimer

This userbot is for educational and personal use only. Users are responsible for complying with Telegram's Terms of Service and applicable laws in their jurisdiction.

## 🔗 Links

- **Repository**: [GitHub](https://github.com/The-Nexus-Bot/Nexus-Userbot)
- **Developer**: [@nexustech_dev](https://t.me/nexustech_dev)
- **Support**: Join our community for help and updates

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

Made with ❤️ by [@nexustech_dev](https://t.me/nexustech_dev)

</div>