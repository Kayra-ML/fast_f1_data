import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


class RaceControlCollector:
    def __init__(self, database_url: str = None):
        if database_url:
            self.engine = create_engine(database_url, future=True)
        else:
            load_dotenv()
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                raise RuntimeError("DATABASE_URL environment variable is required")
            self.engine = create_engine(database_url, future=True)

    def collect_status_overview(self) -> None:
        query = """
        SELECT rr.status,
               COUNT(*) AS count,
               AVG(rr.position) AS avg_position
        FROM race_results rr
        GROUP BY rr.status
        ORDER BY count DESC
        LIMIT 25
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = [dict(row._mapping) for row in result]

        print("=== Race Control Status Overview ===")
        for row in rows:
            print(row)
