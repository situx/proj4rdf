package proj4rdf.data;

import java.io.StringWriter;

import javax.xml.stream.XMLOutputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;

import org.json.JSONObject;

import com.sun.xml.txw2.output.IndentingXMLStreamWriter;

/**
 * Represents the axis of a coordinate system.
 *
 */
public class Axis {
	
	@Override
	public String toString() {
		return "Axis [angleunit=" + angleunit + ", unitconversionfactor=" + unitconversionfactor + ", axisname="
				+ axisname + ", axisdirection=" + axisdirection + ", axisabbreviation=" + axisabbreviation
				+ ", axisorder=" + axisorder + "]";
	}


	public String angleunit;
	
	public Double unitconversionfactor;
	/**The name of the coordinate system axis.*/
	public String axisname;
	/**The direction of the coordinate system axis.*/
	public String axisdirection;
	/**The abbreviation of the coordinate system axis.*/
	public String axisabbreviation;
	/**Order index of the axis in the coordinate system description.*/
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
	
	public String toGML() {
		XMLOutputFactory factory = XMLOutputFactory.newInstance();
		StringWriter strwriter=new StringWriter();
		XMLStreamWriter writer;
		try {
			writer = new IndentingXMLStreamWriter(factory.createXMLStreamWriter(strwriter));
			writer.writeStartElement("gml:CoordinateSystemAxis");	
			writer.writeStartElement("gml:name");
			writer.writeCharacters(this.axisname);
			writer.writeEndElement();
			writer.writeStartElement("gml:axisAbbrev");
			writer.writeCharacters(this.axisabbreviation);
			writer.writeEndElement();
			writer.writeStartElement("gml:axisDirection");
			writer.writeCharacters(this.axisdirection);
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
