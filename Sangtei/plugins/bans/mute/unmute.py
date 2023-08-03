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
from Sangtei.helper.chat_status import CheckAllAdminsStuffs
from Sangtei.helper.get_user import get_text, get_user_id

UNMUTE_PERMISSIONS = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_animations=True,
    can_send_games=True,
    can_use_inline_bots=True,
    can_add_web_page_previews=True,
    can_send_polls=True
)


@SangteiCli.on_message(custom_filter.command(commands=('unmute')))
@anonadmin_checker
async def ban(client, message):

    chat_id = message.chat.id 
    chat_title = message.chat.title

    if not await CheckAllAdminsStuffs(message, permissions='can_restrict_members'):
        return
    
    user_info = await get_user_id(message)
    user_id = user_info.id
    
    await SangteiCli.restrict_chat_member(
        chat_id,
        user_id,
        UNMUTE_PERMISSIONS
        )
    
    await message.reply(
        "Alright, they can speak again."
    )
