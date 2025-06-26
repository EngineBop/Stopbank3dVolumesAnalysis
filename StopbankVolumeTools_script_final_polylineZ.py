import arcpy
import math
import os
from datetime import datetime

def main(centerline_fc, dem, output_gdb):
    arcpy.env.overwriteOutput = True

    if not arcpy.Exists(output_gdb):
        gdb_folder = os.path.dirname(output_gdb)
        gdb_name = os.path.basename(output_gdb)
        arcpy.CreateFileGDB_management(gdb_folder, gdb_name)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cross_fc = os.path.join(output_gdb, f"crossSections_" + timestamp)
    sampled_fc = os.path.join(output_gdb, f"sampledElev_" + timestamp)
    polylineZ_fc = os.path.join(output_gdb, f"stopbank3DLines_" + timestamp)

    def generate_cross_sections(centerline_fc, spacing=10, length=40):
        arcpy.management.GeneratePointsAlongLines(centerline_fc, "in_memory/temp_points", "DISTANCE", Distance=f"{spacing} Meters")
        sr = arcpy.Describe(centerline_fc).spatialReference
        arcpy.CreateFeatureclass_management("in_memory", "cross_temp", "POLYLINE", spatial_reference=sr)

        centerline_geom = [row[0] for row in arcpy.da.SearchCursor(centerline_fc, ["SHAPE@"])][0]

        with arcpy.da.InsertCursor("in_memory/cross_temp", ["SHAPE@"]) as ic:
            with arcpy.da.SearchCursor("in_memory/temp_points", ["SHAPE@"]) as sc:
                for row in sc:
                    pt = row[0].firstPoint
                    next_pt = centerline_geom.positionAlongLine(centerline_geom.measureOnLine(pt) + 1).firstPoint
                    dx = next_pt.X - pt.X
                    dy = next_pt.Y - pt.Y
                    angle = math.atan2(dy, dx)
                    perp_angle = angle + math.pi / 2

                    half_len = length / 2
                    dx_perp = math.cos(perp_angle) * half_len
                    dy_perp = math.sin(perp_angle) * half_len

                    p1 = arcpy.Point(pt.X - dx_perp, pt.Y - dy_perp)
                    p2 = arcpy.Point(pt.X + dx_perp, pt.Y + dy_perp)
                    line = arcpy.Polyline(arcpy.Array([p1, p2]), sr)
                    ic.insertRow([line])

        arcpy.CopyFeatures_management("in_memory/cross_temp", cross_fc)
        return cross_fc

    def sample_elevations(cross_sections, dem, sampled_output_fc):
        arcpy.ddd.InterpolateShape(dem, cross_sections, sampled_output_fc, 1)
        return sampled_output_fc

    def promote_to_z_lines(input_fc, output_fc):
        arcpy.management.FeatureVerticesToPoints(input_fc, "in_memory/temp_pts", "ALL")
        sr = arcpy.Describe(input_fc).spatialReference
        arcpy.CreateFeatureclass_management(os.path.dirname(output_fc), os.path.basename(output_fc), "POLYLINE", spatial_reference=sr, has_z="ENABLED")

        lines = {}
        with arcpy.da.SearchCursor("in_memory/temp_pts", ["SHAPE@", "ORIG_FID"]) as cursor:
            for pt, oid in cursor:
                if oid not in lines:
                    lines[oid] = []
                lines[oid].append(pt.centroid)

        with arcpy.da.InsertCursor(output_fc, ["SHAPE@"]) as insert_cursor:
            for pts in lines.values():
                z_line = arcpy.Polyline(arcpy.Array(pts), sr, True)
                insert_cursor.insertRow([z_line])

        return output_fc

    cross_sections = generate_cross_sections(centerline_fc)
    sampled = sample_elevations(cross_sections, dem, sampled_fc)
    promote_to_z_lines(sampled, polylineZ_fc)

if __name__ == "__main__":
    main(arcpy.GetParameterAsText(0),
         arcpy.GetParameterAsText(1),
         arcpy.GetParameterAsText(2))
