package proj4rdf.functions.srs;

import org.apache.jena.sparql.expr.ExprEvalException;
import org.apache.jena.sparql.expr.NodeValue;
import org.apache.jena.sparql.function.FunctionBase1;
import org.apache.sis.referencing.CRS;
import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.Geometry;
import org.opengis.referencing.crs.CoordinateReferenceSystem;
import org.opengis.referencing.cs.CoordinateSystemAxis;
import org.opengis.util.FactoryException;

import io.github.galbiston.geosparql_jena.implementation.GeometryWrapper;

public class IsInCRSAreaOfValidity extends FunctionBase1 {

	@Override
	public NodeValue exec(NodeValue v) {
		GeometryWrapper wrapper1=GeometryWrapper.extract(v);
		CoordinateReferenceSystem crs=null;
		Geometry geom=null;
		try {
			if(wrapper1 instanceof GeometryWrapper) {
				crs = CRS.forCode("EPSG:"+((GeometryWrapper)wrapper1).getXYGeometry().getSRID());
				geom=((GeometryWrapper)wrapper1).getXYGeometry();
			}
			CoordinateSystemAxis x = crs.getCoordinateSystem().getAxis(0);
		    CoordinateSystemAxis y = crs.getCoordinateSystem().getAxis(1);
		    boolean xUnbounded = Double.isInfinite(x.getMinimumValue()) && Double.isInfinite(x.getMaximumValue());
	        boolean yUnbounded = Double.isInfinite(y.getMinimumValue()) && Double.isInfinite(y.getMaximumValue());
	        if (xUnbounded && yUnbounded) {
	            return NodeValue.makeBoolean(false);
	        }
	        Coordinate[] c = geom.getCoordinates();
	        for (int i = 0; i < c.length; i++) {
	            if (!xUnbounded && ((c[i].x < x.getMinimumValue()) || (c[i].x > x.getMaximumValue()))) {
	            	return NodeValue.makeBoolean(false);
	            }
	            if (!yUnbounded && ((c[i].y < y.getMinimumValue()) || (c[i].y > y.getMaximumValue()))) {
	                return NodeValue.makeBoolean(false);
	            }
	        }
			return NodeValue.makeBoolean(true);
		} catch (FactoryException ex) {
			throw new ExprEvalException(ex.getMessage(), ex);
		}
	}

}
