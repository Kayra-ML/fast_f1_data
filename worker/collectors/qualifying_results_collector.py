import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


class QualifyingResultsCollector:
    def __init__(self, database_url: str = None):
        if database_url:
            self.engine = create_engine(database_url, future=True)
        else:
            load_dotenv()
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                raise RuntimeError("DATABASE_URL environment variable is required")
            self.engine = create_engine(database_url, future=True)

    def collect_qualifying_summary(self) -> None:
        query = """
        SELECT season,
               round,
               driver_id,
               position,
               q1,
               q2,
               q3,
               constructor_id
        FROM qualifying_results_2024
        ORDER BY season DESC, round DESC, position ASC
        UNION ALL
        SELECT season,
               round,
               driver_id,
               position,
               q1,
               q2,
               q3,
               constructor_id
        FROM qualifying_results_2025
        ORDER BY season DESC, round DESC, position ASC
        LIMIT 100
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = [dict(row._mapping) for row in result]

        print("=== Qualifying Results Summary ===")
        for row in rows:
            print(row)
