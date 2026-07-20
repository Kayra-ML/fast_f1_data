import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


class SessionCollector:
    def __init__(self, database_url: str = None):
        if database_url:
            self.engine = create_engine(database_url, future=True)
        else:
            load_dotenv()
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                raise RuntimeError("DATABASE_URL environment variable is required")
            self.engine = create_engine(database_url, future=True)

    def collect_session_summary(self) -> None:
        query = """
        SELECT session_type,
               COUNT(*) AS total_sessions,
               MIN(date_start) AS first_start,
               MAX(date_end) AS last_end
        FROM sessions
        GROUP BY session_type
        ORDER BY total_sessions DESC
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = [dict(row._mapping) for row in result]

        print("=== Session Summary ===")
        for row in rows:
            print(row)
