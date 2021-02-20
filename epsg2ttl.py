import os
import re
import pyproj
from pyproj import CRS


units={}
units["m"]="om:meter"
units["metre"]="om:metre"
units["degree"]="om:degree"
units["ft"]="om:foot"
units["us-ft"]="om:usfoot"
coordinatesystem={}
coordinatesystem["ellipsoidal"]="geo:EllipsoidalCoordinateSystem"
coordinatesystem["cartesian"]="geo:CartesianCoordinateSystem"
coordinatesystem["ft"]="om:foot"
coordinatesystem["us-ft"]="om:usfoot"
spheroids={}
spheroids["GRS80"]="geo:GRS80"
spheroids["GRS 80"]="geo:GRS80"
spheroids["GRS67"]="geo:GRS67"
spheroids["GRS 67"]="geo:GRS67"
spheroids["GRS1980"]="geo:GRS1980"
spheroids["GRS 1980"]="geo:GRS1980"
spheroids["intl"]="geo:International1924"
spheroids["aust_SA"]="geo:AustralianNationalSpheroid"
spheroids["Australian National Spheroid"]="geo:AustralianNationalSpheroid"
spheroids["International 1924"]="geo:International1924"
spheroids["clrk"]="geo:Clarke1866"
spheroids["evrst30"]="geo:Everest1930"
spheroids["clrk66"]="geo:Clarke1866"
spheroids["Clarke 1866"]="geo:Clarke1866"
spheroids["Clarke 1858"]="geo:Clarke1858"
spheroids["clrk80"]="geo:Clarke1880RGS"
spheroids["Clarke 1880 (RGS)"]="geo:Clarke1880RGS"
spheroids["Clarke 1880 (IGN)"]="geo:Clarke1880IGN"
spheroids["clrk80ign"]="geo:Clarke1880IGN"
spheroids["WGS66"]="geo:WGS66"
spheroids["WGS 66"]="geo:WGS66"
spheroids["WGS72"]="geo:WGS72"
spheroids["WGS 72"]="geo:WGS72"
spheroids["WGS84"]="geo:WGS84"
spheroids["WGS 84"]="geo:WGS84"
spheroids["Krassowsky 1940"]="geo:Krassowsky1940"
spheroids["krass"]="geo:Krassowsky1940"
spheroids["Bessel 1841"]="geo:Bessel1841"
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
ttl.add("geo:AreaOfUse rdf:type owl:Class .\n")
ttl.add("geo:AreaOfUse rdfs:label \"area of use\"@en .\n")
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
ttl.add("geo:GeographicCRS  rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:AffineCoordinateSystem rdfs:subClassOf geo:CoordinateSystem .\n")
ttl.add("geo:AffineCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geo:AffineCoordinateSystem owl:equivalentClass wd:Q382510 .\n")
ttl.add("geo:AffineCoordinateSystem rdfs:label \"Affine coordinate system\"@en .\n")
ttl.add("geo:AffineCoordinateSystem skos:definition \"coordinate system in Euclidean space with straight axes that are not necessarily mutually perpendicular\"@en .\n")
ttl.add("geo:AffineCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:GeodeticCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:GeodeticCRS rdf:type owl:Class .\n")
ttl.add("geo:GeodeticCRS rdfs:label \"Geodetic coordinate reference system\"@en .\n")
ttl.add("geo:GeodeticCRS skos:definition \"three-dimensional coordinate reference system based on a geodetic reference frame and having either a three-dimensional Cartesian or a spherical coordinate system\"@en .\n")
ttl.add("geo:GeodeticCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:CompoundCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:CompoundCRS rdf:type owl:Class .\n")
ttl.add("geo:CompoundCRS skos:definition \"coordinate reference system using at least two independent coordinate reference systems\"@en .\n")
ttl.add("geo:CompoundCRS rdfs:label \"Compound coordinate reference system\"@en .\n")
ttl.add("geo:CompoundCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:CoordinateTransformation rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:CoordinateTransformation rdf:type owl:Class .\n")
ttl.add("geo:CoordinateTransformation rdfs:label \"coordinate transformation\"@en .\n")
ttl.add("geo:CoordinateTransformation skos:definition \"coordinate operation that changes coordinates in a source coordinate reference system to coordinates in a target coordinate reference system in which the source and target coordinate reference systems are based on different datums\"@en .\n")
ttl.add("geo:BoundCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:BoundCRS rdf:type owl:Class .\n")
ttl.add("geo:BoundCRS rdfs:label \"Bound coordinate reference system\"@en .\n")
ttl.add("geo:BoundCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:TemporalCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:TemporalCRS rdf:type owl:Class .\n")
ttl.add("geo:TemporalCRS rdfs:label \"Temporal coordinate reference system\"@en .\n")
ttl.add("geo:TemporalCRS skos:definition \"coordinate reference system based on a temporal datum\"@en .\n")
ttl.add("geo:TemporalCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:ParametricCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:ParametricCRS rdf:type owl:Class .\n")
ttl.add("geo:ParametricCRS rdfs:label \"Parametric coordinate reference system\"@en .\n")
ttl.add("geo:ParametricCRS skos:definition \"one-dimensional coordinate system where the axis units are parameter values which are not inherently spatial\"@en .\n")
ttl.add("geo:ParametricCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:SpatioParametricCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:SpatioParametricCRS rdf:type owl:Class .\n")
ttl.add("geo:SpatioParametricCRS rdfs:label \"Spatio-Parametric coordinate reference system\"@en .\n")
ttl.add("geo:SpatioParametricCRS skos:definition \"compound coordinate reference system in which one constituent coordinate reference system is a spatial coordinate reference system and one is a parametric coordinate reference system\"@en .\n")
ttl.add("geo:SpatioParametricCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:DerivedGeographicCRS rdfs:subClassOf geo:GeodeticCRS .\n")
ttl.add("geo:DerivedGeographicCRS rdf:type owl:Class .\n")
ttl.add("geo:DerivedGeographicCRS rdfs:label \"Derived geographic coordinate reference system\"@en .\n")
ttl.add("geo:DerivedGeographicCRS skos:definition \"coordinate reference system that is defined through the application of a specified coordinate conversion to the coordinates within a previously established coordinate reference system\"@en .\n")
ttl.add("geo:DerivedGeographicCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:EngineeringCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:EngineeringCRS rdf:type owl:Class .\n")
ttl.add("geo:EngineeringCRS skos:definition \"coordinate reference system based on an engineering datum\"@en .\n")
ttl.add("geo:EngineeringCRS rdfs:label \"Engineering coordinate reference system\"@en .\n")
ttl.add("geo:EngineeringCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:VerticalCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:VerticalCRS rdf:type owl:Class .\n")
ttl.add("geo:VerticalCRS rdfs:label \"Vertical coordinate reference system\"@en .\n")
ttl.add("geo:VerticalCRS skos:definition \"one-dimensional coordinate reference system based on a vertical reference frame\"@en .\n")
ttl.add("geo:VerticalCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:SphericCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:SphericCRS rdf:type owl:Class .\n")
ttl.add("geo:SphericCRS rdfs:label \"Spheric coordinate reference system\"@en .\n")
ttl.add("geo:SphericCRS skos:definition \"three-dimensional coordinate system in Euclidean space in which position is specified by one distance coordinate and two angular coordinates\"@en .\n")
ttl.add("geo:SphericCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:GeocentricCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:GeocentricCRS rdf:type owl:Class .\n")
ttl.add("geo:GeocentricCRS rdfs:label \"Geocentric coordinate reference system\"@en .\n")
ttl.add("geo:GeocentricCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:GeodeticReferenceFrame rdfs:subClassOf geo:Datum .\n")
ttl.add("geo:GeodeticReferenceFrame rdf:type owl:Class .\n")
ttl.add("geo:GeodeticReferenceFrame rdfs:label \"Geodetic reference frame\"@en .\n")
ttl.add("geo:GeodeticReferenceFrame skos:definition \"reference frame describing the relationship of a two- or three-dimensional coordinate system to the Earth\"@en .\n")
ttl.add("geo:GeodeticReferenceFrame rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:DynamicReferenceFrame rdfs:subClassOf geo:Datum .\n")
ttl.add("geo:DynamicReferenceFrame rdf:type owl:Class .\n")
ttl.add("geo:DynamicReferenceFrame rdfs:label \"Dynamic reference frame\"@en .\n")
ttl.add("geo:DynamicReferenceFrame skos:definition \"reference frame in which the defining parameters include time evolution\"@en .\n")
ttl.add("geo:DynamicReferenceFrame rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:VerticalReferenceFrame rdfs:subClassOf geo:Datum .\n")
ttl.add("geo:VerticalReferenceFrame rdf:type owl:Class .\n")
ttl.add("geo:VerticalReferenceFrame rdfs:label \"Vertical reference frame\"@en .\n")
ttl.add("geo:VerticalReferenceFrame skos:definition \"reference frame describing the relation of gravity-related heights or depths to the Earth\"@en .\n")
ttl.add("geo:VerticalReferenceFrame rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:StaticCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:StaticCRS rdf:type owl:Class .\n")
ttl.add("geo:StaticCRS rdfs:label \"Static coordinate reference system\"@en .\n")
ttl.add("geo:StaticCRS skos:definition \"coordinate reference system that has a static reference frame\"@en .\n")
ttl.add("geo:StaticCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:ProjectedCRS rdfs:subClassOf geo:CRS .\n")
ttl.add("geo:ProjectedCRS rdf:type owl:Class .\n")
ttl.add("geo:ProjectedCRS rdfs:label \"Projected coordinate reference system\"@en .\n")
ttl.add("geo:ProjectedCRS skos:definition \"coordinate reference system derived from a geographic coordinate reference system by applying a map projection\"@en .\n")
ttl.add("geo:ProjectedCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:Datum rdf:type owl:Class .\n")
ttl.add("geo:Datum owl:equivalentClass wd:Q1502887 .\n")
ttl.add("geo:Datum rdfs:label \"datum\"@en .\n")
ttl.add("geo:Datum skos:definition \"specification of the relationship of a coordinate system to an object, thus creating a coordinate reference system\"@en .\n")
ttl.add("geo:Datum rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:TemporalDatum rdfs:subClassOf geo:Datum .\n")
ttl.add("geo:TemporalDatum rdf:type owl:Class .\n")
ttl.add("geo:TemporalDatum rdfs:label \"temporal datum\"@en .\n")
ttl.add("geo:TemporalDatum skos:definition \"coordinate reference system based on a temporal datum\"@en .\n")
ttl.add("geo:TemporalDatum rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:VerticalDatum rdfs:subClassOf geo:Datum .\n")
ttl.add("geo:VerticalDatum rdf:type owl:Class .\n")
ttl.add("geo:VerticalDatum rdfs:label \"vertical datum\"@en .\n")
ttl.add("geo:VerticalDatum skos:definition \"reference frame describing the relation of gravity-related heights or depths to the Earth\"@en .\n")
ttl.add("geo:VerticalDatum rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:EngineeringDatum rdfs:subClassOf geo:Datum .\n")
ttl.add("geo:EngineeringDatum rdf:type owl:Class .\n")
ttl.add("geo:EngineeringDatum rdfs:label \"engineering datum\"@en .\n")
ttl.add("geo:EngineeringDatum skos:definition \"datum describing the relationship of a coordinate system to a local reference\"@en .\n")
ttl.add("geo:EngineeringDatum rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:Ellipsoid rdf:type owl:Class .\n")
ttl.add("geo:Ellipsoid rdfs:label \"ellipsoid\"@en .\n")
ttl.add("geo:Ellipsoid skos:definition \"reference ellipsoid\"@en .\n")
ttl.add("geo:Ellipsoid rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:PrimeMeridian rdf:type owl:Class .\n")
ttl.add("geo:PrimeMeridian rdfs:label \"prime meridian\"@en .\n")
ttl.add("geo:PrimeMeridian skos:definition \"meridian from which the longitudes of other meridians are quantified\"@en .\n")
ttl.add("geo:PrimeMeridian rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geo:Projection rdf:type owl:Class .\n")
ttl.add("geo:Projection rdfs:label \"projection\"@en .\n")
ttl.add("geo:Axis rdf:type owl:Class .\n")
ttl.add("geo:Axis rdfs:label \"axis\"@en .\n")
ttl.add("geo:CoordinateOperation rdf:type owl:Class .\n")
ttl.add("geo:CoordinateOperation rdfs:label \"coordinate operation\"@en .\n")
ttl.add("geo:CoordinateConversionOperation rdfs:subClassOf geo:CoordinateOperation .\n")
ttl.add("geo:CoordinateConversionOperation rdf:type owl:Class .\n")
ttl.add("geo:CoordinateConversionOperation rdfs:label \"coordinate conversion operation\"@en .\n")
ttl.add("geo:CoordinateTransformationOperation rdfs:subClassOf geo:CoordinateOperation .\n")
ttl.add("geo:CoordinateTransformationOperation rdf:type owl:Class .\n")
ttl.add("geo:CoordinateTransformationOperation rdfs:label \"coordinate transformation operation\"@en .\n")
ttl.add("geo:CoordinateConcatenatedOperation rdfs:subClassOf geo:CoordinateOperation .\n")
ttl.add("geo:CoordinateConcatenatedOperation rdf:type owl:Class .\n")
ttl.add("geo:CoordinateConcatenatedOperation rdfs:label \"coordinate concatenated operation\"@en .\n")
ttl.add("geo:OtherCoordinateOperation rdfs:subClassOf geo:CoordinateOperation .\n")
ttl.add("geo:OtherCoordinateOperation rdf:type owl:Class .\n")
ttl.add("geo:OtherCoordinateOperation rdfs:label \"other coordinate operation\"@en .\n")
ttl.add("geo:CardinalDirection rdf:type owl:Class .\n")
ttl.add("geo:CardinalDirection rdfs:label \"cardinal direction\"@en .\n")
ttl.add("geo:asProj4 rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:asProj4 rdfs:label \"asProj4\"@en .\n")
ttl.add("geo:asProj4 skos:definition \"proj4 representation of the CRS\"@en .\n")
ttl.add("geo:asProj4 rdfs:range xsd:string .\n")
ttl.add("geo:asProj4 rdfs:domain geo:CRS .\n")
ttl.add("geo:asProjJSON rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:asProjJSON rdfs:label \"asProjJSON\"@en .\n")
ttl.add("geo:asProjJSON skos:definition \"ProjJSON representation of the CRS\"@en .\n")
ttl.add("geo:asProjJSON rdfs:range xsd:string .\n")
ttl.add("geo:asProjJSON rdfs:domain geo:CRS .\n")
ttl.add("geo:isProjected rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:isProjected rdfs:label \"isProjected\"@en .\n")
ttl.add("geo:isProjected rdfs:range xsd:boolean .\n")
ttl.add("geo:isProjected rdfs:domain geo:CRS .\n")
ttl.add("geo:isGeographic rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:isGeographic rdfs:label \"isGeographic\"@en .\n")
ttl.add("geo:isGeographic rdfs:range xsd:boolean .\n")
ttl.add("geo:isGeographic rdfs:domain geo:CRS .\n")
ttl.add("geo:isBound rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:isBound rdfs:label \"isBound\"@en .\n")
ttl.add("geo:isBound rdfs:range xsd:boolean .\n")
ttl.add("geo:isBound rdfs:domain geo:CRS .\n")
ttl.add("geo:isGeocentric rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:isGeocentric rdfs:label \"isGeocentric\"@en .\n")
ttl.add("geo:isGeocentric rdfs:range xsd:boolean .\n")
ttl.add("geo:isGeocentric rdfs:domain geo:CRS .\n")
ttl.add("geo:isVertical rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:isVertical rdfs:label \"isVertical\"@en .\n")
ttl.add("geo:isVertical rdfs:range xsd:boolean .\n")
ttl.add("geo:isVertical rdfs:domain geo:CRS .\n")
ttl.add("geo:asWKT rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:asWKT rdfs:label \"asWKT\"@en .\n")
ttl.add("geo:asWKT rdfs:range geo:wktLiteral .\n")
ttl.add("geo:asWKT skos:definition \"WKT representation of the CRS\"@en .\n")
ttl.add("geo:asWKT rdfs:domain geo:CRS .\n")
ttl.add("geo:unit rdf:type owl:ObjectProperty .\n")
ttl.add("geo:unit rdfs:label \"unit\"@en .\n")
ttl.add("geo:unit rdfs:domain geo:CRS .\n")
ttl.add("geo:unit rdfs:range om:Unit .\n")
ttl.add("geo:ellipse rdf:type owl:ObjectProperty .\n")
ttl.add("geo:ellipse rdfs:label \"ellipse\"@en .\n")
ttl.add("geo:ellipse rdfs:domain geo:CRS .\n")
ttl.add("geo:ellipse rdfs:domain geo:Datum .\n")
ttl.add("geo:ellipse rdfs:range geo:Ellipsoid .\n")
ttl.add("geo:primeMeridian rdf:type owl:ObjectProperty .\n")
ttl.add("geo:primeMeridian rdfs:label \"prime meridian\"@en .\n")
ttl.add("geo:primeMeridian rdfs:domain geo:Datum .\n")
ttl.add("geo:primeMeridian rdfs:domain geo:CRS .\n")
ttl.add("geo:projection rdf:type owl:ObjectProperty .\n")
ttl.add("geo:projection rdfs:label \"projection\"@en .\n")
ttl.add("geo:projection rdfs:domain geo:CRS .\n")
ttl.add("geo:projection rdfs:range geo:Projection .\n")
ttl.add("geo:coordinateSystem rdf:type owl:ObjectProperty .\n")
ttl.add("geo:coordinateSystem rdfs:label \"coordinate system\"@en .\n")
ttl.add("geo:coordinateSystem rdfs:domain geo:CRS .\n")
ttl.add("geo:coordinateSystem rdfs:range geo:CoordinateSystem .\n")
ttl.add("geo:datum rdf:type owl:ObjectProperty .\n")
ttl.add("geo:datum rdfs:label \"datum\"@en .\n")
ttl.add("geo:datum rdfs:domain geo:CRS .\n")
ttl.add("geo:datum rdfs:range geo:Datum .\n")
ttl.add("geo:axis rdf:type owl:ObjectProperty .\n")
ttl.add("geo:axis rdfs:label \"axis\"@en .\n")
ttl.add("geo:axis rdfs:domain geo:CRS .\n")
ttl.add("geo:axis rdfs:range geo:Axis .\n")
ttl.add("geo:area_of_use rdf:type owl:ObjectProperty .\n")
ttl.add("geo:area_of_use rdfs:label \"area of use\"@en .\n")
ttl.add("geo:coordinateOperation rdf:type owl:ObjectProperty .\n")
ttl.add("geo:coordinateOperation rdfs:label \"coordinate operation\"@en .\n")
ttl.add("geo:coordinateOperation rdfs:domain geo:CRS .\n")
ttl.add("geo:coordinateOperation rdfs:range geo:CoordinateOperation .\n")
ttl.add("geo:direction rdf:type owl:ObjectProperty .\n")
ttl.add("geo:direction rdfs:label \"cardinal direction\"@en .\n")
ttl.add("geo:direction rdfs:domain geo:Datum .\n")
ttl.add("geo:direction rdfs:range geo:CardinalDirection .\n")
ttl.add("geo:unit_conversion_factor rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:unit_conversion_factor rdfs:label \"unit conversion factor\"@en .\n")
ttl.add("geo:unit_conversion_factor rdfs:domain geo:Axis .\n")
ttl.add("geo:unit_conversion_factor rdfs:range xsd:string .\n")
ttl.add("geo:epsgCode rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:epsgCode rdfs:label \"epsgCode\"@en .\n")
ttl.add("geo:epsgCode rdfs:domain geo:CRS .\n")
ttl.add("geo:epsgCode rdfs:range xsd:string .\n")
ttl.add("geo:accuracy rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:accuracy rdfs:label \"accuracy\"@en .\n")
ttl.add("geo:accuracy rdfs:domain geo:CoordinateOperation .\n")
ttl.add("geo:accuracy rdfs:range xsd:double .\n")
ttl.add("geo:envelope rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:envelope rdfs:label \"envelope\"@en .\n")
ttl.add("geo:envelope rdfs:domain geo:CRS .\n")
ttl.add("geo:envelope rdfs:range geo:wktLiteral .\n")
ttl.add("geo:utm_zone rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:utm_zone rdfs:label \"utm zone\"@en .\n")
ttl.add("geo:scope rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:scope rdfs:label \"scope\"@en .\n")
ttl.add("geo:scope rdfs:range xsd:string .\n")
ttl.add("geo:inverse_flattening rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:inverse_flattening rdfs:label \"inverse flattening\"@en .\n")
ttl.add("geo:inverse_flattening rdfs:range xsd:double .\n")
ttl.add("geo:has_ballpark_transformation rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:has_ballpark_transformation rdfs:label \"has ballpark transformation\"@en .\n")
ttl.add("geo:has_ballpark_transformation rdfs:range xsd:boolean .\n")
ttl.add("geo:semi_major_metre rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:semi_major_metre rdfs:label \"semi major metre\"@en .\n")
ttl.add("geo:semi_major_metre rdfs:range xsd:double .\n")
ttl.add("geo:is_semi_minor_computed rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:is_semi_minor_computed rdfs:label \"is semi minor computed\"@en .\n")
ttl.add("geo:is_semi_minor_computed rdfs:range xsd:double .\n")
ttl.add("geo:semi_minor_metre rdf:type owl:DatatypeProperty .\n")
ttl.add("geo:semi_minor_metre rdfs:label \"semi minor metre\"@en .\n")
ttl.add("geo:semi_minor_metre rdfs:range xsd:double .\n")
f = open("ontology.ttl", "w", encoding="utf-8")
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
		if "Projected CRS" in curcrs.type_name:
			ttl.add("geoepsg:"+epsgcode+" rdf:type geo:ProjectedCRS .\n")
		elif "Geographic 2D CRS" in curcrs.type_name:
			ttl.add("geoepsg:"+epsgcode+" rdf:type geo:GeographicCRS .\n")
		elif "Geocentric CRS" in curcrs.type_name:
			ttl.add("geoepsg:"+epsgcode+" rdf:type geo:GeocentricCRS .\n")
		elif "Compound CRS" in curcrs.type_name:
			ttl.add("geoepsg:"+epsgcode+" rdf:type geo:CompoundCRS .\n")
		else:
			ttl.add("geoepsg:"+epsgcode+" rdf:type geo:CRS .\n")
		ttl.add("geoepsg:"+epsgcode+" rdf:type owl:NamedIndividual .\n")
		ttl.add("geoepsg:"+epsgcode+" rdfs:label \""+curname.strip()+"\"@en .\n")
		if curcrs.area_of_use!=None:
			ttl.add("geoepsg:"+epsgcode+" geo:envelope \"ENVELOPE("+str(curcrs.area_of_use.west)+" "+str(curcrs.area_of_use.south)+","+str(curcrs.area_of_use.east)+" "+str(curcrs.area_of_use.north)+")\"^^geo:wktLiteral . \n")
		ttl.add("geoepsg:"+epsgcode+" geo:isBound \""+str(curcrs.is_bound).lower()+"\"^^xsd:boolean . \n")
		if curcrs.coordinate_system!=None and curcrs.coordinate_system.name in coordinatesystem:
			ttl.add("geoepsg:"+epsgcode+" geo:coordinateSystem "+coordinatesystem[curcrs.coordinate_system.name]+" . \n")		
		elif  curcrs.coordinate_system!=None:
			ttl.add("geoepsg:"+epsgcode+" geo:coordinateSystem \""+str(curcrs.coordinate_system)+"\"^^xsd:string . \n")
		if curcrs.coordinate_operation!=None:
			coordoperationid=curcrs.coordinate_operation.name.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_").replace(",","_").replace("&","and").strip()
			ttl.add("geoepsg:"+epsgcode+" geo:coordinateOperation geoepsg:"+str(coordoperationid)+" . \n")
			ttl.add("geoepsg:"+str(coordoperationid)+" geo:accuracy \""+str(curcrs.coordinate_operation.accuracy)+"\"^^xsd:double . \n")
			ttl.add("geoepsg:"+str(coordoperationid)+" geo:scope \""+str(curcrs.coordinate_operation.scope)+"\"^^xsd:string . \n")
			ttl.add("geoepsg:"+str(coordoperationid)+" geo:has_ballpark_transformation \""+str(curcrs.coordinate_operation.has_ballpark_transformation)+"\"^^xsd:boolean . \n")
			ttl.add("geoepsg:"+str(coordoperationid)+" geo:grids \""+str(curcrs.coordinate_operation.grids).replace("\n","").replace("\"","'")+"\"^^xsd:string . \n")
			if curcrs.coordinate_operation.area_of_use!=None:
				ttl.add("geoepsg:"+str(coordoperationid)+" geo:area_of_use geoepsg:"+str(coordoperationid)+"_area_of_use . \n")
				ttl.add("geoepsg:"+str(coordoperationid)+"_area_of_use"+" rdf:type geo:AreaOfUse .\n")
				ttl.add("geoepsg:"+str(coordoperationid)+"_area_of_use"+" rdfs:label \""+str(curcrs.coordinate_operation.area_of_use.name).replace("\"","'")+"\"@en .\n")
				ttl.add("geoepsg:"+str(coordoperationid)+"_area_of_use"+" geo:envelope \"ENVELOPE("+str(curcrs.area_of_use.west)+" "+str(curcrs.area_of_use.south)+","+str(curcrs.area_of_use.east)+" "+str(curcrs.area_of_use.north)+")\"^^geo:wktLiteral . \n")
			for par in curcrs.coordinate_operation.params:
				ttl.add(" geo:"+str(par.name).replace(" ","_")+" rdf:type owl:DatatypeProperty . \n") 
				ttl.add(" geo:"+str(par.name).replace(" ","_")+" rdfs:range xsd:double . \n") 
				ttl.add(" geo:"+str(par.name).replace(" ","_")+" rdfs:domain geo:CoordinateOperation . \n") 
				ttl.add(" geo:"+str(par.name).replace(" ","_")+" rdfs:label \""+str(par.name)+"\"@en . \n")				
				ttl.add("geoepsg:"+str(coordoperationid)+" geo:"+str(par.name).replace(" ","_")+" \""+str(par.value)+"\"^^xsd:double . \n") 
			if curcrs.coordinate_operation.type_name==None:
				ttl.add("geoepsg:"+str(coordoperationid)+" rdf:type geo:CoordinateOperation . \n")
			elif curcrs.coordinate_operation.type_name=="Conversion":
				ttl.add("geoepsg:"+str(coordoperationid)+" rdf:type geo:CoordinateConversionOperation . \n")
			elif curcrs.coordinate_operation.type_name=="Transformation":
				ttl.add("geoepsg:"+str(coordoperationid)+" rdf:type geo:CoordinateTransformationOperation . \n")
			elif curcrs.coordinate_operation.type_name=="Concatenated Operation":
				ttl.add("geoepsg:"+str(coordoperationid)+" rdf:type geo:CoordinateConcatenatedOperation . \n")
			elif curcrs.coordinate_operation.type_name=="Other Coordinate Operation":
				ttl.add("geoepsg:"+str(coordoperationid)+" rdf:type geo:OtherCoordinateOperation . \n")
			ttl.add("geoepsg:"+str(coordoperationid)+" rdfs:label \""+curcrs.coordinate_operation.name+": "+curcrs.coordinate_operation.method_name+"\"@en . \n")
		if curcrs.prime_meridian!=None:
			ttl.add("geoepsg:"+epsgcode+" geo:primeMeridian geoepsg:"+curcrs.prime_meridian.name.replace(" ","")+" . \n")
			ttl.add("geoepsg:"+curcrs.prime_meridian.name.replace(" ","")+" rdf:type geo:PrimeMeridian . \n")
			ttl.add("geoepsg:"+curcrs.prime_meridian.name.replace(" ","")+" rdfs:label \""+curcrs.prime_meridian.name+"\"@en . \n")
		if curcrs.datum!=None:
			datumid=str(curcrs.datum.name.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_").replace("+","_plus"))
			ttl.add("geoepsg:"+epsgcode+" geo:datum geoepsg:"+str(datumid)+" . \n")
			if "Geodetic Reference Frame" in curcrs.datum.type_name:
				ttl.add("geoepsg:"+str(datumid)+" rdf:type geo:GeodeticReferenceFrame . \n")
			else:
				ttl.add("geoepsg:"+str(datumid)+" rdf:type geo:Datum . \n")
			ttl.add("geoepsg:"+str(datumid)+" rdfs:label \""+curcrs.datum.name+"\"@en . \n")
			if curcrs.datum.ellipsoid.name in spheroids:
				ttl.add("geoepsg:"+str(datumid)+" geo:ellipse "+spheroids[curcrs.datum.ellipsoid.name]+" . \n")
				ttl.add(spheroids[curcrs.datum.ellipsoid.name]+" rdfs:label \""+str(curcrs.datum.ellipsoid.name)+"\"@en . \n")
				ttl.add(spheroids[curcrs.datum.ellipsoid.name]+" rdf:type geo:Ellipsoid .\n")	
				ttl.add(spheroids[curcrs.datum.ellipsoid.name]+" geo:inverse_flattening \""+str(curcrs.datum.ellipsoid.inverse_flattening)+"\"^^xsd:double .\n")
				ttl.add(spheroids[curcrs.datum.ellipsoid.name]+" geo:semi_minor_metre \""+str(curcrs.datum.ellipsoid.semi_minor_metre)+"\"^^xsd:double .\n")
				ttl.add(spheroids[curcrs.datum.ellipsoid.name]+" geo:semi_major_metre \""+str(curcrs.datum.ellipsoid.semi_major_metre)+"\"^^xsd:double .\n")			
				if curcrs.datum.ellipsoid.remarks!=None:
					ttl.add(spheroids[curcrs.datum.ellipsoid.name]+" rdfs:comment \""+str(curcrs.datum.ellipsoid.remarks)+"\"^^xsd:string .\n")
				ttl.add(spheroids[curcrs.datum.ellipsoid.name]+" geo:is_semi_minor_computed \""+str(curcrs.datum.ellipsoid.is_semi_minor_computed).lower()+"\"^^xsd:boolean .\n")
			else:	
				ttl.add("geoepsg:"+str(datumid)+" geo:ellipse \""+curcrs.datum.ellipsoid.name+"\" . \n")
			ttl.add("geoepsg:"+str(datumid)+" geo:primeMeridian geoepsg:"+curcrs.datum.prime_meridian.name.replace(" ","")+" . \n")
			ttl.add("geoepsg:"+curcrs.datum.prime_meridian.name.replace(" ","")+" rdf:type geo:PrimeMeridian . \n")				
		ttl.add("geoepsg:"+epsgcode+" geo:isVertical \""+str(curcrs.is_vertical).lower()+"\"^^xsd:boolean . \n")
		ttl.add("geoepsg:"+epsgcode+" geo:isProjected \""+str(curcrs.is_projected).lower()+"\"^^xsd:boolean . \n")
		ttl.add("geoepsg:"+epsgcode+" geo:isGeocentric \""+str(curcrs.is_geocentric).lower()+"\"^^xsd:boolean . \n")
		ttl.add("geoepsg:"+epsgcode+" geo:isGeographic \""+str(curcrs.is_geographic).lower()+"\"^^xsd:boolean . \n")
		if curcrs.utm_zone!=None:
			ttl.add("geoepsg:"+epsgcode+" geo:utm_zone \""+str(curcrs.utm_zone)+"\"^^xsd:string . \n")
		if curcrs.axis_info!=None:
			for axis in curcrs.axis_info:
				axisid=axis.name.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_")+"_"+axis.unit_name.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_")+"_"+axis.direction.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_")
				ttl.add("geoepsg:"+epsgcode+" geo:axis geoepsg:"+axisid+" . \n")
				ttl.add("geoepsg:"+axisid+" rdf:type geo:Axis . \n")
				ttl.add("geoepsg:"+axisid+" geo:direction geoepsg:"+axis.direction+" . \n")	
				ttl.add("geoepsg:"+axisid+" geo:unit_conversion_factor \""+str(axis.unit_conversion_factor)+"\"^^xsd:double . \n")	
				ttl.add("geoepsg:"+axis.direction+" rdf:type geo:CardinalDirection . \n")
				ttl.add("geoepsg:"+axis.direction+" rdfs:label \""+axis.direction+"\"@en . \n")					
				ttl.add("geoepsg:"+axisid+" rdfs:label \""+axis.name+"\"@en . \n")
				if axis.unit_name in units:
					ttl.add("geoepsg:"+axisid+" geo:unit "+units[axis.unit_name]+" . \n")	
				else:
					ttl.add("geoepsg:"+axisid+" geo:unit \""+axis.unit_name+"\"@en . \n")					
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
					ttl.add(projections[param[1].strip()]+" rdfs:label \""+param[1].strip()+"\"@en .\n")
				else:
					ttl.add("geoepsg:"+epsgcode+" geo:projection \""+param[1].strip()+"\" . \n")
			elif param[0]=="ellps":
				if param[1].strip() in spheroids:
					ttl.add("geoepsg:"+epsgcode+" geo:ellipse "+spheroids[param[1].strip()]+" . \n")
					ttl.add(spheroids[param[1].strip()]+" rdfs:label \""+str(curcrs.ellipsoid)+"\"@en . \n")
					ttl.add(spheroids[param[1].strip()]+" rdf:type geo:Ellipsoid .\n")
					ttl.add(spheroids[param[1].strip()]+" rdfs:label \""+param[1].strip()+"\"@en .\n")						
				else:	
					ttl.add("geoepsg:"+epsgcode+" geo:ellipse \""+param[1].strip()+"\" . \n")
			elif param[0]=="units":
				if param[1].strip() in units:
					ttl.add("geoepsg:"+epsgcode+" geo:unit om:"+units[param[1].strip()]+" . \n")
					ttl.add(units[param[1].strip()]+" rdf:type om:Unit .\n")					
				else:
					ttl.add("geoepsg:"+epsgcode+" geo:unit \""+param[1].strip()+"\" . \n")				
	i+=1
f = open("result.ttl", "w", encoding="utf-8")
f.write(ttlhead)
for line in ttl:
	f.write(line)
f.close()
