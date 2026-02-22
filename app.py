from flask import Flask, render_template_string
import folium
import geopandas as gpd

app = Flask(__name__)

KML_FILE = "6.kml"

@app.route("/")
def home():

    # Create map
    m = folium.Map(
        location=[33.8938, 35.5018],
        zoom_start=8,
        tiles=None
    )

    # Satellite basemap (Esri)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/"
              "World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery",
        name="Satellite",
    ).add_to(m)

    # Load KML
    gdf = gpd.read_file(KML_FILE)

    if gdf.crs and gdf.crs.to_string() != "EPSG:4326":
        gdf = gdf.to_crs(epsg=4326)

    folium.GeoJson(gdf, name="KML Layer").add_to(m)

    folium.LayerControl().add_to(m)

    return m._repr_html_()

if __name__ == "__main__":
    app.run(debug=True)
