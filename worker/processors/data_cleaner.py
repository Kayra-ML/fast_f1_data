from sqlalchemy import create_engine, text


class DataCleaner:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, future=True)

    def clean_all(self) -> None:
        self.clean_sessions()
        self.clean_race_results()
        self.clean_pit_stops()
        self.clean_laps()

    def clean_sessions(self) -> None:
        with self.engine.begin() as conn:
            conn.execute(text(
                "UPDATE sessions SET session_name = TRIM(session_name), location = TRIM(location), country_name = TRIM(country_name), circuit_short_name = TRIM(circuit_short_name) WHERE session_key IS NOT NULL"
            ))

    def clean_race_results(self) -> None:
        with self.engine.begin() as conn:
            conn.execute(text(
                "UPDATE race_results SET status = TRIM(status), time = TRIM(time), fastest_lap_time = TRIM(fastest_lap_time) WHERE season IS NOT NULL"
            ))

    def clean_pit_stops(self) -> None:
        with self.engine.begin() as conn:
            conn.execute(text(
                "UPDATE pit_stops SET time = TRIM(time), duration = TRIM(duration) WHERE season IS NOT NULL"
            ))

    def clean_laps(self) -> None:
        with self.engine.begin() as conn:
            conn.execute(text(
                "UPDATE laps SET sector_1 = NULLIF(TRIM(CAST(sector_1 AS TEXT)), ''), sector_2 = NULLIF(TRIM(CAST(sector_2 AS TEXT)), ''), sector_3 = NULLIF(TRIM(CAST(sector_3 AS TEXT)), '') WHERE session_key IS NOT NULL"
            ))
