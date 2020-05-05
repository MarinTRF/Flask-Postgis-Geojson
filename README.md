## This app shows a GeoJSON obtained through a PostgreSQL database of the census tracts of the Madrid community.

- ### /geojsondb ===> The first service shows the GeoJSON filtering with a cusec code.

An example:  
**http://localhost:8000/geojsondb**

- ### /cusec2geojson ===> The second service shows the GeoJSON filtering with a cusec code.

An example:  
http://localhost:8000/geojson2cusec?cusec=2807901072

- ### /wkt2geojson ===> The third service shows the GeoJSON filtering with an object in Well Known Text (WKT).

Some examples:  
http://localhost:8000/wkt2geojson?wkt=POLYGON ((-3.7003111839294434 40.4150807746539, -3.690698146820068 40.4150807746539, -3.690698146820068 40.41976938144622, -3.7003111839294434 40.41976938144622, -3.7003111839294434 40.4150807746539))  
http://localhost:8000/wkt2geojson?wkt=LINESTRING (-3.6950325965881348 40.416093672081765, -3.693830966949463 40.41666546228339, -3.694710731506347 40.4186258489413, -3.6975431442260738 40.418446149209046, -3.7003540992736816 40.41940998761056, -3.70164155960083 40.41650209415018)  
http://localhost:8000/wkt2geojson?wkt=MULTIPOLYGON (((-3.70737075805664 40.41774368201396,-3.693981170654297 40.41774368201396, -3.693981170654297 40.42630348002172,-3.70737075805664 40.42630348002172,-3.70737075805664 40.41774368201396)))  

- ### /geojson2wktcusec ===> The fourth service shows the GeoJSON filtering with a cusec code and/or WKT

An example with a cusec code:  
http://localhost:8000/geojson2cusec?cusec=2807901072

An example with a WKT:  
http://localhost:8000/wkt2geojson?wkt=MULTIPOLYGON (((-3.70737075805664 40.41774368201396,-3.693981170654297 40.41774368201396, -3.693981170654297 40.42630348002172,-3.70737075805664 40.42630348002172,-3.70737075805664 40.41774368201396)))

An example with cusec and WKT:  
http://localhost:8000/geojson2cusec?wkt=MULTIPOLYGON (((-3.70737075805664 40.41774368201396,-3.693981170654297 40.41774368201396, -3.693981170654297 40.42630348002172,-3.70737075805664 40.42630348002172,-3.70737075805664 40.41774368201396)))&cusec=2807901072
