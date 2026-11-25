#!/bin/bash
# Serve the mbirtorch 3D slice viewer on the circuit board at downsampling 2 (940 x 940 x 748), the
# volumes of the IPMR paper's method comparison table (Gautschi jobs 18441112 and 18441114).
# board_x2_slab.py saved, for each method, the slab around the axial slice of Fig. 12: rows 297 to 707,
# columns 157 to 467, and slices 396 to 517.  Slab slice 60 is slice 456, which is slice 105 of the
# paper's 363 x 363 x 251 grid.  The six slabs hold 0.4 GB, so this script runs on a login node:
#     bash serve_viewer3d_board_x2.sh
# The script writes the node, the port, and the URL to viewer_logs/viewer_url_x2.txt.
# Stop the viewer with pkill -f 'serve_viewer3d[.]py' on the same login node.

DIR=/home/li5273/PycharmProjects/scripts/2026/1111/board_viewer
SLAB=/home/li5273/Desktop/data/output/2026/1105/ipmr_timing/methods/board/axial_slab
OUTPUT=/home/li5273/Desktop/data/output
# The tornado link of the 4D viewer trial and the mbirtorch copy of the MBIR-BHC runs are reused.
VENDOR=$OUTPUT/2026/1001/4d_viewer_trial/vendor
PACKAGE=/home/li5273/PycharmProjects/scripts/2026/1110/mbir_bhc/code/mbirtorch
# The gray window of Fig. 12 of the paper, in 1/mm.
WINDOW_MIN=-0.02
WINDOW_MAX=0.06
# The first port WebAgg tries.  The Mac's tunnel must point at the port in the URL file.
PORT=8991
BHC_ITERATION=$(python3 -c "import json; print(json.load(open('$SLAB/slab.json'))['bhc_iteration'])")
SLAB_NOTE="downsampling 2, slab of slices 396 to 517; slab slice 60 is Fig. 12 (paper slice 105)"
echo "host $(hostname)  $(date)"

# The viewer's save and load dialogs start in the current folder.
cd "$SLAB" || exit 1
mkdir -p "$DIR/viewer_logs"
rm -f "$DIR/viewer_logs/viewer_url_x2.txt"
PYTHONPATH=$VENDOR /home/li5273/.conda/envs/mbirtorch/bin/python -u "$DIR/serve_viewer3d.py" \
  --package "$PACKAGE" --url-file "$DIR/viewer_logs/viewer_url_x2.txt" --dpi 55 --port $PORT \
  --vmin $WINDOW_MIN --vmax $WINDOW_MAX \
  --title "Circuit board at downsampling 2, axial slab around Fig. 12 (slab slice 60)" \
  --labels "FDK" "MBIR" "NMAR+MBIR" "MBIR-BHC $BHC_ITERATION" "IPMR (no constraints)" "IPMR" \
  --notes "mbirjax FDK, job 18441112, $SLAB_NOTE" \
          "mbirjax MBIR, job 18441112, $SLAB_NOTE" \
          "NMAR with MBIR, job 18441112, $SLAB_NOTE" \
          "mbirtorch MBIR-BHC iteration $BHC_ITERATION, job 18441114, $SLAB_NOTE" \
          "mbirjax IPMR without constraint updates, job 18441112, $SLAB_NOTE" \
          "mbirjax IPMR, job 18441112, $SLAB_NOTE" \
  --volumes "$SLAB/fdk.npy" "$SLAB/mbir.npy" "$SLAB/nmar_mbir.npy" "$SLAB/mbir_bhc.npy" \
            "$SLAB/ipmr_nc.npy" "$SLAB/ipmr.npy"
