This is a set of scripts to build footprints extents of stopbanks using only a centreline and a dem as the inputs.

The script ran if the lines were merged into a single line.

SO the order is 
- Disolve lines
- Merge Lines
- Clip and save the dem to a fgdb and ensurte to use 32 bit floating
- Download the scripts toolbox
- Run the StopbankVolumeTools_script_final_polylineZ python script
- Then run the StopbankFootprint_SmartToeDetection_Final python script
- Send us 14K
