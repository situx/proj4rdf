package de.hsmainz.cs.semgis.arqextension.util;

import java.awt.Rectangle;
import java.awt.image.DataBuffer;
import java.awt.image.RenderedImage;
import java.awt.image.WritableRaster;
import java.awt.image.renderable.ParameterBlock;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

import javax.media.j3d.BoundingBox;
import javax.media.jai.JAI;
import javax.media.jai.RasterFactory;
import javax.media.jai.RenderedOp;

import org.apache.jena.sparql.expr.NodeValue;
import org.apache.sis.coverage.Category;
import org.apache.sis.coverage.SampleDimension;
import org.apache.sis.coverage.grid.GridCoverage;
import org.apache.sis.coverage.grid.GridExtent;
import org.apache.sis.coverage.grid.GridGeometry;
import org.apache.sis.geometry.DirectPosition2D;
import org.apache.sis.geometry.Envelope2D;
import org.apache.sis.internal.coverage.BufferedGridCoverage;
import org.apache.sis.referencing.CRS;
import org.apache.sis.referencing.CommonCRS;
import org.apache.sis.util.iso.DefaultNameFactory;
import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.Envelope;
import org.locationtech.jts.geom.Geometry;
import org.locationtech.jts.geom.GeometryFactory;
import org.locationtech.jts.geom.LineString;
import org.locationtech.jts.geom.OctagonalEnvelope;
import org.locationtech.jts.geom.Polygon;
import org.opengis.geometry.DirectPosition;
import org.opengis.geometry.MismatchedDimensionException;
import org.opengis.referencing.crs.CoordinateReferenceSystem;
import org.opengis.referencing.datum.PixelInCell;
import org.opengis.referencing.operation.MathTransform;
import org.opengis.referencing.operation.NoninvertibleTransformException;
import org.opengis.referencing.operation.TransformException;
import org.opengis.util.FactoryException;

import org.locationtech.jts.geom.Point;

import io.github.galbiston.geosparql_jena.implementation.GeometryWrapper;
import io.github.galbiston.geosparql_jena.implementation.GeometryWrapperFactory;
import io.github.galbiston.geosparql_jena.implementation.datatype.GeometryDatatype;
import io.github.galbiston.geosparql_jena.implementation.datatype.RasterDataType;
import io.github.galbiston.geosparql_jena.implementation.datatype.geometry.HexWKBDatatype;
import io.github.galbiston.geosparql_jena.implementation.datatype.raster.CoverageWrapper;

public class LiteralUtils {

	public static Wrapper rasterOrVector(NodeValue v) {
		GeometryDatatype datatype=null;
		try {
			datatype=GeometryDatatype.get(v.getDatatypeURI());
		}catch(Exception e) {
			datatype=null;
		}
			if(datatype==null) {
				RasterDataType rdatatype=RasterDataType.get(v.getDatatypeURI());
				if(rdatatype==null) {
					throw new AssertionError("No valid raster or vector geometry definition given!");
				}else {
					return CoverageWrapper.extract(v);	
				}	
			}else{
				return  GeometryWrapper.extract(v);
			}	
	}
	
	
	public static Double maxRasterValue(GridCoverage raster,Integer bandnum) {
		RenderedImage rendered=raster.render(null);
		Double maxVal=Double.MIN_VALUE;
    	for(int i=0;i<rendered.getSampleModel().getWidth();i++) {
    		for(int j=0;j<rendered.getSampleModel().getHeight();j++) {
    			if(rendered.getData().getSample(i, j, bandnum)>maxVal) {
    				maxVal=(double) rendered.getData().getSample(i, j, bandnum);
    			}
    		}
    	}
    	System.out.println("MaxRasterVal: "+maxVal);
    	return maxVal;
	}

