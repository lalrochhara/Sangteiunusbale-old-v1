#    Sangtei (Development)
#    Copyright (C) 2019 - 2023 Famhawite Infosys
#    Copyright (C) 2019 - 2023 Nicky Lalrochhara

#    This program is free software; you can redistribute it and/or modify 
#    it under the terms of the GNU General Public License as published by 
#    the Free Software Foundation; either version 3 of the License, or 
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


import html

from pyrogram.types import ChatPermissions
from Sangtei import USER_ID, SangteiCli
from Sangtei.helper import custom_filter
from Sangtei.helper.anon_admin import anonadmin_checker
from Sangtei.helper.chat_status import (can_restrict_member, isBotAdmin,
                                       isUserAdmin)
from Sangtei.helper.get_user import get_text, get_user_id

MUTE_PERMISSIONS = ChatPermissions(
    can_send_messages=False
)

@SangteiCli.on_message(custom_filter.command(commands=['mute', 'dmute', 'smute']))
@anonadmin_checker
async def mute(client, message):
    chat_id = message.chat.id 
    chat_title = message.chat.title
    message_id = None
    if not await isUserAdmin(message):
        return
    
    user_info = await get_user_id(message)
    user_id = user_info.id
    
    if user_id == USER_ID:
        await message.reply(
            "Yup! Let me just ban myself. Yay!"
        )
        return

    if not await isBotAdmin(message):
        return

    if not await can_restrict_member(message, user_id):
        await message.reply(
            "Surely I don't plan to ban an admin."
        )
        return
    
    await SangteiCli.restrict_chat_member(
        chat_id,
        user_id,
        MUTE_PERMISSIONS
        )
        
    
    if message.command[0].find('dmute') >= 0:
        if message.reply_to_message:
            message_id = message.reply_to_message.message_id

    elif message.command[0].find('smute') >= 0:
        message_id = message.message_id   
    
    
    if not message.command[0].find('smute') >= 0:
        text = f"{user_info.mention} is muted now in {html.escape(chat_title)}.\n"
        
        reason = get_text(message)
        if reason:
            text += f"Reason: {reason}"

        await message.reply(
            text
        )
    
    # Deletaion of message according to user admin command
    if message_id is not None:
        await SangteiCli.delete_messages(
                chat_id=chat_id,
                message_ids=message_id
            )
