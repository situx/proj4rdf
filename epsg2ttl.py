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
coordinatesystem["ellipsoidal"]="geocrs:EllipsoidalCoordinateSystem"
coordinatesystem["cartesian"]="geocrs:CartesianCoordinateSystem"
coordinatesystem["ft"]="om:foot"
coordinatesystem["us-ft"]="om:usfoot"
spheroids={}
spheroids["GRS80"]="geocrs:GRS80"
spheroids["GRS 80"]="geocrs:GRS80"
spheroids["GRS67"]="geocrs:GRS67"
spheroids["GRS 67"]="geocrs:GRS67"
spheroids["GRS1980"]="geocrs:GRS1980"
spheroids["GRS 1980"]="geocrs:GRS1980"
spheroids["intl"]="geocrs:International1924"
spheroids["aust_SA"]="geocrs:AustralianNationalSpheroid"
spheroids["Australian National Spheroid"]="geocrs:AustralianNationalSpheroid"
spheroids["International 1924"]="geocrs:International1924"
spheroids["clrk"]="geocrs:Clarke1866"
spheroids["evrst30"]="geocrs:Everest1930"
spheroids["clrk66"]="geocrs:Clarke1866"
spheroids["Clarke 1866"]="geocrs:Clarke1866"
spheroids["Clarke 1858"]="geocrs:Clarke1858"
spheroids["clrk80"]="geocrs:Clarke1880RGS"
spheroids["Clarke 1880 (RGS)"]="geocrs:Clarke1880RGS"
spheroids["Clarke 1880 (IGN)"]="geocrs:Clarke1880IGN"
spheroids["clrk80ign"]="geocrs:Clarke1880IGN"
spheroids["WGS66"]="geocrs:WGS66"
spheroids["WGS 66"]="geocrs:WGS66"
spheroids["WGS72"]="geocrs:WGS72"
spheroids["WGS 72"]="geocrs:WGS72"
spheroids["WGS84"]="geocrs:WGS84"
spheroids["WGS 84"]="geocrs:WGS84"
spheroids["Krassowsky 1940"]="geocrs:Krassowsky1940"
spheroids["krass"]="geocrs:Krassowsky1940"
spheroids["Bessel 1841"]="geocrs:Bessel1841"
spheroids["bessel"]="geocrs:Bessel1841"
projections={}
projections["latlong"]="geocrs:LatLonProjection"
projections["longlat"]="geocrs:LonLatProjection"
projections["tmerc"]="geocrs:TransverseMercator"
projections["omerc"]="geocrs:LambertConformalConic"
projections["merc"]="geocrs:Mercator"
projections["sterea"]="geocrs:ObliqueStereographic"
projections["cea"]="geocrs:CylindricalEqualArea"
projections["stere"]="geocrs:Stereographic"
projections["eqc"]="geocrs:EquidistantCylindrical"
projections["laea"]="geocrs:LambertAzimuthalEqualArea"
projections["utm"]="geocrs:UTM"
projections["krovak"]="geocrs:Krovak"
projections["lcc"]="geocrs:LambertConformalConic"
projections["geocent"]="geocrs:Geocentric"
ttl=set()
ttlhead="@prefix rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"
ttlhead+="@prefix rdfs:<http://www.w3.org/2000/01/rdf-schema#> .\n"
ttlhead+="@prefix owl:<http://www.w3.org/2002/07/owl#> .\n"
ttlhead+="@prefix xsd:<http://www.w3.org/2001/XMLSchema#> .\n"
ttlhead+="@prefix skos:<http://www.w3.org/2004/02/skos/core#> .\n"
ttlhead+="@prefix geoepsg:<http://www.opengis.net/def/crs/EPSG/0/> .\n"
ttlhead+="@prefix geo:<http://www.opengis.net/ont/geosparql#> .\n"
ttlhead+="@prefix geocrs:<http://www.opengis.net/ont/crs#> .\n"
ttlhead+="@prefix dc:<http://purl.org/dc/elements/1.1/> .\n"
ttlhead+="@prefix wd:<http://www.wikidata.org/entity/> .\n"
ttlhead+="@prefix om:<http://www.ontology-of-units-of-measure.org/resource/om-2/> .\n"
ttl.add("geocrs:GeoSPARQLCRS rdf:type owl:Ontology .\n")
ttl.add("geocrs:GeoSPARQLCRS dc:creator wd:Q67624599 .\n")
ttl.add("geocrs:GeoSPARQLCRS dc:description \"This ontology models coordinate reference systems\"@en .\n")
ttl.add("geocrs:GeoSPARQLCRS rdfs:label \"GeoSPARQL CRS Ontology Draft\"@en .\n")
ttl.add("owl:versionInfo rdfs:label \"0.1\"^^xsd:double .\n")
ttl.add("geocrs:ReferenceSystem rdf:type owl:Class .\n")
ttl.add("geocrs:ReferenceSystem rdfs:label \"reference system\"@en .\n")
ttl.add("geocrs:TemporalReferenceSystem rdf:type owl:Class .\n")
ttl.add("geocrs:TemporalReferenceSystem rdfs:label \"temporal reference system\"@en .\n")
ttl.add("geocrs:TemporalReferenceSystem rdfs:subClassOf geocrs:ReferenceSystem .\n")
ttl.add("geocrs:SpatialReferenceSystem rdf:type owl:Class .\n")
ttl.add("geocrs:SpatialReferenceSystem rdfs:label \"spatial reference system\"@en .\n")
ttl.add("geocrs:SpatialReferenceSystem rdfs:subClassOf geocrs:ReferenceSystem .\n")
ttl.add("geocrs:CoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:CoordinateSystem rdfs:label \"Coordinate system\"@en .\n")
ttl.add("geocrs:CoordinateSystem skos:definition \"non-repeating sequence of coordinate system axes that spans a given coordinate space\"@en .\n")
ttl.add("geocrs:CoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:AreaOfUse rdf:type owl:Class .\n")
ttl.add("geocrs:AreaOfUse rdfs:label \"area of use\"@en .\n")
ttl.add("geocrs:CartesianCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:CartesianCoordinateSystem rdfs:subClassOf geocrs:AffineCoordinateSystem .\n")
ttl.add("geocrs:CartesianCoordinateSystem rdfs:label \"Cartesian coordinate system\"@en .\n")
ttl.add("geocrs:CartesianCoordinateSystem skos:definition \"coordinate system in Euclidean space which gives the position of points relative to n mutually perpendicular straight axes all having the same unit of measure\"@en .\n")
ttl.add("geocrs:CartesianCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:LinearCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:LinearCoordinateSystem rdfs:subClassOf geocrs:CoordinateSystem .\n")
ttl.add("geocrs:LinearCoordinateSystem rdfs:label \"Linear coordinate system\"@en .\n")
ttl.add("geocrs:LinearCoordinateSystem skos:definition \"one-dimensional coordinate system in which a linear feature forms the axis\"@en .\n")
ttl.add("geocrs:LinearCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:EngineeringCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:EngineeringCoordinateSystem rdfs:subClassOf geocrs:CoordinateSystem .\n")
ttl.add("geocrs:EngineeringCoordinateSystem rdfs:label \"Engineering coordinate system\"@en .\n")
ttl.add("geocrs:EngineeringCoordinateSystem skos:definition \"coordinate system used by an engineering coordinate reference system, one of an affine coordinate system, a Cartesian coordinate system, a cylindrical coordinate system, a linear coordinate sytem, an ordinal coordinate system, a polar coordinate system or a spherical coordinate system\"@en .\n")
ttl.add("geocrs:EngineeringCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:GeodeticCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:GeodeticCoordinateSystem rdfs:subClassOf geocrs:CoordinateSystem .\n")
ttl.add("geocrs:GeodeticCoordinateSystem rdfs:label \"Geodetic coordinate system\"@en .\n")
ttl.add("geocrs:GeodeticCoordinateSystem skos:definition \"coordinate system used by a Geodetic CRS, one of a Cartesian coordinate system or a spherical coordinate system\"@en .\n")
ttl.add("geocrs:GeodeticCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:EllipsoidalCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:EllipsoidalCoordinateSystem rdfs:subClassOf geocrs:CoordinateSystem .\n")
ttl.add("geocrs:EllipsoidalCoordinateSystem rdfs:label \"Ellipsoidal coordinate system\"@en .\n")
ttl.add("geocrs:EllipsoidalCoordinateSystem skos:definition \"two- or three-dimensional coordinate system in which position is specified by geodetic latitude, geodetic longitude, and (in the three-dimensional case) ellipsoidal height\"@en .\n")
ttl.add("geocrs:EllipsoidalCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:OrdinalCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:OrdinalCoordinateSystem rdfs:subClassOf geocrs:CoordinateSystem .\n")
ttl.add("geocrs:OrdinalCoordinateSystem rdfs:label \"Ordinal coordinate system\"@en .\n")
ttl.add("geocrs:OrdinalCoordinateSystem skos:definition \"n-dimensional coordinate system in which every axis uses integers\"@en .\n")
ttl.add("geocrs:OrdinalCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DerivedProjectedCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:DerivedProjectedCoordinateSystem  rdfs:subClassOf geocrs:CoordinateSystem .\n")
ttl.add("geocrs:DerivedProjectedCoordinateSystem  rdfs:label \"derived projected coordinate system\"@en .\n")
ttl.add("geocrs:DerivedProjectedCoordinateSystem  skos:definition \"coordinate system used by a DerivedProjected CRS, one of an affine coordinate system, a Cartesian coordinate system, a cylindrical coordinate system, an ordinal coordinate system, a polar coordinate system or a spherical coordinate system\"@en .\n")
ttl.add("geocrs:DerivedProjectedCoordinateSystem  rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:SphericalCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:SphericalCoordinateSystem rdfs:subClassOf geocrs:CoordinateSystem .\n")
ttl.add("geocrs:SphericalCoordinateSystem rdfs:label \"Spherical coordinate system\"@en .\n")
ttl.add("geocrs:SphericalCoordinateSystem skos:definition \"three-dimensional coordinate system in Euclidean space with one distance measured from the origin and two angular coordinates\"@en .\n")
ttl.add("geocrs:SphericalCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:CylindricalCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:CylindricalCoordinateSystem rdfs:subClassOf geocrs:CoordinateSystem .\n")
ttl.add("geocrs:CylindricalCoordinateSystem rdfs:label \"Cylindrical coordinate system\"@en .\n")
ttl.add("geocrs:CylindricalCoordinateSystem skos:definition \"three-dimensional coordinate system in Euclidean space in which position is specified by two linear coordinates and one angular coordinate\"@en .\n")
ttl.add("geocrs:CylindricalCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:PolarCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:PolarCoordinateSystem rdfs:subClassOf geocrs:CoordinateSystem .\n")
ttl.add("geocrs:PolarCoordinateSystem rdfs:label \"Polar coordinate system\"@en .\n")
ttl.add("geocrs:PolarCoordinateSystem skos:definition \"two-dimensional coordinate system in Euclidean space in which position is specified by one distance coordinate and one angular coordinate\"@en .\n")
ttl.add("geocrs:PolarCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:ParametricCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:ParametricCoordinateSystem rdfs:subClassOf geocrs:CoordinateSystem .\n")
ttl.add("geocrs:ParametricCoordinateSystem rdfs:label \"Parametric coordinate system\"@en .\n")
ttl.add("geocrs:ParametricCoordinateSystem skos:definition \"one-dimensional coordinate system where the axis units are parameter values which are not inherently spatial\"@en .\n")
ttl.add("geocrs:ParametricCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:VerticalCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:VerticalCoordinateSystem rdfs:subClassOf geocrs:CoordinateSystem .\n")
ttl.add("geocrs:VerticalCoordinateSystem rdfs:label \"Vertical coordinate system\"@en .\n")
ttl.add("geocrs:VerticalCoordinateSystem skos:definition \"one-dimensional coordinate system used to record the heights or depths of points, usually dependent on the Earth's gravity field\"@en .\n")
ttl.add("geocrs:VerticalCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:TemporalCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:TemporalCoordinateSystem rdfs:subClassOf geocrs:CoordinateSystem .\n")
ttl.add("geocrs:TemporalCoordinateSystem rdfs:label \"Temporal coordinate system\"@en .\n")
ttl.add("geocrs:TemporalCoordinateSystem skos:definition \"one-dimensionalcoordinate system where the axis is time\"@en .\n")
ttl.add("geocrs:TemporalCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DateTimeTemporalCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:DateTimeTemporalCoordinateSystem rdfs:subClassOf geocrs:TemporalCoordinateSystem .\n")
ttl.add("geocrs:DateTimeTemporalCoordinateSystem rdfs:label \"Date time temporal coordinate system\"@en .\n")
ttl.add("geocrs:DateTimeTemporalCoordinateSystem skos:definition \"one-dimensional coordinate system used to record time in dateTime representation as defined in ISO 8601.\"@en .\n")
ttl.add("geocrs:DateTimeTemporalCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:TemporalCountCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:TemporalCountCoordinateSystem rdfs:subClassOf geocrs:TemporalCoordinateSystem .\n")
ttl.add("geocrs:TemporalCountCoordinateSystem rdfs:label \"Temporal count coordinate system\"@en .\n")
ttl.add("geocrs:TemporalCountCoordinateSystem skos:definition \"one-dimensional coordinate system used to record time as an integer count\"@en .\n")
ttl.add("geocrs:TemporalCountCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:TemporalMeasureCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:TemporalMeasureCoordinateSystem rdfs:subClassOf geocrs:TemporalCoordinateSystem .\n")
ttl.add("geocrs:TemporalMeasureCoordinateSystem rdfs:label \"Temporal measure coordinate system\"@en .\n")
ttl.add("geocrs:TemporalMeasureCoordinateSystem skos:definition \"one-dimensional coordinate system used to record a time as a real number\"@en .\n")
ttl.add("geocrs:TemporalMeasureCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:CRS rdf:type owl:Class .\n")
ttl.add("geocrs:CRS rdfs:label \"Coordinate reference system\"@en .\n")
ttl.add("geocrs:CRS rdfs:subClassOf geocrs:SpatialReferenceSystem .\n")
ttl.add("geocrs:CRS skos:definition \"coordinate system that is related to an object by a datum\"@en .\n")
ttl.add("geocrs:CRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:SingleCRS rdf:type owl:Class .\n")
ttl.add("geocrs:SingleCRS rdfs:label \"single coordinate reference system\"@en .\n")
ttl.add("geocrs:SingleCRS rdfs:subClassOf geocrs:CRS .\n")
ttl.add("geocrs:SingleCRS skos:definition \"coordinate reference system consisting of one coordinate system and either one datum or one datum ensemble\"@en .\n")
ttl.add("geocrs:SingleCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:GeographicCRS rdfs:subClassOf geocrs:GeodeticCRS .\n")
ttl.add("geocrs:GeographicCRS rdf:type owl:Class .\n")
ttl.add("geocrs:GeographicCRS rdfs:label \"Geographic coordinate reference system\"@en .\n")
ttl.add("geocrs:GeographicCRS skos:definition \"coordinate reference system that has a geodetic reference frame and an ellipsoidal coordinate system\"@en .\n")
ttl.add("geocrs:GeographicCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:AffineCoordinateSystem rdfs:subClassOf geocrs:CoordinateSystem .\n")
ttl.add("geocrs:AffineCoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:AffineCoordinateSystem owl:equivalentClass wd:Q382510 .\n")
ttl.add("geocrs:AffineCoordinateSystem rdfs:label \"Affine coordinate system\"@en .\n")
ttl.add("geocrs:AffineCoordinateSystem skos:definition \"coordinate system in Euclidean space with straight axes that are not necessarily mutually perpendicular\"@en .\n")
ttl.add("geocrs:AffineCoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:GeodeticCRS rdfs:subClassOf geocrs:SingleCRS .\n")
ttl.add("geocrs:GeodeticCRS rdf:type owl:Class .\n")
ttl.add("geocrs:GeodeticCRS rdfs:label \"Geodetic coordinate reference system\"@en .\n")
ttl.add("geocrs:GeodeticCRS owl:disjointWith geocrs:CartesianCoordinateSystem, geocrs:CompoundCRS, geocrs:EllipsoidalCoordinateSystem .\n")
ttl.add("geocrs:GeodeticCRS skos:definition \"three-dimensional coordinate reference system based on a geodetic reference frame and having either a three-dimensional Cartesian or a spherical coordinate system\"@en .\n")
ttl.add("geocrs:GeodeticCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:CompoundCRS rdfs:subClassOf geocrs:CRS .\n")
ttl.add("geocrs:CompoundCRS rdf:type owl:Class .\n")
ttl.add("geocrs:CompoundCRS skos:definition \"coordinate reference system using at least two independent coordinate reference systems\"@en .\n")
ttl.add("geocrs:CompoundCRS rdfs:label \"Compound coordinate reference system\"@en .\n")
ttl.add("geocrs:CompoundCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:CoordinateTransformation rdf:type owl:Class .\n")
ttl.add("geocrs:CoordinateTransformation rdfs:label \"coordinate transformation\"@en .\n")
ttl.add("geocrs:CoordinateTransformation skos:definition \"coordinate operation that changes coordinates in a source coordinate reference system to coordinates in a target coordinate reference system in which the source and target coordinate reference systems are based on different datums\"@en .\n")
ttl.add("geocrs:BoundCRS rdfs:subClassOf geocrs:CRS .\n")
ttl.add("geocrs:BoundCRS rdf:type owl:Class .\n")
ttl.add("geocrs:BoundCRS rdfs:label \"Bound coordinate reference system\"@en .\n")
ttl.add("geocrs:BoundCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:TemporalCRS rdfs:subClassOf geocrs:SingleCRS .\n")
ttl.add("geocrs:TemporalCRS rdf:type owl:Class .\n")
ttl.add("geocrs:TemporalCRS rdfs:label \"Temporal coordinate reference system\"@en .\n")
ttl.add("geocrs:TemporalCRS skos:definition \"coordinate reference system based on a temporal datum\"@en .\n")
ttl.add("geocrs:TemporalCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:ParametricCRS rdfs:subClassOf geocrs:SingleCRS .\n")
ttl.add("geocrs:ParametricCRS rdf:type owl:Class .\n")
ttl.add("geocrs:ParametricCRS rdfs:label \"Parametric coordinate reference system\"@en .\n")
ttl.add("geocrs:ParametricCRS skos:definition \"one-dimensional coordinate system where the axis units are parameter values which are not inherently spatial\"@en .\n")
ttl.add("geocrs:ParametricCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:SpatioParametricCRS rdfs:subClassOf geocrs:CRS .\n")
ttl.add("geocrs:SpatioParametricCRS rdf:type owl:Class .\n")
ttl.add("geocrs:SpatioParametricCRS rdfs:label \"Spatio-Parametric coordinate reference system\"@en .\n")
ttl.add("geocrs:SpatioParametricCRS skos:definition \"compound coordinate reference system in which one constituent coordinate reference system is a spatial coordinate reference system and one is a parametric coordinate reference system\"@en .\n")
ttl.add("geocrs:SpatioParametricCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DerivedGeographicCRS rdfs:subClassOf geocrs:GeographicCRS .\n")
ttl.add("geocrs:DerivedGeographicCRS rdfs:subClassOf geocrs:DerivedCRS .\n")
ttl.add("geocrs:DerivedGeographicCRS rdf:type owl:Class .\n")
ttl.add("geocrs:DerivedGeographicCRS rdfs:label \"Derived geographic coordinate reference system\"@en .\n")
ttl.add("geocrs:DerivedGeographicCRS skos:definition \"coordinate reference system that is defined through the application of a specified coordinate conversion to the coordinates within a previously established coordinate reference system\"@en .\n")
ttl.add("geocrs:DerivedGeographicCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DerivedProjectedCRS rdfs:subClassOf geocrs:ProjectedCRS .\n")
ttl.add("geocrs:DerivedProjectedCRS rdfs:subClassOf geocrs:DerivedCRS .\n")
ttl.add("geocrs:DerivedProjectedCRS rdf:type owl:Class .\n")
ttl.add("geocrs:DerivedProjectedCRS rdfs:label \"Derived projected coordinate reference system\"@en .\n")
ttl.add("geocrs:DerivedProjectedCRS skos:definition \"derived coordinate reference system which has a projected coordinate reference system as its base CRS, thereby inheriting a geodetic reference frame, but also inheriting the distortion characteristics of the base projected CRS\"@en .\n")
ttl.add("geocrs:DerivedProjectedCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DerivedCRS rdfs:subClassOf geocrs:SingleCRS .\n")
ttl.add("geocrs:DerivedCRS rdf:type owl:Class .\n")
ttl.add("geocrs:DerivedCRS rdfs:label \"Derived coordinate reference system\"@en .\n")
ttl.add("geocrs:DerivedCRS skos:definition \"derived coordinate reference system which has a projected coordinate reference system as its base CRS, thereby inheriting a geodetic reference frame, but also inheriting the distortion characteristics of the base projected CRS\"@en .\n")
ttl.add("geocrs:DerivedCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DerivedVerticalCRS rdfs:subClassOf geocrs:VerticalCRS .\n")
ttl.add("geocrs:DerivedVerticalCRS rdfs:subClassOf geocrs:DerivedCRS .\n")
ttl.add("geocrs:DerivedVerticalCRS rdf:type owl:Class .\n")
ttl.add("geocrs:DerivedVerticalCRS rdfs:label \"Derived vertical coordinate reference system\"@en .\n")
ttl.add("geocrs:DerivedVerticalCRS skos:definition \"derived coordinate reference system which has a vertical coordinate reference system as its base CRS, thereby inheriting a vertical reference frame, and a vertical coordinate system\"@en .\n")
ttl.add("geocrs:DerivedVerticalCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DerivedGeodeticCRS rdfs:subClassOf geocrs:DerivedCRS .\n")
ttl.add("geocrs:DerivedGeodeticCRS rdfs:subClassOf geocrs:GeodeticCRS .\n")
ttl.add("geocrs:DerivedGeodeticCRS rdf:type owl:Class .\n")
ttl.add("geocrs:DerivedGeodeticCRS rdfs:label \"Derived geodetic coordinate reference system\"@en .\n")
ttl.add("geocrs:DerivedGeodeticCRS skos:definition \"derived coordinate reference system which has either a geodetic or a geographic coordinate reference system as its base CRS, thereby inheriting a geodetic reference frame, and associated with a 3D Cartesian or spherical coordinate system\"@en .\n")
ttl.add("geocrs:DerivedGeodeticCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DerivedParametricCRS rdfs:subClassOf geocrs:ParametricCRS .\n")
ttl.add("geocrs:DerivedParametricCRS rdfs:subClassOf geocrs:DerivedCRS .\n")
ttl.add("geocrs:DerivedParametricCRS rdf:type owl:Class .\n")
ttl.add("geocrs:DerivedParametricCRS rdfs:label \"Derived parametric coordinate reference system\"@en .\n")
ttl.add("geocrs:DerivedParametricCRS skos:definition \"derived coordinate reference system which has a parametric coordinate reference system as its base CRS, thereby inheriting a parametric datum, and a parametric coordinate system\"@en .\n")
ttl.add("geocrs:DerivedParametricCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DerivedEngineeringCRS rdfs:subClassOf geocrs:EngineeringCRS .\n")
ttl.add("geocrs:DerivedEngineeringCRS rdfs:subClassOf geocrs:DerivedCRS .\n")
ttl.add("geocrs:DerivedEngineeringCRS rdf:type owl:Class .\n")
ttl.add("geocrs:DerivedEngineeringCRS rdfs:label \"Derived engineering coordinate reference system\"@en .\n")
ttl.add("geocrs:DerivedEngineeringCRS skos:definition \"derived coordinate reference system which has an engineering coordinate reference system as its base CRS, thereby inheriting an engineering datum, and is associated with one of the coordinate system types within the engineeringCS class\"@en .\n")
ttl.add("geocrs:DerivedEngineeringCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:EngineeringCRS rdfs:subClassOf geocrs:SingleCRS .\n")
ttl.add("geocrs:EngineeringCRS rdf:type owl:Class .\n")
ttl.add("geocrs:EngineeringCRS skos:definition \"coordinate reference system based on an engineering datum\"@en .\n")
ttl.add("geocrs:EngineeringCRS rdfs:label \"Engineering coordinate reference system\"@en .\n")
ttl.add("geocrs:EngineeringCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:VerticalCRS rdfs:subClassOf geocrs:SingleCRS .\n")
ttl.add("geocrs:VerticalCRS rdf:type owl:Class .\n")
ttl.add("geocrs:VerticalCRS rdfs:label \"Vertical coordinate reference system\"@en .\n")
ttl.add("geocrs:VerticalCRS skos:definition \"one-dimensional coordinate reference system based on a vertical reference frame\"@en .\n")
ttl.add("geocrs:VerticalCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:GeocentricCRS rdfs:subClassOf geocrs:CRS .\n")
ttl.add("geocrs:GeocentricCRS rdf:type owl:Class .\n")
ttl.add("geocrs:GeocentricCRS rdfs:label \"Geocentric coordinate reference system\"@en .\n")
ttl.add("geocrs:GeocentricCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:GeodeticReferenceFrame rdfs:subClassOf geocrs:Datum .\n")
ttl.add("geocrs:GeodeticReferenceFrame rdf:type owl:Class .\n")
ttl.add("geocrs:GeodeticReferenceFrame rdfs:label \"Geodetic reference frame\"@en .\n")
ttl.add("geocrs:GeodeticReferenceFrame skos:definition \"reference frame describing the relationship of a two- or three-dimensional coordinate system to the Earth\"@en .\n")
ttl.add("geocrs:GeodeticReferenceFrame rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DynamicReferenceFrame rdfs:subClassOf geocrs:Datum .\n")
ttl.add("geocrs:DynamicReferenceFrame rdf:type owl:Class .\n")
ttl.add("geocrs:DynamicReferenceFrame rdfs:label \"Dynamic reference frame\"@en .\n")
ttl.add("geocrs:DynamicReferenceFrame skos:definition \"reference frame in which the defining parameters include time evolution\"@en .\n")
ttl.add("geocrs:DynamicReferenceFrame rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DynamicGeodeticReferenceFrame rdfs:subClassOf geocrs:GeodeticReferenceFrame .\n")
ttl.add("geocrs:DynamicGeodeticReferenceFrame rdf:type owl:Class .\n")
ttl.add("geocrs:DynamicGeodeticReferenceFrame rdfs:label \"Dynamic geodetic reference frame\"@en .\n")
ttl.add("geocrs:DynamicGeodeticReferenceFrame skos:definition \"geodetic reference frame in which some of the parameters describe time evolution of defining station coordinates\"@en .\n")
ttl.add("geocrs:DynamicGeodeticReferenceFrame rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DynamicVerticalReferenceFrame rdfs:subClassOf geocrs:VerticalReferenceFrame .\n")
ttl.add("geocrs:DynamicVerticalReferenceFrame rdf:type owl:Class .\n")
ttl.add("geocrs:DynamicVerticalReferenceFrame rdfs:label \"Dynamic vertical reference frame\"@en .\n")
ttl.add("geocrs:DynamicVerticalReferenceFrame skos:definition \"vertical reference frame in which some of the defining parameters have time dependency\"@en .\n")
ttl.add("geocrs:DynamicVerticalReferenceFrame rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:VerticalReferenceFrame rdfs:subClassOf geocrs:Datum .\n")
ttl.add("geocrs:VerticalReferenceFrame rdf:type owl:Class .\n")
ttl.add("geocrs:VerticalReferenceFrame rdfs:label \"Vertical reference frame\"@en .\n")
ttl.add("geocrs:VerticalReferenceFrame skos:definition \"reference frame describing the relation of gravity-related heights or depths to the Earth\"@en .\n")
ttl.add("geocrs:VerticalReferenceFrame rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:StaticCRS rdfs:subClassOf geocrs:CRS .\n")
ttl.add("geocrs:StaticCRS rdf:type owl:Class .\n")
ttl.add("geocrs:StaticCRS rdfs:label \"Static coordinate reference system\"@en .\n")
ttl.add("geocrs:StaticCRS skos:definition \"coordinate reference system that has a static reference frame\"@en .\n")
ttl.add("geocrs:StaticCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:ProjectedCRS rdfs:subClassOf geocrs:CRS .\n")
ttl.add("geocrs:ProjectedCRS rdf:type owl:Class .\n")
ttl.add("geocrs:ProjectedCRS rdfs:label \"Projected coordinate reference system\"@en .\n")
ttl.add("geocrs:ProjectedCRS skos:definition \"coordinate reference system derived from a geographic coordinate reference system by applying a map projection\"@en .\n")
ttl.add("geocrs:ProjectedCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:Datum rdf:type owl:Class .\n")
ttl.add("geocrs:Datum owl:equivalentClass wd:Q1502887 .\n")
ttl.add("geocrs:Datum rdfs:label \"datum\"@en .\n")
ttl.add("geocrs:Datum skos:definition \"specification of the relationship of a coordinate system to an object, thus creating a coordinate reference system\"@en .\n")
ttl.add("geocrs:Datum rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:ParametricDatum rdf:type owl:Class .\n")
ttl.add("geocrs:ParametricDatum rdfs:label \"parametric datum\"@en .\n")
ttl.add("geocrs:ParametricDatum skos:definition \"textual description and/or a set of parameters identifying a particular reference surface used as the origin of a parametric coordinate system, including its position with respect to the Earth\"@en .\n")
ttl.add("geocrs:ParametricDatum rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:TemporalDatum rdfs:subClassOf geocrs:Datum .\n")
ttl.add("geocrs:TemporalDatum rdf:type owl:Class .\n")
ttl.add("geocrs:TemporalDatum rdfs:label \"temporal datum\"@en .\n")
ttl.add("geocrs:TemporalDatum skos:definition \"coordinate reference system based on a temporal datum\"@en .\n")
ttl.add("geocrs:TemporalDatum rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:VerticalDatum rdfs:subClassOf geocrs:Datum .\n")
ttl.add("geocrs:VerticalDatum rdf:type owl:Class .\n")
ttl.add("geocrs:VerticalDatum rdfs:label \"vertical datum\"@en .\n")
ttl.add("geocrs:VerticalDatum skos:definition \"reference frame describing the relation of gravity-related heights or depths to the Earth\"@en .\n")
ttl.add("geocrs:VerticalDatum rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:EngineeringDatum rdfs:subClassOf geocrs:Datum .\n")
ttl.add("geocrs:EngineeringDatum rdf:type owl:Class .\n")
ttl.add("geocrs:EngineeringDatum rdfs:label \"engineering datum\"@en .\n")
ttl.add("geocrs:EngineeringDatum skos:definition \"datum describing the relationship of a coordinate system to a local reference\"@en .\n")
ttl.add("geocrs:EngineeringDatum rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:Ellipsoid rdf:type owl:Class .\n")
ttl.add("geocrs:Ellipsoid rdfs:label \"ellipsoid\"@en .\n")
ttl.add("geocrs:Ellipsoid owl:disjointWith geocrs:PrimeMeridian .\n")
ttl.add("geocrs:Ellipsoid skos:definition \"reference ellipsoid\"@en .\n")
ttl.add("geocrs:Ellipsoid rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:PrimeMeridian rdf:type owl:Class .\n")
ttl.add("geocrs:PrimeMeridian rdfs:label \"prime meridian\"@en .\n")
ttl.add("geocrs:PrimeMeridian skos:definition \"meridian from which the longitudes of other meridians are quantified\"@en .\n")
ttl.add("geocrs:PrimeMeridian rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:Projection rdf:type owl:Class .\n")
ttl.add("geocrs:Projection rdfs:label \"projection\"@en .\n")
ttl.add("geocrs:OperationParameter rdf:type owl:Class .\n")
ttl.add("geocrs:OperationParameter rdfs:label \"operation parameter\"@en .\n")
ttl.add("geocrs:OperationValue rdf:type owl:Class .\n")
ttl.add("geocrs:OperationValue rdfs:label \"operation value\"@en .\n")
ttl.add("geocrs:Axis rdf:type owl:Class .\n")
ttl.add("geocrs:Axis rdfs:label \"axis\"@en .\n")
ttl.add("geocrs:CoordinateOperation rdf:type owl:Class .\n")
ttl.add("geocrs:CoordinateOperation rdfs:label \"coordinate operation\"@en .\n")
ttl.add("geocrs:CoordinateConversionOperation rdfs:subClassOf geocrs:CoordinateOperation .\n")
ttl.add("geocrs:CoordinateConversionOperation rdf:type owl:Class .\n")
ttl.add("geocrs:CoordinateConversionOperation rdfs:label \"coordinate conversion operation\"@en .\n")
ttl.add("geocrs:CoordinateTransformationOperation rdfs:subClassOf geocrs:CoordinateOperation .\n")
ttl.add("geocrs:CoordinateTransformationOperation rdf:type owl:Class .\n")
ttl.add("geocrs:CoordinateTransformationOperation rdfs:label \"coordinate transformation operation\"@en .\n")
ttl.add("geocrs:CoordinateConcatenatedOperation rdfs:subClassOf geocrs:CoordinateOperation .\n")
ttl.add("geocrs:CoordinateConcatenatedOperation rdf:type owl:Class .\n")
ttl.add("geocrs:CoordinateConcatenatedOperation rdfs:label \"coordinate concatenated operation\"@en .\n")
ttl.add("geocrs:OtherCoordinateOperation rdfs:subClassOf geocrs:CoordinateOperation .\n")
ttl.add("geocrs:OtherCoordinateOperation rdf:type owl:Class .\n")
ttl.add("geocrs:OtherCoordinateOperation rdfs:label \"other coordinate operation\"@en .\n")
ttl.add("geocrs:CardinalDirection rdf:type owl:Class .\n")
ttl.add("geocrs:CardinalDirection rdfs:label \"cardinal direction\"@en .\n")
ttl.add("geocrs:asProj4 rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:asProj4 rdfs:label \"asProj4\"@en .\n")
ttl.add("geocrs:asProj4 skos:definition \"proj4 representation of the CRS\"@en .\n")
ttl.add("geocrs:asProj4 rdfs:range xsd:string .\n")
ttl.add("geocrs:asProj4 rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:asProjJSON rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:asProjJSON rdfs:label \"asProjJSON\"@en .\n")
ttl.add("geocrs:asProjJSON skos:definition \"ProjJSON representation of the CRS\"@en .\n")
ttl.add("geocrs:asProjJSON rdfs:range xsd:string .\n")
ttl.add("geocrs:asProjJSON rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:isProjected rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:isProjected rdfs:label \"isProjected\"@en .\n")
ttl.add("geocrs:isProjected rdfs:range xsd:boolean .\n")
ttl.add("geocrs:isProjected rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:isGeographic rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:isGeographic rdfs:label \"isGeographic\"@en .\n")
ttl.add("geocrs:isGeographic rdfs:range xsd:boolean .\n")
ttl.add("geocrs:isGeographic rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:isBound rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:isBound rdfs:label \"isBound\"@en .\n")
ttl.add("geocrs:isBound rdfs:range xsd:boolean .\n")
ttl.add("geocrs:isBound rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:isGeocentric rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:isGeocentric rdfs:label \"isGeocentric\"@en .\n")
ttl.add("geocrs:isGeocentric rdfs:range xsd:boolean .\n")
ttl.add("geocrs:isGeocentric rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:isVertical rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:isVertical rdfs:label \"isVertical\"@en .\n")
ttl.add("geocrs:isVertical rdfs:range xsd:boolean .\n")
ttl.add("geocrs:isVertical rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:asWKT rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:asWKT rdfs:label \"asWKT\"@en .\n")
ttl.add("geocrs:asWKT rdfs:range geocrs:wktLiteral .\n")
ttl.add("geocrs:asWKT skos:definition \"WKT representation of the CRS\"@en .\n")
ttl.add("geocrs:asWKT rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:unit rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:unit rdfs:label \"unit\"@en .\n")
ttl.add("geocrs:unit rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:unit rdfs:range om:Unit .\n")
ttl.add("geocrs:ellipse rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:ellipse rdfs:label \"ellipse\"@en .\n")
ttl.add("geocrs:ellipse rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:ellipse rdfs:domain geocrs:Datum .\n")
ttl.add("geocrs:ellipse rdfs:range geocrs:Ellipsoid .\n")
ttl.add("geocrs:primeMeridian rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:primeMeridian rdfs:label \"prime meridian\"@en .\n")
ttl.add("geocrs:primeMeridian rdfs:domain geocrs:Datum .\n")
ttl.add("geocrs:primeMeridian rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:projection rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:projection rdfs:label \"projection\"@en .\n")
ttl.add("geocrs:projection rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:projection rdfs:range geocrs:Projection .\n")
ttl.add("geocrs:coordinateSystem rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:coordinateSystem rdfs:label \"coordinate system\"@en .\n")
ttl.add("geocrs:coordinateSystem rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:coordinateSystem rdfs:range geocrs:CoordinateSystem .\n")
ttl.add("geocrs:datum rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:datum rdfs:label \"datum\"@en .\n")
ttl.add("geocrs:datum rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:datum rdfs:range geocrs:Datum .\n")
ttl.add("geocrs:axis rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:axis rdfs:label \"axis\"@en .\n")
ttl.add("geocrs:axis rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:axis rdfs:range geocrs:Axis .\n")
ttl.add("geocrs:area_of_use rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:area_of_use rdfs:label \"area of use\"@en .\n")
ttl.add("geocrs:area_of_use rdfs:range geocrs:AreaOfUse .\n")
ttl.add("geocrs:area_of_use rdfs:domain geocrs:CoordinateConcatenatedOperation, geocrs:CoordinateConversionOperation, geocrs:CoordinateTransformationOperation, geocrs:OtherCoordinateOperation, geocrs:CoordinateOperation .\n")
ttl.add("geocrs:coordinateOperation rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:coordinateOperation rdfs:label \"coordinate operation\"@en .\n")
ttl.add("geocrs:coordinateOperation rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:coordinateOperation rdfs:range geocrs:CoordinateOperation .\n")
ttl.add("geocrs:direction rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:direction rdfs:label \"cardinal direction\"@en .\n")
ttl.add("geocrs:direction rdfs:domain geocrs:Datum .\n")
ttl.add("geocrs:direction rdfs:range geocrs:CardinalDirection .\n")
ttl.add("geocrs:unit_conversion_factor rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:unit_conversion_factor rdfs:label \"unit conversion factor\"@en .\n")
ttl.add("geocrs:unit_conversion_factor rdfs:domain geocrs:Axis .\n")
ttl.add("geocrs:unit_conversion_factor rdfs:range xsd:string .\n")
ttl.add("geocrs:abbreviation rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:abbreviation rdfs:label \"axis abbreviation\"@en .\n")
ttl.add("geocrs:abbreviation rdfs:domain geocrs:Axis .\n")
ttl.add("geocrs:abbreviation rdfs:range xsd:string .\n")
ttl.add("geocrs:unit rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:unit rdfs:label \"unit\"@en .\n")
ttl.add("geocrs:unit rdfs:domain geocrs:Axis .\n")
ttl.add("geocrs:epsgCode rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:epsgCode rdfs:label \"epsgCode\"@en .\n")
ttl.add("geocrs:epsgCode rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:epsgCode rdfs:range xsd:string .\n")
ttl.add("geocrs:accuracy rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:accuracy rdfs:label \"accuracy\"@en .\n")
ttl.add("geocrs:accuracy rdfs:domain geocrs:CoordinateOperation .\n")
ttl.add("geocrs:accuracy rdfs:range xsd:double .\n")
ttl.add("geocrs:envelope rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:envelope rdfs:label \"envelope\"@en .\n")
ttl.add("geocrs:envelope rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:envelope rdfs:range geocrs:wktLiteral .\n")
ttl.add("geocrs:utm_zone rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:utm_zone rdfs:label \"utm zone\"@en .\n")
ttl.add("geocrs:scope rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:scope rdfs:label \"scope\"@en .\n")
ttl.add("geocrs:scope rdfs:range xsd:string .\n")
ttl.add("geocrs:inverse_flattening rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:inverse_flattening rdfs:label \"inverse flattening\"@en .\n")
ttl.add("geocrs:inverse_flattening rdfs:range xsd:double .\n")
ttl.add("geocrs:has_ballpark_transformation rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:has_ballpark_transformation rdfs:label \"has ballpark transformation\"@en .\n")
ttl.add("geocrs:has_ballpark_transformation rdfs:range xsd:boolean .\n")
ttl.add("geocrs:semi_major_metre rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:semi_major_metre rdfs:label \"semi major metre\"@en .\n")
ttl.add("geocrs:semi_major_metre rdfs:range xsd:double .\n")
ttl.add("geocrs:is_semi_minor_computed rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:is_semi_minor_computed rdfs:label \"is semi minor computed\"@en .\n")
ttl.add("geocrs:is_semi_minor_computed rdfs:range xsd:double .\n")
ttl.add("geocrs:semi_minor_metre rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:semi_minor_metre rdfs:label \"semi minor metre\"@en .\n")
ttl.add("geocrs:semi_minor_metre rdfs:range xsd:double .\n")
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
			ttl.add("geoepsg:"+epsgcode+" rdf:type geocrs:ProjectedCRS .\n")
		elif "Geographic 2D CRS" in curcrs.type_name:
			ttl.add("geoepsg:"+epsgcode+" rdf:type geocrs:GeographicCRS .\n")
		elif "Geocentric CRS" in curcrs.type_name:
			ttl.add("geoepsg:"+epsgcode+" rdf:type geocrs:GeocentricCRS .\n")
		elif "Compound CRS" in curcrs.type_name:
			ttl.add("geoepsg:"+epsgcode+" rdf:type geocrs:CompoundCRS .\n")
		else:
			ttl.add("geoepsg:"+epsgcode+" rdf:type geocrs:CRS .\n")
		ttl.add("geoepsg:"+epsgcode+" rdf:type owl:NamedIndividual .\n")
		ttl.add("geoepsg:"+epsgcode+" rdfs:label \""+curname.strip()+"\"@en .\n")
		if curcrs.area_of_use!=None:
			ttl.add("geoepsg:"+epsgcode+" geocrs:envelope \"ENVELOPE("+str(curcrs.area_of_use.west)+" "+str(curcrs.area_of_use.south)+","+str(curcrs.area_of_use.east)+" "+str(curcrs.area_of_use.north)+")\"^^geocrs:wktLiteral . \n")
		ttl.add("geoepsg:"+epsgcode+" geocrs:isBound \""+str(curcrs.is_bound).lower()+"\"^^xsd:boolean . \n")
		if curcrs.coordinate_system!=None and curcrs.coordinate_system.name in coordinatesystem:
			ttl.add("geoepsg:"+epsgcode+" geocrs:coordinateSystem "+coordinatesystem[curcrs.coordinate_system.name]+" . \n")		
		elif curcrs.coordinate_system!=None:
			ttl.add("geoepsg:"+epsgcode+" geocrs:coordinateSystem \""+str(curcrs.coordinate_system)+"\"^^xsd:string . \n")
		if curcrs.coordinate_operation!=None:
			coordoperationid=curcrs.coordinate_operation.name.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_").replace(",","_").replace("&","and").strip()
			ttl.add("geoepsg:"+epsgcode+" geocrs:coordinateOperation geoepsg:"+str(coordoperationid)+" . \n")
			ttl.add("geoepsg:"+str(coordoperationid)+" geocrs:accuracy \""+str(curcrs.coordinate_operation.accuracy)+"\"^^xsd:double . \n")
			ttl.add("geoepsg:"+str(coordoperationid)+" geocrs:typename \""+str(curcrs.coordinate_operation.type_name)+"\" . \n")
			ttl.add("geoepsg:"+str(coordoperationid)+" geocrs:scope \""+str(curcrs.coordinate_operation.scope)+"\"^^xsd:string . \n")
			ttl.add("geoepsg:"+str(coordoperationid)+" geocrs:has_ballpark_transformation \""+str(curcrs.coordinate_operation.has_ballpark_transformation)+"\"^^xsd:boolean . \n")
			ttl.add("geoepsg:"+str(coordoperationid)+" geocrs:grids \""+str(curcrs.coordinate_operation.grids).replace("\n","").replace("\"","'")+"\"^^xsd:string . \n")
			if curcrs.coordinate_operation.area_of_use!=None:
				ttl.add("geoepsg:"+str(coordoperationid)+" geocrs:area_of_use geoepsg:"+str(coordoperationid)+"_area_of_use . \n")
				ttl.add("geoepsg:"+str(coordoperationid)+"_area_of_use"+" rdf:type geocrs:AreaOfUse .\n")
				ttl.add("geoepsg:"+str(coordoperationid)+"_area_of_use"+" rdfs:label \""+str(curcrs.coordinate_operation.area_of_use.name).replace("\"","'")+"\"@en .\n")
				ttl.add("geoepsg:"+str(coordoperationid)+"_area_of_use"+" geocrs:envelope \"ENVELOPE("+str(curcrs.area_of_use.west)+" "+str(curcrs.area_of_use.south)+","+str(curcrs.area_of_use.east)+" "+str(curcrs.area_of_use.north)+")\"^^geocrs:wktLiteral . \n")
			for par in curcrs.coordinate_operation.params:
				ttl.add(" geocrs:"+str(par.name).replace(" ","_")+" rdf:type owl:DatatypeProperty . \n") 
				ttl.add(" geocrs:"+str(par.name).replace(" ","_")+" rdfs:range xsd:double . \n") 
				ttl.add(" geocrs:"+str(par.name).replace(" ","_")+" rdfs:domain geocrs:CoordinateOperation . \n") 
				ttl.add(" geocrs:"+str(par.name).replace(" ","_")+" rdfs:label \""+str(par.name)+"\"@en . \n")				
				ttl.add("geoepsg:"+str(coordoperationid)+" geocrs:"+str(par.name).replace(" ","_")+" \""+str(par.value)+"\"^^xsd:double . \n") 
			for grid in curcrs.coordinate_operation.grids:
				ttl.add("geoepsg:"+str(coordoperationid)+" geocrs:grid geoepsg:"+str(grid.name).replace(" ","_")+" . \n")
				ttl.add("geoepsg:"+str(grid.name).replace(" ","_")+" rdf:type geoepsg:Grid . \n")
				ttl.add("geoepsg:"+str(grid.name).replace(" ","_")+" rdfs:label \""+str(grid.full_name)+"\"@en . \n")
				ttl.add("geoepsg:"+str(grid.name).replace(" ","_")+" rdfs:label \""+str(grid.url)+"\"@en . \n")
			if curcrs.coordinate_operation.type_name==None:
				ttl.add("geoepsg:"+str(coordoperationid)+" rdf:type geocrs:CoordinateOperation . \n")
			elif curcrs.coordinate_operation.type_name=="Conversion":
				ttl.add("geoepsg:"+str(coordoperationid)+" rdf:type geocrs:CoordinateConversionOperation . \n")
			elif curcrs.coordinate_operation.type_name=="Transformation":
				ttl.add("geoepsg:"+str(coordoperationid)+" rdf:type geocrs:CoordinateTransformationOperation . \n")
			elif curcrs.coordinate_operation.type_name=="Concatenated Operation":
				ttl.add("geoepsg:"+str(coordoperationid)+" rdf:type geocrs:CoordinateConcatenatedOperation . \n")
			elif curcrs.coordinate_operation.type_name=="Other Coordinate Operation":
				ttl.add("geoepsg:"+str(coordoperationid)+" rdf:type geocrs:OtherCoordinateOperation . \n")
			ttl.add("geoepsg:"+str(coordoperationid)+" rdfs:label \""+curcrs.coordinate_operation.name+": "+curcrs.coordinate_operation.method_name+"\"@en . \n")
		if curcrs.prime_meridian!=None:
			ttl.add("geoepsg:"+epsgcode+" geocrs:primeMeridian geoepsg:"+curcrs.prime_meridian.name.replace(" ","")+" . \n")
			ttl.add("geoepsg:"+curcrs.prime_meridian.name.replace(" ","")+" rdf:type geocrs:PrimeMeridian . \n")
			ttl.add("geoepsg:"+curcrs.prime_meridian.name.replace(" ","")+" rdfs:label \""+curcrs.prime_meridian.name+"\"@en . \n")
			if curcrs.prime_meridian.remarks!=None:
				ttl.add("geoepsg:"+str(datumid)+" rdfs:comment \""+str(curcrs.prime_meridian.remarks)+"\"@en . \n")
			if curcrs.prime_meridian.scope!=None:
				ttl.add("geoepsg:"+str(datumid)+" geocrs:scope \""+str(curcrs.prime_meridian.scope)+"\"^^xsd:string . \n")
		if curcrs.datum!=None:
			datumid=str(curcrs.datum.name.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_").replace("+","_plus"))
			ttl.add("geoepsg:"+epsgcode+" geocrs:datum geoepsg:"+str(datumid)+" . \n")
			if "Geodetic Reference Frame" in curcrs.datum.type_name:
				ttl.add("geoepsg:"+str(datumid)+" rdf:type geocrs:GeodeticReferenceFrame . \n")
			else:
				ttl.add("geoepsg:"+str(datumid)+" rdf:type geocrs:Datum . \n")
			ttl.add("geoepsg:"+str(datumid)+" rdfs:label \""+curcrs.datum.name+"\"@en . \n")
			if curcrs.datum.remarks!=None:
				ttl.add("geoepsg:"+str(datumid)+" rdfs:comment \""+str(curcrs.datum.remarks)+"\"@en . \n")
			if curcrs.datum.scope!=None:
				ttl.add("geoepsg:"+str(datumid)+" geocrs:scope \""+str(curcrs.datum.scope)+"\"^^xsd:string . \n")
			if curcrs.datum.ellipsoid.name in spheroids:
				ttl.add("geoepsg:"+str(datumid)+" geocrs:ellipse "+spheroids[curcrs.datum.ellipsoid.name]+" . \n")
				ttl.add(spheroids[curcrs.datum.ellipsoid.name]+" rdfs:label \""+str(curcrs.datum.ellipsoid.name)+"\"@en . \n")
				ttl.add(spheroids[curcrs.datum.ellipsoid.name]+" rdf:type geocrs:Ellipsoid .\n")	
				ttl.add(spheroids[curcrs.datum.ellipsoid.name]+" geocrs:inverse_flattening \""+str(curcrs.datum.ellipsoid.inverse_flattening)+"\"^^xsd:double .\n")
				ttl.add(spheroids[curcrs.datum.ellipsoid.name]+" geocrs:semi_minor_metre \""+str(curcrs.datum.ellipsoid.semi_minor_metre)+"\"^^xsd:double .\n")
				ttl.add(spheroids[curcrs.datum.ellipsoid.name]+" geocrs:semi_major_metre \""+str(curcrs.datum.ellipsoid.semi_major_metre)+"\"^^xsd:double .\n")			
				if curcrs.datum.ellipsoid.remarks!=None:
					ttl.add(spheroids[curcrs.datum.ellipsoid.name]+" rdfs:comment \""+str(curcrs.datum.ellipsoid.remarks)+"\"^^xsd:string .\n")
				ttl.add(spheroids[curcrs.datum.ellipsoid.name]+" geocrs:is_semi_minor_computed \""+str(curcrs.datum.ellipsoid.is_semi_minor_computed).lower()+"\"^^xsd:boolean .\n")
			else:	
				ttl.add("geoepsg:"+str(datumid)+" geocrs:ellipse \""+curcrs.datum.ellipsoid.name+"\" . \n")
			ttl.add("geoepsg:"+str(datumid)+" geocrs:primeMeridian geoepsg:"+curcrs.datum.prime_meridian.name.replace(" ","")+" . \n")
			ttl.add("geoepsg:"+curcrs.datum.prime_meridian.name.replace(" ","")+" rdf:type geocrs:PrimeMeridian . \n")				
		ttl.add("geoepsg:"+epsgcode+" geocrs:isVertical \""+str(curcrs.is_vertical).lower()+"\"^^xsd:boolean . \n")
		ttl.add("geoepsg:"+epsgcode+" geocrs:isProjected \""+str(curcrs.is_projected).lower()+"\"^^xsd:boolean . \n")
		ttl.add("geoepsg:"+epsgcode+" geocrs:isGeocentric \""+str(curcrs.is_geocentric).lower()+"\"^^xsd:boolean . \n")
		ttl.add("geoepsg:"+epsgcode+" geocrs:isGeographic \""+str(curcrs.is_geographic).lower()+"\"^^xsd:boolean . \n")
		if curcrs.utm_zone!=None:
			ttl.add("geoepsg:"+epsgcode+" geocrs:utm_zone \""+str(curcrs.utm_zone)+"\"^^xsd:string . \n")
		if curcrs.axis_info!=None:
			for axis in curcrs.axis_info:
				axisid=axis.name.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_")+"_"+axis.unit_name.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_")+"_"+axis.direction.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_")
				ttl.add("geoepsg:"+epsgcode+" geocrs:axis geoepsg:"+axisid+" . \n")
				ttl.add("geoepsg:"+axisid+" rdf:type geocrs:Axis . \n")
				ttl.add("geoepsg:"+axisid+" geocrs:direction geoepsg:"+axis.direction+" . \n")
				ttl.add("geoepsg:"+axisid+" geocrs:abbreviation \""+str(axis.abbrev).replace("\"","'")+"\"^^xsd:string . \n")				
				ttl.add("geoepsg:"+axisid+" geocrs:unit_conversion_factor \""+str(axis.unit_conversion_factor)+"\"^^xsd:double . \n")				
				ttl.add("geoepsg:"+axis.direction+" rdf:type geocrs:CardinalDirection . \n")				
				if axis.unit_name in units:
					ttl.add("geoepsg:"+axisid+" geocrs:unit "+units[axis.unit_name]+" . \n")
					ttl.add("geoepsg:"+axisid+" rdfs:label \""+axis.name+" ("+str(units[axis.unit_name])+")\"@en . \n")						
				else:
					ttl.add("geoepsg:"+axisid+" geocrs:unit \""+axis.unit_name+"\" . \n")
					ttl.add("geoepsg:"+axisid+" rdfs:label \""+axis.name+" ("+str(axis.unit_name)+")\"@en . \n")						
		ttl.add("geoepsg:"+epsgcode+" geocrs:asProj4 \""+proj4string.strip()+"\"^^xsd:string . \n")
		ttl.add("geoepsg:"+epsgcode+" geocrs:asProjJSON \""+curcrs.to_json().strip().replace("\"","'")+"\"^^xsd:string . \n")
		if wkt!="":
			ttl.add("geoepsg:"+epsgcode+" geocrs:asWKT \""+wkt+"\"^^geocrs:wktLiteral . \n")
		ttl.add("geoepsg:"+epsgcode+" geocrs:epsgCode \"EPSG:"+epsgcode+"\"^^xsd:string . \n")
		for spl in proj4string.split("+"):
			param=spl.split("=")
			if param[0]=="proj":
				if param[1].strip() in projections:
					ttl.add("geoepsg:"+epsgcode+" geocrs:projection "+projections[param[1].strip()]+" . \n")
					ttl.add(projections[param[1].strip()]+" rdf:type geocrs:Projection .\n")
					ttl.add(projections[param[1].strip()]+" rdfs:label \""+param[1].strip()+"\"@en .\n")
				else:
					ttl.add("geoepsg:"+epsgcode+" geocrs:projection \""+param[1].strip()+"\" . \n")
			elif param[0]=="ellps":
				if param[1].strip() in spheroids:
					ttl.add("geoepsg:"+epsgcode+" geocrs:ellipse "+spheroids[param[1].strip()]+" . \n")
					ttl.add(spheroids[param[1].strip()]+" rdfs:label \""+str(curcrs.ellipsoid)+"\"@en . \n")
					ttl.add(spheroids[param[1].strip()]+" rdf:type geocrs:Ellipsoid .\n")
					ttl.add(spheroids[param[1].strip()]+" rdfs:label \""+param[1].strip()+"\"@en .\n")						
				else:	
					ttl.add("geoepsg:"+epsgcode+" geocrs:ellipse \""+param[1].strip()+"\" . \n")
			elif param[0]=="units":
				if param[1].strip() in units:
					ttl.add("geoepsg:"+epsgcode+" geocrs:unit om:"+units[param[1].strip()]+" . \n")
					ttl.add(units[param[1].strip()]+" rdf:type om:Unit .\n")					
				else:
					ttl.add("geoepsg:"+epsgcode+" geocrs:unit \""+param[1].strip()+"\" . \n")				
	i+=1
f = open("result.ttl", "w", encoding="utf-8")
f.write(ttlhead)
for line in ttl:
	f.write(line)
f.close()
