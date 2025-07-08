"""Analysis module for raster data operations."""

import rasterio
from rasterio.warp import transform

from exceptions import OutOfBoundsError


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
