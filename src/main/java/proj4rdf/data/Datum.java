package proj4rdf.data;

import org.apache.jena.query.ResultSet;
import org.json.JSONObject;

public class Datum {

	public String datumType;
	
	public String datumName;
	
	public Ellipsoid ellipsoid;
	
	public PrimeMeridian primeMeridian;
	
	public String toProj() {
		StringBuilder builder=new StringBuilder();
		return builder.toString();
	}
	
	public JSONObject toProjJSON() {
		JSONObject result=new JSONObject();
		result.put("name",datumName);		
		result.put("type",datumType);
		result.put("ellipsoid", ellipsoid.toProjJSON());
		return result;
	}
	
	public JSONObject toGML() {
		JSONObject result=new JSONObject();
		return result;
	}
	
	
	@Override
	public String toString() {
		return "Datum [datumType=" + datumType + ", datumName=" + datumName + ", ellipsoid=" + ellipsoid + "]";
	}

	public String toWKT() {
		StringBuilder builder=new StringBuilder();	
		builder.append("DATUM["+"'"+datumName+"',");
		builder.append(ellipsoid.toWKT());
		if(primeMeridian!=null) {
			builder.append(","+primeMeridian.toWKT());
		}
		builder.append("]");
		return builder.toString();
	}
	
	public ResultSet datumQuery() {
		return null;
	}
}
