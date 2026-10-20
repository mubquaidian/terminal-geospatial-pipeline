import numpy as np
import sys
import os

# Add parent directory to path to import flood_pipeline
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flood_pipeline import calculate_elev_slope_ratio

def test_ratio_standard_calculation():
    """Tests standard mathematical correctness."""
    elevation = np.array([100.0, 500.0])
    slope = np.array([10.0, 25.0])
    result = calculate_elev_slope_ratio(elevation, slope)
    
    assert result[0] == 10.0
    assert result[1] == 20.0

def test_ratio_zero_slope_edge_case():
    """QA/QC Test: Ensures zero slope does not cause infinity or crash."""
    elevation = np.array([100.0])
    slope = np.array([0.0]) # This would normally cause a ZeroDivisionError
    
    result = calculate_elev_slope_ratio(elevation, slope)
    
    # Assert it handled the zero slope safely using our 0.001 threshold
    assert result[0] == 100000.0
    assert not np.isinf(result).any()

def test_ratio_nan_handling():
    """QA/QC Test: Ensures NaNs are handled deterministically."""
    elevation = np.array([np.nan, 200.0])
    slope = np.array([10.0, 10.0])
    result = calculate_elev_slope_ratio(elevation, slope)
    
    assert result[0] == 0.0 # NaN replaced by 0.0
    assert result[1] == 20.0