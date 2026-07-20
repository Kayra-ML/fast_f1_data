import os
from sqlalchemy import create_engine, text
from typing import List, Dict, Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = os.getenv("ENV_FILE", ".env")


class AnalysisService:
    def __init__(self, settings: Settings = Settings()):
        self.engine = create_engine(settings.database_url, future=True)

    def _execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            return [dict(row._mapping) for row in result]

    def get_driver_performance(
        self,
        season: Optional[int] = None,
        driver_id: Optional[str] = None,
        constructor_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict]:
        limit = min(max(1, limit), 200)
        offset = max(0, offset)

        query = """
        SELECT d.driver_id, d.given_name, d.family_name,
               COUNT(rr.*) AS races,
               SUM(rr.points) AS total_points,
               AVG(rr.position) AS avg_position,
               SUM(CASE WHEN rr.position = 1 THEN 1 ELSE 0 END) AS wins
        FROM drivers d
        JOIN race_results rr ON d.driver_id = rr.driver_id
        """
        filters = []
        params: Dict[str, object] = {"limit": limit, "offset": offset}

        if season is not None:
            filters.append("rr.season = :season")
            params["season"] = season
        if driver_id is not None:
            filters.append("d.driver_id = :driver_id")
            params["driver_id"] = driver_id
        if constructor_id is not None:
            filters.append("rr.constructor_id = :constructor_id")
            params["constructor_id"] = constructor_id

        if filters:
            query += "WHERE " + " AND ".join(filters) + "\n"

        query += "GROUP BY d.driver_id, d.given_name, d.family_name\n"
        query += "ORDER BY total_points DESC\nLIMIT :limit OFFSET :offset"
        return self._execute_query(query, params)

    def get_constructor_trends(
        self,
        season: Optional[int] = None,
        constructor_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict]:
        limit = min(max(1, limit), 200)
        offset = max(0, offset)

        query = """
        SELECT c.constructor_id, c.name, c.nationality,
               COUNT(rr.*) AS races,
               SUM(rr.points) AS total_points,
               SUM(CASE WHEN rr.position = 1 THEN 1 ELSE 0 END) AS wins
        FROM constructors c
        JOIN race_results rr ON c.constructor_id = rr.constructor_id
        """
        filters = []
        params: Dict[str, object] = {"limit": limit, "offset": offset}

        if season is not None:
            filters.append("rr.season = :season")
            params["season"] = season
        if constructor_id is not None:
            filters.append("c.constructor_id = :constructor_id")
            params["constructor_id"] = constructor_id

        if filters:
            query += "WHERE " + " AND ".join(filters) + "\n"

        query += "GROUP BY c.constructor_id, c.name, c.nationality\n"
        query += "ORDER BY total_points DESC\nLIMIT :limit OFFSET :offset"
        return self._execute_query(query, params)

    def get_circuit_insights(
        self,
        season: Optional[int] = None,
        country: Optional[str] = None,
        circuit_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict]:
        limit = min(max(1, limit), 200)
        offset = max(0, offset)

        query = """
        SELECT c.circuit_id, c.circuit_name, c.country,
               COUNT(r.*) AS races,
               AVG(rr.position) AS avg_finish_position
        FROM circuits c
        JOIN races r ON c.circuit_id = r.circuit_id
        JOIN race_results rr ON r.season = rr.season AND r.round = rr.round
        """
        filters = []
        params: Dict[str, object] = {"limit": limit, "offset": offset}

        if season is not None:
            filters.append("r.season = :season")
            params["season"] = season
        if country is not None:
            filters.append("c.country ILIKE :country")
            params["country"] = f"%{country}%"
        if circuit_id is not None:
            filters.append("c.circuit_id = :circuit_id")
            params["circuit_id"] = circuit_id

        if filters:
            query += "WHERE " + " AND ".join(filters) + "\n"

        query += "GROUP BY c.circuit_id, c.circuit_name, c.country\n"
        query += "ORDER BY races DESC\nLIMIT :limit OFFSET :offset"
        return self._execute_query(query, params)
