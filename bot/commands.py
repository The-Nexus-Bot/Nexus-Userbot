#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         NEXUS USERBOT COMMANDS                              ║
║                                                                              ║
║ Created by: @nexustech_dev                                                   ║
║ Copyright (c) 2025 NexusTech Development                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import time
import psutil
import platform
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Callable
from pyrogram.types import Message
from pyrogram.errors import MessageTooLong

from .utils import BotUtils
from .fingerprint import SystemFingerprint

logger = logging.getLogger(__name__)

class CommandManager:
    """
    Manages all bot commands and their execution
    """
    
    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.utils = BotUtils()
        self.fingerprint = SystemFingerprint()
        self.commands: Dict[str, Callable] = {}
        self.command_stats: Dict[str, int] = {}
        self.command_aliases: Dict[str, str] = {}
        
        # Register all commands
        self._register_commands()
        
        # Store start time for uptime calculations
        self.start_time = datetime.now()
        
    def _register_commands(self):
        """Register all available commands"""
        # Basic commands
        self.commands['help'] = self._cmd_help
        self.commands['ping'] = self._cmd_ping
        self.commands['info'] = self._cmd_info
        self.commands['stats'] = self._cmd_stats
        self.commands['uptime'] = self._cmd_uptime
        
        # System commands
        self.commands['sys'] = self._cmd_system
        
        # Utility commands
        self.commands['echo'] = self._cmd_echo
        self.commands['calc'] = self._cmd_calc
        self.commands['time'] = self._cmd_time
        
        # Nexus specific commands
        self.commands['nexus'] = self._cmd_nexus
        
        # Set up aliases
        self.command_aliases.update({
            'h': 'help',
            'p': 'ping',
            'i': 'info',
            's': 'stats',
            'up': 'uptime',
            'system': 'sys',
            'ps': 'processes',
            'e': 'echo',
            'c': 'calc',
            't': 'time',
            'w': 'weather',
            'a': 'ascii',
            'f': 'figlet',
            'r': 'random',
            'n': 'nexus',
            'inst': 'instance',
            'fp': 'fingerprint',
            'prot': 'protection'
        })
        
        logger.info(f"Registered {len(self.commands)} commands with {len(self.command_aliases)} aliases")
    
    async def handle_command(self, message: Message):
        """Handle incoming commands"""
        try:
            text = message.text
            
            # Check if message starts with command prefix
            if not text.startswith(self.config.COMMAND_PREFIX):
                return
            
            # Parse command and arguments
            parts = text[len(self.config.COMMAND_PREFIX):].split()
            if not parts:
                return
            
            command = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []
            
            # Resolve alias
            if command in self.command_aliases:
                command = self.command_aliases[command]
            
            # Check if command exists
            if command not in self.commands:
                await message.edit_text(f"❌ Unknown command: `{command}`\nUse `{self.config.COMMAND_PREFIX}help` to see available commands.")
                return
            
            # Log command usage
            if self.config.ENABLE_COMMAND_LOGGING:
                self.command_stats[command] = self.command_stats.get(command, 0) + 1
                logger.info(f"Command executed: {command} (args: {args})")
            
            # Execute command
            await self.commands[command](message, args)
            
        except Exception as e:
            logger.error(f"Error handling command: {e}")
            try:
                await message.edit_text(f"❌ Command execution failed: `{str(e)}`")
            except:
                pass
    
    async def _cmd_help(self, message, args):
        """Show help message"""
        if args and args[0] in self.commands:
            # Show help for specific command
            command = args[0]
            help_text = f"**🔧 Command: {self.config.COMMAND_PREFIX}{command}**\n\n"
            
            # Add command-specific help here
            command_help = {
                'ping': 'Check bot latency and status',
                'info': 'Show detailed bot information',
                'stats': 'Display usage statistics',
                'uptime': 'Show bot uptime',
                'sys': 'System information',
                'echo': 'Echo the provided text',
                'calc': 'Calculate mathematical expressions',
                'time': 'Show current time',
                'nexus': 'Show Nexus branding information'
            }
            
            help_text += command_help.get(command, 'No detailed help available for this command.')
            
        else:
            # Show general help
            help_text = f"""
**🤖 Nexus Userbot v{self.config.BOT_VERSION} - Command Help**

**📋 Basic Commands:**
`{self.config.COMMAND_PREFIX}ping` - Check bot status
`{self.config.COMMAND_PREFIX}info` - Bot information  
`{self.config.COMMAND_PREFIX}stats` - Usage statistics
`{self.config.COMMAND_PREFIX}uptime` - Bot uptime

**🖥️ System Commands:**
`{self.config.COMMAND_PREFIX}sys` - System information

**🛠️ Utility Commands:**
`{self.config.COMMAND_PREFIX}echo <text>` - Echo text
`{self.config.COMMAND_PREFIX}calc <expression>` - Calculator
`{self.config.COMMAND_PREFIX}time` - Current time

**⚡ Nexus Commands:**
`{self.config.COMMAND_PREFIX}nexus` - Nexus information

**📱 Created by @nexustech_dev**
Use `{self.config.COMMAND_PREFIX}help <command>` for detailed help.
            """.strip()
        
        await message.edit_text(help_text)
    
    async def _cmd_ping(self, message, args):
        """Ping command"""
        start_time = time.time()
        await message.edit_text("🏃‍♂️ Pinging...")
        end_time = time.time()
        
        ping_time = round((end_time - start_time) * 1000, 2)
        
        response = f"""
**🏓 Pong!**

⚡ **Response Time:** `{ping_time}ms`
🤖 **Bot Status:** `Online`
🔄 **Version:** `v{self.config.BOT_VERSION}`
🌟 **Nexus Userbot** - Running smoothly!

*Created by @nexustech_dev*
        """.strip()
        
        await message.edit_text(response)
    
    async def _cmd_info(self, message, args):
        """Bot information command"""
        me = await self.client.get_me()
        
        # Get system info
        system_info = self.utils.get_platform_info()
        
        info_text = f"""
**🤖 Nexus Userbot Information**

**👤 User Details:**
• **Name:** {me.first_name} {me.last_name or ''}
• **Username:** @{me.username or 'N/A'}
• **User ID:** `{me.id}`
• **Phone:** `{me.phone_number or 'Hidden'}`

**🔧 Bot Details:**
• **Version:** `v{self.config.BOT_VERSION}`
• **Instance ID:** `{self.fingerprint.generate_instance_id()[:16]}...`
• **Command Prefix:** `{self.config.COMMAND_PREFIX}`
• **Platform:** `{system_info['platform']}`

**📊 Statistics:**
• **Commands Used:** `{sum(self.command_stats.values())}`
• **Available Commands:** `{len(self.commands)}`
• **Command Aliases:** `{len(self.command_aliases)}`

**⚙️ Features:**
• **Auto Response:** `{'✅ Enabled' if self.config.ENABLE_AUTO_RESPONSE else '❌ Disabled'}`
• **Analytics:** `{'✅ Enabled' if self.config.ENABLE_ANALYTICS else '❌ Disabled'}`
• **Protection:** `{'✅ Enabled' if self.config.ENABLE_PROTECTION else '❌ Disabled'}`

**💎 Nexus Userbot v{self.config.BOT_VERSION}**
*Created by @nexustech_dev*
        """.strip()
        
        await message.edit_text(info_text)
    
    async def _cmd_stats(self, message, args):
        """Statistics command"""
        # Calculate uptime
        uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
        
        stats_text = f"""
**📊 Nexus Userbot Statistics**

**💻 System Stats:**
• **CPU Usage:** `{psutil.cpu_percent()}%`
• **RAM Usage:** `{psutil.virtual_memory().percent}%`
• **Disk Usage:** `{psutil.disk_usage('/').percent}%`
• **System Uptime:** `{str(uptime).split('.')[0]}`

**🤖 Bot Stats:**
• **Total Commands:** `{sum(self.command_stats.values())}`
• **Unique Commands:** `{len(self.command_stats)}`

**📈 Top Commands:**
        """.strip()
        
        # Add top 5 most used commands
        if self.command_stats:
            sorted_commands = sorted(self.command_stats.items(), key=lambda x: x[1], reverse=True)[:5]
            for i, (cmd, count) in enumerate(sorted_commands, 1):
                stats_text += f"\n{i}. `{cmd}` - {count} uses"
        else:
            stats_text += "\nNo commands used yet."
        
        stats_text += f"\n\n**🌟 Powered by Nexus Userbot v{self.config.BOT_VERSION}**"
        
        await message.edit_text(stats_text)
    
    async def _cmd_uptime(self, message, args):
        """Uptime command"""
        # Bot uptime
        bot_uptime = datetime.now() - self.start_time
        
        # System uptime
        system_uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
        
        uptime_text = f"""
**⏰ Uptime Information**

**🤖 Bot Uptime:**
`{str(bot_uptime).split('.')[0]}`

**💻 System Uptime:**
`{str(system_uptime).split('.')[0]}`

**📅 Current Time:**
`{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`

**🌟 Nexus Userbot - Always Running!**
        """.strip()
        
        await message.edit_text(uptime_text)
    
    async def _cmd_system(self, message, args):
        """System information command"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        system_text = f"""
