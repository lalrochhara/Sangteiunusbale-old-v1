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

from pykeyboard import InlineKeyboard
from Sangtei import SangteiCli
from Sangtei.helper import custom_filter
from Sangtei.plugins.urban_dictionary.get_data import getData


@SangteiCli.on_message(custom_filter.command(commands=('ud')))
async def urbanDictionary(client, message):
    message_id = message.message_id 
    chat_id = message.chat.id 
    GetWord = ' '.join(message.command[1:])
    if not GetWord:
        message = await SangteiCli.ask(
            message.chat.id,
            'Now give any word for query!'
        )
        GetWord = message.text
    
    CurrentPage = 1
    UDReasult, PageLen = await getData(chat_id, message_id, GetWord, CurrentPage)
    
    keyboard = InlineKeyboard()
    keyboard.paginate(PageLen, CurrentPage, 'pagination_keyboard#{number}' + f'#{GetWord}')
    await message.reply(
        text=f"{UDReasult}",
        reply_markup=keyboard
    )   
