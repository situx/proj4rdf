package io.github.galbiston.geosparql_jena.implementation.datatype.raster;

import java.io.IOException;

import org.apache.sis.coverage.grid.GridCoverage;
import org.geotoolkit.coverage.wkb.WKBRasterReader;
import org.geotoolkit.coverage.wkb.WKBRasterWriter;
import org.opengis.util.FactoryException;

import com.sun.jersey.core.util.Base64;

import io.github.galbiston.geosparql_jena.implementation.datatype.RasterDataType;
import proj4rdf.vocabulary.SRSGeo;

public class WKBRastDatatype extends RasterDataType {

	public static final String URI = SRSGeo.WKBRaster;
	
	public static final WKBRastDatatype INSTANCE = new WKBRastDatatype();
	
	public WKBRastDatatype() {
		super(URI);
	}
	
	@Override
	public String unparse(Object geometry) {
		if (geometry instanceof CoverageWrapper) {
            CoverageWrapper geometryWrapper = (CoverageWrapper) geometry;
            WKBRasterWriter writer=new WKBRasterWriter();
			String rasterWKB;
			try {
				rasterWKB = writer.write(geometryWrapper.getGridGeometry()).toString();
				return rasterWKB.toString();
			} catch (IOException | FactoryException e) {
				throw new AssertionError(e.getMessage());
			}

        } else {
            throw new AssertionError("Object passed to WKBRastDatatype is not a CoverageWrapper: " + geometry);
        }
	}

	@Override
	public CoverageWrapper read(String geometryLiteral) {
		WKBRasterReader reader2=new WKBRasterReader();
		GridCoverage coverage;
		try {
			coverage = reader2.readCoverage(Base64.decode(geometryLiteral), null);
			System.out.println(coverage);
			return new CoverageWrapper(coverage, URI);
		} catch (IOException | FactoryException e) {
			e.printStackTrace();
			throw new RuntimeException(e.getMessage());
		}

	}
	
    @Override
    public String toString() {
        return "WKBRasterDatatype{" + URI + '}';
    }

}
