package proj4rdf.functions.srs;

import org.apache.jena.sparql.expr.NodeValue;
import org.apache.jena.sparql.function.FunctionBase1;
import org.apache.sis.referencing.CRS;
import org.opengis.util.FactoryException;

public class EPSGToWKT extends FunctionBase1 {

	@Override
	public NodeValue exec(NodeValue v) {		
		String epsg=v.getString();
		try {
			return NodeValue.makeString(CRS.forCode(epsg).getCoordinateSystem().toWKT());
		} catch (UnsupportedOperationException | FactoryException e) {
			return NodeValue.nvNothing;
		}
	}

}
