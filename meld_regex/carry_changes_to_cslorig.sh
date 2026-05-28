echo "Step 1. Merge fragments from vcp2_split folder to ../vac-vcp-cmp2/vcp2.txt"
cat vcp2_split/vcp_* > ../vac-vcp-cmp2/vcp2.txt
echo "Step 2. Carry changes from ../vac-vcp-cmp2/vcp2.txt to vcp_corrected_file.txt"
python3 merge_corrected_file_with_vcp.py ../../../cologne/csl-orig/v02/vcp/vcp.txt ../vac-vcp-cmp2/vcp2.txt vcp_corrected_file.txt
echo "Step 3. Copy vcp_corrected_file.txt to ../../../cologne/csl-orig/v02/vcp/vcp.txt"
cp vcp_corrected_file.txt ../../../cologne/csl-orig/v02/vcp/vcp.txt