**💻 System Information**

**🖥️ Hardware:**
• **CPU:** `{platform.processor() or 'Unknown'}`
• **CPU Usage:** `{cpu_percent}%`
• **CPU Cores:** `{psutil.cpu_count()}`

**🧠 Memory:**
• **Total RAM:** `{self.utils.format_bytes(memory.total)}`
• **Used RAM:** `{self.utils.format_bytes(memory.used)} ({memory.percent}%)`
• **Available RAM:** `{self.utils.format_bytes(memory.available)}`

**💾 Storage:**
• **Total Disk:** `{self.utils.format_bytes(disk.total)}`
• **Used Disk:** `{self.utils.format_bytes(disk.used)} ({disk.percent}%)`
• **Free Disk:** `{self.utils.format_bytes(disk.free)}`

**🐧 Operating System:**
• **OS:** `{platform.system()}`
• **Version:** `{platform.release()}`
• **Architecture:** `{platform.machine()}`
• **Python:** `{platform.python_version()}`

**🌟 Monitored by Nexus Userbot**
        """.strip()
        
        await message.edit_text(system_text)
    
    async def _cmd_echo(self, message, args):
        """Echo command"""
        if not args:
            await message.edit_text("❌ Please provide text to echo.\nUsage: `.echo <text>`")
            return
        
        text = " ".join(args)
        echo_text = f"🔊 **Echo:**\n{text}"
        
        await message.edit_text(echo_text)
    
    async def _cmd_calc(self, message, args):
        """Calculator command"""
        if not args:
            await message.edit_text("❌ Please provide an expression to calculate.\nUsage: `.calc <expression>`")
            return
        
        expression = " ".join(args)
        
        try:
            # Safe evaluation
            result = eval(expression, {"__builtins__": {}}, {
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow, "len": len
            })
            
            calc_text = f"""