	public static Double arithmeticMeanRasterValue(GridCoverage raster, Integer bandnum) {
		RenderedImage rendered=raster.render(null);
		Double sum=0.,counter=0.;
        for(int i=0;i<rendered.getSampleModel().getWidth();i++) {
        	for(int j=0;j<rendered.getSampleModel().getHeight();j++) {
        		sum+=(double) rendered.getData().getSample(i, j, bandnum);
        		counter++;
        	}
        }
    	System.out.println("MeanRasterVal: "+(sum/counter));
		return (sum/counter);
	}

	public static Double minRasterValue(GridCoverage raster, Integer bandnum) {
		RenderedImage rendered=raster.render(null);
		Double maxVal=Double.MAX_VALUE;
        	for(int i=0;i<rendered.getSampleModel().getWidth();i++) {
        		for(int j=0;j<rendered.getSampleModel().getHeight();j++) {
        			if(rendered.getData().getSample(i, j, bandnum)<maxVal) {
        				maxVal=(double) rendered.getData().getSample(i, j, bandnum);
        			}
        		}
        	}
        System.out.println("MinRasterVal: "+maxVal);
		return maxVal;
	}
	
	
	public static Boolean containsRasterValue(GridCoverage raster, Integer bandnum, Double value) {
		RenderedImage rendered=raster.render(null);
        	for(int i=0;i<rendered.getSampleModel().getWidth();i++) {
        		for(int j=0;j<rendered.getSampleModel().getHeight();j++) {
        			if(rendered.getData().getSample(i, j, bandnum)==value) {
        				return true;
        			}
        		}
        	}
		return false;
	}
	
	public static Coordinate worldToRaster(GridCoverage raster, Double latitude, Double longitude) throws MismatchedDimensionException, TransformException {    	
    	 GridGeometry gg2D = raster.getGridGeometry();
         MathTransform gridToCRS = gg2D.getGridToCRS(PixelInCell.CELL_CENTER);
         MathTransform crsToGrid = gridToCRS.inverse();
         DirectPosition realPos=new DirectPosition2D(latitude, longitude);
         DirectPosition gridPos = new DirectPosition2D();
         DirectPosition res=crsToGrid.transform(realPos, gridPos);
         Coordinate coord=new Coordinate(res.getCoordinate()[0],res.getCoordinate()[1]);
         return coord;
	}
	
	public static Coordinate worldToRaster(CoverageWrapper wrapper, Double latitude, Double longitude) throws MismatchedDimensionException, TransformException {
    	 GridCoverage raster=wrapper.getXYGeometry();      	
    	 GridGeometry gg2D = raster.getGridGeometry();
         MathTransform gridToCRS = gg2D.getGridToCRS(PixelInCell.CELL_CENTER);
         MathTransform crsToGrid = gridToCRS.inverse();
         DirectPosition realPos=new DirectPosition2D(latitude, longitude);
         DirectPosition gridPos = new DirectPosition2D();
         DirectPosition res=crsToGrid.transform(realPos, gridPos);
         Coordinate coord=new Coordinate(res.getCoordinate()[0],res.getCoordinate()[1]);
         return coord;
	}
	
