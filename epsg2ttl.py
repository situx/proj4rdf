import os
import re
import pyproj
from pyproj import CRS


units={}
units["m"]="om:meter"
units["ft"]="om:foot"
units["us-ft"]="om:usfoot"
spheroids={}
spheroids["GRS80"]="geo:GRS80"
spheroids["GRS67"]="geo:GRS67"
spheroids["intl"]="geo:International1924"
spheroids["clrk"]="geo:Clarke1866"
spheroids["clrk66"]="geo:Clarke1866"
spheroids["clrk80"]="geo:Clarke1880RGS"
spheroids["WGS66"]="geo:WGS66"
spheroids["WGS72"]="geo:WGS72"
spheroids["WGS84"]="geo:WGS84"
spheroids["krass"]="geo:Krassovsky1940"
spheroids["bessel"]="geo:Bessel1841"
projections={}
projections["latlong"]="geo:LatLonProjection"
projections["longlat"]="geo:LonLatProjection"
projections["tmerc"]="geo:TransverseMercator"
projections["omerc"]="geo:LambertConformalConic"
projections["merc"]="geo:Mercator"
projections["sterea"]="geo:ObliqueStereographic"
projections["cea"]="geo:CylindricalEqualArea"
projections["stere"]="geo:Stereographic"
projections["eqc"]="geo:EquidistantCylindrical"
projections["laea"]="geo:LambertAzimuthalEqualArea"
projections["utm"]="geo:UTM"
projections["krovak"]="geo:Krovak"
projections["lcc"]="geo:LambertConformalConic"
projections["geocent"]="geo:Geocentric"
ttl=set()
ttlhead="@prefix rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"
ttlhead+="@prefix rdfs:<http://www.w3.org/2000/01/rdf-schema#> .\n"
ttlhead+="@prefix owl:<http://www.w3.org/2002/07/owl#> .\n"
ttlhead+="@prefix xsd:<http://www.w3.org/2001/XMLSchema#> .\n"
ttlhead+="@prefix geoepsg:<http://www.opengis.net/def/crs/EPSG/0/> .\n"
ttlhead+="@prefix geo:<http://www.opengis.net/ont/geosparql#> .\n"
ttlhead+="@prefix dc:<http://purl.org/dc/elements/1.1/> .\n"
ttlhead+="@prefix wd:<http://www.wikidata.org/entity/> .\n"
ttlhead+="@prefix om:<http://www.ontology-of-units-of-measure.org/resource/om-2/> .\n"
ttl.add("geo:GeoSPARQLCRS rdf:type owl:Ontology .\n")
ttl.add("geo:GeoSPARQLCRS dc:creator wd:Q67624599 .\n")
ttl.add("geo:GeoSPARQLCRS dc:description \"This ontology models coordinate reference systems\"@en .\n")
ttl.add("geo:GeoSPARQLCRS rdfs:label \"GeoSPARQL CRS Ontology Draft\"@en .\n")
ttl.add("owl:versionInfo rdfs:label \"0.1\"^^xsd:double .\n")
ttl.add("geo:CRS rdf:type owl:Class .\n")
ttl.add("geo:CRS rdfs:label \"Coordinate reference system\"@en .\n")
ttl.add("geo:GeographicCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:GeographicCRS rdf:type owl:Class .\n")
ttl.add("geo:GeographicCRS rdfs:label \"Geographic coordinate reference system\"@en .\n")
ttl.add("geo:GeodeticCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:GeodeticCRS rdf:type owl:Class .\n")
ttl.add("geo:GeodeticCRS rdfs:label \"Geodetic coordinate reference system\"@en .\n")
ttl.add("geo:CompoundCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:CompoundCRS rdf:type owl:Class .\n")
ttl.add("geo:CompoundCRS rdfs:label \"Compound coordinate reference system\"@en .\n")
ttl.add("geo:BoundCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:BoundCRS rdf:type owl:Class .\n")
ttl.add("geo:BoundCRS rdfs:label \"Bound coordinate reference system\"@en .\n")
ttl.add("geo:TemporalCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:TemporalCRS rdf:type owl:Class .\n")
ttl.add("geo:TemporalCRS rdfs:label \"Temporal coordinate reference system\"@en .\n")
ttl.add("geo:ParametricCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:ParametricCRS rdf:type owl:Class .\n")
ttl.add("geo:ParametricCRS rdfs:label \"Parametric coordinate reference system\"@en .\n")
ttl.add("geo:DerivedGeographicCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:DerivedGeographicCRS rdf:type owl:Class .\n")
ttl.add("geo:DerivedGeographicCRS rdfs:label \"Derived geographic coordinate reference system\"@en .\n")
ttl.add("geo:EngineeringCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:EngineeringCRS rdf:type owl:Class .\n")
ttl.add("geo:EngineeringCRS rdfs:label \"Temporal coordinate reference system\"@en .\n")
ttl.add("geo:VerticalCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:VerticalCRS rdf:type owl:Class .\n")
ttl.add("geo:VerticalCRS rdfs:label \"Temporal coordinate reference system\"@en .\n")
ttl.add("geo:GeocentricCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:GeocentricCRS rdf:type owl:Class .\n")
ttl.add("geo:GeocentricCRS rdfs:label \"Geocentric coordinate reference system\"@en .\n")
ttl.add("geo:ProjectedCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:ProjectedCRS rdf:type owl:Class .\n")
ttl.add("geo:ProjectedCRS rdfs:label \"Projected coordinate reference system\"@en .\n")
ttl.add("geo:Datum rdf:type owl:Class .\n")
ttl.add("geo:Datum rdfs:label \"datum\"@en .\n")
ttl.add("geo:Ellipsoid rdf:type owl:Class .\n")
ttl.add("geo:Ellipsoid rdfs:label \"ellipsoid\"@en .\n")
ttl.add("geo:PrimeMeridian rdf:type owl:Class .\n")
ttl.add("geo:PrimeMeridian rdfs:label \"prime meridian\"@en .\n")
ttl.add("geo:Projection rdf:type owl:Class .\n")
ttl.add("geo:Projection rdfs:label \"projection\"@en .\n")
ttl.add("geo:asProj4 rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:asProj4 rdfs:label \"asProj4\"@en .\n")
ttl.add("geo:asProjJSON rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:asProjJSON rdfs:label \"asProjJSON\"@en .\n")
ttl.add("geo:isProjected rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:isProjected rdfs:label \"isProjected\"@en .\n")
ttl.add("geo:isGeographic rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:isGeographic rdfs:label \"isGeographic\"@en .\n")
ttl.add("geo:isBound rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:isBound rdfs:label \"isBound\"@en .\n")
ttl.add("geo:isGeocentric rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:isGeocentric rdfs:label \"isGeocentric\"@en .\n")
ttl.add("geo:isVertical rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:isVertical rdfs:label \"isVertical\"@en .\n")
ttl.add("geo:asWKT rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:asWKT rdfs:label \"asWKT\"@en .\n")
ttl.add("geo:unit rdf:type owl:ObjectProperty .\n")
ttl.add("geo:unit rdfs:label \"unit\"@en .\n")
ttl.add("geo:ellipse rdf:type owl:ObjectProperty .\n")
ttl.add("geo:ellipse rdfs:label \"ellipse\"@en .\n")
ttl.add("geo:projection rdf:type owl:ObjectProperty .\n")
ttl.add("geo:projection rdfs:label \"projection\"@en .\n")
ttl.add("geo:epsgCode rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:epsgCode rdfs:label \"epsgCode\"@en .\n")
ttl.add("geo:envelope rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:envelope rdfs:label \"envelope\"@en .\n")
f = open("ontology.ttl", "w")
f.write(ttlhead)
for line in ttl:
	f.write(line)
