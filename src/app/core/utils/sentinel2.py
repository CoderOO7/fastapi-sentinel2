import pystac_client

from shapely.geometry import shape
from datetime import datetime, timedelta
from odc.stac import load

from ...core.logger import logging

SENTINEL_CLIENT_URL = "https://earth-search.aws.element84.com/v1"
COLLECTION = "sentinel-2-l2a"
TIME_DELTA_IN_DAYS = 10

logger = logging.getLogger(__name__)

def query_sentinel2_data(date: str, polygon, filters = {
        "eo:cloud_cover":{"lt":0.2},
        "s2:vegetation_percentage": {"gt": 25}
    }):
    
    logger.info("executing query_sentinel2_data---")
    
    catalog = pystac_client.Client.open(
        SENTINEL_CLIENT_URL,
    )
    
    search = catalog.search(
        collections=[COLLECTION],
        intersects=polygon,
        datetime=date,
        query=filters,  
    )
    
    
    available_dates = [item.datetime.strftime("%Y-%m-%d") for item in search.items()]
    
    if not available_dates:
        logger.info('dates not available---')
        # If no data for the requested date, look for available dates around it
        delta_date_range = f"{(datetime.fromisoformat(date) - timedelta(days=TIME_DELTA_IN_DAYS)).strftime('%Y-%m-%d')}/{(datetime.fromisoformat(date) + timedelta(days=TIME_DELTA_IN_DAYS)).strftime('%Y-%m-%d')}"
        logger.info(f"delta_date_range: {delta_date_range}")
        
        search_all = catalog.search(
            collections=[COLLECTION],
            intersects=polygon,
            datetime=delta_date_range,
            query=filters
        )
        available_dates = [item.datetime.strftime("%Y-%m-%d") for item in search_all.items()]
        if not available_dates:
            raise ValueError("No data available for the specified area")

        # Find the nearest available date
        nearest_date = find_nearest_date(date, available_dates)
        logger.info(f"nearest_date: {nearest_date}")
        
        # Query again with the nearest date
        search = catalog.search(
            collections=[COLLECTION],
            intersects=polygon,
            datetime=nearest_date,
            query=filters,  
        )

    items = search.item_collection()
    logger.info(f"Returned {len(items)} items")
    
    if not items:
        raise ValueError("No Sentinel2 data available for the given timestamp and region.")

    data = load(search.items() ,geopolygon=shape(polygon), groupby="solar_day", chunks={})
    data["red"] = data["red"] * getstuff(search,'red', 'scale') + getstuff(search,'red', 'offset')
    data["nir"] = data["nir"] * getstuff(search,'nir', 'scale') + getstuff(search,'nir', 'offset')
    return data


def calculate_ndvi_stats(data, polygon):
    # Calculate NDVI
    ndvi = (data.nir - data.red) / (data.nir + data.red)

    # Calculate statistical values
    mean_ndvi = ndvi.mean(dim=["x", "y"], skipna=True).compute()
    std_ndvi = ndvi.std(dim=["x", "y"], skipna=True).compute()
    
    # Check if mean_ndvi and std_ndvi are single values
    if mean_ndvi.size == 1 and std_ndvi.size == 1:
        mean_ndvi_value = mean_ndvi.item()
        std_ndvi_value = std_ndvi.item()
    else:
        raise ValueError("Unexpected result size for NDVI calculations.")
    
    return {
        "mean_ndvi": mean_ndvi_value,
        "std_ndvi": std_ndvi_value
    }
    
def getstuff(search,band,prop):
    return search.item_collection_as_dict()['features'][0]['assets'][band]['raster:bands'][0][prop]

def find_nearest_date(target_date: str, available_dates: list):
    target = datetime.strptime(target_date, "%Y-%m-%d")
    available_dates = sorted(datetime.strptime(date, "%Y-%m-%d") for date in available_dates)

    # Find the nearest date
    nearest_date = min(available_dates, key=lambda date: abs(date - target))
    return nearest_date.strftime("%Y-%m-%d")
