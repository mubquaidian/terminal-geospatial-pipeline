import numpy as np
import pytest
import rasterio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flood_pipeline import calculate_elev_slope_ratio, validate_geotiff_crs

# SCENARIO 1: Anti-Cheat (Parametrization)
# AI agents often hardcode outputs. We feed multiple inputs to prove it calculates.

@pytest.mark.parametrize("elevation, slope, expected", [
    (np.array([100.0]), np.array([10.0]), 10.0),
    (np.array([500.0]), np.array([25.0]), 20.0),
    (np.array([50.0]), np.array([5.0]), 10.0)
])
def test_anti_cheat_parametrization(elevation, slope, expected):
    result = calculate_elev_slope_ratio(elevation, slope)
    assert result[0] == pytest.approx(expected, rel=1e-5)

# SCENARIO 2: Geospatial Metadata (CRS Trap)
# AI often forgets to set the CRS. We test that our validator catches bad data.

def test_geotiff_crs_validation(tmp_path):
    file_path = tmp_path / "mock_output.tif"
    
    # 1. Create a mock GeoTIFF with a CORRECT CRS
    profile = {
        'driver': 'GTiff', 'dtype': 'float32', 'nodata': -9999.0,
        'width': 10, 'height': 10, 'count': 1, 'crs': 'EPSG:4326',
        'transform': rasterio.transform.from_origin(100, 100, 1, 1)
    }
    with rasterio.open(file_path, 'w', **profile) as dst:
        dst.write(np.ones((10, 10), dtype='float32'), 1)

    # Assert it passes with correct CRS
    assert validate_geotiff_crs(str(file_path), expected_crs="EPSG:4326") is True

    # 2. Assert it throws an error if the AI used the WRONG CRS (e.g., EPSG:3857)
    with pytest.raises(ValueError, match="Incorrect CRS!"):
        validate_geotiff_crs(str(file_path), expected_crs="EPSG:3857")

# SCENARIO 3: Numerical Integrity (Edge Cases)
# We test Zero-Division and NaN handling to ensure the AI's math doesn't crash.

def test_numerical_integrity_zero_slope():
    elevation = np.array([100.0])
    slope = np.array([0.0]) # The Zero-Division Trap
    result = calculate_elev_slope_ratio(elevation, slope)
    
    # Ensure it handled the zero safely
    assert not np.isinf(result).any()
    assert result[0] == 100000.0

def test_numerical_integrity_nan_handling():
    elevation = np.array([np.nan, 200.0])
    slope = np.array([10.0, 10.0])
    result = calculate_elev_slope_ratio(elevation, slope)
    
    # Ensure NaN was replaced with 0.0 deterministically
    assert result[0] == 0.0 
    assert result[1] == 20.0