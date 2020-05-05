from flask import Flask
from flask import render_template, redirect, url_for
from flask import request
import psycopg2
import geojson


app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('error404.html'), 404

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/geojsondb', methods=['GET'])
def return_geojson():
	try:

		conn = psycopg2.connect(host="postgresql-enjoymaps.alwaysdata.net",
								database="enjoymaps_ejercicios",
								user="enjoymaps",
								password="enjoymaps963")
		cur = conn.cursor()
		cur.execute( """SELECT jsonb_build_object(
								'type',     'FeatureCollection',
								'features', jsonb_agg(feature)   
								)
								FROM (
										SELECT jsonb_build_object(
										'type',       'Feature',
										'id',         id,
										'geometry',   ST_AsGeoJSON(geom)::jsonb,
										'properties', to_jsonb(row) - 'geom'
								) AS feature
								 FROM (SELECT p.id,p.cusec,p.geom FROM secciones_censales AS p)row)feature;""")
		rows = cur.fetchall()
		cur.close()
		conn.close()
		geojs = geojson.dumps(rows,indent=2)
		return geojs[5:-3]
		

	except:
		return render_template(alldb.html)
	
@app.route('/geojson2cusec', methods=['GET','POST'])
def return_geojson_by_cusec():
	req = request.args.get('cusec')
	cusec = ""
	if len(req) == 10:
		cusec = cusec + req

		conn = psycopg2.connect(host="postgresql-enjoymaps.alwaysdata.net",
								database="enjoymaps_ejercicios",
								user="enjoymaps",
								password="enjoymaps963")
		cur = conn.cursor()
		cur.execute( """SELECT jsonb_build_object(
								'type',     'FeatureCollection',
								'features', jsonb_agg(feature)   
								)
								FROM (
										SELECT jsonb_build_object(
										'type',       'Feature',
										'id',         id,
										'geometry',   ST_AsGeoJSON(geom)::jsonb,
										'properties', to_jsonb(row) - 'geom'
								) AS feature
								 FROM (SELECT id,cusec,geom FROM secciones_censales WHERE cusec = '{}')row)feature;""".format(cusec))
		rows = cur.fetchall()
		cur.close()
		conn.close()
		geojs = geojson.dumps(rows,indent=2)
		return geojs[5:-3]
	else:
		return render_template('cusec.html')


@app.route('/wkt2geojson', methods=['GET','POST'])
def wkt_to_geojson():
	req = request.args.get('wkt')
	wkt = ""
	if wkt is None:
		wkt = wkt + req
		sql = """SELECT jsonb_build_object(
					            'type',     'FeatureCollection',
					            'features', jsonb_agg(feature)   
					        )
					        FROM (
					            SELECT jsonb_build_object(
					                'type',       'Feature',
					                'id',         id,
					                'geometry',   ST_AsGeoJSON(geom)::jsonb,
					                'properties', to_jsonb(row) - 'geom'
					            ) AS feature
					            FROM (        
					            
					                SELECT p.id, p.cusec, p.geom AS geom 
					                 FROM secciones_censales AS p
									WHERE ST_Intersects(p.geom, 'SRID=4326;{}')

					            )row
					        ) features;""".format(wkt)
		conn = psycopg2.connect(host="postgresql-enjoymaps.alwaysdata.net",
						database="enjoymaps_ejercicios",
						user="enjoymaps",
						password="enjoymaps963")
		cur = conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		cur.close()
		conn.close()
		geojs = geojson.dumps(rows,indent=2)
		return geojs[5:-3]
	else:
		return render_template('wkt.html')

	
@app.route('/geojson2wktcusec', methods=['GET','POST'])
def geojson2wktcusec():
	try:
		
		wkt = request.args.get('wkt')
		cusec = request.args.get('cusec')
		where = ""
		if wkt is not False and cusec is None:
			where = where + ("ST_Intersects(p.geom, 'SRID=4326;"+wkt+"')")
		elif cusec is not  False and wkt is None:
			where = where + ("cusec = '"+ cusec + "'")
		elif wkt and cusec is not False:
			where = where + ("ST_Intersects(p.geom, 'SRID=4326;" + wkt + "')" + " AND cusec = '"+ cusec + "'" )
		sql = """SELECT jsonb_build_object(
					            'type',     'FeatureCollection',
					            'features', jsonb_agg(feature)   
					        )
					        FROM (
					            SELECT jsonb_build_object(
					                'type',       'Feature',
					                'id',         id,
					                'geometry',   ST_AsGeoJSON(geom)::jsonb,
					                'properties', to_jsonb(row) - 'geom'
					            ) AS feature
					            FROM (        
					            
					                SELECT p.id, p.cusec, p.geom AS geom 
					                 FROM secciones_censales AS p
									WHERE {}

					            )row
					        ) features;""".format(where)
		conn = psycopg2.connect(host="postgresql-enjoymaps.alwaysdata.net",
						database="enjoymaps_ejercicios",
						user="enjoymaps",
						password="enjoymaps963")
		cur = conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		cur.close()
		conn.close()
		geojs = geojson.dumps(rows,indent=2)
		return geojs[5:-3]
		

		

	except:
		return render_template('wkt&orcusec')

if __name__ == "__main__":
	app.run(debug=True,port=8000)
	