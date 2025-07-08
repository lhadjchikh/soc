from fastapi import FastAPI, Query, HTTPException
from typing import Annotated
import numpy as np

from analysis import get_value_at_coordinates
from exceptions import OutOfBoundsError
from settings import NODATA

app = FastAPI()


@app.get("/soc-stock")
async def get_soc_stock(
    lat: Annotated[float, Query(ge=-90, le=90, description="Latitude coordinate")],
    lon: Annotated[float, Query(ge=-180, le=180, description="Longitude coordinate")],
):
    """Get SOC stock value at given coordinates."""
    try:
        soc_value = get_value_at_coordinates(lon, lat, "tests/nebraska_30m_soc.tif")

        if soc_value in NODATA or np.isnan(soc_value):
            raise HTTPException(
                status_code=400, detail="No data available at this location"
            )

        return {"soc_stock": soc_value}
    except OutOfBoundsError:
        raise HTTPException(
            status_code=400, detail="Coordinates are outside the data coverage area"
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/stats")
async def get_stats():
    """Get SOC summary statistics for the entire SOC Stock dataset."""
    pass
