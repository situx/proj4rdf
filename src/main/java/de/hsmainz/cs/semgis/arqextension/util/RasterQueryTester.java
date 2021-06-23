package de.hsmainz.cs.semgis.arqextension.util;

import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;


import io.github.galbiston.geosparql_jena.implementation.datatype.raster.CoverageWrapper;

public class RasterQueryTester {

	public static void readRaster() {

	}
	
	public static void main(String[] args) {
		/*GridCoverage2D coverage;
		try {
			coverage = CoverageIO.read(geometryLiteral);
			return new CoverageWrapper(coverage, URI);
		} catch (CoverageStoreException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			throw new RuntimeException();
		}

		//InputStream stream = new ByteArrayInputStream(geometryLiteral.getBytes(StandardCharsets.UTF_8));
		final StorageConnector c;// = new StorageConnector(stream);
		c=new StorageConnector(new File("flood/hochwasser.tif"));
		GeoTiffStoreProvider prov=new GeoTiffStoreProvider();
		GridCoverage cov;
		GeoTiffStore store=new GeoTiffStore(prov,c);
		store.getProvider().open(c);
		cov = store.components().get(0).read(store.components().get(0).getGridGeometry(), 1);
		*/
	}
}
