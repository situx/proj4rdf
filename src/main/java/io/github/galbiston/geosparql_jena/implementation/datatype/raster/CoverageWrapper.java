
/*
 * Copyright 2018 the original author or authors.
 * See the notice.md file distributed with this work for additional
 * information regarding copyright ownership.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package io.github.galbiston.geosparql_jena.implementation.datatype.raster;

import io.github.galbiston.geosparql_jena.implementation.DimensionInfo;
import io.github.galbiston.geosparql_jena.implementation.GeometryReverse;
import io.github.galbiston.geosparql_jena.implementation.GeometryWrapper;
import io.github.galbiston.geosparql_jena.implementation.SRSInfo;
import io.github.galbiston.geosparql_jena.implementation.UnitsOfMeasure;
import io.github.galbiston.geosparql_jena.implementation.datatype.GeometryDatatype;
import io.github.galbiston.geosparql_jena.implementation.datatype.RasterDataType;
import io.github.galbiston.geosparql_jena.implementation.datatype.SpatialWrapper;
import io.github.galbiston.geosparql_jena.implementation.datatype.WKTDatatype;
import io.github.galbiston.geosparql_jena.implementation.great_circle.CoordinatePair;
import io.github.galbiston.geosparql_jena.implementation.great_circle.GreatCircleDistance;
import io.github.galbiston.geosparql_jena.implementation.index.GeometryLiteralIndex.GeometryIndex;
import io.github.galbiston.geosparql_jena.implementation.index.GeometryTransformIndex;
import io.github.galbiston.geosparql_jena.implementation.jts.CoordinateSequenceDimensions;
import io.github.galbiston.geosparql_jena.implementation.jts.CustomCoordinateSequence;
import io.github.galbiston.geosparql_jena.implementation.jts.CustomGeometryFactory;
import io.github.galbiston.geosparql_jena.implementation.registry.MathTransformRegistry;
import io.github.galbiston.geosparql_jena.implementation.registry.SRSRegistry;
import io.github.galbiston.geosparql_jena.implementation.registry.UnitsRegistry;
import io.github.galbiston.geosparql_jena.implementation.vocabulary.SRS_URI;
import io.github.galbiston.geosparql_jena.implementation.vocabulary.Unit_URI;
import java.io.Serializable;
import java.util.List;
import java.util.Objects;

import org.apache.jena.datatypes.DatatypeFormatException;
import org.apache.jena.graph.Node;
import org.apache.jena.rdf.model.Literal;
import org.apache.jena.rdf.model.ResourceFactory;
import org.apache.jena.sparql.expr.NodeValue;
import org.apache.sis.coverage.grid.GridCoverage;
import org.apache.sis.geometry.DirectPosition2D;
import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.Envelope;
import org.locationtech.jts.geom.Geometry;
import org.locationtech.jts.geom.GeometryCollection;
import org.locationtech.jts.geom.GeometryFactory;
import org.locationtech.jts.geom.IntersectionMatrix;
import org.locationtech.jts.geom.LineString;
import org.locationtech.jts.geom.LinearRing;
import org.locationtech.jts.geom.MultiLineString;
import org.locationtech.jts.geom.MultiPoint;
import org.locationtech.jts.geom.MultiPolygon;
import org.locationtech.jts.geom.Point;
import org.locationtech.jts.geom.Polygon;
import org.locationtech.jts.geom.prep.PreparedGeometry;
import org.locationtech.jts.geom.prep.PreparedGeometryFactory;
import org.locationtech.jts.geom.util.AffineTransformation;
import org.opengis.geometry.DirectPosition;
import org.opengis.geometry.MismatchedDimensionException;
import org.opengis.referencing.crs.CoordinateReferenceSystem;
import org.opengis.referencing.operation.MathTransform;
import org.opengis.referencing.operation.TransformException;
import org.opengis.util.FactoryException;

import de.hsmainz.cs.semgis.arqextension.util.Wrapper;

/**
 *
 *
 */
public class CoverageWrapper extends SpatialWrapper {

    private final DimensionInfo dimensionInfo;
    private final SRSInfo srsInfo;
    private final GridCoverage xyGeometry;
    private final GridCoverage parsingGeometry;
    private PreparedGeometry preparedGeometry;
    private Envelope envelope;
    private GridCoverage translateXYGeometry;
    private final String geometryDatatypeURI;
    private RasterDataType geometryDatatype;
    private String lexicalForm;
    private String utmURI = null;
    private Double latitude = null;

