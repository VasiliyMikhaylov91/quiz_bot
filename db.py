import asyncio
import aiosqlite


DB_NAME = 'quiz_bot.db'

async def get_quiz_points(user_id):
    # Подключаемся к базе данных
     async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT user_points FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0


async def create_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index, user_points) VALUES (?, ?, ?)', (user_id, 0, 0, ))
        # Сохраняем изменения
        await db.commit()


async def update_quiz_points(user_id, points):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('UPDATE quiz_state SET user_points = (?) WHERE user_id = (?)', (points, user_id, ))
        # Сохраняем изменения
        await db.commit()


async def get_quiz_index(user_id):
     # Подключаемся к базе данных
     async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0


async def update_quiz_index(user_id, index):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('UPDATE quiz_state SET question_index = (?) WHERE user_id = (?)', (index, user_id, ))
        # Сохраняем изменения
        await db.commit()


async def create_table():
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Создаем таблицу
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER, user_points INTEGER)''')
        # Сохраняем изменения
        await db.commit()

async def get_db():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT * FROM quiz_state') as cursor:
            data = await cursor.fetchall()
            data_text = 'ID Игрока -> Заработанные очки\n'
            for row in data:
                data_text += f'{row[0]} -> {row[2]}\n'
            return data_text


if __name__ == '__main__':
    asyncio.run(get_db())