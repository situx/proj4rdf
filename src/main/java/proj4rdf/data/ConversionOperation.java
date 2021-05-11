package proj4rdf.data;

import java.util.Map;
import java.util.TreeMap;

import org.json.JSONObject;

public class ConversionOperation {

	public String methodName;
	
	public String projectionName;
	
	public Map<String,String> parameters=new TreeMap<String,String>();

	public String scope;
	
	
	public String toProj() {
		StringBuilder builder=new StringBuilder();
		return builder.toString();
	}
	
	public JSONObject toProjJSON() {
		JSONObject cs=new JSONObject();
		return cs;
	}
	
	public String toWKT() {
		StringBuilder builder=new StringBuilder();
		if(projectionName==null && methodName==null) {
			return builder.toString();
		}
		builder.append("CONVERSION[\""+projectionName+"\",METHOD[\""+methodName+"\","+System.lineSeparator());
		for(String para:parameters.keySet()) {
			builder.append("PARAMETER[\""+para+"\","+parameters.get(para)+"],");
		}
		builder.delete(builder.length()-1, builder.length());
		builder.append("]]"+System.lineSeparator());
		return builder.toString();
	}
	
}
