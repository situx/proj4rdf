package proj4rdf.data;

import org.json.JSONObject;

public class Ellipsoid {

	
	@Override
	public String toString() {
		return "Ellipsoid [ellipsoidName=" + ellipsoidName + ", semiMajorAxis=" + semiMajorAxis + ", semiMinorAxis="
				+ semiMinorAxis + ", inverseFlattening=" + inverseFlattening + ", lengthUnit=" + lengthUnit + "]";
	}


	public String ellipsoidName;
	
	public Double semiMajorAxis;
	
	public Double semiMinorAxis;
	
	public Double inverseFlattening;
	
	public String lengthUnit;
	
	public Double eccentricity;
	
	public Double flatteningParameter;
	
	public String toProj() {
		StringBuilder builder=new StringBuilder();
		return builder.toString();
	}
	
	public JSONObject toProjJSON() {
		JSONObject result=new JSONObject();
		result.put("name", ellipsoidName);
		if(semiMajorAxis!=null)
			result.put("semi_major_axis", semiMajorAxis);
		if(semiMinorAxis!=null)
			result.put("semi_minor_axis", semiMinorAxis);
		if(inverseFlattening!=null)
			result.put("inverse_flattening", inverseFlattening);
		return result;
	}
	
	public JSONObject toGML() {
		JSONObject result=new JSONObject();
		return result;
	}
	
	
	public String toWKT() {
		StringBuilder builder=new StringBuilder();	
		builder.append("ELLIPSOID["+"\""+ellipsoidName+"\","+semiMajorAxis+","+inverseFlattening+"]");
		return builder.toString();
	}
}
