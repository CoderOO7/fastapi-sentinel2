from pydantic import BaseModel
from typing import List

class GeoJSONPolygon(BaseModel):
    type: str
    coordinates: List

    def __init__(self, **data):
        super().__init__(**data)
        if self.type != "Polygon":
            raise ValueError("Only Polygon type is supported")

class Sentinel2Query(BaseModel):
    timestamp: str
    geojson_polygon: GeoJSONPolygon
