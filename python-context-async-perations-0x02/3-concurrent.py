"""
2. Concurrent Asynchronous Database Queries

Objective: Run multiple database queries concurrently using asyncio.gather.

Instructions:

Use the aiosqlite library to interact with SQLite asynchronously.

Write two asynchronous functions: async_fetch_users() and async_fetch_older_users() that fetches all users and users older than 40 respectively.

Use the asyncio.gather() to execute both queries concurrently.

Use asyncio.run(fetch_concurrently()) to run the concurrent fetch


"""

import asyncio
import aiosqlite

db_name = "my_db.db"


async def async_fetch_users():
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            await cursor.close()
            await db.close()
            for user in users:
                print(user)
            return user


async def async_fetch_older_users():
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * users WHERE age > 40") as cursor:
            older_users = cursor.fetchall()
            await cursor.close()
            await db.close()
            for user in older_users:
                print(user)
            return older_users


async def fetch_concurrently():
    await asyncio.gather(async_fetch_users(), async_fetch_older_users())


asyncio.run(fetch_concurrently())
