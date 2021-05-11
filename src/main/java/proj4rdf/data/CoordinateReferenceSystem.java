package proj4rdf.data;

import java.io.StringWriter;

import javax.xml.stream.XMLOutputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;

import org.json.JSONObject;

import com.sun.xml.txw2.output.IndentingXMLStreamWriter;

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
	
	public ConversionOperation conv;
	
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
	
	public String toGML() {
		XMLOutputFactory factory = XMLOutputFactory.newInstance();
		StringWriter strwriter=new StringWriter();
		XMLStreamWriter writer;
		try {
			writer = new IndentingXMLStreamWriter(factory.createXMLStreamWriter(strwriter));
			writer.writeStartDocument();
			writer.writeStartElement("gml:GeodeticCRS");		
			writer.writeEndElement();
			writer.writeEndDocument();
		} catch (XMLStreamException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return strwriter.toString();
	}
	
	
	public String toWKT() {
		StringBuilder builder=new StringBuilder();
		builder.append("GEODCRS[");
		builder.append("\""+crsName+"\","+System.lineSeparator());
		if(datum!=null) {
			builder.append(datum.toWKT()+","+System.lineSeparator());
		}
		if(cSystem!=null) {
			builder.append(cSystem.toWKT()+System.lineSeparator());
		}
		if(conv!=null) {
			builder.append(conv.toWKT()+System.lineSeparator());
		}
		if(areaOfValidity!=null) {
			builder.append(areaOfValidity.toWKT()+System.lineSeparator());
		}
		builder.append("]");
		return builder.toString();
	}
	
}
