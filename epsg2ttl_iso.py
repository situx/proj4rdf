import os
import re
import pyproj
import csv
from rdflib import Graph
from pyproj import CRS
import urllib.request
from shapely.geometry import box

convertToGML=False

def crsToTTL(ttl,curcrs,x,geodcounter,crsclass):
	epsgcode=str(x)
	wkt=curcrs.to_wkt().replace("\"","'").strip()
	if crsclass!=None:
		ttl.add("geoepsg:"+epsgcode+" rdf:type "+crsclass+" .\n")
	elif "Projected CRS" in curcrs.type_name:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geocrs:ProjectedCRS .\n")
	elif "Geographic 2D CRS" in curcrs.type_name:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geocrs:GeographicCRS .\n")
	elif "Geographic 3D CRS" in curcrs.type_name:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geocrs:GeographicCRS .\n")
	elif "Bound CRS" in curcrs.type_name:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geocrs:BoundCRS .\n")
	elif "Vertical CRS" in curcrs.type_name:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geocrs:VerticalCRS .\n")
	elif "Geocentric CRS" in curcrs.type_name:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geocrs:GeocentricCRS .\n")
	elif "Geographic 3D CRS" in curcrs.type_name:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geocrs:GeographicCRS .\n")
	elif "Compound CRS" in curcrs.type_name:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geocrs:CompoundCRS .\n")
		for subcrs in curcrs.sub_crs_list:
			ttl.add("geoepsg:"+epsgcode+" geocrs:includesSRS geoepsg:"+str(subcrs.to_epsg())+" .\n")			
	else:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geocrs:CRS .\n")
	ttl.add("geoepsg:"+epsgcode+" rdf:type prov:Entity. \n")
	ttl.add("geoepsg:"+epsgcode+" geocrs:isApplicableTo geocrsisbody:Earth .\n")
	ttl.add("geoepsg:"+epsgcode+" rdf:type owl:NamedIndividual .\n")
	ttl.add("geoepsg:"+epsgcode+" rdfs:label \""+curcrs.name.strip()+"\"@en .\n")
	ttl.add("geoepsg:"+epsgcode+" geocrs:isBound \""+str(curcrs.is_bound).lower()+"\"^^xsd:boolean . \n")
	if curcrs.coordinate_system!=None and curcrs.coordinate_system.name in coordinatesystem:
		ttl.add("geoepsg:"+epsgcode+"_cs rdf:type "+coordinatesystem[curcrs.coordinate_system.name]+" . \n")
		if len(curcrs.coordinate_system.axis_list)==2:
			ttl.add("geoepsg:"+epsgcode+"_cs rdf:type geocrs:PlanarCoordinateSystem . \n")
		elif len(curcrs.coordinate_system.axis_list)==3:
			ttl.add("geoepsg:"+epsgcode+"_cs rdf:type geocrs:3DCoordinateSystem . \n")			
		ttl.add("geoepsg:"+epsgcode+"_cs rdfs:label \"EPSG:"+epsgcode+" CS: "+curcrs.coordinate_system.name+"\" . \n")
		if curcrs.coordinate_system.remarks!=None:
			ttl.add("geoepsg:"+epsgcode+"_cs rdfs:comment \""+str(curcrs.coordinate_system.remarks)+"\"@en . \n")
		if curcrs.coordinate_system.scope!=None:
			ttl.add("geoepsg:"+epsgcode+"_cs geocrs:scope \""+str(curcrs.coordinate_system.scope)+"\" . \n")
		for axis in curcrs.coordinate_system.axis_list:
			axisid=axis.name.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_")+"_"+axis.unit_name.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_")+"_"+axis.direction.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_")
			ttl.add("geoepsg:"+epsgcode+"_cs geocrs:axis geocrsaxis:"+axisid+" . \n")
			ttl.add("geocrsaxis:"+axisid+" rdf:type geocrs:CoordinateSystemAxis . \n")
			ttl.add("geocrsaxis:"+axisid+" geocrs:direction geocrs:"+axis.direction+" . \n")
			ttl.add("geocrsaxis:"+axisid+" geocrs:axisAbbrev \""+str(axis.abbrev).replace("\"","'")+"\"^^xsd:string . \n")				
			ttl.add("geocrsaxis:"+axisid+" geocrs:unit_conversion_factor \""+str(axis.unit_conversion_factor)+"\"^^xsd:double . \n")	
			ttl.add("geocrsaxis:"+axisid+" geocrs:unit_auth_code \""+str(axis.unit_auth_code)+"\"^^xsd:string . \n")
			ttl.add("geocrsaxis:"+axisid+" geocrs:unit_code \""+str(axis.unit_code)+"\"^^xsd:string . \n")					
			ttl.add("geocrsaxis:"+axis.direction+" rdf:type geocrs:AxisDirection . \n")				
			if axis.unit_name in units:
				ttl.add("geocrsaxis:"+axisid+" geocrs:unit "+units[axis.unit_name]+" . \n")
				ttl.add("geocrsaxis:"+axisid+" rdfs:label \""+axis.name+" ("+str(units[axis.unit_name])+")\"@en . \n")						
			else:
				ttl.add("geocrsaxis:"+axisid+" geocrs:unit \""+axis.unit_name+"\" . \n")
				ttl.add("geocrsaxis:"+axisid+" rdfs:label \""+axis.name+" ("+str(axis.unit_name)+")\"@en . \n")	
		ttl.add("geoepsg:"+epsgcode+"_cs geocrs:asWKT \""+str(curcrs.coordinate_system.to_wkt()).replace("\"","'").replace("\n","")+"\" . \n")
		ttl.add("geoepsg:"+epsgcode+"_cs geocrs:asProjJSON \""+str(curcrs.coordinate_system.to_json()).replace("\"","'").replace("\n","")+"\" . \n")
		ttl.add("geoepsg:"+epsgcode+" geocrs:coordinateSystem geoepsg:"+epsgcode+"_cs . \n")		
	elif curcrs.coordinate_system!=None:
		ttl.add("geoepsg:"+epsgcode+" geocrs:coordinateSystem \""+str(curcrs.coordinate_system)+"\"^^xsd:string . \n")
	if curcrs.source_crs!=None:
		ttl.add("geoepsg:"+epsgcode+" geocrs:sourceCRS geoepsg:"+str(curcrs.source_crs.to_epsg())+" . \n")
	if curcrs.target_crs!=None:
		ttl.add("geoepsg:"+epsgcode+" geocrs:targetCRS geoepsg:"+str(curcrs.target_crs.to_epsg())+" . \n")
	if curcrs.scope!=None:
		if "," in curcrs.scope:
			for scp in curcrs.scope.split(","):
				#print("Scope: "+scp)
				if scp.lower().strip().replace(".","") in scope:
					ttl.add("geoepsg:"+epsgcode+" geocrs:usage "+scope[scp.lower().strip().replace(".","")]+" . \n")
					ttl.add(scope[scp.lower().strip().replace(".","")]+" rdfs:subClassOf geocrs:SRSApplication . \n")
				else:
					ttl.add("geoepsg:"+epsgcode+" geocrs:usage \""+str(curcrs.datum.scope)+"\"^^xsd:string . \n")
		ttl.add("geoepsg:"+epsgcode+" geocrs:scope \""+str(curcrs.scope).replace("\"","'")+"\"^^xsd:string . \n")
	if curcrs.area_of_use!=None:
		ttl.add("geoepsg:"+epsgcode+" geocrs:area_of_use geoepsg:"+epsgcode+"_area_of_use . \n")
		ttl.add("geoepsg:"+epsgcode+"_area_of_use"+" rdf:type geocrs:AreaOfUse .\n")
		ttl.add("geoepsg:"+epsgcode+"_area_of_use"+" rdfs:label \""+str(curcrs.area_of_use.name).replace("\"","'")+"\"@en .\n")
		b = box(curcrs.area_of_use.west, curcrs.area_of_use.south, curcrs.area_of_use.east, curcrs.area_of_use.north)
		ttl.add("geoepsg:"+epsgcode+"_area_of_use"+" geocrs:extent   \"<http://www.opengis.net/def/crs/OGC/1.3/CRS84> "+str(b.wkt)+"\"^^geo:wktLiteral . \n")
		#\"ENVELOPE("+str(curcrs.area_of_use.west)+" "+str(curcrs.area_of_use.south)+","+str(curcrs.area_of_use.east)+" "+str(curcrs.area_of_use.north)+")\"^^geo:wktLiteral . \n")
	if curcrs.get_geod()!=None:
		geoid="geocrsgeod:"+str(geodcounter)
		if curcrs.datum.ellipsoid!=None:
			if curcrs.datum.ellipsoid.name in spheroids:
				geoid=spheroids[curcrs.datum.ellipsoid.name]
				ttl.add(geoid+" rdf:type geocrs:Ellipsoid . \n")
				ttl.add(geoid+" rdfs:label \""+curcrs.datum.ellipsoid.name+"\"@en . \n")
				ttl.add(geoid+" geocrs:approximates geocrsisbody:Earth . \n")
			elif curcrs.get_geod().sphere:
				geoid="geocrsgeod:"+str(curcrs.datum.ellipsoid.name).replace(" ","_").replace("(","_").replace(")","_")
				ttl.add(geoid+" rdf:type geocrs:Sphere . \n")
				ttl.add(geoid+" rdfs:label \""+curcrs.datum.ellipsoid.name+"\"@en . \n")
				ttl.add(geoid+" geocrs:approximates geocrsisbody:Earth . \n")
			else:
				geoid="geocrsgeod:"+str(curcrs.datum.ellipsoid.name).replace(" ","_").replace("(","_").replace(")","_")
				ttl.add(geoid+" rdf:type geocrs:Geoid . \n")
				ttl.add(geoid+" rdfs:label \""+curcrs.datum.ellipsoid.name+"\"@en . \n")
				ttl.add(geoid+" geocrs:approximates geocrsisbody:Earth . \n")
		else:
			ttl.add("geoepsg:"+epsgcode+" geocrs:ellipsoid geocrsgeod:"+str(geodcounter)+" . \n")
			ttl.add("geocrsgeod:geod"+str(geodcounter)+" rdf:type geocrs:Geoid . \n")
			ttl.add(geoid+" rdfs:label \"Geoid "+str(geodcounter)+"\"@en . \n")
			ttl.add(geoid+" geocrs:approximates geocrsisbody:Earth . \n")
		ttl.add(geoid+" skos:definition \""+str(curcrs.get_geod().initstring)+"\"^^xsd:string . \n")
		ttl.add(geoid+" geocrs:eccentricity \""+str(curcrs.get_geod().es)+"\"^^xsd:double . \n")
		ttl.add(geoid+" geocrs:isSphere \""+str(curcrs.get_geod().sphere)+"\"^^xsd:boolean . \n")
		ttl.add(geoid+" geocrs:semiMajorAxis \""+str(curcrs.get_geod().a)+"\"^^xsd:string . \n")
		ttl.add(geoid+" geocrs:semiMinorAxis \""+str(curcrs.get_geod().b)+"\"^^xsd:string . \n")
		ttl.add(geoid+" geocrs:flatteningParameter \""+str(curcrs.get_geod().f)+"\"^^xsd:double . \n")
		geodcounter+=1
	if curcrs.coordinate_operation!=None:
		coordoperationid=curcrs.coordinate_operation.name.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_").replace(",","_").replace("&","and").strip()
		ttl.add("geoepsg:"+epsgcode+" geocrs:coordinateOperation geocrsoperation:"+str(coordoperationid)+" . \n")
		ttl.add("geocrsoperation:"+str(coordoperationid)+" geocrs:accuracy \""+str(curcrs.coordinate_operation.accuracy)+"\"^^xsd:double . \n")
		ttl.add("geocrsoperation:"+str(coordoperationid)+" geocrs:method_name \""+str(curcrs.coordinate_operation.method_name)+"\" . \n")
		ttl.add("geocrsoperation:"+str(coordoperationid)+" geocrs:asProj4 \""+str(curcrs.coordinate_operation.to_proj4()).strip().replace("\"","'").replace("\n","")+"\" . \n")
		ttl.add("geocrsoperation:"+str(coordoperationid)+" geocrs:asProjJSON \""+str(curcrs.coordinate_operation.to_json()).strip().replace("\"","'").replace("\n","")+"\" . \n")
		ttl.add("geocrsoperation:"+str(coordoperationid)+" geocrs:asWKT \""+str(curcrs.coordinate_operation.to_wkt()).replace("\"","'").replace("\n","")+"\"^^geo:wktLiteral . \n")
		if curcrs.coordinate_operation.scope!=None:
			ttl.add("geocrsoperation:"+str(coordoperationid)+" geocrs:scope \""+str(curcrs.coordinate_operation.scope).replace("\"","'")+"\"^^xsd:string . \n")
		if curcrs.coordinate_operation.remarks!=None:
			ttl.add("geocrsoperation:"+str(coordoperationid)+" rdfs:comment \""+str(curcrs.coordinate_operation.remarks).replace("\"","'").replace("\n","")+"\"^^xsd:string . \n")
		ttl.add("geocrsoperation:"+str(coordoperationid)+" geocrs:has_ballpark_transformation \""+str(curcrs.coordinate_operation.has_ballpark_transformation)+"\"^^xsd:boolean . \n")
		if curcrs.coordinate_operation.area_of_use!=None:
			ttl.add("geocrsoperation:"+str(coordoperationid)+" geocrs:area_of_use geocrsaou:"+str(coordoperationid)+"_area_of_use . \n")
			ttl.add("geocrsaou:"+str(coordoperationid)+"_area_of_use"+" rdf:type geocrs:AreaOfUse .\n")
			ttl.add("geocrsaou:"+str(coordoperationid)+"_area_of_use"+" rdfs:label \""+str(curcrs.coordinate_operation.area_of_use.name).replace("\"","'")+"\"@en .\n")
			b = box(curcrs.coordinate_operation.area_of_use.west, curcrs.coordinate_operation.area_of_use.south, curcrs.coordinate_operation.area_of_use.east, curcrs.coordinate_operation.area_of_use.north)
			ttl.add("geocrsaou:"+str(coordoperationid)+"_area_of_use geocrs:extent \"<http://www.opengis.net/def/crs/OGC/1.3/CRS84> "+str(b.wkt)+"\"^^geo:wktLiteral . \n")
			#ENVELOPE("+str(curcrs.coordinate_operation.area_of_use.west)+" "+str(curcrs.coordinate_operation.area_of_use.south)+","+str(curcrs.coordinate_operation.area_of_use.east)+" "+str(curcrs.coordinate_operation.area_of_use.north)+")\"^^geocrs:wktLiteral . \n")
		if curcrs.coordinate_operation.towgs84!=None:
			print(curcrs.coordinate_operation.towgs84)
		for par in curcrs.coordinate_operation.params:
			ttl.add(" geocrs:"+str(par.name)[0].lower()+str(par.name).title().replace(" ","")[1:]+" rdf:type owl:DatatypeProperty . \n") 
			ttl.add(" geocrs:"+str(par.name)[0].lower()+str(par.name).title().replace(" ","")[1:]+" rdfs:range xsd:double . \n") 
			ttl.add(" geocrs:"+str(par.name)[0].lower()+str(par.name).title().replace(" ","")[1:]+" rdfs:domain geocrs:CoordinateOperation . \n") 
			ttl.add(" geocrs:"+str(par.name)[0].lower()+str(par.name).title().replace(" ","")[1:]+" rdfs:label \""+str(par.name)+"\"@en . \n")				
			ttl.add("geocrsoperation:"+str(coordoperationid)+" geocrs:"+str(par.name)[0].lower()+str(par.name).title().replace(" ","")[1:]+" \""+str(par.value)+"\"^^xsd:double . \n") 
		for grid in curcrs.coordinate_operation.grids:
			ttl.add("geocrsoperation:"+str(coordoperationid)+" geocrs:grid geocrsgrid:"+str(grid.name).replace(" ","_")+" . \n")
			ttl.add("geocrsgrid:"+str(grid.name).replace(" ","_")+" rdf:type geocrs:Grid . \n")
			ttl.add("geocrsgrid:"+str(grid.name).replace(" ","_")+" rdfs:label \""+str(grid.full_name)+"\"@en . \n")
			ttl.add("geocrsgrid:"+str(grid.name).replace(" ","_")+" rdfs:label \""+str(grid.short_name)+"\"@en . \n")
			ttl.add("geocrsgrid:"+str(grid.name).replace(" ","_")+" geocrs:open_license \""+str(grid.open_license)+"\"^^xsd:boolean . \n")
			ttl.add("geocrsgrid:"+str(grid.name).replace(" ","_")+" rdfs:comment \""+str(grid.url)+"\"@en . \n")
		if curcrs.coordinate_operation.operations!=None:
			for operation in curcrs.coordinate_operation.operations:
				ttl.add("geocrsoperation:"+str(coordoperationid)+" geocrs:operation \""+str(operation).replace("\n","").replace("\"","'")+"\"^^xsd:string . \n")
		if curcrs.coordinate_operation.type_name==None:
			ttl.add("geocrsoperation:"+str(coordoperationid)+" rdf:type geocrs:CoordinateOperation . \n")
		elif curcrs.coordinate_operation.type_name=="Conversion":
			found=False
			if curcrs.coordinate_operation.to_proj4()!=None:
				proj4string=curcrs.coordinate_operation.to_proj4().strip().replace("\"","'").replace("\n","")
				for prj in projections:
					if prj in proj4string:
						ttl.add("geocrsoperation:"+str(coordoperationid)+" rdf:type "+projections[prj]+" . \n")
						found=True
						break
				if not found:
					print(proj4string)
					ttl.add("geocrsoperation:"+str(coordoperationid)+" rdf:type geocrs:Conversion . \n")
		elif curcrs.coordinate_operation.type_name=="Transformation":
			ttl.add("geocrsoperation:"+str(coordoperationid)+" rdf:type geocrs:Transformation . \n")
		elif curcrs.coordinate_operation.type_name=="Concatenated Operation":
			ttl.add("geocrsoperation:"+str(coordoperationid)+" rdf:type geocrs:ConcatenatedOperation . \n")
		elif curcrs.coordinate_operation.type_name=="Other Coordinate Operation":
			ttl.add("geocrsoperation:"+str(coordoperationid)+" rdf:type geocrs:OtherCoordinateOperation . \n")
		ttl.add("geocrsoperation:"+str(coordoperationid)+" rdfs:label \""+curcrs.coordinate_operation.name+": "+curcrs.coordinate_operation.method_name+"\"@en . \n")
	if curcrs.datum!=None:
		datumid=str(curcrs.datum.name.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_").replace("+","_plus").replace("[","_").replace("]","_"))
		ttl.add("geoepsg:"+epsgcode+" geocrs:datum geocrsdatum:"+str(datumid)+" . \n")
		if "Geodetic Reference Frame" in curcrs.datum.type_name:
			ttl.add("geocrsdatum:"+str(datumid)+" rdf:type geocrs:GeodeticReferenceFrame . \n")
		elif "Dynamic Vertical Reference Frame" in curcrs.datum.type_name:
			ttl.add("geocrsdatum:"+str(datumid)+" rdf:type geocrs:DynamicVerticalReferenceFrame . \n")
		elif "Vertical Reference Frame" in curcrs.datum.type_name:
			ttl.add("geocrsdatum:"+str(datumid)+" rdf:type geocrs:VerticalReferenceFrame . \n")
		else:
			#print(curcrs.datum.type_name)
			ttl.add("geocrsdatum:"+str(datumid)+" rdf:type geocrs:Datum . \n")
		ttl.add("geocrsdatum:"+str(datumid)+" rdfs:label \"Datum: "+curcrs.datum.name+"\"@en . \n")
		if curcrs.datum.remarks!=None:
			ttl.add("geocrsdatum:"+str(datumid)+" rdfs:comment \""+str(curcrs.datum.remarks)+"\"@en . \n")
		if curcrs.datum.scope!=None:
			ttl.add("geocrsdatum:"+str(datumid)+" geocrs:scope \""+str(curcrs.datum.scope)+"\"^^xsd:string . \n")
			if "," in curcrs.datum.scope:
				for scp in curcrs.datum.scope.split(","):
					#print("Scope: "+scp)
					if scp.lower().strip().replace(".","") in scope:
						ttl.add("geocrsdatum:"+str(datumid)+" geocrs:usage "+scope[scp.lower().strip().replace(".","")]+" . \n")
						ttl.add(scope[scp.lower().strip().replace(".","")]+" rdfs:subClassOf geocrs:SRSApplication . \n")
					else:
						ttl.add("geocrsdatum:"+str(datumid)+" geocrs:usage \""+str(curcrs.datum.scope)+"\"^^xsd:string . \n")
			#print(str(curcrs.datum.scope))
		if curcrs.datum.ellipsoid!=None and curcrs.datum.ellipsoid.name in spheroids:
			ttl.add("geocrsdatum:"+str(datumid)+" geocrs:ellipsoid "+spheroids[curcrs.datum.ellipsoid.name]+" . \n")
			ttl.add(spheroids[curcrs.datum.ellipsoid.name]+" rdfs:label \""+str(curcrs.datum.ellipsoid.name)+"\"@en . \n")
			ttl.add(spheroids[curcrs.datum.ellipsoid.name]+" rdf:type geocrs:Ellipsoid .\n")	
			ttl.add(spheroids[curcrs.datum.ellipsoid.name]+" geocrs:inverse_flattening \""+str(curcrs.datum.ellipsoid.inverse_flattening)+"\"^^xsd:double .\n")			
			if curcrs.datum.ellipsoid.remarks!=None:
				ttl.add(spheroids[curcrs.datum.ellipsoid.name]+" rdfs:comment \""+str(curcrs.datum.ellipsoid.remarks)+"\"^^xsd:string .\n")
			ttl.add(spheroids[curcrs.datum.ellipsoid.name]+" geocrs:is_semi_minor_computed \""+str(curcrs.datum.ellipsoid.is_semi_minor_computed).lower()+"\"^^xsd:boolean .\n")
		elif curcrs.datum.ellipsoid!=None:	
			ttl.add("geocrsdatum:"+str(datumid)+" geocrs:ellipse \""+curcrs.datum.ellipsoid.name+"\" . \n")
		if curcrs.prime_meridian!=None:
			ttl.add("geocrsdatum:"+str(datumid)+" geocrs:primeMeridian geocrsmeridian:"+curcrs.prime_meridian.name.replace(" ","")+" . \n")
			ttl.add("geocrsmeridian:"+curcrs.prime_meridian.name.replace(" ","")+" rdf:type geocrs:PrimeMeridian . \n")
			ttl.add("geocrsmeridian:"+curcrs.prime_meridian.name.replace(" ","")+" rdfs:label \""+curcrs.prime_meridian.name+"\"@en . \n")
			ttl.add("geocrsmeridian:"+curcrs.prime_meridian.name.replace(" ","")+" geocrs:longitude \""+str(curcrs.prime_meridian.longitude)+"\"^^xsd:double . \n")
			if curcrs.prime_meridian.unit_name in units:
				ttl.add("geocrsmeridian:"+curcrs.prime_meridian.name.replace(" ","")+" geocrs:unit om:"+units[curcrs.prime_meridian.unit_name]+" . \n")
				ttl.add(units[curcrs.prime_meridian.unit_name]+" rdf:type om:Unit .\n")	
			else:
				ttl.add("geocrsmeridian:"+curcrs.prime_meridian.name.replace(" ","")+" geocrs:unit \""+str(curcrs.prime_meridian.unit_name)+"\" . \n")
			ttl.add("geocrsmeridian:"+curcrs.prime_meridian.name.replace(" ","")+" geocrs:asWKT \""+str(curcrs.prime_meridian.to_wkt()).replace("\"","'").replace("\n","")+"\" . \n")
			ttl.add("geocrsmeridian:"+curcrs.prime_meridian.name.replace(" ","")+" geocrs:asProjJSON \""+str(curcrs.prime_meridian.to_json()).replace("\"","'").replace("\n","")+"\" . \n")
			if curcrs.prime_meridian.remarks!=None:
				ttl.add("geocrsmeridian:"+curcrs.prime_meridian.name.replace(" ","")+" rdfs:comment \""+str(curcrs.prime_meridian.remarks)+"\"@en . \n")
			if curcrs.prime_meridian.scope!=None:
				ttl.add("geocrsmeridian:"+curcrs.prime_meridian.name.replace(" ","")+" geocrs:scope \""+str(curcrs.prime_meridian.scope)+"\"^^xsd:string . \n")				
	ttl.add("geoepsg:"+epsgcode+" geocrs:isVertical \""+str(curcrs.is_vertical).lower()+"\"^^xsd:boolean . \n")
	ttl.add("geoepsg:"+epsgcode+" geocrs:isProjected \""+str(curcrs.is_projected).lower()+"\"^^xsd:boolean . \n")
	ttl.add("geoepsg:"+epsgcode+" geocrs:isGeocentric \""+str(curcrs.is_geocentric).lower()+"\"^^xsd:boolean . \n")
	ttl.add("geoepsg:"+epsgcode+" geocrs:isGeographic \""+str(curcrs.is_geographic).lower()+"\"^^xsd:boolean . \n")
	if curcrs.utm_zone!=None:
		ttl.add("geoepsg:"+epsgcode+" geocrs:utm_zone \""+str(curcrs.utm_zone)+"\"^^xsd:string . \n")	
	if curcrs.to_proj4()!=None:
		ttl.add("geoepsg:"+epsgcode+" geocrs:asProj4 \""+curcrs.to_proj4().strip().replace("\"","'")+"\"^^xsd:string . \n")
	if curcrs.to_json()!=None:
		ttl.add("geoepsg:"+epsgcode+" geocrs:asProjJSON \""+curcrs.to_json().strip().replace("\"","'")+"\"^^xsd:string . \n")		
	if wkt!="":
		ttl.add("geoepsg:"+epsgcode+" geocrs:asWKT \""+wkt+"\"^^geocrs:wktLiteral . \n")
	ttl.add("geoepsg:"+epsgcode+" geocrs:epsgCode \"EPSG:"+epsgcode+"\"^^xsd:string . \n")		
	#i+=1

def parseSolarSystemSatellites(filename,ttlstring):
	with open(filename) as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			curname=row["Name"].replace(" ","_").replace("+","_").replace(":","_").replace("(","_").replace(")","_").replace("/","_").replace("*","_").replace("'","_").replace("~","_")
			if curname=="":
				continue
			ttlstring.add("geocrsisbody:"+curname+" rdf:type geocrs:Moon .\n")
			ttlstring.add("geocrsisbody:"+curname+" rdfs:label \""+str(row["Name"])+"\"@en .\n")
			if str(row["radius"])!="":
				ttlstring.add("geocrsisbody:"+curname+" geocrs:radius \""+str(row["radius"])+"\"^^xsd:double .\n")
			if str(row["orbital_period"])!="":
				ttlstring.add("geocrsgeod:"+curname+"_geoid geocrs:orbital_period \""+row["orbital_period"]+"\"^^xsd:double .\n")
			ttlstring.add("geocrsisbody:"+curname+" geocrs:planet_status geocrs:Confirmed .\n")
			ttlstring.add("geocrs:Confirmed rdf:type geocrs:PlanetStatus .\n")
			ttlstring.add("geocrs:Confirmed rdfs:label \"Confirmed\"@en .\n")
			ttlstring.add("geocrsgeod:"+curname+"_geoid rdf:type geocrs:Sphere .\n")
			ttlstring.add("geocrsgeod:"+curname+"_geoid rdfs:label \"Geoid for "+str(row["Name"])+"\"@en .\n")
			if str(row["semi_major_axis"])!="":
				ttlstring.add("geocrsgeod:"+curname+"_geoid geocrs:semiMajorAxis \""+row["semi_major_axis"]+"\"^^xsd:double .\n")
			ttlstring.add("geocrsgeod:"+curname+"_geoid geocrs:isApplicableTo geocrsisbody:"+curname+" .\n")
			if str(row["Parent"])!="":
				starname=row["Parent"].replace(" ","_").replace("+","_").replace(":","_").replace("(","_").replace(")","_").replace("/","_").replace("*","_").replace("'","_")
				if starname!="":
					ttlstring.add("geocrsisbody:"+starname+" rdf:type geocrs:Planet .\n")
					ttlstring.add("geocrsisbody:"+starname+" rdfs:label \""+str(row["Parent"])+"\"@en .\n")	
					ttlstring.add("geocrsisbody:"+curname+" geocrs:satelliteOf geocrsisbody:"+starname+" .\n")					


def parseAdditionalPlanetarySpheroids(filename,ttlstring):
	with open(filename) as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			curname=row["name"].replace(" ","_").replace("+","_").replace(":","_").replace("(","_").replace(")","_").replace("/","_").replace("*","_").replace("'","_")
			ttlstring.add("geocrsisbody:"+curname+" rdf:type geocrs:Planet .\n")
			ttlstring.add("geocrsisbody:"+curname+" rdfs:label \""+str(row["name"])+"\"@en .\n")
			if str(row["mass"])!="":
				ttlstring.add("geocrsisbody:"+curname+" geocrs:mass \""+str(row["mass"])+"\"^^xsd:double .\n")
			if str(row["orbital_period"])!="":
				ttlstring.add("geocrsisbody:"+curname+" geocrs:orbital_period \""+str(row["orbital_period"])+"\"^^xsd:double .\n")
			if str(row["radius"])!="":
				ttlstring.add("geocrsisbody:"+curname+" geocrs:radius \""+str(row["radius"])+"\"^^xsd:double .\n")
			ttlstring.add("geocrsisbody:"+curname+" geocrs:planet_status geocrs:"+str(row["planet_status"])+" .\n")
			ttlstring.add("geocrs:"+str(row["planet_status"])+" rdf:type geocrs:PlanetStatus .\n")
			ttlstring.add("geocrs:"+str(row["planet_status"])+" rdfs:label \""+row["planet_status"]+"\"@en .\n")
			ttlstring.add("geocrsgeod:"+curname+"_geoid rdf:type geocrs:Sphere .\n")
			ttlstring.add("geocrsgeod:"+curname+"_geoid rdfs:label \"Geoid for "+str(row["name"])+"\"@en .\n")
			if str(row["semi_major_axis"])!="":
				ttlstring.add("geocrsgeod:"+curname+"_geoid geocrs:semiMajorAxis \""+row["semi_major_axis"]+"\"^^xsd:double .\n")
			if str(row["eccentricity"])!="":
				ttlstring.add("geocrsgeod:"+curname+"_geoid geocrs:eccentricity \""+row["eccentricity"]+"\"^^xsd:double .\n")
			ttlstring.add("geocrsgeod:"+curname+"_geoid geocrs:approximates geocrsisbody:"+curname+" .\n")
			if str(row["star_name"])!="":
				starname=row["star_name"].replace(" ","_").replace("+","_").replace(":","_").replace("(","_").replace(")","_").replace("/","_").replace("*","_").replace("'","_")
				ttlstring.add("geocrsisbody:"+starname+" rdf:type geocrs:Star .\n")
				ttlstring.add("geocrsisbody:"+starname+" rdfs:label \""+str(row["star_name"])+"\"@en .\n")			
				if str(row["star_mass"])!="":
					ttlstring.add("geocrsisbody:"+starname+" geocrs:mass \""+row["star_mass"]+"\"^^xsd:double .\n")
				if str(row["star_radius"])!="":
					ttlstring.add("geocrsisbody:"+starname+" geocrs:radius \""+row["star_radius"]+"\"^^xsd:double .\n")
				ttlstring.add("geocrsisbody:"+curname+" geocrs:satelliteOf geocrsisbody:"+starname+" .\n")
				if str(row["star_distance"])!="":
					ttlstring.add("geocrsisbody:"+curname+" geocrs:starDistance \""+str(row["star_distance"])+"\"^^xsd:double .\n")
		return ttlstring


units={}
units["m"]="om:meter"
units["metre"]="om:metre"
units["grad"]="om:degree"
units["degree"]="om:degree"
units["ft"]="om:foot"
units["us-ft"]="om:usfoot"
scope={}
scope["geodesy"]="geocrs:Geodesy"
scope["topographic mapping"]="geocrs:TopographicMap"
scope["spatial referencing"]="geocrs:SpatialReferencing"
scope["engineering survey"]="geocrs:EngineeringSurvey"
scope["satellite survey"]="geocrs:SatelliteSurvey"
scope["satellite navigation"]="geocrs:SatelliteNvaigation"
scope["coastal hydrography"]="geocrs:CoastalHydrography"
scope["offshore engineering"]="geocrs:OffshoreEngineering"
scope["hydrography"]="geocrs:Hydrography"
scope["drilling"]="geocrs:Drilling"
scope["nautical charting"]="geocrs:NauticalChart"
scope["oil and gas exploration"]="geocrs:OilAndGasExploration"
scope["cadastre"]="geocrs:CadastreMap"
coordinatesystem={}
coordinatesystem["ellipsoidal"]="geocrs:EllipsoidalCS"
coordinatesystem["cartesian"]="geocrs:CartesianCS"
coordinatesystem["vertical"]="geocrs:VerticalCS"
coordinatesystem["ft"]="om:foot"
coordinatesystem["us-ft"]="om:usfoot"
spheroids={}
spheroids["GRS80"]="geocrsgeod:GRS1980"
spheroids["GRS 80"]="geocrsgeod:GRS1980"
spheroids["GRS67"]="geocrsgeod:GRS67"
spheroids["GRS 1967"]="geocrsgeod:GRS67"
spheroids["GRS 1967 Modified"]="geocrsgeod:GRS67Modified"
spheroids["GRS 67"]="geocrsgeod:GRS67"
spheroids["GRS1980"]="geocrsgeod:GRS1980"
spheroids["GRS 1980"]="geocrsgeod:GRS1980"
spheroids["NWL 9D"]="geocrsgeod:NWL9D"
spheroids["PZ-90"]="geocrsgeod:PZ90"
spheroids["Airy 1830"]="geocrsgeod:Airy1830"
spheroids["Airy Modified 1849"]="geocrsgeod:AiryModified1849"
spheroids["intl"]="geocrsgeod:International1924"
spheroids["aust_SA"]="geocrsgeod:AustralianNationalSpheroid"
spheroids["Australian National Spheroid"]="geocrsgeod:AustralianNationalSpheroid"
spheroids["International 1924"]="geocrsgeod:International1924"
spheroids["clrk"]="geocrsgeod:Clarke1866"
spheroids["War Office"]="geocrsgeod:WarOffice"
spheroids["evrst30"]="geocrsgeod:Everest1930"
spheroids["clrk66"]="geocrsgeod:Clarke1866"
spheroids["Plessis 1817"]="geocrsgeod:Plessis1817"
spheroids["Danish 1876"]="geocrsgeod:Danish1876"
spheroids["Struve 1860"]="geocrsgeod:Struve1860"
spheroids["IAG 1975"]="geocrsgeod:IAG1975"
spheroids["Clarke 1866"]="geocrsgeod:Clarke1866"
spheroids["Clarke 1858"]="geocrsgeod:Clarke1858"
spheroids["Clarke 1880"]="geocrsgeod:Clarke1880"
spheroids["Helmert 1906"]="geocrsgeod:Helmert1906"
spheroids["Moon_2000_IAU_IAG"]="geocrsgeod:Moon2000_IAU_IAG"
spheroids["CGCS2000"]="geocrsgeod:CGCS2000"
spheroids["GSK-2011"]="geocrsgeod:GSK2011"
spheroids["Zach 1812"]="geocrsgeod:Zach1812"
spheroids["Hough 1960"]="geocrsgeod:Hough1960"
spheroids["Hughes 1980"]="geocrsgeod:Hughes1980"
spheroids["Indonesian National Spheroid"]="geocrsgeod:IndonesianNationalSpheroid"
spheroids["clrk80"]="geocrsgeod:Clarke1880RGS"
spheroids["Clarke 1880 (Arc)"]="geocrsgeod:Clarke1880ARC"
spheroids["Clarke 1880 (RGS)"]="geocrsgeod:Clarke1880RGS"
spheroids["Clarke 1880 (IGN)"]="geocrsgeod:Clarke1880IGN"
spheroids["clrk80ign"]="geocrsgeod:Clarke1880IGN"
spheroids["WGS66"]="geocrsgeod:WGS66"
spheroids["WGS 66"]="geocrsgeod:WGS66"
spheroids["WGS72"]="geocrsgeod:WGS72"
spheroids["WGS 72"]="geocrsgeod:WGS72"
spheroids["WGS84"]="geocrsgeod:WGS84"
spheroids["WGS 84"]="geocrsgeod:WGS84"
spheroids["Krassowsky 1940"]="geocrsgeod:Krassowsky1940"
spheroids["krass"]="geocrsgeod:Krassowsky1940"
spheroids["Bessel 1841"]="geocrsgeod:Bessel1841"
spheroids["bessel"]="geocrsgeod:Bessel1841"
spheroids["Bessel Modified"]="geocrsgeod:BesselModified"
projections={}
projections["tmerc"]="geocrs:TransverseMercatorProjection"
projections["omerc"]="geocrs:ObliqueMercatorProjection"
projections["merc"]="geocrs:MercatorProjection"
projections["aeqd"]= "geocrs:AzimuthalEquidistantProjection"
projections["airy"]="geocrs:AiryProjection"
projections["aitoff"]="geocrs:AitoffProjection"
projections["apian"]="geocrs:ApianGlobularIProjection"
projections["august"]= "geocrs:AugustEpicycloidalProjection"
projections["bacon"]= "geocrs:BaconGlobularProjection"
projections["sinu"]="geocrs:SinusoidalProjection"
projections["rpoly"]="geocrs:RectangularPolyconicProjection"
projections["poly"]="geocrs:AmericanPolyconicProjection"
projections["eqdc"]="geocrs:EquidistantConicProjection"
projections["sterea"]="geocrs:ObliqueStereographicProjection"
projections["cea"]="geocrs:CylindricalEqualArea"
projections["guyou"]="geocrs:GuyouProjection"
projections["aea"]="geocrs:AlbersEqualAreaProjection"
projections["eqearth"]="geocrs:EqualEarthProjection"
projections["natearth"]="geocrs:NaturalEarthProjection"
projections["stere"]="geocrs:StereographicProjection"
projections["cass"]="geocrs:CassiniProjection"
projections["nell"]="geocrs:PseudoCylindricalProjection"
projections["eck1"]="geocrs:Eckert1Projection"
projections["eck2"]="geocrs:Eckert2Projection"
projections["eck3"]="geocrs:Eckert3Projection"
projections["eck4"]="geocrs:Eckert4Projection"
projections["eck5"]="geocrs:Eckert5Projection"
projections["eck6"]="geocrs:Eckert6Projection"
projections["eqc"]="geocrs:EquidistantCylindricalProjection"
projections["col_urban"]="geocrs:ColombiaUrbanProjection"
projections["lagrng"]="geocrs:LagrangeProjection"
projections["laea"]="geocrs:LambertAzimuthalEqualArea"
projections["leac"]="geocrs:LambertEqualAreaConic"
projections["labrd"]="geocrs:LabordeProjection"
projections["lcc"]="geocrs:LambertConformalConicProjection"
projections["gnom"]="geocrs:GnomonicProjection"
projections["ortho"]="geocrs:OrthographicProjection"
projections["bonne"]="geocrs:BonneProjection"
projections["moll"]="geocrs:MollweideProjection"
projections["mill"]="geocrs:MillerProjection"
projections["nicol"]="geocrs:NicolosiGlobularProjection"
projections["collg"]="geocrs:CollignonProjection"
projections["robin"]="geocrs:RobinsonProjection"
projections["loxim"]="geocrs:LoximuthalProjection"
projections["aitoff"]="geocrs:AitoffProjection"
projections["ortho"]="geocrs:OrthographicProjection"
projections["kav5"]="geocrs:PseudoCylindricalProjection"
projections["tcea"]="geocrs:CylindricalProjection"
projections["utm"]="geocrs:UniversalTransverseMercatorProjection"
projections["krovak"]="geocrs:Krovak"
projections["fahey"]="geocrs:FaheyProjection"
projections["hatano"]="geocrs:HatanoAsymmetricalEqualAreaProjection"
projections["geocent"]="geocrs:Geocentric"
projections["times"]="geocrs:TheTimesProjection"
projections["robin"]="geocrs:RobinsonProjection"
projections["latlong"]="geocrs:LatLonProjection"
projections["longlat"]="geocrs:LonLatProjection"
projections["vandg"]="geocrs:VanDerGrintenIProjection"
projections["vandg2"]="geocrs:VanDerGrintenIIProjection"
projections["vandg3"]="geocrs:VanDerGrintenIIIProjection"
projections["vandg4"]="geocrs:VanDerGrintenIVProjection"


"""
adams_hemi : Adams Hemisphere in a Square
adams_ws1 : Adams World in a Square I
adams_ws2 : Adams World in a Square II
affine : Affine transformation
alsk : Modified Stereographic of Alaska
axisswap : Axis ordering
bertin1953 : Bertin 1953
bipc : Bipolar conic of western hemisphere
boggs : Boggs Eumorphic
bonne : Bonne (Werner lat_1=90)
calcofi : Cal Coop Ocean Fish Invest Lines/Stations
cart : Geodetic/cartesian conversions
cc : Central Cylindrical
ccon : Central Conic
cea : Equal Area Cylindrical
chamb : Chamberlin Trimetric
col_urban : Colombia Urban
comill : Compact Miller
crast : Craster Parabolic (Putnins P4)
defmodel : Deformation model
deformation : Kinematic grid shift
denoy : Denoyer Semi-Elliptical
eqc : Equidistant Cylindrical (Plate Carree)
euler : Euler
etmerc : Extended Transverse Mercator
fouc : Foucaut
fouc_s : Foucaut Sinusoidal
gall : Gall (Gall Stereographic)
geoc : Geocentric Latitude
geogoffset : Geographic Offset
geos : Geostationary Satellite View
gins8 : Ginsburg VIII (TsNIIGAiK)
gn_sinu : General Sinusoidal Series
goode : Goode Homolosine
gs48 : Modified Stereographic of 48 U.S.
gs50 : Modified Stereographic of 50 U.S.
hammer : Hammer & Eckert-Greifendorff
healpix : HEALPix
rhealpix : rHEALPix
helmert : 3(6)-, 4(8)- and 7(14)-parameter Helmert shift
hgridshift : Horizontal grid shift
horner : Horner polynomial evaluation
igh : Interrupted Goode Homolosine
igh_o : Interrupted Goode Homolosine Oceanic View
imw_p : International Map of the World Polyconic
isea : Icosahedral Snyder Equal Area
kav5 : Kavrayskiy V
kav7 : Kavrayskiy VII
laea : Lambert Azimuthal Equal Area
larr : Larrivee
lask : Laskowski
lonlat : Lat/long (Geodetic)
latlon : Lat/long (Geodetic alias)
lcca : Lambert Conformal Conic Alternative
leac : Lambert Equal Area Conic
lee_os : Lee Oblated Stereographic
lsat : Space oblique for LANDSAT
mbt_s : McBryde-Thomas Flat-Polar Sine (No. 1)
mbt_fps : McBryde-Thomas Flat-Pole Sine (No. 2)
mbtfpp : McBride-Thomas Flat-Polar Parabolic
mbtfpq : McBryde-Thomas Flat-Polar Quartic
mbtfps : McBryde-Thomas Flat-Polar Sinusoidal
mil_os : Miller Oblated Stereographic
mill : Miller Cylindrical
misrsom : Space oblique for MISR
molobadekas : Molodensky-Badekas transformation
molodensky : Molodensky transform
murd1 : Murdoch I
murd2 : Murdoch II
murd3 : Murdoch III
natearth : Natural Earth
natearth2 : Natural Earth 2
nell : Nell
nell_h : Nell-Hammer
nsper : Near-sided perspective
nzmg : New Zealand Map Grid
noop : No operation
ob_tran : General Oblique Transformation
ocea : Oblique Cylindrical Equal Area
oea : Oblated Equal Area
omerc : Oblique Mercator
ortel : Ortelius Oval
pconic : Perspective Conic
patterson : Patterson Cylindrical
peirce_q : Peirce Quincuncial
pipeline : Transformation pipeline manager
poly : Polyconic (American)
pop : Retrieve coordinate value from pipeline stack
push : Save coordinate value on pipeline stack
putp1 : Putnins P1
putp2 : Putnins P2
putp3 : Putnins P3
putp3p : Putnins P3'
putp4p : Putnins P4'
putp5 : Putnins P5
putp5p : Putnins P5'
putp6 : Putnins P6
putp6p : Putnins P6'
qua_aut : Quartic Authalic
qsc : Quadrilateralized Spherical Cube
rouss : Roussilhe Stereographic
rpoly : Rectangular Polyconic
s2 : S2
sch : Spherical Cross-track Height
set : Set coordinate value
somerc : Swiss. Obl. Mercator
stere : Stereographic
sterea : Oblique Stereographic Alternative
gstmerc : Gauss-Schreiber Transverse Mercator (aka Gauss-Laborde Reunion)
tcc : Transverse Central Cylindrical
tcea : Transverse Cylindrical Equal Area
tinshift : Triangulation based transformation
tissot : Tissot
tobmerc : Tobler-Mercator
topocentric : Geocentric/Topocentric conversion
tpeqd : Two Point Equidistant
tpers : Tilted perspective
unitconvert : Unit conversion
ups : Universal Polar Stereographic
urm5 : Urmaev V
urmfps : Urmaev Flat-Polar Sinusoidal
utm : Universal Transverse Mercator (UTM)
vitk1 : Vitkovsky I
vgridshift : Vertical grid shift
wag1 : Wagner I (Kavrayskiy VI)
wag2 : Wagner II
wag3 : Wagner III
wag4 : Wagner IV
wag5 : Wagner V
wag6 : Wagner VI
wag7 : Wagner VII
webmerc : Web Mercator / Pseudo Mercator
weren : Werenskiold I
wink1 : Winkel I
wink2 : Winkel II
wintri : Winkel Tripel
xyzgridshift : Geocentric grid shift
"""
#projections["cc"]="geocrs:CylindricalProjection"
ttl=set()
ttlnoniso=set()
ttldata=set()
ttlprojectionvocab=set()
planetvocab=set()
srsapplication=set()
csvocab=set()
ttlhead="@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"
ttlhead+="@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
ttlhead+="@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
ttlhead+="@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n"
ttlhead+="@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n"
ttlhead+="@prefix prov: <http://www.w3.org/ns/prov-o/> .\n"
ttlhead+="@prefix geoepsg: <http://www.opengis.net/def/crs/EPSG/0/> .\n"
ttlhead+="@prefix geo: <http://www.opengis.net/ont/geosparql#> .\n"
ttlhead+="@prefix geocrs: <http://www.opengis.net/ont/crs/> .\n"
ttlhead+="@prefix geocrsdatum: <http://www.opengis.net/ont/crs/datum/> .\n"
ttlhead+="@prefix geocrsisbody: <http://www.opengis.net/ont/crs/isbody/> .\n"
ttlhead+="@prefix geocrsgrid: <http://www.opengis.net/ont/crs/grid/> .\n"
ttlhead+="@prefix geocrsproj: <http://www.opengis.net/ont/crs/proj/> .\n"
ttlhead+="@prefix geocrsaxis: <http://www.opengis.net/ont/crs/cs/axis/> .\n"
ttlhead+="@prefix geocrsgeod: <http://www.opengis.net/ont/crs/geod/> .\n"
ttlhead+="@prefix geocrsaou: <http://www.opengis.net/ont/crs/areaofuse/> .\n"
ttlhead+="@prefix geocrsmeridian: <http://www.opengis.net/ont/crs/primeMeridian/> .\n"
ttlhead+="@prefix geocrsoperation: <http://www.opengis.net/ont/crs/operation/> .\n"
ttlhead+="@prefix geocs: <http://www.opengis.net/ont/crs/cs/> .\n"
ttlhead+="@prefix dc: <http://purl.org/dc/elements/1.1/> .\n"
ttlhead+="@prefix wd: <http://www.wikidata.org/entity/> .\n"
ttlhead+="@prefix om: <http://www.ontology-of-units-of-measure.org/resource/om-2/> .\n"
ttl.add("geocrs:GeoSPARQLSRS rdf:type owl:Ontology .\n")
ttl.add("geocrs:GeoSPARQLSRS dc:creator wd:Q67624599 .\n")
ttl.add("geocrs:GeoSPARQLSRS dc:description \"This ontology models spatial reference systems\"@en .\n")
ttl.add("geocrs:GeoSPARQLSRS rdfs:label \"GeoSPARQL SRS Ontology Draft\"@en .\n")
ttl.add("owl:versionInfo rdfs:label \"0.1\"^^xsd:double .\n")
ttl.add("prov:Entity rdf:type owl:Class .\n")
ttl.add("prov:Entity rdfs:label \"entity\"@en .\n")
srsapplication.add("geocrs:SRSApplicationOntology rdf:type owl:Ontology .\n")
srsapplication.add("geocrs:SRSApplicationOntology rdfs:label \"SRS Application Ontology\" .\n")
srsapplication.add("geocrs:SRSApplication rdf:type owl:Class .\n")
srsapplication.add("geocrs:SRSApplication rdfs:label \"srs application\"@en .\n")
srsapplication.add("geocrs:SRSApplication skos:definition \"an application for which a spatial reference system is used\"@en .\n")
srsapplication.add("geocrs:GeneralReferenceMap rdf:type owl:Class .\n")
srsapplication.add("geocrs:GeneralReferenceMap rdfs:label \"general reference map\"@en .\n")
srsapplication.add("geocrs:GeneralReferenceMap skos:definition \"general reference map which includes a variety of different information\"@en .\n")
srsapplication.add("geocrs:GeneralReferenceMap rdfs:subClassOf geocrs:SRSApplication .\n")
srsapplication.add("geocrs:NauticalChart rdf:type owl:Class .\n")
srsapplication.add("geocrs:NauticalChart rdfs:label \"nautical chart\"@en .\n")
srsapplication.add("geocrs:NauticalChart skos:definition \"A nautical chart is a graphic representation of a sea area and adjacent coastal regions.\"@en .\n")
srsapplication.add("geocrs:NauticalChart rdfs:subClassOf geocrs:SRSApplication .\n")
srsapplication.add("geocrs:NauticalChart geocrs:uses geocrs:ConformalProjection .\n")
srsapplication.add("geocrs:TopographicMap rdf:type owl:Class .\n")
srsapplication.add("geocrs:TopographicMap rdfs:label \"topographic map\"@en .\n")
srsapplication.add("geocrs:TopographicMap geocrs:uses geocrs:ConformalProjection .\n")
srsapplication.add("geocrs:TopographicMap skos:definition \"A type of map characterized by large-scale detail and quantitative representation of relief.\"@en .\n")
srsapplication.add("geocrs:TopographicMap rdfs:subClassOf geocrs:SRSApplication .\n")
srsapplication.add("geocrs:ThematicMap rdf:type owl:Class .\n")
srsapplication.add("geocrs:ThematicMap rdfs:label \"thematic map\"@en .\n")
srsapplication.add("geocrs:ThematicMap skos:definition \"A map used to highlight a specific phenomenon\"@en .\n")
srsapplication.add("geocrs:ThematicMap rdfs:subClassOf geocrs:SRSApplication .\n")
srsapplication.add("geocrs:CadastreMap rdf:type owl:Class .\n")
srsapplication.add("geocrs:CadastreMap rdfs:label \"cadastre map\"@en .\n")
srsapplication.add("geocrs:CadastreMap skos:definition \"A map displaying a cadastre\"@en .\n")
srsapplication.add("geocrs:CadastreMap rdfs:subClassOf geocrs:SRSApplication .\n")
srsapplication.add("geocrs:ChloroplethMap rdf:type owl:Class .\n")
srsapplication.add("geocrs:ChloroplethMap rdfs:label \"chloropleth map\"@en .\n")
srsapplication.add("geocrs:ChloroplethMap skos:definition \"A thematic map in which is a set of pre-defined areas is colored in proportion to a statistical variable \"@en .\n")
srsapplication.add("geocrs:ChloroplethMap rdfs:subClassOf geocrs:ThematicMap .\n")
srsapplication.add("geocrs:ChloroplethMap geocrs:uses geocrs:EqualAreaProjection .\n")
srsapplication.add("geocrs:HeatMap rdf:type owl:Class .\n")
srsapplication.add("geocrs:HeatMap rdfs:label \"heat map\"@en .\n")
srsapplication.add("geocrs:HeatMap skos:definition \"A data visualization technique that shows magnitude of a phenomenon as color in two dimensions.\"@en .\n")
srsapplication.add("geocrs:HeatMap rdfs:subClassOf geocrs:ThematicMap .\n")
srsapplication.add("geocrs:HeatMap owl:disjointWith geocrs:ChloroplethMap .\n")
srsapplication.add("geocrs:WeatherMap rdf:type owl:Class .\n")
srsapplication.add("geocrs:WeatherMap rdfs:label \"weather map\"@en .\n")
srsapplication.add("geocrs:WeatherMap geocrs:uses geocrs:ConformalProjection .\n")
srsapplication.add("geocrs:WeatherMap skos:definition \"A map for showing the local direction in which weather systems are moving.\"@en .\n")
srsapplication.add("geocrs:WeatherMap rdfs:subClassOf geocrs:ThematicMap .\n")
ttl.add("geocrs:ReferenceSystem rdf:type owl:Class .\n")
ttl.add("geocrs:ReferenceSystem rdfs:label \"reference system\"@en .\n")
ttl.add("geocrs:ReferenceSystem skos:definition \"a system that uses a reference to establish a position\"@en .\n")
ttl.add("geocrs:LinearReferenceSystem rdf:type owl:Class .\n")
ttl.add("geocrs:LinearReferenceSystem rdfs:subClassOf geocrs:SpatialReferenceSystem .\n")
ttl.add("geocrs:LinearReferenceSystem rdfs:label \"linear reference system\"@en .\n")
ttl.add("geocrs:LinearReferenceSystem skos:definition \"a reference system in which the locations of physical features along a linear element are described in terms of measurements from a fixed point\"@en .\n")
ttl.add("geocrs:GeocodeSystem rdf:type owl:Class .\n")
ttl.add("geocrs:GeocodeSystem rdfs:subClassOf geocrs:SpatialReferenceSystem .\n")
ttl.add("geocrs:GeocodeSystem rdfs:label \"geocode system\"@en .\n")
ttl.add("geocrs:GeocodeSystem skos:definition \"a system that uses a geocode to encode a position\"@en .\n")
ttl.add("geocrs:TemporalReferenceSystem rdf:type owl:Class .\n")
ttl.add("geocrs:TemporalReferenceSystem rdfs:label \"temporal reference system\"@en .\n")
ttl.add("geocrs:TemporalReferenceSystem skos:definition \"Reference system against which time is measured\"@en .\n")
ttl.add("geocrs:TemporalReferenceSystem rdfs:subClassOf geocrs:ReferenceSystem .\n")
ttlnoniso.add("geocrs:SpatialReferenceSystem rdf:type owl:Class .\n")
ttlnoniso.add("geocrs:SpatialReferenceSystem rdfs:label \"spatial reference system\"@en .\n")
ttlnoniso.add("geocrs:SpatialReferenceSystem skos:definition \"System for identifying position in the real world\"@en .\n")
ttlnoniso.add("geocrs:SpatialReferenceSystem rdfs:subClassOf geocrs:ReferenceSystem .\n")
ttlnoniso.add("geocrs:UnknownSpatialReferenceSystem rdf:type owl:Class .\n")
ttlnoniso.add("geocrs:UnknownSpatialReferenceSystem rdfs:label \"unknown spatial reference system\"@en .\n")
ttlnoniso.add("geocrs:UnknownSpatialReferenceSystem skos:definition \"A spatial reference system which definition is not known\"@en .\n")
ttlnoniso.add("geocrs:UnknownSpatialReferenceSystem rdfs:subClassOf geocrs:SpatialReferenceSystem .\n")
ttl.add("geocrs:CoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:CoordinateSystem rdfs:label \"coordinate system\"@en .\n")
ttl.add("geocrs:CoordinateSystem skos:definition \"non-repeating sequence of coordinate system axes that spans a given coordinate space\"@en .\n")
ttl.add("geocrs:CoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
csvocab.add("geocrs:PlanarCS rdf:type owl:Class .\n")
csvocab.add("geocrs:PlanarCS rdfs:label \"planar coordinate system\"@en .\n")
csvocab.add("geocrs:PlanarCS rdfs:subClassOf geocrs:CoordinateSystem .\n")
csvocab.add("geocrs:PlanarCS skos:definition \"A two-dimensional measurement system that locates features on a plane based on their distance from an origin (0,0) along two perpendicular axes\"@en .\n")
csvocab.add("geocrs:3DCS rdf:type owl:Class .\n")
csvocab.add("geocrs:3DCS rdfs:label \"3D coordinate system\"@en .\n")
csvocab.add("geocrs:3DCS rdfs:subClassOf geocrs:CoordinateSystem .\n")
csvocab.add("geocrs:3DCS skos:definition \"non-repeating sequence of coordinate system axes that spans a given coordinate space in three dimensions\"@en .\n")
csvocab.add("geocrs:1DCS rdf:type owl:Class .\n")
csvocab.add("geocrs:1DCS rdfs:label \"1D coordinate system\"@en .\n")
csvocab.add("geocrs:1DCS rdfs:subClassOf geocrs:CoordinateSystem .\n")
csvocab.add("geocrs:1DCS skos:definition \"non-repeating sequence of coordinate system axes that spans a given coordinate space in one dimension\"@en .\n")
ttl.add("geocrs:StereographicCS rdf:type owl:Class .\n")
ttl.add("geocrs:StereographicCS rdfs:label \"stereographic coordinate system\"@en .\n")
ttl.add("geocrs:StereographicCS rdfs:subClassOf geocrs:CoordinateSystem .\n")
ttl.add("geocrs:CoordinateSystemAxis rdf:type owl:Class .\n")
ttl.add("geocrs:CoordinateSystemAxis rdfs:label \"coordinate system axis\"@en .\n")
ttl.add("geocrs:CoordinateSystemAxis skos:definition \"Axis defined by a coordinate system\"@en .\n")
ttl.add("geocrs:CoordinateSystemAxis rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:TemporalCoordinateSystemAxis rdf:type owl:Class .\n")
ttl.add("geocrs:TemporalCoordinateSystemAxis rdfs:subClassOf geocrs:CoordinateSystemAxis .\n")
ttl.add("geocrs:TemporalCoordinateSystemAxis skos:definition \"Axis defined by a temporal coordinate system\"@en .\n")
ttl.add("geocrs:TemporalCoordinateSystemAxis rdfs:label \"temporal coordinate system axis\"@en .\n")
ttl.add("geocrs:TemporalCoordinateSystemAxis rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:AreaOfUse rdf:type owl:Class .\n")
ttl.add("geocrs:AreaOfUse rdfs:label \"area of use\"@en .\n")
ttl.add("geocrs:AreaOfUse skos:definition \"area in which a coordinate operation may be used\"@en .\n")
ttl.add("geocrs:CartesianCS rdf:type owl:Class .\n")
ttl.add("geocrs:CartesianCS rdfs:subClassOf geocrs:AffineCS, geocrs:OrthogonalCS .\n")
ttl.add("geocrs:CartesianCS rdfs:label \"cartesian coordinate system\"@en .\n")
ttl.add("geocrs:CartesianCS skos:definition \"coordinate system in Euclidean space which gives the position of points relative to n mutually perpendicular straight axes all having the same unit of measure\"@en .\n")
ttl.add("geocrs:CartesianCS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:LinearCS rdf:type owl:Class .\n")
ttl.add("geocrs:LinearCS rdfs:subClassOf geocrs:1DCS .\n")
ttl.add("geocrs:LinearCS rdfs:label \"linear coordinate system\"@en .\n")
ttl.add("geocrs:LinearCS skos:definition \"one-dimensional coordinate system in which a linear feature forms the axis\"@en .\n")
ttl.add("geocrs:LinearCS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:GridCS rdf:type owl:Class .\n")
ttl.add("geocrs:GridCS rdfs:subClassOf geocrs:CS .\n")
ttl.add("geocrs:GridCS rdfs:label \"grid coordinate system\"@en .\n")
ttl.add("geocrs:GridCS skos:definition \"A grid coordinate system describes areas with a grid\"@en .\n")
csvocab.add("geocrs:CSExtensionOntology rdf:type owl:Ontology .\n")
csvocab.add("geocrs:CSExtensionOntology rdfs:label \"CS Extension Ontology\" .\n")
csvocab.add("geocrs:HexagonalCS rdf:type owl:Class .\n")
csvocab.add("geocrs:HexagonalCS rdfs:subClassOf geocrs:GridCS .\n")
csvocab.add("geocrs:HexagonalCS rdfs:label \"hexagonal coordinate system\"@en .\n")
csvocab.add("geocrs:HexagonalCS skos:definition \"A hexagonal coordinate system describes areas with a hexagonal lattice\"@en .\n")
ttl.add("geocrs:ObliqueCS rdf:type owl:Class .\n")
ttl.add("geocrs:ObliqueCS rdfs:subClassOf geocrs:AffineCS .\n")
ttl.add("geocrs:ObliqueCS rdfs:label \"oblique coordinate system\"@en .\n")
ttl.add("geocrs:ObliqueCS skos:definition \"A plane coordinate system whose axes are not perpendicular\"@en .\n")
planetvocab.add("geocrs:PlanetOntology rdf:type owl:Ontology .\n")
planetvocab.add("geocrs:PlanetOntology rdfs:label \"Planet Ontology\" .\n")
planetvocab.add("geocrs:CelestialCS rdf:type owl:Class .\n")
planetvocab.add("geocrs:CelestialCS rdfs:subClassOf geocrs:CS .\n")
planetvocab.add("geocrs:CelestialCS rdfs:label \"celestial coordinate system\"@en .\n")
planetvocab.add("geocrs:CelestialCS skos:definition \"a coordinate system for specifying positions of celestial objects relative to physical reference points\"@en .\n")
ttl.add("geocrs:EngineeringCS rdf:type owl:Class .\n")
ttl.add("geocrs:EngineeringCS rdfs:subClassOf geocrs:CS .\n")
ttl.add("geocrs:EngineeringCS rdfs:label \"engineering coordinate system\"@en .\n")
ttl.add("geocrs:EngineeringCS skos:definition \"coordinate system used by an engineering coordinate reference system, one of an affine coordinate system, a Cartesian coordinate system, a cylindrical coordinate system, a linear coordinate sytem, an ordinal coordinate system, a polar coordinate system or a spherical coordinate system\"@en .\n")
ttl.add("geocrs:EngineeringCS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:GeodeticCS rdf:type owl:Class .\n")
ttl.add("geocrs:GeodeticCS owl:disjointWith geocrs:CompoundCRS .\n")
ttl.add("geocrs:GeodeticCS rdfs:subClassOf geocrs:CS .\n")
ttl.add("geocrs:GeodeticCS rdfs:label \"geodetic coordinate system\"@en .\n")
ttl.add("geocrs:GeodeticCS skos:definition \"coordinate system used by a Geodetic CRS, one of a Cartesian coordinate system or a spherical coordinate system\"@en .\n")
ttl.add("geocrs:GeodeticCS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:EllipsoidalCS rdf:type owl:Class .\n")
ttl.add("geocrs:EllipsoidalCS rdfs:subClassOf geocrs:OrthogonalCS .\n")
ttl.add("geocrs:EllipsoidalCS rdfs:label \"ellipsoidal coordinate system\"@en .\n")
ttl.add("geocrs:EllipsoidalCS skos:definition \"two- or three-dimensional coordinate system in which position is specified by geodetic latitude, geodetic longitude, and (in the three-dimensional case) ellipsoidal height\"@en .\n")
ttl.add("geocrs:EllipsoidalCS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:HorizontalCS rdf:type owl:Class .\n")
ttl.add("geocrs:HorizontalCS rdfs:subClassOf geocrs:CelestialCS .\n")
ttl.add("geocrs:HorizontalCS rdfs:label \"horizontal coordinate system\"@en .\n")
ttl.add("geocrs:HorizontalCS skos:definition \"A horizontal coordinate system is a celestial coordinate system that uses the observer's local horizon as the fundamental plane\"@en .\n")
planetvocab.add("geocrs:EquatorialCS rdf:type owl:Class .\n")
planetvocab.add("geocrs:EquatorialCS rdfs:subClassOf geocrs:CelestialCS .\n")
planetvocab.add("geocrs:EquatorialCS rdfs:label \"equatorial coordinate system\"@en .\n")
planetvocab.add("geocrs:EquatorialCS skos:definition \"A celestial coordinate system in which an object's position on the celestial sphere is described in terms of its north-south declination and east-west right ascension, measured relative to the celestial equator and vernal equinox, respectively\"@en .\n")
planetvocab.add("geocrs:EclipticCS rdf:type owl:Class .\n")
planetvocab.add("geocrs:EclipticCS rdfs:subClassOf geocrs:CelestialCS .\n")
planetvocab.add("geocrs:EclipticCS rdfs:label \"ecliptic coordinate system\"@en .\n")
planetvocab.add("geocrs:EclipticCS skos:definition \"An ecliptic coordinate system is used for representing the apparent positions and orbits of solar system objects.\"@en .\n")
planetvocab.add("geocrs:SuperGalacticCS rdf:type owl:Class .\n")
planetvocab.add("geocrs:SuperGalacticCS rdfs:subClassOf geocrs:CelestialCS, geocrs:3DCS .\n")
planetvocab.add("geocrs:SuperGalacticCS rdfs:label \"super galactic coordinate system\"@en .\n")
planetvocab.add("geocrs:GalacticCS rdf:type owl:Class .\n")
planetvocab.add("geocrs:GalacticCS rdfs:subClassOf geocrs:CelestialCoordinateSystem, geocrs:3DCS .\n")
planetvocab.add("geocrs:GalacticCS rdfs:label \"galactic coordinate system\"@en .\n")
ttl.add("geocrs:GeographicCS rdf:type owl:Class .\n")
ttl.add("geocrs:GeographicCoordinateSystem rdfs:subClassOf geocrs:CS .\n")
ttl.add("geocrs:GeographicCS rdfs:label \"geographic coordinate system\"@en .\n")
csvocab.add("geocrs:PerifocalCS rdf:type owl:Class .\n")
csvocab.add("geocrs:PerifocalCoordinateSystem rdfs:subClassOf geocrs:CS .\n")
csvocab.add("geocrs:PerifocalCS rdfs:label \"perifocal coordinate system\"@en .\n")
ttl.add("geocrs:OrdinalCS rdf:type owl:Class .\n")
ttl.add("geocrs:OrdinalCoordinateSystem rdfs:subClassOf geocrs:CS .\n")
ttl.add("geocrs:OrdinalCS rdfs:label \"ordinal coordinate system\"@en .\n")
ttl.add("geocrs:OrdinalCS skos:definition \"n-dimensional coordinate system in which every axis uses integers\"@en .\n")
ttl.add("geocrs:OrdinalCS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:ProjectedCS rdf:type owl:Class .\n")
ttl.add("geocrs:ProjectedCoordinateSystem rdfs:subClassOf geocrs:PlanarCS .\n")
ttl.add("geocrs:ProjectedCS rdfs:label \"projected coordinate system\"@en .\n")
ttl.add("geocrs:DerivedProjectedCS rdf:type owl:Class .\n")
ttl.add("geocrs:DerivedProjectedCoordinateSystem  rdfs:subClassOf geocrs:CoordinateSystem .\n")
ttl.add("geocrs:DerivedProjectedCoordinateSystem  rdfs:label \"derived projected coordinate system\"@en .\n")
ttl.add("geocrs:DerivedProjectedCoordinateSystem  skos:definition \"coordinate system used by a DerivedProjected CRS, one of an affine coordinate system, a Cartesian coordinate system, a cylindrical coordinate system, an ordinal coordinate system, a polar coordinate system or a spherical coordinate system\"@en .\n")
ttl.add("geocrs:DerivedProjectedCoordinateSystem  rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:SphericalCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:SphericalCoordinateSystem rdfs:subClassOf geocrs:3DCoordinateSystem .\n")
ttl.add("geocrs:SphericalCoordinateSystem rdfs:label \"spherical coordinate system\"@en .\n")
ttl.add("geocrs:SphericalCoordinateSystem skos:definition \"three-dimensional coordinate system in Euclidean space with one distance measured from the origin and two angular coordinates\"@en .\n")
ttl.add("geocrs:SphericalCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:CylindricalCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:CylindricalCoordinateSystem rdfs:subClassOf geocrs:3DCoordinateSystem .\n")
ttl.add("geocrs:CylindricalCoordinateSystem rdfs:label \"cylindrical coordinate system\"@en .\n")
ttl.add("geocrs:CylindricalCoordinateSystem skos:definition \"three-dimensional coordinate system in Euclidean space in which position is specified by two linear coordinates and one angular coordinate\"@en .\n")
ttl.add("geocrs:CylindricalCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:CurvilinearCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:CurvilinearCoordinateSystem rdfs:subClassOf geocrs:CoordinateSystem .\n")
ttl.add("geocrs:CurvilinearCoordinateSystem rdfs:label \"curvilinear coordinate system\"@en .\n")
ttl.add("geocrs:CurvilinearCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
csvocab.add("geocrs:SkewCoordinateSystem rdf:type owl:Class .\n")
csvocab.add("geocrs:SkewCoordinateSystem rdfs:subClassOf geocrs:CurvilinearCoordinateSystem .\n")
csvocab.add("geocrs:SkewCoordinateSystem rdfs:label \"skew coordinate system\"@en .\n")
csvocab.add("geocrs:SkewCoordinateSystem skos:definition \"A skew coordinate system is a system of curvilinear coordinates in which each family of surfaces intersects the others at angles other than right angles\"@en .\n")
csvocab.add("geocrs:OrthogonalCoordinateSystem rdf:type owl:Class .\n")
csvocab.add("geocrs:OrthogonalCoordinateSystem rdfs:subClassOf geocrs:CurvilinearCoordinateSystem .\n")
csvocab.add("geocrs:OrthogonalCoordinateSystem rdfs:label \"orthogonal coordinate system\"@en .\n")
csvocab.add("geocrs:OrthogonalCoordinateSystem skos:definition \"An orthogonal coordinate system is a system of curvilinear coordinates in which each family of surfaces intersects the others at right angles\"@en .\n")
csvocab.add("geocrs:ConicalCoordinateSystem rdf:type owl:Class .\n")
csvocab.add("geocrs:ConicalCoordinateSystem rdfs:subClassOf geocrs:OrthogonalCoordinateSystem, geocrs:3DCoordinateSystem .\n")
csvocab.add("geocrs:ConicalCoordinateSystem rdfs:label \"conical coordinate system\"@en .\n")
csvocab.add("geocrs:ConicalCoordinateSystem skos:definition \"An conical coordinate system is a three-dimensional orthogonal coordinate system consisting of concentric spheres (described by their radius r) and by two families of perpendicular cones, aligned along the z- and x-axes, respectively\"@en .\n")
csvocab.add("geocrs:HomogeneousCoordinateSystem rdf:type owl:Class .\n")
csvocab.add("geocrs:HomogeneousCoordinateSystem rdfs:subClassOf geocrs:CoordinateSystem .\n")
csvocab.add("geocrs:HomogeneousCoordinateSystem rdfs:label \"homogeneous coordinate system\"@en .\n")
planetvocab.add("geocrs:BarycentricCoordinateSystem rdf:type owl:Class .\n")
planetvocab.add("geocrs:BarycentricCoordinateSystem rdfs:subClassOf geocrs:CoordinateSystem .\n")
planetvocab.add("geocrs:BarycentricCoordinateSystem rdfs:label \"barycentric coordinate system\"@en .\n")
planetvocab.add("geocrs:BarycentricCoordinateSystem skos:definition \"a coordinate system in which the location of a point is specified by reference to a simplex \"@en .\n")
planetvocab.add("geocrs:BarycentricCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:PolarCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:PolarCoordinateSystem rdfs:subClassOf geocrs:OrthogonalCoordinateSystem, geocrs:PlanarCoordinateSystem .\n")
ttl.add("geocrs:PolarCoordinateSystem rdfs:label \"polar coordinate system\"@en .\n")
ttl.add("geocrs:PolarCoordinateSystem skos:definition \"two-dimensional coordinate system in Euclidean space in which position is specified by one distance coordinate and one angular coordinate\"@en .\n")
ttl.add("geocrs:PolarCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:ParametricCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:ParametricCoordinateSystem rdfs:subClassOf geocrs:1DCoordinateSystem .\n")
ttl.add("geocrs:ParametricCoordinateSystem rdfs:label \"parametric coordinate system\"@en .\n")
ttl.add("geocrs:ParametricCoordinateSystem skos:definition \"one-dimensional coordinate system where the axis units are parameter values which are not inherently spatial\"@en .\n")
ttl.add("geocrs:ParametricCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:VerticalCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:VerticalCoordinateSystem rdfs:subClassOf geocrs:1DCoordinateSystem .\n")
ttl.add("geocrs:VerticalCoordinateSystem rdfs:label \"vertical coordinate system\"@en .\n")
ttl.add("geocrs:VerticalCoordinateSystem skos:definition \"one-dimensional coordinate system used to record the heights or depths of points, usually dependent on the Earth's gravity field\"@en .\n")
ttl.add("geocrs:VerticalCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:TemporalCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:TemporalCoordinateSystem rdfs:subClassOf geocrs:1DCoordinateSystem .\n")
ttl.add("geocrs:TemporalCoordinateSystem rdfs:label \"temporal coordinate system\"@en .\n")
ttl.add("geocrs:TemporalCoordinateSystem skos:definition \"one-dimensionalcoordinate system where the axis is time\"@en .\n")
ttl.add("geocrs:TemporalCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DateTimeTemporalCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:DateTimeTemporalCoordinateSystem rdfs:subClassOf geocrs:TemporalCoordinateSystem .\n")
ttl.add("geocrs:DateTimeTemporalCoordinateSystem rdfs:label \"date time temporal coordinate system\"@en .\n")
ttl.add("geocrs:DateTimeTemporalCoordinateSystem skos:definition \"one-dimensional coordinate system used to record time in dateTime representation as defined in ISO 8601.\"@en .\n")
ttl.add("geocrs:DateTimeTemporalCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:TemporalCountCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:TemporalCountCoordinateSystem rdfs:subClassOf geocrs:TemporalCoordinateSystem .\n")
ttl.add("geocrs:TemporalCountCoordinateSystem rdfs:label \"temporal count coordinate system\"@en .\n")
ttl.add("geocrs:TemporalCountCoordinateSystem skos:definition \"one-dimensional coordinate system used to record time as an integer count\"@en .\n")
ttl.add("geocrs:TemporalCountCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:TemporalMeasureCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:TemporalMeasureCoordinateSystem rdfs:subClassOf geocrs:TemporalCoordinateSystem .\n")
ttl.add("geocrs:TemporalMeasureCoordinateSystem rdfs:label \"temporal measure coordinate system\"@en .\n")
ttl.add("geocrs:TemporalMeasureCoordinateSystem skos:definition \"one-dimensional coordinate system used to record a time as a real number\"@en .\n")
ttl.add("geocrs:TemporalMeasureCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:CRS rdf:type owl:Class .\n")
ttl.add("geocrs:CRS rdfs:label \"coordinate reference system\"@en .\n")
ttl.add("geocrs:CRS rdfs:subClassOf geocrs:SpatialReferenceSystem .\n")
ttl.add("geocrs:CRS skos:definition \"coordinate system that is related to an object by a datum\"@en .\n")
ttl.add("geocrs:CRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:AreaCode rdf:type owl:Class .\n")
ttl.add("geocrs:AreaCode rdfs:label \"area code\"@en .\n")
ttl.add("geocrs:AreaCode rdfs:subClassOf geocrs:LocalGridReferenceSystem .\n")
ttl.add("geocrs:AreaCode skos:definition \"a code which describes a certain area for a specific semantic purpose\"@en .\n")
ttl.add("geocrs:AreaCode skos:example \"ISO country code\"@en .\n")
ttl.add("geocrs:AreaCode rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:AdministrativeCode rdf:type owl:Class .\n")
ttl.add("geocrs:AdministrativeCode rdfs:subClassOf geocrs:AreaCode .\n")
ttl.add("geocrs:AdministrativeCode rdfs:label \"administrative code\"@en .\n")
ttl.add("geocrs:AdministrativeCode rdfs:subClassOf geocrs:GeocodeSystem .\n")
ttl.add("geocrs:AdministrativeCode skos:definition \"a code which describes an administrative area\"@en .\n")
ttl.add("geocrs:AdministrativeCode rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:GridReferenceSystem rdf:type owl:Class .\n")
ttl.add("geocrs:GridReferenceSystem rdfs:label \"grid reference system\"@en .\n")
ttl.add("geocrs:GridReferenceSystem rdfs:subClassOf geocrs:GeocodeSystem .\n")
ttl.add("geocrs:GridReferenceSystem skos:definition \"a grid that divides space with precise positions relative to a datum\"@en .\n")
ttl.add("geocrs:GridReferenceSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:HierarchicalGridReferenceSystem rdf:type owl:Class .\n")
ttl.add("geocrs:HierarchicalGridReferenceSystem rdfs:label \"hierarchical grid reference system\"@en .\n")
ttl.add("geocrs:HierarchicalGridReferenceSystem rdfs:subClassOf geocrs:GeocodeSystem .\n")
ttl.add("geocrs:HierarchicalGridReferenceSystem skos:definition \"a grid that divides space with precise positions relative to a datum\"@en .\n")
ttl.add("geocrs:HierarchicalGridReferenceSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:GlobalGridReferenceSystem rdf:type owl:Class .\n")
ttl.add("geocrs:GlobalGridReferenceSystem rdfs:label \"global grid reference system\"@en .\n")
ttl.add("geocrs:GlobalGridReferenceSystem rdfs:subClassOf geocrs:GridReferenceSystem .\n")
ttl.add("geocrs:GlobalGridReferenceSystem skos:definition \"a grid that divides space with precise positions relative to a datum and is valid on the whole earth\"@en .\n")
ttl.add("geocrs:GlobalGridReferenceSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:LocalGridReferenceSystem rdf:type owl:Class .\n")
ttl.add("geocrs:LocalGridReferenceSystem rdfs:label \"local grid reference system\"@en .\n")
ttl.add("geocrs:LocalGridReferenceSystem rdfs:subClassOf geocrs:GridReferenceSystem .\n")
ttl.add("geocrs:LocalGridReferenceSystem skos:definition \"a grid that divides space with precise positions relative to a datum and is valid on a part of the earth\"@en .\n")
ttl.add("geocrs:LocalGridReferenceSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:LocalCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:LocalCoordinateSystem rdfs:label \"local coordinate system\"@en .\n")
ttl.add("geocrs:LocalCoordinateSystem rdfs:subClassOf geocrs:CoordinateSystem .\n")
ttl.add("geocrs:LocalCoordinateSystem skos:definition \"coordinate system with a point of local reference\"@en .\n")
ttlnoniso.add("geocrs:SpatialIndex rdf:type owl:Class .\n")
ttlnoniso.add("geocrs:SpatialIndex rdfs:label \"spatial index\"@en .\n")
ttlnoniso.add("geocrs:SpatialIndex rdfs:subClassOf geocrs:GridReferenceSystem .\n")
ttlnoniso.add("geocrs:SpatialIndex skos:definition \"a grid that divides space with precise positions relative to a datum and acts as a spatial index\"@en .\n")
ttlnoniso.add("geocrs:SpatialIndex rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:SingleCRS rdf:type owl:Class .\n")
ttl.add("geocrs:SingleCRS rdfs:label \"single coordinate reference system\"@en .\n")
ttl.add("geocrs:SingleCRS rdfs:subClassOf geocrs:CRS .\n")
ttl.add("geocrs:SingleCRS skos:definition \"coordinate reference system consisting of one coordinate system and either one datum or one datum ensemble\"@en .\n")
ttl.add("geocrs:SingleCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:GeographicCRS rdfs:subClassOf geocrs:GeodeticCRS .\n")
ttl.add("geocrs:GeographicCRS rdf:type owl:Class .\n")
ttl.add("geocrs:GeographicCRS rdfs:label \"geographic coordinate reference system\"@en .\n")
ttl.add("geocrs:GeographicCRS skos:definition \"coordinate reference system that has a geodetic reference frame and an ellipsoidal coordinate system\"@en .\n")
ttl.add("geocrs:GeographicCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:AffineCoordinateSystem rdfs:subClassOf geocrs:CoordinateSystem .\n")
ttl.add("geocrs:AffineCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:AffineCoordinateSystem owl:equivalentClass wd:Q382510 .\n")
ttl.add("geocrs:AffineCoordinateSystem rdfs:label \"affine coordinate system\"@en .\n")
ttl.add("geocrs:AffineCoordinateSystem skos:definition \"coordinate system in Euclidean space with straight axes that are not necessarily mutually perpendicular\"@en .\n")
ttl.add("geocrs:AffineCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:GeodeticCRS rdfs:subClassOf geocrs:SingleCRS .\n")
ttl.add("geocrs:GeodeticCRS rdf:type owl:Class .\n")
ttl.add("geocrs:GeodeticCRS rdfs:label \"geodetic coordinate reference system\"@en .\n")
ttl.add("geocrs:GeodeticCRS owl:disjointWith geocrs:CartesianCoordinateSystem, geocrs:CompoundCRS, geocrs:EllipsoidalCoordinateSystem .\n")
ttl.add("geocrs:GeodeticCRS skos:definition \"three-dimensional coordinate reference system based on a geodetic reference frame and having either a three-dimensional Cartesian or a spherical coordinate system\"@en .\n")
ttl.add("geocrs:GeodeticCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:CompoundCRS rdfs:subClassOf geocrs:CRS .\n")
ttl.add("geocrs:CompoundCRS rdf:type owl:Class .\n")
ttl.add("geocrs:CompoundCRS skos:definition \"coordinate reference system using at least two independent coordinate reference systems\"@en .\n")
ttl.add("geocrs:CompoundCRS rdfs:label \"compound coordinate reference system\"@en .\n")
ttl.add("geocrs:CompoundCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:SpatialCompoundCRS rdfs:subClassOf geocrs:CompoundCRS .\n")
ttl.add("geocrs:SpatialCompoundCRS rdf:type owl:Class .\n")
ttl.add("geocrs:SpatialCompoundCRS skos:definition \"coordinate reference system using a combination of two compatible spatial reference systems\"@en .\n")
ttl.add("geocrs:SpatialCompoundCRS rdfs:label \"spatial compound coordinate reference system\"@en .\n")
ttl.add("geocrs:SpatialCompoundCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:SpatioTemporalCompoundCRS rdfs:subClassOf geocrs:CompoundCRS .\n")
ttl.add("geocrs:SpatioTemporalCompoundCRS rdf:type owl:Class .\n")
ttl.add("geocrs:SpatioTemporalCompoundCRS skos:definition \"coordinate reference system combining a spatial reference system with at least one temporal reference system\"@en .\n")
ttl.add("geocrs:SpatioTemporalCompoundCRS rdfs:label \"spatio-temporal compound coordinate reference system\"@en .\n")
ttl.add("geocrs:SpatioTemporalCompoundCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:SpatioParametricCompoundCRS rdfs:subClassOf geocrs:CompoundCRS .\n")
ttl.add("geocrs:SpatioParametricCompoundCRS rdf:type owl:Class .\n")
ttl.add("geocrs:SpatioParametricCompoundCRS skos:definition \"A spatio-parametric coordinate reference system is a compound CRS in which one component is a geographic 2D, projected 2D or engineering 2D CRS, supplemented by a parametric CRS to create a three-dimensional CRS\"@en .\n")
ttl.add("geocrs:SpatioParametricCompoundCRS rdfs:label \"spatio-parametric compound coordinate reference system\"@en .\n")
ttl.add("geocrs:SpatioParametricCompoundCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:SpatioParametricTemporalCompoundCRS rdfs:subClassOf geocrs:CompoundCRS .\n")
ttl.add("geocrs:SpatioParametricTemporalCompoundCRS rdf:type owl:Class .\n")
ttl.add("geocrs:SpatioParametricTemporalCompoundCRS rdfs:label \"spatio-parametric-temporal compound coordinate reference system\"@en .\n")
ttl.add("geocrs:SpatioParametricTemporalCompoundCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:BoundCRS rdfs:subClassOf geocrs:CRS .\n")
ttl.add("geocrs:BoundCRS rdf:type owl:Class .\n")
ttl.add("geocrs:BoundCRS rdfs:label \"bound coordinate reference system\"@en .\n")
ttl.add("geocrs:BoundCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DynamicCRS rdfs:subClassOf geocrs:CRS .\n")
ttl.add("geocrs:DynamicCRS rdf:type owl:Class .\n")
ttl.add("geocrs:DynamicCRS rdfs:label \"dynamic coordinate reference system\"@en .\n")
ttl.add("geocrs:DynamicCRS skos:definition \"coordinate reference system that has a dynamic reference frame\"@en .\n")
ttl.add("geocrs:DynamicCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:TemporalCRS rdfs:subClassOf geocrs:SingleCRS .\n")
ttl.add("geocrs:TemporalCRS rdf:type owl:Class .\n")
ttl.add("geocrs:TemporalCRS rdfs:label \"temporal coordinate reference system\"@en .\n")
ttl.add("geocrs:TemporalCRS skos:definition \"coordinate reference system based on a temporal datum\"@en .\n")
ttl.add("geocrs:TemporalCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:ParametricCRS rdfs:subClassOf geocrs:SingleCRS .\n")
ttl.add("geocrs:ParametricCRS rdf:type owl:Class .\n")
ttl.add("geocrs:ParametricCRS rdfs:label \"parametric coordinate reference system\"@en .\n")
ttl.add("geocrs:ParametricCRS skos:definition \"one-dimensional coordinate system where the axis units are parameter values which are not inherently spatial\"@en .\n")
ttl.add("geocrs:ParametricCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:SpatioParametricCRS rdfs:subClassOf geocrs:CRS .\n")
ttl.add("geocrs:SpatioParametricCRS rdf:type owl:Class .\n")
ttl.add("geocrs:SpatioParametricCRS rdfs:label \"spatio-Parametric coordinate reference system\"@en .\n")
ttl.add("geocrs:SpatioParametricCRS skos:definition \"compound coordinate reference system in which one constituent coordinate reference system is a spatial coordinate reference system and one is a parametric coordinate reference system\"@en .\n")
ttl.add("geocrs:SpatioParametricCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DerivedGeographicCRS rdfs:subClassOf geocrs:GeographicCRS .\n")
ttl.add("geocrs:DerivedGeographicCRS rdfs:subClassOf geocrs:DerivedCRS .\n")
ttl.add("geocrs:DerivedGeographicCRS rdf:type owl:Class .\n")
ttl.add("geocrs:DerivedGeographicCRS rdfs:label \"derived geographic coordinate reference system\"@en .\n")
ttl.add("geocrs:DerivedGeographicCRS skos:definition \"coordinate reference system that is defined through the application of a specified coordinate conversion to the coordinates within a previously established coordinate reference system\"@en .\n")
ttl.add("geocrs:DerivedGeographicCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DerivedProjectedCRS rdfs:subClassOf geocrs:ProjectedCRS .\n")
ttl.add("geocrs:DerivedProjectedCRS rdfs:subClassOf geocrs:DerivedCRS .\n")
ttl.add("geocrs:DerivedProjectedCRS rdf:type owl:Class .\n")
ttl.add("geocrs:DerivedProjectedCRS rdfs:label \"derived projected coordinate reference system\"@en .\n")
ttl.add("geocrs:DerivedProjectedCRS skos:definition \"derived coordinate reference system which has a projected coordinate reference system as its base CRS, thereby inheriting a geodetic reference frame, but also inheriting the distortion characteristics of the base projected CRS\"@en .\n")
ttl.add("geocrs:DerivedProjectedCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DerivedCRS rdfs:subClassOf geocrs:SingleCRS .\n")
ttl.add("geocrs:DerivedCRS rdf:type owl:Class .\n")
ttl.add("geocrs:DerivedCRS rdfs:label \"derived coordinate reference system\"@en .\n")
ttl.add("geocrs:DerivedCRS skos:definition \"derived coordinate reference system which has a projected coordinate reference system as its base CRS, thereby inheriting a geodetic reference frame, but also inheriting the distortion characteristics of the base projected CRS\"@en .\n")
ttl.add("geocrs:DerivedCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DerivedVerticalCRS rdfs:subClassOf geocrs:VerticalCRS .\n")
ttl.add("geocrs:DerivedVerticalCRS rdfs:subClassOf geocrs:DerivedCRS .\n")
ttl.add("geocrs:DerivedVerticalCRS rdf:type owl:Class .\n")
ttl.add("geocrs:DerivedVerticalCRS rdfs:label \"derived vertical coordinate reference system\"@en .\n")
ttl.add("geocrs:DerivedVerticalCRS skos:definition \"derived coordinate reference system which has a vertical coordinate reference system as its base CRS, thereby inheriting a vertical reference frame, and a vertical coordinate system\"@en .\n")
ttl.add("geocrs:DerivedVerticalCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DerivedGeodeticCRS rdfs:subClassOf geocrs:DerivedCRS .\n")
ttl.add("geocrs:DerivedGeodeticCRS rdfs:subClassOf geocrs:GeodeticCRS .\n")
ttl.add("geocrs:DerivedGeodeticCRS rdf:type owl:Class .\n")
ttl.add("geocrs:DerivedGeodeticCRS rdfs:label \"derived geodetic coordinate reference system\"@en .\n")
ttl.add("geocrs:DerivedGeodeticCRS skos:definition \"derived coordinate reference system which has either a geodetic or a geographic coordinate reference system as its base CRS, thereby inheriting a geodetic reference frame, and associated with a 3D Cartesian or spherical coordinate system\"@en .\n")
ttl.add("geocrs:DerivedGeodeticCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DerivedParametricCRS rdfs:subClassOf geocrs:ParametricCRS .\n")
ttl.add("geocrs:DerivedParametricCRS rdfs:subClassOf geocrs:DerivedCRS .\n")
ttl.add("geocrs:DerivedParametricCRS rdf:type owl:Class .\n")
ttl.add("geocrs:DerivedParametricCRS rdfs:label \"derived parametric coordinate reference system\"@en .\n")
ttl.add("geocrs:DerivedParametricCRS skos:definition \"derived coordinate reference system which has a parametric coordinate reference system as its base CRS, thereby inheriting a parametric datum, and a parametric coordinate system\"@en .\n")
ttl.add("geocrs:DerivedParametricCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DerivedEngineeringCRS rdfs:subClassOf geocrs:EngineeringCRS .\n")
ttl.add("geocrs:DerivedEngineeringCRS rdfs:subClassOf geocrs:DerivedCRS .\n")
ttl.add("geocrs:DerivedEngineeringCRS rdf:type owl:Class .\n")
ttl.add("geocrs:DerivedEngineeringCRS rdfs:label \"derived engineering coordinate reference system\"@en .\n")
ttl.add("geocrs:DerivedEngineeringCRS skos:definition \"derived coordinate reference system which has an engineering coordinate reference system as its base CRS, thereby inheriting an engineering datum, and is associated with one of the coordinate system types within the engineeringCS class\"@en .\n")
ttl.add("geocrs:DerivedEngineeringCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:EngineeringCRS rdfs:subClassOf geocrs:SingleCRS .\n")
ttl.add("geocrs:EngineeringCRS rdf:type owl:Class .\n")
ttl.add("geocrs:EngineeringCRS skos:definition \"coordinate reference system based on an engineering datum\"@en .\n")
ttl.add("geocrs:EngineeringCRS rdfs:label \"engineering coordinate reference system\"@en .\n")
ttl.add("geocrs:EngineeringCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:VerticalCRS rdfs:subClassOf geocrs:SingleCRS .\n")
ttl.add("geocrs:VerticalCRS rdf:type owl:Class .\n")
ttl.add("geocrs:VerticalCRS rdfs:label \"vertical coordinate reference system\"@en .\n")
ttl.add("geocrs:VerticalCRS skos:definition \"one-dimensional coordinate reference system based on a vertical reference frame\"@en .\n")
ttl.add("geocrs:VerticalCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:GeocentricCRS rdfs:subClassOf geocrs:CRS .\n")
ttl.add("geocrs:GeocentricCRS rdf:type owl:Class .\n")
ttl.add("geocrs:GeocentricCRS rdfs:label \"geocentric coordinate reference system\"@en .\n")
ttl.add("geocrs:GeocentricCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:HorizontalDatum rdfs:subClassOf geocrs:Datum .\n")
ttl.add("geocrs:HorizontalDatum rdf:type owl:Class .\n")
ttl.add("geocrs:HorizontalDatum rdfs:label \"horizontal datum\"@en .\n")
ttl.add("geocrs:HorizontalDatum rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:GeodeticReferenceFrame rdfs:subClassOf geocrs:HorizontalDatum .\n")
ttl.add("geocrs:GeodeticReferenceFrame rdf:type owl:Class .\n")
ttl.add("geocrs:GeodeticReferenceFrame rdfs:label \"geodetic reference frame\"@en .\n")
ttl.add("geocrs:GeodeticReferenceFrame skos:definition \"reference frame describing the relationship of a two- or three-dimensional coordinate system to the Earth\"@en .\n")
ttl.add("geocrs:GeodeticReferenceFrame rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DynamicReferenceFrame rdfs:subClassOf geocrs:Datum .\n")
ttl.add("geocrs:DynamicReferenceFrame rdf:type owl:Class .\n")
ttl.add("geocrs:DynamicReferenceFrame rdfs:label \"dynamic reference frame\"@en .\n")
ttl.add("geocrs:DynamicReferenceFrame skos:definition \"reference frame in which the defining parameters include time evolution\"@en .\n")
ttl.add("geocrs:DynamicReferenceFrame rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DynamicGeodeticReferenceFrame rdfs:subClassOf geocrs:GeodeticReferenceFrame, geocrs:DynamicReferenceFrame .\n")
ttl.add("geocrs:DynamicGeodeticReferenceFrame rdf:type owl:Class .\n")
ttl.add("geocrs:DynamicGeodeticReferenceFrame rdfs:label \"dynamic geodetic reference frame\"@en .\n")
ttl.add("geocrs:DynamicGeodeticReferenceFrame skos:definition \"geodetic reference frame in which some of the parameters describe time evolution of defining station coordinates\"@en .\n")
ttl.add("geocrs:DynamicGeodeticReferenceFrame rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DynamicVerticalReferenceFrame rdfs:subClassOf geocrs:VerticalReferenceFrame, geocrs:DynamicReferenceFrame .\n")
ttl.add("geocrs:DynamicVerticalReferenceFrame rdf:type owl:Class .\n")
ttl.add("geocrs:DynamicVerticalReferenceFrame rdfs:label \"dynamic vertical reference frame\"@en .\n")
ttl.add("geocrs:DynamicVerticalReferenceFrame skos:definition \"vertical reference frame in which some of the defining parameters have time dependency\"@en .\n")
ttl.add("geocrs:DynamicVerticalReferenceFrame rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:VerticalReferenceFrame rdfs:subClassOf geocrs:Datum .\n")
ttl.add("geocrs:VerticalReferenceFrame rdf:type owl:Class .\n")
ttl.add("geocrs:VerticalReferenceFrame rdfs:label \"vertical reference frame\"@en .\n")
ttl.add("geocrs:VerticalReferenceFrame skos:definition \"reference frame describing the relation of gravity-related heights or depths to the Earth\"@en .\n")
ttl.add("geocrs:VerticalReferenceFrame rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:StaticCRS rdfs:subClassOf geocrs:CRS .\n")
ttl.add("geocrs:StaticCRS rdf:type owl:Class .\n")
ttl.add("geocrs:StaticCRS rdfs:label \"Static coordinate reference system\"@en .\n")
ttl.add("geocrs:StaticCRS skos:definition \"coordinate reference system that has a static reference frame\"@en .\n")
ttl.add("geocrs:StaticCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:ProjectedCRS rdfs:subClassOf geocrs:DerivedCRS .\n")
ttl.add("geocrs:ProjectedCRS rdf:type owl:Class .\n")
ttl.add("geocrs:ProjectedCRS rdfs:label \"projected coordinate reference system\"@en .\n")
ttl.add("geocrs:ProjectedCRS skos:definition \"coordinate reference system derived from a geographic coordinate reference system by applying a map projection\"@en .\n")
ttl.add("geocrs:ProjectedCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:Datum rdf:type owl:Class .\n")
ttl.add("geocrs:Datum owl:equivalentClass wd:Q1502887 .\n")
ttl.add("geocrs:Datum rdfs:label \"datum\"@en .\n")
ttl.add("geocrs:Datum skos:definition \"specification of the relationship of a coordinate system to an object, thus creating a coordinate reference system\"@en .\n")
ttl.add("geocrs:Datum rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DatumEnsemble rdf:type owl:Class .\n")
ttl.add("geocrs:DatumEnsemble rdfs:label \"datum ensemble\"@en .\n")
ttl.add("geocrs:DatumEnsemble skos:definition \"collection of two or more geodetic or vertical reference frames (or if not geodetic or vertical reference frame, a collection of two or more datums) which for all but the highest accuracy requirements may be considered to be insignificantly different from each other\"@en .\n")
ttl.add("geocrs:DatumEnsemble rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:ParametricDatum rdf:type owl:Class .\n")
ttl.add("geocrs:ParametricDatum rdfs:subClassOf geocrs:Datum .\n")
ttl.add("geocrs:ParametricDatum rdfs:label \"parametric datum\"@en .\n")
ttl.add("geocrs:ParametricDatum skos:definition \"textual description and/or a set of parameters identifying a particular reference surface used as the origin of a parametric coordinate system, including its position with respect to the Earth\"@en .\n")
ttl.add("geocrs:ParametricDatum rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:TemporalDatum rdfs:subClassOf geocrs:Datum .\n")
ttl.add("geocrs:TemporalDatum rdf:type owl:Class .\n")
ttl.add("geocrs:TemporalDatum rdfs:label \"temporal datum\"@en .\n")
ttl.add("geocrs:TemporalDatum skos:definition \"coordinate reference system based on a temporal datum\"@en .\n")
ttl.add("geocrs:TemporalDatum rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:EngineeringDatum rdfs:subClassOf geocrs:Datum .\n")
ttl.add("geocrs:EngineeringDatum rdf:type owl:Class .\n")
ttl.add("geocrs:EngineeringDatum rdfs:label \"engineering datum\"@en .\n")
ttl.add("geocrs:EngineeringDatum skos:definition \"datum describing the relationship of a coordinate system to a local reference\"@en .\n")
ttl.add("geocrs:EngineeringDatum rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:Ellipsoid rdf:type owl:Class .\n")
ttl.add("geocrs:Ellipsoid rdfs:subClassOf geocrs:Geoid .\n")
ttl.add("geocrs:Ellipsoid rdfs:label \"ellipsoid\"@en .\n")
ttl.add("geocrs:Ellipsoid owl:disjointWith geocrs:PrimeMeridian .\n")
ttl.add("geocrs:Ellipsoid skos:definition \"reference ellipsoid\"@en .\n")
ttl.add("geocrs:Ellipsoid rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:TriaxialEllipsoid rdf:type owl:Class .\n")
ttlnoniso.add("geocrs:TriaxialEllipsoid rdfs:subClassOf geocrs:Ellipsoid.\n")
ttlnoniso.add("geocrs:TriaxialEllipsoid rdfs:label \"triaxial ellipsoid\"@en .\n")
ttlnoniso.add("geocrs:TriaxialEllipsoid owl:disjointWith geocrs:PrimeMeridian .\n")
ttlnoniso.add("geocrs:TriaxialEllipsoid skos:definition \"triaxial reference ellipsoid\"@en .\n")
ttl.add("geocrs:Sphere rdf:type owl:Class .\n")
ttl.add("geocrs:Sphere rdfs:subClassOf geocrs:Geoid .\n")
ttl.add("geocrs:Sphere rdfs:label \"sphere\"@en .\n")
ttl.add("geocrs:Sphere skos:definition \"reference sphere\"@en .\n")
ttl.add("geocrs:Sphere rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:Geoid rdf:type owl:Class .\n")
ttl.add("geocrs:Geoid rdfs:label \"geoid\"@en .\n")
ttl.add("geocrs:Geoid skos:definition \"equipotential surface of the Earth’s gravity field which is perpendicular to the direction of gravity and which best fits mean sea level either locally, regionally or globally\"@en .\n")
ttl.add("geocrs:Geoid rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:PrimeMeridian rdf:type owl:Class .\n")
ttl.add("geocrs:PrimeMeridian rdfs:label \"prime meridian\"@en .\n")
ttl.add("geocrs:PrimeMeridian skos:definition \"meridian from which the longitudes of other meridians are quantified\"@en .\n")
ttl.add("geocrs:PrimeMeridian rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttlnoniso.add("geocrs:SRSRegistry rdf:type owl:Class .\n")
ttlnoniso.add("geocrs:SRSRegistry rdfs:label \"srs registry\"@en .\n")
ttlnoniso.add("geocrs:SRSRegistry skos:definition \"A rdf-enabled registry for SRS definitions\"@en .\n")
ttlprojectionvocab.add("geocrs:ProjectionOntology rdf:type owl:Ontology .\n")
ttlprojectionvocab.add("geocrs:ProjectionOntology rdfs:label \"Projection Ontology\"@en .\n")
ttlprojectionvocab.add("geocrs:isInverseProjectionOf rdf:type owl:ObjectProperty .\n")
ttlprojectionvocab.add("geocrs:isInverseProjectionOf rdfs:label \"is inverse projection of\"@en .\n")
ttlprojectionvocab.add("geocrs:isTransverseProjectionOf rdf:type owl:ObjectProperty .\n")
ttlprojectionvocab.add("geocrs:isTransverseProjectionOf rdfs:label \"is transverse projection of\"@en .\n")
ttlprojectionvocab.add("geocrs:Projection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:Projection rdfs:label \"projection\"@en .\n")
ttlprojectionvocab.add("geocrs:Projection rdfs:subClassOf geocrs:Conversion .\n")
ttlprojectionvocab.add("geocrs:Projection skos:definition \"coordinate conversion from an ellipsoidal coordinate system to a plane\"@en .\n")
ttlprojectionvocab.add("geocrs:PerspectiveProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:PerspectiveProjection rdfs:label \"perspective projection\"@en .\n")
ttlprojectionvocab.add("geocrs:PerspectiveProjection rdfs:subClassOf geocrs:Projection .\n")
ttlprojectionvocab.add("geocrs:GlobularProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:GlobularProjection rdfs:label \"globular projection\"@en .\n")
ttlprojectionvocab.add("geocrs:GlobularProjection rdfs:subClassOf geocrs:Projection .\n")
ttlprojectionvocab.add("geocrs:OvalProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:OvalProjection rdfs:label \"oval projection\"@en .\n")
ttlprojectionvocab.add("geocrs:OvalProjection rdfs:subClassOf geocrs:Projection .\n")
ttlprojectionvocab.add("geocrs:CylindricalProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:CylindricalProjection rdfs:label \"cylindrical projection\"@en .\n")
ttlprojectionvocab.add("geocrs:CylindricalProjection rdfs:subClassOf geocrs:Projection .\n")
ttlprojectionvocab.add("geocrs:PolyconicProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:PolyconicProjection rdfs:label \"polyconic projection\"@en .\n")
ttlprojectionvocab.add("geocrs:PolyconicProjection rdfs:subClassOf geocrs:Projection .\n")
ttlprojectionvocab.add("geocrs:MinimumErrorProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:MinimumErrorProjection rdfs:label \"minimum error projection\"@en .\n")
ttlprojectionvocab.add("geocrs:MinimumErrorProjection rdfs:subClassOf geocrs:Projection .\n")
ttlprojectionvocab.add("geocrs:CordiformProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:CordiformProjection rdfs:label \"cordiform projection\"@en .\n")
ttlprojectionvocab.add("geocrs:CordiformProjection rdfs:subClassOf geocrs:Projection .\n")
ttlprojectionvocab.add("geocrs:PerspectiveConicProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:PerspectiveConicProjection rdfs:label \"perspective conic projection\"@en .\n")
ttlprojectionvocab.add("geocrs:PerspectiveConicProjection rdfs:subClassOf geocrs:PerspectiveProjection, geocrs:ConicalProjection .\n")
ttlprojectionvocab.add("geocrs:EquidistantProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:EquidistantProjection rdfs:label \"equidistant projection\"@en .\n")
ttlprojectionvocab.add("geocrs:EquidistantProjection skos:definition \"Projection in which all points on the map exhibit proportionally correct distances from the center point\"@en .\n")
ttlprojectionvocab.add("geocrs:EquidistantProjection rdfs:subClassOf geocrs:Projection .\n")
ttlprojectionvocab.add("geocrs:ConformalProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:ConformalProjection rdfs:label \"conformal projection\"@en .\n")
ttlprojectionvocab.add("geocrs:ConformalProjection skos:definition \"A projection in which every angle between two curves that crosss each other on a celestical boday is preserved in the image of the projection\"@en .\n")
ttlprojectionvocab.add("geocrs:ConformalProjection rdfs:subClassOf geocrs:Projection .\n")
ttlprojectionvocab.add("geocrs:AzimuthalProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:AzimuthalProjection rdfs:label \"azimuthal projection\"@en .\n")
ttlprojectionvocab.add("geocrs:AzimuthalProjection skos:definition \"A projection with the property that directions from a central point are preserved\"@en .\n")
ttlprojectionvocab.add("geocrs:AzimuthalProjection rdfs:subClassOf geocrs:Projection .\n")
ttlprojectionvocab.add("geocrs:BerghausStarProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:BerghausStarProjection rdfs:label \"berghaus star projection\"@en .\n")
ttlprojectionvocab.add("geocrs:BerghausStarProjection rdfs:subClassOf geocrs:EquidistantProjection .\n")
ttlprojectionvocab.add("geocrs:RetroazimuthalProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:RetroazimuthalProjection rdfs:label \"retroazimuthal projection\"@en .\n")
ttlprojectionvocab.add("geocrs:RetroazimuthalProjection rdfs:subClassOf geocrs:Projection .\n")
ttlprojectionvocab.add("geocrs:PlateCarreeProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:PlateCarreeProjection rdfs:label \"Plate Carree Projection\"@en .\n")
ttlprojectionvocab.add("geocrs:PlateCarreeProjection rdfs:subClassOf geocrs:EquidistantProjection, geocrs:CylindricalProjection .\n")
ttlprojectionvocab.add("geocrs:ObliquePlateCarreeProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:ObliquePlateCarreeProjection rdfs:label \"Oblique Plate Carree Projection\"@en .\n")
ttlprojectionvocab.add("geocrs:ObliquePlateCarreeProjection rdfs:subClassOf geocrs:EquidistantProjection, geocrs:CylindricalProjection .\n")
ttlprojectionvocab.add("geocrs:CollignonProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:CollignonProjection rdfs:label \"collignon projection\"@en .\n")
ttlprojectionvocab.add("geocrs:CollignonProjection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:GaussKruegerProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:GaussKruegerProjection rdfs:label \"gauss-krüger projection\"@en .\n")
ttlprojectionvocab.add("geocrs:GaussKruegerProjection rdfs:subClassOf geocrs:CylindricalProjection, geocrs:ConformalProjection .\n")
ttlprojectionvocab.add("geocrs:AuthaGraphProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:AuthaGraphProjection rdfs:label \"autha graph projection\"@en .\n")
ttlprojectionvocab.add("geocrs:AuthaGraphProjection rdfs:subClassOf geocrs:PolyhedralProjection, geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:ToblerHyperelliptical rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:ToblerHyperelliptical rdfs:label \"tobler hyperelliptical projection\"@en .\n")
ttlprojectionvocab.add("geocrs:ToblerHyperelliptical rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:ToblerCylindricalIProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:ToblerCylindricalIProjection rdfs:label \"tobler cylindrical I projection\"@en .\n")
ttlprojectionvocab.add("geocrs:ToblerCylindricalIProjection rdfs:subClassOf geocrs:CylindricalProjection .\n")
ttlprojectionvocab.add("geocrs:ToblerCylindricalIIProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:ToblerCylindricalIIProjection rdfs:label \"tobler cylindrical II projection\"@en .\n")
ttlprojectionvocab.add("geocrs:ToblerCylindricalIIProjection rdfs:subClassOf geocrs:CylindricalProjection .\n")
ttlprojectionvocab.add("geocrs:ToblerG1Projection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:ToblerG1Projection rdfs:label \"tobler g1 projection\"@en .\n")
ttlprojectionvocab.add("geocrs:ToblerG1Projection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:PutninsP5Projection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:PutninsP5Projection rdfs:label \"putnins p5 projection\"@en .\n")
ttlprojectionvocab.add("geocrs:PutninsP5Projection rdfs:subClassOf geocrs:PseudoCylindricalProjection .\n")
ttlprojectionvocab.add("geocrs:OrteliusOvalProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:OrteliusOvalProjection rdfs:label \"ortelius oval projection\"@en .\n")
ttlprojectionvocab.add("geocrs:OrteliusOvalProjection rdfs:subClassOf geocrs:OvalProjection .\n")
ttlprojectionvocab.add("geocrs:LagrangeProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:LagrangeProjection rdfs:label \"lagrange projection\"@en .\n")
ttlprojectionvocab.add("geocrs:LagrangeProjection rdfs:subClassOf geocrs:ConformalProjection, geocrs:PolyconicProjection .\n")
ttlprojectionvocab.add("geocrs:EisenlohrProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:EisenlohrProjection rdfs:label \"eisenlohr projection\"@en .\n")
ttlprojectionvocab.add("geocrs:EisenlohrProjection rdfs:subClassOf geocrs:ConformalProjection .\n")
ttlprojectionvocab.add("geocrs:DenoyerSemiEllipticalProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:DenoyerSemiEllipticalProjection rdfs:label \"denoyer semi-elliptical projection\"@en .\n")
ttlprojectionvocab.add("geocrs:CahillKeyesProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:CahillKeyesProjection rdfs:label \"cahill-keyes projection\"@en .\n")
ttlprojectionvocab.add("geocrs:CahillKeyesProjection rdfs:subClassOf geocrs:PolyhedralProjection, geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:CentralCylindricalProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:CentralCylindricalProjection rdfs:label \"central cylindrical projection\"@en .\n")
ttlprojectionvocab.add("geocrs:CentralCylindricalProjection rdfs:subClassOf geocrs:CylindricalProjection, geocrs:PerspectiveProjection .\n")
ttlprojectionvocab.add("geocrs:LittrowProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:LittrowProjection rdfs:label \"littrow projection\"@en .\n")
ttlprojectionvocab.add("geocrs:LittrowProjection rdfs:subClassOf geocrs:RetroazimuthalProjection, geocrs:ConformalProjection .\n")
ttlprojectionvocab.add("geocrs:QuarticAuthalicProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:QuarticAuthalicProjection rdfs:label \"quartic authalic projection\"@en .\n")
ttlprojectionvocab.add("geocrs:QuarticAuthalicProjection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:CraigRetroazimuthalProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:CraigRetroazimuthalProjection rdfs:label \"craig retroazimuthal projection\"@en .\n")
ttlprojectionvocab.add("geocrs:CraigRetroazimuthalProjection rdfs:subClassOf geocrs:RetroazimuthalProjection, geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:HatanoAsymmetricalEqualAreaProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:HatanoAsymmetricalEqualAreaProjection rdfs:label \"peirce quincuncial projection\"@en .\n")
ttlprojectionvocab.add("geocrs:HatanoAsymmetricalEqualAreaProjection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:PeirceQuincuncialProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:PeirceQuincuncialProjection rdfs:label \"peirce quincuncial projection\"@en .\n")
ttlprojectionvocab.add("geocrs:PeirceQuincuncialProjection rdfs:subClassOf geocrs:ConformalProjection .\n")
ttlprojectionvocab.add("geocrs:VerticalPerspectiveProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:VerticalPerspectiveProjection rdfs:label \"vertical perspective projection\"@en .\n")
ttlprojectionvocab.add("geocrs:VerticalPerspectiveProjection rdfs:subClassOf geocrs:AzimuthalProjection, geocrs:PerspectiveProjection .\n")
ttlprojectionvocab.add("geocrs:NicolosiGlobularProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:NicolosiGlobularProjection rdfs:label \"nicolosi globular projection\"@en .\n")
ttlprojectionvocab.add("geocrs:NicolosiGlobularProjection rdfs:subClassOf geocrs:PseudoConicalProjection, geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:BehrmannProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:BehrmannProjection rdfs:label \"behrmann projection\"@en .\n")
ttlprojectionvocab.add("geocrs:BehrmannProjection rdfs:subClassOf geocrs:CylindricalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:HoboDyerProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:HoboDyerProjection rdfs:label \"hobo-dyer projection\"@en .\n")
ttlprojectionvocab.add("geocrs:HoboDyerProjection rdfs:subClassOf geocrs:CylindricalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:GringortenProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:GringortenProjection rdfs:label \"gringorten projection\"@en .\n")
ttlprojectionvocab.add("geocrs:GringortenProjection rdfs:subClassOf geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:BakerDinomicProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:BakerDinomicProjection rdfs:label \"baker dinomic projection\"@en .\n")
ttlprojectionvocab.add("geocrs:BakerDinomicProjection rdfs:subClassOf geocrs:Projection .\n")
ttlprojectionvocab.add("geocrs:GallPetersProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:GallPetersProjection rdfs:label \"gall-peters projection\"@en .\n")
ttlprojectionvocab.add("geocrs:GallPetersProjection rdfs:subClassOf geocrs:CylindricalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:GallStereographicProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:GallStereographicProjection rdfs:label \"gall stereographic projection\"@en .\n")
ttlprojectionvocab.add("geocrs:GallStereographicProjection rdfs:subClassOf geocrs:CylindricalProjection, geocrs:CompromiseProjection, geocrs:StereographicProjection .\n")
ttlprojectionvocab.add("geocrs:Strebe1995Projection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:Strebe1995Projection rdfs:label \"strebe 1995 projection\"@en .\n")
ttlprojectionvocab.add("geocrs:Strebe1995Projection rdfs:subClassOf geocrs:PseudoAzimuthalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:WatermanButterflyProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:WatermanButterflyProjection rdfs:label \"waterman butterfly projection\"@en .\n")
ttlprojectionvocab.add("geocrs:WatermanButterflyProjection rdfs:subClassOf geocrs:PolyhedralProjection, geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:QuadrilateralizedSphericalCubeProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:QuadrilateralizedSphericalCubeProjection rdfs:label \"quadrilateralized spherical cube projection\"@en .\n")
ttlprojectionvocab.add("geocrs:QuadrilateralizedSphericalCubeProjection rdfs:subClassOf geocrs:PolyhedralProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:GeneralVerticalPerspectiveProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:GeneralVerticalPerspectiveProjection rdfs:label \"general vertical perspective projection\"@en .\n")
ttlprojectionvocab.add("geocrs:GeneralVerticalPerspectiveProjection rdfs:subClassOf geocrs:AzimuthalProjection, geocrs:PerspectiveProjection .\n")
ttlprojectionvocab.add("geocrs:BonneProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:BonneProjection rdfs:label \"bonne projection\"@en .\n")
ttlprojectionvocab.add("geocrs:BonneProjection rdfs:subClassOf geocrs:PseudoConicalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:ArmadilloProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:ArmadilloProjection rdfs:label \"armadillo projection\"@en .\n")
ttlprojectionvocab.add("geocrs:ArmadilloProjection rdfs:subClassOf geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:GS50Projection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:GS50Projection rdfs:label \"gs50 projection\"@en .\n")
ttlprojectionvocab.add("geocrs:GS50Projection rdfs:subClassOf geocrs:ConformalProjection .\n")
ttlprojectionvocab.add("geocrs:GS50Projection skos:definition \"A map projection that was developed by John Parr Snyder of the USGS in 1982. The GS50 projection provides a conformal projection suitable only for maps of the 50 United States\"@en .\n")
ttlprojectionvocab.add("geocrs:BipolarObliqueConicConformalProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:BipolarObliqueConicConformalProjection rdfs:label \"Bipolar Oblique Conic Conformal Projection\"@en .\n")
ttlprojectionvocab.add("geocrs:BipolarObliqueConicConformalProjection rdfs:subClassOf geocrs:ConicalProjection, geocrs:ConformalProjection .\n")
ttlprojectionvocab.add("geocrs:Eckert1Projection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:Eckert1Projection rdfs:label \"Eckert I projection\"@en .\n")
ttlprojectionvocab.add("geocrs:Eckert1Projection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:Eckert2Projection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:Eckert2Projection rdfs:label \"Eckert II projection\"@en .\n")
ttlprojectionvocab.add("geocrs:Eckert2Projection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:Eckert3Projection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:Eckert3Projection rdfs:label \"Eckert III projection\"@en .\n")
ttlprojectionvocab.add("geocrs:Eckert3Projection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:Eckert4Projection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:Eckert4Projection rdfs:label \"Eckert IV projection\"@en .\n")
ttlprojectionvocab.add("geocrs:Eckert4Projection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:Eckert5Projection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:Eckert5Projection rdfs:label \"Eckert V projection\"@en .\n")
ttlprojectionvocab.add("geocrs:Eckert5Projection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:Eckert6Projection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:Eckert6Projection rdfs:label \"Eckert VI projection\"@en .\n")
ttlprojectionvocab.add("geocrs:Eckert6Projection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:Kavrayskiy7Projection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:Kavrayskiy7Projection rdfs:label \"Kavrayskiy VII projection\"@en .\n")
ttlprojectionvocab.add("geocrs:Kavrayskiy7Projection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:AzimuthalEquidistantProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:AzimuthalEquidistantProjection rdfs:label \"azimuthal equidistant projection\"@en .\n")
ttlprojectionvocab.add("geocrs:AzimuthalEquidistantProjection rdfs:subClassOf geocrs:AzimuthalProjection, geocrs:EquidistantProjection .\n")
ttlprojectionvocab.add("geocrs:GuyouProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:GuyouProjection rdfs:label \"guyou projection\"@en .\n")
ttlprojectionvocab.add("geocrs:GuyouProjection rdfs:subClassOf geocrs:ConformalProjection .\n")
ttlprojectionvocab.add("geocrs:RoussilheProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:RoussilheProjection rdfs:label \"roussilhe projection\"@en .\n")
ttlprojectionvocab.add("geocrs:RoussilheProjection rdfs:subClassOf geocrs:ObliqueProjection, geocrs:StereographicProjection .\n")
ttlprojectionvocab.add("geocrs:LeeProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:LeeProjection rdfs:label \"lee projection\"@en .\n")
ttlprojectionvocab.add("geocrs:LeeProjection rdfs:subClassOf geocrs:PolyhedralProjection, geocrs:ConformalProjection .\n")
ttlprojectionvocab.add("geocrs:AdamsProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:AdamsProjection rdfs:label \"adams projection\"@en .\n")
ttlprojectionvocab.add("geocrs:AdamsProjection skos:definition \"The Adams hemisphere-in-a-square projection is a conformal map projection for a hemisphere\"@en .\n")
ttlprojectionvocab.add("geocrs:AdamsProjection rdfs:subClassOf geocrs:ConformalProjection .\n")
ttlprojectionvocab.add("geocrs:OrteliusOvalProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:OrteliusOvalProjection rdfs:label \"ortelius oval projection\"@en .\n")
ttlprojectionvocab.add("geocrs:OrteliusOvalProjection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:GoodeHomolosineProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:GoodeHomolosineProjection rdfs:label \"goode homolosine projection\"@en .\n")
ttlprojectionvocab.add("geocrs:GoodeHomolosineProjection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:HEALPixProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:HEALPixProjection rdfs:label \"HEALPix projection\"@en .\n")
ttlprojectionvocab.add("geocrs:HEALPixProjection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:BoggsEumorphicProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:BoggsEumorphicProjection rdfs:label \"boggs eumorphic projection\"@en .\n")
ttlprojectionvocab.add("geocrs:BoggsEumorphicProjection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:CrasterParabolicProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:CrasterParabolicProjection rdfs:label \"craster parabolic projection\"@en .\n")
ttlprojectionvocab.add("geocrs:CrasterParabolicProjection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:TheTimesProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:TheTimesProjection rdfs:label \"the times projection\"@en .\n")
ttlprojectionvocab.add("geocrs:TheTimesProjection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:DymaxionProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:DymaxionProjection rdfs:label \"dymaxion projection\"@en .\n")
ttlprojectionvocab.add("geocrs:DymaxionProjection rdfs:subClassOf geocrs:PolyhedralProjection, geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:MollweideProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:MollweideProjection rdfs:label \"mollweide projection\"@en .\n")
ttlprojectionvocab.add("geocrs:MollweideProjection skos:altLabel \"Babinet projection\"@en .\n")
ttlprojectionvocab.add("geocrs:MollweideProjection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:MyrahedalProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:MyrahedalProjection rdfs:label \"myrahedal projection\"@en .\n")
ttlprojectionvocab.add("geocrs:MyrahedalProjection rdfs:subClassOf geocrs:PolyhedralProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:BaconGlobularProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:BaconGlobularProjection rdfs:label \"bacon globular projection\"@en .\n")
ttlprojectionvocab.add("geocrs:BaconGlobularProjection rdfs:subClassOf geocrs:GlobularProjection .\n")
ttlprojectionvocab.add("geocrs:NicolosiGlobularProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:NicolosiGlobularProjection rdfs:label \"nicolosi globular projection\"@en .\n")
ttlprojectionvocab.add("geocrs:NicolosiGlobularProjection rdfs:subClassOf geocrs:GlobularProjection, geocrs:PolyconicProjection .\n")
ttlprojectionvocab.add("geocrs:ApianGlobularIProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:ApianGlobularIProjection rdfs:label \"apian globular I projection\"@en .\n")
ttlprojectionvocab.add("geocrs:ApianGlobularIProjection rdfs:subClassOf geocrs:GlobularProjection .\n")
ttlprojectionvocab.add("geocrs:ApianIIProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:ApianIIProjection rdfs:label \"apian II projection\"@en .\n")
ttlprojectionvocab.add("geocrs:ApianIIProjection rdfs:subClassOf geocrs:PseudocylindricalProjection .\n")
ttlprojectionvocab.add("geocrs:FournierGlobularIProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:FournierGlobularIProjection rdfs:label \"fournier globular I projection\"@en .\n")
ttlprojectionvocab.add("geocrs:FournierGlobularIProjection rdfs:subClassOf geocrs:GlobularProjection .\n")
ttlprojectionvocab.add("geocrs:WagnerIVProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:WagnerIVProjection rdfs:label \"wagner IV projection\"@en .\n")
ttlprojectionvocab.add("geocrs:WagnerIVProjection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:WagnerVIIProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:WagnerVIIProjection rdfs:label \"wagner VII projection\"@en .\n")
ttlprojectionvocab.add("geocrs:WagnerVIIProjection rdfs:subClassOf geocrs:PseudoAzimuthalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:AtlantisProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:AtlantisProjection rdfs:label \"atlantis projection\"@en .\n")
ttlprojectionvocab.add("geocrs:AtlantisProjection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:BertinProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:BertinProjection rdfs:label \"bertin projection\"@en .\n")
ttlprojectionvocab.add("geocrs:BertinProjection rdfs:subClassOf geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:AiryProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:AiryProjection rdfs:label \"airy projection\"@en .\n")
ttlprojectionvocab.add("geocrs:AiryProjection rdfs:subClassOf geocrs:AzimuthalProjection, geocrs:MinimumErrorProjection .\n")
ttlprojectionvocab.add("geocrs:WiechelProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:WiechelProjection rdfs:label \"wiechel projection\"@en .\n")
ttlprojectionvocab.add("geocrs:WiechelProjection rdfs:subClassOf geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:TiltedPerspectiveProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:TiltedPerspectiveProjection rdfs:label \"tilted perspective projection\"@en .\n")
ttlprojectionvocab.add("geocrs:TiltedPerspectiveProjection rdfs:subClassOf geocrs:PerspectiveProjection .\n")
ttlprojectionvocab.add("geocrs:FaheyProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:FaheyProjection rdfs:label \"fahey projection\"@en .\n")
ttlprojectionvocab.add("geocrs:FaheyProjection rdfs:subClassOf geocrs:PseudocylindricalProjection .\n")
ttlprojectionvocab.add("geocrs:FairgrieveProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:FairgrieveProjection rdfs:label \"fairgrieve projection\"@en .\n")
ttlprojectionvocab.add("geocrs:BriesemeisterProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:BriesemeisterProjection rdfs:label \"briesemeister projection\"@en .\n")
ttlprojectionvocab.add("geocrs:BriesemeisterProjection rdfs:subClassOf geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:WernerProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:WernerProjection rdfs:label \"werner projection\"@en .\n")
ttlprojectionvocab.add("geocrs:WernerProjection rdfs:subClassOf geocrs:PseudoConicalProjection, geocrs:EqualAreaProjection, geocrs:CordiformProjection .\n")
ttlprojectionvocab.add("geocrs:EquirectangularProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:EquirectangularProjection rdfs:label \"equirectangular projection\"@en .\n")
ttlprojectionvocab.add("geocrs:EquirectangularProjection rdfs:subClassOf geocrs:CylindricalProjection, geocrs:EquidistantProjection .\n")
ttlprojectionvocab.add("geocrs:ConicalProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:ConicalProjection rdfs:label \"conical projection\"@en .\n")
ttlprojectionvocab.add("geocrs:ConicalProjection rdfs:subClassOf geocrs:Projection .\n")
ttlprojectionvocab.add("geocrs:ObliqueMercatorProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:ObliqueMercatorProjection rdfs:label \"oblique mercator projection\"@en .\n")
ttlprojectionvocab.add("geocrs:ObliqueMercatorProjection rdfs:subClassOf geocrs:MercatorProjection, geocrs:CylindricalProjection, geocrs:ObliqueProjection .\n")
ttlprojectionvocab.add("geocrs:SpaceObliqueMercatorProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:SpaceObliqueMercatorProjection rdfs:label \"space oblique mercator projection\"@en .\n")
ttlprojectionvocab.add("geocrs:SpaceObliqueMercatorProjection rdfs:subClassOf geocrs:ObliqueMercatorProjection .\n")
ttlprojectionvocab.add("geocrs:PolyhedralProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:PolyhedralProjection rdfs:label \"polyhedral projection\"@en .\n")
ttlprojectionvocab.add("geocrs:PolyhedralProjection rdfs:subClassOf geocrs:Projection .\n")
ttlprojectionvocab.add("geocrs:PseudoCylindricalProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:PseudoCylindricalProjection rdfs:label \"pseudo-cylindrical projection\"@en .\n")
ttlprojectionvocab.add("geocrs:PseudoCylindricalProjection rdfs:subClassOf geocrs:Projection .\n")
ttlprojectionvocab.add("geocrs:PseudoAzimuthalProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:PseudoAzimuthalProjection rdfs:label \"pseudo-azimuthal projection\"@en .\n")
ttlprojectionvocab.add("geocrs:PseudoAzimuthalProjection rdfs:subClassOf geocrs:Projection .\n")
ttlprojectionvocab.add("geocrs:CylindricalProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:CylindricalProjection rdfs:label \"cylindrical projection\"@en .\n")
ttlprojectionvocab.add("geocrs:CylindricalProjection rdfs:subClassOf geocrs:Projection .\n")
ttlprojectionvocab.add("geocrs:EqualAreaProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:EqualAreaProjection rdfs:label \"equal-area projection\"@en .\n")
ttlprojectionvocab.add("geocrs:EqualAreaProjection rdfs:subClassOf geocrs:Projection .\n")
ttlprojectionvocab.add("geocrs:AmericanPolyconicProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:AmericanPolyconicProjection  rdfs:label \"american polyconic projection\"@en .\n")
ttlprojectionvocab.add("geocrs:AmericanPolyconicProjection  rdfs:subClassOf geocrs:PseudoConicalProjection, geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:RectangularPolyconicProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:RectangularPolyconicProjection  rdfs:label \"rectangular polyconic projection\"@en .\n")
ttlprojectionvocab.add("geocrs:RectangularPolyconicProjection  rdfs:subClassOf geocrs:PolyconicProjection, geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:ObliqueProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:ObliqueProjection rdfs:label \"oblique projection\"@en .\n")
ttlprojectionvocab.add("geocrs:ObliqueProjection skos:definition \"a projection made by parallel lines drawn from every point of a figure and meeting the plane of projection obliquely\"@en .\n")
ttlprojectionvocab.add("geocrs:ObliqueProjection rdfs:subClassOf geocrs:Projection .\n")
ttlprojectionvocab.add("geocrs:LoximuthalProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:LoximuthalProjection rdfs:label \"loximuthal projection\"@en .\n")
ttlprojectionvocab.add("geocrs:LoximuthalProjection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:AlbersEqualAreaProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:AlbersEqualAreaProjection rdfs:label \"albers equal-area projection\"@en .\n")
ttlprojectionvocab.add("geocrs:AlbersEqualAreaProjection skos:definition \"a conic, equal area map projection that uses two standard parallels\"@en .\n")
ttlprojectionvocab.add("geocrs:AlbersEqualAreaProjection rdfs:subClassOf geocrs:EqualAreaProjection, geocrs:ConicalProjection .\n")
ttlprojectionvocab.add("geocrs:WinkelTripelProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:WinkelTripelProjection rdfs:label \"winkel tripel projection\"@en .\n")
ttlprojectionvocab.add("geocrs:WinkelTripelProjection rdfs:subClassOf geocrs:PseudoAzimuthalProjection, geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:NellProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:NellProjection rdfs:label \"nell projection\"@en .\n")
ttlprojectionvocab.add("geocrs:NellProjection rdfs:subClassOf geocrs:PseudoCylindricalProjection .\n")
ttlprojectionvocab.add("geocrs:OctantProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:OctantProjection rdfs:label \"octant projection\"@en .\n")
ttlprojectionvocab.add("geocrs:OctantProjection rdfs:subClassOf geocrs:PolyhedralProjection, geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:EqualEarthProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:EqualEarthProjection rdfs:label \"equal earth projection\"@en .\n")
ttlprojectionvocab.add("geocrs:EqualEarthProjection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:NaturalEarthProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:NaturalEarthProjection rdfs:label \"natural earth projection\"@en .\n")
ttlprojectionvocab.add("geocrs:NaturalEarthProjection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:OrthographicProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:OrthographicProjection rdfs:label \"orthographic projection\"@en .\n")
ttlprojectionvocab.add("geocrs:OrthographicProjection rdfs:subClassOf geocrs:AzimuthalProjection, geocrs:PerspectiveProjection .\n")
ttlprojectionvocab.add("geocrs:LabordeProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:LabordeProjection rdfs:label \"laborde projection\"@en .\n")
ttlprojectionvocab.add("geocrs:LabordeProjection rdfs:subClassOf geocrs:CylindricalProjection, geocrs:ConformalProjection .\n")
ttlprojectionvocab.add("geocrs:GnomonicProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:GnomonicProjection rdfs:label \"gnomonic projection\"@en .\n")
ttlprojectionvocab.add("geocrs:GnomonicProjection skos:definition \"A map projection which displays all great circles as straight lines, resulting in any straight line segment on a gnomonic map showing a geodesic, the shortest route between the segment's two endpoints\"@en .")
ttlprojectionvocab.add("geocrs:GnomonicProjection rdfs:subClassOf geocrs:AzimuthalProjection .\n")
ttlprojectionvocab.add("geocrs:CassiniProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:CassiniProjection rdfs:label \"cassini projection\"@en .\n")
ttlprojectionvocab.add("geocrs:CassiniProjection rdfs:subClassOf geocrs:CylindricalProjection, geocrs:EquidistantProjection .\n")
ttlprojectionvocab.add("geocrs:AitoffProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:AitoffProjection rdfs:label \"aitoff projection\"@en .\n")
ttlprojectionvocab.add("geocrs:AitoffProjection rdfs:subClassOf geocrs:PseudoAzimuthalProjection, geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:AitoffObliqueProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:AitoffObliqueProjection rdfs:label \"aitoff oblique projection\"@en .\n")
ttlprojectionvocab.add("geocrs:AitoffObliqueProjection rdfs:subClassOf geocrs:PseudoAzimuthalProjection, geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:CompromiseProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:CompromiseProjection rdfs:label \"compromise projection\"@en .\n")
ttlprojectionvocab.add("geocrs:CompromiseProjection rdfs:subClassOf geocrs:Projection .\n")
ttlprojectionvocab.add("geocrs:HammerProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:HammerProjection rdfs:label \"hammer projection\"@en .\n")
ttlprojectionvocab.add("geocrs:HammerProjection rdfs:subClassOf geocrs:PseudoAzimuthalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:TwoPointEquidistantProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:TwoPointEquidistantProjection rdfs:label \"two-point equidistance projection\"@en .\n")
ttlprojectionvocab.add("geocrs:TwoPointEquidistantProjection rdfs:subClassOf geocrs:AzimuthalProjection, geocrs:EquidistantProjection .\n")
ttlprojectionvocab.add("geocrs:SinusoidalProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:SinusoidalProjection rdfs:label \"sinusoidal projection\"@en .\n")
ttlprojectionvocab.add("geocrs:SinusoidalProjection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:EqualAreaProjection, geocrs:EquidistantProjection .\n")
ttlprojectionvocab.add("geocrs:PseudoConicalProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:PseudoConicalProjection rdfs:label \"pseudo-conical projection\"@en .\n")
ttlprojectionvocab.add("geocrs:PseudoConicalProjection rdfs:subClassOf geocrs:Projection .\n")
ttlprojectionvocab.add("geocrs:ColombiaUrbanProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:ColombiaUrbanProjection rdfs:label \"colombia urban projection\"@en .\n")
ttlprojectionvocab.add("geocrs:ColombiaUrbanProjection rdfs:subClassOf geocrs:Projection .\n")
ttlprojectionvocab.add("geocrs:StereographicProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:StereographicProjection rdfs:label \"stereographic projection\"@en .\n")
ttlprojectionvocab.add("geocrs:StereographicProjection skos:definition \"A projection which can be constructed using the tangent's points antipoide as the point of perspective\"@en .\n")
ttlprojectionvocab.add("geocrs:StereographicProjection rdfs:subClassOf geocrs:ConformalProjection, geocrs:AzimuthalProjection .\n")
ttlprojectionvocab.add("geocrs:ObliqueStereographicProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:ObliqueStereographicProjection rdfs:label \"oblique stereographic projection\"@en .\n")
ttlprojectionvocab.add("geocrs:ObliqueStereographicProjection rdfs:subClassOf geocrs:CylindricalProjection, geocrs:ObliqueProjection .\n")
ttlprojectionvocab.add("geocrs:MercatorProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:MercatorProjection rdfs:label \"mercator projection\"@en .\n")
ttlprojectionvocab.add("geocrs:MercatorProjection rdfs:subClassOf geocrs:ConformalProjection, geocrs:CylindricalProjection .\n")
ttlprojectionvocab.add("geocrs:BraunPerspectiveProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:BraunPerspectiveProjection rdfs:label \"Braun perspective projection\"@en .\n")
ttlprojectionvocab.add("geocrs:BraunPerspectiveProjection rdfs:subClassOf geocrs:CylindricalProjection .\n")
ttlprojectionvocab.add("geocrs:BreusingGeometricProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:BreusingGeometricProjection rdfs:label \"breusing geometric projection\"@en .\n")
ttlprojectionvocab.add("geocrs:BreusingGeometricProjection rdfs:subClassOf geocrs:AzimuthalProjection .\n")
ttlprojectionvocab.add("geocrs:BreusingHarmonicProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:BreusingHarmonicProjection rdfs:label \"breusing harmonic projection\"@en .\n")
ttlprojectionvocab.add("geocrs:BreusingHarmonicProjection rdfs:subClassOf geocrs:AzimuthalProjection .\n")
ttlprojectionvocab.add("geocrs:BottomleyProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:BottomleyProjection rdfs:label \"bottomley projection\"@en .\n")
ttlprojectionvocab.add("geocrs:BottomleyProjection rdfs:subClassOf geocrs:PseudoConicalProjection, geocrs:EqualAreaProjection .\n")
ttlprojectionvocab.add("geocrs:VanDerGrintenIProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:VanDerGrintenIProjection rdfs:label \"van der grinten I projection\"@en .\n")
ttlprojectionvocab.add("geocrs:VanDerGrintenIProjection rdfs:subClassOf geocrs:CompromiseProjection, geocrs:PolyconicProjection .\n")
ttlprojectionvocab.add("geocrs:VanDerGrintenIIProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:VanDerGrintenIIProjection rdfs:label \"van der grinten II projection\"@en .\n")
ttlprojectionvocab.add("geocrs:VanDerGrintenIIProjection rdfs:subClassOf geocrs:CompromiseProjection, geocrs:PolyconicProjection .\n")
ttlprojectionvocab.add("geocrs:VanDerGrintenIIIProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:VanDerGrintenIIIProjection rdfs:label \"van der grinten III projection\"@en .\n")
ttlprojectionvocab.add("geocrs:VanDerGrintenIIIProjection rdfs:subClassOf geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:VanDerGrintenIVProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:VanDerGrintenIVProjection rdfs:label \"van der grinten IV projection\"@en .\n")
ttlprojectionvocab.add("geocrs:VanDerGrintenIVProjection rdfs:subClassOf geocrs:PolyconicProjection, geocrs:GlobularProjection .\n")
ttlprojectionvocab.add("geocrs:RobinsonProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:RobinsonProjection rdfs:label \"robinson projection\"@en .\n")
ttlprojectionvocab.add("geocrs:RobinsonProjection rdfs:subClassOf geocrs:PseudoCylindricalProjection, geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:WebMercatorProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:WebMercatorProjection rdfs:label \"web mercator projection\"@en .\n")
ttlprojectionvocab.add("geocrs:WebMercatorProjection rdfs:subClassOf geocrs:CylindricalProjection, geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:MillerProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:MillerProjection rdfs:label \"miller projection\"@en .\n")
ttlprojectionvocab.add("geocrs:MillerProjection rdfs:subClassOf geocrs:CylindricalProjection, geocrs:CompromiseProjection .\n")
ttlprojectionvocab.add("geocrs:Krovak rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:Krovak rdfs:label \"krovak projection\"@en .\n")
ttlprojectionvocab.add("geocrs:Krovak rdfs:subClassOf geocrs:ConicalProjection .\n")
ttlprojectionvocab.add("geocrs:TransverseMercatorProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:TransverseMercatorProjection rdfs:label \"transverse mercator projection\"@en .\n")
ttlprojectionvocab.add("geocrs:TransverseMercatorProjection rdfs:subClassOf geocrs:MercatorProjection .\n")
ttlprojectionvocab.add("geocrs:UniversalTransverseMercatorProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:UniversalTransverseMercatorProjection rdfs:label \"universal transverse mercator projection\"@en .\n")
ttlprojectionvocab.add("geocrs:UniversalTransverseMercatorProjection rdfs:subClassOf geocrs:TransverseMercatorProjection .\n")
ttlprojectionvocab.add("geocrs:LambertConformalConicProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:LambertConformalConicProjection rdfs:label \"lambert conformal conic projection\"@en .\n")
ttlprojectionvocab.add("geocrs:LambertConformalConicProjection rdfs:subClassOf geocrs:ConformalProjection, geocrs:ConicalProjection .\n")
ttlprojectionvocab.add("geocrs:CylindricalEqualArea rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:CylindricalEqualArea rdfs:label \"cylindrical equal area projection\"@en .\n")
ttlprojectionvocab.add("geocrs:CylindricalEqualArea rdfs:subClassOf geocrs:EqualAreaProjection, geocrs:CylindricalProjection .\n")
ttlprojectionvocab.add("geocrs:LambertAzimuthalEqualArea rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:LambertAzimuthalEqualArea rdfs:label \"lambert azimuthal equal area projection\"@en .\n")
ttlprojectionvocab.add("geocrs:LambertAzimuthalEqualArea rdfs:subClassOf geocrs:EqualAreaProjection, geocrs:AzimuthalProjection .\n")
ttlprojectionvocab.add("geocrs:EquidistantCylindricalProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:EquidistantCylindricalProjection rdfs:label \"equidistant cylindrical projection\"@en .\n")
ttlprojectionvocab.add("geocrs:EquidistantCylindricalProjection rdfs:subClassOf geocrs:EquidistantProjection, geocrs:CylindricalProjection .\n")
ttlprojectionvocab.add("geocrs:EquidistantConicProjection rdf:type owl:Class .\n")
ttlprojectionvocab.add("geocrs:EquidistantConicProjection rdfs:label \"equidistant conic projection\"@en .\n")
ttlprojectionvocab.add("geocrs:EquidistantConicProjection rdfs:subClassOf geocrs:EquidistantProjection, geocrs:ConicalProjection .\n")
ttlnoniso.union(ttlprojectionvocab)
ttl.add("geocrs:OperationParameter rdf:type owl:Class .\n")
ttl.add("geocrs:OperationParameter rdfs:label \"operation parameter\"@en .\n")
ttl.add("geocrs:OperationParameter skos:definition \"Parameter used by a method to perform some coordinate operation\"@en .\n")
ttl.add("geocrs:OperationValue rdf:type owl:Class .\n")
ttl.add("geocrs:OperationValue rdfs:label \"operation value\"@en .\n")
ttl.add("geocrs:OperationValue skos:definition \"Value of a parameter used by a method to perform some coordinate operation\"@en .\n")
ttl.add("geocrs:CoordinateOperation rdf:type owl:Class .\n")
ttl.add("geocrs:CoordinateOperation rdfs:label \"coordinate operation\"@en .\n")
ttl.add("geocrs:CoordinateOperation skos:definition \"mathematical operation (a) on coordinates that transforms or converts them from one coordinate reference system to another coordinate reference system, or (b) that decribes the change of coordinate values within one coordinate reference system due to the motion of the point between one coordinate epoch and another coordinate epoch\"@en .\n")
ttl.add("geocrs:CoordinateOperation rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:2DCoordinateTransformationOperation rdf:type owl:Class .\n")
ttl.add("geocrs:2DCoordinateTransformationOperation rdfs:subClassOf geocrs:CoordinateTransformationOperation .\n")
ttl.add("geocrs:2DCoordinateTransformationOperation rdfs:label \"2d coordinate transformation operation\"@en .\n")
ttl.add("geocrs:2DCoordinateTransformationOperation skos:definition \"Coordinate operation in which the two 2-dimensional coordinate reference systems are based on different datums\"@en .\n")
ttl.add("geocrs:2DCoordinateTransformationOperation rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:3DCoordinateTransformationOperation rdf:type owl:Class .\n")
ttl.add("geocrs:3DCoordinateTransformationOperation rdfs:subClassOf geocrs:CoordinateTransformationOperation .\n")
ttl.add("geocrs:3DCoordinateTransformationOperation rdfs:label \"3d coordinate transformation operation\"@en .\n")
ttl.add("geocrs:3DCoordinateTransformationOperation skos:definition \"Coordinate operation in which the two 3-dimensional coordinate reference systems are based on different datums\"@en .\n")
ttl.add("geocrs:3DCoordinateTransformationOperation rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:AffineTransformation rdf:type owl:Class .\n")
ttl.add("geocrs:AffineTransformation rdfs:subClassOf geocrs:Transformation .\n")
ttl.add("geocrs:AffineTransformation rdfs:label \"affine coordinate transformation operation\"@en .\n")
ttl.add("geocrs:ReflectionOperation rdf:type owl:Class .\n")
ttl.add("geocrs:ReflectionOperation rdfs:subClassOf geocrs:AffineTransformation .\n")
ttl.add("geocrs:ReflectionOperation rdfs:label \"reflection transformation operation\"@en .\n")
ttl.add("geocrs:ScaleOperation rdf:type owl:Class .\n")
ttl.add("geocrs:ScaleOperation rdfs:subClassOf geocrs:AffineTransformation .\n")
ttl.add("geocrs:ScaleOperation rdfs:label \"scale transformation operation\"@en .\n")
planetvocab.add("geocrs:InterstellarBody rdf:type owl:Class .\n")
planetvocab.add("geocrs:InterstellarBody rdfs:label \"interstellar body\"@en .\n")
planetvocab.add("geocrs:Planet rdf:type owl:Class .\n")
planetvocab.add("geocrs:Planet rdfs:label \"planet\"@en .\n")
planetvocab.add("geocrs:Planet rdfs:subClassOf geocrs:InterstellarBody .\n")
planetvocab.add("geocrs:DwarfPlanet rdf:type owl:Class .\n")
planetvocab.add("geocrs:DwarfPlanet rdfs:label \"dwarf planet\"@en .\n")
planetvocab.add("geocrs:DwarfPlanet rdfs:subClassOf geocrs:Planet .\n")
planetvocab.add("geocrs:Plutoid rdf:type owl:Class .\n")
planetvocab.add("geocrs:Plutoid rdfs:label \"plutoid\"@en .\n")
planetvocab.add("geocrs:Plutoid rdfs:subClassOf geocrs:DwarfPlanet .\n")
planetvocab.add("geocrs:NaturalSatellite rdf:type owl:Class .\n")
planetvocab.add("geocrs:NaturalSatellite rdfs:label \"natural satellite\"@en .\n")
planetvocab.add("geocrs:NaturalSatellite skos:definition \"an interstellar body orbiting around another interstellar body\"@en .\n")
planetvocab.add("geocrs:NaturalSatellite rdfs:subClassOf geocrs:InterstellarBody .\n")
planetvocab.add("geocrs:Star rdf:type owl:Class .\n")
planetvocab.add("geocrs:Star rdfs:label \"star\"@en .\n")
planetvocab.add("geocrs:Star rdfs:subClassOf geocrs:InterstellarBody .\n")
planetvocab.add("geocrs:Moon rdf:type owl:Class .\n")
planetvocab.add("geocrs:Moon rdfs:label \"moon\"@en .\n")
planetvocab.add("geocrs:Moon rdfs:subClassOf geocrs:NaturalSatellite .\n")
planetvocab.add("geocrs:Comet rdf:type owl:Class .\n")
planetvocab.add("geocrs:Comet rdfs:label \"comet\"@en .\n")
planetvocab.add("geocrs:Comet rdfs:subClassOf geocrs:InterstellarBody .\n")
planetvocab.add("geocrs:ArtificialSatellite rdf:type owl:Class .\n")
planetvocab.add("geocrs:ArtificialSatellite rdfs:label \"artificial satellite\"@en .\n")
planetvocab.add("geocrs:ArtificialSatellite rdfs:subClassOf geocrs:InterstellarBody .\n")
planetvocab.add("geocrs:Asteroid rdf:type owl:Class .\n")
planetvocab.add("geocrs:Asteroid rdfs:label \"asteroid\"@en .\n")
planetvocab.add("geocrs:Asteroid rdfs:subClassOf geocrs:InterstellarBody .\n")
planetvocab.add("geocrs:satelliteOf rdf:type owl:ObjectProperty .\n")
planetvocab.add("geocrs:satelliteOf rdfs:label \"satellite of\"@en .\n")
planetvocab.add("geocrs:satelliteOf skos:definition \"Defines an interstellar body as the natural satellite of another interstellar body.\"@en .\n")
planetvocab.add("geocrs:satelliteOf rdfs:domain geocrs:InterstellarBody .\n")
planetvocab.add("geocrs:satelliteOf rdfs:range geocrs:InterstellarBody .\n")
planetvocab.add("geocrs:planet_status rdf:type owl:ObjectProperty .\n")
planetvocab.add("geocrs:planet_status rdfs:label \"planet status\"@en .\n")
planetvocab.add("geocrs:planet_status skos:definition \"The status of the discovery of the planet, e.g. confirmed, unsure etc.\"@en .\n")
planetvocab.add("geocrs:planet_status rdfs:domain geocrs:InterstellarBody .\n")
planetvocab.add("geocrs:planet_status rdfs:range geocrs:PlanetStatus .\n")
ttlnoniso.union(planetvocab)
ttlnoniso.union(csvocab)
ttlnoniso.add("geocrs:GeoSPARQLSRS rdf:type owl:Ontology .\n")
ttlnoniso.add("geocrs:GeoSPARQLSRS dc:creator wd:Q67624599 .\n")
ttlnoniso.add("geocrs:GeoSPARQLSRS dc:description \"This ontology models spatial reference systems\"@en .\n")
ttlnoniso.add("geocrs:GeoSPARQLSRS rdfs:label \"GeoSPARQL SRS Ontology Draft NonISO classes\"@en .\n")
ttlnoniso.add("geocrs:RotationOperation rdf:type owl:Class .\n")
ttlnoniso.add("geocrs:RotationOperation rdfs:subClassOf geocrs:AffineTransformation .\n")
ttlnoniso.add("geocrs:RotationOperation rdfs:label \"rotation transformation operation\"@en .\n")
ttlnoniso.add("geocrs:TranslationOperation rdf:type owl:Class .\n")
ttlnoniso.add("geocrs:TranslationOperation rdfs:subClassOf geocrs:AffineTransformation .\n")
ttlnoniso.add("geocrs:TranslationOperation rdfs:label \"translation transformation operation\"@en .\n")
ttlnoniso.add("geocrs:IdentityOperation rdf:type owl:Class .\n")
ttlnoniso.add("geocrs:IdentityOperation rdfs:subClassOf geocrs:AffineTransformation .\n")
ttlnoniso.add("geocrs:IdentityOperation rdfs:label \"identity transformation operation\"@en .\n")
ttlnoniso.add("geocrs:ShearOperation rdf:type owl:Class .\n")
ttlnoniso.add("geocrs:ShearOperation rdfs:subClassOf geocrs:AffineTransformation .\n")
ttlnoniso.add("geocrs:ShearOperation rdfs:label \"shear transformation operation\"@en .\n")
ttlnoniso.add("geocrs:asProj4 rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:asProj4 rdfs:label \"asProj4\"@en .\n")
ttlnoniso.add("geocrs:asProj4 skos:definition \"proj4 representation of the CRS\"@en .\n")
ttlnoniso.add("geocrs:asProj4 rdfs:range xsd:string .\n")
ttlnoniso.add("geocrs:asProj4 rdfs:domain geocrs:CRS, geocrs:CoordinateSystem, geocrs:PrimeMeridian .\n")
ttlnoniso.add("geocrs:asProjJSON rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:asProjJSON rdfs:label \"asProjJSON\"@en .\n")
ttlnoniso.add("geocrs:asProjJSON skos:definition \"ProjJSON representation of the CRS\"@en .\n")
ttlnoniso.add("geocrs:asProjJSON rdfs:range xsd:string .\n")
ttlnoniso.add("geocrs:asProjJSON rdfs:domain geocrs:CRS, geocrs:CoordinateSystem, geocrs:PrimeMeridian .\n")
ttlnoniso.add("geocrs:isProjected rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:isProjected rdfs:label \"isProjected\"@en .\n")
ttlnoniso.add("geocrs:isProjected skos:definition \"Indicates if the spatial reference system is projected\"@en .\n")
ttlnoniso.add("geocrs:isProjected rdfs:range xsd:boolean .\n")
ttlnoniso.add("geocrs:isProjected rdfs:domain geocrs:CRS .\n")
ttlnoniso.add("geocrs:isGeographic rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:isGeographic rdfs:label \"isGeographic\"@en .\n")
ttlnoniso.add("geocrs:isGeographic skos:definition \"Indicates if the spatial reference system is geographic\"@en .\n")
ttlnoniso.add("geocrs:isGeographic rdfs:range xsd:boolean .\n")
ttlnoniso.add("geocrs:isGeographic rdfs:domain geocrs:CRS .\n")
ttlnoniso.add("geocrs:isBound rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:isBound rdfs:label \"isBound\"@en .\n")
ttlnoniso.add("geocrs:isBound skos:definition \"Indicates if the spatial reference system is bound\"@en .\n")
ttlnoniso.add("geocrs:isBound rdfs:range xsd:boolean .\n")
ttlnoniso.add("geocrs:isBound rdfs:domain geocrs:CRS .\n")
ttlnoniso.add("geocrs:longitude rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:longitude rdfs:label \"longitude\"@en .\n")
ttlnoniso.add("geocrs:longitude skos:definition \"Longitude of a prime meridian\"@en .\n")
ttlnoniso.add("geocrs:longitude rdfs:range xsd:double .\n")
ttlnoniso.add("geocrs:longitude rdfs:domain geocrs:PrimeMeridian .\n")
ttlnoniso.add("geocrs:isGeocentric rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:isGeocentric rdfs:label \"isGeocentric\"@en .\n")
ttlnoniso.add("geocrs:isGeocentric skos:definition \"Indicates if the spatial reference system is geocentric\"@en .\n")
ttlnoniso.add("geocrs:isGeocentric rdfs:range xsd:boolean .\n")
ttlnoniso.add("geocrs:isGeocentric rdfs:domain geocrs:CRS .\n")
ttlnoniso.add("geocrs:isDeprecated rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:isDeprecated rdfs:label \"isDeprecated\"@en .\n")
ttlnoniso.add("geocrs:isDeprecated skos:definition \"Indicates if the spatial reference system is deprecated\"@en .\n")
ttlnoniso.add("geocrs:isDeprecated rdfs:range xsd:boolean .\n")
ttlnoniso.add("geocrs:isDeprecated rdfs:domain geocrs:CRS .\n")
ttlnoniso.add("geocrs:isVertical rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:isVertical rdfs:label \"isVertical\"@en .\n")
ttlnoniso.add("geocrs:isVertical skos:definition \"Indicates if the spatial reference system is vertical\"@en .\n")
ttlnoniso.add("geocrs:isVertical rdfs:range xsd:boolean .\n")
ttlnoniso.add("geocrs:isVertical rdfs:domain geocrs:CRS .\n")
ttlnoniso.add("geocrs:asWKT rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:asWKT rdfs:label \"asWKT\"@en .\n")
ttlnoniso.add("geocrs:asWKT rdfs:range geocrs:wktLiteral .\n")
ttlnoniso.add("geocrs:asWKT skos:definition \"WKT representation of the CRS\"@en .\n")
ttlnoniso.add("geocrs:asWKT rdfs:domain geocrs:CRS, geocrs:CoordinateSystem, geocrs:PrimeMeridian .\n")
ttlnoniso.add("geocrs:unit rdf:type owl:ObjectProperty .\n")
ttlnoniso.add("geocrs:unit rdfs:label \"unit\"@en .\n")
ttlnoniso.add("geocrs:unit rdfs:domain geocrs:CRS .\n")
ttlnoniso.add("geocrs:unit rdfs:range om:Unit .\n")
ttl.add("geocrs:coordinateSystem rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:coordinateSystem rdfs:label \"coordinate system\"@en .\n")
ttl.add("geocrs:coordinateSystem skos:definition \"Associates a coordinate system with a coordinate reference system\"@en .\n")
ttl.add("geocrs:coordinateSystem rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:coordinateSystem rdfs:range geocrs:SingleCRS .\n")
ttl.add("geocrs:sourceCRS rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:sourceCRS rdfs:label \"source CRS\"@en .\n")
ttl.add("geocrs:sourceCRS skos:definition \"The dimension of the coordinate reference system associated with the data used as input of an operation\"@en .\n")
ttl.add("geocrs:sourceCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:sourceCRS rdfs:domain geocrs:CoordinateOperation .\n")
ttl.add("geocrs:sourceCRS rdfs:range geocrs:CRS .\n")
ttl.add("geocrs:targetCRS rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:targetCRS rdfs:label \"target CRS\"@en .\n")
ttl.add("geocrs:targetCRS skos:definition \"The dimension of the coordinate reference system associated with the data obtained as output of an operation\"@en .\n")
ttl.add("geocrs:targetCRS rdfs:domain geocrs:CoordinateOperation .\n")
ttl.add("geocrs:targetCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:targetCRS rdfs:range geocrs:CRS .\n")
ttl.add("geocrs:datum rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:datum rdfs:label \"datum\"@en .\n")
ttl.add("geocrs:datum skos:definition \"Associates a datum with a coordinate reference system\"@en .\n")
ttl.add("geocrs:datum rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:datum rdfs:domain geocrs:DatumEnsemble .\n")
ttl.add("geocrs:datum rdfs:range geocrs:Datum, geocrs:SingleCRS .\n")
ttl.add("geocrs:includesSRS rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:includesSRS rdfs:label \"includes srs\"@en .\n")
ttl.add("geocrs:includesSRS skos:definition \"Indicates spatial reference systems used by a compound reference system\"@en .\n")
ttl.add("geocrs:includesSRS rdfs:domain geocrs:CompoundCRS .\n")
ttl.add("geocrs:includesSRS rdfs:range geocrs:CRS .\n")
ttlnoniso.add("geocrs:usage rdf:type owl:ObjectProperty .\n")
ttlnoniso.add("geocrs:usage rdfs:label \"usage\"@en .\n")
ttlnoniso.add("geocrs:usage skos:definition \"Indicates an application of an SRS for which this datum may be used\"@en .\n")
ttlnoniso.add("geocrs:usage rdfs:domain geocrs:Datum .\n")
ttlnoniso.add("geocrs:usage rdfs:range geocrs:SRSApplication .\n")
ttl.add("geocrs:axis rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:axis rdfs:label \"axis\"@en .\n")
ttl.add("geocrs:axis skos:definition \"An axis used by some ellipsoidal or cartesian coordinate system\"@en .\n")
ttl.add("geocrs:axis rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:axis rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:axis rdfs:range geocrs:CoordinateSystemAxis .\n")
ttlnoniso.add("geocrs:area_of_use rdf:type owl:ObjectProperty .\n")
ttlnoniso.add("geocrs:area_of_use rdfs:label \"area of use\"@en .\n")
ttlnoniso.add("geocrs:area_of_use skos:definition \"Defines an area of use of an operation\"@en .\n")
ttlnoniso.add("geocrs:area_of_use rdfs:range geocrs:AreaOfUse .\n")
ttlnoniso.add("geocrs:area_of_use rdfs:domain geocrs:ConcatenatedOperation, geocrs:Conversion, geocrs:Transformation, geocrs:OtherCoordinateOperation, geocrs:CoordinateOperation .\n")
ttl.add("geocrs:coordinateOperation rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:coordinateOperation rdfs:label \"coordinate operation\"@en .\n")
ttl.add("geocrs:coordinateOperation skos:definition \"Associates a coordinate operation with a CRS\"@en .\n")
ttl.add("geocrs:coordinateOperation rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:coordinateOperation rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:coordinateOperation rdfs:range geocrs:CoordinateOperation .\n")
ttl.add("geocrs:direction rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:direction rdfs:label \"cardinal direction\"@en .\n")
ttl.add("geocrs:direction skos:definition \"Associates a direction with a datum\"@en .\n")
ttl.add("geocrs:direction rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:direction rdfs:domain geocrs:CoordinateSystemAxis .\n")
ttl.add("geocrs:direction rdfs:range geocrs:AxisDirection .\n")
ttlnoniso.add("geocrs:unit_conversion_factor rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:unit_conversion_factor rdfs:label \"unit conversion factor\"@en .\n")
ttlnoniso.add("geocrs:unit_conversion_factor rdfs:domain geocrs:CoordinateSystemAxis .\n")
ttlnoniso.add("geocrs:unit_conversion_factor rdfs:range xsd:string .\n")
ttlnoniso.add("geocrs:isAppliedTo rdf:type owl:ObjectProperty .\n")
ttlnoniso.add("geocrs:isAppliedTo rdfs:label \"is applied to\"@en .\n")
ttlnoniso.add("geocrs:isAppliedTo skos:definition \"defines an srs application for which a srs definition has been used\"@en .\n")
ttlnoniso.add("geocrs:isAppliedTo rdfs:domain geocrs:ReferenceSystem .\n")
ttlnoniso.add("geocrs:isAppliedTo rdfs:range geocrs:SRSApplication .\n")
ttlnoniso.add("geocrs:uses rdf:type owl:ObjectProperty .\n")
ttlnoniso.add("geocrs:uses rdfs:label \"uses\"@en .\n")
ttlnoniso.add("geocrs:uses skos:definition \"defines an srs application which uses a given projection\"@en .\n")
ttlnoniso.add("geocrs:uses rdfs:domain geocrs:SRSApplication .\n")
ttlnoniso.add("geocrs:uses rdfs:range geocrs:Projection .\n")
ttlnoniso.add("geocrs:isApplicableTo rdf:type owl:ObjectProperty .\n")
ttlnoniso.add("geocrs:isApplicableTo rdfs:label \"is applicable to\"@en .\n")
ttlnoniso.add("geocrs:isApplicableTo skos:definition \"defines to which interstellar body the srs is applicable\"@en .\n")
ttlnoniso.add("geocrs:isApplicableTo rdfs:domain geocrs:SpatialReferenceSystem .\n")
ttlnoniso.add("geocrs:isApplicableTo rdfs:range geocrs:InterstellarBody .\n")
ttlnoniso.add("geocrs:approximates rdf:type owl:ObjectProperty .\n")
ttlnoniso.add("geocrs:approximates rdfs:label \"approximates\"@en .\n")
ttlnoniso.add("geocrs:approximates skos:definition \"defines an interstellar body which is approximated by the geoid\"@en .\n")
ttlnoniso.add("geocrs:approximates rdfs:domain geocrs:Geoid .\n")
ttlnoniso.add("geocrs:approximates rdfs:range geocrs:InterstellarBody .\n")
ttl.add("geocrs:abbreviation rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:abbreviation rdfs:label \"axis abbreviation\"@en .\n")
ttl.add("geocrs:abbreviation skos:definition \"The abbreviation used to identify an axis\"@en .\n")
ttl.add("geocrs:abbreviation rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:abbreviation rdfs:domain geocrs:CoordinateSystemAxis .\n")
ttl.add("geocrs:abbreviation rdfs:range xsd:string .\n")
ttlnoniso.add("geocrs:unit rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:unit rdfs:label \"unit\"@en .\n")
ttlnoniso.add("geocrs:unit rdfs:domain geocrs:CoordinateSystemAxis .\n")
ttlnoniso.add("geocrs:unit_auth_code rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:unit_auth_code rdfs:label \"unit auth code\"@en .\n")
ttlnoniso.add("geocrs:unit_auth_code rdfs:domain geocrs:CoordinateSystemAxis .\n")
ttlnoniso.add("geocrs:unit_auth_code rdfs:range xsd:string .\n")
ttlnoniso.add("geocrs:unit_code rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:unit_code rdfs:label \"unit code\"@en .\n")
ttlnoniso.add("geocrs:unit_code rdfs:domain geocrs:CoordinateSystemAxis .\n")
ttlnoniso.add("geocrs:unit_code rdfs:range xsd:string .\n")
ttlnoniso.add("geocrs:epsgCode rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:epsgCode rdfs:label \"epsgCode\"@en .\n")
ttlnoniso.add("geocrs:epsgCode rdfs:domain geocrs:CRS .\n")
ttlnoniso.add("geocrs:epsgCode rdfs:range xsd:string .\n")
ttlnoniso.add("geocrs:accuracy rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:accuracy rdfs:label \"accuracy\"@en .\n")
ttlnoniso.add("geocrs:accuracy rdfs:domain geocrs:CoordinateOperation .\n")
ttlnoniso.add("geocrs:accuracy rdfs:range xsd:double .\n")
ttlnoniso.add("geocrs:eccentricity rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:eccentricity rdfs:label \"eccentricity\"@en .\n")
ttlnoniso.add("geocrs:eccentricity skos:definition \"deviation of a curve or orbit from circularity\"@en .\n")
ttlnoniso.add("geocrs:eccentricity rdfs:domain geocrs:Geoid .\n")
ttlnoniso.add("geocrs:eccentricity rdfs:range xsd:double .\n")
ttl.add("geocrs:coordinateEpoch rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:coordinateEpoch rdfs:label \"coordinate epoch\"@en .\n")
ttl.add("geocrs:coordinateEpoch rdfs:domain geocrs:DynamicCRS .\n")
ttl.add("geocrs:coordinateEpoch rdfs:range xsd:double .\n")
ttlnoniso.add("geocrs:flatteningParameter rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:flatteningParameter rdfs:label \"flattening parameter\"@en .\n")
ttlnoniso.add("geocrs:flatteningParameter rdfs:domain geocrs:Geoid .\n")
ttlnoniso.add("geocrs:flatteningParameter rdfs:range xsd:double .\n")
planetvocab.add("geocrs:orbital_period rdf:type owl:DatatypeProperty .\n")
planetvocab.add("geocrs:orbital_period rdfs:label \"orbital period\"@en .\n")
planetvocab.add("geocrs:orbital_period rdfs:domain geocrs:InterstellarBody .\n")
planetvocab.add("geocrs:orbital_period rdfs:range xsd:double .\n")
planetvocab.add("geocrs:radius rdf:type owl:DatatypeProperty .\n")
planetvocab.add("geocrs:radius rdfs:label \"radius\"@en .\n")
planetvocab.add("geocrs:radius rdfs:domain geocrs:InterstellarBody .\n")
planetvocab.add("geocrs:radius rdfs:range xsd:double .\n")
planetvocab.add("geocrs:starDistance rdf:type owl:DatatypeProperty .\n")
planetvocab.add("geocrs:starDistance rdfs:label \"star distance\"@en .\n")
planetvocab.add("geocrs:starDistance skos:definition \"the distance of an interstellar body to the next star\"@en .\n")
planetvocab.add("geocrs:starDistance rdfs:domain geocrs:InterstellarBody .\n")
planetvocab.add("geocrs:starDistance rdfs:range xsd:double .\n")
planetvocab.add("geocrs:mass rdf:type owl:DatatypeProperty .\n")
planetvocab.add("geocrs:mass rdfs:label \"mass\"@en .\n")
planetvocab.add("geocrs:mass skos:definition \"the mass of an interstellar body\"@en .\n")
planetvocab.add("geocrs:mass rdfs:domain geocrs:InterstellarBody .\n")
planetvocab.add("geocrs:mass rdfs:range xsd:double .\n")
ttl.add("geocrs:semiMajorAxis rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:semiMajorAxis rdfs:label \"semi major axis\"@en .\n")
ttl.add("geocrs:semiMajorAxis skos:definition \"Indicates the length of the semi major axis of an ellipsoid\"@en .\n")
ttl.add("geocrs:semiMajorAxis rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:semiMajorAxis rdfs:domain geocrs:Geoid .\n")
ttl.add("geocrs:semiMajorAxis rdfs:range xsd:double .\n")
ttl.add("geocrs:semiMinorAxis rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:semiMinorAxis rdfs:label \"semi minor axis\"@en .\n")
ttl.add("geocrs:semiMinorAxis skos:definition \"Indicates the length of the semi minor axis of an ellipsoid\"@en .\n")
ttl.add("geocrs:semiMinorAxis rdfs:domain geocrs:Geoid .\n")
ttl.add("geocrs:semiMinorAxis rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:semiMinorAxis rdfs:range xsd:double .\n")
ttl.add("geocrs:isSphere rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:isSphere rdfs:label \"is sphere\"@en .\n")
ttl.add("geocrs:isSphere skos:definition \"Indicates whether the ellipsoid is a sphere\"@en .\n")
ttl.add("geocrs:isSphere rdfs:domain geocrs:Geoid .\n")
ttl.add("geocrs:isSphere rdfs:range xsd:double .\n")
ttlnoniso.add("geocrs:extent rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:extent rdfs:label \"extent\"@en .\n")
ttlnoniso.add("geocrs:extent skos:definition \"The extent of the area of use of a spatial reference system\"@en .\n")
ttlnoniso.add("geocrs:extent rdfs:domain geocrs:AreaOfUse .\n")
ttlnoniso.add("geocrs:extent rdfs:range geocrs:wktLiteral .\n")
ttlnoniso.add("geocrs:utm_zone rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:utm_zone rdfs:label \"utm zone\"@en .\n")
ttl.add("geocrs:scope rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:scope rdfs:label \"scope\"@en .\n")
ttl.add("geocrs:scope skos:definition \"the scope of the referring object\"@en .\n")
ttl.add("geocrs:scope rdfs:range xsd:string .\n")
ttlnoniso.add("geocrs:falseNorthing rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:falseNorthing rdfs:label \"false northing\"@en .\n")
ttlnoniso.add("geocrs:falseNorthing skos:definition \"A value relating to distance north of a standard latitude but with a constant added to make the numbers convenient\"@en .\n")
ttlnoniso.add("geocrs:falseNorthing rdfs:range xsd:string .\n")
ttlnoniso.add("geocrs:falseEasting rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:falseEasting rdfs:label \"false easting\"@en .\n")
ttlnoniso.add("geocrs:falseEasting skos:definition \"A value relating to distance east of a standard meridian but with a constant added to make the numbers convenient\"@en .\n")
ttlnoniso.add("geocrs:falseEasting rdfs:range xsd:string .\n")
ttlnoniso.add("geocrs:flatteningParameter rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:flatteningParameter rdfs:label \"flattening parameter\"@en .\n")
ttlnoniso.add("geocrs:flatteningParameter rdfs:range xsd:string .\n")
ttlnoniso.add("geocrs:inverse_flattening rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:inverse_flattening rdfs:label \"inverse flattening\"@en .\n")
ttlnoniso.add("geocrs:inverse_flattening skos:definition \"Indicates the inverse flattening value of an ellipsoid, expressed as a number or a ratio (percentage rate, parts per million, etc.)\"@en .\n")
ttlnoniso.add("geocrs:inverse_flattening rdfs:range xsd:double .\n")
ttlnoniso.add("geocrs:has_ballpark_transformation rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:has_ballpark_transformation rdfs:label \"has ballpark transformation\"@en .\n")
ttlnoniso.add("geocrs:has_ballpark_transformation rdfs:range xsd:boolean .\n")
ttlnoniso.add("geocrs:is_semi_minor_computed rdf:type owl:DatatypeProperty .\n")
ttlnoniso.add("geocrs:is_semi_minor_computed rdfs:label \"is semi minor computed\"@en .\n")
ttlnoniso.add("geocrs:is_semi_minor_computed rdfs:range xsd:double .\n")
geodcounter=1
graph = Graph()
graph.parse(data = ttlhead+"".join(ttl), format='turtle')
graph.serialize(destination='owl/ontology.ttl', format='turtle')
graph = Graph()
graph.parse(data = ttlhead+"".join(ttlnoniso), format='turtle')
graph.serialize(destination='owl/ontology_noniso.ttl', format='turtle')
graph = Graph()
graph.parse(data = ttlhead+"".join(ttlnoniso), format='turtle')
graph.parse("iso_changed_srsnamespace.ttl",format='turtle')
graph.serialize(destination='owl/ontology_isobased.ttl', format='turtle')

i=0
curname=""
mapp=pyproj.list.get_proj_operations_map()
ttldata=set()
parseAdditionalPlanetarySpheroids("exoplanet.eu_catalog.csv",ttldata)
parseSolarSystemSatellites("solar_system_satellites.csv",ttldata)
for x in list(range(2000,10000))+list(range(20000,30000)):
	try:
		curcrs=CRS.from_epsg(x)
		print("EPSG: "+str(x))
	except:
		continue
	crsToTTL(ttldata,curcrs,x,geodcounter,None)
crsToTTL(ttldata,CRS.from_wkt('GEOGCS["GCS_Moon_2000",DATUM["D_Moon_2000",SPHEROID["Moon_2000_IAU_IAG",1737400.0,0.0]],PRIMEM["Moon_Reference_Meridian",0.0],UNIT["Degree",0.0174532925199433]]'),"GCS_Moon",geodcounter,"geocrs:SelenographicCRS")
f = open("owl/result.nt", "w", encoding="utf-8")
f.write(ttlhead+"".join(ttl)+"".join(ttldata))
f.close()
graph2 = Graph()
graph2.parse(data = ttlhead+"".join(ttl)+"".join(ttldata), format='n3')
graph2.serialize(destination='owl/result.ttl', format='turtle')
graph2 = Graph()
graph2.parse(data = ttlhead+"".join(ttlnoniso)+"".join(ttldata), format='n3')
graph2.parse("iso_changed_srsnamespace.ttl",format='turtle')
graph2.serialize(destination='owl/result_iso.ttl', format='turtle')
graph3 = Graph()
graph3.parse(data = ttlhead+"".join(ttlprojectionvocab), format='n3')
graph3.serialize(destination='projection_vocabulary/projection_vocabulary.ttl', format='turtle')
graph4 = Graph()
graph4.parse(data = ttlhead+"".join(planetvocab), format='n3')
graph4.serialize(destination='planet_vocabulary/planet_vocabulary.ttl', format='turtle')
graph5 = Graph()
graph5.parse(data = ttlhead+"".join(csvocab), format='n3')
graph5.serialize(destination='cs_vocabulary/cs_vocabulary.ttl', format='turtle')
graph6 = Graph()
graph6.parse(data = ttlhead+"".join(srsapplication), format='n3')
graph6.serialize(destination='srs_application/srs_application.ttl', format='turtle')
ttldata=set()
crsToTTL(ttldata,CRS.from_epsg(7856),7856,geodcounter,None)
f2=open("owl/epsg7856.ttl","w",encoding="utf-8")
f2.write(ttlhead
         #+"".join(ttl)
         +"".join(ttldata))
f2.close()
ttldata=set()
crsToTTL(ttldata,CRS.from_epsg(32756),32756,geodcounter,None)
f3=open("owl/epsg32756.ttl","w",encoding="utf-8")
f3.write(ttlhead
         #+"".join(ttl)
         +"".join(ttldata))
f3.close()
ttldata=set()
crsToTTL(ttldata,CRS.from_epsg(8859),8859,geodcounter,None)
f4=open("owl/epsg8859.ttl","w",encoding="utf-8")
f4.write(ttlhead
         #+"".join(ttl)
         +"".join(ttldata))
f4.close()
#f = open("result.ttl", "w", encoding="utf-8")
#f.write(ttlhead)
#for line in ttl:
#	f.write(line)
#f.close()

