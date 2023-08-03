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
from Sangtei.database.blocklists_mongo import setblocklistreason_db
from Sangtei.helper import custom_filter
from Sangtei.helper.chat_status import isUserCan


@SangteiCli.on_message(custom_filter.command(commands=('resetblocklistreason')))
async def resetblocklistreason(client, message):
    
    chat_id = message.chat.id 

    if not await isUserCan(message, permissions='can_change_info'):
        return
    
    setblocklistreason_db(chat_id, None)
    await message.reply(
        "The default blocklist reason has been reset."
    )
