from database import DatabaseManager


class DataPrinter:
    @staticmethod
    async def print_aggregated_data(db: "DatabaseManager"):
        data = await db.get_aggregated_data()
        for row in data:
            print(f"Region: {row.region}")
            print(f"Total Population: {row.total_population:,}")
            print(f"Largest Country: {row.max_country}")
            print(f"Largest Country Population: {row.max_population:,}")
            print(f"Smallest Country: {row.min_country}")
            print(f"Smallest Country Population: {row.min_population:,}")
            print("-" * 50)