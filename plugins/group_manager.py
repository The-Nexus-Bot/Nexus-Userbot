"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         NEXUS GROUP MANAGER PLUGIN                          ║
║                                                                              ║
║ Created by: @nexustech_dev                                                   ║
║ Copyright (c) 2025 NexusTech Development                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant

# Plugin metadata
__plugin_name__ = "Group Manager"
__plugin_description__ = "Leave groups and manage group participation"
__plugin_version__ = "1.0.0"
__plugin_commands__ = [".leave", ".leaveall", ".groups"]

def setup_plugin(client, config):
    """Setup the group manager plugin"""
    
    @client.on_message(filters.command("leave", config.COMMAND_PREFIX) & filters.me)
    async def leave_command(client, message: Message):
        """Leave current group or specified group"""
        try:
            args = message.text.split()
            
            # Check if we're in a group
            if message.chat.type == "private":
                await message.edit("❌ This command can only be used in groups or provide a group ID")
                return
            
            if len(args) == 1:
                # Leave current group
                chat_title = message.chat.title or "Unknown Group"
                chat_id = message.chat.id
                
                await message.edit(f"👋 Leaving group: **{chat_title}**\n\nGoodbye!")
                await asyncio.sleep(2)
                
                try:
                    await client.leave_chat(chat_id)
                except Exception as e:
                    # If we can't edit (already left), that's fine
                    pass
                    
            else:
                # Leave specific group by ID
                try:
                    target_chat_id = int(args[1])
                except ValueError:
                    await message.edit("❌ Invalid chat ID. Use: `.leave <chat_id>`")
                    return
                
                try:
                    chat_info = await client.get_chat(target_chat_id)
                    chat_title = chat_info.title or "Unknown Group"
                    
                    await client.leave_chat(target_chat_id)
                    await message.edit(f"✅ Successfully left group: **{chat_title}**")
                    
                except Exception as e:
                    await message.edit(f"❌ Failed to leave group: {str(e)}")
                    
        except Exception as e:
            await message.edit(f"❌ Error: {str(e)}")
    
    @client.on_message(filters.command("leaveall", config.COMMAND_PREFIX) & filters.me)
    async def leaveall_command(client, message: Message):
        """Leave all groups (with confirmation)"""
        try:
            args = message.text.split()
            
            if len(args) < 2 or args[1].lower() != "confirm":
                await message.edit("""
⚠️ **LEAVE ALL GROUPS**

This will leave ALL groups you're currently in!

**To confirm, use:**
`.leaveall confirm`

**Warning:** This action cannot be undone!
                """)
                return
            
            await message.edit("🔍 Scanning groups...")
            
            left_count = 0
            failed_count = 0
            group_list = []
            
            # Get all chats
            async for dialog in client.get_dialogs():
                chat = dialog.chat
                
                # Check if it's a group or supergroup
                if chat.type in ["group", "supergroup"]:
                    group_list.append((chat.id, chat.title or "Unknown Group"))
            
            if not group_list:
                await message.edit("ℹ️ No groups found to leave.")
                return
            
            await message.edit(f"📤 Leaving {len(group_list)} groups...")
            
            for chat_id, chat_title in group_list:
                try:
                    await client.leave_chat(chat_id)
                    left_count += 1
                    await asyncio.sleep(1)  # Rate limiting
                except Exception as e:
                    failed_count += 1
                    print(f"Failed to leave {chat_title}: {e}")
            
            result_text = f"""
✅ **GROUP CLEANUP COMPLETE**

📤 **Left:** {left_count} groups
❌ **Failed:** {failed_count} groups
📊 **Total processed:** {len(group_list)} groups

**Status:** All accessible groups have been left.
            """
            
            await message.edit(result_text)
            
        except Exception as e:
            await message.edit(f"❌ Error during mass leave: {str(e)}")
    
    @client.on_message(filters.command("groups", config.COMMAND_PREFIX) & filters.me)
    async def groups_command(client, message: Message):
        """List all groups you're in"""
        try:
            await message.edit("🔍 Scanning groups...")
            
            groups = []
            supergroups = []
            channels = []
            
            # Get all chats
            async for dialog in client.get_dialogs():
                chat = dialog.chat
                chat_info = f"**{chat.title or 'Unknown'}** (`{chat.id}`)"
                
                if chat.type == "group":
                    groups.append(chat_info)
                elif chat.type == "supergroup":
                    supergroups.append(chat_info)
                elif chat.type == "channel":
                    channels.append(chat_info)
            
            result_text = "📋 **YOUR GROUPS & CHANNELS**\n\n"
            
            if groups:
                result_text += f"👥 **Groups ({len(groups)}):**\n"
                for group in groups[:10]:  # Limit to 10 to avoid message length issues
                    result_text += f"• {group}\n"
                if len(groups) > 10:
                    result_text += f"• ... and {len(groups) - 10} more\n"
                result_text += "\n"
            
            if supergroups:
                result_text += f"🏢 **Supergroups ({len(supergroups)}):**\n"
                for supergroup in supergroups[:10]:
                    result_text += f"• {supergroup}\n"
                if len(supergroups) > 10:
                    result_text += f"• ... and {len(supergroups) - 10} more\n"
                result_text += "\n"
            
            if channels:
                result_text += f"📢 **Channels ({len(channels)}):**\n"
                for channel in channels[:5]:
                    result_text += f"• {channel}\n"
                if len(channels) > 5:
                    result_text += f"• ... and {len(channels) - 5} more\n"
                result_text += "\n"
            
            total = len(groups) + len(supergroups) + len(channels)
            result_text += f"📊 **Total:** {total} chats\n\n"
            result_text += "**Commands:**\n"
            result_text += "• `.leave` - Leave current group\n"
            result_text += "• `.leave <chat_id>` - Leave specific group\n"
            result_text += "• `.leaveall confirm` - Leave all groups"
            
            if not groups and not supergroups and not channels:
                result_text = "ℹ️ **No groups or channels found.**\n\nYou're not currently in any groups or subscribed to any channels."
            
            await message.edit(result_text)
            
        except Exception as e:
            await message.edit(f"❌ Error listing groups: {str(e)}")

# Plugin info for the plugin manager
PLUGIN_INFO = {
    "name": __plugin_name__,
    "description": __plugin_description__,
    "version": __plugin_version__,
    "commands": __plugin_commands__,
    "setup": setup_plugin
}