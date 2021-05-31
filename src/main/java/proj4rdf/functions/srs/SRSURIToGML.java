package proj4rdf.functions.srs;

import org.apache.jena.sparql.expr.NodeValue;
import org.apache.jena.sparql.function.FunctionBase2;

import proj4rdf.RDFCRSToWKT;

/**
 * Converts an SRS URI to its GML representation.
 *
 */
public class SRSURIToGML extends FunctionBase2 {

	@Override
	public NodeValue exec(NodeValue v1, NodeValue v2) {		
		String srsURI=v1.getString();
		String endpoint=null;
		if(v2!=null) {
			endpoint=v2.getString();
		}
		String res="";
		try {
			if(endpoint!=null) {
				res = RDFCRSToWKT.getCRSFromTripleStore(srsURI, endpoint, "GML");
			}else {
				res = RDFCRSToWKT.getCRSFromTripleStore(srsURI, endpoint, "GML");			
			}
			return NodeValue.makeString(res.toString());
		} catch (UnsupportedOperationException e) {
			return NodeValue.nvNothing;
		}
	}


}
