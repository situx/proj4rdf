package proj4rdf.functions.srs;

import java.util.LinkedList;
import java.util.List;

import org.apache.jena.sparql.expr.ExprEvalException;
import org.apache.jena.sparql.expr.NodeValue;
import org.apache.jena.sparql.function.FunctionBase3;
import org.apache.sis.geometry.DirectPosition2D;
import org.apache.sis.referencing.CRS;
import org.locationtech.jts.geom.Coordinate;
import org.opengis.geometry.DirectPosition;
import org.opengis.geometry.MismatchedDimensionException;
import org.opengis.referencing.crs.CoordinateReferenceSystem;
import org.opengis.referencing.operation.CoordinateOperation;
import org.opengis.referencing.operation.TransformException;
import org.opengis.util.FactoryException;

import io.github.galbiston.geosparql_jena.implementation.GeometryWrapper;
import proj4rdf.RDFCRSToWKT;

public class ConvertCRS extends FunctionBase3 {

	@Override
	public NodeValue exec(NodeValue geomliteral, NodeValue crsURI, NodeValue endpoint) {
		GeometryWrapper geomwrap=GeometryWrapper.extract(geomliteral);
		String res = RDFCRSToWKT.getCRSFromTripleStore(crsURI.getString(), endpoint.getString(), "WKT");
		try {
			CoordinateReferenceSystem targetCRS = CRS.fromWKT(res);
			CoordinateOperation op;
			op = CRS.findOperation(geomwrap.getCRS(), targetCRS, null);
			List<Coordinate> coords=new LinkedList<Coordinate>();
			for(Coordinate coord:geomwrap.getXYGeometry().getCoordinates()) {
				 DirectPosition pos;
					pos = op.getMathTransform().transform(new DirectPosition2D(coord.x,coord.y), null);
				 Coordinate curcor=new Coordinate(pos.getCoordinate()[0],pos.getCoordinate()[1]);
				 coords.add(curcor);
			}
			return RDFCRSToWKT.createGeometry(coords.toArray(new Coordinate[0]), geomwrap.getGeometryType(), geomwrap).asNodeValue();
		} catch (FactoryException | MismatchedDimensionException | TransformException ex) {
            throw new ExprEvalException(ex.getMessage(), ex);
		}
		
	}
	

}
