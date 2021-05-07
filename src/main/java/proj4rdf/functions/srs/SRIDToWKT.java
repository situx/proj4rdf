package proj4rdf.functions.srs;

import java.math.BigInteger;

import org.apache.jena.sparql.expr.NodeValue;
import org.apache.jena.sparql.function.FunctionBase1;
import org.apache.sis.referencing.CRS;
import org.opengis.util.FactoryException;

public class SRIDToWKT extends FunctionBase1 {

	@Override
	public NodeValue exec(NodeValue v) {
		BigInteger srid=v.getInteger();
		try {
			return NodeValue.makeString(CRS.forCode("EPSG:"+srid.intValue()).toWKT());
		} catch (UnsupportedOperationException | FactoryException e) {
			return NodeValue.nvNothing;
		}
	}

}
