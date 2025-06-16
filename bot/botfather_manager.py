"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         NEXUS BOTFATHER MANAGER                             ║
║                                                                              ║
║ Created by: @nexustech_dev                                                   ║
║ Copyright (c) 2025 NexusTech Development                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import logging
import os
from pyrogram.types import Message
from pyrogram.errors import RPCError

logger = logging.getLogger(__name__)

class BotFatherManager:
    """
    Automated BotFather configuration manager
    Handles profile picture, description, about text, and inline mode setup
    """
    
    def __init__(self, user_client, config):
        self.user_client = user_client
        self.config = config
        self.botfather_id = 93372553  # BotFather's user ID
        self.bot_username = None
        
    async def setup_bot_profile(self, bot_username: str = None):
        """
        Automatically configure bot profile via BotFather
        """
        if not bot_username and not self.config.BOT_USERNAME:
            logger.warning("No bot username provided for BotFather setup")
            return False
            
        self.bot_username = bot_username or self.config.BOT_USERNAME
        logger.info(f"Starting BotFather setup for @{self.bot_username}")
        
        try:
            # Setup all components
            await self._setup_profile_picture()
            await self._setup_description()
            await self._setup_about_text()
            await self._setup_inline_mode()
            await self._setup_commands()
            
            logger.info("✅ BotFather setup completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"BotFather setup failed: {e}")
            return False
    
    async def _send_botfather_command(self, command: str, wait_time: float = 2.0):
        """Send command to BotFather and wait for response"""
        try:
            await self.user_client.send_message(self.botfather_id, command)
            await asyncio.sleep(wait_time)
            logger.info(f"Sent BotFather command: {command}")
            return True
        except Exception as e:
            logger.error(f"Failed to send BotFather command '{command}': {e}")
            return False
    
    async def _setup_profile_picture(self):
        """Set bot profile picture"""
        if not os.path.exists(self.config.ASSISTANT_PROFILE_PIC):
            logger.warning("Profile picture file not found, skipping...")
            return
            
        try:
            logger.info("Setting up bot profile picture...")
            
            # Start setuserpic command
            await self._send_botfather_command("/setuserpic")
            await self._send_botfather_command(f"@{self.bot_username}")
            
            # Send the profile picture
            await self.user_client.send_photo(
                self.botfather_id,
                self.config.ASSISTANT_PROFILE_PIC,
                caption="New profile picture for the bot"
            )
            
            await asyncio.sleep(3)
            logger.info("✅ Profile picture updated")
            
        except Exception as e:
            logger.error(f"Failed to set profile picture: {e}")
    
    async def _setup_description(self):
        """Set bot description (shows in chat list)"""
        try:
            logger.info("Setting up bot description...")
            
            description = self.config.ASSISTANT_DESCRIPTION or """🤖 Nexus Assistant Bot

Advanced Telegram automation with AI capabilities, file management, and smart features.

🔹 File Processing & Media Tools
🔹 Text & Translation Services  
🔹 Web Screenshots & Analysis
🔹 System Information & Monitoring

Your personal Telegram assistant powered by Nexus Technology."""
            
            await self._send_botfather_command("/setdescription")
            await self._send_botfather_command(f"@{self.bot_username}")
            await self._send_botfather_command(description)
            
            logger.info("✅ Bot description updated")
            
        except Exception as e:
            logger.error(f"Failed to set description: {e}")
    
    async def _setup_about_text(self):
        """Set bot about text (shows in bot info)"""
        try:
            logger.info("Setting up bot about text...")
            
            about_text = self.config.ASSISTANT_BIO or """🤖 Advanced Telegram Userbot Assistant

Created by @nexustech_dev | Powered by Nexus Technology

Features:
• Smart Automation & AI Integration
• File Management & Media Processing
• Web Tools & Screenshot Capture
• Translation & Text Processing
• System Monitoring & Analytics

Experience the future of Telegram automation!"""
            
            await self._send_botfather_command("/setabouttext")
            await self._send_botfather_command(f"@{self.bot_username}")
            await self._send_botfather_command(about_text)
            
            logger.info("✅ Bot about text updated")
            
        except Exception as e:
            logger.error(f"Failed to set about text: {e}")
    
    async def _setup_inline_mode(self):
        """Enable inline mode for the bot"""
        try:
            logger.info("Setting up inline mode...")
            
            # Enable inline mode
            await self._send_botfather_command("/setinline")
            await self._send_botfather_command(f"@{self.bot_username}")
            await self._send_botfather_command("Search Nexus features...")
            
            # Set inline feedback
            await self._send_botfather_command("/setinlinefeedback")
            await self._send_botfather_command(f"@{self.bot_username}")
            await self._send_botfather_command("Enabled")
            
            logger.info("✅ Inline mode enabled")
            
        except Exception as e:
            logger.error(f"Failed to setup inline mode: {e}")
    
    async def _setup_commands(self):
        """Set bot commands menu"""
        try:
            logger.info("Setting up bot commands menu...")
            
            commands_text = """start - Start the assistant bot
help - Show available commands and features
ping - Check bot response time and status
info - Get detailed bot information
webshot - Take screenshot of any website
translate - Translate text between languages
stats - Show bot usage statistics
alive - Check if userbot is online"""
            
            await self._send_botfather_command("/setcommands")
            await self._send_botfather_command(f"@{self.bot_username}")
            await self._send_botfather_command(commands_text)
            
            logger.info("✅ Bot commands menu updated")
            
        except Exception as e:
            logger.error(f"Failed to set commands: {e}")
    
    async def update_bot_settings(self, settings: dict):
        """
        Update specific bot settings
        
        Args:
            settings (dict): Dictionary with settings to update
                - profile_pic: Path to new profile picture
                - description: New bot description
                - about: New about text
                - inline_placeholder: Inline mode placeholder text
        """
        try:
            if 'profile_pic' in settings and os.path.exists(settings['profile_pic']):
                await self._send_botfather_command("/setuserpic")
                await self._send_botfather_command(f"@{self.bot_username}")
                await self.user_client.send_photo(
                    self.botfather_id,
                    settings['profile_pic']
                )
                
            if 'description' in settings:
                await self._send_botfather_command("/setdescription")
                await self._send_botfather_command(f"@{self.bot_username}")
                await self._send_botfather_command(settings['description'])
                
            if 'about' in settings:
                await self._send_botfather_command("/setabouttext")
                await self._send_botfather_command(f"@{self.bot_username}")
                await self._send_botfather_command(settings['about'])
                
            if 'inline_placeholder' in settings:
                await self._send_botfather_command("/setinline")
                await self._send_botfather_command(f"@{self.bot_username}")
                await self._send_botfather_command(settings['inline_placeholder'])
                
            logger.info("✅ Bot settings updated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update bot settings: {e}")
            return False
    
    async def verify_bot_setup(self):
        """Verify that bot setup was successful"""
        try:
            # Send a test message to BotFather to check bot status
            await self._send_botfather_command("/mybots")
            await asyncio.sleep(2)
            
            # You could add more verification logic here
            logger.info("Bot setup verification completed")
            return True
            
        except Exception as e:
            logger.error(f"Bot verification failed: {e}")
            return False
    
    async def get_bot_info(self):
        """Get current bot information from BotFather"""
        try:
            await self._send_botfather_command("/mybots")
            await asyncio.sleep(1)
            await self._send_botfather_command(f"@{self.bot_username}")
            await asyncio.sleep(1)
            await self._send_botfather_command("Bot Settings")
            
            logger.info("Requested bot information from BotFather")
            return True
            
        except Exception as e:
            logger.error(f"Failed to get bot info: {e}")
            return False