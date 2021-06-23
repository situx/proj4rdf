package io.github.galbiston.geosparql_jena.implementation.datatype.raster;

import java.awt.image.BufferedImage;
import java.io.IOException;

import org.apache.sis.coverage.grid.GridCoverage;
import org.apache.sis.referencing.CRS;
import org.apache.sis.referencing.crs.DefaultGeographicCRS;
import org.geotoolkit.coverage.wkb.WKBRasterReader;
import org.geotoolkit.coverage.wkb.WKBRasterWriter;
import org.locationtech.jts.io.WKBReader;
import org.locationtech.jts.io.WKBWriter;
import org.opengis.referencing.crs.CRSAuthorityFactory;
import org.opengis.util.FactoryException;

import de.hsmainz.cs.semgis.arqextension.vocabulary.PostGISGeo;
import io.github.galbiston.geosparql_jena.implementation.datatype.RasterDataType;
import proj4rdf.vocabulary.SRSGeo;

public class HexWKBRastDatatype extends RasterDataType {

	public static final String URI = SRSGeo.HexWKBRaster;
	
	public static final HexWKBRastDatatype INSTANCE =new HexWKBRastDatatype();
	
	public HexWKBRastDatatype() {
		super(URI);
	}
	
	@Override
	public String unparse(Object geometry) {
		if (geometry instanceof CoverageWrapper) {
            CoverageWrapper geometryWrapper = (CoverageWrapper) geometry;
            WKBRasterWriter writer=new WKBRasterWriter();
			String rasterWKB;
			try {
				rasterWKB = WKBWriter.toHex(writer.write(geometryWrapper.getGridGeometry())).toString();
				return rasterWKB.toString();
			} catch (IOException | FactoryException e) {
				throw new AssertionError(e.getMessage());
			}

        } else {
            throw new AssertionError("Object passed to HexWKBRasterDatatype is not a GeometryWrapper: " + geometry);
        }
	}

	@Override
	public CoverageWrapper read(String geometryLiteral) {
		WKBRasterReader reader2=new WKBRasterReader();
		GridCoverage coverage;
		try {
			//BufferedImage img=reader2.read(WKBReader.hexToBytes(geometryLiteral));
			//CRS.forCode("EPSG:4326").getCoordinateSystem().
			coverage = reader2.readCoverage(WKBReader.hexToBytes(geometryLiteral),null);
			//System.out.println(coverage);
			return new CoverageWrapper(coverage, URI);
		} catch (IOException | FactoryException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			throw new RuntimeException(e.getMessage());
		}

	}
	
    @Override
    public String toString() {
        return "HexWKBRasterDatatype{" + URI + '}';
    }
}