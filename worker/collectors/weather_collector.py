import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


class WeatherCollector:
    def __init__(self, database_url: str = None):
        if database_url:
            self.engine = create_engine(database_url, future=True)
        else:
            load_dotenv()
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                raise RuntimeError("DATABASE_URL environment variable is required")
            self.engine = create_engine(database_url, future=True)

    def collect_race_weather_summary(self) -> None:
        query = """
        SELECT session_key,
               COUNT(*) AS total_records,
               AVG(air_temperature) AS avg_air_temp,
               AVG(track_temperature) AS avg_track_temp,
               AVG(humidity) AS avg_humidity,
               AVG(pressure) AS avg_pressure,
               AVG(wind_speed) AS avg_wind_speed,
               SUM(CASE WHEN rainfall THEN 1 ELSE 0 END) AS rainfall_count
        FROM weather_race_2024
        GROUP BY session_key
        UNION ALL
        SELECT session_key,
               COUNT(*) AS total_records,
               AVG(air_temperature) AS avg_air_temp,
               AVG(track_temperature) AS avg_track_temp,
               AVG(humidity) AS avg_humidity,
               AVG(pressure) AS avg_pressure,
               AVG(wind_speed) AS avg_wind_speed,
               SUM(CASE WHEN rainfall THEN 1 ELSE 0 END) AS rainfall_count
        FROM weather_race_2025
        GROUP BY session_key
        ORDER BY session_key DESC
        LIMIT 50
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = [dict(row._mapping) for row in result]

        print("=== Race Weather Summary ===")
        for row in rows:
            print(row)

    def collect_practice_weather_summary(self) -> None:
        query = """
        SELECT session_key,
               COUNT(*) AS total_records,
               AVG(air_temperature) AS avg_air_temp,
               AVG(track_temperature) AS avg_track_temp,
               AVG(humidity) AS avg_humidity,
               AVG(pressure) AS avg_pressure,
               AVG(wind_speed) AS avg_wind_speed,
               SUM(CASE WHEN rainfall THEN 1 ELSE 0 END) AS rainfall_count
        FROM weather_practice_2024
        GROUP BY session_key
        UNION ALL
        SELECT session_key,
               COUNT(*) AS total_records,
               AVG(air_temperature) AS avg_air_temp,
               AVG(track_temperature) AS avg_track_temp,
               AVG(humidity) AS avg_humidity,
               AVG(pressure) AS avg_pressure,
               AVG(wind_speed) AS avg_wind_speed,
               SUM(CASE WHEN rainfall THEN 1 ELSE 0 END) AS rainfall_count
        FROM weather_practice_2025
        GROUP BY session_key
        ORDER BY session_key DESC
        LIMIT 50
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = [dict(row._mapping) for row in result]

        print("=== Practice Weather Summary ===")
        for row in rows:
            print(row)
