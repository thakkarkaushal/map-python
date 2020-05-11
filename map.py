import folium
import pandas

data = pandas.read_csv("Volcanoes.csv")
LAT = list(data["LAT"])
LOT = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])
location1 = folium.Map(location=[38, -99], tiles="Stamen Terrain")
fgv = folium.FeatureGroup(name="Volcanoes")

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""


for la, lt, el, name in zip(LAT, LOT, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    if 0 < el < 1000:
        fgv.add_child(folium.Marker(location=[la, lt], popup=folium.Popup(iframe), icon=folium.Icon(color='green')))
    elif 1000 < el < 2000:
        fgv.add_child(folium.Marker(location=[la, lt], popup=folium.Popup(iframe), icon=folium.Icon(color='orange')))
    elif el > 2000:
        fgv.add_child(folium.Marker(location=[la, lt], popup=folium.Popup(iframe), icon=folium.Icon(color='red')))

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open("world.json", "r", encoding='utf-8-sig').read(),
                             style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 1000000
                             else 'orange' if 1000000 <= x['properties']['POP2005'] < 2000000 else 'red'}))

location1.add_child(fgv)
location1.add_child(fgp)
location1.add_child(folium.LayerControl())

location1.save("Map1.html")
