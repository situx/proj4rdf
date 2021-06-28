package io.github.galbiston.geosparql_jena.implementation.datatype.raster;

import java.awt.image.BandedSampleModel;
import java.awt.image.DataBuffer;
import java.awt.image.Raster;
import java.awt.image.WritableRaster;

import io.github.galbiston.geosparql_jena.implementation.datatype.RasterDataType;
import proj4rdf.vocabulary.SRSGeo;

public class XYZDatatype extends RasterDataType {

	public static final String URI = SRSGeo.XYZASCII;
	
	public static final XYZDatatype INSTANCE =new XYZDatatype();
	
	public XYZDatatype() {
		super(URI);
	}

	@Override
	public CoverageWrapper read(String geometryLiteral) {
		// TODO Auto-generated method stub
		return null;
	}
	
	@Override
	public String unparse(Object value) {
		//GridCoverageBuilder builder=new GridCoverageBuilder();
		//DataBuffer buffer=new DataBufferFloat(10);
		/*builder.setValues(buffer);
		SampleModel sm=new BandedSampleModel(dataType, w, h, numBands);
		WritableRaster rast=new WritableRaster(null, buffer, null);
		Raster.createWritableRaster(sm, buffer, null);
		builder.setValues(rast);
		builder.setDomain(envelope)
		GridCoverage2D cov=(GridCoverage2D) value;
		cov.getSampleDimensions().get(0).forConvertedValues(true).
		// TODO Auto-generated method stub*/
		return super.unparse(value);
	}

}
