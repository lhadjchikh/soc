from fastapi import FastAPI, Query, HTTPException
from typing import Annotated
import numpy as np

from analysis import get_statistics, get_value_at_coordinates
from exceptions import OutOfBoundsError
from schemas import SocStockResponse, StatsResponse
from settings import NODATA

app = FastAPI(
    title="SOC API",
    description="API for querying Soil Organic Carbon raster data.",
    version="1.0.0",
)


@app.get("/soc-stock", response_model=SocStockResponse)
async def get_soc_stock(
    lat: Annotated[
        float, Query(ge=-90, le=90, description="Latitude coordinate (WGS84)")
    ],
    lon: Annotated[
        float, Query(ge=-180, le=180, description="Longitude coordinate (WGS84)")
    ],
):
    """Get SOC stock value at given WGS84 coordinates."""
    try:
        soc_value = get_value_at_coordinates(lon, lat, "data/nebraska_30m_soc.tif")

        if soc_value in NODATA or np.isnan(soc_value):
            raise HTTPException(
                status_code=400, detail="No data available at this location"
            )

        return SocStockResponse(soc_stock=soc_value)
    except OutOfBoundsError:
        raise HTTPException(
            status_code=400, detail="Coordinates are outside the data coverage area"
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get SOC summary statistics for the entire SOC Stock dataset."""
    try:
        stats = get_statistics()
        return StatsResponse(
            min_soc=stats.min_value,
            max_soc=stats.max_value,
            mean_soc=stats.mean_value,
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
