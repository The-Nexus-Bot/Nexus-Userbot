# Nexus Telegram Userbot v2.0

## Overview

Nexus is a sophisticated hybrid Telegram userbot system featuring both personal automation and public assistant bot capabilities. Built with Python and Pyrogram framework, it combines advanced userbot functionality with a public bot interface, offering comprehensive plugin architecture, real-time monitoring, and extensive security features. The system includes 26+ built-in commands, file-based plugin installation, log group integration, and multi-platform deployment support with complete documentation.

## System Architecture

### Core Architecture
- **Framework**: Python-based using Pyrogram 2.0+ for Telegram API interactions
- **Language**: Python 3.11+
- **Session Management**: Uses session strings for authentication
- **Configuration**: Environment variable-based configuration with dotenv support
- **Logging**: Comprehensive logging system with file and console output

### Security Layer
- **Code Protection**: Advanced protection system with integrity verification
- **Fingerprinting**: Unique system identification and environment detection
- **PM Protection**: Private message filtering and auto-response system
- **Authorization**: User-based access control with blacklisting capabilities

### Modular Design
- **Core Bot**: Main application logic in `main.py`
- **Bot Package**: Modular components in `/bot` directory
- **Commands**: Extensible command system with 20+ built-in plugins
- **Utilities**: Helper functions and system monitoring tools

## Key Components

### 1. Main Application (`main.py`)
- Entry point for the userbot application
- Handles client initialization and connection management
- Implements banner display and startup procedures

### 2. Configuration System (`config.py`)
- Centralized configuration management
- Environment variable loading and validation
- Supports both direct environment variables and .env files

### 3. Bot Package (`/bot`)
- **Commands** (`commands.py`): Command registration and execution system
- **Protection** (`protection.py`): Security and code integrity features
- **Fingerprinting** (`fingerprint.py`): System identification and tracking
- **Handlers** (`handlers.py`): Message processing and auto-response logic
- **Notifications** (`notifications.py`): Deployment tracking and analytics
- **Utils** (`utils.py`): Helper functions and formatting utilities

### 4. Hybrid Bot System
**Personal Userbot (main.py)**:
- 24+ built-in commands with extensive functionality
- PM protection with auto-response redirection
- Advanced plugin installation and management
- System monitoring and diagnostics

**Assistant Bot (bot/assistant_bot.py)**:
- Public commands (/start, /help, /ping, /info, /webshot, /translate)
- Inline mode support for quick access
- Automatic BotFather profile configuration on deployment
- Real-time command statistics and activity logging

### 5. Advanced Plugin System
**Built-in Plugins (26+ Commands)**:
- **Core**: alive, ping, help, info, stats, uptime, system, echo, calc, time, nexus
- **Media**: sticker maker, webshot, translator
- **Management**: userinfo, id, pmpermit, delete, purge, edit, speedtest, quote
- **Group Tools**: leave, leaveall, groups
- **Text Effects**: write, type, reverse
- **Development**: update, autoupdate, install, repo

**Installable Plugins**:
- File-based installation from messages or GitHub URLs
- Hot loading without restart
- Full API access for custom development
- Plugin repository with webshot, translator, sticker_maker, group_manager

### 6. Log Group Integration System
**Real-time Monitoring**:
- Command usage tracking with user statistics
- Error monitoring and professional formatted reporting
- User activity analytics with timestamps
- Performance metrics and system health monitoring

**Professional Logging Features**:
- Formatted logs with emoji indicators and timestamps
- Command execution tracking with user information
- Error reporting with detailed stack traces
- Usage statistics and engagement metrics

### 7. Asset System (`/assets`)
- Custom hexagonal Nexus bot profile picture (nexus_bot_profile.png)
- Stylish alive status graphics (nexus_alive.png)
- Protection system visual elements (nexus_protection.png)
- Professional PNG images optimized for Telegram compatibility

### 8. Comprehensive Documentation
**README.md Features**:
- Complete hybrid system documentation covering all 26+ features
- Detailed configuration options with 20+ environment variables
- Multi-platform deployment instructions (Railway, Render, Heroku, Koyeb, Local)
- Plugin development guide with code examples
- Troubleshooting section with common issues and solutions
- Security features documentation
- Professional styling with badges and structured sections

