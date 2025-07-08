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
def get_statistics(
    directory: str = DATASET_DIR, band: int = 1, window_size: int = 1024
) -> SummaryStatistics:
    """
    Calculate statistics for all GeoTIFF files in the dataset directory using windowed reading.

    Args:
        dataset_dir: Directory containing GeoTIFF files (default: DATASET_DIR from settings)
        band: Band number to read from (default: 1)
        window_size: Size of windows for reading large rasters (default: 1024)

    Returns:
        SummaryStatistics with min, max, and mean values across all files
    """
    tiff_files = list(Path(directory).rglob("*.tif")) + list(
        Path(directory).rglob("*.tiff")
    )
    if not tiff_files:
        raise ValueError(f"No GeoTIFF files found in directory: {directory}")

    min_val, max_val, sum_val, count = None, None, 0.0, 0

    for filepath in tiff_files:
        with rasterio.open(filepath) as src:
            # Process the raster in windows for memory efficiency
            for window in src.block_windows(band):
                # Read only this window
                data = src.read(band, window=window[1], masked=True)

                if data.mask.all():
                    continue  # all values in this window are masked

                valid = data.compressed()  # removes masked elements
                if valid.size == 0:
                    continue

                # Update statistics incrementally
                window_min = np.min(valid)
                window_max = np.max(valid)
                window_sum = np.sum(valid)
                window_count = valid.size

                min_val = window_min if min_val is None else min(min_val, window_min)
                max_val = window_max if max_val is None else max(max_val, window_max)
                sum_val += window_sum
                count += window_count

    if count == 0:
        raise ValueError("No valid data found in any GeoTIFF files")

    return SummaryStatistics(
        min_value=float(min_val),
        max_value=float(max_val),
        mean_value=float(sum_val / count),
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
        ValueError: If the pixel is masked (nodata)
    """
    with rasterio.open(filepath) as src:
        x, y = transform(crs, src.crs, [lon], [lat])
        row, col = src.index(x[0], y[0])

        if not (0 <= row < src.height and 0 <= col < src.width):
            raise OutOfBoundsError(
                f"Coordinates ({lon}, {lat}) are outside the bounds of raster '{filepath}'"
            )

        window = ((row, row + 1), (col, col + 1))
        value = src.read(band, window=window, masked=True)[0, 0]

        if np.ma.is_masked(value):
            raise ValueError("The value at the given coordinates is masked (nodata).")

        return float(value)
