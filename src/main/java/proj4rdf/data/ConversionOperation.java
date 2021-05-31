package proj4rdf.data;

import java.io.StringWriter;
import java.util.Map;
import java.util.TreeMap;

import javax.xml.stream.XMLOutputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;

import org.json.JSONObject;

import com.sun.xml.txw2.output.IndentingXMLStreamWriter;

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
	
	public String toGML() {
		XMLOutputFactory factory = XMLOutputFactory.newInstance();
		StringWriter strwriter=new StringWriter();
		XMLStreamWriter writer;
		try {
			writer = new IndentingXMLStreamWriter(factory.createXMLStreamWriter(strwriter));
			writer.writeStartElement("gml:Conversion");
			for(String key:parameters.keySet()) {
				writer.writeStartElement("gml:usesParameterValue");
				writer.writeStartElement("gml:value");
				writer.writeCharacters(parameters.get(key));
				writer.writeEndElement();
				writer.writeEndElement();
			}
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