	public static GridCoverage cropRaster2(GridCoverage raster,Double width, Double height, Double x, Double y) throws MismatchedDimensionException, TransformException {
		 Coordinate coord=worldToRaster(raster, x, y);
		 Coordinate coord2=worldToRaster(raster, x+width, y+height);
		 Double xx=coord.getX();
		 Double yy=coord.getY();
		 xx=Double.valueOf(xx.intValue())-1;
		 yy=Double.valueOf(yy.intValue())-1;
		 Double widthh=coord2.getX()-x;
		 Double heightt=coord2.getY()-y;	
		 if(widthh==0)
			 widthh=1.;
		 if(heightt==0)
			 heightt=1.;
	     RenderedImage rendered = raster.render(null);
		 ParameterBlock pbSubtracted = new ParameterBlock(); 
	     pbSubtracted.addSource(rendered); 
	     pbSubtracted.add(xx.floatValue()); 
	     pbSubtracted.add(yy.floatValue()); 
	     pbSubtracted.add(widthh.floatValue());
	     pbSubtracted.add(heightt.floatValue());

	     System.out.println(rendered.getMinX()+" "+rendered.getMinY());
	     System.out.println(rendered.getWidth()+" "+rendered.getHeight());
	     System.out.println(xx+" "+yy+" "+widthh+" "+heightt);
	     RenderedOp subtractedImage = JAI.create("crop",pbSubtracted);
			final SampleDimension sd =raster.getSampleDimensions().get(0);
			List<SampleDimension>sds=new LinkedList<SampleDimension>();
			sds.add(sd);
	        GridExtent extent=new GridExtent(subtractedImage.getWidth(), subtractedImage.getHeight());
	        GridGeometry gridgeom=new GridGeometry(extent, PixelInCell.CELL_CENTER, raster.getGridGeometry().getGridToCRS(PixelInCell.CELL_CENTER), raster.getCoordinateReferenceSystem());
	        List<SampleDimension> dimensions=new LinkedList<SampleDimension>();
	        DefaultNameFactory fac=new DefaultNameFactory();
	        for(int i=0;i<subtractedImage.getNumBands();i++) {
	        	dimensions.add(new SampleDimension(fac.createGenericName(null,  "Dimension "+i),0.,new LinkedList<Category>()));
	        }
	        BufferedGridCoverage coverage=new BufferedGridCoverage(
	        		gridgeom, dimensions, subtractedImage.getData().getDataBuffer());
			return coverage;
	}
	
	public static NodeValue cropRaster(CoverageWrapper wrapper,Double width, Double height, Double x, Double y) throws MismatchedDimensionException, TransformException {
		 GridCoverage raster=wrapper.getXYGeometry();
		 Coordinate coord=worldToRaster(wrapper, x, y);
		 Coordinate coord2=worldToRaster(wrapper, x+width, y+height);
		 Double xx=coord.getX();
		 Double yy=coord.getY();
		 xx=Double.valueOf(xx.intValue())-1;
		 yy=Double.valueOf(yy.intValue())-1;
		 Double widthh=coord2.getX()-x;
		 Double heightt=coord2.getY()-y;		 
		 ParameterBlock pbSubtracted = new ParameterBlock(); 
	     pbSubtracted.addSource(raster.render(null)); 
	     pbSubtracted.add(xx.floatValue()); 
	     pbSubtracted.add(yy.floatValue()); 
	     pbSubtracted.add(widthh.floatValue());
	     pbSubtracted.add(heightt.floatValue());
	     System.out.println(raster.render(null).getWidth()+" "+raster.render(null).getHeight());
	     System.out.println(xx+" "+yy+" "+widthh+" "+heightt);
	     RenderedOp subtractedImage = JAI.create("crop",pbSubtracted);
	     final SampleDimension sd =raster.getSampleDimensions().get(0);
			List<SampleDimension>sds=new LinkedList<SampleDimension>();
			sds.add(sd);
	        GridExtent extent=new GridExtent(subtractedImage.getWidth(), subtractedImage.getHeight());
	        GridGeometry gridgeom=new GridGeometry(extent, PixelInCell.CELL_CENTER, raster.getGridGeometry().getGridToCRS(PixelInCell.CELL_CENTER), raster.getCoordinateReferenceSystem());
	        List<SampleDimension> dimensions=new LinkedList<SampleDimension>();
	        DefaultNameFactory fac=new DefaultNameFactory();
	        for(int i=0;i<subtractedImage.getNumBands();i++) {
	        	dimensions.add(new SampleDimension(fac.createGenericName(null,  "Dimension "+i),0.,new LinkedList<Category>()));
	        }
	        BufferedGridCoverage coverage=new BufferedGridCoverage(
	        		gridgeom, dimensions, subtractedImage.getData().getDataBuffer());
			return CoverageWrapper.createCoverage((GridCoverage)coverage, wrapper.getSrsURI(), wrapper.getRasterDatatypeURI())
					.asNodeValue();
	}
	
	
	public static NodeValue createEmptyRaster(Double width, Double height, Double upperleftx, Double upperlefty, Double val) {
		Double pixelsize;
		WritableRaster raster;
		if(width.intValue()<=0 || height.intValue()<=0) {
			raster = RasterFactory.createBandedRaster(DataBuffer.TYPE_FLOAT, 2, 2, 1, null);
		}else {
			raster = RasterFactory.createBandedRaster(DataBuffer.TYPE_FLOAT, width.intValue(), height.intValue(), 1, null);
		}

		for (int y = 0; y < height; y++) {
			for (int x = 0; x < width; x++) {
				raster.setSample(x, y, 0, val);
			}
		}
		//CoordinateReferenceSystem crs = CommonCRS.WGS84.defaultGeographic();
		CoordinateReferenceSystem crss=null;
		Envelope2D envelope=null;
		try {
			crss = CRS.forCode("EPSG:4326");
			envelope = new Envelope2D(crss, 0, 0, 30, 30);
		} catch (FactoryException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			
			envelope = new Envelope2D(CommonCRS.WGS84.defaultGeographic(), 0, 0, 30, 30);
		}
        GridExtent extent=new GridExtent(raster.getWidth(), raster.getHeight());
        GridGeometry gridgeom=new GridGeometry(extent, PixelInCell.CELL_CENTER, null, crss);
        List<SampleDimension> dimensions=new LinkedList<SampleDimension>();
        DefaultNameFactory fac=new DefaultNameFactory();
        for(int i=0;i<raster.getNumBands();i++) {
        	dimensions.add(new SampleDimension(fac.createGenericName(null,  "Dimension "+i),0.,new LinkedList<Category>()));
        }
        BufferedGridCoverage coverage=new BufferedGridCoverage(
        		gridgeom, dimensions, raster.getDataBuffer());		
		return CoverageWrapper.createCoverage(coverage, "EPSG:4326", HexWKBDatatype.URI.toString()).asNodeValue();
	}
	