    /**
     *
     * @param coverage In X/Y or Y/X coordinate order of the SRS URI.
     * @param srsURI
     * @param geometryDatatypeURI
     * @param dimensionInfo
     */
    public CoverageWrapper(GridCoverage geometry, String srsURI, String geometryDatatypeURI, DimensionInfo dimensionInfo) {
        this(geometry, srsURI, geometryDatatypeURI, dimensionInfo, null);
    }
    
    /**
     *
     * @param geometry In X/Y or Y/X coordinate order of the SRS URI.
     * @param srsURI
     * @param geometryDatatypeURI
     * @param dimensionInfo
     * @param geometryLiteral
     */
    public CoverageWrapper(GridCoverage geometry,String srsURI, String geometryDatatypeURI, DimensionInfo dimensionInfo, String geometryLiteral) {
        this(geometry, geometry, srsURI.isEmpty() ? SRS_URI.DEFAULT_WKT_CRS84 : srsURI, geometryDatatypeURI, dimensionInfo, geometryLiteral);
    }

    private CoverageWrapper(GridCoverage parsingGeometry, GridCoverage xyGeometry, String srsURI, String geometryDatatypeURI, DimensionInfo dimensionInfo) {
        this(parsingGeometry, xyGeometry, srsURI, geometryDatatypeURI, dimensionInfo, null);
    }

    private CoverageWrapper(GridCoverage parsingGeometry, GridCoverage xyGeometry, String srsURI, String geometryDatatypeURI, DimensionInfo dimensionInfo, String lexicalForm) {

        this.parsingGeometry = parsingGeometry;
        this.xyGeometry = xyGeometry;
        this.preparedGeometry = null; //Initialised when required by spatial relations checkPreparedGeometry.
        this.envelope = null; //Initialised when required by getEnvelope().
        this.translateXYGeometry = null; //Initialised when required by translateGeometry().
        this.geometryDatatypeURI = geometryDatatypeURI;
        this.geometryDatatype = null; //Inilialised when required by getGeometryDatatype().

        if (srsURI.isEmpty()) {
            srsURI = SRS_URI.DEFAULT_WKT_CRS84;
        }

        this.srsInfo = SRSRegistry.getSRSInfo(srsURI);

        this.dimensionInfo = dimensionInfo;
        this.lexicalForm = lexicalForm; //If not Initialised then required by asLiteral() etc.
    }

    /**
     * Default to WGS84 geometry and XY coordinate dimensions.
     *
     * @param coverage In X/Y or Y/X coordinate order of WGS84.
     * @param geometryDatatypeURI
     */
    public CoverageWrapper(GridCoverage geometry, String geometryDatatypeURI) {
        this(geometry, "", geometryDatatypeURI, DimensionInfo.XY_POINT);
    }

    /**
     * Default to XY coordinate dimensions.
     *
     * @param geometry In X/Y or Y/X coordinate order of the SRS URI.
     * @param srsURI
     * @param geometryDatatypeURI
     */
    public CoverageWrapper(GridCoverage geometry, String srsURI, String geometryDatatypeURI) {
        this(geometry, srsURI, geometryDatatypeURI, DimensionInfo.XY_POINT);
    }

    transient private static final GeometryFactory GEOMETRY_FACTORY = CustomGeometryFactory.theInstance();

   /* /**
     * Empty geometry with specified parameters.
     *
     * @param srsURI
     * @param geometryDatatypeURI
<<<<<<< HEAD
     *
    public CoverageWrapper(String srsURI, String geometryDatatypeURI) {
        this(new CustomCoordinateSequence(DimensionInfo.XY_POINT.getDimensions()), geometryDatatypeURI, srsURI);
    }
*/

    
    /**
     * Copy GeometryWrapper.
     *
     * @param geometryWrapper
     */
    public CoverageWrapper(CoverageWrapper geometryWrapper) {

        this.xyGeometry = geometryWrapper.xyGeometry;
        this.parsingGeometry = geometryWrapper.parsingGeometry;
        this.preparedGeometry = geometryWrapper.preparedGeometry;
        this.envelope = geometryWrapper.envelope;
        this.translateXYGeometry = geometryWrapper.translateXYGeometry;
        this.utmURI = geometryWrapper.utmURI;
        this.latitude = geometryWrapper.latitude;
        this.geometryDatatypeURI = geometryWrapper.geometryDatatypeURI;
        this.geometryDatatype = geometryWrapper.geometryDatatype;

        this.srsInfo = geometryWrapper.srsInfo;
        this.dimensionInfo = geometryWrapper.dimensionInfo;
        this.lexicalForm = geometryWrapper.lexicalForm;
    }

