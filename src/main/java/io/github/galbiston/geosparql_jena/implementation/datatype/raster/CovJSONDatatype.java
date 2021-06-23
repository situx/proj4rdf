package io.github.galbiston.geosparql_jena.implementation.datatype.raster;

import org.apache.sis.coverage.grid.GridCoverage;
import org.json.JSONObject;

import de.hsmainz.cs.semgis.arqextension.util.parsers.CoverageJSONReader;
import de.hsmainz.cs.semgis.arqextension.util.parsers.CoverageJsonWriter;
import de.hsmainz.cs.semgis.arqextension.vocabulary.PostGISGeo;
import io.github.galbiston.geosparql_jena.implementation.datatype.RasterDataType;


public class CovJSONDatatype extends RasterDataType{

	public static final String URI = PostGISGeo.CoverageJSON;
	
	public static final CovJSONDatatype INSTANCE=new CovJSONDatatype();

	public CovJSONDatatype() {
		super(URI);
	}

	@Override
	public CoverageWrapper read(String geometryLiteral) {
		GridCoverage coverage=CoverageJSONReader.covJSONStringToCoverage(geometryLiteral);
		return new CoverageWrapper(coverage, URI);
	}
	
	@Override
	public String unparse(Object value) {
		if (value instanceof CoverageWrapper) {
			CoverageWrapper covWrapper = (CoverageWrapper) value;
			JSONObject res=CoverageJsonWriter.coverageToCovJSON(covWrapper.getGridGeometry());
			return res.toString();
		}else {
            throw new AssertionError("Object passed to CoverageJSONDatatype is not a CoverageWrapper: " + value);
        }
	}

}
