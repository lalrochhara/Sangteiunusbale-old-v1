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

from Sangtei import SangteiCli
from Sangtei.helper import custom_filter
from Sangtei.helper.chat_status import CheckAllAdminsStuffs


@SangteiCli.on_message(custom_filter.command(commands=('del')))
async def delete(client, message):
    chat_id = message.chat.id
    message_id = message.message_id

    if not await CheckAllAdminsStuffs(message, permissions='can_delete_messages'):
        return

    if not message.reply_to_message:
        await message.reply(
            'I message paih duh eng pawh kha reply rawh.'
        )
        return
        
    try:
        reply_to_message = message.reply_to_message.message_id
        await SangteiCli.delete_messages(
            chat_id=chat_id,
            message_ids=(
                [message_id, reply_to_message]
            )
        )
    except:
        await message.reply(
            "He tah hian Message ka paih thei lo! Admin ka ni em en chiang la, Midangte Message ka paih thei em tih te."
        )
