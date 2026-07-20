from sqlalchemy import create_engine, text


class SessionCollector:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, future=True)

    def collect_session_summary(self):
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
        print("Session summary:")
        for row in rows:
            print(row)
