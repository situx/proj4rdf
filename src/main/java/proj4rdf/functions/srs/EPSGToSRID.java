package proj4rdf.functions.srs;

import org.apache.jena.sparql.expr.NodeValue;
import org.apache.jena.sparql.function.FunctionBase1;

/**
 * Converts an EPSG code to its SRID representation.
 *
 */
public class EPSGToSRID extends FunctionBase1 {

	@Override
	public NodeValue exec(NodeValue v) {
		String epsg=v.getString();
		return NodeValue.makeInteger(Integer.valueOf(epsg.substring(epsg.indexOf(':')+1)));
	}

}