    /**
     * Transforms, if necessary, the provided target GeometryWrapper according
     * to this GeometryWrapper SRS_URI.
     *
     * @param targetGeometryWrapper
     * @return GeometryWrapper after transformation.
     * @throws FactoryException
     * @throws MismatchedDimensionException
     * @throws TransformException
     */
    /*public CoverageWrapper checkTransformSRS(CoverageWrapper targetGeometryWrapper) throws FactoryException, MismatchedDimensionException, TransformException {

        CoverageWrapper transformedGeometryWrapper;
        String srsURI = srsInfo.getSrsURI();
        if (srsURI.equals(targetGeometryWrapper.srsInfo.getSrsURI())) {
            transformedGeometryWrapper = targetGeometryWrapper;
        } else {
            transformedGeometryWrapper = targetGeometryWrapper.transform(srsURI);
        }

        return transformedGeometryWrapper;
    }*/

    /**
     * Transform the GeometryWrapper into another spatial reference system.<br>
     *
     * @param srsURI
     * @return New GeometryWrapper after transformation, or this GeometryWrapper
     * if no transformation.
     * @throws MismatchedDimensionException
     * @throws TransformException
     * @throws FactoryException
     */
   /* public CoverageWrapper transform(String srsURI) throws MismatchedDimensionException, TransformException, FactoryException {
        return transform(srsURI, true);
    }*/

    /**
     * Transform the GeometryWrapper into another spatial reference system.<br>
     *
     * @param srsInfo
     * @return New GeometryWrapper after transformation, or this GeometryWrapper
     * if no transformation.
     * @throws MismatchedDimensionException
     * @throws TransformException
     * @throws FactoryException
     */
    /*public CoverageWrapper transform(SRSInfo srsInfo) throws MismatchedDimensionException, TransformException, FactoryException {
        return transform(srsInfo.getSrsURI(), true);
    }*/


    /**
     * Returns this geometry wrapper converted to the SRS_URI URI.
     *
     * @param srsURI
     * @return GeometryWrapper after conversion.
     * @throws FactoryException
     * @throws MismatchedDimensionException
     * @throws TransformException
     */
    /*public CoverageWrapper convertSRS(String srsURI) throws FactoryException, MismatchedDimensionException, TransformException {
        return transform(srsURI);
    }*/

    /**
     *
     * @return Coordinate/Spatial reference system of the GeometryWrapper.
     */
    public CoordinateReferenceSystem getCRS() {
        return srsInfo.getCrs();
    }



    /**
     *
     * @return Geometry with coordinates as originally provided.
     */
    public GridCoverage getParsingGeometry() {
        return parsingGeometry;
    }
    
    /**
    *
    * @return Geometry with coordinates as originally provided.
    */
   public GridCoverage getGridGeometry() {
       return parsingGeometry;
   }
   
   /**
   *
   * @return Geometry with coordinates as originally provided.
   */
  public GridCoverage getXYGeometry() {
      return parsingGeometry;
  }

   

    /**
     *
     * @return Coordinate/Spatial reference system URI.
     */
    public String getSrsURI() {
        return srsInfo.getSrsURI();
    }

    /**
     *
     * @return getSRID used in GeoSPARQL Standard page 22 to refer to srsURI.
     * i.e. getSrsURI and getSRID are the same.
     */
    public String getSRID() {
        return srsInfo.getSrsURI();
    }

    /**
     *
     * @return SRS information that the Geometry Wrapper is using.
     */
    public SRSInfo getSrsInfo() {
        return srsInfo;
    }

    /**
     *
     * @return Whether the SRS URI has been recognised. Operations may fail or
     * not perform correctly when false.
     */
    public Boolean isSRSRecognised() {
        return srsInfo.isSRSRecognised();
    }

    /**
     *
     * @return Datatype URI of the literal.
     */
    public String getRasterDatatypeURI() {
        return geometryDatatypeURI;
    }

   
    /**
     *
     * @return GeometryDatatype of the literal.
     */
    public RasterDataType getRasterDatatype() {

        if (geometryDatatype == null) {
            geometryDatatype = RasterDataType.get(geometryDatatypeURI);
        }
        return geometryDatatype;
    }

    

