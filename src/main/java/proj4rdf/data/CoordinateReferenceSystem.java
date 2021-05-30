package proj4rdf.data;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.StringWriter;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;

import javax.xml.stream.XMLOutputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;

import org.apache.jena.ontology.OntModel;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.sis.referencing.CRS;
import org.json.JSONObject;
import org.opengis.referencing.NoSuchAuthorityCodeException;
import org.opengis.util.FactoryException;

import com.sun.xml.txw2.output.IndentingXMLStreamWriter;

public class CoordinateReferenceSystem {

	public CoordinateReferenceSystem sourceCRS;

	public String crsName;
	
	public String crsType;
	
	public String id;
	
	@Override
	public String toString() {
		return "CoordinateReferenceSystem [sourceCRS=" + sourceCRS + ", crsName=" + crsName + ", crsType=" + crsType
				+ ", id=" + id + ", authority=" + authority + ", scope=" + scope + ", area=" + area + ", remarks="
				+ remarks + ", areaOfValidity=" + areaOfValidity + ", conv=" + conv + ", datum=" + datum + ", cSystem="
				+ cSystem + "]";
	}


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
			switch(crsType) {
			case "PROJCRS": writer.writeStartElement("gml:ProjectedCRS");
			break;
			case "GEODCRS": writer.writeStartElement("gml:GeodeticCRS");
			break;
			case "BOUNDCRS": writer.writeStartElement("gml:BoundCRS");
			break;
			case "COMPOUNDCRS": writer.writeStartElement("gml:CompoundCRS");
			break;
			case "VERTCRS": writer.writeStartElement("gml:VerticalCRS");
			break;
			case "ENGCRS": writer.writeStartElement("gml:EngineeringCRS");
			break;
			case "PARAMETRICCRS": writer.writeStartElement("gml:ParametricCRS");
			break;
			case "TIMECRS": writer.writeStartElement("gml:TimeCRS");
			break;
			default: 
				writer.writeStartElement("gml:GeographicCRS");
			}
			writer.writeStartElement("gml:srsName");
			writer.writeCharacters(this.crsName);
			writer.writeEndElement();
			if(this.cSystem!=null) {
				writer.writeStartElement("gml:usesEllipsoidalCS");
				writer.writeCharacters(System.lineSeparator());
				writer.flush();
				strwriter.write(this.cSystem.toGML()+System.lineSeparator());
				writer.writeEndElement();
			}
			if(this.datum!=null) {
				writer.writeStartElement("gml:usesGeodeticDatum");
				writer.writeCharacters(System.lineSeparator());
				writer.flush();
				strwriter.write(this.datum.toGML()+System.lineSeparator());
				writer.writeEndElement();
			}
			writer.writeEndElement();
			writer.writeEndDocument();
		} catch (XMLStreamException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return strwriter.toString();
	}
	
	public static OntModel WKTToRDF(String wkt) throws FactoryException, IOException {
		OntModel result=ModelFactory.createOntologyModel();
		Set<String> resultset=new TreeSet<String>();
		org.opengis.referencing.crs.CoordinateReferenceSystem res = CRS.fromWKT(wkt);
		String crsid="geocrs:"+res.getName().getCode().replace(" ", "_");
		String csid=crsid+"_cs";//geocrs:"+res.getCoordinateSystem().getName().getCode().replace(" ", "_").replace(".", "").replace(",", "").replace(":", "");		
		resultset.add(crsid+" rdf:type geocrs:"+res.ALIAS_KEY+" ."+System.lineSeparator());
		resultset.add(crsid+" rdfs:label \""+res.getName()+"\"@en ."+System.lineSeparator());
		resultset.add(crsid+" geocrs:coordinateSystem "+csid+" ."+System.lineSeparator());
		resultset.add(crsid+" geocrs:scope \""+res.getScope()+"\"@en ."+System.lineSeparator());
		resultset.add(crsid+" geocrs:area_of_use geocrs:"+crsid+"_aou ."+System.lineSeparator());
		resultset.add(crsid+"_aou rdf:type geocrs:AreaOfUse ."+System.lineSeparator());
		resultset.add(crsid+"_aou geo:asWKT \"ENVELOPE()\"^^geo:wktLiteral ."+System.lineSeparator());
		resultset.add(csid+" rdf:type geocrs:CoordinateSystem ."+System.lineSeparator());
		resultset.add(csid+" rdfs:label \""+res.getCoordinateSystem().getName()+"\"@en ."+System.lineSeparator());
		resultset.add("geocrs:coordinateSystem rdf:type owl:ObjectProperty ."+System.lineSeparator());
		resultset.add("geocrs:area_of_use rdf:type owl:ObjectProperty ."+System.lineSeparator());
		resultset.add("geocrs:axis rdf:type owl:ObjectProperty ."+System.lineSeparator());
		for(int i=0;i<res.getCoordinateSystem().getDimension();i++) {
			String axisid=csid+"_axis"+i;
			resultset.add(csid+" geocrs:axis "+axisid+" ."+System.lineSeparator());
			resultset.add(axisid+" rdf:type geocrs:CoordinateSystemAxis ."+System.lineSeparator());
			resultset.add(axisid+" geocrs:abbreviation \""+res.getCoordinateSystem().getAxis(i).getAbbreviation()+"\" ."+System.lineSeparator());				
			resultset.add(axisid+" geocrs:direction geocrs:"+res.getCoordinateSystem().getAxis(i).getDirection().identifier()+" ."+System.lineSeparator());
			resultset.add(axisid+" geocrs:unit om:"+res.getCoordinateSystem().getAxis(i).getUnit().getName()+" ."+System.lineSeparator());
			resultset.add("geocrs:"+res.getCoordinateSystem().getAxis(i).getDirection().identifier()+" rdf:type geocrs:AxisDirection ."+System.lineSeparator());
		}
		StringBuilder builder=new StringBuilder();
		builder.append("@prefix geocrs:<http://www.opengis.net/ont/crs/> ."+System.lineSeparator());
		builder.append("@prefix geo:<http://www.opengis.net/ont/> ."+System.lineSeparator());
		builder.append("@prefix rdfs:<http://www.w3.org/2000/01/rdf-schema#> ."+System.lineSeparator());
		builder.append("@prefix rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> ."+System.lineSeparator());
		builder.append("@prefix owl:<http://www.w3.org/2002/07/owl#> ."+System.lineSeparator());	
		builder.append("@prefix om:<http://www.ontology-of-units-of-measure.org/resource/om-2/> ."+System.lineSeparator());			
		for(String trip:resultset) {
			builder.append(trip);
		}
		System.out.println(builder.toString());
		FileWriter writer=new FileWriter(new File("importtest.ttl"));
		writer.write(builder.toString());
		writer.close();
		return result;
	}

	public static OntModel GMLToRDF(String gml) throws FactoryException {
		CRS.fromXML(gml);
		OntModel result=ModelFactory.createOntologyModel();
		return result;
	}
	
	
	public String toWKT() {
		StringBuilder builder=new StringBuilder();
		builder.append(crsType+"[");
		builder.append("\""+crsName+"\","+System.lineSeparator());
		if(sourceCRS!=null) {
			builder.append(sourceCRS.toWKT()+","+System.lineSeparator());
		}
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
	
	public static OntModel fromWKT(String wktString) {
		OntModel result=ModelFactory.createOntologyModel();
		List<String> parts=new LinkedList<String>();
		System.out.println("{"+wktString+"}");
		String lastWord="";
		int bracketopencounter=0,bracketclosecounter=0;
		for(int i=0;i<wktString.length();i++) {
			System.out.println(wktString.charAt(i));
			if(wktString.charAt(i)==' ') {
				lastWord="";
			}else {
				lastWord+=wktString.charAt(i);
			}
			if(wktString.charAt(i)=='[') {
				//System.out.println("Bracket open!!!");
				bracketopencounter++;
				if(parts.size()<bracketopencounter) {
					parts.add(lastWord);
				}

			}
			//System.out.println(parts);
			for(int j=0;j<bracketopencounter;j++) {
				parts.set(j, parts.get(j)+wktString.charAt(i));
			}
		}
		for(String p:parts) {
			System.out.println("====");
			System.out.println(p);
		}
		return result;
	}
	
	
	public static void main(String[] args) throws NoSuchAuthorityCodeException, UnsupportedOperationException, FactoryException, IOException {
		fromWKT(CRS.forCode("EPSG:4326").toWKT());
	}
	
}
