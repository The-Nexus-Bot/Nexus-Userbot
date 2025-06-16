"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         NEXUS PLUGIN MANAGER                                ║
║                                                                              ║
║ Created by: @nexustech_dev                                                   ║
║ Copyright (c) 2025 NexusTech Development                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import importlib.util
import inspect
from typing import Dict, List, Optional
import aiohttp
import asyncio

class PluginManager:
    """
    Manages plugin installation, loading, and execution for Nexus Userbot
    """
    
    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.plugins_dir = "plugins"
        self.loaded_plugins = {}
        self.available_plugins = {
            "webshot": {
                "description": "Take website screenshots",
                "url": "https://raw.githubusercontent.com/The-Nexus-Bot/Nexus-Plugins/main/webshot.py",
                "commands": ["webshot"],
                "dependencies": ["aiohttp"]
            },
            "translator": {
                "description": "Text translation using Google Translate",
                "url": "https://raw.githubusercontent.com/The-Nexus-Bot/Nexus-Plugins/main/translator.py",
                "commands": ["tr", "translate"],
                "dependencies": ["aiohttp"]
            },
            "weather": {
                "description": "Weather information",
                "url": "https://raw.githubusercontent.com/The-Nexus-Bot/Nexus-Plugins/main/weather.py",
                "commands": ["weather"],
                "dependencies": ["aiohttp"]
            },
            "qrcode": {
                "description": "QR code generator",
                "url": "https://raw.githubusercontent.com/The-Nexus-Bot/Nexus-Plugins/main/qrcode.py",
                "commands": ["qr"],
                "dependencies": ["qrcode", "pillow"]
            },
            "sticker_maker": {
                "description": "Create custom stickers from text with various styles",
                "url": "https://raw.githubusercontent.com/The-Nexus-Bot/Nexus-Plugins/main/sticker_maker.py",
                "commands": ["sticker", "stickerpack"],
                "dependencies": ["pillow"]
            },
            "group_manager": {
                "description": "Leave groups and manage group participation",
                "url": "https://raw.githubusercontent.com/The-Nexus-Bot/Nexus-Plugins/main/group_manager.py",
                "commands": ["leave", "leaveall", "groups"],
                "dependencies": []
            }
        }
        
        # Ensure plugins directory exists
        os.makedirs(self.plugins_dir, exist_ok=True)
    
    async def list_available_plugins(self) -> Dict:
        """Get list of available plugins"""
        return self.available_plugins
    
    async def list_installed_plugins(self) -> List[str]:
        """Get list of installed plugins"""
        if not os.path.exists(self.plugins_dir):
            return []
        
        installed = []
        for file in os.listdir(self.plugins_dir):
            if file.endswith('.py') and file != '__init__.py':
                installed.append(file[:-3])  # Remove .py extension
        return installed
    
    async def install_plugin_from_url(self, plugin_name: str) -> bool:
        """Install plugin from URL"""
        try:
            if plugin_name not in self.available_plugins:
                return False
            
            plugin_info = self.available_plugins[plugin_name]
            plugin_url = plugin_info["url"]
            
            async with aiohttp.ClientSession() as session:
                async with session.get(plugin_url) as response:
                    if response.status == 200:
                        plugin_code = await response.text()
                        
                        # Save plugin file
                        plugin_path = os.path.join(self.plugins_dir, f"{plugin_name}.py")
                        with open(plugin_path, 'w', encoding='utf-8') as f:
                            f.write(plugin_code)
                        
                        return True
            return False
            
        except Exception as e:
            print(f"Error installing plugin {plugin_name}: {e}")
            return False
    
    async def install_plugin_from_file(self, file_path: str, plugin_name: str) -> bool:
        """Install plugin from local file"""
        try:
            if not os.path.exists(file_path):
                return False
            
            # Read plugin file
            with open(file_path, 'r', encoding='utf-8') as f:
                plugin_code = f.read()
            
            # Validate plugin structure
            if not self._validate_plugin_code(plugin_code):
                return False
            
            # Save to plugins directory
            plugin_path = os.path.join(self.plugins_dir, f"{plugin_name}.py")
            with open(plugin_path, 'w', encoding='utf-8') as f:
                f.write(plugin_code)
            
            return True
            
        except Exception as e:
            print(f"Error installing plugin from file: {e}")
            return False
    
    def _validate_plugin_code(self, code: str) -> bool:
        """Validate plugin code structure"""
        try:
            # Check if code contains required elements
            required_elements = [
                "def register_plugin(",
                "from pyrogram",
                "async def"
            ]
            
            for element in required_elements:
                if element not in code:
                    return False
            
            return True
        except:
            return False
    
    async def load_plugin(self, plugin_name: str) -> bool:
        """Load a plugin dynamically"""
        try:
            plugin_path = os.path.join(self.plugins_dir, f"{plugin_name}.py")
            if not os.path.exists(plugin_path):
                return False
            
            # Import plugin module
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Register plugin with client
            if hasattr(module, 'register_plugin'):
                module.register_plugin(self.client)
                self.loaded_plugins[plugin_name] = module
                return True
            
            return False
            
        except Exception as e:
            print(f"Error loading plugin {plugin_name}: {e}")
            return False
    
    async def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin"""
        try:
            if plugin_name in self.loaded_plugins:
                del self.loaded_plugins[plugin_name]
                return True
            return False
        except Exception as e:
            print(f"Error unloading plugin {plugin_name}: {e}")
            return False
    
    async def remove_plugin(self, plugin_name: str) -> bool:
        """Remove plugin file"""
        try:
            plugin_path = os.path.join(self.plugins_dir, f"{plugin_name}.py")
            if os.path.exists(plugin_path):
                os.remove(plugin_path)
                # Also unload if loaded
                await self.unload_plugin(plugin_name)
                return True
            return False
        except Exception as e:
            print(f"Error removing plugin {plugin_name}: {e}")
            return False
    
    async def load_all_plugins(self):
        """Load all installed plugins"""
        installed_plugins = await self.list_installed_plugins()
        loaded_count = 0
        
        for plugin_name in installed_plugins:
            if await self.load_plugin(plugin_name):
                loaded_count += 1
        
        return loaded_count
    
    def get_plugin_info(self, plugin_name: str) -> Optional[Dict]:
        """Get information about a plugin"""
        if plugin_name in self.available_plugins:
            return self.available_plugins[plugin_name]
        return None