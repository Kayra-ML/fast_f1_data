import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


class LapCollector:
    def __init__(self, database_url: str = None):
        if database_url:
            self.engine = create_engine(database_url, future=True)
        else:
            load_dotenv()
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                raise RuntimeError("DATABASE_URL environment variable is required")
            self.engine = create_engine(database_url, future=True)

    def collect_lap_summary(self) -> None:
        query = """
        SELECT session_key,
               driver_number,
               COUNT(*) AS lap_count,
               AVG(lap_duration) AS avg_lap_time,
               MIN(lap_duration) AS best_lap_time,
               MAX(lap_duration) AS worst_lap_time
        FROM laps
        GROUP BY session_key, driver_number
        ORDER BY avg_lap_time ASC
        LIMIT 50
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = [dict(row._mapping) for row in result]

        print("=== Lap Summary ===")
        for row in rows:
            print(row)
