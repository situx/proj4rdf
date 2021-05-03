package proj4rdf;

import java.io.IOException;
import java.io.Writer;
import java.util.Map;
import java.util.TreeMap;

import org.apache.jena.query.ResultSet;

import proj4rdf.formatter.ProjFormatter;
import proj4rdf.formatter.ProjJSONFormatter;
import proj4rdf.formatter.WKTCRSFormatter;

/**
 * Abstract class to downlift query results.
 *
 */
public abstract class ResultFormatter {

	public static Map<String,ResultFormatter> resultMap=new TreeMap<String, ResultFormatter>();

	public static Map<String, String> labelMap=new TreeMap<String, String>();
	
	public Integer lastQueriedElemCount=0;
	
	public String mimeType="text/plain";
	
	public String exposedType="application/vnd.geojson";
	
	public String urlformat="json";
	
	public String label="JSON";
	
	public String definition="";
	
	public String fileextension="json";
	
	public Boolean constructQuery=false;
	
	
	public static final Integer FLUSHTHRESHOLD=20;

	public static final String[] mediatypes= {
			"application/vnd.geo+json+ld",
			"text/csv",			
	};
	
	public static ResultFormatter getFormatter(String formatString) {
		formatString=formatString.toLowerCase();
		if(resultMap.containsKey(formatString)) {
			return resultMap.get(formatString);
		}
		if(formatString.contains("proj")) {
			return resultMap.get("proj");
		}
		if(formatString.contains("projjson")) {
			return resultMap.get("projjson");
		}
		if(formatString.contains("wktcrs")) {
			return resultMap.get("wktcrs");
		}
		return resultMap.get("projjson");
	}
	
	static void addToMaps(String key,ResultFormatter format) {
		resultMap.put(key, format);
		labelMap.put(key,format.label);
		resultMap.put(format.mimeType, format);
	}
	
	static {
		addToMaps("proj",new ProjFormatter());
		addToMaps("projjson",new ProjJSONFormatter());
		addToMaps("wktcrs",new WKTCRSFormatter());
	}

	
	public abstract String formatter(ResultSet results,Writer out) throws IOException;

}
