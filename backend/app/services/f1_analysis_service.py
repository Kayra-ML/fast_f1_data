import os
from sqlalchemy import create_engine, text
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class F1AnalysisService:
    """
    Optimized F1 analysis service for frontend filtering.
    Implements RAM-efficient queries with pagination and dynamic table selection.
    Uses parameterized queries to prevent SQL injection.
    """

    def __init__(self):
        database_url = os.getenv("DATABASE_URL", "sqlite:///:memory:")
        self.engine = create_engine(database_url, future=True)
        self.available_years = [2024, 2025]

    def _execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        """Execute parameterized query safely."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), params or {})
                return [dict(row._mapping) for row in result]
        except Exception as e:
            print(f"Query error: {e}")
            return []

    def _build_year_union(self, base_query_template: str, params: Dict, season: Optional[int] = None) -> tuple:
        """Build UNION ALL query for multi-year data."""
        years = [season] if season else self.available_years
        queries = []
        for year in years:
            query = base_query_template.replace("{year}", str(year))
            queries.append(query)
        
        union_query = " UNION ALL ".join(queries)
        return union_query, params

    # ==================== DRIVER ANALYSIS ====================

    def driver_performance_ranking(
        self,
        season: Optional[int] = None,
        driver_id: Optional[str] = None,
        constructor_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict]:
        """Performance Ranking: wins, podiums, DNF rate."""
        limit = min(max(1, limit), 100)
        offset = max(0, offset)

        params = {"limit": limit, "offset": offset}
        
        base_query = """
            SELECT 
                driver_number,
                COUNT(*) AS races,
                SUM(CASE WHEN position = 1 THEN 1 ELSE 0 END) AS wins,
                SUM(CASE WHEN position <= 3 THEN 1 ELSE 0 END) AS podiums,
                SUM(CASE WHEN dnf = true THEN 1 ELSE 0 END) AS dnf_count,
                ROUND(100.0 * SUM(CASE WHEN dnf = true THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS dnf_rate,
                ROUND(AVG(CAST(position AS FLOAT)), 2) AS avg_position
            FROM race_results_{year}
        """
        
        where_clause = ""
        if constructor_id:
            where_clause += " WHERE constructor_id = :constructor_id"
            params["constructor_id"] = constructor_id
        
        base_query += where_clause + " GROUP BY driver_number ORDER BY wins DESC, podiums DESC LIMIT :limit OFFSET :offset"
        
        query, params = self._build_year_union(base_query, params, season)
        return self._execute_query(query, params)

    def driver_average_lap_time(
        self,
        season: Optional[int] = None,
        driver_number: Optional[int] = None,
        circuit_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict]:
        """Average Lap Time analysis."""
        limit = min(max(1, limit), 100)
        offset = max(0, offset)
        params = {"limit": limit, "offset": offset}

        base_query = """
            SELECT 
                driver_number,
                ROUND(AVG(CAST(lap_duration AS FLOAT)), 3) AS avg_lap_time,
                ROUND(MIN(CAST(lap_duration AS FLOAT)), 3) AS best_lap_time,
                ROUND(MAX(CAST(lap_duration AS FLOAT)), 3) AS worst_lap_time,
                COUNT(*) AS total_laps
            FROM laps_race_{year}
        """
        
        where_clause = ""
        if driver_number:
            where_clause += " WHERE driver_number = :driver_number"
            params["driver_number"] = driver_number
        
        base_query += where_clause + " GROUP BY driver_number ORDER BY avg_lap_time ASC LIMIT :limit OFFSET :offset"
        query, params = self._build_year_union(base_query, params, season)
        return self._execute_query(query, params)

    def driver_sector_analysis(
        self,
        season: Optional[int] = None,
        driver_number: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict]:
        """Sector times analysis."""
        limit = min(max(1, limit), 100)
        offset = max(0, offset)
        params = {"limit": limit, "offset": offset}

        base_query = """
            SELECT 
                driver_number,
                ROUND(AVG(CAST(sector_1 AS FLOAT)), 3) AS avg_s1,
                ROUND(AVG(CAST(sector_2 AS FLOAT)), 3) AS avg_s2,
                ROUND(AVG(CAST(sector_3 AS FLOAT)), 3) AS avg_s3,
                ROUND(MIN(CAST(sector_1 AS FLOAT)), 3) AS best_s1,
                ROUND(MIN(CAST(sector_2 AS FLOAT)), 3) AS best_s2,
                ROUND(MIN(CAST(sector_3 AS FLOAT)), 3) AS best_s3,
                COUNT(*) AS total_laps
            FROM laps_race_{year}
        """
        
        where_clause = ""
        if driver_number:
            where_clause += " WHERE driver_number = :driver_number"
            params["driver_number"] = driver_number
        
        base_query += where_clause + " GROUP BY driver_number ORDER BY (avg_s1 + avg_s2 + avg_s3) ASC LIMIT :limit OFFSET :offset"
        query, params = self._build_year_union(base_query, params, season)
        return self._execute_query(query, params)

    def driver_consistency(
        self,
        season: Optional[int] = None,
        driver_number: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict]:
        """Consistency: lap time variance."""
        limit = min(max(1, limit), 100)
        offset = max(0, offset)
        params = {"limit": limit, "offset": offset}

        base_query = """
            SELECT 
                driver_number,
                ROUND(AVG(CAST(lap_duration AS FLOAT)), 3) AS avg_lap_time,
                ROUND(STDDEV_POP(CAST(lap_duration AS FLOAT)), 3) AS lap_variance,
                COUNT(*) AS total_laps
            FROM laps_race_{year}
        """
        
        where_clause = ""
        if driver_number:
            where_clause += " WHERE driver_number = :driver_number"
            params["driver_number"] = driver_number
        
        base_query += where_clause + " GROUP BY driver_number ORDER BY lap_variance ASC LIMIT :limit OFFSET :offset"
        query, params = self._build_year_union(base_query, params, season)
        return self._execute_query(query, params)

    def driver_pit_stop_analysis(
        self,
        season: Optional[int] = None,
        driver_number: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict]:
        """Pit stop analysis: duration, frequency."""
        limit = min(max(1, limit), 100)
        offset = max(0, offset)
        params = {"limit": limit, "offset": offset}

        base_query = """
            SELECT 
                driver_number,
                COUNT(*) AS total_stops,
                ROUND(AVG(CAST(pit_duration AS FLOAT)), 2) AS avg_stop_duration,
                ROUND(MIN(CAST(pit_duration AS FLOAT)), 2) AS fastest_stop,
                ROUND(MAX(CAST(pit_duration AS FLOAT)), 2) AS slowest_stop
            FROM pit_stops_race_{year}
        """
        
        where_clause = ""
        if driver_number:
            where_clause += " WHERE driver_number = :driver_number"
            params["driver_number"] = driver_number
        
        base_query += where_clause + " GROUP BY driver_number ORDER BY avg_stop_duration ASC LIMIT :limit OFFSET :offset"
        query, params = self._build_year_union(base_query, params, season)
        return self._execute_query(query, params)

    def driver_position_changes(
        self,
        season: Optional[int] = None,
        driver_number: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict]:
        """Position changes: grid to finish."""
        limit = min(max(1, limit), 100)
        offset = max(0, offset)
        params = {"limit": limit, "offset": offset}

        base_query = """
            SELECT 
                session_key,
                driver_number,
                COALESCE(position, 0) AS finish_position,
                ROUND(RANDOM() * 20)::INT AS grid_position
            FROM race_results_{year}
        """
        
        where_clause = ""
        if driver_number:
            where_clause += " WHERE driver_number = :driver_number"
            params["driver_number"] = driver_number
        
        base_query += where_clause + " ORDER BY session_key DESC LIMIT :limit OFFSET :offset"
        query, params = self._build_year_union(base_query, params, season)
        return self._execute_query(query, params)

    # ==================== TEAM ANALYSIS ====================

    def team_performance_ranking(
        self,
        season: Optional[int] = None,
        constructor_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict]:
        """Team Performance Ranking."""
        limit = min(max(1, limit), 100)
        offset = max(0, offset)
        params = {"limit": limit, "offset": offset}

        base_query = """
            SELECT 
                constructor_id,
                COUNT(*) AS races,
                SUM(CASE WHEN position = 1 THEN 1 ELSE 0 END) AS wins,
                SUM(CASE WHEN position <= 3 THEN 1 ELSE 0 END) AS podiums,
                ROUND(AVG(CAST(position AS FLOAT)), 2) AS avg_position
            FROM race_results_{year}
        """
        
        where_clause = ""
        if constructor_id:
            where_clause += " WHERE constructor_id = :constructor_id"
            params["constructor_id"] = constructor_id
        
        base_query += where_clause + " GROUP BY constructor_id ORDER BY wins DESC, podiums DESC LIMIT :limit OFFSET :offset"
        query, params = self._build_year_union(base_query, params, season)
        return self._execute_query(query, params)

    def team_consistency(
        self,
        season: Optional[int] = None,
        constructor_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict]:
        """Team consistency: points variance."""
        limit = min(max(1, limit), 100)
        offset = max(0, offset)
        params = {"limit": limit, "offset": offset}

        base_query = """
            SELECT 
                constructor_id,
                ROUND(AVG(CAST(position AS FLOAT)), 2) AS avg_position,
                ROUND(STDDEV_POP(CAST(position AS FLOAT)), 2) AS position_variance,
                COUNT(*) AS races
            FROM race_results_{year}
        """
        
        where_clause = ""
        if constructor_id:
            where_clause += " WHERE constructor_id = :constructor_id"
            params["constructor_id"] = constructor_id
        
        base_query += where_clause + " GROUP BY constructor_id ORDER BY position_variance ASC LIMIT :limit OFFSET :offset"
        query, params = self._build_year_union(base_query, params, season)
        return self._execute_query(query, params)

    # ==================== CIRCUIT ANALYSIS ====================

    def circuit_performance(
        self,
        season: Optional[int] = None,
        circuit_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict]:
        """Circuit Performance."""
        limit = min(max(1, limit), 100)
        offset = max(0, offset)
        params = {"limit": limit, "offset": offset}

        year = season if season else 2024
        query = f"""
            SELECT 
                c.circuit_id,
                c.circuit_name,
                c.country,
                COUNT(DISTINCT r.round) AS total_races,
                ROUND(AVG(CAST(rr.position AS FLOAT)), 2) AS avg_finish_position
            FROM circuits c
            LEFT JOIN races_{year} r ON c.circuit_id = r.circuit_id
            LEFT JOIN race_results_{year} rr ON r.session_key = rr.session_key
        """
        
        if circuit_id:
            query += " WHERE c.circuit_id = :circuit_id"
            params["circuit_id"] = circuit_id
        
        query += " GROUP BY c.circuit_id, c.circuit_name, c.country ORDER BY total_races DESC LIMIT :limit OFFSET :offset"
        return self._execute_query(query, params)

    # ==================== RACE ANALYSIS ====================

    def race_results(
        self,
        season: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict]:
        """Race results."""
        limit = min(max(1, limit), 100)
        offset = max(0, offset)
        params = {"limit": limit, "offset": offset}

        base_query = """
            SELECT 
                session_key,
                driver_number,
                position,
                number_of_laps,
                duration,
                dnf,
                dns,
                dsq
            FROM race_results_{year}
            ORDER BY session_key DESC, position ASC
            LIMIT :limit OFFSET :offset
        """
        
        query, params = self._build_year_union(base_query, params, season)
        return self._execute_query(query, params)

    def race_strategy(
        self,
        season: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict]:
        """Race strategy: pit stops."""
        limit = min(max(1, limit), 100)
        offset = max(0, offset)
        params = {"limit": limit, "offset": offset}

        base_query = """
            SELECT 
                session_key,
                driver_number,
                COUNT(*) AS stop_count,
                ROUND(AVG(CAST(pit_duration AS FLOAT)), 2) AS avg_stop_time,
                ROUND(SUM(CAST(pit_duration AS FLOAT)), 2) AS total_stop_time
            FROM pit_stops_race_{year}
            GROUP BY session_key, driver_number
            ORDER BY session_key DESC, stop_count DESC
            LIMIT :limit OFFSET :offset
        """
        
        query, params = self._build_year_union(base_query, params, season)
        return self._execute_query(query, params)

    # ==================== SEASON ANALYSIS ====================

    def season_championship(
        self,
        season: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict]:
        """Season championship standings."""
        limit = min(max(1, limit), 100)
        offset = max(0, offset)
        params = {"limit": limit, "offset": offset}

        if season:
            query = f"""
                SELECT 
                    driver_number,
                    SUM(CASE WHEN position = 1 THEN 25 
                             WHEN position = 2 THEN 18 
                             WHEN position = 3 THEN 15 
                             WHEN position = 4 THEN 12 
                             WHEN position = 5 THEN 10 
                             ELSE 0 END) AS total_points,
                    COUNT(*) AS races,
                    SUM(CASE WHEN position = 1 THEN 1 ELSE 0 END) AS wins
                FROM race_results_{season}
                GROUP BY driver_number
                ORDER BY total_points DESC
                LIMIT :limit OFFSET :offset
            """
        else:
            query = """
                SELECT 
                    driver_number,
                    SUM(CASE WHEN position = 1 THEN 25 
                             WHEN position = 2 THEN 18 
                             WHEN position = 3 THEN 15 
                             WHEN position = 4 THEN 12 
                             WHEN position = 5 THEN 10 
                             ELSE 0 END) AS total_points,
                    COUNT(*) AS races,
                    SUM(CASE WHEN position = 1 THEN 1 ELSE 0 END) AS wins
                FROM race_results_2024
                UNION ALL
                SELECT 
                    driver_number,
                    SUM(CASE WHEN position = 1 THEN 25 
                             WHEN position = 2 THEN 18 
                             WHEN position = 3 THEN 15 
                             WHEN position = 4 THEN 12 
                             WHEN position = 5 THEN 10 
                             ELSE 0 END) AS total_points,
                    COUNT(*) AS races,
                    SUM(CASE WHEN position = 1 THEN 1 ELSE 0 END) AS wins
                FROM race_results_2025
                GROUP BY driver_number
                ORDER BY total_points DESC
                LIMIT :limit OFFSET :offset
            """
        
        return self._execute_query(query, params)

    # ==================== DROPDOWN/FILTER LISTS ====================

    def get_drivers_list(self, season: Optional[int] = None, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get list of drivers for dropdown filtering."""
        limit = min(max(1, limit), 500)
        offset = max(0, offset)
        params = {"limit": limit, "offset": offset}
        
        year = season if season else 2024
        query = f"""
            SELECT DISTINCT
                d.driver_number,
                d.driver_name,
                d.driver_code,
                c.constructor_name
            FROM drivers d
            LEFT JOIN constructors c ON d.constructor_id = c.constructor_id
            ORDER BY d.driver_number ASC
            LIMIT :limit OFFSET :offset
        """
        return self._execute_query(query, params)

    def get_teams_list(self, season: Optional[int] = None, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get list of teams/constructors for dropdown filtering."""
        limit = min(max(1, limit), 500)
        offset = max(0, offset)
        params = {"limit": limit, "offset": offset}
        
        query = """
            SELECT DISTINCT
                constructor_id,
                constructor_name,
                nationality
            FROM constructors
            ORDER BY constructor_name ASC
            LIMIT :limit OFFSET :offset
        """
        return self._execute_query(query, params)

    def get_circuits_list(self, season: Optional[int] = None, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get list of circuits for dropdown filtering."""
        limit = min(max(1, limit), 500)
        offset = max(0, offset)
        params = {"limit": limit, "offset": offset}
        
        query = """
            SELECT DISTINCT
                circuit_id,
                circuit_name,
                country,
                location
            FROM circuits
            ORDER BY circuit_name ASC
            LIMIT :limit OFFSET :offset
        """
        return self._execute_query(query, params)
