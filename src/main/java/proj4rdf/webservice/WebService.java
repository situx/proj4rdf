package proj4rdf.webservice;

import java.io.IOException;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.PathParam;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.xml.stream.XMLStreamWriter;


import org.apache.http.HttpEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.json.JSONObject;
import org.opengis.util.FactoryException;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.info.License;
import proj4rdf.RDFCRSToWKT;
import proj4rdf.data.CoordinateReferenceSystem;


/**
 * Implements OGC API Features and WFS webservice functionality.
 *
 */
@OpenAPIDefinition(
		 info = @Info(
				    title = "Proj4RDF API",
				    version = "1.0",
				    description = "This web service provides conversions between coordinate reference systems defined in RDF",
				    contact = @Contact(
				      name = "Anonymous User",
				      email = "email@example.com"
				    ),
				    license = @License(
				      url = "https://www.govdata.de/dl-de/by-2-0",
				      name = "Datenlizenz Deutschland"
				    )
				  ),
				  security = {}
)
@Path("/")
public class WebService {

	public static JSONObject triplestoreconf = null;

	public static JSONObject wfsconf = null;
	
	public static final MediaType openapijson=new MediaType("application", "vnd.oai.openapi+json;version=3.0");

	public static long milliesInDays = 24 * 60 * 60 * 1000;

	public XMLStreamWriter xmlwriter;

	String htmlHead;

	/**
	 * Constructor for this class.
	 * Loads configuration files and performs initializations.
	 * @throws IOException on error
	 */
	public WebService() throws IOException {

	}
				
	@GET
	@Produces({"application/vnd.oai.openapi+json;version=3.0"})
	@Path("/openapi3")
	public Response openapiJSON() {
		System.out.println("OpenAPI JSON");
		CloseableHttpClient httpClient = HttpClients.createDefault();
		HttpGet request = new HttpGet(wfsconf.get("baseurl")+"/openapi.json");
		CloseableHttpResponse response;
		try {
			response = httpClient.execute(request);
			HttpEntity entity = response.getEntity();
			String result = EntityUtils.toString(entity);
			System.out.println(result);
			response.close();
			httpClient.close();
			Response res=Response.status(Response.Status.OK).entity(result).build();//.type(OpenAPIMediaType.OA3_TYPE).build();
			return res;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;//Response.ok("",OpenAPIMediaType.OA3_TYPE).build();
		}
	}
	
	@GET
	@Produces(MediaType.TEXT_PLAIN)
	@Path("/queryservice")
    public String queryService(@QueryParam("query") String query,@QueryParam("dataset") String dataset) { 
		final String dir = System.getProperty("user.dir");
        System.out.println("current dir = " + dir); 
		return TripleStoreConnection.executeQuery(query,dataset);
	}
	
	@GET
	@Produces(MediaType.TEXT_PLAIN)
	@Path("/queryservicegeojson")
    public String queryService(@QueryParam("query") String query,@QueryParam("dataset") String dataset,@QueryParam("geojson") String geojson) { 
		final String dir = System.getProperty("user.dir");
        System.out.println("current dir = " + dir); 
		return TripleStoreConnection.executeQuery(query,dataset,true);
	}
	
	@GET
	@Produces({ MediaType.APPLICATION_JSON })
	@Path("/crsFromRDF")
	@Operation(
            summary = "Returns a CRS definition given in a RDF graph in a predefined format",
            description = "Returns a CRS definition given in a RDF graph in a predefined format")
	public Response getCRSByURI(
			@Parameter(description="The URI of the CRS defined in RDF") @PathParam("crsuri") String crsuri,
			@Parameter(description="The endpoint of the CRS definition") @PathParam("endpoint") String crsendpoint,
			@Parameter(description="The return format")@PathParam("returnformat") String returnformat) {
		return Response.ok(RDFCRSToWKT.getCRSFromTripleStore(crsuri, crsendpoint, returnformat)).build();
	}
	
	@GET
	@Produces({ MediaType.APPLICATION_JSON })
	@Path("/getEligibleCRSForFeature")
	@Operation(
            summary = "Returns a CRS definition given in a RDF graph in a predefined format",
            description = "Returns a CRS definition given in a RDF graph in a predefined format")
	public Response getEligibleCRS(
			@Parameter(description="The URI of the CRS defined in RDF") @PathParam("crsuri") String crsuri,
			@Parameter(description="The endpoint of the CRS definition") @PathParam("endpoint") String crsendpoint,
			@Parameter(description="boundingbox to check the area of validity") @PathParam("bbox") String bbox,
			@Parameter(description="The return format")@PathParam("returnformat") String returnformat) {
		return Response.ok(RDFCRSToWKT.getEligibleCRSFromTripleStore(bbox)).build();
		//return getFeatureById(collectionid, featureid, style, format);
	}
	
	@GET
	@Produces({ MediaType.APPLICATION_JSON })
	@Path("/convertCRS")
	@Operation(
            summary = "Converts a feature defined in a given CRS to another CRS.",
            description = "Converts a feature defined in a given CRS to another CRS.")
	public Response convertFeaturetoCRSDefinedinRDF(
			@Parameter(description="The URI of the CRS defined in RDF") @PathParam("crsuri") String crsuri,
			@Parameter(description="The endpoint of the CRS definition") @PathParam("endpoint") String crsendpoint,
			@Parameter(description="The return format")@PathParam("returnformat") String returnformat) {
		return null;
	}
	
	@GET
	@Produces({ MediaType.TEXT_PLAIN })
	@Path("/wkt2RDF")
	@Operation(
            summary = "Converts a WKT CRS definition to RDF.",
            description = "Converts a WKT CRS definition to RDF.")
	public Response convertFeaturetoCRSDefinedinRDF(
			@Parameter(description="The WKT String to convert") @PathParam("wktstring") String wktstring) {
		try {
			return Response.ok(CoordinateReferenceSystem.WKTToRDF(wktstring)).build();
		} catch (FactoryException | IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return Response.ok("").build();
	}


}
