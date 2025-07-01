# Stopbank Footprints from Profiles

**Python script for ArcGIS Pro — generates toe points and footprint polygons from 3D stopbank profile data**

---

## 📌 Purpose
This tool takes a set of 3D stopbank profile lines and:
- Identifies left and right toe points based on slope, curvature, elevation drop, and distance from crest
- Creates a polygon footprint by connecting these toe points
- Outputs feature classes for toe points and the footprint polygon

The tool is designed to support stopbank volume estimation and footprint mapping.

---

## ⚙ Parameters

| Parameter | Description |
|------------|-------------|
| **Profile Data** | Input 3D profile lines (typically output from a stopbank profile sampling tool). |
| **Output Geodatabase** | Geodatabase where output feature classes will be written. |
| **Slope Threshold** | The maximum slope (in degrees) at the toe location — lower values force flatter toe detection. _Default: 15_ |
| **Curvature Threshold** | The minimum curvature difference to identify a toe (difference between adjacent slopes). Larger values make detection stricter. _Default: 3_ |
| **Min Elevation Drop** | Minimum elevation difference from crest to candidate toe point — helps exclude minor undulations. _Default: 0.7_ |
| **Min Horizontal Dist** | Minimum horizontal distance from crest to toe point — prevents points too close to crest being classified as toes. _Default: 1.5_ |
| **Max Horizontal Dist** | Maximum horizontal distance from crest — filters out points too far to be valid toes. _Default: 12_ |

👉 **Adjusting thresholds:**  
- Loosening thresholds (larger slope or smaller curvature values) will detect more toe points but may include noise.  
- Tightening thresholds will give cleaner results but may miss subtle toes.

---

## 📝 Outputs

| Output | Description |
|---------|--------------|
| **toePoints_YYYYMMDD_HHMMSS** | Point feature class with detected toe points, includes attributes: Side (Left/Right), SlopeDeg, Curvature, DistCrest, ElevDrop. |
| **stopbankFootprint_YYYYMMDD_HHMMSS** | Polygon feature class representing the stopbank footprint created from the toe points. |

---

## 💡 Notes
- The footprint will only be generated if both left and right toes were found for at least some profiles.  
- The tool assumes profiles run consistently across the stopbank (perpendicular to crest).  
- It works best with clean 3D profile data derived from accurate DEMs.

---

## 🛠 Example usage
Run the tool from an ArcGIS Pro script tool with parameters set as:

Profile Data: stopbank3DLines_20250625_164443
Output GDB: C:\GIS_Temp\dataoutputs_test.gdb
Slope Threshold: 15
Curvature Threshold: 3
Min Elevation Drop: 0.7
Min Horizontal Dist: 1.5
Max Horizontal Dist: 12


---

## 📂 File
`StopbankFootprint_SmartToeDetection.py`  
Place this in your ArcGIS toolbox as a script tool, mapping the parameters in order.

