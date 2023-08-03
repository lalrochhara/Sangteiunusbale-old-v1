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
from Sangtei.helper.chat_status import isUserAdmin
from Sangtei.helper.custom_filter import DISABLE_COMMANDS


@SangteiCli.on_message(custom_filter.command(commands=('disableable')))
async def disable_list(client, message):

    if not await isUserAdmin(message):
        return
        
    text_header = 'The following commands can be disabled:\n'
    for diable in DISABLE_COMMANDS:
        text_header += f"- `{diable}`\n"
    
    await message.reply(
        text_header,
        quote=True
    )
