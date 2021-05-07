package proj4rdf.functions.srs;

import java.math.BigInteger;

import org.apache.jena.datatypes.DatatypeFormatException;
import org.apache.jena.sparql.expr.ExprEvalException;
import org.apache.jena.sparql.expr.NodeValue;
import org.apache.jena.sparql.function.FunctionBase2;
import org.locationtech.jts.geom.Geometry;

import io.github.galbiston.geosparql_jena.implementation.GeometryWrapper;
import io.github.galbiston.geosparql_jena.implementation.GeometryWrapperFactory;

/**
 * Set the SRID on a geometry to a particular integer value.
 *
 */
public class SetSRID extends FunctionBase2 {

	@Override
	public NodeValue exec(NodeValue v1, NodeValue v2) {
        try {
            GeometryWrapper geometry = GeometryWrapper.extract(v1);
            Geometry geom = geometry.getXYGeometry();
            BigInteger srid=v2.getInteger();
            geom.setSRID(srid.intValue());
            return GeometryWrapperFactory.createGeometry(geom, geometry.getGeometryDatatypeURI()).asNodeValue();
        } catch (DatatypeFormatException ex) {
            throw new ExprEvalException(ex.getMessage(), ex);
        }
	}

}
