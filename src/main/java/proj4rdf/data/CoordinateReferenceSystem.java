package proj4rdf.data;

import org.json.JSONObject;

public class CoordinateReferenceSystem {

	public String crsName;
	
	public String crsType;
	
	public String id;
	
	public String authority;
	
	public String scope;
	
	public String area;
	
	public AreaOfValidity areaOfValidity;
	
	public Datum datum;
	
	public CoordinateSystem cSystem;
	
	public String toProj() {
		StringBuilder builder=new StringBuilder();
		return builder.toString();
	}
	
	public JSONObject toProjJSON() {
		JSONObject result=new JSONObject();
		result.put("name", crsName);
		result.put("type",crsType);
		result.put("scope", scope);
		result.put("area", area);
		result.put("datum", datum.toProjJSON());
		result.put("coordinate_system",cSystem.toProjJSON());
		result.put("bbox", areaOfValidity.toProjJSON());
		result.put("id", new JSONObject());
		result.getJSONObject("id").put("code",id);
		result.getJSONObject("id").put("authority",authority);
		return result;
	}
	
	public JSONObject toGML() {
		JSONObject result=new JSONObject();
		return result;
	}
	
	
	public String toWKT() {
		StringBuilder builder=new StringBuilder();	
		return builder.toString();
	}
	
}
