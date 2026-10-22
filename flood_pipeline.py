import numpy as np
import rasterio

def calculate_elev_slope_ratio(elevation, slope):
    """
    Calculates the elevation-to-slope ratio for flood susceptibility.
    QA/QC: Handles zero-slope edge cases to prevent division-by-zero errors.
    """
    safe_slope = np.where(slope <= 0.0, 0.001, slope)
    ratio = elevation / safe_slope
    ratio = np.nan_to_num(ratio, nan=0.0)
    return ratio

def validate_geotiff_crs(dataset_path, expected_crs="EPSG:4326"):
    """
    QA/QC: Validates that the AI-generated GeoTIFF has the correct CRS.
    AI agents often forget to set the CRS, leading to physically invalid outputs.
    """
    with rasterio.open(dataset_path) as src:
        if src.crs is None:
            raise ValueError("CRS is missing! The AI failed to project the data.")
        if src.crs.to_string() != expected_crs:
            raise ValueError(f"Incorrect CRS! Expected {expected_crs}, got {src.crs.to_string()}")
        return True