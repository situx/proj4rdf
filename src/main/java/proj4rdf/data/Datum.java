package proj4rdf.data;

import java.io.StringWriter;
import java.util.List;

import javax.xml.stream.XMLOutputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;

import org.apache.jena.query.ResultSet;
import org.json.JSONObject;

import com.sun.xml.txw2.output.IndentingXMLStreamWriter;

/**
 * Representation of a geodetic datum.
 *
 */
public class Datum {

	/** The type of the datum.*/
	public String datumType;
	
	/** An identifier for the datum.*/
	public String datumName;
	
	/**The description of the ellipsoid/geoid which this datum uses.*/
	public Ellipsoid ellipsoid;
	
	/**Optional description of a prime meridian.*/
	public PrimeMeridian primeMeridian;
	
	public String interstellarbody;
	
	public List<String> usagescope;
	
	public String toProj() {
		StringBuilder builder=new StringBuilder();
		return builder.toString();
	}
	
	public JSONObject toProjJSON() {
		JSONObject result=new JSONObject();
		result.put("name",datumName);		
		result.put("type",datumType);
		result.put("ellipsoid", ellipsoid.toProjJSON());
		return result;
	}
	
	public String toGML() {
		XMLOutputFactory factory = XMLOutputFactory.newInstance();
		StringWriter strwriter=new StringWriter();
		XMLStreamWriter writer;
		try {
			writer = new IndentingXMLStreamWriter(factory.createXMLStreamWriter(strwriter));
			if(datumType.contains("ReferenceFrame")) {
				writer.writeStartElement("gml:"+datumType.replace("ReferenceFrame", "Datum"));
			}else {
				writer.writeStartElement("gml:"+datumType);					
			}
			writer.writeStartElement("gml:datumName");
			writer.writeCharacters(this.datumName);
			writer.writeEndElement();
			if(primeMeridian!=null) {
				writer.writeStartElement("gml:usesPrimeMeridian");
				writer.writeCharacters(System.lineSeparator());
				writer.flush();
				strwriter.write(primeMeridian.toGML()+System.lineSeparator());
				writer.writeEndElement();
			}
			if(ellipsoid!=null) {
				writer.writeStartElement("gml:usesEllipsoid");
				writer.writeCharacters(System.lineSeparator());
				writer.flush();
				strwriter.write(this.ellipsoid.toGML()+System.lineSeparator());
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
	
	
	@Override
	public String toString() {
		return "Datum [datumType=" + datumType + ", datumName=" + datumName + ", ellipsoid=" + ellipsoid + "]";
	}

	public String toWKT() {
		StringBuilder builder=new StringBuilder();	
		if(datumName==null)
			return builder.toString();
		builder.append("DATUM["+"\""+datumName.replace("Datum:","").trim()+"\","+System.lineSeparator());
		builder.append(ellipsoid.toWKT()+"]"+System.lineSeparator());
		if(primeMeridian!=null) {
			builder.append(","+primeMeridian.toWKT()+System.lineSeparator());
		}
		//builder.append("]");
		return builder.toString();
	}
	
	public ResultSet datumQuery() {
		return null;
	}
}
