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
ttlhead+="@prefix skos:<http://www.w3.org/2004/02/skos/core#> .\n"
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
ttl.add("geo:CoordinateSystem rdf:type owl:Class .\n")
ttl.add("geo:CoordinateSystem rdfs:label \"Coordinate system\"@en .\n")
ttl.add("geo:CartesianCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geo:CartesianCoordinateSystem rdfs:subClassOf geo:CoordinateSystem .\n")
ttl.add("geo:CartesianCoordinateSystem rdfs:label \"Cartesian coordinate system\"@en .\n")
ttl.add("geo:CartesianCoordinateSystem skos:definition \"coordinate system in Euclidean space which gives the position of points relative to n mutually perpendicular straight axes all having the same unit of measure\"@en .\n")
ttl.add("geo:CartesianCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:LinearCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geo:LinearCoordinateSystem rdfs:subClassOf geo:CoordinateSystem .\n")
ttl.add("geo:LinearCoordinateSystem rdfs:label \"Linear coordinate system\"@en .\n")
ttl.add("geo:LinearCoordinateSystem skos:definition \"one-dimensional coordinate system in which a linear feature forms the axis\"@en .\n")
ttl.add("geo:LinearCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:EngineeringCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geo:EngineeringCoordinateSystem rdfs:subClassOf geo:CoordinateSystem .\n")
ttl.add("geo:EngineeringCoordinateSystem rdfs:label \"Engineering coordinate system\"@en .\n")
ttl.add("geo:EngineeringCoordinateSystem skos:definition \"coordinate system used by an engineering coordinate reference system, one of an affine coordinate system, a Cartesian coordinate system, a cylindrical coordinate system, a linear coordinate sytem, an ordinal coordinate system, a polar coordinate system or a spherical coordinate system\"@en .\n")
ttl.add("geo:EngineeringCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:GeodeticCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geo:GeodeticCoordinateSystem rdfs:subClassOf geo:CoordinateSystem .\n")
ttl.add("geo:GeodeticCoordinateSystem rdfs:label \"Geodetic coordinate system\"@en .\n")
ttl.add("geo:GeodeticCoordinateSystem skos:definition \"coordinate system used by a Geodetic CRS, one of a Cartesian coordinate system or a spherical coordinate system\"@en .\n")
ttl.add("geo:GeodeticCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:EllipsoidalCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geo:EllipsoidalCoordinateSystem rdfs:subClassOf geo:CoordinateSystem .\n")
ttl.add("geo:EllipsoidalCoordinateSystem rdfs:label \"Ellipsoidal coordinate system\"@en .\n")
ttl.add("geo:EllipsoidalCoordinateSystem skos:definition \"two- or three-dimensional coordinate system in which position is specified by geodetic latitude, geodetic longitude, and (in the three-dimensional case) ellipsoidal height\"@en .\n")
ttl.add("geo:EllipsoidalCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:OrdinalCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geo:OrdinalCoordinateSystem rdfs:subClassOf geo:CoordinateSystem .\n")
ttl.add("geo:OrdinalCoordinateSystem rdfs:label \"Ordinal coordinate system\"@en .\n")
ttl.add("geo:OrdinalCoordinateSystem skos:definition \"n-dimensional coordinate system in which every axis uses integers\"@en .\n")
ttl.add("geo:OrdinalCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:SphericalCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geo:SphericalCoordinateSystem rdfs:subClassOf geo:CoordinateSystem .\n")
ttl.add("geo:SphericalCoordinateSystem rdfs:label \"Spherical coordinate system\"@en .\n")
ttl.add("geo:SphericalCoordinateSystem skos:definition \"three-dimensional coordinate system in Euclidean space with one distance measured from the origin and two angular coordinates\"@en .\n")
ttl.add("geo:SphericalCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:CylindricalCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geo:CylindricalCoordinateSystem rdfs:subClassOf geo:CoordinateSystem .\n")
ttl.add("geo:CylindricalCoordinateSystem rdfs:label \"Cylindrical coordinate system\"@en .\n")
ttl.add("geo:CylindricalCoordinateSystem skos:definition \"three-dimensional coordinate system in Euclidean space in which position is specified by two linear coordinates and one angular coordinate\"@en .\n")
ttl.add("geo:CylindricalCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:PolarCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geo:PolarCoordinateSystem rdfs:subClassOf geo:CoordinateSystem .\n")
ttl.add("geo:PolarCoordinateSystem rdfs:label \"Polar coordinate system\"@en .\n")
ttl.add("geo:PolarCoordinateSystem skos:definition \"two-dimensional coordinate system in Euclidean space in which position is specified by one distance coordinate and one angular coordinate\"@en .\n")
ttl.add("geo:PolarCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:ParametricCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geo:ParametricCoordinateSystem rdfs:subClassOf geo:CoordinateSystem .\n")
ttl.add("geo:ParametricCoordinateSystem rdfs:label \"Parametric coordinate system\"@en .\n")
ttl.add("geo:ParametricCoordinateSystem skos:definition \"one-dimensional coordinate system where the axis units are parameter values which are not inherently spatial\"@en .\n")
ttl.add("geo:ParametricCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:VerticalCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geo:VerticalCoordinateSystem rdfs:subClassOf geo:CoordinateSystem .\n")
ttl.add("geo:VerticalCoordinateSystem rdfs:label \"Vertical coordinate system\"@en .\n")
ttl.add("geo:VerticalCoordinateSystem skos:definition \"one-dimensional coordinate system used to record the heights or depths of points, usually dependent on the Earth's gravity field\"@en .\n")
ttl.add("geo:VerticalCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:TemporalCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geo:TemporalCoordinateSystem rdfs:subClassOf geo:CoordinateSystem .\n")
ttl.add("geo:TemporalCoordinateSystem rdfs:label \"Temporal coordinate system\"@en .\n")
ttl.add("geo:TemporalCoordinateSystem skos:definition \"one-dimensionalcoordinate system where the axis is time\"@en .\n")
ttl.add("geo:TemporalCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:CRS rdf:type owl:Class .\n")
ttl.add("geo:CRS rdfs:label \"Coordinate reference system\"@en .\n")
ttl.add("geo:CRS skos:definition \"coordinate system that is related to an object by a datum\"@en .\n")
ttl.add("geo:CRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:GeographicCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:GeographicCRS rdf:type owl:Class .\n")
ttl.add("geo:GeographicCRS rdfs:label \"Geographic coordinate reference system\"@en .\n")
ttl.add("geo:GeographicCRS skos:definition \"coordinate reference system that has a geodetic reference frame and an ellipsoidal coordinate system\"@en .\n")
ttl.add("geo:AffineCoordinateSystem rdfs:subClassOf geo:CoordinateSystem .\n")
ttl.add("geo:AffineCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geo:AffineCoordinateSystem rdfs:label \"Affine coordinate system\"@en .\n")
ttl.add("geo:AffineCoordinateSystem skos:definition \"coordinate system in Euclidean space with straight axes that are not necessarily mutually perpendicular\"@en .\n")
ttl.add("geo:AffineCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:GeodeticCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:GeodeticCRS rdf:type owl:Class .\n")
ttl.add("geo:GeodeticCRS rdfs:label \"Geodetic coordinate reference system\"@en .\n")
ttl.add("geo:GeodeticCRS skos:definition \"three-dimensional coordinate reference system based on a geodetic reference frame and having either a three-dimensional Cartesian or a spherical coordinate system\"@en .\n")
ttl.add("geo:CompoundCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:CompoundCRS rdf:type owl:Class .\n")
ttl.add("geo:CompoandCRS skos:definition \"coordinate reference system using at least two independent coordinate reference systems\"@en .\n")
ttl.add("geo:CompoundCRS rdfs:label \"Compound coordinate reference system\"@en .\n")
ttl.add("geo:CoordinateConversion rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:CoordinateConversion rdf:type owl:Class .\n")
ttl.add("geo:CoordinateConversion rdfs:label \"Compound coordinate reference system\"@en .\n")
ttl.add("geo:BoundCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:BoundCRS rdf:type owl:Class .\n")
ttl.add("geo:BoundCRS rdfs:label \"Bound coordinate reference system\"@en .\n")
ttl.add("geo:TemporalCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:TemporalCRS rdf:type owl:Class .\n")
ttl.add("geo:TemporalCRS rdfs:label \"Temporal coordinate reference system\"@en .\n")
ttl.add("geo:TemporalCRS skos:definition \"coordinate reference system based on a temporal datum\"@en .\n")
ttl.add("geo:ParametricCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:ParametricCRS rdf:type owl:Class .\n")
ttl.add("geo:ParametricCRS rdfs:label \"Parametric coordinate reference system\"@en .\n")
ttl.add("geo:ParametricCRS skos:definition \"one-dimensional coordinate system where the axis units are parameter values which are not inherently spatial\"@en .\n")
ttl.add("geo:DerivedGeographicCRS rdfs:subClassOf geo:GeodeticCRS .\n")
ttl.add("geo:DerivedGeographicCRS rdf:type owl:Class .\n")
ttl.add("geo:DerivedGeographicCRS rdfs:label \"Derived geographic coordinate reference system\"@en .\n")
ttl.add("geo:DerivedGeographicCRS skos:definition \"coordinate reference system that is defined through the application of a specified coordinate conversion to the coordinates within a previously established coordinate reference system\"@en .\n")
ttl.add("geo:EngineeringCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:EngineeringCRS rdf:type owl:Class .\n")
ttl.add("geo:EngineeringCRS rdfs:label \"Engineering coordinate reference system\"@en .\n")
ttl.add("geo:VerticalCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:VerticalCRS rdf:type owl:Class .\n")
ttl.add("geo:VerticalCRS rdfs:label \"Vertical coordinate reference system\"@en .\n")
ttl.add("geo:SphericCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:SphericCRS rdf:type owl:Class .\n")
ttl.add("geo:SphericCRS rdfs:label \"Spheric coordinate reference system\"@en .\n")
ttl.add("geo:SphericCRS skos:definition \"three-dimensional coordinate system in Euclidean space in which position is specified by one distance coordinate and two angular coordinates\"@en .\n")
ttl.add("geo:GeocentricCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:GeocentricCRS rdf:type owl:Class .\n")
ttl.add("geo:GeocentricCRS rdfs:label \"Geocentric coordinate reference system\"@en .\n")
ttl.add("geo:StaticCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:StaticCRS rdf:type owl:Class .\n")
ttl.add("geo:StaticCRS rdfs:label \"Static coordinate reference system\"@en .\n")
ttl.add("geo:StaticCRS skos:definition \"coordinate reference system that has a static reference frame\"@en .\n")
ttl.add("geo:ProjectedCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:ProjectedCRS rdf:type owl:Class .\n")
ttl.add("geo:ProjectedCRS rdfs:label \"Projected coordinate reference system\"@en .\n")
ttl.add("geo:ProjectedCRS skos:definition \"coordinate reference system derived from a geographic coordinate reference system by applying a map projection\"@en .\n")
ttl.add("geo:Datum rdf:type owl:Class .\n")
ttl.add("geo:Datum rdfs:label \"datum\"@en .\n")
ttl.add("geo:Datum skos:definition \"specification of the relationship of a coordinate system to an object, thus creating a coordinate reference system\"@en .\n")
ttl.add("geo:TemporalDatum rdfs:subClassOf geo:Datum .\n")
ttl.add("geo:TemporalDatum rdf:type owl:Class .\n")
ttl.add("geo:TemporalDatum rdfs:label \"temporal datum\"@en .\n")
ttl.add("geo:TemporalDatum skos:definition \"coordinate reference system based on a temporal datum\"@en .\n")
ttl.add("geo:VerticalDatum rdfs:subClassOf geo:Datum .\n")
ttl.add("geo:VerticalDatum rdf:type owl:Class .\n")
ttl.add("geo:VerticalDatum rdfs:label \"vertical datum\"@en .\n")
ttl.add("geo:VerticalDatum skos:definition \"reference frame describing the relation of gravity-related heights or depths to the Earth\"@en .\n")
ttl.add("geo:EngineeringDatum rdfs:subClassOf geo:Datum .\n")
ttl.add("geo:EngineeringDatum rdf:type owl:Class .\n")
ttl.add("geo:EngineeringDatum rdfs:label \"engineering datum\"@en .\n")
ttl.add("geo:EngineeringDatum skos:definition \"datum describing the relationship of a coordinate system to a local reference\"@en .\n")
ttl.add("geo:Ellipsoid rdf:type owl:Class .\n")
ttl.add("geo:Ellipsoid rdfs:label \"ellipsoid\"@en .\n")
ttl.add("geo:Ellipsoid skos:definition \"reference ellipsoid\"@en .\n")
ttl.add("geo:PrimeMeridian rdf:type owl:Class .\n")
ttl.add("geo:PrimeMeridian rdfs:label \"prime meridian\"@en .\n")
ttl.add("geo:PrimeMeridian skos:definition \"meridian from which the longitudes of other meridians are quantified\"@en .\n")
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
ttl.add("geo:utm_zone rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:utm_zone rdfs:label \"utm zone\"@en .\n")
f = open("ontology.ttl", "w","utf-8")
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
		if curcrs.coordinate_system!=None:
			ttl.add("geoepsg:"+epsgcode+" geo:coordinateSystem \""+str(curcrs.coordinate_system)+"\"^^xsd:string . \n")
		if curcrs.coordinate_operation!=None:
			ttl.add("geoepsg:"+epsgcode+" geo:coordinateOperation \""+str(curcrs.coordinate_operation)+"\"^^xsd:string . \n")
		if curcrs.prime_meridian!=None:
			ttl.add("geoepsg:"+epsgcode+" geo:primeMeridian \""+str(curcrs.prime_meridian)+"\"^^xsd:string . \n")
		ttl.add("geoepsg:"+epsgcode+" geo:axis_info \""+str(curcrs.datum)+"\"^^xsd:string . \n")
		ttl.add("geoepsg:"+epsgcode+" geo:isVertical \""+str(curcrs.is_vertical)+"\"^^xsd:boolean . \n")
		ttl.add("geoepsg:"+epsgcode+" geo:isProjected \""+str(curcrs.is_projected)+"\"^^xsd:boolean . \n")
		ttl.add("geoepsg:"+epsgcode+" geo:isGeocentric \""+str(curcrs.is_geocentric)+"\"^^xsd:boolean . \n")
		ttl.add("geoepsg:"+epsgcode+" geo:isGeographic \""+str(curcrs.is_geographic)+"\"^^xsd:boolean . \n")
		if curcrs.utm_zone!=None:
			ttl.add("geoepsg:"+epsgcode+" geo:utm_zone \""+str(curcrs.utm_zone)+"\"^^xsd:string . \n")
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
f = open("result.ttl", "w", "utf-8")
f.write(ttlhead)
for line in ttl:
	f.write(line)
f.close()
