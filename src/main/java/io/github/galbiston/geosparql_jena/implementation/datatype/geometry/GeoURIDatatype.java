package io.github.galbiston.geosparql_jena.implementation.datatype.geometry;

import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.Geometry;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import io.github.galbiston.geosparql_jena.implementation.GeometryWrapper;
import io.github.galbiston.geosparql_jena.implementation.GeometryWrapperFactory;
import io.github.galbiston.geosparql_jena.implementation.datatype.GeometryDatatype;
import proj4rdf.vocabulary.SRSGeo;

public class GeoURIDatatype extends GeometryDatatype {

	public GeoURIDatatype() {
		super(URI);
	}

	private static final Logger LOGGER = LoggerFactory.getLogger(GeoURIDatatype.class);

    /**
     * The default WKT type URI.
     */
    public static final String URI = SRSGeo.GeoURI;

    /**
     * A static instance of WKTDatatype.
     */
    public static final GeoURIDatatype INSTANCE = new GeoURIDatatype();

	@Override
	public GeometryWrapper read(String geometryLiteral) {
		String[] items=geometryLiteral.split(";");
		if(items.length==0 || items.length>4) {
			throw new AssertionError("Not a valid geoURI: " + geometryLiteral);
		}
		String[] coordinates=items[0].replace("geo:", "").split(",");
		return GeometryWrapperFactory.createPoint(new Coordinate(Double.valueOf(coordinates[0]),Double.valueOf(coordinates[1])), URI);	
	}
	
	@Override
	public String unparse(Object geometry) {
		if (geometry instanceof GeometryWrapper) {
            Geometry geom = ((GeometryWrapper)geometry).getXYGeometry();
            if("POINT".equalsIgnoreCase(geom.getGeometryType())) {
            	return "geo:"+geom.getCoordinate().x+","+geom.getCoordinate().y+";crs=EPSG:"+geom.getSRID();
            }
            return "geo:"+geom.getCentroid().getCoordinate().x+","+geom.getCentroid().getCoordinate().y+";crs=EPSG:"+geom.getSRID();
    	} else {
            throw new AssertionError("Object passed to GeoURIDatatype is not a GeometryWrapper: " + geometry);
        }		
	}
    
    

}
