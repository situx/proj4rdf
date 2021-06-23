package de.hsmainz.cs.semgis.arqextension.util;

import java.io.IOException;

import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.CoordinateSequence;
import org.locationtech.jts.geom.Geometry;
import org.locationtech.jts.geom.GeometryCollection;
import org.locationtech.jts.geom.LineString;
import org.locationtech.jts.geom.MultiPoint;
import org.locationtech.jts.geom.Point;
import org.locationtech.jts.geom.Polygon;

public class JtsPolyshapeWriter extends PolyshapeWriter {

  // --------------------------------------------------------------
  // Write JTS To GeoJSON
  // --------------------------------------------------------------
/*
  protected void write(Encoder output, CoordinateSequence coordseq) throws IOException {
    int dim = coordseq.getDimension();
//    if(dim>2) {
//      throw new IllegalArgumentException("only supports 2d geometry now ("+dim+")");
//    }
    for (int i = 0; i < coordseq.size(); i++) {
      output.write(coordseq.getOrdinate(i, 0),
                   coordseq.getOrdinate(i, 1));
    }
  }

  protected void write(Encoder output, Coordinate[] coord) throws IOException {
    for (int i = 0; i < coord.length; i++) {
      output.write(coord[i].x, coord[i].y);
    }
  }

  protected void write(Encoder output, Polygon p) throws IOException {
    output.write(PolyshapeWriter.KEY_POLYGON);
    write(output, p.getExteriorRing().getCoordinateSequence());
    for (int i = 0; i < p.getNumInteriorRing(); i++) {
      output.startRing();
      write(output, p.getInteriorRingN(i).getCoordinateSequence());
    }
  }

  public void write(Encoder output, Geometry geom) throws IOException {
    if (geom instanceof Point) {
      Point v = (Point) geom;
      output.write(PolyshapeWriter.KEY_POINT);
      write(output, v.getCoordinateSequence());
      return;
    } else if (geom instanceof Polygon) {
      write(output, (Polygon) geom);
      return;
    } else if (geom instanceof LineString) {
      LineString v = (LineString) geom;
      output.write(PolyshapeWriter.KEY_LINE);
      write(output, v.getCoordinateSequence());
      return;
    } else if (geom instanceof MultiPoint) {
      MultiPoint v = (MultiPoint) geom;
      output.write(PolyshapeWriter.KEY_MULTIPOINT);
      write(output, v.getCoordinates());
      return;
    } else if (geom instanceof GeometryCollection) {
      GeometryCollection v = (GeometryCollection) geom;
      for (int i = 0; i < v.getNumGeometries(); i++) {
        if (i > 0) {
          output.seperator();
        }
        write(output, v.getGeometryN(i));
      }
    } else {
      throw new UnsupportedOperationException("unknown: " + geom);
    }
  }
*/

}