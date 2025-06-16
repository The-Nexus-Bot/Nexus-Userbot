#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        NEXUS USERBOT MESSAGE HANDLERS                       ║
║                                                                              ║
║ Created by: @nexustech_dev                                                   ║
║ Copyright (c) 2025 NexusTech Development                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Set
from pyrogram.types import Message, User

logger = logging.getLogger(__name__)

class MessageHandler:
    """
    Handles incoming messages and auto-responses
    """
    
    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.last_responses: Dict[int, datetime] = {}
        self.flood_protection: Dict[int, list] = {}
        self.auto_response_users: Set[int] = set()
        
    async def handle_message(self, event):
        """Handle incoming messages"""
        try:
            # Skip if auto-response is disabled
            if not self.config.ENABLE_AUTO_RESPONSE:
                return
            
            # Skip if message is from self
            if event.is_outgoing:
                return
            
            # Get sender info
            sender = await event.get_sender()
            if not isinstance(sender, User):
                return
            
            # Skip if sender is in blacklist
            if str(sender.id) in self.config.BLACKLISTED_USERS:
                return
            
            # Check if sender is authorized (if authorization is enabled)
            if self.config.AUTHORIZED_USERS and str(sender.id) not in self.config.AUTHORIZED_USERS:
                return
            
            # Apply flood protection
            if self.config.FLOOD_PROTECTION and self._is_flooding(sender.id):
                logger.warning(f"Flood protection triggered for user {sender.id}")
                return
            
            # Check if we should send auto-response
            if await self._should_send_auto_response(event, sender):
                await self._send_auto_response(event, sender)
                
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    def _is_flooding(self, user_id: int) -> bool:
        """Check if user is flooding messages"""
        now = datetime.now()
        
        if user_id not in self.flood_protection:
            self.flood_protection[user_id] = []
        
        # Clean old messages (older than 1 minute)
        self.flood_protection[user_id] = [
            msg_time for msg_time in self.flood_protection[user_id]
            if now - msg_time < timedelta(minutes=1)
        ]
        
        # Add current message
        self.flood_protection[user_id].append(now)
        
        # Check if user sent more than 5 messages in the last minute
        return len(self.flood_protection[user_id]) > 5
    
    async def _should_send_auto_response(self, event, sender) -> bool:
        """Determine if auto-response should be sent"""
        # Check if we already responded to this user recently
        now = datetime.now()
        last_response = self.last_responses.get(sender.id)
        
        if last_response:
            time_diff = now - last_response
            if time_diff.total_seconds() < self.config.AUTO_RESPONSE_DELAY:
                return False
        
        # Check if this is a private message
        if not event.is_private:
            return False
        
        # Check if message mentions the bot or is a direct message
        return True
    
    async def _send_auto_response(self, event, sender):
        """Send auto-response message"""
        try:
            # Mark that we responded to this user
            self.last_responses[sender.id] = datetime.now()
            
            # Customize response message
            response = self.config.AUTO_RESPONSE_MESSAGE
            
            # Add some personalization
            if sender.first_name:
                response = f"Hi {sender.first_name}! {response}"
            
            # Add assistant bot reference
            if hasattr(self.config, 'BOT_USERNAME') and self.config.BOT_USERNAME:
                response += f"\n\n💬 **For quick assistance, chat with me at @{self.config.BOT_USERNAME}**"
            
            # Add Nexus branding
            response += "\n\n🤖 Powered by Nexus Userbot v2.0"
            response += "\n📧 Created by @nexustech_dev"
            
            # Send response
            await event.respond(response)
            
            logger.info(f"Auto-response sent to {sender.first_name} (@{sender.username})")
            
        except Exception as e:
            logger.error(f"Failed to send auto-response: {e}")
    
    async def enable_auto_response_for_user(self, user_id: int):
        """Enable auto-response for specific user"""
        self.auto_response_users.add(user_id)
        logger.info(f"Auto-response enabled for user {user_id}")
    
    async def disable_auto_response_for_user(self, user_id: int):
        """Disable auto-response for specific user"""
        self.auto_response_users.discard(user_id)
        logger.info(f"Auto-response disabled for user {user_id}")
    
    async def get_handler_stats(self) -> dict:
        """Get handler statistics"""
        return {
            'total_responses_sent': len(self.last_responses),
            'flood_protection_active': len(self.flood_protection),
            'auto_response_users': len(self.auto_response_users),
            'last_24h_responses': len([
                timestamp for timestamp in self.last_responses.values()
                if datetime.now() - timestamp < timedelta(hours=24)
            ])
        }
    
    def clear_handler_data(self):
        """Clear handler data (for maintenance)"""
        self.last_responses.clear()
        self.flood_protection.clear()
        self.auto_response_users.clear()
        logger.info("Handler data cleared")

class EventLogger:
    """
    Logs various events for analytics
    """
    
    def __init__(self, config):
        self.config = config
        self.events_log = []
        
    async def log_event(self, event_type: str, data: dict):
        """Log an event"""
        if not self.config.ENABLE_ANALYTICS:
            return
        
        event_data = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'data': data
        }
        
        self.events_log.append(event_data)
        
        # Keep only last 1000 events to prevent memory issues
        if len(self.events_log) > 1000:
            self.events_log = self.events_log[-1000:]
        
        logger.debug(f"Event logged: {event_type}")
    
    def get_events(self, event_type: str = None, limit: int = 100) -> list:
        """Get logged events"""
        events = self.events_log
        
        if event_type:
            events = [e for e in events if e['type'] == event_type]
        
        return events[-limit:]
    
    def get_event_stats(self) -> dict:
        """Get event statistics"""
        if not self.events_log:
            return {'total_events': 0}
        
        event_types = {}
        for event in self.events_log:
            event_type = event['type']
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        return {
            'total_events': len(self.events_log),
            'event_types': event_types,
            'oldest_event': self.events_log[0]['timestamp'] if self.events_log else None,
            'newest_event': self.events_log[-1]['timestamp'] if self.events_log else None
        }
