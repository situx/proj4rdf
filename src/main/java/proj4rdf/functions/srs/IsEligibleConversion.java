package proj4rdf.functions.srs;

import org.apache.jena.sparql.expr.NodeValue;
import org.apache.jena.sparql.function.FunctionBase1;
import org.apache.jena.sparql.function.FunctionBase2;
import org.apache.sis.referencing.CRS;

import io.github.galbiston.geosparql_jena.implementation.GeometryWrapper;

/**
 * Indicates whether two srs definitions are eligible for a conversion of coordinates.
 */
public class IsEligibleConversion extends FunctionBase2 {

	@Override
	public NodeValue exec(NodeValue v1, NodeValue v2) {
		GeometryWrapper wrapper1=GeometryWrapper.extract(v1);
    	if(wrapper1 instanceof GeometryWrapper) {
    		GeometryWrapper geometry = GeometryWrapper.extract(v1);
    		return NodeValue.makeBoolean(CRS.isHorizontalCRS(geometry.getCRS()));
    	}
    	return NodeValue.FALSE;
	}

}
