import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


class DriverCollector:
    def __init__(self, database_url: str = None):
        if database_url:
            self.engine = create_engine(database_url, future=True)
        else:
            load_dotenv()
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                raise RuntimeError("DATABASE_URL environment variable is required")
            self.engine = create_engine(database_url, future=True)

    def collect_driver_rankings(self) -> None:
        query = """
        SELECT d.driver_id,
               d.given_name,
               d.family_name,
               COUNT(rr.*) AS races,
               SUM(rr.points) AS total_points,
               AVG(rr.position) AS avg_finish_position,
               SUM(CASE WHEN rr.position = 1 THEN 1 ELSE 0 END) AS wins
        FROM drivers d
        JOIN race_results rr ON d.driver_id = rr.driver_id
        GROUP BY d.driver_id, d.given_name, d.family_name
        ORDER BY total_points DESC
        LIMIT 25
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = [dict(row._mapping) for row in result]

        print("=== Driver Rankings ===")
        for row in rows:
            print(row)
