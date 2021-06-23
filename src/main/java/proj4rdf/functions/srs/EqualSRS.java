package proj4rdf.functions.srs;

import org.apache.jena.sparql.expr.NodeValue;
import org.apache.jena.sparql.function.FunctionBase2;

import io.github.galbiston.geosparql_jena.implementation.GeometryWrapper;

public class EqualSRS extends FunctionBase2 {

	@Override
	public NodeValue exec(NodeValue v1, NodeValue v2) {
		GeometryWrapper geomwrap=GeometryWrapper.extract(v1);
		GeometryWrapper geomwrap2=GeometryWrapper.extract(v2);
		// TODO Auto-generated method stub
		return null;
	}

}
