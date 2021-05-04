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

import proj4rdf.data.Axis;
import proj4rdf.data.CoordinateReferenceSystem;
import proj4rdf.data.CoordinateSystem;
import proj4rdf.data.Datum;
import proj4rdf.data.Ellipsoid;
import proj4rdf.data.PrimeMeridian;

public class RDFCRSToWKT {
	
	public static String prefixCollection="";
	
	public static String curCRSURI="http://www.opengis.net/def/crs/EPSG/0/4326";
	
	public static String GeoSPARQLCRSURI="http://www.opengis.net/ont/crs/";
	
	public static String downliftQuery="SELECT DISTINCT * WHERE { BIND(<"+curCRSURI+"> AS ?sub) ?sub ?rel ?obj . OPTIONAL {?obj ?rel2 ?obj2 . "
			+ "FILTER(STRSTARTS(STR(?rel2), \""+GeoSPARQLCRSURI+"\") || STRSTARTS(STR(?rel2), \"http://www.w3.org/2000/01/rdf-schema#\")) "
			+ "OPTIONAL {?obj2 ?rel3 ?obj3 . "
			+ "FILTER(STRSTARTS(STR(?rel3), \""+GeoSPARQLCRSURI+"\") || STRSTARTS(STR(?rel3), \"http://www.w3.org/2000/01/rdf-schema#\"))"
			+ "}} "
			+ "FILTER(STRSTARTS(STR(?rel), \""+GeoSPARQLCRSURI+"\") || STRSTARTS(STR(?rel), \"http://www.w3.org/2000/01/rdf-schema#\"))"
			+ " } ORDER BY ?rel ?rel2 ";
	
	//public static String downliftQuery="SELECT "
	
	static OntModel model;
	
