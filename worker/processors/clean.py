from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os


class DataCleaner:
    def __init__(self):
        load_dotenv()
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise RuntimeError("DATABASE_URL environment variable is required")
        self.engine = create_engine(database_url, future=True)

    def clean_sessions(self):
        query = """
        UPDATE sessions
        SET session_name = TRIM(session_name),
            location = TRIM(location),
            country_name = TRIM(country_name),
            circuit_short_name = TRIM(circuit_short_name)
        WHERE session_key IS NOT NULL
        """
        with self.engine.begin() as conn:
            conn.execute(text(query))
