import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


class RacesCollector:
    def __init__(self, database_url: str = None):
        if database_url:
            self.engine = create_engine(database_url, future=True)
        else:
            load_dotenv()
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                raise RuntimeError("DATABASE_URL environment variable is required")
            self.engine = create_engine(database_url, future=True)

    def collect_races_2024(self) -> None:
        query = """
        SELECT season,
               round,
               race_name,
               circuit_id,
               date,
               time,
               url
        FROM races_2024
        ORDER BY round ASC
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = [dict(row._mapping) for row in result]

        print("=== 2024 Races ===")
        for row in rows:
            print(row)

    def collect_races_2025(self) -> None:
        query = """
        SELECT season,
               round,
               race_name,
               circuit_id,
               date,
               time,
               url
        FROM races_2025
        ORDER BY round ASC
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = [dict(row._mapping) for row in result]

        print("=== 2025 Races ===")
        for row in rows:
            print(row)

    def collect_all_races(self) -> None:
        query = """
        SELECT season,
               round,
               race_name,
               circuit_id,
               date,
               time,
               url
        FROM races_2024
        UNION ALL
        SELECT season,
               round,
               race_name,
               circuit_id,
               date,
               time,
               url
        FROM races_2025
        ORDER BY season DESC, round ASC
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = [dict(row._mapping) for row in result]

        print("=== All Races ===")
        for row in rows:
            print(row)