**🧮 Calculator**

**Expression:** `{expression}`
**Result:** `{result}`

*Powered by Nexus Userbot*
            """.strip()
            
        except Exception as e:
            calc_text = f"❌ **Calculation Error:**\n`{str(e)}`"
        
        await message.edit_text(calc_text)
    
    async def _cmd_time(self, message, args):
        """Time command"""
        now = datetime.now()
        
        time_text = f"""
**🕐 Current Time**

**📅 Date:** `{now.strftime('%Y-%m-%d')}`
**⏰ Time:** `{now.strftime('%H:%M:%S')}`
**🌍 Timezone:** `{now.astimezone().tzname()}`
**📊 Unix Timestamp:** `{int(now.timestamp())}`

**🌟 Nexus Userbot Time Service**
        """.strip()
        
        await message.edit_text(time_text)
    
    async def _cmd_nexus(self, message, args):
        """Nexus information command"""
        nexus_text = f"""
**🌟 Nexus Userbot v{self.config.BOT_VERSION}**

**🛡️ Protected & Unique Features:**
• Advanced code protection system
• Deployment tracking & notifications
• Unique system fingerprinting
• Anti-tampering mechanisms
• Real-time analytics

**⚡ Technical Specifications:**
• Built with Pyrogram library
• Multi-platform deployment support
• Comprehensive command system
• Auto-response capabilities
• System monitoring tools

**👨‍💻 Created by @nexustech_dev**
**📄 License:** MIT with Attribution Requirements
**🔗 Repository:** https://github.com/nexustech-dev/nexus-userbot

**💎 This is a unique, protected userbot with distinctive features.**
*Unauthorized modifications are tracked and reported.*
        """.strip()
        
        await message.edit_text(nexus_text)

