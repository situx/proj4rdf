/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


package de.hsmainz.cs.semgis.arqextension.util;

import java.io.IOException;
import java.io.Reader;
import java.io.StringReader;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.List;

import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.Geometry;
import org.locationtech.jts.geom.GeometryFactory;
import org.locationtech.jts.geom.LineString;
import org.locationtech.jts.geom.Point;
import org.locationtech.jts.geom.Polygon;
import org.locationtech.jts.util.GeometricShapeFactory;


/**
 * @see PolyshapeWriter
 */
public class PolyshapeReader {

  final GeometryFactory shpFactory=new GeometryFactory();

  
  public String getFormatName() {
    return "PolyShape";
  }

  
  public Geometry read(Object value) throws IOException, ParseException {
    return read(new StringReader(value.toString().trim()));
  }

  public Geometry readIfSupported(Object value) {
    String v = value.toString().trim();
    char first = v.charAt(0);
    if(first >= '0' && first <= '9') {
      try {
        return read(new StringReader(v));
      } catch (ParseException e) {
      } catch (IOException e) {
      }
    }
    return null;
  }

  // --------------------------------------------------------------
  // Read GeoJSON
  // --------------------------------------------------------------

  public final Geometry read(Reader r) throws ParseException, IOException
  {
    XReader reader = new XReader(r, shpFactory);
    Double arg = null;
    GeometryFactory fac=new GeometryFactory();     
    Geometry lastShape = null;
    List<Geometry> shapes = null;
    /*
    while(!reader.isDone()) {
      char event = reader.readKey();
      if(event<'0' || event > '9') {
        if(event == PolyshapeWriter.KEY_SEPERATOR) {
          continue; // read the next key
        }
        throw new ParseException("expecting a shape key.  not '"+event+"'", -1);
      }

      if(lastShape!=null) {
        if(shapes==null) {
          shapes = new ArrayList<Geometry>();
        }
        shapes.add(lastShape);
      }
      arg = null;
      
      if(reader.peek()==PolyshapeWriter.KEY_ARG_START) {
        reader.readKey(); // skip the key
        arg = reader.readDouble();
        if(reader.readKey()!=PolyshapeWriter.KEY_ARG_END) {
          throw new ParseException("expecting an argument end", -1);
        }
      }
      if(reader.isEvent()) {
        throw new ParseException("Invalid input. Event should be followed by data", -1);
      }
     
      switch(event) {
        case PolyshapeWriter.KEY_POINT: {
          lastShape = shpFactory.createPoint(new Coordinate(reader.readLat(),reader.readLng()));
          break;
        }
        case PolyshapeWriter.KEY_LINE: {

          //reader.readPoints(builder)
          lastShape=fac.createLineString(reader.readPoints());
          //GeometryFactory.LineStringBuilder lineBuilder = shpFactory.lineString();
          
          
          //if(arg!=null) {
            //lineBuilder.buffer(shpFactory.normDist(arg));
          //}
          //lastShape = lineBuilder.build();
          break;
        }
        /*case PolyshapeWriter.KEY_BOX: {

          double lat1 = reader.readLat();
          double lon1 = reader.readLng();
          double lat2= reader.readLat();
          double lon2= reader.readLng();
      	  lastShape=new Envelope(lat1, lon1, lat2, lon2).;

          break;
        }
        case PolyshapeWriter.KEY_MULTIPOINT : {
        	lastShape=fac.createMultiPoint(reader.readPoints());
          break;
        }
        case PolyshapeWriter.KEY_CIRCLE : {
          if(arg==null) {
            throw new IllegalArgumentException("the input should have a radius argument");
          }
          GeometricShapeFactory fac2=new GeometricShapeFactory();
          fac2.setCentre(new Coordinate(reader.readLat(),reader.readLng()));
          fac2.setWidth(arg.doubleValue());
          lastShape=fac2.createCircle();
          /*Polygon circle=fac2.createCircle();
          circle.
          fac.createLinearRing(coordinates)
          lastShape = shpFactory.circle(shpFactory.normX(reader.readLat()), shpFactory.normY(reader.readLng()), 
                shpFactory.normDist(arg.doubleValue()));
          break;
        }
        case PolyshapeWriter.KEY_POLYGON: {
          lastShape = readPolygon(reader);
          break;
        }
        default: {
          throw new ParseException("unhandled key: "+event, -1);
        }
      }
    }
    
    if(shapes!=null) {
      if(lastShape!=null) {
        shapes.add(lastShape);
      }
      if(!shapes.isEmpty() && shapes.get(0)!=null) {
    	  if(shapes.get(0) instanceof Point) {
    		  return fac.createMultiPoint(GeometryFactory.toPointArray(shapes));
    	  }else if(shapes.get(0) instanceof LineString) {
    		  return fac.createMultiLineString(GeometryFactory.toLineStringArray(shapes));    		  
    	  }else if(shapes.get(0) instanceof Polygon) {
    		  return fac.createMultiPolygon(GeometryFactory.toPolygonArray(shapes));
    	  }
      }
    }
    return lastShape;*/
    return null;
  }
  
  protected Geometry readPolygon(XReader reader) throws IOException {
    //Geometry.PolygonBuilder polyBuilder = shpFactory.polygon();
    GeometryFactory fac=new GeometryFactory();
    Polygon poly=fac.createPolygon(reader.readPoints());
    //reader.readPoints(polyBuilder);

    /*if(!reader.isDone() && reader.peek()==PolyshapeWriter.KEY_ARG_START) {
      List<LinearRing> list = new ArrayList<LinearRing>();
      while(reader.isEvent() && reader.peek()==PolyshapeWriter.KEY_ARG_START) {
        reader.readKey(); // eat the event;
        reader.readPoints(polyBuilder.hole()).endHole();
      }
    }

    return polyBuilder.build();*/
    return poly;
  }

  /**
   * from Apache 2.0 licensed:
   * https://github.com/googlemaps/android-maps-utils/blob/master/library/src/com/google/maps/android/PolyUtil.java
   */
  public static class XReader {
    int lat = 0;
    int lng = 0;
    
    int head = -1;
    final Reader input;
    final GeometryFactory shpFactory;

    public XReader(final Reader input, GeometryFactory shpFactory) throws IOException {
      this.input = input;
      this.shpFactory = shpFactory;
      head = input.read();
    }
    
    public Coordinate[] readPoints() throws IOException {
      List<Coordinate> coords=new ArrayList<Coordinate>();
      while(isData()) {
    	  coords.add(new Coordinate(readLat(),readLng()));
      }
      return coords.toArray(new Coordinate[0]);
    }

    public double readLat() throws IOException {
      lat += readInt();
      return lat * 1e-5;
    }

    public double readLng() throws IOException {
      lng += readInt();
      return lng * 1e-5;
    }
    
    public double readDouble() throws IOException {
      return readInt() * 1e-5;
    }
    
    public int peek() {
      return head;
    }

    public char readKey() throws IOException {
      lat = lng = 0; // reset the offset
      char key = (char)head;
      head = input.read();
      return key;
    }

    public boolean isData() {
      return head >= '?';
    }

    public boolean isDone() {
      return head < 0;
    }
    
    public boolean isEvent() {
      return head > 0 && head < '?';
    }
    
    int readInt() throws IOException
    {
      int b;
      int result = 1;
      int shift = 0;
      do {
        b = head - 63 - 1;
        result += b << shift;
        shift += 5;
        
        head = input.read();
      } while (b >= 0x1f);
      return (result & 1) != 0 ? ~(result >> 1) : (result >> 1);
    }
  }
}