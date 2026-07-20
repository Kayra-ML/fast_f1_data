import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


class PositionCollector:
    def __init__(self, database_url: str = None):
        if database_url:
            self.engine = create_engine(database_url, future=True)
        else:
            load_dotenv()
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                raise RuntimeError("DATABASE_URL environment variable is required")
            self.engine = create_engine(database_url, future=True)

    def collect_grid_to_finish(self) -> None:
        query = """
        SELECT rr.season,
               rr.round,
               rr.driver_id,
               rr.grid,
               rr.position AS finish_position,
               (rr.position - rr.grid) AS position_change
        FROM race_results rr
        ORDER BY season DESC, round DESC, position_change ASC
        LIMIT 50
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = [dict(row._mapping) for row in result]

        print("=== Grid to Finish Position Changes ===")
        for row in rows:
            print(row)
