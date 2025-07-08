from dataclasses import dataclass


@dataclass
class SummaryStatistics:
    """Statistics for raster data."""

    min_value: float
    max_value: float
    mean_value: float
