#!/usr/bin/env python
"""Test Railway database connection and backend service."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv

# Load .env from backend directory
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

db_url = os.getenv("DATABASE_URL")
print(f"DATABASE_URL: {db_url[:50]}..." if db_url else "DATABASE_URL not set")

if db_url:
    try:
        from backend.app.services.f1_analysis_service import F1AnalysisService
        service = F1AnalysisService()
        
        # Test connection with simple query
        result = service._execute_query("SELECT 1 AS test")
        print(f"✓ Database connection successful: {result}")
        
        # Test driver performance ranking
        driver_perf = service.driver_performance_ranking(season=2024, limit=5)
        print(f"✓ Driver performance ranking: {len(driver_perf)} records fetched")
        if driver_perf:
            print(f"  Sample: {driver_perf[0]}")
            
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {str(e)}")
else:
    print("✗ DATABASE_URL not set in environment")
