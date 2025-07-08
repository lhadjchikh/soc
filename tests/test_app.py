from fastapi.testclient import TestClient
from unittest.mock import patch
from app import app
from settings import TEST_DATA_DIR

# Test file: nebraska_30m_soc.tif
# Bounds:
#   West: -97.940439
#   East: -97.852314
#   South: 41.930530
#   North: 41.989047

client = TestClient(app)


@patch("settings.DATASET_DIR", TEST_DATA_DIR)
class TestSocStock:
    """Tests for the /soc-stock endpoint."""

    def test_soc_stock(self):
        """Test that the endpoint returns SOC stock value for the given coordinates."""
        response = client.get("/soc-stock?lat=41.940000&lon=-97.900000")

        assert response.status_code == 200
        data = response.json()
        assert "soc_stock" in data
        assert isinstance(data["soc_stock"], (int, float))
        assert data["soc_stock"] > 0

    def test_soc_outside_bounds(self):
        """Test that valid coordinates outside GeoTIFF coverage return 400."""
        response = client.get("/soc-stock?lat=37.7749&lon=-122.4194")
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Coordinates are outside the data coverage area"

    def test_soc_invalid_latitude_high(self):
        """Test that latitude > 90 returns 422."""
        response = client.get("/soc-stock?lat=91.0&lon=-97.896377")
        assert response.status_code == 422

    def test_soc_invalid_latitude_low(self):
        """Test that latitude < -90 returns 422."""
        response = client.get("/soc-stock?lat=-91.0&lon=-97.896377")
        assert response.status_code == 422

    def test_soc_invalid_longitude_high(self):
        """Test that longitude > 180 returns 422."""
        response = client.get("/soc-stock?lat=41.959795&lon=181.0")
        assert response.status_code == 422

    def test_soc_invalid_longitude_low(self):
        """Test that longitude < -180 returns 422."""
        response = client.get("/soc-stock?lat=41.959795&lon=-181.0")
        assert response.status_code == 422

    def test_soc_stock_missing_both_parameters(self):
        """Test that missing both latitude and longitude returns 422."""
        response = client.get("/soc-stock")
        assert response.status_code == 422

    def test_soc_stock_missing_latitude(self):
        """Test that missing latitude returns 422."""
        response = client.get("/soc-stock?lon=-97.896377")
        assert response.status_code == 422

    def test_soc_stock_missing_longitude(self):
        """Test that missing longitude returns 422."""
        response = client.get("/soc-stock?lat=41.959795")
        assert response.status_code == 422

    def test_soc_stock_non_numeric_latitude(self):
        """Test that non-numeric latitude returns 422."""
        response = client.get("/soc-stock?lat=abc&lon=-97.896377")
        assert response.status_code == 422

    def test_soc_stock_non_numeric_longitude(self):
        """Test that non-numeric longitude returns 422."""
        response = client.get("/soc-stock?lat=41.959795&lon=xyz")
        assert response.status_code == 422

    def test_soc_stock_non_numeric_both(self):
        """Test that non-numeric lat and lon returns 422."""
        response = client.get("/soc-stock?lat=abc&lon=xyz")
        assert response.status_code == 422


@patch("settings.DATASET_DIR", TEST_DATA_DIR)
class TestStats:
    """Tests for the /stats endpoint."""

    def test_stats_status_code(self):
        """Test that the /stats endpoint returns a 200 status code."""
        response = client.get("/stats")
        assert response.status_code == 200

    def test_stats_response_fields(self):
        """Test that the /stats endpoint returns the required fields."""
        response = client.get("/stats")
        data = response.json()
        assert "min_soc" in data
        assert "max_soc" in data
        assert "mean_soc" in data

    def test_stats_min_soc_positive(self):
        """Test that min_soc is greater than 0."""
        response = client.get("/stats")
        data = response.json()
        assert data["min_soc"] > 0

    def test_stats_max_soc_greater_than_min_soc(self):
        """Test that max_soc is greater than min_soc."""
        response = client.get("/stats")
        data = response.json()
        assert data["max_soc"] > data["min_soc"]

    def test_stats_mean_soc_within_bounds(self):
        """Test that mean_soc is between min_soc and max_soc."""
        response = client.get("/stats")
        data = response.json()
        assert data["min_soc"] <= data["mean_soc"] <= data["max_soc"]