f.close()
f = open("epsg.txt", "r")
i=0
curname=""
for line in f: 
	if i%2==0:
		curname=line.replace("#","").replace("\n","").replace("\r","")
	else:
		#Split epsg
		m = re.search('^.*\<([0-9]+)\> (.*)$', line)
		epsgcode="1234"
		wkt=""	
		if m:
			epsgcode = m.group(1)
			proj4string=m.group(2).replace("<","").replace(">","")	
		if epsgcode!="1234":
			curcrs=CRS.from_epsg(epsgcode)
			test=curcrs.to_proj4()
			if test!=None and test!="":
				proj4string=test
		else:
			curcrs=CRS.from_proj4(proj4string)
		try:
			wkt=curcrs.to_wkt().replace("\"","'").strip()
		except:
			print("")	
		if "PROJCS" in wkt:
			ttl.add("geoepsg:"+epsgcode+" rdf:type geo:ProjectedCRS .\n")
		elif "GEOGCS" in wkt:
			ttl.add("geoepsg:"+epsgcode+" rdf:type geo:GeographicCRS .\n")
		else:
			ttl.add("geoepsg:"+epsgcode+" rdf:type geo:CRS .\n")
		ttl.add("geoepsg:"+epsgcode+" rdf:type owl:NamedIndividual .\n")
		ttl.add("geoepsg:"+epsgcode+" rdfs:label \""+curname.strip()+"\"@en .\n")
		ttl.add("geoepsg:"+epsgcode+" geo:type \""+str(curcrs.type_name)+"\"^^xsd:boolean . \n")
		if curcrs.area_of_use!=None:
			ttl.add("geoepsg:"+epsgcode+" geo:envelope \"ENVELOPE("+str(curcrs.area_of_use.west)+" "+str(curcrs.area_of_use.south)+","+str(curcrs.area_of_use.east)+" "+str(curcrs.area_of_use.north)+")\"^^geo:wktLiteral . \n")
		ttl.add("geoepsg:"+epsgcode+" geo:isBound \""+str(curcrs.is_bound)+"\"^^xsd:boolean . \n")
		ttl.add("geoepsg:"+epsgcode+" geo:axis_info \""+str(curcrs.datum)+"\"^^xsd:string . \n")
		ttl.add("geoepsg:"+epsgcode+" geo:isVertical \""+str(curcrs.is_vertical)+"\"^^xsd:boolean . \n")
		ttl.add("geoepsg:"+epsgcode+" geo:isProjected \""+str(curcrs.is_projected)+"\"^^xsd:boolean . \n")
		ttl.add("geoepsg:"+epsgcode+" geo:isGeocentric \""+str(curcrs.is_geocentric)+"\"^^xsd:boolean . \n")
		ttl.add("geoepsg:"+epsgcode+" geo:isGeographic \""+str(curcrs.is_geographic)+"\"^^xsd:boolean . \n")
		ttl.add("geoepsg:"+epsgcode+" geo:asProj4 \""+proj4string.strip()+"\"^^xsd:string . \n")
		ttl.add("geoepsg:"+epsgcode+" geo:asProjJSON \""+curcrs.to_json().strip().replace("\"","'")+"\"^^xsd:string . \n")
		if wkt!="":
			ttl.add("geoepsg:"+epsgcode+" geo:asWKT \""+wkt+"\"^^geo:wktLiteral . \n")
		ttl.add("geoepsg:"+epsgcode+" geo:epsgCode \"EPSG:"+epsgcode+"\"^^xsd:string . \n")
		for spl in proj4string.split("+"):
			param=spl.split("=")
			if param[0]=="proj":
				if param[1].strip() in projections:
					ttl.add("geoepsg:"+epsgcode+" geo:projection "+projections[param[1].strip()]+" . \n")
					ttl.add(projections[param[1].strip()]+" rdf:type geo:Projection .\n")
				else:
					ttl.add("geoepsg:"+epsgcode+" geo:projection \""+param[1].strip()+"\" . \n")
			elif param[0]=="ellps":
				if param[1].strip() in spheroids:
					ttl.add("geoepsg:"+epsgcode+" geo:ellipse "+spheroids[param[1].strip()]+" . \n")
					ttl.add(spheroids[param[1].strip()]+" rdfs:label \""+str(curcrs.ellipsoid)+"\"@en . \n")
					ttl.add(spheroids[param[1].strip()]+" rdf:type geo:Ellipsoid .\n")	
				else:	
					ttl.add("geoepsg:"+epsgcode+" geo:ellipse \""+param[1].strip()+"\" . \n")
			elif param[0]=="units":
				if param[1].strip() in units:
					ttl.add("geoepsg:"+epsgcode+" geo:unit om:"+units[param[1].strip()]+" . \n")
					ttl.add(units[param[1].strip()]+" rdf:type om:Unit .\n")					
				else:
					ttl.add("geoepsg:"+epsgcode+" geo:unit \""+param[1].strip()+"\" . \n")				
	i+=1
f = open("result.ttl", "w")
f.write(ttlhead)
for line in ttl:
	f.write(line)
f.close()
