import asyncio
import os
from dotenv import load_dotenv
from database import DatabaseManager
from fetcher import DataFetcher
from printer import DataPrinter


async def get_data():
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    data_source = os.getenv("DATA_SOURCE", "wikipedia")

    db = DatabaseManager(database_url)
    await db.init_db()

    fetcher = DataFetcher(data_source)
    countries = await fetcher.fetch_data()
    await db.save_countries(countries)
    print(f"Saved {len(countries)} countries to database")


async def print_data():
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    db = DatabaseManager(database_url)
    await DataPrinter.print_aggregated_data(db)


if __name__ == "__main__":
    import sys

    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "get_data":
        asyncio.run(get_data())
    elif command == "print_data":
        asyncio.run(print_data())
    else:
        print("Usage: python main.py {get_data,print_data}")