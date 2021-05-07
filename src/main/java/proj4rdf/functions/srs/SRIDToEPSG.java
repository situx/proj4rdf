package proj4rdf.functions.srs;

import java.math.BigInteger;

import org.apache.jena.sparql.expr.NodeValue;
import org.apache.jena.sparql.function.FunctionBase1;

public class SRIDToEPSG extends FunctionBase1 {

	@Override
	public NodeValue exec(NodeValue v) {
		BigInteger srid=v.getInteger();
		return NodeValue.makeString("EPSG:"+srid.intValue());
	}

}
