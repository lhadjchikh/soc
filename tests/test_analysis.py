import pytest
from unittest.mock import patch

from analysis import get_statistics, get_value_at_coordinates
from models import SummaryStatistics
from exceptions import OutOfBoundsError
from settings import TEST_DATA_DIR

FILEPATH = f"{TEST_DATA_DIR}/nebraska_30m_soc.tif"
# Bounds:
#   West: -97.940439
#   East: -97.852314
#   South: 41.930530
#   North: 41.989047


@patch("settings.DATASET_DIR", TEST_DATA_DIR)
class TestGetStatistics:
    """Tests for the get_statistics function."""

    def test_statistics_calculation(self):
        """Test that statistics are calculated correctly."""
        stats = get_statistics()

        assert isinstance(stats, SummaryStatistics)

        assert isinstance(stats.min_value, float)
        assert isinstance(stats.max_value, float)
        assert isinstance(stats.mean_value, float)

        assert stats.min_value <= stats.mean_value <= stats.max_value
        assert stats.min_value >= 0
        assert stats.max_value > stats.min_value

    def test_statistics_caching(self):
        """Test that statistics are cached after first calculation."""
        stats1 = get_statistics()
        stats2 = get_statistics()

        assert stats1 is stats2  # should return the same object
        assert stats1 == stats2

    def test_with_custom_path(self):
        """Test getting statistics with custom directory."""
        stats = get_statistics(TEST_DATA_DIR)
        assert isinstance(stats, SummaryStatistics)
        assert stats.min_value > 0
        assert stats.max_value > stats.min_value

    def test_summary_statistics(self):
        """Test for regression in the summary statistics calculations."""
        stats = get_statistics()

        assert isinstance(stats, SummaryStatistics)

        assert abs(stats.min_value - 38.999664) < 1e-6
        assert abs(stats.max_value - 88.948524) < 1e-6
        assert abs(stats.mean_value - 63.135494) < 1e-6


@patch("settings.DATASET_DIR", TEST_DATA_DIR)
class TestGetValueAtCoordinates:
    """Tests for the get_value_at_coordinates function."""

    def test_valid_coordinates(self):
        """Test getting SOC value at valid coordinates."""
        value = get_value_at_coordinates(-97.900000, 41.950000, FILEPATH)
        assert isinstance(value, float)
        assert value > 0

    def test_out_of_bounds_coordinates(self):
        """Test that out-of-bounds coordinates raise OutOfBoundsError."""
        with pytest.raises(OutOfBoundsError):
            get_value_at_coordinates(-122.4194, 37.7749, FILEPATH)

    def test_with_custom_path(self):
        """Test getting SOC value with custom GeoTIFF path."""
        value = get_value_at_coordinates(-97.900000, 41.940000, FILEPATH)
        assert isinstance(value, float)
        assert value > 0
