from session_auth.core.configs import settings
from session_auth.core.database import engine


async def create_tables() -> None:
    import session_auth.models._all_models
    print("creating table in DB")

    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
    print("table created with success")

if __name__ == "__main__":
    import asyncio

    asyncio.run(create_tables())