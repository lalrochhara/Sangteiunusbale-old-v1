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

from pyrogram.errors import BadRequest
from pyrogram.types import ChatPermissions
from Sangtei import SangteiCli
from Sangtei.database.locks_mongo import lock_db
from Sangtei.helper import custom_filter
from Sangtei.helper.chat_status import check_bot, check_user

from . import lock_map


@SangteiCli.on_message(custom_filter.command(commands=('lock')))
async def lock(client, message):
    
    chat_id = message.chat.id

    if not await check_bot(message, permissions=['can_delete_messages', 'can_restrict_members']):
        return

    if not await check_user(message, permissions='can_change_info'):
        return
    
    if not (
        len(message.command) >= 2
    ):
        await message.reply(
            "You haven't specified a type to lock."
        )
        return

    LOCKS_LIST = lock_map.LocksMap.list()

    lock_args = message.command[1:]
    
    LOCK_ITMES = []
    INCORRECT_ITEMS = []

    for lock in lock_args:
        if lock not in LOCKS_LIST:
            INCORRECT_ITEMS.append(lock)
        else:
            LOCK_ITMES.append(lock)
    
    if (
        len(INCORRECT_ITEMS) != 0
    ):
        text = (
            "Unknown lock types:\n"
        )
        for item in INCORRECT_ITEMS:
            text += f'- {item}\n'
        text += "Check /locktypes!"
        await message.reply(
                text
            )
        return
    
    for item in LOCK_ITMES:
        lock_value = lock_map.LocksMap[item].value
        lock_db(chat_id, lock_value)

    text = 'Locked:\n'
    for lock_arg in LOCK_ITMES:
        if len(LOCK_ITMES) != 1:
            text += f'- `{lock_arg}`\n'
        else:
            text = (
                f"Locked `{lock_arg}`."
            )

    if 'all' in LOCK_ITMES:
        try:
            await SangteiCli.set_chat_permissions(
                chat_id,
                ChatPermissions()
            )
        except BadRequest:
            await message.reply(
                (
                    "Non-admins already can't send messages. What are you even trying to do m8?"
                )
            )
            return

    await message.reply(
        text
    )
