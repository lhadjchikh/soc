"""Analysis module for raster data operations."""

import rasterio
import numpy as np
from pathlib import Path
from functools import lru_cache
from rasterio.warp import transform

from exceptions import OutOfBoundsError
from models import SummaryStatistics
from settings import DATASET_DIR


@lru_cache(maxsize=1)
def get_statistics(directory: str = DATASET_DIR, band: int = 1) -> SummaryStatistics:
    """
    Calculate statistics for all GeoTIFF files in the dataset directory.

    Args:
        dataset_dir: Directory containing GeoTIFF files (default: DATASET_DIR from settings)
        band: Band number to read from (default: 1)

    Returns:
        SummaryStatistics with min, max, and mean values across all files
    """
    tiff_files = list(Path(directory).rglob("*.tif")) + list(
        Path(directory).rglob("*.tiff")
    )

    if not tiff_files:
        raise ValueError(f"No GeoTIFF files found in directory: {directory}")

    all_valid_data = []

    for filepath in tiff_files:
        with rasterio.open(filepath) as src:
            data = src.read(band)
            valid_data = data[~np.isnan(data)]  # remove NaN and nodata values
            if len(valid_data) > 0:
                all_valid_data.extend(valid_data.flatten())

    if len(all_valid_data) == 0:
        raise ValueError("No valid data found in any GeoTIFF files")

    all_valid_data = np.array(all_valid_data)

    return SummaryStatistics(
        min_value=float(np.min(all_valid_data)),
        max_value=float(np.max(all_valid_data)),
        mean_value=float(np.mean(all_valid_data)),
    )


def get_value_at_coordinates(
    lon: float,
    lat: float,
    filepath: str,
    band: int = 1,
    crs: str = "EPSG:4326",
) -> float:
    """
    Extract raster value at given coordinates.

    Args:
        lon: Longitude coordinate
        lat: Latitude coordinate
        filepath: Path to the GeoTIFF file
        band: Band number to read from (default: 1)
        crs: Coordinate reference system (default: EPSG:4326)

    Returns:
        Raster value at the given coordinates

    Raises:
        OutOfBoundsError: If coordinates are outside the GeoTIFF bounds
    """
    with rasterio.open(filepath) as src:
        x, y = transform(crs, src.crs, [lon], [lat])

        row, col = src.index(x[0], y[0])

        if not (0 <= row < src.height and 0 <= col < src.width):
            raise OutOfBoundsError("Coordinates are outside the GeoTIFF bounds")

        return float(src.read(band)[row, col])
