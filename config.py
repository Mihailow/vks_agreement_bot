from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from apscheduler.schedulers.asyncio import AsyncIOScheduler

DB_HOST = "localhost"
DB_NAME = "vks_main"
DB_USER = "postgres"
DB_PASS = "postgres"

telegram_token = "6353026522:AAGREBRShS_G8yYK93my6fOSDQgLDhUPyqc"
is_testing = True
from_email = "mihailbramnik@yandex.ru"
password = "ufongxhxzjwmkryk"
dest_email = "mike-bramnik@yandex.ru"

# telegram_token = "6363900608:AAFDltNwtWq4KQKxG5uzf1ZoeRuBavmgrkM"
# is_testing = False
# from_email = "vksproektbuh@yandex.ru"
# password = "jhayzhxitespnowp"
# dest_email = "buh@vksproekt.com"

subject = "Платёж по счёту"

bot = Bot(token=telegram_token)
dp = Dispatcher(bot, storage=MemoryStorage())
scheduler = AsyncIOScheduler()

last_message = {}
