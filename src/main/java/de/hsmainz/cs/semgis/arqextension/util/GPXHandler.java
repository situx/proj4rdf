package de.hsmainz.cs.semgis.arqextension.util;

import java.util.LinkedList;
import java.util.List;

import org.locationtech.jts.geom.Coordinate;
import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.ext.DefaultHandler2;

public class GPXHandler extends DefaultHandler2{

	public List<List<Coordinate>> coordinates=new LinkedList<List<Coordinate>>();
	
	public Boolean insegment=false;
	
	public Integer currentIndex=0;
	
	@Override
	public void startElement(String uri, String localName, String qName, Attributes attributes) throws SAXException {
		// TODO Auto-generated method stub
		super.startElement(uri, localName, qName, attributes);
		switch(qName) {
		case "trkseg":
			coordinates.add(new LinkedList<Coordinate>());
			insegment=true;
			break;
		case "trkpt":
			Coordinate coord=new Coordinate(Double.valueOf(attributes.getValue("lat")),Double.valueOf(attributes.getValue("lon")));
			coordinates.get(currentIndex).add(coord);
			break;
		}
	}
	
	@Override
	public void endElement(String uri, String localName, String qName) throws SAXException {
		// TODO Auto-generated method stub
		super.endElement(uri, localName, qName);
		switch(qName) {
		case "trkseg":
			insegment=false;	
			break;
		}
	}
	
}
