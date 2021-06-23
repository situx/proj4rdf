package io.github.galbiston.geosparql_jena.implementation.datatype.raster;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;

import org.apache.sis.storage.StorageConnector;

import io.github.galbiston.geosparql_jena.implementation.datatype.RasterDataType;
import proj4rdf.vocabulary.SRSGeo;

public class NetCDFDatatype extends RasterDataType {

	public static final String URI = SRSGeo.NetCDF;
	
	public static final NetCDFDatatype INSTANCE=new NetCDFDatatype();
	
	public NetCDFDatatype() {
		super(URI);
	}

	@Override
	public CoverageWrapper read(String geometryLiteral) {
		InputStream stream = new ByteArrayInputStream(geometryLiteral.getBytes(StandardCharsets.UTF_8));
		final StorageConnector c = new StorageConnector(stream);
		//NetcdfStoreProvider prov=new NetcdfStoreProvider();
		throw new UnsupportedOperationException("Not yet implemented");
		//NetcdfStore store=new NetcdfStore(prov,c);
		
		//GridCoverage cov=store.components().read(store.components().iterator().next().getGridGeometry(), 1);
		//return new CoverageWrapper(cov, URI);
	}
	
	@Override
	public String unparse(Object value) {
		// TODO Auto-generated method stub
		return super.unparse(value);
	}

}
