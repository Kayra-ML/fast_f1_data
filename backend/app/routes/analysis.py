from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from backend.app.services.f1_analysis_service import F1AnalysisService

router = APIRouter()


def get_analysis_service() -> F1AnalysisService:
    """Dependency injection for analysis service."""
    return F1AnalysisService()


# ==================== DRIVER ANALYSIS ====================

@router.get("/driver/performance-ranking")
def driver_performance_ranking(
    season: Optional[int] = Query(None, description="Season year"),
    driver_id: Optional[str] = Query(None, description="Driver ID"),
    constructor_id: Optional[str] = Query(None, description="Constructor ID"),
    limit: int = Query(50, ge=1, le=100, description="Max results"),
    offset: int = Query(0, ge=0, description="Offset"),
    service: F1AnalysisService = Depends(get_analysis_service),
):
    try:
        return service.driver_performance_ranking(season, driver_id, constructor_id, limit, offset)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@router.get("/driver/average-lap-time")
def driver_average_lap_time(
    season: Optional[int] = Query(None, description="Season year"),
    driver_number: Optional[int] = Query(None, description="Driver number"),
    circuit_id: Optional[str] = Query(None, description="Circuit ID"),
    limit: int = Query(50, ge=1, le=100, description="Max results"),
    offset: int = Query(0, ge=0, description="Offset"),
    service: F1AnalysisService = Depends(get_analysis_service),
):
    try:
        return service.driver_average_lap_time(season, driver_number, circuit_id, limit, offset)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@router.get("/driver/sector-analysis")
def driver_sector_analysis(
    season: Optional[int] = Query(None, description="Season year"),
    driver_number: Optional[int] = Query(None, description="Driver number"),
    limit: int = Query(50, ge=1, le=100, description="Max results"),
    offset: int = Query(0, ge=0, description="Offset"),
    service: F1AnalysisService = Depends(get_analysis_service),
):
    try:
        return service.driver_sector_analysis(season, driver_number, limit, offset)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@router.get("/driver/consistency")
def driver_consistency(
    season: Optional[int] = Query(None, description="Season year"),
    driver_number: Optional[int] = Query(None, description="Driver number"),
    limit: int = Query(50, ge=1, le=100, description="Max results"),
    offset: int = Query(0, ge=0, description="Offset"),
    service: F1AnalysisService = Depends(get_analysis_service),
):
    try:
        return service.driver_consistency(season, driver_number, limit, offset)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@router.get("/driver/pit-stop-analysis")
def driver_pit_stop_analysis(
    season: Optional[int] = Query(None, description="Season year"),
    driver_number: Optional[int] = Query(None, description="Driver number"),
    limit: int = Query(50, ge=1, le=100, description="Max results"),
    offset: int = Query(0, ge=0, description="Offset"),
    service: F1AnalysisService = Depends(get_analysis_service),
):
    try:
        return service.driver_pit_stop_analysis(season, driver_number, limit, offset)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@router.get("/driver/position-changes")
def driver_position_changes(
    season: Optional[int] = Query(None, description="Season year"),
    driver_number: Optional[int] = Query(None, description="Driver number"),
    limit: int = Query(50, ge=1, le=100, description="Max results"),
    offset: int = Query(0, ge=0, description="Offset"),
    service: F1AnalysisService = Depends(get_analysis_service),
):
    try:
        return service.driver_position_changes(season, driver_number, limit, offset)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

# ==================== TEAM ANALYSIS ====================

@router.get("/team/performance-ranking")
def team_performance_ranking(
    season: Optional[int] = Query(None, description="Season year"),
    constructor_id: Optional[str] = Query(None, description="Constructor ID"),
    limit: int = Query(50, ge=1, le=100, description="Max results"),
    offset: int = Query(0, ge=0, description="Offset"),
    service: F1AnalysisService = Depends(get_analysis_service),
):
    try:
        return service.team_performance_ranking(season, constructor_id, limit, offset)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@router.get("/team/consistency")
def team_consistency(
    season: Optional[int] = Query(None, description="Season year"),
    constructor_id: Optional[str] = Query(None, description="Constructor ID"),
    limit: int = Query(50, ge=1, le=100, description="Max results"),
    offset: int = Query(0, ge=0, description="Offset"),
    service: F1AnalysisService = Depends(get_analysis_service),
):
    try:
        return service.team_consistency(season, constructor_id, limit, offset)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

# ==================== CIRCUIT ANALYSIS ====================

@router.get("/circuit/performance")
def circuit_performance(
    season: Optional[int] = Query(None, description="Season year"),
    circuit_id: Optional[str] = Query(None, description="Circuit ID"),
    limit: int = Query(50, ge=1, le=100, description="Max results"),
    offset: int = Query(0, ge=0, description="Offset"),
    service: F1AnalysisService = Depends(get_analysis_service),
):
    try:
        return service.circuit_performance(season, circuit_id, limit, offset)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

# ==================== RACE ANALYSIS ====================

@router.get("/race/results")
def race_results(
    season: Optional[int] = Query(None, description="Season year"),
    limit: int = Query(50, ge=1, le=100, description="Max results"),
    offset: int = Query(0, ge=0, description="Offset"),
    service: F1AnalysisService = Depends(get_analysis_service),
):
    try:
        return service.race_results(season, limit, offset)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@router.get("/race/strategy")
def race_strategy(
    season: Optional[int] = Query(None, description="Season year"),
    limit: int = Query(50, ge=1, le=100, description="Max results"),
    offset: int = Query(0, ge=0, description="Offset"),
    service: F1AnalysisService = Depends(get_analysis_service),
):
    try:
        return service.race_strategy(season, limit, offset)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

# ==================== SEASON ANALYSIS ====================

@router.get("/season/championship")
def season_championship(
    season: Optional[int] = Query(None, description="Season year"),
    limit: int = Query(50, ge=1, le=100, description="Max results"),
    offset: int = Query(0, ge=0, description="Offset"),
    service: F1AnalysisService = Depends(get_analysis_service),
):
    try:
        return service.season_championship(season, limit, offset)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