    /**
     *
     * @return GeometryWrapper as NodeValue
     */
    public NodeValue asNodeValue() throws DatatypeFormatException {
        Literal literal = asLiteral();
        return NodeValue.makeNode(literal.getLexicalForm(), literal.getDatatype());
    }

    /**
     *
     * @return GeometryWrapper as Node
     */
    public Node asNode() throws DatatypeFormatException {
        return asNodeValue().asNode();
    }

    /**
     *
     * @return GeometryWrapper as Literal
     */
    public Literal asLiteral() throws DatatypeFormatException {

        RasterDataType datatype = getRasterDatatype(); //Datatype is only retrieved when required.
        if (lexicalForm != null) {
            return ResourceFactory.createTypedLiteral(lexicalForm, datatype);
        }

        Literal literal = asLiteral(datatype);
        lexicalForm = literal.getLexicalForm();
        return literal;
    }

    /**
     *
     * @param outputGeometryDatatypeURI
     * @return GeometryWrapper as Literal in datatype form.
     */
    public Literal asLiteral(String outputGeometryDatatypeURI) throws DatatypeFormatException {
        RasterDataType datatype = RasterDataType.get(outputGeometryDatatypeURI);
        return asLiteral(datatype);
    }

    /**
     *
     * @param datatype
     * @return GeometryWrapper as Literal
     */
    public Literal asLiteral(RasterDataType datatype) {
        String tempLexicalForm = datatype.unparse(this);
        return ResourceFactory.createTypedLiteral(tempLexicalForm, datatype);
    }

    /**
     *
     * @return Coordinate dimension, i.e. 2 (x,y), 3 (x,y,z or x,y,m) or 4
     * (x,y,z,m)
     */
    public int getCoordinateDimension() {
        return dimensionInfo.getCoordinate();
    }

    /**
     *
     * @return Spatial dimension, i.e. 2 or 3
     */
    public int getSpatialDimension() {
        return dimensionInfo.getSpatial();
    }

    /**
     *
     * @return Topological dimension, i.e. 0, 1 or 2
     */
    public int getTopologicalDimension() {
        return dimensionInfo.getTopological();
    }

    /**
     *
     * @return Enum of coordinate dimensions.
     */
    public CoordinateSequenceDimensions getCoordinateSequenceDimensions() {
        return dimensionInfo.getDimensions();
    }

    /**
     *
     * @return Units of Measure for the GeometryWrapper SRS.
     */
    public UnitsOfMeasure getUnitsOfMeasure() {
        return srsInfo.getUnitsOfMeasure();
    }

    /**
     *
     * @return GeometryWrapper's coordinate, spatial and topological dimensions.
     */
    public DimensionInfo getDimensionInfo() {
        return dimensionInfo;
    }

    /**
     *
     * @return String literal of Geometry Wrapper.
     */
    public String getLexicalForm() {

        if (lexicalForm != null) {
            return lexicalForm;
        } else {
            Literal literal = asLiteral();
            return literal.getLexicalForm();
        }
    }


    /**
     * Extract Geometry Wrapper from Geometry Literal.
     *
     * @param geometryLiteral
     * @param targetIndex
     * @return Geometry Wrapper of the Geometry Literal.
     */
    public static final CoverageWrapper extract(NodeValue geometryLiteral, GeometryIndex targetIndex) {

        Node node = geometryLiteral.asNode();

        return extract(node, targetIndex);
    }

    /**
     * Extract Geometry Wrapper from Geometry Literal.
     *
     * @param geometryLiteral
     * @param targetIndex
     * @return Geometry Wrapper of the Geometry Literal.
     */
    public static final CoverageWrapper extract(Node geometryLiteral, GeometryIndex targetIndex) {

        if (!geometryLiteral.isLiteral()) {
            throw new DatatypeFormatException("Not a Literal: " + geometryLiteral);
        }

        String datatypeURI = geometryLiteral.getLiteralDatatypeURI();
        String lexicalForm = geometryLiteral.getLiteralLexicalForm();
        return extract(lexicalForm, datatypeURI, targetIndex);
    }

    /**
     * Extract Geometry Wrapper from Geometry Literal.
     *
     * @param geometryLiteral
     * @return Geometry Wrapper of the Geometry Literal.
     */
    public static final CoverageWrapper extract(NodeValue geometryLiteral) {
        return extract(geometryLiteral, GeometryIndex.PRIMARY);
    }

