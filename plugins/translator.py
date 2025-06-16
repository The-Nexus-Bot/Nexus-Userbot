"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         TRANSLATOR PLUGIN                                   ║
║                                                                              ║
║ Created by: @nexustech_dev                                                   ║
║ Copyright (c) 2025 NexusTech Development                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from pyrogram import filters
from pyrogram.types import Message
import asyncio
import aiohttp
import json

async def translate_handler(client, message: Message):
    """Translate text using Google Translate API"""
    try:
        args = message.text.split(maxsplit=2)[1:]
        
        if len(args) < 2:
            await message.edit("""
**🌐 TRANSLATOR USAGE**

`.tr <lang_code> <text>` - Translate text
`.tr <lang_code>` - Translate replied message

**Language Codes:**
• en - English
• es - Spanish  
• fr - French
• de - German
• it - Italian
• pt - Portuguese
• ru - Russian
• ar - Arabic
• hi - Hindi
• ja - Japanese
• ko - Korean
• zh - Chinese

**Example:** `.tr en Hola mundo`
            """)
            return
            
        target_lang = args[0].lower()
        
        # Get text to translate
        if len(args) > 1:
            text_to_translate = args[1]
        elif message.reply_to_message and message.reply_to_message.text:
            text_to_translate = message.reply_to_message.text
        else:
            await message.edit("❌ **No text to translate**\nProvide text or reply to a message")
            return
            
        await message.edit(f"🌐 **Translating to {target_lang.upper()}...**")
        
        # Use Google Translate API (free endpoint)
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            'client': 'gtx',
            'sl': 'auto',
            'tl': target_lang,
            'dt': 't',
            'q': text_to_translate
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    result = await response.text()
                    # Parse the response
                    translation_data = json.loads(result)
                    translated_text = translation_data[0][0][0]
                    detected_lang = translation_data[2]
                    
                    translation_result = f"""
🌐 **TRANSLATION RESULT**

**Original ({detected_lang.upper()}):**
{text_to_translate}

**Translated ({target_lang.upper()}):**
{translated_text}

Powered by Google Translate
                    """
                    
                    await message.edit(translation_result)
                else:
                    await message.edit("❌ **Translation failed**\nCheck language code and try again")
                    
    except Exception as e:
        await message.edit(f"❌ **Translation error:** {str(e)}")

def register_plugin(client):
    """Register translator plugin"""
    @client.on_message(filters.outgoing & filters.text & filters.command(["tr", "translate"], prefixes="."))
    async def translate_command(client, message: Message):
        await translate_handler(client, message)