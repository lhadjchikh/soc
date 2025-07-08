# SOC API

A REST API for querying Soil Organic Carbon (SOC) data from GeoTIFF raster files. Provides coordinate-based queries and statistical analysis endpoints.

## Getting Started

### Quick Start

1. **Install dependencies**:

   ```bash
   poetry install
   ```

2. **Place your GeoTIFF files in the `data/` directory**:

   ```bash
   cp your-raster.tif data/
   ```

   For example:

   ```bash
   cp tests/test_data/nebraska_30m_soc.tif data/
   ```

3. **Start the server**:

   ```bash
   poetry run uvicorn app:app
   ```

   The API will be available at `http://localhost:8000`

4. **Query the endpoints**:

   ```bash
   curl "http://localhost:8000/soc-stock?lat=41.94&lon=-97.90"

   curl "http://localhost:8000/stats"
   ```

### Running Tests

```bash
poetry run pytest
```

## Approach

This project implements a REST API for querying geospatial raster data using Test-Driven Development (TDD) and functional programming principles.

Key technical decisions:

- **FastAPI** for high-performance REST API with automatic OpenAPI documentation
- **Rasterio** for efficient GeoTIFF processing with coordinate reprojection
- **Windowed reading** for memory-efficient processing of large raster files
- **Functional approach** with pure functions and LRU caching for performance

## Future Improvements

- **Cloud storage**: Store raster data in S3 for scalable, distributed access
- **STAC integration**: Create a SpatioTemporal Asset Catalog (STAC) and use STAC API to identify relevant raster tiles
- **Virtual datasets**: Add support for GDAL Virtual Raster Tables (VRTs) to efficiently handle large, multi-file datasets
