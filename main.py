#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        NEXUS TELEGRAM USERBOT v2.0                          ║
║                                                                              ║
║ Created by: Pankaj                                                          ║
║ Copyright (c) 2025 The-Nexus-Bot                                            ║
║ License: MIT (with attribution requirements)                                ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import logging
import sys
import os
from datetime import datetime, timedelta
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from pyrogram.errors import RPCError, MessageIdInvalid, PhotoExtInvalid, PeerIdInvalid

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nexus_userbot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class NexusUserbot:
    """
    Nexus Telegram Userbot - Fixed and stable version
    """
    
    def __init__(self):
        self.config = Config()
        self.client = None
        self.assistant_bot = None
        self.start_time = datetime.now()
        self._display_banner()

    def _display_banner(self):
        """Display the Nexus Userbot banner"""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        NEXUS TELEGRAM USERBOT v2.0                          ║
║                                                                              ║
║ ✨ Hybrid Bot Architecture  🔌 Advanced Plugin System                       ║
║ 🛡️ Security & Monitoring   🎨 Rich Media Features                          ║
║                                                                              ║
║ Created by: @nexustech_dev                                                   ║
║ Copyright (c) 2025 NexusTech Development                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
        logger.info("Nexus Userbot v2.0 - Starting...")

    def initialize_client(self):
        """Initialize the Pyrogram client with error handling"""
        try:
            # Use session string if available, otherwise use session file
            session_name = self.config.SESSION_STRING or "nexus_userbot"
            
            self.client = Client(
                session_name,
                api_id=self.config.API_ID,
                api_hash=self.config.API_HASH,
                in_memory=bool(self.config.SESSION_STRING)
            )
            
            logger.info("Pyrogram client initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Pyrogram client: {e}")
            return False

    async def setup_handlers(self):
        """Setup event handlers with comprehensive error handling"""
        try:
            # Ping command
            @self.client.on_message(filters.outgoing & filters.text & filters.command("ping", prefixes=self.config.COMMAND_PREFIX))
            async def ping_command(client, message: Message):
                try:
                    start_time = datetime.now()
                    sent_message = await message.edit("🏓 Pong!")
                    end_time = datetime.now()
                    ping_time = (end_time - start_time).total_seconds() * 1000
                    await sent_message.edit(f"🏓 **Pong!**\n⚡ **Ping:** `{ping_time:.2f}ms`")
                except Exception as e:
                    logger.error(f"Error in ping command: {e}")
                    try:
                        await message.edit("❌ Error in ping command")
                    except:
                        pass

            # Help command
            @self.client.on_message(filters.outgoing & filters.text & filters.command("help", prefixes=self.config.COMMAND_PREFIX))
            async def help_command(client, message: Message):
                try:
                    help_text = f"""
**🤖 Nexus Userbot v2.0**

**📊 Information Commands:**
• `{self.config.COMMAND_PREFIX}alive` - Check if bot is alive
• `{self.config.COMMAND_PREFIX}ping` - Check bot latency
• `{self.config.COMMAND_PREFIX}info` - Bot information
• `{self.config.COMMAND_PREFIX}uptime` - Bot uptime
• `{self.config.COMMAND_PREFIX}system` - System information

**✍️ Text Commands:**
• `{self.config.COMMAND_PREFIX}echo <text>` - Echo text
• `{self.config.COMMAND_PREFIX}write <text>` - Animated writing
• `{self.config.COMMAND_PREFIX}type <text>` - Typewriter effect

**🛠️ Utilities:**
• `{self.config.COMMAND_PREFIX}calc <expression>` - Calculator
• `{self.config.COMMAND_PREFIX}time` - Current time

**🤖 Bot Management:**
• `{self.config.COMMAND_PREFIX}setupbot` - Configure bot via BotFather
• `{self.config.COMMAND_PREFIX}botstatus` - Check assistant bot status

**🔧 Development:**
• `{self.config.COMMAND_PREFIX}install <plugin>` - Install plugins
• `{self.config.COMMAND_PREFIX}repo` - Repository info

**Built with ❤️ by @nexustech_dev**
                    """
                    await message.edit(help_text)
                except Exception as e:
                    logger.error(f"Error in help command: {e}")

            # Alive command - Fixed version
            @self.client.on_message(filters.outgoing & filters.text & filters.command("alive", prefixes=self.config.COMMAND_PREFIX))
            async def alive_command(client, message: Message):
                try:
                    me = await client.get_me()
                    uptime = datetime.now() - self.start_time
                    
                    alive_text = f"""
**🌟 Nexus Userbot Status**

**👤 Owner:** [{me.first_name}](tg://user?id={me.id})
**⚡ Version:** v2.0
**🚀 Framework:** Pyrogram
**⏰ Uptime:** {str(uptime).split('.')[0]}
**🌟 Status:** Online & Running

**🛡️ Protected by Nexus Security**
                    """
                    
                    await message.edit(alive_text)
                except Exception as e:
                    logger.error(f"Error in alive command: {e}")
                    try:
                        await message.edit("✅ **Nexus Userbot is alive and running!**")
                    except:
                        pass

            # Info command
            @self.client.on_message(filters.outgoing & filters.text & filters.command("info", prefixes=self.config.COMMAND_PREFIX))
            async def info_command(client, message: Message):
                try:
                    import platform
                    import psutil
                    
                    python_version = platform.python_version()
                    system_info = f"{platform.system()} {platform.release()}"
                    cpu_usage = psutil.cpu_percent()
                    memory = psutil.virtual_memory()
                    
                    info_text = f"""
**🤖 Nexus Userbot Information**

**🐍 Python:** {python_version}
**💻 System:** {system_info}
**🔧 Framework:** Pyrogram v2.0
**📊 CPU Usage:** {cpu_usage}%
**💾 Memory:** {memory.percent}%

**⚡ Status:** Running smoothly
                    """
                    await message.edit(info_text)
                except Exception as e:
                    logger.error(f"Error in info command: {e}")
                    await message.edit("❌ Error getting system information")

            # Echo command
            @self.client.on_message(filters.outgoing & filters.text & filters.command("echo", prefixes=self.config.COMMAND_PREFIX))
            async def echo_command(client, message: Message):
                try:
                    text = message.text.split(None, 1)
                    if len(text) < 2:
                        await message.edit("❌ **Usage:** `.echo <text>`")
                        return
                    
                    await message.edit(f"🔊 **Echo:** {text[1]}")
                except Exception as e:
                    logger.error(f"Error in echo command: {e}")

            # Calculator command
            @self.client.on_message(filters.outgoing & filters.text & filters.command("calc", prefixes=self.config.COMMAND_PREFIX))
            async def calc_command(client, message: Message):
                try:
                    expression = message.text.split(None, 1)
                    if len(expression) < 2:
                        await message.edit("❌ **Usage:** `.calc <expression>`")
                        return
                    
                    try:
                        # Safe evaluation
                        result = eval(expression[1], {"__builtins__": {}}, {})
                        await message.edit(f"🧮 **Result:** `{result}`")
                    except Exception as calc_error:
                        await message.edit(f"❌ **Error:** Invalid expression")
                except Exception as e:
                    logger.error(f"Error in calc command: {e}")

            # Time command
            @self.client.on_message(filters.outgoing & filters.text & filters.command("time", prefixes=self.config.COMMAND_PREFIX))
            async def time_command(client, message: Message):
                try:
                    now = datetime.now()
                    time_text = f"""
**🕐 Current Time**

**📅 Date:** {now.strftime('%Y-%m-%d')}
**⏰ Time:** {now.strftime('%H:%M:%S')}
**🌍 Timezone:** UTC
**📊 Timestamp:** {int(now.timestamp())}
                    """
                    await message.edit(time_text)
                except Exception as e:
                    logger.error(f"Error in time command: {e}")

            # Repository command
            @self.client.on_message(filters.outgoing & filters.text & filters.command("repo", prefixes=self.config.COMMAND_PREFIX))
            async def repo_command(client, message: Message):
                try:
                    repo_text = """
**📁 Nexus Userbot Repository**

**🔗 GitHub:** [The-Nexus-Bot/Nexus-Userbot](https://github.com/The-Nexus-Bot/Nexus-Userbot)
**👨‍💻 Developer:** [@nexustech_dev](https://t.me/nexustech_dev)
**📄 License:** MIT with Attribution
**⭐ Version:** v2.0

**🚀 Deploy on:**
• Railway • Render • Heroku • Koyeb

**💡 Features:** 26+ Commands, Plugin System, Hybrid Bot
                    """
                    await message.edit(repo_text)
                except Exception as e:
                    logger.error(f"Error in repo command: {e}")

            # BotFather setup command
            @self.client.on_message(filters.outgoing & filters.text & filters.command("setupbot", prefixes=self.config.COMMAND_PREFIX))
            async def setupbot_command(client, message: Message):
                try:
                    if not self.assistant_bot or not self.assistant_bot.botfather_manager:
                        await message.edit("❌ **Assistant bot not initialized**\n\nEnable hybrid mode by setting BOT_TOKEN")
                        return
                    
                    await message.edit("🤖 **Setting up bot via BotFather...**\n\nThis may take a few moments...")
                    
                    # Get bot username
                    bot_me = await self.assistant_bot.bot_client.get_me()
                    bot_username = bot_me.username
                    
                    if not bot_username:
                        await message.edit("❌ **Error:** Bot username not found")
                        return
                    
                    # Run BotFather setup
                    success = await self.assistant_bot.botfather_manager.setup_bot_profile(bot_username)
                    
                    if success:
                        await message.edit(f"""
✅ **BotFather Setup Completed**

**Bot:** @{bot_username}
**Profile Picture:** Updated
**Description:** Updated  
**About Text:** Updated
**Inline Mode:** Enabled
**Commands Menu:** Updated

Your assistant bot is now fully configured!
                        """)
                    else:
                        await message.edit("❌ **BotFather setup failed**\n\nCheck logs for details.")
                        
                except Exception as e:
                    logger.error(f"Error in setupbot command: {e}")
                    await message.edit("❌ **Error during BotFather setup**")

            # Bot status command
            @self.client.on_message(filters.outgoing & filters.text & filters.command("botstatus", prefixes=self.config.COMMAND_PREFIX))
            async def botstatus_command(client, message: Message):
                try:
                    if not self.assistant_bot:
                        await message.edit("❌ **Assistant bot not initialized**\n\n**Hybrid Mode:** Disabled")
                        return
                    
                    bot_me = await self.assistant_bot.bot_client.get_me()
                    
                    status_text = f"""
**🤖 Assistant Bot Status**

**Username:** @{bot_me.username}
**Name:** {bot_me.first_name}
**ID:** `{bot_me.id}`
**Status:** Online & Active

**Configuration:**
• **Auto BotFather Setup:** {'Enabled' if self.config.AUTO_SETUP_BOTFATHER else 'Disabled'}
• **Profile Updates:** {'Enabled' if self.config.AUTO_UPDATE_BOT_PROFILE else 'Disabled'}
• **Inline Mode:** {'Enabled' if self.config.ENABLE_INLINE_MODE else 'Disabled'}
• **Log Group:** {'Enabled' if self.config.ENABLE_LOG_GROUP else 'Disabled'}

**Commands Available:**
• `/start` - Start the bot
• `/help` - Show help menu
• `/ping` - Response time
• `/info` - Bot information
• `/webshot` - Website screenshots
• `/translate` - Text translation

**Usage:** Use `.setupbot` to configure via BotFather
                    """
                    
                    await message.edit(status_text)
                    
                except Exception as e:
                    logger.error(f"Error in botstatus command: {e}")
                    await message.edit("❌ **Error getting bot status**")

            logger.info("Event handlers setup successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup handlers: {e}")
            return False

    async def run(self):
        """Main run method with comprehensive error handling"""
        try:
            # Initialize client
            if not self.initialize_client():
                logger.error("Failed to initialize client")
                return
            
            # Setup handlers
            if not await self.setup_handlers():
                logger.error("Failed to setup handlers")
                return
            
            # Start client
            try:
                await self.client.start()
                logger.info("Pyrogram client started successfully")
            except Exception as e:
                logger.error(f"Failed to start client: {e}")
                return
            
            # Get user information
            try:
                me = await self.client.get_me()
                username = f"@{me.username}" if me.username else "No username"
                logger.info(f"Logged in as: {me.first_name} ({username})")
            except Exception as e:
                logger.error(f"Failed to get user info: {e}")
                logger.info("Client started but couldn't fetch user info")
            
            # Initialize assistant bot if token provided
            if self.config.BOT_TOKEN:
                try:
                    from bot.assistant_bot import AssistantBot
                    self.assistant_bot = AssistantBot(self.config, self.client)
                    if await self.assistant_bot.initialize_bot():
                        logger.info("Assistant bot initialized successfully")
                    else:
                        logger.warning("Failed to initialize assistant bot")
                except Exception as e:
                    logger.error(f"Assistant bot error: {e}")
            else:
                logger.info("No BOT_TOKEN provided - running in userbot-only mode")
            
            logger.info("🎉 Nexus Userbot is now running!")
            logger.info(f"Prefix: {self.config.COMMAND_PREFIX}")
            logger.info("Type .help to see available commands")
            
            # Keep running
            await idle()
            
        except KeyboardInterrupt:
            logger.info("Userbot stopped by user")
        except Exception as e:
            logger.error(f"Critical error: {e}")
            import traceback
            logger.error(traceback.format_exc())
        finally:
            try:
                if hasattr(self, 'client') and self.client:
                    await self.client.stop()
                    logger.info("Client stopped")
            except Exception as e:
                logger.error(f"Error stopping client: {e}")

async def main():
    """Main function"""
    try:
        userbot = NexusUserbot()
        await userbot.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(main())