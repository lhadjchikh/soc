import pytest

from analysis import get_value_at_coordinates
from exceptions import OutOfBoundsError

FILEPATH = "tests/nebraska_30m_soc.tif"
# Bounds:
#   West: -97.940439
#   East: -97.852314
#   South: 41.930530
#   North: 41.989047


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
