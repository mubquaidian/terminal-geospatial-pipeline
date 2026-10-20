import numpy as np

def calculate_elev_slope_ratio(elevation, slope):
    """
    Calculates the elevation-to-slope ratio for flood susceptibility.
    QA/QC: Handles zero-slope edge cases to prevent division-by-zero errors.
    """
    # Define a safe minimum slope to prevent divide-by-zero (QA/QC best practice)
    safe_slope = np.where(slope <= 0.0, 0.001, slope)
    
    # Calculate ratio
    ratio = elevation / safe_slope
    
    # Handle NaNs explicitly
    ratio = np.nan_to_num(ratio, nan=0.0)
    
    return ratio