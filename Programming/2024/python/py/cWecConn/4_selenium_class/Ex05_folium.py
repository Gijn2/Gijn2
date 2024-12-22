import folium

# 1. 지도 위도 경도 설정 및 파일 저장
map_osm = folium.Map(location=[38.572807, 126.975918])
map_osm.save('./map/map1.html')

# 2. 지도 줌 설정
map_osm = folium.Map(location=[38.572807, 126.975918],zoom_start=17,zoom_control=True)
map_osm.save('./map/map2.html')

# 3. 지도모양 설정
map_osm = folium.Map(location=[37.900007, 126.975918]
                     ,zoom_start=17
                     ,tiles='Stamen Terrain') # types : 'Stamen Toner','Mapbox Bright', 'Mapbox Control room tiles'
map_osm.save('./map/map3.html')

# 4. Marker
map_osm = folium.Map(location=[37.900007, 126.975918]
                     ,zoom_start=17
                     ,zoom_control=True)
folium.Marker(location=[37.572807, 126.975918], popup='test').add_to(map_osm)
#folium.Marker(location=[37.800007, 126.975918], popup='test2').add_to(map_osm)
folium.RegularPolygonMarker(location=[37.9009997, 126.975918]
                            , popup='test2'
                            ,icon = folium.Icon(color='red',icon='info-sign')
                            ).add_to(map_osm)
folium.CircleMarker(location=[37.9999907, 126.975918]
              , popup='test3'
              , radius=11
              ,fill_color='orange').add_to(map_osm)
map_osm.save('./map/map4.html')