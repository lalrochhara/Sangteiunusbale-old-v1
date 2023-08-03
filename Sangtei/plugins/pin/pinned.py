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

from Sangtei import SangteiCli
from Sangtei.helper import custom_filter


@SangteiCli.on_message(custom_filter.command(commands=('pinned')))
async def pinned(client, message):

    chat_id = message.chat.id
    chat_title = message.chat.title

    chat_data = await SangteiCli.get_chat(
        chat_id=chat_id
    )
    if chat_data.pinned_message:
        pinned_message_id = chat_data.pinned_message.message_id
        message_link = f"http://t.me/c/{str(chat_id).replace(str(-100), '')}/{pinned_message_id}"
        await message.reply(
            (
                f"The pinned message in {html.escape(chat_title)} is [here]({message_link})."
            )
        )
    else:
        await message.reply(
            (
                f"There is no pinned message in {html.escape(chat_title)}."
            )
        )
