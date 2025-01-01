import folium
import base64
import io
from PIL import Image

def plot_route(route):
    map_ = folium.Map(zoom_start=6)
    plot_route_on_map(route, map_)
    return map_

def plot_route_on_map(route, m):
    folium.PolyLine(
        route['routes'][0]['geometry']['coordinates'], color="blue"
    ).add_to(m)
    return m

def plot_point_on_map(point, m, label, color):
    folium.Marker(
        [point[0], point[1]], 
        popup=label,
        icon=folium.Icon(color=color, icon='truck')
    ).add_to(m)
    return m

def save_map_to_image(m, filename):
    # Ensure the filename ends with .png
    if not filename.lower().endswith('.png'):
        filename += '.png'
    img_data = m._to_png(2)
    img = Image.open(io.BytesIO(base64.b64decode(img_data)))
    img.save(filename)
    return img