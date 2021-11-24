from aiogram import Bot, Dispatcher
import config

# prerequisites
if not config.TOKEN:
    exit("No token provided")

# init
bot = Bot(token=config.TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
