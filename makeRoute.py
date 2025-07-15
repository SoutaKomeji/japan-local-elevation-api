import requests
import folium

loc_pick = [140.726230, 41.773214]  # 函館駅
loc_del = [140.709204, 41.765184]  # 旧函館区公会堂
query_url = "http://172.28.148.142:5000/route/v1/driving/{},{};{},{}?steps=true".format(loc_pick[0], loc_pick[1], loc_del[0], loc_del[1])
response = requests.get(query_url)
result = response.json()

route = result["routes"][0]
legs = route["legs"][0]["steps"]
list_locations = []

for point in legs:
    for it in point["intersections"]:
        list_locations.append(it["location"][::-1])

# 中間地点を計算
loc_mid = [
    (loc_pick[0] + loc_del[0]) / 2,
    (loc_pick[1] + loc_del[1]) / 2
]

folium_map = folium.Map(location=loc_mid[::-1], zoom_start=14)
folium.Marker(location=loc_pick[::-1], icon=folium.Icon(color='red')).add_to(folium_map)
folium.Marker(location=loc_del[::-1]).add_to(folium_map)
line = folium.vector_layers.PolyLine(locations=list_locations, color='black', weight=10)
line.add_to(folium_map)

# 各交差点にピン（番号付き）
for idx, loc in enumerate(list_locations):
    folium.Marker(
        location=loc,
        icon=folium.Icon(color='blue', icon='info-sign'),
        tooltip=f'交差点 {idx}'
    ).add_to(folium_map)

    # 番号ラベル（必要ならコメントアウトも可）
    folium.map.Marker(
        location=loc,
        icon=folium.DivIcon(html=f'<div style="font-size: 10pt; color: black;">{idx}</div>')
    ).add_to(folium_map)


folium_map.save("map.html")