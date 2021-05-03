package proj4rdf.webservice;

import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.StringWriter;
import java.io.BufferedWriter;
import java.io.Writer;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

import javax.ws.rs.Consumes;
import javax.ws.rs.DefaultValue;
import javax.ws.rs.GET;
import javax.ws.rs.NotFoundException;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.PathParam;
import javax.ws.rs.QueryParam;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.HttpHeaders;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.StreamingOutput;
import javax.xml.stream.XMLOutputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;

import com.sun.xml.txw2.output.IndentingXMLStreamWriter;

import org.apache.http.HttpEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.enums.ParameterStyle;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.info.License;
import proj4rdf.RDFCRSToWKT;


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
	@Produces({ MediaType.APPLICATION_JSON })
	@Path("/crsFromRDF")
	@Operation(
            summary = "Returns a CRS definition given in a RDF graph in a predefined format",
            description = "Returns a CRS definition given in a RDF graph in a predefined format")
	public Response getCRSByURI(
			@Parameter(description="The URI of the CRS defined in RDF") @PathParam("crsuri") String crsuri,
			@Parameter(description="The endpoint of the CRS definition") @PathParam("endpoint") String crsendpoint,
			@Parameter(description="The return format")@PathParam("returnformat") String returnformat) {
		
		return null;
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

}
