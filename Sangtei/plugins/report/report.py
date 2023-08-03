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

from pyrogram import filters
from Sangtei import SangteiCli
from Sangtei.database.report_mongo import get_report
from Sangtei.helper import custom_filter
from Sangtei.helper.chat_status import isUserAdmin


async def report_(client, message):
    chat_id = message.chat.id

    if not get_report(chat_id):
        return
    
    if await isUserAdmin(message, silent=True):
        await message.reply(
            "Tah hian admin i ni reng a, engvanga midang report duh deuh kher chu nge i nih le?"
        )
        return
    
    if not message.reply_to_message:
        await message.reply(
            "Tu ber chu nge i report duh ni a?"
        )
        return
    
    if await isUserAdmin(message.reply_to_message, silent=True):
        await message.reply(
            "Admin i report thei leuh."
        )
        return
    
    reported_user = message.reply_to_message.from_user

    admin_data = await SangteiCli.get_chat_members(
        chat_id=chat_id,
        filter='administrators'
        )
        
    ADMINS_TAG = str()
    TAG = u'\u200b'
    for admin in admin_data:
        if not admin.user.is_bot:
            ADMINS_TAG = ADMINS_TAG + f'[{TAG}](tg://user?id={admin.user.id})'

    await message.reply(
        f"Reported {reported_user.mention} to admins.{ADMINS_TAG}"
    )

@SangteiCli.on_message(custom_filter.command(commands=('report')))
async def report(client, message):
    await report_(client, message)

@SangteiCli.on_message(filters.regex(pattern=(r"(?i)@admin(s)?")))
async def regex_report(client, message):
    await report_(client, message)