    /**
     * Extract Geometry Wrapper from Geometry Literal.
     *
     * @param geometryLiteral
     * @return Geometry Wrapper of the Geometry Literal.
     */
    public static final CoverageWrapper extract(Node geometryLiteral) {
        return extract(geometryLiteral, GeometryIndex.PRIMARY);
    }

    /**
     * Extract Geometry Wrapper from Geometry Literal. Returns null if invalid
     * literal provided.
     *
     * @param geometryLiteral
     * @param targetIndex
     * @return Geometry Wrapper of the Geometry Literal.
     */
    public static final CoverageWrapper extract(Literal geometryLiteral, GeometryIndex targetIndex) {
        return extract(geometryLiteral.getLexicalForm(), geometryLiteral.getDatatypeURI(), targetIndex);
    }

    /**
     * Extract Geometry Wrapper from Geometry Literal.
     *
     * @param geometryLiteral
     * @return Geometry Wrapper of the Geometry Literal.
     */
    public static final CoverageWrapper extract(Literal geometryLiteral) {
        return extract(geometryLiteral, GeometryIndex.PRIMARY);
    }

    /**
     * Extract Geometry Wrapper from Geometry Literal.
     *
     * @param lexicalForm
     * @param datatypeURI
     * @return Geometry Wrapper of the Geometry Literal.
     */
    public static CoverageWrapper extract(String lexicalForm, String datatypeURI) {
        return extract(lexicalForm, datatypeURI, GeometryIndex.PRIMARY);
    }

    /**
     * Extract Geometry Wrapper from Geometry Literal.
     *
     * @param lexicalForm
     * @param datatypeURI
     * @param targetIndex
     * @return Geometry Wrapper of the Geometry Literal.
     */
    public static CoverageWrapper extract(String lexicalForm, String datatypeURI, GeometryIndex targetIndex) {

        if (lexicalForm == null || datatypeURI == null) {
            throw new DatatypeFormatException("GeometryWrapper extraction: arguments cannot be null - " + lexicalForm + ", " + datatypeURI);
        }

        RasterDataType datatype = RasterDataType.get(datatypeURI);
        CoverageWrapper geometry = datatype.parse(lexicalForm, targetIndex);
        return geometry;
    }

    /**
     *
     * @return Empty GeometryWrapper in WKT datatype.
     */
    public static final GeometryWrapper getEmptyWKT() {
        return WKTDatatype.INSTANCE.read("");
    }



         /**
     * Create Geometry GeometryWrapper.
     *
     * @param coverage In X/Y order.
     * @param srsURI
     * @param geometryDatatypeURI
     * @return GeometryWrapper with SRS URI and GeometryDatatype URI.
     */
    public static final CoverageWrapper createCoverage(GridCoverage geometry, String srsURI, String geometryDatatypeURI) {
        GridCoverage xyGeometry = geometry;
        //GridCoverage parsingGeometry = GeometryReverse.check(xyGeometry, srsURI);
        DimensionInfo dimsInfo = DimensionInfo.XY_POINT;

        return new CoverageWrapper(xyGeometry, xyGeometry, srsURI, geometryDatatypeURI, dimsInfo);
    }



    
    @Override
    public int hashCode() {
        int hash = 3;
        hash = 23 * hash + Objects.hashCode(this.dimensionInfo);
        hash = 23 * hash + Objects.hashCode(this.srsInfo);
        hash = 23 * hash + Objects.hashCode(this.xyGeometry);
        hash = 23 * hash + Objects.hashCode(this.geometryDatatypeURI);
        return hash;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null) {
            return false;
        }
        if (getClass() != obj.getClass()) {
            return false;
        }
        final CoverageWrapper other = (CoverageWrapper) obj;
        if (!Objects.equals(this.geometryDatatypeURI, other.geometryDatatypeURI)) {
            return false;
        }
        if (!Objects.equals(this.dimensionInfo, other.dimensionInfo)) {
            return false;
        }
        if (!Objects.equals(this.srsInfo, other.srsInfo)) {
            return false;
        }
        return Objects.equals(this.xyGeometry, other.xyGeometry);
    }

    @Override
    public String toString() {
        return "GeometryWrapper{" + "dimensionInfo=" + dimensionInfo + ", geometryDatatypeURI=" + geometryDatatypeURI + ", lexicalForm=" + lexicalForm + ", utmURI=" + utmURI + ", latitude=" + latitude + ", xyGeometry=" + xyGeometry + ", parsingGeometry=" + parsingGeometry + ", preparedGeometry=" + preparedGeometry + ", srsInfo=" + srsInfo + '}';
    }



}
