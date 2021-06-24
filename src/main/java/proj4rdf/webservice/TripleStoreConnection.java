package proj4rdf.webservice;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

import org.apache.jena.ontology.OntModel;
import org.apache.jena.query.Query;
import org.apache.jena.query.QueryExecution;
import org.apache.jena.query.QueryExecutionFactory;
import org.apache.jena.query.QueryFactory;
import org.apache.jena.query.QuerySolution;
import org.apache.jena.query.ResultSet;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.sparql.expr.NodeValue;
import org.json.JSONArray;
import org.json.JSONObject;

import io.github.galbiston.geosparql_jena.configuration.GeoSPARQLConfig;
import proj4rdf.CRSConfig;

public class TripleStoreConnection {

	public static final TripleStoreConnection INSTANCE = new TripleStoreConnection();

	public static final String prefixCollection = "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>"
			+ System.lineSeparator() + "PREFIX geo: <http://www.opengis.net/ont/geosparql#>"
					+ System.lineSeparator() + "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
					+ System.lineSeparator() + "PREFIX geo2: <http://www.opengis.net/ont/geosparqlplus#>";

	public final Map<String, OntModel> modelmap;

	public static Integer resultSetSize = 0;

	public TripleStoreConnection() {
		GeoSPARQLConfig.setupMemoryIndex();
		CRSConfig.setup();
		modelmap = new TreeMap<String, OntModel>();
		modelmap.put("proj4.ttl", ModelFactory.createOntologyModel());
		//modelmap.put("owl/proj4rdf_data.ttl", ModelFactory.createOntologyModel());
		/*modelmap.put("linkedgeodata.ttl", ModelFactory.createOntologyModel());
		modelmap.put("cologne.ttl", ModelFactory.createOntologyModel());
		modelmap.put("gag.ttl", ModelFactory.createOntologyModel());
		modelmap.put("geonames.ttl", ModelFactory.createOntologyModel());
		modelmap.put("hotspots.ttl", ModelFactory.createOntologyModel());
		modelmap.put("synthetic.ttl", ModelFactory.createOntologyModel());
		modelmap.put("rasterexample.ttl", ModelFactory.createOntologyModel());*/
		// modelmap.put("testdata3.ttl", ModelFactory.createOntologyModel());
		// modelmap.put("testdata4.ttl", ModelFactory.createOntologyModel());
		try {
			modelmap.get("proj4.ttl").read(new FileInputStream("ontology.ttl"), null, "TTL");

		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		try {
			modelmap.get("proj4.ttl").read(new FileInputStream("proj4.ttl"), null, "TTL");
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		

		/*
		for (String mod : modelmap.keySet()) {
			try {

			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}*/
	}

	public static String executeQuery(String query, String model) {
		return executeQuery(query, model, false);
	}
	
	public static String executeQueryTripleStore(String query, String uri) {
		return executeQuery(query, uri, false);
	}

	public static String executeQuery(String query, String model, Boolean geojsonout) {
		query = prefixCollection + query;
		System.out.println(query);
		System.out.println(model);
		System.out.println(INSTANCE.modelmap.keySet());
		QueryExecution qe=null;
		if(model.startsWith("http")) {
			Query queryjena = QueryFactory.create(query);
			//"http://localhost:8080/rdf4j-server/repositories/pleiades"
			qe = QueryExecutionFactory.sparqlService(model, queryjena);
		}else {
			if (!INSTANCE.modelmap.containsKey(model)) {
				model = INSTANCE.modelmap.keySet().iterator().next();
			}
			System.out.println(INSTANCE.modelmap.get(model));
			qe = QueryExecutionFactory.create(query, INSTANCE.modelmap.get(model));
		}

			ResultSet rs = qe.execSelect();
			//List<QuerySolution> test = ResultSetFormatter.toList(rs);
			//qe.close();
			JSONArray geojsonresults = new JSONArray();
			List<JSONArray> allfeatures = new LinkedList<JSONArray>();
			JSONObject result = new JSONObject();
			JSONArray obj = new JSONArray();
			Boolean first = true;
			String geomvarname="";
			String relationName = "";
			Integer counter=0;
			Boolean newobject=true;
			JSONObject jsonobj = new JSONObject();
			JSONObject properties = new JSONObject();
			List<JSONObject> geoms = new LinkedList<JSONObject>();
			String lastgeom="";
			int geomvars=0;
			while (rs.hasNext()) {
				QuerySolution solu=rs.next();
				if(!first) {
					if(!geomvarname.isEmpty() && solu.get(geomvarname)!=null && solu.get(geomvarname).toString().equals(lastgeom)) {
						newobject=false;
					}else {
						newobject=true;
					}
					if(newobject) {
						//System.out.println("Geomvars: "+geomvars);
						int geomcounter = 0;
						for (JSONObject geom : geoms) {
							JSONObject geojsonobj = new JSONObject();
							geojsonobj.put("type", "Feature");
							geojsonobj.put("properties", properties);
							geojsonobj.put("geometry", geom);
							allfeatures.get(geomcounter % geomvars).put(geojsonobj);
							geomcounter++;
						}
					}
				}
				if(newobject) {
					geomvars = 0;
					jsonobj = new JSONObject();
					properties = new JSONObject();
					geoms = new LinkedList<JSONObject>();
				}
				//System.out.println(counter);
				Iterator<String> varnames = solu.varNames();
				while (varnames.hasNext()) {

					String name = varnames.next();
					if(newobject) {
					if (name.endsWith("_geom")) {
						geomvars++;
						geomvarname=name;
						if (first) {
							JSONObject geojsonresult = new JSONObject();
							geojsonresult.put("type", "FeatureCollection");
							geojsonresult.put("name", name);
							JSONArray features = new JSONArray();
							allfeatures.add(features);
							geojsonresults.put(geojsonresult);
							geojsonresults.getJSONObject(geojsonresults.length() - 1).put("features", features);
						}
						AsGeoJSON geojson = new AsGeoJSON();
						lastgeom=solu.get(name).toString();
						try {
							NodeValue val = geojson.exec(NodeValue.makeNode(solu.getLiteral(name).getString(),
									solu.getLiteral(name).getDatatype()));
							JSONObject geomobj = new JSONObject(val.asNode().getLiteralValue().toString());
							geoms.add(geomobj);
						} catch (Exception e) {
							e.printStackTrace();
						}
						properties.put(name, solu.get(name));
					} 
					}else{
						properties.put(name, lastgeom);
					}
					if (name.endsWith("_rel")) {
						relationName = solu.get(name).toString();
					} else {
						if (!relationName.isEmpty()) {
							//System.out.println("Putting property: "+relationName+" - "+solu.get(name));
							properties.put(relationName, solu.get(name));
						} else {
							properties.put(name, solu.get(name));
						}
					}
					//System.out.println(relationName);
					//System.out.println(name);
					//System.out.println(solu.get(name));
					//if(!geojsonout) {
						jsonobj.put(name, solu.get(name));
						obj.put(jsonobj);
					//}
				}
				first = false;
			}
			qe.close();
			result.put("geojson", geojsonresults);
			result.put("data", obj);
			result.put("size", counter);
			resultSetSize=counter;
			System.out.println(resultSetSize);
			if (geojsonout) {
				return geojsonresults.toString();
			}
			return result.toString();
	}

	public static void main(String[] args) {
		String res = TripleStoreConnection.executeQuery(
				"SELECT ?a ?c WHERE { ?a ?b ?c . } LIMIT 1000",
				"proj4.ttl");
		// System.out.println(res[0]);
		System.out.println(res);
		/*System.out.println(
				"=====================================================================================================");
		res = TripleStoreConnection.executeQuery(
				"SELECT ?geom ?wkt WHERE { ?geom geo:asWKT ?wkt . FILTER(geo2:ST_Area(?wkt)>10) }", "testdata.ttl");
		// System.out.println(res[0]);
		System.out.println(res);
		res = TripleStoreConnection.executeQuery(
				"SELECT ?wkt2 WHERE { ?geom geo:asWKT ?wkt . BIND(geo2:ST_YMax(?wkt) AS ?wkt2). FILTER(geo2:ST_Area(?wkt)>10) } ",
				"testdata.ttl");
		System.out.println(res);
		System.out.println(res);*/
	}
}