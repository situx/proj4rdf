package proj4rdf.data;

import org.json.JSONObject;

public class PrimeMeridian {

	public String primeMeridianName;
	
	public String angleunit;
	
	public Double longitude;
	
	public String toProj() {
		StringBuilder builder=new StringBuilder();
		return builder.toString();
	}
	
	public JSONObject toProjJSON() {
		JSONObject result=new JSONObject();
		result.put("type", "PrimeMeridian");
		result.put("name", primeMeridianName);
		result.put("longitude", longitude);
		return result;
	}
	
	public JSONObject toGML() {
		JSONObject result=new JSONObject();
		return result;
	}
	
	
	public String toWKT() {
		StringBuilder builder=new StringBuilder();
		builder.append("PRIMEM[");
		builder.append("\""+primeMeridianName+"\",");
		builder.append(longitude+",");
		if(angleunit.contains("degree") || angleunit.contains("rad")) {
			builder.append("ANGLEUNIT[\""+angleunit+"\",0.0174532925199433]");			
		}else {
			builder.append("LENGTHUNIT[\""+angleunit+"\",0.0174532925199433]");
		}
		builder.append("]");
		return builder.toString();
	}
	
}
