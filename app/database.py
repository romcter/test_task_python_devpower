from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import os
from models import Base, Country


class DatabaseManager:
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url, echo=False)
        self.Session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def save_countries(self, countries: list[dict]):
        async with self.Session() as session:
            async with session.begin():
                await session.execute(text("DELETE FROM countries"))
                for country in countries:
                    session.add(Country(**country))
                await session.commit()

    async def get_aggregated_data(self):
        query = """
        SELECT 
            region,
            SUM(population) as total_population,
            MAX(CASE WHEN rn_max = 1 THEN name END) as max_country,
            MAX(CASE WHEN rn_max = 1 THEN population END) as max_population,
            MAX(CASE WHEN rn_min = 1 THEN name END) as min_country,
            MAX(CASE WHEN rn_min = 1 THEN population END) as min_population
        FROM (
            SELECT 
                name,
                population,
                region,
                ROW_NUMBER() OVER (PARTITION BY region ORDER BY population DESC) as rn_max,
                ROW_NUMBER() OVER (PARTITION BY region ORDER BY population ASC) as rn_min
            FROM countries
        ) t
        GROUP BY region
        ORDER BY region
        """
        async with self.Session() as session:
            result = await session.execute(text(query))
            return result.fetchall()