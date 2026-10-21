import asyncio
import sqlite3

from aiogram import Bot, Dispatcher, F
from cfg import token
import logging
from handler import router
import aioschedule as schedule

async def refresh_stamina():
    db = sqlite3.connect('base.db')
    sql = db.cursor()
    sql.execute('SELECT user_id FROM users')
    all_users = sql.fetchall()
    for user in all_users:
        sql.execute('SELECT level FROM users WHERE user_id = ?', (user[0],))
        user_lvl = sql.fetchone()[0]
        new_stam = 50 + 10 * (user_lvl - 1)
        sql.execute('UPDATE users SET stamina = ? WHERE user_id = ?', (new_stam, user[0]))
        db.commit()

bot = Bot(token = token)
dp = Dispatcher()


async def main():
    schedule.every().day.at("00:00").do(refresh_stamina)
    dp.include_router(router)
    await dp.start_polling(bot)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)


if __name__ == '__main__':
    #logging.basicConfig(level=logging.INFO)
    asyncio.run(main())