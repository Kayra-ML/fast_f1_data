import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


class SessionResultsCollector:
    def __init__(self, database_url: str = None):
        if database_url:
            self.engine = create_engine(database_url, future=True)
        else:
            load_dotenv()
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                raise RuntimeError("DATABASE_URL environment variable is required")
            self.engine = create_engine(database_url, future=True)

    def collect_race_results_summary(self) -> None:
        query = """
        SELECT season,
               round,
               COUNT(*) AS total_results,
               AVG(position) AS avg_finish_position,
               SUM(points) AS total_points
        FROM race_results
        GROUP BY season, round
        ORDER BY season DESC, round DESC
        LIMIT 25
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = [dict(row._mapping) for row in result]

        print("=== Race Results Summary ===")
        for row in rows:
            print(row)
