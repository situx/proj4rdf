package proj4rdf.functions.srs;

import org.apache.jena.sparql.expr.NodeValue;
import org.apache.jena.sparql.function.FunctionBase1;
import org.apache.sis.referencing.CRS;
import org.opengis.referencing.crs.CoordinateReferenceSystem;
import org.opengis.util.FactoryException;

import io.github.galbiston.geosparql_jena.implementation.GeometryWrapper;

/**
 * Returns the name of the second axis defined in the spatial reference system.
 *
 */
public class SRIDGetAxis2Name extends FunctionBase1 {

	@Override
	public NodeValue exec(NodeValue v) {
		GeometryWrapper wrapper1=GeometryWrapper.extract(v);
		CoordinateReferenceSystem crs;
		try {
			if(wrapper1 instanceof GeometryWrapper) {
				crs = CRS.forCode("EPSG:"+((GeometryWrapper)wrapper1).getXYGeometry().getSRID());
				return NodeValue.makeString(crs.getCoordinateSystem().getAxis(1).getName().toString());
			}
		} catch (FactoryException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return NodeValue.nvEmptyString;
	}

}
