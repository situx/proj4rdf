import os
import re
import pyproj
from pyproj import CRS


units={}
units["m"]="om:meter"
units["metre"]="om:metre"
units["grad"]="om:degree"
units["degree"]="om:degree"
units["ft"]="om:foot"
units["us-ft"]="om:usfoot"
coordinatesystem={}
coordinatesystem["ellipsoidal"]="geocrs:EllipsoidalCoordinateSystem"
coordinatesystem["cartesian"]="geocrs:CartesianCoordinateSystem"
coordinatesystem["ft"]="om:foot"
coordinatesystem["us-ft"]="om:usfoot"
spheroids={}
spheroids["GRS80"]="geocrs:GRS1980"
spheroids["GRS 80"]="geocrs:GRS1980"
spheroids["GRS67"]="geocrs:GRS67"
spheroids["GRS 1967"]="geocrs:GRS67"
spheroids["GRS 1967 Modified"]="geocrs:GRS67Modified"
spheroids["GRS 67"]="geocrs:GRS67"
spheroids["GRS1980"]="geocrs:GRS1980"
spheroids["GRS 1980"]="geocrs:GRS1980"
spheroids["NWL 9D"]="geocrs:NWL9D"
spheroids["PZ-90"]="geocrs:PZ90"
spheroids["Airy 1830"]="geocrs:Airy1830"
spheroids["Airy Modified 1849"]="geocrs:AiryModified1849"
spheroids["intl"]="geocrs:International1924"
spheroids["aust_SA"]="geocrs:AustralianNationalSpheroid"
spheroids["Australian National Spheroid"]="geocrs:AustralianNationalSpheroid"
spheroids["International 1924"]="geocrs:International1924"
spheroids["clrk"]="geocrs:Clarke1866"
spheroids["War Office"]="geocrs:WarOffice"
spheroids["evrst30"]="geocrs:Everest1930"
spheroids["clrk66"]="geocrs:Clarke1866"
spheroids["Plessis 1817"]="geocrs:Plessis1817"
spheroids["Danish 1876"]="geocrs:Danish1876"
spheroids["Struve 1860"]="geocrs:Struve1860"
spheroids["IAG 1975"]="geocrs:IAG1975"
spheroids["Clarke 1866"]="geocrs:Clarke1866"
spheroids["Clarke 1858"]="geocrs:Clarke1858"
spheroids["Clarke 1880"]="geocrs:Clarke1880"
spheroids["Helmert 1906"]="geocrs:Helmert1906"
spheroids["CGCS2000"]="geocrs:CGCS2000"
spheroids["GSK-2011"]="geocrs:GSK2011"
spheroids["Zach 1812"]="geocrs:Zach1812"
spheroids["Hough 1960"]="geocrs:Hough1960"
spheroids["Hughes 1980"]="geocrs:Hughes1980"
spheroids["Indonesian National Spheroid"]="geocrs:IndonesianNationalSpheroid"
spheroids["clrk80"]="geocrs:Clarke1880RGS"
spheroids["Clarke 1880 (Arc)"]="geocrs:Clarke1880ARC"
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
spheroids["Bessel Modified"]="geocrs:BesselModified"
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
ttlhead+="@prefix geocrsdata:<http://www.opengis.net/ont/crs/> .\n"
ttlhead+="@prefix geocrsdatum:<http://www.opengis.net/ont/crs/datum/> .\n"
ttlhead+="@prefix geocrsgrid:<http://www.opengis.net/ont/crs/grid/> .\n"
ttlhead+="@prefix geocrsaxis:<http://www.opengis.net/ont/crs/cs/axis/> .\n"
ttlhead+="@prefix geocrsgeod:<http://www.opengis.net/ont/crs/geod/> .\n"
ttlhead+="@prefix geocrsaou:<http://www.opengis.net/ont/crs/areaofuse/> .\n"
ttlhead+="@prefix geocrsmeridian:<http://www.opengis.net/ont/crs/primeMeridian/> .\n"
ttlhead+="@prefix geocrsoperation:<http://www.opengis.net/ont/crs/operation/> .\n"
ttlhead+="@prefix geocs:<http://www.opengis.net/ont/crs/cs/> .\n"
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
ttl.add("geocrs:TemporalReferenceSystem skos:definition \"Reference system against which time is measured\"@en .\n")
ttl.add("geocrs:TemporalReferenceSystem rdfs:subClassOf geocrs:ReferenceSystem .\n")
ttl.add("geocrs:SpatialReferenceSystem rdf:type owl:Class .\n")
ttl.add("geocrs:SpatialReferenceSystem rdfs:label \"spatial reference system\"@en .\n")
ttl.add("geocrs:SpatialReferenceSystem skos:definition \"System for identifying position in the real world\"@en .\n")
ttl.add("geocrs:SpatialReferenceSystem rdfs:subClassOf geocrs:ReferenceSystem .\n")
ttl.add("geocrs:CoordinateSystem rdf:type owl:Class .\n")
ttl.add("geocrs:CoordinateSystem rdfs:label \"Coordinate system\"@en .\n")
ttl.add("geocrs:CoordinateSystem skos:definition \"non-repeating sequence of coordinate system axes that spans a given coordinate space\"@en .\n")
ttl.add("geocrs:CoordinateSystem rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:CoordinateSystemAxis rdf:type owl:Class .\n")
ttl.add("geocrs:CoordinateSystemAxis rdfs:label \"Coordinate system axis\"@en .\n")
ttl.add("geocrs:CoordinateSystemAxis rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:TemporalCoordinateSystemAxis rdf:type owl:Class .\n")
ttl.add("geocrs:TemporalCoordinateSystemAxis rdfs:subClassOf geocrs:CoordinateSystemAxis .\n")
ttl.add("geocrs:TemporalCoordinateSystemAxis rdfs:label \"Temporal coordinate system axis\"@en .\n")
ttl.add("geocrs:TemporalCoordinateSystemAxis rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
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
ttl.add("geocrs:GeodeticCoordinateSystem owl:disjointWith geocrs:CompoundCRS .\n")
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
ttl.add("geocrs:CoordinateTransformation rdf:type owl:Class .\n")
ttl.add("geocrs:CoordinateTransformation rdfs:label \"coordinate transformation\"@en .\n")
ttl.add("geocrs:CoordinateTransformation skos:definition \"coordinate operation that changes coordinates in a source coordinate reference system to coordinates in a target coordinate reference system in which the source and target coordinate reference systems are based on different datums\"@en .\n")
ttl.add("geocrs:BoundCRS rdfs:subClassOf geocrs:CRS .\n")
ttl.add("geocrs:BoundCRS rdf:type owl:Class .\n")
ttl.add("geocrs:BoundCRS rdfs:label \"Bound coordinate reference system\"@en .\n")
ttl.add("geocrs:BoundCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:DynamicCRS rdfs:subClassOf geocrs:CRS .\n")
ttl.add("geocrs:DynamicCRS rdf:type owl:Class .\n")
ttl.add("geocrs:DynamicCRS rdfs:label \"Dynamic coordinate reference system\"@en .\n")
ttl.add("geocrs:DynamicCRS skos:definition \"coordinate reference system that has a dynamic reference frame\"@en .\n")
ttl.add("geocrs:DynamicCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
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
ttl.add("geocrs:ProjectedCRS rdfs:subClassOf geocrs:DerivedCRS .\n")
ttl.add("geocrs:ProjectedCRS rdf:type owl:Class .\n")
ttl.add("geocrs:ProjectedCRS rdfs:label \"Projected coordinate reference system\"@en .\n")
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
ttl.add("geocrs:Geoid rdf:type owl:Class .\n")
ttl.add("geocrs:Geoid rdfs:label \"geoid\"@en .\n")
ttl.add("geocrs:Geoid skos:definition \"equipotential surface of the Earth’s gravity field which is perpendicular to the direction of gravity and which best fits mean sea level either locally, regionally or globally\"@en .\n")
ttl.add("geocrs:Geoid rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
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
ttl.add("geocrs:CoordinateOperation rdf:type owl:Class .\n")
ttl.add("geocrs:CoordinateOperation rdfs:label \"coordinate operation\"@en .\n")
ttl.add("geocrs:CoordinateOperation skos:definition \"mathematical operation (a) on coordinates that transforms or converts them from one coordinate reference system to another coordinate reference system, or (b) that decribes the change of coordinate values within one coordinate reference system due to the motion of the point between one coordinate epoch and another coordinate epoch\"@en .\n")
ttl.add("geocrs:CoordinateOperation rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:PassThroughOperation rdf:type owl:Class .\n")
ttl.add("geocrs:PassThroughOperation rdfs:label \"passthrough operation\"@en .\n")
ttl.add("geocrs:PassThroughOperation skos:definition \"specification of a subset of coordinate tuples that is subject to a coordinate operation\"@en .\n")
ttl.add("geocrs:PassThroughOperation rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:CoordinateConversionOperation rdf:type owl:Class .\n")
ttl.add("geocrs:CoordinateConversionOperation rdfs:subClassOf geocrs:SingleOperation .\n")
ttl.add("geocrs:CoordinateConversionOperation rdfs:label \"coordinate conversion operation\"@en .\n")
ttl.add("geocrs:CoordinateConversionOperation skos:definition \"Coordinate operation in which both coordinate reference systems are based on the same datum\"@en .\n")
ttl.add("geocrs:CoordinateConversionOperation rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:CoordinateTransformationOperation rdf:type owl:Class .\n")
ttl.add("geocrs:CoordinateTransformationOperation rdfs:subClassOf geocrs:SingleOperation .\n")
ttl.add("geocrs:CoordinateTransformationOperation rdfs:label \"coordinate transformation operation\"@en .\n")
ttl.add("geocrs:CoordinateTransformationOperation skos:definition \"Coordinate operation in which the two coordinate reference systems are based on different datums\"@en .\n")
ttl.add("geocrs:CoordinateTransformationOperation rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:CoordinateConcatenatedOperation rdfs:subClassOf geocrs:CoordinateOperation .\n")
ttl.add("geocrs:CoordinateConcatenatedOperation rdf:type owl:Class .\n")
ttl.add("geocrs:CoordinateConcatenatedOperation rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:CoordinateConcatenatedOperation rdfs:label \"coordinate concatenated operation\"@en .\n")
ttl.add("geocrs:CoordinateConcatenatedOperation skos:definition \"ordered sequence of two or more single coordinate operations\"@en .\n")
ttl.add("geocrs:OtherCoordinateOperation rdfs:subClassOf geocrs:CoordinateOperation .\n")
ttl.add("geocrs:OtherCoordinateOperation rdf:type owl:Class .\n")
ttl.add("geocrs:OtherCoordinateOperation rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:OtherCoordinateOperation rdfs:label \"other coordinate operation\"@en .\n")
ttl.add("geocrs:SingleOperation rdfs:subClassOf geocrs:CoordinateOperation .\n")
ttl.add("geocrs:SingleOperation rdf:type owl:Class .\n")
ttl.add("geocrs:SingleOperation rdfs:label \"single operation\"@en .\n")
ttl.add("geocrs:SingleOperation skos:definition \"single (not concatenated) coordinate operation\"@en .\n")
ttl.add("geocrs:SingleOperation rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
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
ttl.add("geocrs:isProjected skos:definition \"Indicates if the spatial reference system is projected\"@en .\n")
ttl.add("geocrs:isProjected rdfs:range xsd:boolean .\n")
ttl.add("geocrs:isProjected rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:isGeographic rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:isGeographic rdfs:label \"isGeographic\"@en .\n")
ttl.add("geocrs:isGeographic skos:definition \"Indicates if the spatial reference system is geographic\"@en .\n")
ttl.add("geocrs:isGeographic rdfs:range xsd:boolean .\n")
ttl.add("geocrs:isGeographic rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:isBound rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:isBound rdfs:label \"isBound\"@en .\n")
ttl.add("geocrs:isBound skos:definition \"Indicates if the spatial reference system is bound\"@en .\n")
ttl.add("geocrs:isBound rdfs:range xsd:boolean .\n")
ttl.add("geocrs:isBound rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:isGeocentric rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:isGeocentric rdfs:label \"isGeocentric\"@en .\n")
ttl.add("geocrs:isGeocentric skos:definition \"Indicates if the spatial reference system is geocentric\"@en .\n")
ttl.add("geocrs:isGeocentric rdfs:range xsd:boolean .\n")
ttl.add("geocrs:isGeocentric rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:isDeprecated rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:isDeprecated rdfs:label \"isDeprecated\"@en .\n")
ttl.add("geocrs:isDeprecated skos:definition \"Indicates if the spatial reference system is deprecated\"@en .\n")
ttl.add("geocrs:isDeprecated rdfs:range xsd:boolean .\n")
ttl.add("geocrs:isDeprecated rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:isVertical rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:isVertical rdfs:label \"isVertical\"@en .\n")
ttl.add("geocrs:isVertical skos:definition \"Indicates if the spatial reference system is vertical\"@en .\n")
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
ttl.add("geocrs:ellipse skos:definition \"The ellipsoid used by a geodetic datum\"@en .\n")
ttl.add("geocrs:ellipse rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:ellipse rdfs:domain geocrs:Datum .\n")
ttl.add("geocrs:ellipse rdfs:range geocrs:Ellipsoid .\n")
ttl.add("geocrs:primeMeridian rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:primeMeridian rdfs:label \"prime meridian\"@en .\n")
ttl.add("geocrs:primeMeridian skos:definition \"The prime meridian used by a geodetic datum\"@en .\n")
ttl.add("geocrs:primeMeridian rdfs:domain geocrs:Datum .\n")
ttl.add("geocrs:primeMeridian rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:projection rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:projection rdfs:label \"projection\"@en .\n")
ttl.add("geocrs:projection rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:projection rdfs:range geocrs:Projection .\n")
ttl.add("geocrs:coordinateSystem rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:coordinateSystem rdfs:label \"coordinate system\"@en .\n")
ttl.add("geocrs:coordinateSystem skos:definition \"Associates a coordinate system with a coordinate reference system\"@en .\n")
ttl.add("geocrs:coordinateSystem rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:coordinateSystem rdfs:range geocrs:CoordinateSystem .\n")
ttl.add("geocrs:sourceCRS rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:sourceCRS rdfs:label \"source CRS\"@en .\n")
ttl.add("geocrs:sourceCRS skos:definition \"The dimension of the coordinate reference system associated with the data used as input of an operation\"@en .\n")
ttl.add("geocrs:sourceCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:sourceCRS rdfs:domain geocrs:CoordinateConversionOperation .\n")
ttl.add("geocrs:sourceCRS rdfs:range geocrs:CRS .\n")
ttl.add("geocrs:targetCRS rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:targetCRS rdfs:label \"target CRS\"@en .\n")
ttl.add("geocrs:targetCRS skos:definition \"The dimension of the coordinate reference system associated with the data obtained as output of an operation\"@en .\n")
ttl.add("geocrs:targetCRS rdfs:domain geocrs:CoordinateConversionOperation .\n")
ttl.add("geocrs:targetCRS rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:targetCRS rdfs:range geocrs:CRS .\n")
ttl.add("geocrs:datum rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:datum rdfs:label \"datum\"@en .\n")
ttl.add("geocrs:datum skos:definition \"Associates a datum with a coordinate reference system\"@en .\n")
ttl.add("geocrs:datum rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:datum rdfs:domain geocrs:DatumEnsemble .\n")
ttl.add("geocrs:datum rdfs:range geocrs:Datum .\n")
ttl.add("geocrs:includesSRS rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:includesSRS rdfs:label \"includes srs\"@en .\n")
ttl.add("geocrs:includesSRS skos:definition \"Indicates spatial reference systems used by a compound reference system\"@en .\n")
ttl.add("geocrs:includesSRS rdfs:domain geocrs:CompoundCRS .\n")
ttl.add("geocrs:includesSRS rdfs:range geocrs:CRS .\n")
ttl.add("geocrs:axis rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:axis rdfs:label \"axis\"@en .\n")
ttl.add("geocrs:axis skos:definition \"An axis used by some ellipsoidal or cartesian coordinate system\"@en .\n")
ttl.add("geocrs:axis rdfs:isDefinedBy <http://docs.opengeospatial.org/as/18-005r4/18-005r4.html> .\n")
ttl.add("geocrs:axis rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:axis rdfs:range geocrs:CoordinateSystemAxis .\n")
ttl.add("geocrs:area_of_use rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:area_of_use rdfs:label \"area of use\"@en .\n")
ttl.add("geocrs:area_of_use skos:definition \"Defines an area of use of an operation\"@en .\n")
ttl.add("geocrs:area_of_use rdfs:range geocrs:AreaOfUse .\n")
ttl.add("geocrs:area_of_use rdfs:domain geocrs:CoordinateConcatenatedOperation, geocrs:CoordinateConversionOperation, geocrs:CoordinateTransformationOperation, geocrs:OtherCoordinateOperation, geocrs:CoordinateOperation .\n")
ttl.add("geocrs:coordinateOperation rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:coordinateOperation rdfs:label \"coordinate operation\"@en .\n")
ttl.add("geocrs:coordinateOperation skos:definition \"Associates a coordinate operation with a CRS\"@en .\n")
ttl.add("geocrs:coordinateOperation rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:coordinateOperation rdfs:range geocrs:CoordinateOperation .\n")
ttl.add("geocrs:direction rdf:type owl:ObjectProperty .\n")
ttl.add("geocrs:direction rdfs:label \"cardinal direction\"@en .\n")
ttl.add("geocrs:direction skos:definition \"Associates a direction with a datum\"@en .\n")
ttl.add("geocrs:direction rdfs:domain geocrs:Datum .\n")
ttl.add("geocrs:direction rdfs:range geocrs:CardinalDirection .\n")
ttl.add("geocrs:unit_conversion_factor rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:unit_conversion_factor rdfs:label \"unit conversion factor\"@en .\n")
ttl.add("geocrs:unit_conversion_factor rdfs:domain geocrs:CoordinateSystemAxis .\n")
ttl.add("geocrs:unit_conversion_factor rdfs:range xsd:string .\n")
ttl.add("geocrs:abbreviation rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:abbreviation rdfs:label \"axis abbreviation\"@en .\n")
ttl.add("geocrs:abbreviation skos:definition \"The abbreviation used to identify an axis\"@en .\n")
ttl.add("geocrs:abbreviation rdfs:domain geocrs:CoordinateSystemAxis .\n")
ttl.add("geocrs:abbreviation rdfs:range xsd:string .\n")
ttl.add("geocrs:unit rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:unit rdfs:label \"unit\"@en .\n")
ttl.add("geocrs:unit rdfs:domain geocrs:CoordinateSystemAxis .\n")
ttl.add("geocrs:unit_auth_code rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:unit_auth_code rdfs:label \"unit auth code\"@en .\n")
ttl.add("geocrs:unit_auth_code rdfs:domain geocrs:CoordinateSystemAxis .\n")
ttl.add("geocrs:unit_auth_code rdfs:range xsd:string .\n")
ttl.add("geocrs:unit_code rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:unit_code rdfs:label \"unit code\"@en .\n")
ttl.add("geocrs:unit_code rdfs:domain geocrs:CoordinateSystemAxis .\n")
ttl.add("geocrs:unit_code rdfs:range xsd:string .\n")
ttl.add("geocrs:epsgCode rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:epsgCode rdfs:label \"epsgCode\"@en .\n")
ttl.add("geocrs:epsgCode rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:epsgCode rdfs:range xsd:string .\n")
ttl.add("geocrs:accuracy rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:accuracy rdfs:label \"accuracy\"@en .\n")
ttl.add("geocrs:accuracy rdfs:domain geocrs:CoordinateOperation .\n")
ttl.add("geocrs:accuracy rdfs:range xsd:double .\n")
ttl.add("geocrs:eccentricity rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:eccentricity rdfs:label \"eccentricity\"@en .\n")
ttl.add("geocrs:eccentricity rdfs:domain geocrs:Geoid .\n")
ttl.add("geocrs:eccentricity rdfs:range xsd:double .\n")
ttl.add("geocrs:flatteningParameter rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:flatteningParameter rdfs:label \"flattening parameter\"@en .\n")
ttl.add("geocrs:flatteningParameter rdfs:domain geocrs:Geoid .\n")
ttl.add("geocrs:flatteningParameter rdfs:range xsd:double .\n")
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
ttl.add("geocrs:extent rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:extent rdfs:label \"envelope\"@en .\n")
ttl.add("geocrs:extent rdfs:domain geocrs:CRS .\n")
ttl.add("geocrs:extent rdfs:range geocrs:wktLiteral .\n")
ttl.add("geocrs:utm_zone rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:utm_zone rdfs:label \"utm zone\"@en .\n")
ttl.add("geocrs:scope rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:scope rdfs:label \"scope\"@en .\n")
ttl.add("geocrs:scope skos:definition \"the scope of the referring object\"@en .\n")
ttl.add("geocrs:scope rdfs:range xsd:string .\n")
ttl.add("geocrs:inverse_flattening rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:inverse_flattening rdfs:label \"inverse flattening\"@en .\n")
ttl.add("geocrs:inverse_flattening skos:definition \"Indicates the inverse flattening value of an ellipsoid, expressed as a number or a ratio (percentage rate, parts per million, etc.)\"@en .\n")
ttl.add("geocrs:inverse_flattening rdfs:range xsd:double .\n")
ttl.add("geocrs:has_ballpark_transformation rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:has_ballpark_transformation rdfs:label \"has ballpark transformation\"@en .\n")
ttl.add("geocrs:has_ballpark_transformation rdfs:range xsd:boolean .\n")
ttl.add("geocrs:is_semi_minor_computed rdf:type owl:DatatypeProperty .\n")
ttl.add("geocrs:is_semi_minor_computed rdfs:label \"is semi minor computed\"@en .\n")
ttl.add("geocrs:is_semi_minor_computed rdfs:range xsd:double .\n")
geodcounter=1
f = open("ontology.ttl", "w", encoding="utf-8")
f.write(ttlhead)
for line in ttl:
	f.write(line)
f.close()
i=0
curname=""
for x in list(range(2000,10000))+list(range(20000,30000)):
	try:
		curcrs=CRS.from_epsg(x)
		print("EPSG: "+str(x))
	except:
		continue	
	epsgcode=str(x)
	wkt=curcrs.to_wkt().replace("\"","'").strip()
	if "Projected CRS" in curcrs.type_name:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geocrs:ProjectedCRS .\n")
	elif "Geographic 2D CRS" in curcrs.type_name:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geocrs:GeographicCRS .\n")
	elif "Bound CRS" in curcrs.type_name:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geocrs:BoundCRS .\n")
	elif "Vertical CRS" in curcrs.type_name:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geocrs:VerticalCRS .\n")
	elif "Geocentric CRS" in curcrs.type_name:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geocrs:GeocentricCRS .\n")
	elif "Compound CRS" in curcrs.type_name:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geocrs:CompoundCRS .\n")
		for subcrs in curcrs.sub_crs_list:
			ttl.add("geoepsg:"+epsgcode+" geocrs:includesSRS geoepsg:"+str(subcrs.to_epsg())+" .\n")			
	else:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geocrs:CRS .\n")
	ttl.add("geoepsg:"+epsgcode+" rdf:type owl:NamedIndividual .\n")
	ttl.add("geoepsg:"+epsgcode+" rdfs:label \""+curcrs.name.strip()+"\"@en .\n")
	ttl.add("geoepsg:"+epsgcode+" geocrs:isBound \""+str(curcrs.is_bound).lower()+"\"^^xsd:boolean . \n")
	if curcrs.coordinate_system!=None and curcrs.coordinate_system.name in coordinatesystem:
		ttl.add("geoepsg:"+epsgcode+"_cs rdf:type "+coordinatesystem[curcrs.coordinate_system.name]+" . \n")
		ttl.add("geoepsg:"+epsgcode+"_cs rdfs:label \"EPSG:"+epsgcode+" CS: "+curcrs.coordinate_system.name+"\" . \n")
		if curcrs.coordinate_system.remarks!=None:
			ttl.add("geoepsg:"+epsgcode+"_cs rdfs:comment \""+str(curcrs.coordinate_system.remarks)+"\"@en . \n")
		if curcrs.coordinate_system.scope!=None:
			ttl.add("geoepsg:"+epsgcode+"_cs geocrs:scope \""+str(curcrs.coordinate_system.scope)+"\" . \n")
		for axis in curcrs.coordinate_system.axis_list:
			axisid=axis.name.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_")+"_"+axis.unit_name.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_")+"_"+axis.direction.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_")
			ttl.add("geoepsg:"+epsgcode+"_cs geocrs:axis geocrsaxis:"+axisid+" . \n")
			ttl.add("geocrsaxis:"+axisid+" rdf:type geocrs:CoordinateSystemAxis . \n")
			ttl.add("geocrsaxis:"+axisid+" geocrs:direction geocrsaxis:"+axis.direction+" . \n")
			ttl.add("geocrsaxis:"+axisid+" geocrs:abbreviation \""+str(axis.abbrev).replace("\"","'")+"\"^^xsd:string . \n")				
			ttl.add("geocrsaxis:"+axisid+" geocrs:unit_conversion_factor \""+str(axis.unit_conversion_factor)+"\"^^xsd:double . \n")	
			ttl.add("geocrsaxis:"+axisid+" geocrs:unit_auth_code \""+str(axis.unit_auth_code)+"\"^^xsd:string . \n")
			ttl.add("geocrsaxis:"+axisid+" geocrs:unit_code \""+str(axis.unit_code)+"\"^^xsd:string . \n")					
			ttl.add("geocrsaxis:"+axis.direction+" rdf:type geocrs:CardinalDirection . \n")				
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
	if curcrs.get_geod()!=None:
		geoid="geocrsgeod:"+str(geodcounter)
		if curcrs.datum.ellipsoid!=None:
			if curcrs.datum.ellipsoid.name in spheroids:
				geoid=spheroids[curcrs.datum.ellipsoid.name]
				ttl.add(geoid+" rdf:type geocrs:Ellipsoid . \n")
				ttl.add(geoid+" rdfs:label \""+curcrs.datum.ellipsoid.name+"\"@en . \n")
			else:
				geoid="geocrsgeod:"+str(curcrs.datum.ellipsoid.name).replace(" ","_").replace("(","_").replace(")","_")
				ttl.add(geoid+" rdf:type geocrs:Geoid . \n")
				ttl.add(geoid+" rdfs:label \""+curcrs.datum.ellipsoid.name+"\"@en . \n")
		else:
			ttl.add("geoepsg:"+epsgcode+" geocrs:ellipsoid geocrsgeod:"+str(geodcounter)+" . \n")
			ttl.add("geocrsgeod:geod"+str(geodcounter)+" rdf:type geocrs:Geoid . \n")
			ttl.add(geoid+" rdfs:label \"Geoid "+str(geodcounter)+"\"@en . \n")
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
			ttl.add("geocrsaou:"+str(coordoperationid)+"_area_of_use"+" geocrs:extent \"ENVELOPE("+str(curcrs.area_of_use.west)+" "+str(curcrs.area_of_use.south)+","+str(curcrs.area_of_use.east)+" "+str(curcrs.area_of_use.north)+")\"^^geocrs:wktLiteral . \n")
		for par in curcrs.coordinate_operation.params:
			ttl.add(" geocrs:"+str(par.name).replace(" ","_")+" rdf:type owl:DatatypeProperty . \n") 
			ttl.add(" geocrs:"+str(par.name).replace(" ","_")+" rdfs:range xsd:double . \n") 
			ttl.add(" geocrs:"+str(par.name).replace(" ","_")+" rdfs:domain geocrs:CoordinateOperation . \n") 
			ttl.add(" geocrs:"+str(par.name).replace(" ","_")+" rdfs:label \""+str(par.name)+"\"@en . \n")				
			ttl.add("geocrsoperation:"+str(coordoperationid)+" geocrs:"+str(par.name).replace(" ","_")+" \""+str(par.value)+"\"^^xsd:double . \n") 
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
			ttl.add("geocrsoperation:"+str(coordoperationid)+" rdf:type geocrs:CoordinateConversionOperation . \n")
		elif curcrs.coordinate_operation.type_name=="Transformation":
			ttl.add("geocrsoperation:"+str(coordoperationid)+" rdf:type geocrs:CoordinateTransformationOperation . \n")
		elif curcrs.coordinate_operation.type_name=="Concatenated Operation":
			ttl.add("geocrsoperation:"+str(coordoperationid)+" rdf:type geocrs:CoordinateConcatenatedOperation . \n")
		elif curcrs.coordinate_operation.type_name=="Other Coordinate Operation":
			ttl.add("geocrsoperation:"+str(coordoperationid)+" rdf:type geocrs:OtherCoordinateOperation . \n")
		ttl.add("geocrsoperation:"+str(coordoperationid)+" rdfs:label \""+curcrs.coordinate_operation.name+": "+curcrs.coordinate_operation.method_name+"\"@en . \n")
	if curcrs.datum!=None:
		datumid=str(curcrs.datum.name.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_").replace("+","_plus").replace("[","_").replace("]","_"))
		ttl.add("geoepsg:"+epsgcode+" geocrs:datum geocrsdatum:"+str(datumid)+" . \n")
		if "Geodetic Reference Frame" in curcrs.datum.type_name:
			ttl.add("geocrsdatum:"+str(datumid)+" rdf:type geocrs:GeodeticReferenceFrame . \n")
		else:
			ttl.add("geocrsdatum:"+str(datumid)+" rdf:type geocrs:Datum . \n")
		ttl.add("geocrsdatum:"+str(datumid)+" rdfs:label \"Datum: "+curcrs.datum.name+"\"@en . \n")
		if curcrs.datum.remarks!=None:
			ttl.add("geocrsdatum:"+str(datumid)+" rdfs:comment \""+str(curcrs.datum.remarks)+"\"@en . \n")
		if curcrs.datum.scope!=None:
			ttl.add("geocrsdatum:"+str(datumid)+" geocrs:scope \""+str(curcrs.datum.scope)+"\"^^xsd:string . \n")
		if curcrs.datum.ellipsoid!=None and curcrs.datum.ellipsoid.name in spheroids:
			ttl.add("geocrsdatum:"+str(datumid)+" geocrs:ellipse "+spheroids[curcrs.datum.ellipsoid.name]+" . \n")
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
	i+=1
f = open("result.ttl", "w", encoding="utf-8")
f.write(ttlhead)
for line in ttl:
	f.write(line)
f.close()
