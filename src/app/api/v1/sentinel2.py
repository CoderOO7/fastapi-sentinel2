from fastapi import APIRouter, Depends, Request, Response
from shapely.geometry import shape
from datetime import datetime

from ...schemas.sentinel2 import Sentinel2Query
from ...core.exceptions.http_exceptions import CustomException
from ...core.utils.sentinel2 import query_sentinel2_data, calculate_ndvi_stats

router = APIRouter(prefix="/sentinel2", tags=["sentinel2"])

@router.post("/query")
async def query_sentinel2(data: Sentinel2Query):
    try:
        timestamp = datetime.fromisoformat(data.timestamp).strftime('%Y-%m-%d')
        polygon = shape(data.geojson_polygon.dict())
    except Exception as e:
        raise CustomException(status_code=400, detail=f"Invalid GeoJSON Polygon: {e}")
    
    try:
        data = query_sentinel2_data(timestamp, polygon)
        stats = calculate_ndvi_stats(data, polygon)
        return stats
    except Exception as e:
        raise CustomException(status_code=500, detail=f"Error querying Sentinel2 data: {e}")

