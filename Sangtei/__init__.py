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

import sys
import dns.resolver

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pymongo import MongoClient
from pyrogram import Client
from pyromod import listen

from config import config
from Sangtei.SangteiGban import SangteiClient

#from Sangteigban import SangteiClient

OWNER_ID = config.settings.owner
USER_ID = config.telegram.bot.id
NAME = config.telegram.bot.name
USER_USERNAME = config.telegram.bot.username
LOG_CHANNEL = config.settings.log.chat_id
SUDO_USERS = config.settings.sudo_users
PREFIX = config.settings.commands.prefix
BACKUP_CHAT = config.settings.backup.chat_id

SangteiCli = Client(
    session_name='SangteiSession',
    api_id=config.telegram.api_id,
    api_hash=config.telegram.api_hash,
    bot_token=config.telegram.bot.token
)

# MongoDatabase dns configurations
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8'] 

SangteiAPI = SangteiClient(api_key=config.api.Sangtei.api_key)

# Async scheduler
scheduler = AsyncIOScheduler()

try:
  SangteiMongoClient = MongoClient(config.database.database_url)
  SangteiDB = SangteiMongoClient.Sangtei_mongo
except:
  sys.exit(f"{BOT_NAME}'s database hi a nung lo!")

TELEGRAM_SERVICES_IDs = (
    [
        777000, # Telegram Service Notifications(No need to change this, leave it as it is)
        6400219046 # SangteiBot Identification/ID
    ]
)

NICKY_Sangtei_BOT = 6400219046