	static {
		try {
			model=ModelFactory.createOntologyModel();
			model.read(new FileReader(new File("result.ttl")),"","TTL");
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
	
	
	public static String getCRSFromTripleStore(String crsURI, String endpointURL, String format, OntModel model) {
		String queryString=downliftQuery;
		System.out.println(prefixCollection+queryString);
		Query query = QueryFactory.create(prefixCollection+queryString);
		QueryExecution qexec = QueryExecutionFactory.create(query, model);
		ResultSet res=qexec.execSelect();
		CoordinateReferenceSystem refsys=downliftSytem(res);
		switch(format) {
			case "WKT": return refsys.toWKT();
			case "GML": return refsys.toGML().toString();
			case "ProjJSON": return refsys.toProjJSON().toString();
			case "Proj": return refsys.toProj();
			default: return refsys.toProjJSON().toString();
		}
	}
	
	public static String[] getEligibleCRSFromTripleStore(String bbox) {
		String queryString="SELECT DISTINCT ?crs WHERE { ?crs  <"+GeoSPARQLCRSURI+"datum> ?datum . ?datum ?datumrel ?datumobj .  } ";
		System.out.println(prefixCollection+queryString);
		Query query = QueryFactory.create(prefixCollection+queryString);
		QueryExecution qexec = QueryExecutionFactory.create(query, model);
		ResultSet res=qexec.execSelect();
		return null;		
	}
	
	public static CoordinateReferenceSystem downliftSytem(ResultSet res) {
		boolean datum=false,coordinateSystem=false,ellipse=false;
		CoordinateReferenceSystem refsys=new CoordinateReferenceSystem();
		refsys.datum=new Datum();
		refsys.datum.ellipsoid=new Ellipsoid();
		refsys.datum.primeMeridian=new PrimeMeridian();
		refsys.cSystem=new CoordinateSystem();
		String curraxis="";
		Axis curaxis=null;
		while(res.hasNext()) {
			QuerySolution sol=res.next();
			Iterator<String> vars=sol.varNames();
			if(sol.get("rel").toString().contains("datum") && !datum) {
				datum=true;
				coordinateSystem=false;
			}
			else if(sol.get("rel").toString().contains("coordinateSystem") && !coordinateSystem) {
				datum=false;
				coordinateSystem=true;
			}else {
				datum=false;
				coordinateSystem=false;
				if(sol.get("rel").toString().contains("scope")) {
					refsys.scope=sol.get("obj").toString();
				}
				if(sol.get("rel").toString().contains("label")) {
					refsys.crsName=sol.getLiteral("obj").getString();
				}
			}
			if(sol.get("rel").toString().contains("datum")) {
				if(sol.get("rel2").toString().contains("primeMeridian")) {
					if(sol.get("rel3").toString().contains("unit")) {
						refsys.datum.primeMeridian.angleunit=sol.get("obj3").toString().substring(sol.get("obj3").toString().lastIndexOf('/')+1).replace("om:","");
					}
					if(sol.get("rel3").toString().contains("longitude")) {
						refsys.datum.primeMeridian.longitude=sol.getLiteral("obj3").getDouble();
					}
					if(sol.get("rel3").toString().contains("label")) {
						refsys.datum.primeMeridian.primeMeridianName=sol.getLiteral("obj3").getString();
					}
				}
				if(sol.get("rel2").toString().contains("ellipse") && !ellipse) {
					if(sol.get("rel3").toString().contains("label")) {
						refsys.datum.ellipsoid.ellipsoidName=sol.getLiteral("obj3").getString();
					}
					if(sol.get("rel3").toString().contains("inverse_flattening")) {
						refsys.datum.ellipsoid.inverseFlattening=sol.getLiteral("obj3").getDouble();
					}
					if(sol.get("rel3").toString().contains("semiMajorAxis")) {
						refsys.datum.ellipsoid.semiMajorAxis=sol.getLiteral("obj3").getDouble();
					}
					if(sol.get("rel3").toString().contains("semiMinorAxis")) {
						refsys.datum.ellipsoid.semiMinorAxis=sol.getLiteral("obj3").getDouble();
					}
					if(sol.get("rel3").toString().contains("eccentricity")) {
						refsys.datum.ellipsoid.eccentricity=sol.getLiteral("obj3").getDouble();
					}
					if(sol.get("rel3").toString().contains("flatteningParameter")) {
						refsys.datum.ellipsoid.flatteningParameter=sol.getLiteral("obj3").getDouble();
					}
				}else if(sol.get("rel2").toString().contains("label")) {
					refsys.datum.datumName=sol.getLiteral("obj2").getString();
				}
			}
			if(sol.get("rel").toString().contains("coordinateSystem")) {
				if(sol.get("rel2").toString().contains("label")) {
					System.out.println("Label: "+sol.get("obj2").toString());
					refsys.cSystem.coordinateSystemType=sol.get("obj2").toString();
				}
				if(sol.get("rel2").toString().contains("axis")) {
					String curaxis_string=sol.get("obj2").toString();
					System.out.println(curaxis_string+" - "+curraxis);
					if(!curraxis.equals(curaxis_string)) {
						curaxis=new Axis();
						refsys.cSystem.axisList.add(curaxis);
						curraxis=curaxis_string;
						curaxis.axisorder=refsys.cSystem.axisList.size()-1;
					}
					if(sol.get("rel3").toString().contains("label")) {
						curaxis.axisname=sol.getLiteral("obj3").getString().substring(sol.getLiteral("obj3").getString().lastIndexOf('/')+1);
					}
					if(sol.get("rel3").toString().contains("direction")) {
						curaxis.axisdirection=sol.get("obj3").toString().substring(sol.get("obj3").toString().lastIndexOf('/')+1);
					}
					if(sol.get("rel3").toString().contains("abbreviation")) {
						curaxis.axisabbreviation=sol.get("obj3").toString();
					}
					if(sol.get("rel3").toString().contains("unit_conversion_factor")) {
						curaxis.unitconversionfactor=sol.getLiteral("obj3").getDouble();
					}
					if(sol.get("rel3").toString().endsWith("unit")) {
						curaxis.angleunit=sol.get("obj3").toString().substring(sol.get("obj3").toString().lastIndexOf('/')+1);
					}
				}
			}
		}
		refsys.cSystem.numberDimensions=refsys.cSystem.axisList.size();
		return refsys;
	}
	
	public static void main(String[] args) throws IOException {
		String queryString="SELECT DISTINCT * WHERE { <"+curCRSURI+"> <"+GeoSPARQLCRSURI+"datum> ?datum . ?datum ?datumrel ?datumobj .  } ";
		System.out.println(prefixCollection+queryString);
		Query query = QueryFactory.create(prefixCollection+queryString);
		QueryExecution qexec = QueryExecutionFactory.create(query, model);
		ResultSet res=qexec.execSelect();
		queryString=downliftQuery;
		System.out.println(prefixCollection+queryString);
		query = QueryFactory.create(prefixCollection+queryString);
		qexec = QueryExecutionFactory.create(query, model);
		res=qexec.execSelect();
		FileWriter writer=new FileWriter(new File("queryresult.txt"));
		writer.write(ResultSetFormatter.asText(res));
		writer.close();
		queryString=downliftQuery;
		System.out.println(prefixCollection+queryString);
		query = QueryFactory.create(prefixCollection+queryString);
		qexec = QueryExecutionFactory.create(query, model);
		res=qexec.execSelect();
		CoordinateReferenceSystem refsys=downliftSytem(res);
		System.out.println(refsys);
		System.out.println(refsys.toWKT());
		System.out.println(refsys.toProjJSON());
}
	
//{'$schema':'https://proj.org/schemas/v0.2/projjson.schema.json','type':'GeographicCRS','name':'WGS 84','datum':{'type':'GeodeticReferenceFrame','name':'World Geodetic System 1984','ellipsoid':{'name':'WGS 84','semi_major_axis':6378137,'inverse_flattening':298.257223563}},'coordinate_system':{'subtype':'ellipsoidal','axis':[{'name':'Geodetic latitude','abbreviation':'Lat','direction':'north','unit':'degree'},{'name':'Geodetic longitude','abbreviation':'Lon','direction':'east','unit':'degree'}]},'scope':'Horizontal component of 3D system.','area':'World.','bbox':{'south_latitude':-90,'west_longitude':-180,'north_latitude':90,'east_longitude':180},'id':{'authority':'EPSG','code':4326}}	
}
