import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


class PitStopCollector:
    def __init__(self, database_url: str = None):
        if database_url:
            self.engine = create_engine(database_url, future=True)
        else:
            load_dotenv()
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                raise RuntimeError("DATABASE_URL environment variable is required")
            self.engine = create_engine(database_url, future=True)

    def collect_pit_stop_stats(self) -> None:
        query = """
        SELECT season,
               round,
               driver_id,
               COUNT(*) AS pit_stops,
               AVG(milliseconds) AS avg_stop_ms,
               MIN(milliseconds) AS fastest_stop_ms,
               MAX(milliseconds) AS slowest_stop_ms
        FROM pit_stops
        GROUP BY season, round, driver_id
        ORDER BY avg_stop_ms ASC
        LIMIT 50
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = [dict(row._mapping) for row in result]

        print("=== Pit Stop Statistics ===")
        for row in rows:
            print(row)
