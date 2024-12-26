import contextily as ctx
import gc
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from shapely.geometry import Point

def get_KL_boundary() -> gpd.GeoDataFrame:
    """Retrieve Kuala Lumpur boundary using precise geographic coordinates."""
    from shapely.geometry import Polygon

    kl_coords = [
        (101.6, 3.0),   # Southwest
        (101.8, 3.0),   # Southeast
        (101.8, 3.3),   # Northeast
        (101.6, 3.3)    # Northwest
    ]

    kl_polygon = Polygon(kl_coords)

    return gpd.GeoDataFrame(
        {'name': ['Kuala Lumpur'], 'geometry': [kl_polygon]}, 
        crs="EPSG:4326"
    )


def generate_random_points_within_boundary(
    malaysia_boundary: gpd.GeoDataFrame,
    num_points: int = 100,
) -> pd.DataFrame:
    """Generate random points within Malaysia's boundary."""
    print("Generating random points within boundary")
    min_lon, min_lat, max_lon, max_lat = malaysia_boundary.total_bounds
    lons = np.random.uniform(min_lon, max_lon, num_points)
    lats = np.random.uniform(min_lat, max_lat, num_points)
    random_points = pd.DataFrame({'lon': lons, 'lat': lats})
    random_points = random_points[
        random_points.apply(
            lambda row: Point(row['lon'], row['lat'])
                .within(malaysia_boundary.geometry.iloc[0]),
            axis=1,
        )
    ]

    print(f"Generated {len(random_points)} points within boundary")
    return random_points


def main():
    malaysia_boundary = get_KL_boundary()
    random_points_within_boundary = generate_random_points_within_boundary(
        malaysia_boundary,
        num_points=100,
    )
    random_points_within_boundary.to_csv(
        'malaysia_random_points.csv',
        index=False,
    )

    ax = random_points_within_boundary.plot(
        kind="scatter",
        x="lon", y="lat",
        alpha=0.7, s=5, color="red", figsize=(10, 10),
    )
    ctx.add_basemap(ax, crs=malaysia_boundary.crs)
    ax.set_title("Random Points in Malaysia")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    plt.tight_layout()
    plt.savefig(
        'malaysia_random_points_map_actual.png',
        bbox_inches='tight',
    )

    plt.close()
    gc.collect()


if __name__ == '__main__':
    main()
