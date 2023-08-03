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

import datetime
import json

from Sangtei import (BACKUP_CHAT, OWNER_ID, SUDO_USERS, SangteiCli, SangteiDB,
                    scheduler)
from Sangtei.helper import custom_filter

COLLECTIONS_NAMES = SangteiDB.list_collection_names()

@SangteiCli.on_message(custom_filter.command(commands=('dbexport')))
async def SangteiExport(client, message):
    user_id = message.from_user.id

    if not user_id in OWNER_ID:
        return

    if (
        user_id in SUDO_USERS
    ):
        await message.reply(
            "Mate he command hi maw min siamtu te tan chauh a siam ania!"
        )
        return
    
    collect_collections()
    await SangteiCli.send_document(
        chat_id=BACKUP_CHAT,
        document='Sangtei_Backup.json',
        caption='Lakchhuah ani!'
    )

async def export_scheduler():
    collect_collections()
    await SangteiCli.send_document(
        chat_id=BACKUP_CHAT,
        document='Sangtei_Backup.json',
        caption='Lakchhuah ani!'
    )

# Async scheduler for auto export at 3 A.M
scheduler.add_job(export_scheduler, "cron", day_of_week ='mon-sun', hour=3, minute=00)

def exports_in_json(COLLECTIONS_LIST):
    with open('Sangtei_Backup.json', 'w') as backup_file:
        json.dump(COLLECTIONS_LIST, backup_file, indent=4, sort_keys=True, cls=DateTimeEncoder)

def collect_collections():
    COLLECTIONS_LIST  = {
        'collections': [],
        'exports_data': []
    }

    for collection in COLLECTIONS_NAMES:
        COLLECTIONS_LIST['collections'].append(collection)
        all_collec = list(SangteiDB[collection].find({}))
        #print(all_collec)
        COLLECTIONS_LIST['exports_data'].append(
            {
                collection: all_collec
            }
        )
    exports_in_json(COLLECTIONS_LIST)
  
class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return (str(z))
        else:
            return super().default(z)
