from fastapi import FastAPI
from backend.app.routes.analysis import router as analysis_router
from backend.app.services.f1_analysis_service import F1AnalysisService

app = FastAPI(title="F1 Data Analysis API")

app.include_router(analysis_router, prefix="/analysis", tags=["analysis"])

@app.get("/", tags=["root"])
def root():
    return {"message": "F1 Data Analysis API is running."}

@app.get("/health", tags=["health"])
def health_check():
    """Test Railway PostgreSQL connection."""
    try:
        service = F1AnalysisService()
        # Simple test query
        result = service._execute_query("SELECT 1 AS test")
        if result:
            return {"status": "healthy", "database": "connected", "test": result[0]}
        else:
            return {"status": "unhealthy", "database": "error"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
