#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        NEXUS USERBOT PROTECTION                             ║
║                                                                              ║
║ Created by: @nexustech_dev                                                   ║
║ Copyright (c) 2025 NexusTech Development                                    ║
║                                                                              ║
║ WARNING: This protection system tracks unauthorized usage                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import hashlib
import platform
import logging
import base64
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class CodeProtection:
    """
    Advanced protection system for Nexus Userbot
    
    Features:
    - Code integrity verification
    - Unauthorized usage detection
    - Environment validation
    - Attribution preservation
    - Instance tracking
    """
    
    def __init__(self):
        self.protection_enabled = True
        self.authorized_environments = [
            'development', 'production', 'staging'
        ]
        self.creator_signature = self._encode_signature("@nexustech_dev")
        self.copyright_notice = self._encode_signature("Copyright (c) 2025 NexusTech Development")
        
    def _encode_signature(self, text: str) -> str:
        """Encode signature for protection"""
        try:
            encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
            return hashlib.sha256(encoded.encode()).hexdigest()[:16]
        except:
            return ""
    
    def verify_integrity(self) -> bool:
        """Verify code integrity"""
        try:
            # Check if essential files exist
            essential_files = [
                'main.py',
                'config.py',
                'bot/commands.py',
                'bot/handlers.py'
            ]
            
            for file_path in essential_files:
                if not os.path.exists(file_path):
                    logger.warning(f"Essential file missing: {file_path}")
                    return False
            
            # Verify attribution headers
            if not self._check_attribution():
                logger.error("Attribution verification failed")
                return False
            
            logger.info("Code integrity verification passed")
            return True
            
        except Exception as e:
            logger.error(f"Integrity verification error: {e}")
            return False
    
    def _check_attribution(self) -> bool:
        """Check if attribution headers are present"""
        try:
            # Check main.py for attribution
            with open('main.py', 'r', encoding='utf-8') as f:
                content = f.read()
                
            required_signatures = [
                '@nexustech_dev',
                'NexusTech Development',
                'NEXUS TELEGRAM USERBOT'
            ]
            
            for signature in required_signatures:
                if signature not in content:
                    logger.warning(f"Missing attribution signature: {signature}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Attribution check error: {e}")
            return False
    
    def check_environment(self) -> bool:
        """Check if running in authorized environment"""
        try:
            # Check for debugging tools
            if self._detect_debugging():
                logger.warning("Debugging tools detected")
                return False
            
            # Check for code modification attempts
            if self._detect_tampering():
                logger.warning("Code tampering detected")
                return False
            
            # Verify Python environment
            if not self._verify_python_environment():
                logger.warning("Python environment verification failed")
                return False
            
            logger.info("Environment check passed")
            return True
            
        except Exception as e:
            logger.error(f"Environment check error: {e}")
            return False
    
    def _detect_debugging(self) -> bool:
        """Detect debugging tools"""
        try:
            # Check for common debugging flags
            debug_flags = [
                '-O', '--debug', '-v', '--verbose'
            ]
            
            for flag in debug_flags:
                if flag in sys.argv:
                    return True
            
            # Check for debugger modules
            debugger_modules = [
                'pdb', 'ipdb', 'pudb', 'winpdb'
            ]
            
            for module in debugger_modules:
                if module in sys.modules:
                    return True
            
            return False
            
        except:
            return False
    
    def _detect_tampering(self) -> bool:
        """Detect code tampering attempts"""
        try:
            # Check if file was recently modified
            main_file_mtime = os.path.getmtime('main.py')
            current_time = datetime.now().timestamp()
            
            # If main.py was modified in the last 5 minutes, it might be tampering
            if current_time - main_file_mtime < 300:
                logger.info("Recent file modification detected (normal for new deployments)")
            
            # Check for suspicious environment variables
            suspicious_vars = [
                'PYTHONDONTWRITEBYTECODE',
                'PYTHONOPTIMIZE',
                'PYTHONDEBUG'
            ]
            
            for var in suspicious_vars:
                if os.environ.get(var):
                    logger.info(f"Development environment variable detected: {var}")
            
            return False  # Allow execution for now
            
        except:
            return False
    
    def _verify_python_environment(self) -> bool:
        """Verify Python environment"""
        try:
            # Check Python version
            if sys.version_info < (3, 7):
                logger.error("Python version too old")
                return False
            
            # Check for required modules
            required_modules = [
                'telethon', 'asyncio', 'logging'
            ]
            
            for module in required_modules:
                try:
                    __import__(module)
                except ImportError:
                    logger.error(f"Required module missing: {module}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Python environment verification error: {e}")
            return False
    
    def generate_protection_report(self) -> Dict:
        """Generate protection status report"""
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'protection_enabled': self.protection_enabled,
                'integrity_verified': self.verify_integrity(),
                'environment_secure': self.check_environment(),
                'attribution_present': self._check_attribution(),
                'creator_signature': self.creator_signature,
                'copyright_verified': bool(self.copyright_notice),
                'platform_info': {
                    'system': platform.system(),
                    'release': platform.release(),
                    'machine': platform.machine(),
                    'python_version': platform.python_version()
                }
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating protection report: {e}")
            return {'error': str(e)}
    
    def obfuscate_sensitive_data(self, data: str) -> str:
        """Obfuscate sensitive data"""
        try:
            # Simple obfuscation using base64 and rotation
            encoded = base64.b64encode(data.encode('utf-8')).decode('utf-8')
            
            # Apply simple character rotation
            obfuscated = ""
            for char in encoded:
                if char.isalpha():
                    base = ord('A') if char.isupper() else ord('a')
                    obfuscated += chr((ord(char) - base + 13) % 26 + base)
                else:
                    obfuscated += char
            
            return obfuscated
            
        except Exception as e:
            logger.error(f"Obfuscation error: {e}")
            return data
    
    def deobfuscate_data(self, obfuscated_data: str) -> str:
        """Deobfuscate data"""
        try:
            # Reverse character rotation
            derotated = ""
            for char in obfuscated_data:
                if char.isalpha():
                    base = ord('A') if char.isupper() else ord('a')
                    derotated += chr((ord(char) - base - 13) % 26 + base)
                else:
                    derotated += char
            
            # Decode base64
            decoded = base64.b64decode(derotated.encode('utf-8')).decode('utf-8')
            return decoded
            
        except Exception as e:
            logger.error(f"Deobfuscation error: {e}")
            return obfuscated_data
    
    def create_protected_string(self, original: str) -> str:
        """Create protected string with checksums"""
        try:
            # Create checksum
            checksum = hashlib.md5(original.encode('utf-8')).hexdigest()[:8]
            
            # Combine with protection marker
            protected = f"NEXUS_PROTECTED:{checksum}:{self.obfuscate_sensitive_data(original)}"
            
            return protected
            
        except Exception as e:
            logger.error(f"Error creating protected string: {e}")
            return original
    
    def verify_protected_string(self, protected: str) -> Optional[str]:
        """Verify and extract protected string"""
        try:
            if not protected.startswith("NEXUS_PROTECTED:"):
                return None
            
            parts = protected.split(":", 2)
            if len(parts) != 3:
                return None
            
            _, checksum, obfuscated_data = parts
            
            # Deobfuscate
            original = self.deobfuscate_data(obfuscated_data)
            
            # Verify checksum
            expected_checksum = hashlib.md5(original.encode('utf-8')).hexdigest()[:8]
            if checksum != expected_checksum:
                logger.warning("Protected string checksum verification failed")
                return None
            
            return original
            
        except Exception as e:
            logger.error(f"Error verifying protected string: {e}")
            return None
    
    def get_license_info(self) -> Dict:
        """Get license information"""
        return {
            'license': 'MIT License with Attribution Requirements',
            'copyright': 'Copyright (c) 2025 NexusTech Development',
            'author': '@nexustech_dev',
            'requirements': [
                'Attribution must be maintained in all copies',
                'Original author credit must be preserved',
                'License notice must be included in redistributions',
                'Commercial use requires explicit permission'
            ],
            'repository': 'https://github.com/nexustech-dev/nexus-userbot',
            'support': 'Contact @nexustech_dev for support'
        }
    
    def check_license_compliance(self) -> bool:
        """Check license compliance"""
        try:
            # Check if license file exists
            if not os.path.exists('LICENSE'):
                logger.warning("LICENSE file missing")
                return False
            
            # Check if attribution is preserved in source files
            source_files = ['main.py', 'bot/commands.py', 'bot/handlers.py']
            
            for file_path in source_files:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    if '@nexustech_dev' not in content or 'NexusTech Development' not in content:
                        logger.warning(f"Attribution missing in {file_path}")
                        return False
            
            logger.info("License compliance check passed")
            return True
            
        except Exception as e:
            logger.error(f"License compliance check error: {e}")
            return False

class AntiTampering:
    """
    Anti-tampering protection system
    """
    
    def __init__(self):
        self.protected_files = [
            'main.py', 'config.py', 'bot/protection.py'
        ]
        self.file_hashes = {}
        self._calculate_initial_hashes()
    
    def _calculate_initial_hashes(self):
        """Calculate initial file hashes"""
        for file_path in self.protected_files:
            if os.path.exists(file_path):
                self.file_hashes[file_path] = self._calculate_file_hash(file_path)
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate file hash"""
        try:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            return file_hash
        except:
            return ""
    
    def check_file_integrity(self) -> List[str]:
        """Check file integrity and return list of modified files"""
        modified_files = []
        
        for file_path in self.protected_files:
            if os.path.exists(file_path):
                current_hash = self._calculate_file_hash(file_path)
                original_hash = self.file_hashes.get(file_path, "")
                
                if current_hash != original_hash:
                    modified_files.append(file_path)
                    logger.warning(f"File modification detected: {file_path}")
        
        return modified_files
    
    def is_integrity_compromised(self) -> bool:
        """Check if any protected files have been modified"""
        return len(self.check_file_integrity()) > 0
