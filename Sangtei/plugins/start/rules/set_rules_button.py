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
from Sangtei.database.rules_mongo import get_rules_button, set_rule_button
from Sangtei.helper import custom_filter
from Sangtei.helper.anon_admin import anonadmin_checker
from Sangtei.helper.chat_status import isUserCan


@SangteiCli.on_message(custom_filter.command(commands=('setrulesbutton')))
@anonadmin_checker
async def set_rules(client, message):
    
    chat_id = message.chat.id 
    chat_title = message.chat.title

    if not await isUserCan(message, permissions='can_change_info'):
        return
    
    if not (
        len(message.command) >= 2
    ):
        current_rules_button = get_rules_button(chat_id)
        await message.reply(
            (
                f"The rules button will be called:\n `{current_rules_button}`\n\n"
                "To change the button name, try this command again followed by the new name"
            ),
            quote=True
        )
        return
    
    rules_button = ' '.join(message.text.markdown[1:])

    set_rule_button(chat_id, rules_button)
    await message.reply(
        "Updated the rules button name!",
        quote=True
    )
