import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


class CircuitsCollector:
    def __init__(self, database_url: str = None):
        if database_url:
            self.engine = create_engine(database_url, future=True)
        else:
            load_dotenv()
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                raise RuntimeError("DATABASE_URL environment variable is required")
            self.engine = create_engine(database_url, future=True)

    def collect_circuits_list(self) -> None:
        query = """
        SELECT circuit_id,
               circuit_name,
               location,
               country,
               lat,
               lng
        FROM circuits
        ORDER BY country, circuit_name
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = [dict(row._mapping) for row in result]

        print("=== Circuits List ===")
        for row in rows:
            print(row)
