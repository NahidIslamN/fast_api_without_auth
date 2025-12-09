import asyncio
from database import engine, Base
import models  # make sure this imports your User model

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_models())
print("Tables created successfully!")

