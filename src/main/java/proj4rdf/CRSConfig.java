package proj4rdf;



import org.apache.jena.sparql.function.FunctionRegistry;

import proj4rdf.functions.srs.AreaOfValidity;
import proj4rdf.functions.srs.ConvertCRS;
import proj4rdf.functions.srs.HasHorizontalCRS;
import proj4rdf.functions.srs.IsEligibleConversion;
import proj4rdf.functions.srs.IsInCRSAreaOfValidity;
import proj4rdf.functions.srs.SRIDGetAxis1Name;
import proj4rdf.functions.srs.SRIDGetAxis1Orientation;
import proj4rdf.functions.srs.SRIDGetAxis2Name;
import proj4rdf.functions.srs.SRIDGetAxis2Orientation;
import proj4rdf.functions.srs.SRIDHasFlippedAxis;
import proj4rdf.functions.srs.SRIDToEPSG;
import proj4rdf.functions.srs.SRIDToGML;
import proj4rdf.functions.srs.SRIDToWKT;
import proj4rdf.functions.srs.SRSURIToGML;
import proj4rdf.functions.srs.SRSURIToWKT;
import proj4rdf.functions.srs.SetGeoReference;
import proj4rdf.functions.srs.SuggestProjection;
import proj4rdf.vocabulary.CRSGeo;


public class CRSConfig {

    private static Boolean IS_FUNCTIONS_REGISTERED = false;

    public static final void setup() {

        //Only register functions once.
        if (!IS_FUNCTIONS_REGISTERED) {
            FunctionRegistry functionRegistry = FunctionRegistry.get();

            //POSTGIS functionRegistry
            functionRegistry.put(CRSGeo.st_srsAreaOfValidity.getURI(), AreaOfValidity.class);
            functionRegistry.put(CRSGeo.st_epsgToWKT.getURI(), SRIDToEPSG.class);
            functionRegistry.put(CRSGeo.st_sridGetAxis1Name.getURI(), SRIDGetAxis1Name.class);
            functionRegistry.put(CRSGeo.st_sridGetAxis1Orientation.getURI(), SRIDGetAxis1Orientation.class);
            functionRegistry.put(CRSGeo.st_sridGetAxis2Name.getURI(), SRIDGetAxis2Name.class);
            functionRegistry.put(CRSGeo.st_sridGetAxis2Orientation.getURI(), SRIDGetAxis2Orientation.class);
            functionRegistry.put(CRSGeo.st_sridHasFlippedAxis.getURI(), SRIDHasFlippedAxis.class);
            functionRegistry.put(CRSGeo.st_sridToEPSG.getURI(), SRIDToEPSG.class);
            functionRegistry.put(CRSGeo.st_isInSRSAreaOfValidity.getURI(), IsInCRSAreaOfValidity.class);
            functionRegistry.put(CRSGeo.st_isEligibleConversion.getURI(), IsEligibleConversion.class);
            functionRegistry.put(CRSGeo.st_hasHorizontalCRS.getURI(), HasHorizontalCRS.class);
            functionRegistry.put(CRSGeo.st_setGeoReference.getURI(), SetGeoReference.class);
            functionRegistry.put(CRSGeo.st_suggestProjection.getURI(), SuggestProjection.class);
            functionRegistry.put(CRSGeo.st_sridToWKT.getURI(), SRIDToWKT.class);
            functionRegistry.put(CRSGeo.st_sridToGML.getURI(), SRIDToGML.class);
            functionRegistry.put(CRSGeo.st_srsURIToWKT.getURI(), SRSURIToWKT.class);
            functionRegistry.put(CRSGeo.st_srsURIToGML.getURI(), SRSURIToGML.class);
            functionRegistry.put(CRSGeo.st_transform.getURI(), ConvertCRS.class);
            // extra utility functionRegistry
            System.out.println(functionRegistry);
            GeoSPARQLConfig.setupMemoryIndex();
            IS_FUNCTIONS_REGISTERED = true;
        }
    }
    public static void main(String[] args) {
    	setup();
    }
}