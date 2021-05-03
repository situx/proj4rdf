package proj4rdf.data;

import java.util.LinkedList;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONObject;

public class CoordinateSystem {

	@Override
	public String toString() {
		return "CoordinateSystem [axisList=" + axisList + ", coordinateSystemType=" + coordinateSystemType
				+ ", numberDimensions=" + numberDimensions + "]";
	}



	List<Axis> axisList=new LinkedList<Axis>();
	
	public String coordinateSystemType;
	
	public Integer numberDimensions;
	
	public String toProj() {
		StringBuilder builder=new StringBuilder();
		return builder.toString();
	}
	
	public JSONObject toProjJSON() {
		JSONObject cs=new JSONObject();
		cs.put("type", "CoordinateSystem");
		cs.put("subtype", coordinateSystemType);
		cs.put("axis", new JSONArray());
		for(Axis axis:axisList) {
			cs.getJSONArray("axis").put(axis.toProjJSON());
		}
		return cs;
	}
	

	
	public String toWKT() {
		StringBuilder builder=new StringBuilder();
		builder.append("CS["+coordinateSystemType+","+numberDimensions+"],");
		for(Axis axis:axisList) {
			builder.append(axis.toWKT()+",");
		}
		builder.delete(builder.length()-1, builder.length());
		return builder.toString();
	}
	
}
