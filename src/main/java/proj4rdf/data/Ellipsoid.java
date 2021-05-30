package proj4rdf.data;

import java.io.StringWriter;

import javax.xml.stream.XMLOutputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;

import org.json.JSONObject;

import com.sun.xml.txw2.output.IndentingXMLStreamWriter;

/**
 * Representation of the ellipsoid of a geodetic datum.
 *
 */
public class Ellipsoid {

	
	@Override
	public String toString() {
		return "Ellipsoid [ellipsoidName=" + ellipsoidName + ", semiMajorAxis=" + semiMajorAxis + ", semiMinorAxis="
				+ semiMinorAxis + ", inverseFlattening=" + inverseFlattening + ", lengthUnit=" + lengthUnit + "]";
	}

	/** Identifier of the ellipsoid.*/
	public String ellipsoidName;
	/**The semi major axis of the ellipsoid.*/
	public Double semiMajorAxis;
	/**The semi minor axis of the ellipsoid.*/
	public Double semiMinorAxis;
	/**The inverse flattening parameter of the ellipsoid.*/
	public Double inverseFlattening;
	
	public String lengthUnit;
	/**The eccentricity of the ellipsoid.*/
	public Double eccentricity;
	/**The flattening parameter of the ellipsoid.*/
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
	
	public String toGML() {
		XMLOutputFactory factory = XMLOutputFactory.newInstance();
		StringWriter strwriter=new StringWriter();
		XMLStreamWriter writer;
		try {
			writer = new IndentingXMLStreamWriter(factory.createXMLStreamWriter(strwriter));
			writer.writeStartElement("gml:Ellipsoid");	
			writer.writeStartElement("gml:ellipsoidName");
			writer.writeCharacters(this.ellipsoidName);
			writer.writeEndElement();
			writer.writeStartElement("gml:semiMajorAxis");
			writer.writeCharacters(this.semiMajorAxis.toString());
			writer.writeEndElement();
			writer.writeStartElement("gml:secondDefiningParameter");
			writer.writeStartElement("gml:inverseFlattening");
			if(this.lengthUnit!=null)
				writer.writeAttribute("gml:uom", this.lengthUnit);
			writer.writeCharacters(this.inverseFlattening.toString());
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
	
	/**
	 * Converts the representation to WKT.
	 * @return The WKT representation of the ellipsoid as String
	 */
	public String toWKT() {
		StringBuilder builder=new StringBuilder();	
		builder.append("ELLIPSOID["+"\""+ellipsoidName+"\","+semiMajorAxis+","+inverseFlattening+System.lineSeparator());
		if(lengthUnit!=null) {
			builder.append(",LENGTHUNIT[\""+lengthUnit+"\",1]"+System.lineSeparator());
		}
		builder.append("]");
		return builder.toString();
	}
}
