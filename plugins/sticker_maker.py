"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         NEXUS STICKER MAKER PLUGIN                          ║
║                                                                              ║
║ Created by: @nexustech_dev                                                   ║
║ Copyright (c) 2025 NexusTech Development                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import io
import textwrap
from PIL import Image, ImageDraw, ImageFont
import asyncio
from pyrogram import filters
from pyrogram.types import Message

# Plugin metadata
__plugin_name__ = "Sticker Maker"
__plugin_description__ = "Create custom stickers from text with various styles"
__plugin_version__ = "1.0.0"
__plugin_commands__ = [".sticker", ".stickerpack"]

def get_font_size_for_text(text, max_width, max_height, font_path):
    """Calculate optimal font size for text to fit within dimensions"""
    font_size = 100
    while font_size > 10:
        try:
            font = ImageFont.truetype(font_path, font_size)
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            if text_width <= max_width and text_height <= max_height:
                return font_size
        except:
            pass
        font_size -= 5
    return 20

def create_text_sticker(text, style="default"):
    """Create a sticker image from text"""
    # Sticker dimensions (512x512 is standard)
    width, height = 512, 512
    
    # Style configurations
    styles = {
        "default": {
            "bg_color": (255, 255, 255, 0),  # Transparent
            "text_color": (0, 0, 0, 255),    # Black
            "font_size": 60,
            "stroke_width": 0,
            "stroke_color": (255, 255, 255, 255)
        },
        "bold": {
            "bg_color": (255, 255, 255, 0),
            "text_color": (0, 0, 0, 255),
            "font_size": 70,
            "stroke_width": 3,
            "stroke_color": (255, 255, 255, 255)
        },
        "neon": {
            "bg_color": (0, 0, 0, 255),      # Black background
            "text_color": (0, 255, 255, 255), # Cyan
            "font_size": 60,
            "stroke_width": 2,
            "stroke_color": (255, 0, 255, 255) # Magenta
        },
        "fire": {
            "bg_color": (255, 255, 255, 0),
            "text_color": (255, 69, 0, 255),  # Red-orange
            "font_size": 60,
            "stroke_width": 2,
            "stroke_color": (255, 215, 0, 255) # Gold
        },
        "ice": {
            "bg_color": (255, 255, 255, 0),
            "text_color": (135, 206, 250, 255), # Light blue
            "font_size": 60,
            "stroke_width": 2,
            "stroke_color": (255, 255, 255, 255) # White
        }
    }
    
    style_config = styles.get(style, styles["default"])
    
    # Create image with transparency
    img = Image.new('RGBA', (width, height), style_config["bg_color"])
    draw = ImageDraw.Draw(img)
    
    # Wrap text for long strings
    wrapped_text = textwrap.fill(text, width=20)
    
    try:
        # Try to use a system font
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", style_config["font_size"])
    except:
        try:
            font = ImageFont.truetype("arial.ttf", style_config["font_size"])
        except:
            # Fallback to default font
            font = ImageFont.load_default()
    
    # Calculate text position (centered)
    bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw text with stroke if specified
    if style_config["stroke_width"] > 0:
        # Draw stroke
        for dx in range(-style_config["stroke_width"], style_config["stroke_width"] + 1):
            for dy in range(-style_config["stroke_width"], style_config["stroke_width"] + 1):
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), wrapped_text, font=font, fill=style_config["stroke_color"])
    
    # Draw main text
    draw.text((x, y), wrapped_text, font=font, fill=style_config["text_color"])
    
    return img

def setup_plugin(client, config):
    """Setup the sticker maker plugin"""
    
    @client.on_message(filters.command("sticker", config.COMMAND_PREFIX) & filters.me)
    async def sticker_command(client, message: Message):
        """Create a sticker from text"""
        try:
            args = message.text.split(maxsplit=2)
            
            if len(args) < 2:
                await message.edit("""
🎨 **STICKER MAKER**

**Usage:**
• `.sticker <text>` - Create basic sticker
• `.sticker <style> <text>` - Create styled sticker

**Available Styles:**
• `default` - Basic black text
• `bold` - Bold text with outline
• `neon` - Neon cyan on black
• `fire` - Orange-red with gold outline
• `ice` - Light blue with white outline

**Example:**
`.sticker bold Hello World!`
                """)
                return
            
            # Parse arguments
            if len(args) == 2:
                style = "default"
                text = args[1]
            else:
                style = args[1].lower()
                text = args[2]
            
            # Validate style
            valid_styles = ["default", "bold", "neon", "fire", "ice"]
            if style not in valid_styles:
                # If style is invalid, treat it as part of text
                text = " ".join(args[1:])
                style = "default"
            
            # Limit text length
            if len(text) > 100:
                await message.edit("❌ Text too long! Maximum 100 characters.")
                return
            
            await message.edit("🎨 Creating sticker...")
            
            # Create sticker
            sticker_img = create_text_sticker(text, style)
            
            # Save to bytes
            img_bytes = io.BytesIO()
            sticker_img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            # Send as sticker
            await message.delete()
            await client.send_sticker(
                chat_id=message.chat.id,
                sticker=img_bytes,
                reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None
            )
            
        except Exception as e:
            await message.edit(f"❌ Failed to create sticker: {str(e)}")
    
    @client.on_message(filters.command("stickerpack", config.COMMAND_PREFIX) & filters.me)
    async def stickerpack_command(client, message: Message):
        """Show sticker pack information"""
        try:
            pack_info = """
📦 **NEXUS STICKER PACK**

**Create Custom Stickers:**
Use `.sticker` command to create text-based stickers

**Features:**
• Multiple text styles
• Transparent backgrounds
• 512x512 standard size
• Auto text wrapping
• Color themes

**Tips:**
• Keep text short for best results
• Use styles for visual impact
• Experiment with different themes

**Created by Nexus Userbot v2.0**
            """
            await message.edit(pack_info)
            
        except Exception as e:
            await message.edit(f"❌ Error: {str(e)}")

# Plugin info for the plugin manager
PLUGIN_INFO = {
    "name": __plugin_name__,
    "description": __plugin_description__,
    "version": __plugin_version__,
    "commands": __plugin_commands__,
    "setup": setup_plugin
}