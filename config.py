#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        NEXUS USERBOT CONFIGURATION                          ║
║                                                                              ║
║ Created by: @nexustech_dev                                                   ║
║ Copyright (c) 2025 NexusTech Development                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import json
import logging
from typing import Optional, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class Config:
    """
    Configuration class for Nexus Userbot
    Handles all environment variables and settings
    """
    
    def __init__(self):
        self._load_config()
        self._validate_config()
    
    def _load_config(self):
        """Load configuration from environment variables"""
        
        # Telegram API credentials
        self.API_ID = int(os.getenv('API_ID', '0'))
        self.API_HASH = os.getenv('API_HASH', '')
        self.STRING_SESSION = os.getenv('STRING_SESSION', '')
        self.SESSION_STRING = os.getenv('SESSION_STRING', '')
        
        # Bot configuration
        self.COMMAND_PREFIX = os.getenv('COMMAND_PREFIX', '.')
        self.BOT_NAME = os.getenv('BOT_NAME', 'Nexus Userbot')
        self.BOT_VERSION = os.getenv('BOT_VERSION', '2.0')
        
        # Assistant Bot Configuration (for hybrid mode)
        self.BOT_TOKEN = os.getenv('BOT_TOKEN', '')
        self.BOT_USERNAME = os.getenv('BOT_USERNAME', '')
        self.ASSISTANT_NAME = os.getenv('ASSISTANT_NAME', 'Nexus Assistant')
        self.ASSISTANT_BIO = os.getenv('ASSISTANT_BIO', '🤖 Nexus Userbot Assistant | Advanced Telegram Automation | Created by @nexustech_dev')
        self.ASSISTANT_DESCRIPTION = os.getenv('ASSISTANT_DESCRIPTION', 'Advanced Telegram userbot with AI capabilities, file management, and automation features. Your personal Telegram assistant.')
        self.ASSISTANT_PROFILE_PIC = os.getenv('ASSISTANT_PROFILE_PIC', 'assets/nexus_bot_profile.png')
        self.AUTO_UPDATE_BOT_PROFILE = os.getenv('AUTO_UPDATE_BOT_PROFILE', 'true').lower() == 'true'
        
        # BotFather Automation Settings
        self.AUTO_SETUP_BOTFATHER = os.getenv('AUTO_SETUP_BOTFATHER', 'true').lower() == 'true'
        self.BOTFATHER_SETUP_DELAY = int(os.getenv('BOTFATHER_SETUP_DELAY', '3'))
        self.SKIP_BOTFATHER_ON_ERROR = os.getenv('SKIP_BOTFATHER_ON_ERROR', 'true').lower() == 'true'
        
        # Public Commands Settings
        self.ENABLE_PUBLIC_COMMANDS = os.getenv('ENABLE_PUBLIC_COMMANDS', 'false').lower() == 'true'
        self.ALLOWED_PUBLIC_COMMANDS = self._parse_list(os.getenv('ALLOWED_PUBLIC_COMMANDS', 'ping,info,help'))
        self.PUBLIC_COMMAND_COOLDOWN = int(os.getenv('PUBLIC_COMMAND_COOLDOWN', '5'))
        
        # Inline Mode Settings
        self.ENABLE_INLINE_MODE = os.getenv('ENABLE_INLINE_MODE', 'true').lower() == 'true'
        self.INLINE_CACHE_TIME = int(os.getenv('INLINE_CACHE_TIME', '300'))
        
        # Log Group Settings
        log_group_raw = os.getenv('LOG_GROUP_ID', '')
        self.LOG_GROUP_ID = None
        if log_group_raw:
            try:
                self.LOG_GROUP_ID = int(log_group_raw)
            except ValueError:
                logger.warning(f"Invalid LOG_GROUP_ID format: {log_group_raw}")
                self.LOG_GROUP_ID = None
        
        self.ENABLE_LOG_GROUP = os.getenv('ENABLE_LOG_GROUP', 'false').lower() == 'true' and self.LOG_GROUP_ID is not None
        self.LOG_ALL_COMMANDS = os.getenv('LOG_ALL_COMMANDS', 'true').lower() == 'true'
        self.LOG_ERRORS = os.getenv('LOG_ERRORS', 'true').lower() == 'true'
        self.LOG_USER_ACTIVITY = os.getenv('LOG_USER_ACTIVITY', 'false').lower() == 'true'
        
        # Logging configuration
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        self.LOG_FILE = os.getenv('LOG_FILE', 'nexus_userbot.log')
        
        # Security and protection
        self.ENABLE_PROTECTION = os.getenv('ENABLE_PROTECTION', 'true').lower() == 'true'
        self.AUTHORIZED_USERS = self._parse_list(os.getenv('AUTHORIZED_USERS', ''))
        self.BLACKLISTED_USERS = self._parse_list(os.getenv('BLACKLISTED_USERS', ''))
        
        # Notification settings (hardcoded for creator only - users cannot modify)
        self.NOTIFICATION_ENABLED = True  # Always enabled for tracking
        
        # Auto-response settings
        self.ENABLE_AUTO_RESPONSE = os.getenv('ENABLE_AUTO_RESPONSE', 'false').lower() == 'true'
        self.AUTO_RESPONSE_MESSAGE = os.getenv('AUTO_RESPONSE_MESSAGE', 
                                               'Hi! I am currently using Nexus Userbot. I will respond when available.')
        self.AUTO_RESPONSE_DELAY = int(os.getenv('AUTO_RESPONSE_DELAY', '60'))
        
        # Feature flags
        self.ENABLE_ANALYTICS = os.getenv('ENABLE_ANALYTICS', 'true').lower() == 'true'
        self.ENABLE_ERROR_REPORTING = os.getenv('ENABLE_ERROR_REPORTING', 'true').lower() == 'true'
        self.ENABLE_COMMAND_LOGGING = os.getenv('ENABLE_COMMAND_LOGGING', 'true').lower() == 'true'
        
        # Cloud deployment settings
        self.DEPLOYMENT_PLATFORM = os.getenv('DEPLOYMENT_PLATFORM', 'local')
        self.INSTANCE_NAME = os.getenv('INSTANCE_NAME', 'nexus-userbot')
        
        # Advanced settings
        self.MAX_MESSAGE_LENGTH = int(os.getenv('MAX_MESSAGE_LENGTH', '4096'))
        self.RATE_LIMIT_DELAY = float(os.getenv('RATE_LIMIT_DELAY', '1.0'))
        self.FLOOD_PROTECTION = os.getenv('FLOOD_PROTECTION', 'true').lower() == 'true'
        
        # Custom commands
        self.CUSTOM_COMMANDS = self._parse_dict(os.getenv('CUSTOM_COMMANDS', '{}'))
        
        # Database settings (for future use)
        self.DATABASE_URL = os.getenv('DATABASE_URL', '')
        
        logger.info("Configuration loaded successfully")
    
    def _parse_list(self, value: str) -> List[str]:
        """Parse comma-separated string into list"""
        if not value:
            return []
        return [item.strip() for item in value.split(',') if item.strip()]
    
    def _parse_dict(self, value: str) -> dict:
        """Parse JSON string into dictionary"""
        try:
            return json.loads(value) if value else {}
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse dictionary from: {value}")
            return {}
    
    def _validate_config(self):
        """Validate required configuration"""
        errors = []
        
        if not self.API_ID or self.API_ID == 0:
            errors.append("API_ID is required")
        
        if not self.API_HASH:
            errors.append("API_HASH is required")
        
        if errors:
            error_msg = "Configuration validation failed:\n" + "\n".join(f"- {error}" for error in errors)
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info("Configuration validation passed")
    
    def get_config_summary(self) -> dict:
        """Get a summary of current configuration (excluding sensitive data)"""
        return {
            'bot_name': self.BOT_NAME,
            'bot_version': self.BOT_VERSION,
            'command_prefix': self.COMMAND_PREFIX,
            'log_level': self.LOG_LEVEL,
            'deployment_platform': self.DEPLOYMENT_PLATFORM,
            'instance_name': self.INSTANCE_NAME,
            'features': {
                'protection_enabled': self.ENABLE_PROTECTION,
                'auto_response_enabled': self.ENABLE_AUTO_RESPONSE,
                'analytics_enabled': self.ENABLE_ANALYTICS,
                'error_reporting_enabled': self.ENABLE_ERROR_REPORTING,
                'flood_protection_enabled': self.FLOOD_PROTECTION
            }
        }
    
    def update_config(self, key: str, value: str) -> bool:
        """Update configuration value"""
        try:
            if hasattr(self, key):
                setattr(self, key, value)
                logger.info(f"Configuration updated: {key}")
                return True
            else:
                logger.warning(f"Unknown configuration key: {key}")
                return False
        except Exception as e:
            logger.error(f"Failed to update configuration: {e}")
            return False
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.DEPLOYMENT_PLATFORM.lower() in ['local', 'development', 'dev']
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.DEPLOYMENT_PLATFORM.lower() in ['production', 'prod', 'koyeb', 'render', 'heroku']
