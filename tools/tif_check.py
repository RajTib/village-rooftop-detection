import rasterio

paths = [
    r"D:\Teams\Ardra\TechfestIITB\GeoAI\workspace\dataset\processed\images\Badetumnar",
    r"D:\Teams\Ardra\TechfestIITB\GeoAI\workspace\dataset\processed\images\mungdanda",
]

for p in paths:
    with rasterio.open(p) as ds:
        print("\n", p)
        print("CRS:", ds.crs)
        print("Transform:", ds.transform)
        print("Bounds:", ds.bounds)
