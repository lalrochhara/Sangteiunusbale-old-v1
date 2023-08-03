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


from Sangtei import USER_ID, SUDO_USERS, SangteiCli
from Sangtei.helper import custom_filter
from Sangtei.helper.anon_admin import anonadmin_checker
from Sangtei.helper.chat_status import CheckAllAdminsStuffs, isUserAdmin
from Sangtei.helper.get_user import get_user_id


@SangteiCli.on_message(custom_filter.command(commands=('promote')))
@anonadmin_checker
async def promote(client, message):

    if not await CheckAllAdminsStuffs(message, permissions='can_promote_members'):
        return
    
    user_info = await get_user_id(message)
    user_id = user_info.id 
    chat_id = message.chat.id 

    if user_id == USER_ID:
        await message.reply(
            "Damn, I wish I could promote myself."
        )
        return

    print(user_id)
    if await isUserAdmin(message, user_id=user_id, silent=True):
        await message.reply(
            "So you're tellimg me you wanna promote someone who's already an admin? How big brain of you!"
        )
        return

    await SangteiCli.promote_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        can_change_info=False
    )

    await message.reply(
        f"{user_info.mention} has been promoted!"
    )