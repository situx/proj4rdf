package proj4rdf.data;

import java.io.StringWriter;
import java.util.LinkedList;
import java.util.List;

import javax.xml.stream.XMLOutputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;

import org.json.JSONArray;
import org.json.JSONObject;

import com.sun.xml.txw2.output.IndentingXMLStreamWriter;

/**
 * Representation of a coordinate system as a part of a SRS.
 *
 */
public class CoordinateSystem {

	@Override
	public String toString() {
		return "CoordinateSystem [axisList=" + axisList + ", coordinateSystemType=" + coordinateSystemType
				+ ", numberDimensions=" + numberDimensions + "]";
	}

	public List<Axis> axisList=new LinkedList<Axis>();
	
	public String coordinateSystemType;
	
	public Integer numberDimensions;

	public String coordinateSystemName;
	
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
	
	
	public String toGML() {
		XMLOutputFactory factory = XMLOutputFactory.newInstance();
		StringWriter strwriter=new StringWriter();
		XMLStreamWriter writer;
		try {
			writer = new IndentingXMLStreamWriter(factory.createXMLStreamWriter(strwriter));
			if(coordinateSystemType.contains("PlanarCoordinateSystem")) {
				writer.writeStartElement("gml:CartesianCS");
			}else {
				writer.writeStartElement("gml:"+coordinateSystemType);				
			}
			if(this.coordinateSystemName!=null) {
				writer.writeStartElement("gml:csName");
				writer.writeCharacters(this.coordinateSystemName);
				writer.writeEndElement();
			}
			for(Axis ax:axisList) {
				writer.writeStartElement("gml:usesAxis");
				writer.writeCharacters(System.lineSeparator());
				writer.flush();
				strwriter.write(ax.toGML()+System.lineSeparator());
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
		if(coordinateSystemType==null)
			return builder.toString();
		builder.append("CS["+System.lineSeparator());
		if(coordinateSystemType.contains("CS:")) {
			builder.append(coordinateSystemType.substring(coordinateSystemType.lastIndexOf(':')+1).trim()+System.lineSeparator());
		}else {
			builder.append(coordinateSystemType+System.lineSeparator());
		}
		builder.append(","+numberDimensions+"],");
		for(Axis axis:axisList) {
			builder.append(axis.toWKT()+",");
		}
		builder.delete(builder.length()-1, builder.length());
		return builder.toString()+System.lineSeparator();
	}
	
}
