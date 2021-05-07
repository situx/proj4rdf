package proj4rdf.functions.srs;

import org.apache.jena.sparql.expr.NodeValue;
import org.apache.jena.sparql.function.FunctionBase1;
import org.apache.sis.referencing.CRS;
import org.opengis.referencing.crs.CoordinateReferenceSystem;
import org.opengis.util.FactoryException;

import io.github.galbiston.geosparql_jena.implementation.GeometryWrapper;

public class SRIDGetAxis1Orientation extends FunctionBase1 {

	@Override
	public NodeValue exec(NodeValue v) {
		GeometryWrapper wrapper1=GeometryWrapper.extract(v);
		CoordinateReferenceSystem crs;
		try {
			crs = CRS.forCode("EPSG:"+((GeometryWrapper)wrapper1).getXYGeometry().getSRID());
			return NodeValue.makeString(crs.getCoordinateSystem().getAxis(0).getDirection().identifier());
		} catch (FactoryException e) {
			return NodeValue.nvNothing;
		}
	}

}
