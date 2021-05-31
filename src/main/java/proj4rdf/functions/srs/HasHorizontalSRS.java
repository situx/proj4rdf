package proj4rdf.functions.srs;

import org.apache.jena.sparql.expr.NodeValue;
import org.apache.jena.sparql.function.FunctionBase1;
import org.apache.sis.referencing.CRS;

import io.github.galbiston.geosparql_jena.implementation.GeometryWrapper;

/**
 * Indicates if a geometry is associated with a horizontal spatial reference system.
 *
 */
public class HasHorizontalSRS extends FunctionBase1 {

	@Override
	public NodeValue exec(NodeValue v) {
		GeometryWrapper wrapper1=GeometryWrapper.extract(v);
    	if(wrapper1 instanceof GeometryWrapper) {
    		GeometryWrapper geometry = GeometryWrapper.extract(v);
    		return NodeValue.makeBoolean(CRS.isHorizontalCRS(geometry.getCRS()));
    	}
    	return NodeValue.FALSE;
	}
}
