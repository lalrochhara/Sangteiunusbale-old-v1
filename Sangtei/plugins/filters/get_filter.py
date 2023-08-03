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


import re

from pyrogram import filters
from Sangtei import SangteiCli
from Sangtei.database.filters_mongo import get_filter, get_filters_list
from Sangtei.helper import custom_filter
from Sangtei.helper.filters_helper.send_filter_message import SendFilterMessage


@SangteiCli.on_message(filters.all & filters.group, group=8)
async def FilterCheckker(client, message):
    
    if not message.text:
        return
    text = message.text
    chat_id = message.chat.id

    # If 'chat_id' has no filters then simply return  
    if (
        len(get_filters_list(chat_id)) == 0
    ):
        return

    ALL_FILTERS = get_filters_list(chat_id)
    for filter_ in ALL_FILTERS:
        
        if (
            message.command
            and message.command[0] == 'filter'
            and len(message.command) >= 2
            and message.command[1] ==  filter_
        ):
            return
            
        pattern = r"( |^|[^\w])" + re.escape(filter_) + r"( |$|[^\w])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            filter_name, content, text, data_type = get_filter(chat_id, filter_)
            await SendFilterMessage(
                message=message,
                filter_name=filter_,
                content=content,
                text=text,
                data_type=data_type
            )
