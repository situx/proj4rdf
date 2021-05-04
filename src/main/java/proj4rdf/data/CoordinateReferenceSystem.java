package proj4rdf.data;

import org.json.JSONObject;

public class CoordinateReferenceSystem {

	@Override
	public String toString() {
		return "CoordinateReferenceSystem [crsName=" + crsName + ", crsType=" + crsType + ", id=" + id + ", authority="
				+ authority + ", scope=" + scope + ", area=" + area + ", areaOfValidity=" + areaOfValidity + ", datum="
				+ datum + ", cSystem=" + cSystem + "]";
	}


	public String crsName;
	
	public String crsType;
	
	public String id;
	
	public String authority;
	
	public String scope;
	
	public String area;
	
	public String remarks;
	
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
		if(areaOfValidity!=null)
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
		builder.append("GEOGCRS[");
		builder.append("\""+crsName+"\",");
		if(datum!=null) {
			builder.append(datum.toWKT()+",");
		}
		if(cSystem!=null) {
			builder.append(cSystem.toWKT());
		}
		builder.append("]");
		return builder.toString();
	}
	
}
