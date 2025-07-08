from pydantic import BaseModel


class SocStockResponse(BaseModel):
    """Response model for SOC stock endpoint."""

    soc_stock: float


class StatsResponse(BaseModel):
    """Response model for stats endpoint."""

    min_soc: float
    max_soc: float
    mean_soc: float
