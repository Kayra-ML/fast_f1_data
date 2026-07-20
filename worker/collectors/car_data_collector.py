import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


class CarDataCollector:
    def __init__(self, database_url: str = None):
        if database_url:
            self.engine = create_engine(database_url, future=True)
        else:
            load_dotenv()
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                raise RuntimeError("DATABASE_URL environment variable is required")
            self.engine = create_engine(database_url, future=True)

    def collect_race_car_data_summary(self) -> None:
        query = """
        SELECT session_key,
               driver_number,
               COUNT(*) AS total_records,
               AVG(rpm) AS avg_rpm,
               AVG(speed) AS avg_speed,
               AVG(throttle) AS avg_throttle,
               AVG(brake) AS avg_brake,
               AVG(drs) AS avg_drs,
               MAX(speed) AS max_speed
        FROM car_data_race_2024
        GROUP BY session_key, driver_number
        UNION ALL
        SELECT session_key,
               driver_number,
               COUNT(*) AS total_records,
               AVG(rpm) AS avg_rpm,
               AVG(speed) AS avg_speed,
               AVG(throttle) AS avg_throttle,
               AVG(brake) AS avg_brake,
               AVG(drs) AS avg_drs,
               MAX(speed) AS max_speed
        FROM car_data_race_2025
        GROUP BY session_key, driver_number
        ORDER BY max_speed DESC
        LIMIT 50
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = [dict(row._mapping) for row in result]

        print("=== Race Car Data Summary ===")
        for row in rows:
            print(row)

    def collect_practice_car_data_summary(self) -> None:
        query = """
        SELECT session_key,
               driver_number,
               COUNT(*) AS total_records,
               AVG(rpm) AS avg_rpm,
               AVG(speed) AS avg_speed,
               AVG(throttle) AS avg_throttle,
               AVG(brake) AS avg_brake,
               AVG(drs) AS avg_drs,
               MAX(speed) AS max_speed
        FROM car_data_practice_2024
        GROUP BY session_key, driver_number
        UNION ALL
        SELECT session_key,
               driver_number,
               COUNT(*) AS total_records,
               AVG(rpm) AS avg_rpm,
               AVG(speed) AS avg_speed,
               AVG(throttle) AS avg_throttle,
               AVG(brake) AS avg_brake,
               AVG(drs) AS avg_drs,
               MAX(speed) AS max_speed
        FROM car_data_practice_2025
        GROUP BY session_key, driver_number
        ORDER BY max_speed DESC
        LIMIT 50
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = [dict(row._mapping) for row in result]

        print("=== Practice Car Data Summary ===")
        for row in rows:
            print(row)
