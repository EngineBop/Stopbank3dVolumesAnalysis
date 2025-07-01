
# 🛠️ Stopbank 3D Volume & Footprint Tools

This repository contains tools and Python scripts for automating the extraction of **3D stopbank profiles**, **footprint polygons**, and enabling **volume estimation**—using only a stopbank **centerline** and a **DEM**.

These tools are designed for use in **ArcGIS Pro** and are especially useful in flood protection asset management and stopbank volume auditing.

---

## 🚀 What This Toolkit Does

With only a centerline and a DEM, this set of scripts will:

1. Generate evenly spaced 3D **cross-section profiles**
2. Automatically detect **toe points** on each side of the stopbank
3. Construct a **footprint polygon** from these points
4. Enable volume estimation using ArcGIS **Cut/Fill**

---

## 🗂️ Repository Contents

This repository contains:

| Script | Description |
|--------|-------------|
| `Stopbank3DProfiles_FromCenterline.py` | Generates 3D cross-section profiles from a centerline and DEM |
| `StopbankFootprint_SmartToeDetection_Final.py` | Detects toe points and builds a polygon footprint from 3D profiles |
| `/docs/` | Contains individual `README.md` files for each script explaining their parameters, usage, and outputs |
| `README.md` | You're reading it now – the main project overview |

---

## 🔄 Workflow: From Centerline to Volume

Follow this workflow to extract your stopbank footprint and estimate its volume:

### Step 1: Prepare the Data

✅ Merge or dissolve your **stopbank centerline** into a single continuous line  
✅ Clip your **DEM** to the relevant area and export it to a **File Geodatabase** as a **32-bit float raster**  
✅ Ensure both inputs are in the **same coordinate system**

---

### Step 2: Generate 3D Profiles  
**Tool**: `Stopbank3DProfiles_FromCenterline.py`

This script:
- Generates cross-sections every ~10m along the centerline
- Samples elevation values from the DEM
- Produces a feature class of 3D polyline profiles

📄 See `/docs/Stopbank3DProfiles_FromCenterline_README.md` for usage and parameter explanations.

---

### Step 3: Build Stopbank Footprint  
**Tool**: `StopbankFootprint_SmartToeDetection_Final.py`

This script:
- Detects the left and right **toe points** based on slope, curvature, and elevation change
- Constructs a **polygon footprint** using these points
- Outputs:
  - `toePoints_<timestamp>` – individual toe points
  - `stopbankFootprint_<timestamp>` – polygon representing the stopbank extent

📄 See `/docs/StopbankFootprint_SmartToeDetection_Final_README.md` for parameter guidance and interpretation.

---

### Step 4: Calculate Stopbank Volume  
**Tool**: ArcGIS Pro → *Cut Fill (3D Analyst Tool)*

Use the `stopbankFootprint_...` polygon as the **Analysis Mask** and the **DEM** as the **Input Surface**.

> ⚠️ **You do not need a second surface or base DEM.** ArcGIS will assume a flat surface at zero elevation beneath the masked area if none is provided.

- Outputs include **cut** (fill removed) and **fill** (material added) in cubic meters
- These can be exported to tables for reporting

---

## ⚙️ Tips & Notes

- DEM **must be 32-bit float** (set during raster export to FGDB)
- Toe detection is sensitive to **slope and curvature thresholds**
- Adjust these if:
  - Toes are missing or poorly placed
  - Footprint appears incomplete
- QA is recommended: visually inspect toe points overlaid on the DEM

---

## ✅ Example Outputs

| Output Name | Description |
|-------------|-------------|
| `stopbank3DLines_YYYYMMDD_HHMMSS` | 3D cross-section profiles |
| `toePoints_YYYYMMDD_HHMMSS` | Toe points identified on each profile |
| `stopbankFootprint_YYYYMMDD_HHMMSS` | Polygon outlining the base of the stopbank |

---

## 📋 License and Attribution

Created by [EngineBop](https://github.com/EngineBop)  
Intended for public sector use and infrastructure asset management.

---

## 💬 Questions or Suggestions?

Feel free to open an [Issue](https://github.com/EngineBop/Stopbank3dVolumesAnalysis/issues) or get in touch via GitHub Discussions if you want help or want to suggest improvements!