## Data Flow

### 1. Initialization Flow
```
Environment Loading → Configuration Validation → Client Creation → 
Protection System → Command Registration → Event Handlers → Start Listening
```

### 2. Command Processing Flow
```
Message Received → Command Detection → Permission Check → 
Command Execution → Response Generation → Message Sending
```

### 3. Auto-Response Flow
```
Private Message → User Verification → Flood Protection Check → 
Auto-Response Logic → Message Delivery
```

### 4. Protection Flow
```
Startup → Fingerprint Generation → Environment Detection → 
Notification Sending → Continuous Monitoring
```

## External Dependencies

### Core Dependencies
- **pyrogram** (≥2.0.106): Telegram MTProto API framework
- **tgcrypto** (≥1.2.5): Cryptographic functions for Pyrogram
- **python-dotenv** (≥1.0.0): Environment variable management
- **aiohttp** (≥3.8.0): Async HTTP client for webhooks
- **psutil** (≥5.9.0): System and process monitoring
- **cryptography** (≥40.0.0): Additional cryptographic operations
- **requests** (≥2.28.0): HTTP requests for external APIs
- **python-dateutil** (≥2.8.0): Date and time utilities

### External Services
- **Telegram API**: Core messaging platform
- **Webhook Endpoints**: For deployment notifications and analytics
- **System Resources**: CPU, memory, and disk monitoring

## Deployment Strategy

### Supported Platforms
1. **Heroku**: Complete configuration with `app.json` and `Procfile`
2. **Render**: YAML-based deployment with `render.yaml`
3. **Railway/Koyeb**: Generic Python deployment support
4. **Local Development**: Direct Python execution
5. **Replit**: Integrated development environment support

### Deployment Files
- **Procfile**: Process definition for Heroku-style platforms
- **app.json**: Heroku deployment metadata and environment variables
- **render.yaml**: Render-specific deployment configuration
- **runtime.txt**: Python version specification
- **dependencies.txt**: Python package requirements
- **.replit**: Replit environment configuration

### Environment Variables
#### Required
- `API_ID`: Telegram API ID
- `API_HASH`: Telegram API hash
- `SESSION_STRING`: Pyrogram session string

#### Optional
- `COMMAND_PREFIX`: Command prefix (default: ".")
- `BOT_NAME`: Bot display name
- `BOT_VERSION`: Version identifier
- Various feature flags and security settings

### Security Considerations
- Session files excluded from version control
- Environment variables for sensitive data
- Code integrity protection system
- Deployment tracking and notifications

## Changelog
- June 16, 2025: Initial setup with 20+ plugins
- June 16, 2025: Added repository management plugins (.update, .autoupdate, .install, .repo)
- June 16, 2025: Updated alive image to cyberpunk robot design
- June 16, 2025: Removed fingerprint.py for cleaner structure
- June 16, 2025: Total plugins increased to 24+
- June 16, 2025: Implemented hybrid userbot + assistant bot system
- June 16, 2025: Added public commands, inline mode, and automatic bot profile management
- June 16, 2025: Created file-based plugin installation system with real-time loading
- June 16, 2025: Updated branding from @nexustech_dev to @nexus_ub across all files
- June 16, 2025: Added comprehensive log group functionality for command tracking and error monitoring
- June 16, 2025: Created new hexagonal Nexus bot profile picture (assets/nexus_bot_profile.png)
- June 16, 2025: Enhanced assistant bot with real-time command statistics and activity logging
- June 16, 2025: Created comprehensive sticker maker plugin with multiple visual styles
- June 16, 2025: Implemented group management system with smart leaving and analytics
- June 16, 2025: Updated README with complete hybrid system documentation covering all 26+ features
- June 16, 2025: Added extensive configuration options and deployment instructions for all platforms
- June 16, 2025: Converted all SVG assets to PNG format for Telegram compatibility, preventing PHOTO_EXT_INVALID errors
- June 16, 2025: Added automatic BotFather configuration system with profile picture, description, about text, inline mode, and commands menu setup
- June 16, 2025: Created new userbot commands (.setupbot, .botstatus) for managing assistant bot configuration

## User Preferences

Preferred communication style: Simple, everyday language.
Branding: Use @nexus_ub for all developer references instead of @nexustech_dev