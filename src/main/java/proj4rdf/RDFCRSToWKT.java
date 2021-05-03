package proj4rdf;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Iterator;

import org.apache.jena.ontology.OntModel;
import org.apache.jena.query.Query;
import org.apache.jena.query.QueryExecution;
import org.apache.jena.query.QueryExecutionFactory;
import org.apache.jena.query.QueryFactory;
import org.apache.jena.query.QuerySolution;
import org.apache.jena.query.ResultSet;
import org.apache.jena.query.ResultSetFormatter;
import org.apache.jena.rdf.model.ModelFactory;

public class RDFCRSToWKT {
	
	public static String prefixCollection="";
	
	public static String curCRSURI="http://www.opengis.net/def/crs/EPSG/0/4326";
	
	public static String GeoSPARQLCRSURI="http://www.opengis.net/ont/crs/";
	
	//public static String downliftQuery="SELECT "
	
	static OntModel model;
	
	static {
		try {
			BufferedReader reader=new BufferedReader(new FileReader(new File("prefixes.txt")));
			String line;
			while((line=reader.readLine())!=null){
				prefixCollection+=line+System.lineSeparator();
			}
			reader.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	
	public static String getCRSFromTripleStore(String crsURI, String endpointURL, OntModel model) {
		String queryString="SELECT DISTINCT * WHERE { <"+curCRSURI+"> <"+GeoSPARQLCRSURI+"datum> ?datum . ?datum ?datumrel ?datumobj .  } ";
		System.out.println(prefixCollection+queryString);
		Query query = QueryFactory.create(prefixCollection+queryString);
		QueryExecution qexec = QueryExecutionFactory.create(query, model);
		ResultSet res=qexec.execSelect();
		return endpointURL;		
	}
	
	/*public static getEligibleCRSFromTripleStore(String bbox) {
		String queryString="SELECT DISTINCT ?crs WHERE { ?crs  <"+GeoSPARQLCRSURI+"datum> ?datum . ?datum ?datumrel ?datumobj .  } ";
		System.out.println(prefixCollection+queryString);
		Query query = QueryFactory.create(prefixCollection+queryString);
		QueryExecution qexec = QueryExecutionFactory.create(query, model);
		ResultSet res=qexec.execSelect();
		return endpointURL;		
	}*/
	
	public static void main(String[] args) throws IOException {
		model=ModelFactory.createOntologyModel();
		model.read(new FileReader(new File("result.ttl")),"","TTL");
		String queryString="SELECT DISTINCT * WHERE { <"+curCRSURI+"> <"+GeoSPARQLCRSURI+"datum> ?datum . ?datum ?datumrel ?datumobj .  } ";
		System.out.println(prefixCollection+queryString);
		Query query = QueryFactory.create(prefixCollection+queryString);
		QueryExecution qexec = QueryExecutionFactory.create(query, model);
		ResultSet res=qexec.execSelect();
		System.out.println(ResultSetFormatter.asText(res));
		
		//"query":"SELECT ?item ?rel ?val ?rel1 ?val1 ?rel2 ?val2 ?the_geom WHERE{ ?item rdf:type <http://inspire.ec.europa.eu/schemas/gn/4.0#NamedPlace> . ?item ?rel ?val . OPTIONAL{ ?val <http://www.opengis.net/ont/geosparql#asWKT> ?the_geom } OPTIONAL{?val ?rel1 ?val1 . FILTER(STRSTARTS(STR(?rel1), \"http://inspire.ec.europa.eu/schemas/gn/4.0#\")) OPTIONAL { ?val1 ?rel2 ?val2 . FILTER(STRSTARTS(STR(?rel2), \"http://inspire.ec.europa.eu/schemas/gn/4.0#\")) }} }",

		queryString="SELECT DISTINCT * WHERE { BIND(<"+curCRSURI+"> AS ?sub) ?sub ?rel ?obj . OPTIONAL {?obj ?rel2 ?obj2 . FILTER(STRSTARTS(STR(?rel2), \""+GeoSPARQLCRSURI+"\")) OPTIONAL {?obj2 ?rel3 ?obj3 . FILTER(STRSTARTS(STR(?rel3), \""+GeoSPARQLCRSURI+"\"))}} FILTER(STRSTARTS(STR(?rel), \""+GeoSPARQLCRSURI+"\")) } ORDER BY ?rel ";
		System.out.println(prefixCollection+queryString);
		query = QueryFactory.create(prefixCollection+queryString);
		qexec = QueryExecutionFactory.create(query, model);
		res=qexec.execSelect();
		FileWriter writer=new FileWriter(new File("queryresult.txt"));
		writer.write(ResultSetFormatter.asText(res));
		writer.close();
		queryString="SELECT DISTINCT * WHERE { BIND(<"+curCRSURI+"> AS ?sub) ?sub ?rel ?obj . OPTIONAL {?obj ?rel2 ?obj2 . FILTER(STRSTARTS(STR(?rel2), \""+GeoSPARQLCRSURI+"\")) OPTIONAL {?obj2 ?rel3 ?obj3 . FILTER(STRSTARTS(STR(?rel3), \""+GeoSPARQLCRSURI+"\"))}} FILTER(STRSTARTS(STR(?rel), \""+GeoSPARQLCRSURI+"\")) } ORDER BY ?rel ";
		System.out.println(prefixCollection+queryString);
		query = QueryFactory.create(prefixCollection+queryString);
		qexec = QueryExecutionFactory.create(query, model);
		res=qexec.execSelect();
		boolean datum=false,coordinateSystem=false;
		while(res.hasNext()) {
			QuerySolution sol=res.next();
			Iterator<String> vars=sol.varNames();
			if(sol.get("rel").toString().contains("datum")) {
				datum=true;
				coordinateSystem=false;
			}
			else if(sol.get("rel").toString().contains("coordinateSystem")) {
				datum=false;
				coordinateSystem=true;
			}else {
				datum=false;
				coordinateSystem=false;
			}
			if(datum) {
				
			}
			while(vars.hasNext()) {
				String curvar=vars.next();
				System.out.println(curvar+" "+sol.get(curvar));
			}
			
			//System.out.println(curCRSURI+" - "+sol.get("b").toString()+" - "+sol.get("c").toString());
		}
	}
}
