package proj4rdf.data;

import org.json.JSONObject;

public class Axis {
	
	@Override
	public String toString() {
		return "Axis [angleunit=" + angleunit + ", unitconversionfactor=" + unitconversionfactor + ", axisname="
				+ axisname + ", axisdirection=" + axisdirection + ", axisabbreviation=" + axisabbreviation
				+ ", axisorder=" + axisorder + "]";
	}


	public String angleunit;
	
	public Double unitconversionfactor;
	
	public String axisname;
	
	public String axisdirection;
	
	public String axisabbreviation;
	
	public Integer axisorder;

	public String toProj() {
		StringBuilder builder=new StringBuilder();
		return builder.toString();
	}
	
	public JSONObject toProjJSON() {
		JSONObject result=new JSONObject();
		result.put("name", axisname);
		result.put("abbreviation", axisabbreviation);
		result.put("direction", axisdirection);
		result.put("unit", angleunit);
		return result;
	}
	
	public JSONObject toGML() {
		JSONObject result=new JSONObject();
		result.put("name", axisname);
		result.put("abbreviation", axisabbreviation);
		result.put("direction", axisdirection);
		result.put("unit", angleunit);
		return result;
	}
	
	
	public String toWKT() {
		StringBuilder builder=new StringBuilder();	
		builder.append("AXIS["+"\""+axisname+"\","+axisdirection+",ORDER["+axisorder+"],");
		if(angleunit.contains("degree") || angleunit.contains("rad")) {
			builder.append("ANGLEUNIT[");			
		}else {
			builder.append("LENGTHUNIT[");
		}
		builder.append("\""+angleunit+"\","+unitconversionfactor+"]");
		builder.append("]");
		return builder.toString();
	}
	
}
