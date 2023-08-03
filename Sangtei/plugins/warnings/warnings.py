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
from Sangtei.database.warnings_mongo import get_warn_mode, warn_limit
from Sangtei.helper import custom_filter
from Sangtei.helper.chat_status import isUserAdmin
from Sangtei.helper.disable import disable
from Sangtei.plugins.warnings.set_warn_mode import WarnModeMap


def warn_mode_map(warn_mode_in):
    warn_mode_raw = WarnModeMap(warn_mode_in)
    warn_mode_out = warn_mode_raw.name 
    return warn_mode_out

@SangteiCli.on_message(custom_filter.command(commands=('warnings'), disable=True))
@disable
async def warnings(client, message):

    chat_id = message.chat.id 
    chat_title = message.chat.title 
    if not await isUserAdmin(message):
        return
    
    warn_chat_limit = warn_limit(chat_id)
    text = (
        f"There is a {warn_chat_limit} warning limit in {html.escape(chat_title)}. "
    )
    warn_mode_in, warn_mode_time = get_warn_mode(chat_id) 
    warn_mode = warn_mode_map(warn_mode_in)
    if warn_mode == 'Ban': 
        text += (
            "When that limit has been exceeded, the user will be banned."
        ) 
    elif warn_mode == 'Kick':
        text += (
            "When that limit has been exceeded, the user will be kicked."
        )
    elif warn_mode == 'Mute':
        text += (
            "When that limit has been exceeded, the user will be muted."
        )
    elif warn_mode == 'Tmute':
        text += (
            "When that limit has been exceeded, the user will be temporarily muted."
        )
    elif warn_mode == 'Tban':
        text += (
            "When that limit has been exceeded, the user will be temporarily banned."
        )
    
    await message.reply(
        text,
        quote=True
    )

        
