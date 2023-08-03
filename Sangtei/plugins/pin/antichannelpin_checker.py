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

from pyrogram import filters
from pyrogram.types import Message
from Sangtei import SangteiCli
from Sangtei.database.pin_mongo import get_antichannelpin
from Sangtei.helper.chat_status import isBotCan


@SangteiCli.on_message(filters.all & filters.group, group=7)
async def cleanlinkedChecker(client, message):
    chat_id = message.chat.id
    message_id = message.message_id
    if not get_antichannelpin(chat_id):
        return

    channel_id = await GetLinkedChannel(chat_id)
    if channel_id is not None:
        if (
            message.forward_from_chat
            and message.forward_from_chat.type == 'channel'
            and message.forward_from_chat.id == channel_id
        ):
            if not await isBotCan(message , permissions='can_pin_messages', silent=True):
                await message.reply(
                    "I don't have the right to pin or unpin messages in this chat.\nError: `could_not_unpin`"
                )
                return
    
            await SangteiCli.unpin_chat_message(
                chat_id=chat_id,
                message_id=message_id
            )

async def GetLinkedChannel(chat_id: int) -> str:
    chat_data = await SangteiCli.get_chat(
        chat_id=chat_id
    )
    if chat_data.linked_chat:
        return chat_data.linked_chat.id
    else:
        return None
