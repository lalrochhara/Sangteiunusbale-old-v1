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

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Sangtei import USERNAME, SangteiCli
from Sangtei.database.rules_mongo import (get_private_note, get_rules,
                                         get_rules_button)
from Sangtei.helper import custom_filter
from Sangtei.helper.button_gen import button_markdown_parser
from Sangtei.helper.disable import disable
from Sangtei.helper.get_data import GetChat
from Sangtei.helper.note_helper.note_fillings import \
    NoteFillings as rules_filler


@SangteiCli.on_message(custom_filter.command(commands=('rules'), disable=True))
@disable
async def rules(client, message):

    chat_id = message.chat.id 
    chat_title = message.chat.title 
    rules_text = get_rules(chat_id)
    if rules_text is None:
        await message.reply(
            "This chat doesn't seem to have had any rules set yet... I wouldn't take that as an invitation though.",
            quote=True
        )
        return
    
    if not get_private_note(chat_id):
        rules_text, buttons = button_markdown_parser(rules_text)
        button_markdown = None
        if len(buttons) > 0:
            button_markdown = InlineKeyboardMarkup(buttons)

        rules_text = rules_filler(message, rules_text)

        await message.reply(
            (
                f"The rules for `{html.escape(chat_title)}` are:\n\n"
                f"{rules_text}"
            ),
            reply_markup=button_markdown,
            quote=True
        )
    else:
        button_text = get_rules_button(chat_id)
        button = [[InlineKeyboardButton(text=button_text, url=f'http://t.me/{BOT_USERNAME}?start=rules_{chat_id}')]]

        await message.reply(
            "Click on the button to see the chat rules!",
            reply_markup=InlineKeyboardMarkup(button),
            quote=True
        )

async def rulesRedirect(message):
    chat_id = int(message.command[1].split('_')[1])
    chat_title = await GetChat(chat_id)
    rules_text = get_rules(chat_id)
    
    rules_text, buttons = button_markdown_parser(rules_text)
    button_markdown = None
    if len(buttons) > 0:
        button_markdown = InlineKeyboardMarkup(buttons)

    rules_text = rules_filler(message, rules_text)
    await message.reply(
        (
            f"The rules for `{html.escape(chat_title)}` are:\n\n"
            f"{rules_text}"
        ),
        reply_markup=button_markdown,
        quote=True
    )
