import json
import os
from typing import Any, Dict, List, Optional

import pandas as pd
from sqlalchemy import Table, MetaData, create_engine
from sqlalchemy.dialects.postgresql import insert


class PostgresLoader:
    def __init__(self, database_url: str, data_dir: str = "f1_data", years: Optional[List[int]] = None):
        self.engine = create_engine(database_url, future=True)
        self.data_dir = data_dir
        self.years = years or [2024, 2025]
        self.metadata = MetaData()

    def _read_json_file(self, path: str) -> List[Dict[str, Any]]:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            if "data" in data and isinstance(data["data"], list):
                return data["data"]
            if "MRData" in data:
                inner = data["MRData"]
                if "RaceTable" in inner and "Races" in inner["RaceTable"]:
                    return inner["RaceTable"]["Races"]
                if "DriverTable" in inner and "Drivers" in inner["DriverTable"]:
                    return inner["DriverTable"]["Drivers"]
                if "ConstructorTable" in inner and "Constructors" in inner["ConstructorTable"]:
                    return inner["ConstructorTable"]["Constructors"]
            return [data]
        return data if isinstance(data, list) else []

    def _read_yearly_files(self, patterns: List[str]) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        for year in self.years:
            for pattern in patterns:
                path = os.path.join(self.data_dir, str(year), pattern.format(year=year))
                if os.path.exists(path):
                    rows.extend(self._read_json_file(path))
        return rows

    def _normalize_dataframe(self, rows: List[Dict[str, Any]]) -> pd.DataFrame:
        if not rows:
            return pd.DataFrame()
        return pd.json_normalize(rows, sep="_")

    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        for column in df.columns:
            if df[column].dtype == object:
                df[column] = df[column].astype(str).str.strip()
                df[column] = df[column].replace({"nan": None, "None": None, "": None})
        return df

    def _bulk_upsert(self, df: pd.DataFrame, table_name: str, primary_keys: List[str]) -> int:
        if df.empty:
            return 0

        df = self._clean_dataframe(df)
        df = df.where(pd.notnull(df), None)
        df = df.drop_duplicates(subset=primary_keys)
        records = df.to_dict(orient="records")

        table = Table(table_name, self.metadata, autoload_with=self.engine)
        stmt = insert(table).values(records)
        update_dict = {c.name: c for c in stmt.excluded if c.name not in primary_keys}
        if update_dict:
            stmt = stmt.on_conflict_do_update(index_elements=primary_keys, set_=update_dict)
        else:
            stmt = stmt.on_conflict_do_nothing(index_elements=primary_keys)

        with self.engine.begin() as conn:
            conn.execute(stmt)

        return len(records)

    def _cast_columns(self, df: pd.DataFrame, date_columns: List[str], int_columns: List[str], float_columns: List[str]):
        for column in date_columns:
            if column in df.columns:
                df[column] = pd.to_datetime(df[column], errors="coerce")
        for column in int_columns:
            if column in df.columns:
                df[column] = pd.to_numeric(df[column], errors="coerce", downcast="integer")
        for column in float_columns:
            if column in df.columns:
                df[column] = pd.to_numeric(df[column], errors="coerce")
        return df

    def _load_table(self, patterns: List[str], rename_map: Dict[str, str], table_name: str, primary_keys: List[str], date_columns: Optional[List[str]] = None, int_columns: Optional[List[str]] = None, float_columns: Optional[List[str]] = None):
        rows = self._read_yearly_files(patterns)
        if not rows:
            print(f"{table_name} için veri dosyası bulunamadı.")
            return 0

        df = self._normalize_dataframe(rows)
        df = df.rename(columns=rename_map)
        df = self._cast_columns(df, date_columns or [], int_columns or [], float_columns or [])
        count = self._bulk_upsert(df, table_name, primary_keys)
        print(f"{table_name} tablosuna {count} kayıt aktarıldı.")
        return count

    def load_drivers(self) -> int:
        return self._load_table(
            patterns=["drivers_{year}.json"],
            rename_map={
                "driverId": "driver_id",
                "permanentNumber": "permanent_number",
                "code": "code",
                "givenName": "given_name",
                "familyName": "family_name",
                "dateOfBirth": "date_of_birth",
                "nationality": "nationality"
            },
            table_name="drivers",
            primary_keys=["driver_id"],
            date_columns=["date_of_birth"],
            int_columns=["permanent_number"]
        )

    def load_constructors(self) -> int:
        return self._load_table(
            patterns=["constructors_{year}.json"],
            rename_map={"constructorId": "constructor_id", "name": "name", "nationality": "nationality"},
            table_name="constructors",
            primary_keys=["constructor_id"]
        )

    def load_circuits(self) -> int:
        rows = self._read_yearly_files(["circuits_{year}.json"])
        if not rows:
            print("circuits için veri dosyası bulunamadı.")
            return 0

        df = self._normalize_dataframe(rows)
        if "Location_lat" in df.columns:
            df["lat"] = pd.to_numeric(df["Location_lat"], errors="coerce")
        if "Location_long" in df.columns:
            df["lng"] = pd.to_numeric(df["Location_long"], errors="coerce")
        if "Location_locality" in df.columns:
            df["location"] = df["Location_locality"]
        if "Location_country" in df.columns:
            df["country"] = df["Location_country"]

        df = df.rename(columns={"circuitId": "circuit_id", "circuitName": "circuit_name"})
        df = self._cast_columns(df, date_columns=[], int_columns=[], float_columns=["lat", "lng"])
        count = self._bulk_upsert(df, "circuits", ["circuit_id"])
        print(f"circuits tablosuna {count} kayıt aktarıldı.")
        return count

    def load_races(self) -> int:
        rows = self._read_yearly_files(["races_{year}.json"])
        if not rows:
            print("races için veri dosyası bulunamadı.")
            return 0

        df = self._normalize_dataframe(rows)
        if "Circuit_circuitId" in df.columns:
            df["circuit_id"] = df["Circuit_circuitId"]
        df = df.rename(columns={"raceName": "race_name"})
        df = self._cast_columns(df, date_columns=["date"], int_columns=["season", "round"], float_columns=[])
        count = self._bulk_upsert(df, "races", ["season", "round"])
        print(f"races tablosuna {count} kayıt aktarıldı.")
        return count

    def load_sessions(self) -> int:
        return self._load_table(
            patterns=["sessions_{year}.json"],
            rename_map={
                "sessionKey": "session_key",
                "sessionName": "session_name",
                "dateStart": "date_start",
                "dateEnd": "date_end",
                "gmtOffset": "gmt_offset",
                "sessionType": "session_type",
                "meetingKey": "meeting_key",
                "location": "location",
                "countryKey": "country_key",
                "countryCode": "country_code",
                "countryName": "country_name",
                "circuitKey": "circuit_key",
                "circuitShortName": "circuit_short_name",
                "year": "year"
            },
            table_name="sessions",
            primary_keys=["session_key"],
            date_columns=["date_start", "date_end"],
            int_columns=["session_key", "meeting_key", "country_key", "circuit_key", "year"]
        )

    def load_race_results(self) -> int:
        return self._load_table(
            patterns=["race_results_{year}.json", "results_{year}.json"],
            rename_map={
                "season": "season",
                "round": "round",
                "driverId": "driver_id",
                "constructorId": "constructor_id",
                "position": "position",
                "grid": "grid",
                "points": "points",
                "laps": "laps",
                "time": "time",
                "status": "status",
                "fastestLapTime": "fastest_lap_time",
                "fastestLapSpeed": "fastest_lap_speed"
            },
            table_name="race_results",
            primary_keys=["season", "round", "driver_id"],
            int_columns=["season", "round", "position", "grid", "laps"],
            float_columns=["points", "fastest_lap_speed"]
        )

    def load_qualifying_results(self) -> int:
        return self._load_table(
            patterns=["qualifying_results_{year}.json", "qualifying_{year}.json"],
            rename_map={
                "season": "season",
                "round": "round",
                "driverId": "driver_id",
                "constructorId": "constructor_id",
                "position": "position",
                "q1": "q1",
                "q2": "q2",
                "q3": "q3"
            },
            table_name="qualifying_results",
            primary_keys=["season", "round", "driver_id"],
            int_columns=["season", "round", "position"]
        )

    def load_pit_stops(self) -> int:
        return self._load_table(
            patterns=["pit_stops_{year}.json"],
            rename_map={
                "season": "season",
                "round": "round",
                "driverId": "driver_id",
                "stop": "stop",
                "lap": "lap",
                "time": "time",
                "duration": "duration",
                "milliseconds": "milliseconds"
            },
            table_name="pit_stops",
            primary_keys=["season", "round", "driver_id", "stop"],
            int_columns=["season", "round", "stop", "lap", "milliseconds"]
        )

    def load_laps(self) -> int:
        return self._load_table(
            patterns=["laps_{year}.json"],
            rename_map={
                "sessionKey": "session_key",
                "driverNumber": "driver_number",
                "lapNumber": "lap_number",
                "lapDuration": "lap_duration",
                "sector_1": "sector_1",
                "sector_2": "sector_2",
                "sector_3": "sector_3",
                "isPitOutLap": "is_pit_out_lap"
            },
            table_name="laps",
            primary_keys=["session_key", "driver_number", "lap_number"],
            int_columns=["session_key", "driver_number", "lap_number"],
            float_columns=["lap_duration", "sector_1", "sector_2", "sector_3"]
        )

    def load_weather(self) -> int:
        return self._load_table(
            patterns=["weather_{year}.json"],
            rename_map={
                "sessionKey": "session_key",
                "date": "date",
                "airTemperature": "air_temperature",
                "trackTemperature": "track_temperature",
                "humidity": "humidity",
                "pressure": "pressure",
                "windSpeed": "wind_speed",
                "windDirection": "wind_direction",
                "rainfall": "rainfall"
            },
            table_name="weather",
            primary_keys=["session_key", "date"],
            date_columns=["date"],
            int_columns=["session_key", "wind_direction"],
            float_columns=["air_temperature", "track_temperature", "humidity", "pressure", "wind_speed"]
        )

    def load_team_radio(self) -> int:
        return self._load_table(
            patterns=["team_radio_{year}.json"],
            rename_map={
                "sessionKey": "session_key",
                "driverNumber": "driver_number",
                "date": "date",
                "recordingUrl": "recording_url"
            },
            table_name="team_radio",
            primary_keys=["session_key", "driver_number", "date"],
            date_columns=["date"],
            int_columns=["session_key", "driver_number"]
        )

    def load_driver_standings(self) -> int:
        return self._load_table(
            patterns=["driver_standings_{year}.json"],
            rename_map={
                "season": "season",
                "round": "round",
                "driverId": "driver_id",
                "points": "points",
                "position": "position",
                "wins": "wins"
            },
            table_name="driver_standings",
            primary_keys=["season", "round", "driver_id"],
            int_columns=["season", "round", "position", "wins"],
            float_columns=["points"]
        )

    def load_constructor_standings(self) -> int:
        return self._load_table(
            patterns=["constructor_standings_{year}.json"],
            rename_map={
                "season": "season",
                "round": "round",
                "constructorId": "constructor_id",
                "points": "points",
                "position": "position",
                "wins": "wins"
            },
            table_name="constructor_standings",
            primary_keys=["season", "round", "constructor_id"],
            int_columns=["season", "round", "position", "wins"],
            float_columns=["points"]
        )

    def load_all(self):
        self.load_drivers()
        self.load_constructors()
        self.load_circuits()
        self.load_races()
        self.load_sessions()
        self.load_race_results()
        self.load_qualifying_results()
        self.load_pit_stops()
        self.load_laps()
        self.load_weather()
        self.load_team_radio()
        self.load_driver_standings()
        self.load_constructor_standings()
