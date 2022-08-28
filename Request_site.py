import logging
import time
from aiogram import Bot, Dispatcher, executor, types
from random import choice

from bs4 import BeautifulSoup
import requests

import aiogram.utils.markdown as fmt

logging.basicConfig(level=logging.INFO)

#url = 'https://epscape.com/series/the-blacklist'
url ='https://www.championat.com/news/football/1.html'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}

TOKEN = '5020690773:AAHwlPw5xLf6vBZo3Dzr-nnG0BLLnT1hBW0'
stickers=['CAACAgEAAxkBAAEDqe5h3VsrbV8cQRN9xdUbJ9kJAAEkZJcAAgYAA1qqCUyCbvObrMeIKiME',
'CAACAgIAAxkBAAEDqgNh3WzLB4srFKrS9z4F5HyFRj3mvwAC2RsAAoluUEkD_GtD9fgcSyME',
'CAACAgIAAxkBAAEDq_5h3sgSet8AAXDNEdVnnQVw_cxR4scAAlIEAAKc1ucKPuR11-h0UrYjBA',
'CAACAgIAAxkBAAEDsDBh4nF5G-4IJ03SLjIHYTNtX4D2JQACNQEAAjDUnRG0uDX9ZqC2fCME',
'CAACAgIAAxkBAAEDsDJh4nGWg_decp8O3kWerXf6AAGj6Y0AAkEAA6_GURqSbAx00CciPiME']


def getPage():
    allNews = []
    filteredNews = []
# start new session to persist data between requests
    session = requests.Session()

    page = session.get(url, headers = header)
    print('Вернулось - {}'.format(page.status_code))
#print(page.text)
    soup = BeautifulSoup(page.text, "html.parser")

    allNews = soup.findAll('a',  class_='news-item__title _important')
    for x in allNews:
        s1=str(x.contents).replace('\'','')
        filteredNews.append(s1+'nnn')
    return filteredNews

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    await message.answer("Hi! <b>{}</b>\nI'm EchoBot!\n".format(message.chat.first_name),parse_mode='html')
    await bot.send_sticker(message.chat.id, choice(stickers))


@dp.message_handler(commands="news")
async def gettext(message: types.Message):
    s1=str(getPage()).replace('[','').replace(']','').replace('\'','').replace(',','').replace('nnn','\n \n')
    await message.answer(s1)

@dp.message_handler(commands="help")
async def gettext(message: types.Message):
    await message.answer(
        f"{fmt.hide_link('http://viruseproject.tv/releases/serials/dekster-novaya-krov-dexter-new-blood-sezon-1')}",
               parse_mode=types.ParseMode.HTML)



@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
