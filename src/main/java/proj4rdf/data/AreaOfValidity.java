package proj4rdf.data;

import org.json.JSONObject;

public class AreaOfValidity {

	public String toProj() {
		StringBuilder builder=new StringBuilder();
		return builder.toString();
	}
	
	public JSONObject toProjJSON() {
		JSONObject result=new JSONObject();
		return result;
	}
	
	public JSONObject toGML() {
		JSONObject result=new JSONObject();
		return result;
	}
	
	
	public String toWKT() {
		StringBuilder builder=new StringBuilder();	
		//builder.append("ELLIPSOID["+"'"+ellipsoidName+"',"+semiMajorAxis+","+inverseFlattening+"]");
		return builder.toString();
	}
	
}
