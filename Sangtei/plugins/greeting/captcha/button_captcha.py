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
from pyrogram.types import (CallbackQuery, ChatPermissions,
                            InlineKeyboardButton, InlineKeyboardMarkup)
from Sangtei import USERNAME, SangteiCli
from Sangtei.database.rules_mongo import get_rules
from Sangtei.database.welcome_mongo import (GetCaptchaSettings,
                                           GetUserCaptchaMessageIDs,
                                           GetWelcome, isReCaptcha,
                                           isRuleCaptcha, isUserVerified,
                                           isWelcome)
from Sangtei.helper.button_gen import button_markdown_parser
from Sangtei.helper.chat_status import isUserAdmin

from .captcharules_button import ruleCaptchaButton


async def CaptchaButton(chat_id, user_id):

    captcha_mode, captcha_text, captcha_kick_time = GetCaptchaSettings(chat_id)
    captchaButton = list()
    
    if (
        isRuleCaptcha(chat_id)
        and get_rules(chat_id) is not None
    ):
        captchaButton = (
            [
                [
                    InlineKeyboardButton(text=captcha_text, url=f'http://t.me/{BOT_USERNAME}?start=captcha_button_{user_id}_{chat_id}')
                ]
            ]
        )
    else:
        if isUserVerified(chat_id, user_id):
            captchaButton = None
        else:
            captchaButton = (
                [
                    [
                        InlineKeyboardButton(text=captcha_text, callback_data=f'captcha_{user_id}')
                    ]
                ]
            )
        
    return captchaButton

    
@SangteiCli.on_callback_query(filters.create(lambda _, __, query: 'captcha_' in query.data))
async def CaptchaCallback(client: SangteiCli, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id 
    new_user_id = int(callback_query.data.split('_')[1])

    if new_user_id == user_id:

        if isWelcome(chat_id):
            Content, Text, DataType = GetWelcome(chat_id)
            Text, buttons = button_markdown_parser(Text)

            reply_markup = None
            if len(buttons) > 0:
                reply_markup = InlineKeyboardMarkup(buttons)
        else:
            reply_markup = None
        await callback_query.edit_message_reply_markup(
            reply_markup=reply_markup
        )
        await callback_query.answer(
            text="Hun min pek avangin ka lawm e!"
        )
        await SangteiCli.restrict_chat_member(
                chat_id,
                new_user_id,
                ChatPermissions(
                    can_send_messages=True
                )
            )
    else:
        await callback_query.answer(
            text="He button hi i tan anilo!"
        )


async def buttonCaptchaRedirect(message):
    user_id = message.from_user.id 
    chat_id = message.chat.id
    if message.command[1].split('_')[1] == 'button':
        new_user_id = int(message.command[1].split('_')[2])
        new_chat_id = int(message.command[1].split('_')[3])
    
        if new_user_id == user_id:

            # Already Verified users
            if not isReCaptcha(chat_id=new_chat_id):
                if isUserVerified(new_chat_id, new_user_id):
                    await message.reply(
                        "You already passed the CAPTCHA, You don't need to verify yourself again.",
                        quote=True
                    )
                    return

            # Admins captcha message
            if await isUserAdmin(message, pm_mode=True, chat_id=new_chat_id, user_id=new_user_id, silent=True):
                await message.reply(
                    "You are admin, You don't have to complete CAPTCHA.",
                    quote=True  
                )
                return  

            message_id, correct_captcha, chances, captcha_list = GetUserCaptchaMessageIDs(chat_id=new_chat_id, user_id=user_id)
            await ruleCaptchaButton(message=message, chat_id=new_chat_id, message_id=message_id)
