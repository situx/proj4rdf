package io.github.galbiston.geosparql_jena.implementation.datatype.raster;

import io.github.galbiston.geosparql_jena.implementation.datatype.RasterDataType;
import proj4rdf.vocabulary.SRSGeo;

public class GMLCOVDatatype extends RasterDataType {
	
	public GMLCOVDatatype() {
		super(URI);
		// TODO Auto-generated constructor stub
	}
	public static final String URI=SRSGeo.GMLCOV;
	
	public static final GMLCOVDatatype INSTANCE=new GMLCOVDatatype();

	@Override
	public CoverageWrapper read(String geometryLiteral) {
		// TODO Auto-generated method stub
		return null;
	}

}
