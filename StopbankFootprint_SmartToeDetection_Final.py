
import os
import arcpy
import math
from datetime import datetime

def main(sampled_elev_fc, output_gdb, slope_threshold, curvature_threshold, min_elev_drop, min_horiz_dist, max_horiz_dist):
    slope_threshold = float(slope_threshold)
    curvature_threshold = float(curvature_threshold)
    min_elev_drop = float(min_elev_drop)
    min_horiz_dist = float(min_horiz_dist)
    max_horiz_dist = float(max_horiz_dist)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    toe_points_fc = os.path.join(output_gdb, f"toePoints_{timestamp}")
    footprint_fc = os.path.join(output_gdb, f"stopbankFootprint_{timestamp}")

    sr = arcpy.Describe(sampled_elev_fc).spatialReference
    arcpy.CreateFeatureclass_management(output_gdb, os.path.basename(toe_points_fc), "POINT", spatial_reference=sr)
    arcpy.AddField_management(toe_points_fc, "Side", "TEXT")
    arcpy.AddField_management(toe_points_fc, "SlopeDeg", "DOUBLE")
    arcpy.AddField_management(toe_points_fc, "Curvature", "DOUBLE")
    arcpy.AddField_management(toe_points_fc, "DistCrest", "DOUBLE")
    arcpy.AddField_management(toe_points_fc, "ElevDrop", "DOUBLE")

    toe_points = []

    with arcpy.da.SearchCursor(sampled_elev_fc, ["OID@", "SHAPE@"]) as cursor:
        for oid, shape in cursor:
            if shape.length == 0:
                continue

            points = [shape.positionAlongLine(float(d)/shape.length, True).firstPoint for d in [i*0.5 for i in range(int(shape.length/0.5)+1)]]
            crest = points[len(points)//2]
            crest_z = crest.Z

            slopes = []
            curvatures = []

            for i in range(1, len(points)-1):
                dz = points[i+1].Z - points[i-1].Z
                dx = points[i+1].X - points[i-1].X
                dy = points[i+1].Y - points[i-1].Y
                horiz = math.hypot(dx, dy)
                slope = math.degrees(math.atan2(dz, horiz)) if horiz > 0 else 0
                slopes.append(slope)

            for i in range(1, len(slopes)-1):
                curv = slopes[i+1] - slopes[i-1]
                curvatures.append(curv)

            left_toe = None
            right_toe = None

            for side, seq in [("left", range(1, len(curvatures)//2)), ("right", range(len(curvatures)-2, len(curvatures)//2, -1))]:
                for idx in seq:
                    slope_val = slopes[idx]
                    curv = curvatures[idx-1]
                    pt = points[idx+1]
                    elev_drop = crest_z - pt.Z
                    dist = math.hypot(pt.X - crest.X, pt.Y - crest.Y)

                    if abs(slope_val) < slope_threshold and abs(curv) > curvature_threshold and elev_drop > min_elev_drop and min_horiz_dist < dist < max_horiz_dist:
                        if side == "left" and not left_toe:
                            left_toe = pt
                        elif side == "right" and not right_toe:
                            right_toe = pt
                        break

            if left_toe:
                arcpy.da.InsertCursor(toe_points_fc, ["SHAPE@", "Side", "SlopeDeg", "Curvature", "DistCrest", "ElevDrop"]).insertRow(
                    [arcpy.PointGeometry(left_toe, sr), "Left", slope_val, curv, dist, elev_drop])

            if right_toe:
                arcpy.da.InsertCursor(toe_points_fc, ["SHAPE@", "Side", "SlopeDeg", "Curvature", "DistCrest", "ElevDrop"]).insertRow(
                    [arcpy.PointGeometry(right_toe, sr), "Right", slope_val, curv, dist, elev_drop])

            if left_toe and right_toe:
                toe_points.append((left_toe, right_toe))

    if toe_points:
        arr = arcpy.Array([pt for pt, _ in toe_points] + [pt for _, pt in reversed(toe_points)] + [toe_points[0][0]])
        poly = arcpy.Polygon(arr, sr)
        arcpy.CreateFeatureclass_management(output_gdb, os.path.basename(footprint_fc), "POLYGON", spatial_reference=sr)
        with arcpy.da.InsertCursor(footprint_fc, ["SHAPE@"]) as ic:
            ic.insertRow([poly])

if __name__ == "__main__":
    main(
        arcpy.GetParameterAsText(0),
        arcpy.GetParameterAsText(1),
        arcpy.GetParameterAsText(2),
        arcpy.GetParameterAsText(3),
        arcpy.GetParameterAsText(4),
        arcpy.GetParameterAsText(5),
        arcpy.GetParameterAsText(6)
    )
