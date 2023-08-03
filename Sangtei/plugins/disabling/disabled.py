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
from Sangtei.database.disable_mongo import get_disabled
from Sangtei.helper import custom_filter
from Sangtei.helper.chat_status import isUserAdmin


@SangteiCli.on_message(custom_filter.command(commands=('disabled')))
async def disable(client, message):

    chat_id = message.chat.id 

    if not await isUserAdmin(message):
        return
    
    DISABLE_LIST = get_disabled(chat_id)

    if (
        len(DISABLE_LIST) == 0
    ):
        await message.reply(
            "There are no disabled commands in this chat."
        )
        return
    
    text = "The following commands are disabled in this chat:\n"
    for item in DISABLE_LIST:
        text += f'- `{item}`\n'
    
    await message.reply(
        text
    )
