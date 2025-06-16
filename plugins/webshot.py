"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         WEBSHOT PLUGIN                                      ║
║                                                                              ║
║ Created by: @nexustech_dev                                                   ║
║ Copyright (c) 2025 NexusTech Development                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from pyrogram import filters
from pyrogram.types import Message
import asyncio
import aiohttp
import os

async def webshot_handler(client, message: Message):
    """Take screenshot of website"""
    try:
        args = message.text.split()[1:]
        if not args:
            await message.edit("Usage: `.webshot <url>`\nExample: `.webshot https://google.com`")
            return
            
        url = args[0]
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        await message.edit(f"📸 Taking screenshot of: {url}")
        
        # Use a screenshot API service
        api_url = f"https://api.screenshotone.com/take?url={url}&viewport_width=1920&viewport_height=1080&device_scale_factor=1&format=png&block_ads=true&block_cookie_banners=true"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    screenshot_data = await response.read()
                    
                    # Save screenshot temporarily
                    screenshot_path = f"screenshot_{message.id}.png"
                    with open(screenshot_path, 'wb') as f:
                        f.write(screenshot_data)
                    
                    # Send screenshot
                    await message.delete()
                    await client.send_photo(
                        chat_id=message.chat.id,
                        photo=screenshot_path,
                        caption=f"📸 **Website Screenshot**\n\n🔗 **URL**: {url}\n📱 **Resolution**: 1920x1080"
                    )
                    
                    # Clean up
                    os.remove(screenshot_path)
                else:
                    await message.edit("❌ Failed to take screenshot. Please check the URL.")
    except Exception as e:
        await message.edit(f"❌ Error: {str(e)}")

# Plugin registration
def register_plugin(client):
    """Register webshot plugin"""
    @client.on_message(filters.outgoing & filters.text & filters.command("webshot", prefixes="."))
    async def webshot_command(client, message: Message):
        await webshot_handler(client, message)