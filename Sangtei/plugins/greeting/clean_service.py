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
from Sangtei.database.welcome_mongo import (
    SetCleanService,
    GetCleanService
)
from Sangtei.plugins.connection.connection import connection
from Sangtei.helper.anon_admin import anonadmin_checker

CLEAN_SERVICE_TRUE = ['on', 'aw']
CLEAN_SERVICE_FALSE = ['off', 'aih']

@SangteiCli.on_message(custom_filter.command(commands=('cleanservice')))
@anonadmin_checker
async def CleanService(client, message):
    
    if await connection(message) is not None:
        chat_id = await connection(message)
    else:
        chat_id = message.chat.id

    if not (
        await  CheckAllAdminsStuffs(message, permissions='can_delete_messages')
    ):
        return 

    if (
        len(message.command) >= 2
    ):
        get_clean_service = message.command[1]

        if (
            get_clean_service in CLEAN_SERVICE_TRUE
        ):
            clean_service = True
            SetCleanService(chat_id, clean_service)
            await message.reply(
                "I'll be deleting all service messages from now on!",
                quote=True
            )

        elif (
            get_clean_service in CLEAN_SERVICE_FALSE
        ):
            clean_service = False 
            SetCleanService(chat_id, clean_service)
            await message.reply(
                "I'll leave service messages.",
                quote=True
            )
        
        else:
            await message.reply(
                "Your input was not recognised as one of: yes/no/on/off",
                quote=True
            )
    elif (
        len(message.command) == 1
    ):
        if GetCleanService(chat_id):
            CleanServiceis = "I am currently deleting service messages when new members join or leave."

        else:
            CleanServiceis = "I am not currently deleting service messages when members join or leave."
        
        await message.reply(
            (
                f'{CleanServiceis}\n\n'
                "To change this setting, try this command again followed by one of yes/no/on/off"
            ),
            quote=True
        )