	public static Geometry getCorrectVectorRepresentation(Wrapper wrapper) {
		if(wrapper instanceof GeometryWrapper) {
			return ((GeometryWrapper) wrapper).getXYGeometry();
		}else {
			return toGeometry(((CoverageWrapper) wrapper).getParsingGeometry().getGridGeometry().getEnvelope());
		}
	}
	
	public static Geometry toGeometry(final Envelope2D envelope) {
        GeometryFactory gf = new GeometryFactory();
        return gf.createPolygon(gf.createLinearRing(
                new Coordinate[]{
                    new Coordinate(envelope.getMinX(), envelope.getMinY()),
                    new Coordinate(envelope.getMaxX(), envelope.getMinY()),
                    new Coordinate(envelope.getMaxX(), envelope.getMaxY()),
                    new Coordinate(envelope.getMinX(), envelope.getMaxY()),
                    new Coordinate(envelope.getMinX(), envelope.getMinY())
                }), null);
    }
	
	public static Geometry toGeometry(final OctagonalEnvelope envelope) {
        GeometryFactory gf = new GeometryFactory();
        return gf.createPolygon(gf.createLinearRing(
                new Coordinate[]{
                    new Coordinate(envelope.getMinX(), envelope.getMinY()),
                    new Coordinate(envelope.getMaxX(), envelope.getMinY()),
                    new Coordinate(envelope.getMaxX(), envelope.getMaxY()),
                    new Coordinate(envelope.getMinX(), envelope.getMaxY()),
                    new Coordinate(envelope.getMinX(), envelope.getMinY())
                }), null);
    }
	
	public static Geometry toGeometry(final Envelope envelope) {
        GeometryFactory gf = new GeometryFactory();
        return gf.createPolygon(gf.createLinearRing(
                new Coordinate[]{
                    new Coordinate(envelope.getMinX(), envelope.getMinY()),
                    new Coordinate(envelope.getMaxX(), envelope.getMinY()),
                    new Coordinate(envelope.getMaxX(), envelope.getMaxY()),
                    new Coordinate(envelope.getMinX(), envelope.getMaxY()),
                    new Coordinate(envelope.getMinX(), envelope.getMinY())
                }), null);
    }

