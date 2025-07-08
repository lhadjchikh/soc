from fastapi import FastAPI

app = FastAPI()


@app.get("/soc-stock")
async def get_soc_stock():
    """Get SOC stock value at given coordinates."""
    pass


@app.get("/stats")
async def get_stats():
    """Get SOC summary statistics for the entire SOC Stock dataset."""
    pass
