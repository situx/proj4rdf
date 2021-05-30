package proj4rdf.data;

import java.io.StringWriter;

import javax.xml.stream.XMLOutputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;

import org.json.JSONObject;

import com.sun.xml.txw2.output.IndentingXMLStreamWriter;

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
	
	public String toGML() {
		XMLOutputFactory factory = XMLOutputFactory.newInstance();
		StringWriter strwriter=new StringWriter();
		XMLStreamWriter writer;
		try {
			writer = new IndentingXMLStreamWriter(factory.createXMLStreamWriter(strwriter));
			writer.writeStartElement("gml:PrimeMeridian");	
			writer.writeStartElement("gml:meridianName");
			writer.writeCharacters(this.primeMeridianName);
			writer.writeEndElement();
			writer.writeStartElement("gml:greenwichLongitude");
			writer.writeStartElement("gml:angle");
			writer.writeAttribute("gml:uom", angleunit);
			writer.writeCharacters(longitude.toString());
			writer.writeEndElement();
			writer.writeEndElement();		
			writer.writeEndElement();
			writer.flush();
		} catch (XMLStreamException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return strwriter.toString();
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