	public static Geometry toGeometry(final org.opengis.geometry.Envelope envelope) {
        GeometryFactory gf = new GeometryFactory();
        return gf.createPolygon(gf.createLinearRing(
                new Coordinate[]{
                    new Coordinate(envelope.getMinimum(0), envelope.getMinimum(1)),
                    new Coordinate(envelope.getMaximum(0), envelope.getMinimum(1)),
                    new Coordinate(envelope.getMaximum(0), envelope.getMaximum(1)),
                    new Coordinate(envelope.getMinimum(0), envelope.getMaximum(1)),
                    new Coordinate(envelope.getMinimum(0), envelope.getMinimum(1))
                }), null);
    }
	
	/*public static Geometry toGeometry(final BoundingBox envelope) {
        GeometryFactory gf = new GeometryFactory();
        return gf.createPolygon(gf.createLinearRing(
                new Coordinate[]{
                    new Coordinate(envelope.getMinX(), envelope.getMinY()),
                    new Coordinate(envelope.getMaxX(), envelope.getMinY()),
                    new Coordinate(envelope.getMaxX(), envelope.getMaxY()),
                    new Coordinate(envelope.getMinX(), envelope.getMaxY()),
                    new Coordinate(envelope.getMinX(), envelope.getMinY())
                }), null);
    }*/
	
	 public static Geometry toGeometry(final Rectangle envelope) {
	        GeometryFactory gf = new GeometryFactory();
	        return gf.createPolygon(gf.createLinearRing(
	                new Coordinate[]{
	                    new Coordinate(envelope.getMinX(), envelope.getMinY()),
	                    new Coordinate(envelope.getMaxX(), envelope.getMinY()),
	                    new Coordinate(envelope.getMaxX(), envelope.getMaxY()),
	                    new Coordinate(envelope.getMinX(), envelope.getMaxY()),
	                    new Coordinate(envelope.getMinX(), envelope.getMinY())
	                }), null);
	    }
	
	 
		public static GeometryWrapper createGeometry(List<Coordinate> coordinates,String geomtype,GeometryWrapper geometry) {
			switch(geomtype) {
			case "Point":
				return GeometryWrapperFactory.createPoint(coordinates.get(0), geometry.getSrsURI(), geometry.getGeometryDatatypeURI());
			case "MultiPoint":
				return GeometryWrapperFactory.createMultiPoint(coordinates, geometry.getSrsURI(), geometry.getGeometryDatatypeURI());
			case "LineString":
				return GeometryWrapperFactory.createLineString(coordinates, geometry.getSrsURI(), geometry.getGeometryDatatypeURI());
			case "Polygon":
				return GeometryWrapperFactory.createPolygon(coordinates, geometry.getSrsURI(), geometry.getGeometryDatatypeURI());
			case "MultiLineString":
				List<LineString> list=new LinkedList<LineString>();
				list.add((LineString)GeometryWrapperFactory.createLineString(coordinates, geometry.getSrsURI(), geometry.getGeometryDatatypeURI()).getXYGeometry());
				return GeometryWrapperFactory.createMultiLineString(list, geometry.getSrsURI(), geometry.getGeometryDatatypeURI());
			case "MultiPolygon":
				List<Polygon> plist=new LinkedList<Polygon>();
				plist.add((Polygon)GeometryWrapperFactory.createPolygon(coordinates, geometry.getSrsURI(), geometry.getGeometryDatatypeURI()).getXYGeometry());
				return GeometryWrapperFactory.createMultiPolygon(plist, geometry.getSrsURI(), geometry.getGeometryDatatypeURI());
			default:
				return null;
			}
		}
		
		public static GeometryWrapper createGeometry(Coordinate[] coordarray,String geomtype,GeometryWrapper geometry) {
			return createGeometry(Arrays.asList(coordarray), geomtype, geometry);
		}
}
