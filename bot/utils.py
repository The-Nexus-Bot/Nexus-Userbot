#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          NEXUS USERBOT UTILITIES                            ║
║                                                                              ║
║ Created by: @nexustech_dev                                                   ║
║ Copyright (c) 2025 NexusTech Development                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import platform
import logging
import hashlib
import base64
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class BotUtils:
    """
    Utility functions for the Nexus Userbot
    """
    
    @staticmethod
    def format_bytes(bytes_value: int) -> str:
        """Format bytes into human readable format"""
        try:
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if bytes_value < 1024.0:
                    return f"{bytes_value:.1f} {unit}"
                bytes_value /= 1024.0
            return f"{bytes_value:.1f} PB"
        except:
            return "0 B"
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format duration in seconds to human readable format"""
        try:
            if seconds < 60:
                return f"{seconds:.1f} seconds"
            elif seconds < 3600:
                minutes = seconds / 60
                return f"{minutes:.1f} minutes"
            elif seconds < 86400:
                hours = seconds / 3600
                return f"{hours:.1f} hours"
            else:
                days = seconds / 86400
                return f"{days:.1f} days"
        except:
            return "0 seconds"
    
    @staticmethod
    def get_platform_info() -> Dict[str, str]:
        """Get platform information"""
        try:
            return {
                'platform': platform.system(),
                'platform_release': platform.release(),
                'platform_version': platform.version(),
                'architecture': platform.machine(),
                'hostname': platform.node(),
                'processor': platform.processor(),
                'python_version': platform.python_version(),
                'python_implementation': platform.python_implementation()
            }
        except Exception as e:
            logger.error(f"Error getting platform info: {e}")
            return {'platform': 'Unknown'}
    
    @staticmethod
    def generate_hash(data: str, algorithm: str = 'sha256') -> str:
        """Generate hash from data"""
        try:
            hash_obj = hashlib.new(algorithm)
            hash_obj.update(data.encode('utf-8'))
            return hash_obj.hexdigest()
        except Exception as e:
            logger.error(f"Error generating hash: {e}")
            return ""
    
    @staticmethod
    def encode_base64(data: str) -> str:
        """Encode string to base64"""
        try:
            encoded_bytes = base64.b64encode(data.encode('utf-8'))
            return encoded_bytes.decode('utf-8')
        except Exception as e:
            logger.error(f"Error encoding base64: {e}")
            return ""
    
    @staticmethod
    def decode_base64(data: str) -> str:
        """Decode base64 string"""
        try:
            decoded_bytes = base64.b64decode(data.encode('utf-8'))
            return decoded_bytes.decode('utf-8')
        except Exception as e:
            logger.error(f"Error decoding base64: {e}")
            return ""
    
    @staticmethod
    def safe_json_loads(json_str: str, default: Any = None) -> Any:
        """Safely load JSON with default fallback"""
        try:
            return json.loads(json_str)
        except (json.JSONDecodeError, TypeError):
            return default
    
    @staticmethod
    def safe_json_dumps(data: Any, default: str = "{}") -> str:
        """Safely dump JSON with default fallback"""
        try:
            return json.dumps(data, indent=2, ensure_ascii=False)
        except (TypeError, ValueError):
            return default
    
    @staticmethod
    def validate_command_args(args: List[str], min_args: int = 0, max_args: Optional[int] = None) -> bool:
        """Validate command arguments"""
        if len(args) < min_args:
            return False
        if max_args is not None and len(args) > max_args:
            return False
        return True
    
    @staticmethod
    def sanitize_input(text: str, max_length: int = 4096) -> str:
        """Sanitize user input"""
        try:
            # Remove potential harmful characters
            sanitized = text.replace('<', '&lt;').replace('>', '&gt;')
            
            # Limit length
            if len(sanitized) > max_length:
                sanitized = sanitized[:max_length-3] + "..."
            
            return sanitized
        except:
            return ""
    
    @staticmethod
    def format_error_message(error: Exception, context: str = "") -> str:
        """Format error message for display"""
        error_type = type(error).__name__
        error_msg = str(error)
        
        formatted = f"**❌ {error_type}**"
        if context:
            formatted += f"\n**Context:** {context}"
        formatted += f"\n**Error:** `{error_msg}`"
        
        return formatted
    
    @staticmethod
    def create_progress_bar(current: int, total: int, length: int = 20) -> str:
        """Create a text progress bar"""
        try:
            if total == 0:
                return "▱" * length
            
            progress = current / total
            filled_length = int(length * progress)
            
            bar = "▰" * filled_length + "▱" * (length - filled_length)
            percentage = f"{progress * 100:.1f}%"
            
            return f"{bar} {percentage}"
        except:
            return "▱" * length
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """Get file size safely"""
        try:
            return os.path.getsize(file_path)
        except (OSError, IOError):
            return 0
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if URL is valid"""
        try:
            import re
            url_pattern = re.compile(
                r'^https?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            return url_pattern.match(url) is not None
        except:
            return False
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
        """Truncate text to specified length"""
        try:
            if len(text) <= max_length:
                return text
            return text[:max_length - len(suffix)] + suffix
        except:
            return ""
    
    @staticmethod
    def get_timestamp() -> str:
        """Get current timestamp"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def get_iso_timestamp() -> str:
        """Get current ISO timestamp"""
        return datetime.now().isoformat()

class TextFormatter:
    """
    Text formatting utilities for Telegram messages
    """
    
    @staticmethod
    def bold(text: str) -> str:
        """Format text as bold"""
        return f"**{text}**"
    
    @staticmethod
    def italic(text: str) -> str:
        """Format text as italic"""
        return f"__{text}__"
    
    @staticmethod
    def code(text: str) -> str:
        """Format text as inline code"""
        return f"`{text}`"
    
    @staticmethod
    def code_block(text: str, language: str = "") -> str:
        """Format text as code block"""
        return f"```{language}\n{text}\n```"
    
    @staticmethod
    def link(text: str, url: str) -> str:
        """Format text as link"""
        return f"[{text}]({url})"
    
    @staticmethod
    def strikethrough(text: str) -> str:
        """Format text as strikethrough"""
        return f"~~{text}~~"
    
    @staticmethod
    def underline(text: str) -> str:
        """Format text as underline"""
        return f"__{text}__"
    
    @staticmethod
    def create_table(headers: List[str], rows: List[List[str]]) -> str:
        """Create a simple text table"""
        try:
            # Calculate column widths
            widths = [len(header) for header in headers]
            for row in rows:
                for i, cell in enumerate(row):
                    if i < len(widths):
                        widths[i] = max(widths[i], len(str(cell)))
            
            # Create table
            table = ""
            
            # Header
            header_row = " | ".join(header.ljust(widths[i]) for i, header in enumerate(headers))
            table += header_row + "\n"
            
            # Separator
            separator = " | ".join("-" * width for width in widths)
            table += separator + "\n"
            
            # Rows
            for row in rows:
                row_str = " | ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row))
                table += row_str + "\n"
            
            return f"```\n{table.strip()}\n```"
        except:
            return "Error creating table"

class FileUtils:
    """
    File operation utilities
    """
    
    @staticmethod
    def read_file(file_path: str, encoding: str = 'utf-8') -> Optional[str]:
        """Read file content safely"""
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except (IOError, OSError) as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return None
    
    @staticmethod
    def write_file(file_path: str, content: str, encoding: str = 'utf-8') -> bool:
        """Write content to file safely"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            return True
        except (IOError, OSError) as e:
            logger.error(f"Error writing file {file_path}: {e}")
            return False
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Check if file exists"""
        return os.path.isfile(file_path)
    
    @staticmethod
    def create_directory(dir_path: str) -> bool:
        """Create directory if it doesn't exist"""
        try:
            os.makedirs(dir_path, exist_ok=True)
            return True
        except OSError as e:
            logger.error(f"Error creating directory {dir_path}: {e}")
            return False

class ValidationUtils:
    """
    Input validation utilities
    """
    
    @staticmethod
    def is_valid_telegram_username(username: str) -> bool:
        """Validate Telegram username format"""
        try:
            import re
            pattern = r'^@?[a-zA-Z][a-zA-Z0-9_]{4,31}$'
            username = username.lstrip('@')
            return bool(re.match(pattern, username))
        except:
            return False
    
    @staticmethod
    def is_valid_user_id(user_id: str) -> bool:
        """Validate Telegram user ID"""
        try:
            user_id_int = int(user_id)
            return 0 < user_id_int < 10**12  # Reasonable range for Telegram user IDs
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def is_valid_chat_id(chat_id: str) -> bool:
        """Validate Telegram chat ID"""
        try:
            chat_id_int = int(chat_id)
            return -10**15 < chat_id_int < 10**12  # Range for Telegram chat IDs
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe file operations"""
        try:
            import re
            # Remove or replace invalid characters
            sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
            sanitized = sanitized.strip('. ')
            return sanitized[:255]  # Limit filename length
        except:
            return "unknown_file"
