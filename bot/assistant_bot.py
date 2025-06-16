"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         NEXUS ASSISTANT BOT                                 ║
║                                                                              ║
║ Created by: @nexustech_dev                                                   ║
║ Copyright (c) 2025 NexusTech Development                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from pyrogram.types import BotCommand
import aiohttp
from .botfather_manager import BotFatherManager

class AssistantBot:
    """
    Assistant bot for Nexus Userbot - handles public commands, inline mode, and profile management
    """
    
    def __init__(self, config, user_client):
        self.config = config
        self.user_client = user_client
        self.bot_client = None
        self.cooldowns = {}
        self.command_stats = {}
        self.error_count = 0
        self.botfather_manager = None
        
    async def initialize_bot(self):
        """Initialize the assistant bot client"""
        if not self.config.BOT_TOKEN:
            return False
            
        try:
            self.bot_client = Client(
                "nexus_assistant",
                bot_token=self.config.BOT_TOKEN,
                api_id=self.config.API_ID,
                api_hash=self.config.API_HASH
            )
            
            await self.bot_client.start()
            
            # Initialize BotFather manager
            self.botfather_manager = BotFatherManager(self.user_client, self.config)
            
            # Setup bot profile via BotFather (if enabled)
            if self.config.AUTO_SETUP_BOTFATHER:
                await self._setup_via_botfather()
            
            await self.setup_bot_profile()
            await self.setup_bot_handlers()
            await self.setup_bot_commands()
            
            return True
        except Exception as e:
            print(f"Failed to initialize assistant bot: {e}")
            return False
    
    async def _setup_via_botfather(self):
        """Setup bot profile via BotFather automatically"""
        try:
            print("🤖 Setting up bot profile via BotFather...")
            
            # Get bot username
            bot_me = await self.bot_client.get_me()
            bot_username = bot_me.username
            
            if not bot_username:
                print("❌ Bot username not found, skipping BotFather setup")
                return
            
            # Run BotFather setup
            success = await self.botfather_manager.setup_bot_profile(bot_username)
            
            if success:
                print("✅ BotFather setup completed successfully")
                
                # Log to group if enabled
                if self.config.ENABLE_LOG_GROUP:
                    await self.log_to_group(
                        "BOT_SETUP",
                        f"🤖 **Bot Profile Updated**\n\n"
                        f"• **Username:** @{bot_username}\n"
                        f"• **Profile Picture:** Updated\n"
                        f"• **Description:** Updated\n"
                        f"• **About Text:** Updated\n"
                        f"• **Inline Mode:** Enabled\n"
                        f"• **Commands Menu:** Updated\n\n"
                        f"Bot is now fully configured via BotFather!"
                    )
            else:
                print("❌ BotFather setup failed")
                
        except Exception as e:
            print(f"BotFather setup error: {e}")
    
    async def setup_bot_profile(self):
        """Update bot profile automatically"""
        if not self.config.AUTO_UPDATE_BOT_PROFILE:
            return
            
        try:
            bot_me = await self.bot_client.get_me()
            
            # Update bot name if different
            if bot_me.first_name != self.config.ASSISTANT_NAME:
                await self.bot_client.set_chat_title(
                    chat_id="me",
                    title=self.config.ASSISTANT_NAME
                )
            
            # Update bot description
            await self.bot_client.set_chat_description(
                chat_id="me",
                description=self.config.ASSISTANT_DESCRIPTION
            )
            
            # Update profile picture if exists
            if os.path.exists(self.config.ASSISTANT_PROFILE_PIC):
                await self.bot_client.set_chat_photo(
                    chat_id="me",
                    photo=self.config.ASSISTANT_PROFILE_PIC
                )
                
            print("✅ Bot profile updated successfully")
            
        except Exception as e:
            print(f"Failed to update bot profile: {e}")
    
    async def setup_bot_commands(self):
        """Setup bot commands menu"""
        try:
            commands = [
                BotCommand("start", "Start the assistant bot"),
                BotCommand("help", "Show available commands"),
                BotCommand("ping", "Check bot response time"),
                BotCommand("info", "Get bot information"),
                BotCommand("webshot", "Take website screenshot"),
                BotCommand("translate", "Translate text"),
                BotCommand("stats", "Show bot statistics")
            ]
            
            await self.bot_client.set_bot_commands(commands)
            print("✅ Bot commands menu updated")
            
        except Exception as e:
            print(f"Failed to setup bot commands: {e}")
    
    async def log_to_group(self, message_type: str, content: str, user_info: str = ""):
        """Send logs to the configured log group"""
        if not self.config.ENABLE_LOG_GROUP or not self.config.LOG_GROUP_ID:
            return
            
        try:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            log_message = f"""
🔸 **NEXUS BOT LOG**

**Type:** {message_type}
**Time:** {timestamp}
{f"**User:** {user_info}" if user_info else ""}

**Details:**
{content}

**Stats:**
• Commands: {sum(self.command_stats.values())}
• Errors: {self.error_count}
            """
            
            await self.bot_client.send_message(
                chat_id=int(self.config.LOG_GROUP_ID),
                text=log_message
            )
        except Exception as e:
            print(f"Failed to log to group: {e}")
    
    async def track_command_usage(self, command: str, user_id: int, username: str = ""):
        """Track command usage and log if enabled"""
        if command not in self.command_stats:
            self.command_stats[command] = 0
        self.command_stats[command] += 1
        
        if self.config.LOG_ALL_COMMANDS:
            user_info = f"@{username} ({user_id})" if username else f"ID: {user_id}"
            await self.log_to_group(
                "COMMAND", 
                f"Command: /{command}\nUsage Count: {self.command_stats[command]}", 
                user_info
            )
    
    async def log_error(self, error: str, command: str = "", user_info: str = ""):
        """Log errors to the group"""
        if not self.config.LOG_ERRORS:
            return
            
        self.error_count += 1
        error_content = f"Error in {command}: {error}" if command else f"Error: {error}"
        await self.log_to_group("ERROR", error_content, user_info)
    
    async def setup_bot_handlers(self):
        """Setup assistant bot message handlers"""
        
        @self.bot_client.on_message(filters.command("start"))
        async def start_command(client, message: Message):
            try:
                await self.track_command_usage("start", message.from_user.id, message.from_user.username)
                
                welcome_text = f"""
🤖 **Welcome to Nexus Assistant!**

I'm the assistant bot for **Nexus Userbot v2.0**

**🔧 Available Commands:**
• `/help` - Show all commands
• `/ping` - Check response time
• `/info` - Bot information
• `/webshot <url>` - Website screenshot
• `/translate <text>` - Translate text

**💡 Features:**
• Public command access
• Inline mode support
• File management
• Real-time assistance

**👨‍💻 Developer:** @nexustech_dev
**🏷️ Version:** {self.config.BOT_VERSION}

Type `/help` for detailed command information!
                """
                await message.reply(welcome_text)
            except Exception as e:
                await self.log_error(str(e), "start", f"@{message.from_user.username} ({message.from_user.id})")
        
        @self.bot_client.on_message(filters.command("help"))
        async def help_command(client, message: Message):
            help_text = """
🤖 **Nexus Assistant Commands**

**📊 Information:**
• `/ping` - Check bot latency
• `/info` - Detailed bot information
• `/stats` - Usage statistics

**🛠️ Utilities:**
• `/webshot <url>` - Take website screenshot
• `/translate <text>` - Translate text to English
• `/echo <text>` - Echo your message

**📱 Inline Mode:**
Use `@your_bot_username <query>` in any chat:
• `webshot:url` - Quick screenshot
• `translate:text` - Quick translation
• `ping` - Quick ping test

**ℹ️ About:**
This is the assistant bot for Nexus Userbot v2.0
Created by @nexustech_dev
            """
            await message.reply(help_text)
        
        @self.bot_client.on_message(filters.command("ping"))
        async def ping_command(client, message: Message):
            if not self._check_cooldown(message.from_user.id, "ping"):
                await message.reply("⏳ Please wait before using this command again")
                return
                
            import time
            start_time = time.time()
            sent_message = await message.reply("🏓 Pinging...")
            end_time = time.time()
            
            ping_time = round((end_time - start_time) * 1000, 2)
            await sent_message.edit(f"🏓 **Pong!**\n📶 **Latency:** {ping_time}ms")
        
        @self.bot_client.on_message(filters.command("info"))
        async def info_command(client, message: Message):
            if not self._check_cooldown(message.from_user.id, "info"):
                await message.reply("⏳ Please wait before using this command again")
                return
                
            bot_me = await client.get_me()
            info_text = f"""
🤖 **Nexus Assistant Information**

**📋 Details:**
• **Name:** {bot_me.first_name}
• **Username:** @{bot_me.username}
• **Version:** {self.config.BOT_VERSION}
• **Framework:** Pyrogram

**🔧 Capabilities:**
• Public command access
• Inline query support
• File management
• Real-time responses

**👨‍💻 Developer:** @nexustech_dev
**🌐 Repository:** The-Nexus-Bot/Nexus-Userbot
            """
            await message.reply(info_text)
        
        @self.bot_client.on_message(filters.command("webshot"))
        async def webshot_command(client, message: Message):
            if not self._check_cooldown(message.from_user.id, "webshot"):
                await message.reply("⏳ Please wait before using this command again")
                return
                
            args = message.text.split()[1:]
            if not args:
                await message.reply("Usage: `/webshot <url>`\nExample: `/webshot https://google.com`")
                return
                
            url = args[0]
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            await message.reply(f"📸 Taking screenshot of: {url}\n⏳ Please wait...")
            
            # Use a simple screenshot service
            screenshot_url = f"https://api.screenshotone.com/take?url={url}&viewport_width=1920&viewport_height=1080&device_scale_factor=1&format=png"
            
            try:
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=screenshot_url,
                    caption=f"📸 **Screenshot**\n🔗 **URL:** {url}",
                    reply_to_message_id=message.id
                )
            except:
                await message.reply("❌ Failed to take screenshot. Please check the URL.")
        
        # Inline query handler
        @self.bot_client.on_inline_query()
        async def inline_query_handler(client, query: InlineQuery):
            if not self.config.ENABLE_INLINE_MODE:
                return
                
            query_text = query.query.lower()
            results = []
            
            if query_text.startswith("webshot:"):
                url = query_text.replace("webshot:", "").strip()
                if url:
                    results.append(
                        InlineQueryResultArticle(
                            title=f"📸 Screenshot: {url}",
                            description="Take a screenshot of this website",
                            input_message_content=InputTextMessageContent(
                                f"📸 Taking screenshot of: {url}"
                            )
                        )
                    )
            
            elif query_text.startswith("translate:"):
                text = query_text.replace("translate:", "").strip()
                if text:
                    results.append(
                        InlineQueryResultArticle(
                            title=f"🌐 Translate: {text[:50]}...",
                            description="Translate this text",
                            input_message_content=InputTextMessageContent(
                                f"🌐 Translating: {text}"
                            )
                        )
                    )
            
            elif query_text == "ping":
                results.append(
                    InlineQueryResultArticle(
                        title="🏓 Ping Test",
                        description="Check bot response time",
                        input_message_content=InputTextMessageContent("🏓 Pong! Bot is online and responsive")
                    )
                )
            
            else:
                # Default suggestions
                results = [
                    InlineQueryResultArticle(
                        title="📸 Website Screenshot",
                        description="Type: webshot:url",
                        input_message_content=InputTextMessageContent("📸 Use: webshot:https://example.com")
                    ),
                    InlineQueryResultArticle(
                        title="🌐 Text Translation",
                        description="Type: translate:text",
                        input_message_content=InputTextMessageContent("🌐 Use: translate:Hello world")
                    ),
                    InlineQueryResultArticle(
                        title="🏓 Ping Test",
                        description="Type: ping",
                        input_message_content=InputTextMessageContent("🏓 Pong! Bot is responsive")
                    )
                ]
            
            await query.answer(results, cache_time=self.config.INLINE_CACHE_TIME)
    
    def _check_cooldown(self, user_id: int, command: str) -> bool:
        """Check if user is on cooldown for command"""
        import time
        
        key = f"{user_id}:{command}"
        current_time = time.time()
        
        if key in self.cooldowns:
            if current_time - self.cooldowns[key] < self.config.PUBLIC_COMMAND_COOLDOWN:
                return False
        
        self.cooldowns[key] = current_time
        return True
    
    async def stop_bot(self):
        """Stop the assistant bot"""
        if self.bot_client:
            await self.bot_client.stop()
            print("Assistant bot stopped")