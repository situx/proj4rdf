package io.github.galbiston.geosparql_jena.implementation.datatype.geometry;

import java.io.IOException;
import java.text.ParseException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import io.github.galbiston.geosparql_jena.implementation.GeometryWrapper;
import io.github.galbiston.geosparql_jena.implementation.GeometryWrapperFactory;
import io.github.galbiston.geosparql_jena.implementation.datatype.GeometryDatatype;
import proj4rdf.vocabulary.SRSGeo;

public class PolyshapeDatatype extends GeometryDatatype {

    private static final Logger LOGGER = LoggerFactory.getLogger(EncodedPolylineDatatype.class);

    /**
     * The default WKT type URI.
     */
    public static final String URI = SRSGeo.Polyshape;

    /**
     * A static instance of WKTDatatype.
     */
    public static final PolyshapeDatatype INSTANCE = new PolyshapeDatatype();
    
   // private static final PolyshapeReader reader=new PolyshapeReader();
    
    //private static final JtsPolyshapeWriter writer=new JtsPolyshapeWriter();

    /**
     * private constructor - single global instance.
     */
    private PolyshapeDatatype() {
        super(URI);
    }

    /**
     * This method Un-parses the JTS Geometry to the WKT literal
     *
     * @param geometry - the JTS Geometry to be un-parsed
     * @return WKT - the returned WKT Literal.
     * <br> Notice that the Spatial Reference System is not specified in
     * returned WKT literal.
     *
     */
    @Override
    public String unparse(Object geometry) {

        if (geometry instanceof GeometryWrapper) {
            GeometryWrapper geometryWrapper = (GeometryWrapper) geometry;
            throw new UnsupportedOperationException("Not yet implemented");
            //return writer.toString();           	
        } else {
            throw new AssertionError("Object passed to PolyshapeDatatype is not a GeometryWrapper: " + geometry);
        }
    }

    @Override
    public GeometryWrapper read(String geometryLiteral) {
	    GeometryWrapper wrapper;
		/*try {
			wrapper = GeometryWrapperFactory.createGeometry(reader.read(geometryLiteral), "<http://www.opengis.net/def/crs/EPSG/0/4326>", PolyshapeDatatype.URI);
			return wrapper;
		} catch (IOException | ParseException e) {
			// TODO Auto-generated catch block
			throw new RuntimeException(e.getMessage());
		}*/
        throw new UnsupportedOperationException("Not yet implemented");
    }
}
