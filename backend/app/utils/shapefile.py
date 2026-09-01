import numpy as np
import rasterio
from rasterio.features import shapes
import geopandas as gpd

# сопоставление класс -> кг/га азота, вынеси в конфиг если нужно менять
NITROGEN_MAP = {0: 0, 1: 40, 2: 80, 3: 120, 4: 160}

def tif_to_shapefile(tif_path: str, shp_path: str, nodata_class: int | None = None) -> gpd.GeoDataFrame:

    with rasterio.open(tif_path) as src:
        band = src.read(1).astype(np.int32)
        transform = src.transform
        crs = src.crs

    mask = band != nodata_class if nodata_class is not None else None

    geoms = (
        {"properties": {"class": int(value)}, "geometry": geom}
        for geom, value in shapes(band, mask=mask, transform=transform)
    )

    gdf = gpd.GeoDataFrame.from_features(list(geoms), crs=crs)
    gdf["nitrogen"] = gdf["class"].map(NITROGEN_MAP)
    gdf.to_file(shp_path, driver="ESRI Shapefile", encoding="utf-8")
    
    return gdf
