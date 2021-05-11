package proj4rdf.data;

import org.json.JSONObject;

public class AreaOfValidity {

	public String areaString;
	
	public String bbox;
	
	public String scope;
	
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
		builder.append("");
		if(scope==null && areaString==null && bbox==null)
			return builder.toString();
		if(scope!=null) {
			builder.append("SCOPE[\""+scope+"\"],"+System.lineSeparator());
		}
		if(areaString!=null) {
			builder.append("AREA[\""+areaString+"\"],"+System.lineSeparator());
		}
		if(bbox!=null) {
			if(bbox.contains("ENVELOPE")) {
				builder.append("BBOX["+bbox.replace("ENVELOPE(","").replace(")","").replace(" ", ",")+"],");	
			}	
		}
		if(builder.substring(builder.length()-1, builder.length()).equals(",")) {
			builder.delete(builder.length()-1, builder.length());			
		}
		if(!builder.substring(0, 1).equals(",")) {
			builder.insert(0, ",");			
		}
		builder.append(System.lineSeparator());
		return builder.toString();
	}
	
}
