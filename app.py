from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI()


@app.get("/soc-stock")
async def get_soc_stock(
    lat: Annotated[float, Query(ge=-90, le=90, description="Latitude coordinate")],
    lon: Annotated[float, Query(ge=-180, le=180, description="Longitude coordinate")],
):
    """Get SOC stock value at given coordinates."""
    pass


@app.get("/stats")
async def get_stats():
    """Get SOC summary statistics for the entire SOC Stock dataset."""
    pass
