#!/bin/bash
# Serve the mbirtorch 3D slice viewer on the full resolution circuit board recons of the IPMR
# runtime study (Horizontal_Elec_Board_1800, 900 views, full detector, 1733 x 1733 x 953):
# FDK, MBIR, and IPMR.  The full volumes hold 11.4 GB each, more than a login node allows one
# user, so the viewer opens slices 612 to 676 only, which save_board_slab.py saved.  Slice 644,
# the middle of the slab, matches slice 105 of the paper's 363 x 363 x 251 volume of Fig. 12.
# The three slabs hold 2.3 GB, so this script runs on a Gautschi login node:
#     bash serve_viewer3d_board_full_res.sh
# The script writes the node, the port, and the URL to viewer_logs/viewer_url_full_res.txt.
# Stop the viewer with pkill -f 'serve_viewer3d[.]py' on the same login node.

DIR=/home/li5273/PycharmProjects/scripts/2026/1111/board_viewer
OUTPUT=/home/li5273/Desktop/data/output
SLAB=$OUTPUT/2026/1105/ipmr_timing/real/board/slab_612_676
# The tornado link of the 4D viewer trial and the mbirtorch copy of the MBIR-BHC runs are reused.
VENDOR=$OUTPUT/2026/1001/4d_viewer_trial/vendor
PACKAGE=/home/li5273/PycharmProjects/scripts/2026/1110/mbir_bhc/code/mbirtorch
# The upper end of the gray window of Fig. 12 of the paper, in 1/mm.
WINDOW_MAX=0.06
SLAB_NOTE="slices 612 to 676 of 953; slab slice 32 is full resolution slice 644"
echo "host $(hostname)  $(date)"

# The viewer's save and load dialogs start in the current folder.
cd "$SLAB" || exit 1
mkdir -p "$DIR/viewer_logs"
rm -f "$DIR/viewer_logs/viewer_url_full_res.txt"
PYTHONPATH=$VENDOR /home/li5273/.conda/envs/mbirtorch/bin/python -u "$DIR/serve_viewer3d.py" \
  --package "$PACKAGE" --url-file "$DIR/viewer_logs/viewer_url_full_res.txt" --dpi 80 --vmax $WINDOW_MAX \
  --title "Circuit board, full resolution 1733 x 1733 x 953, slices 612 to 676" \
  --labels "FDK" "MBIR" "IPMR" \
  --notes "mbirjax 0.7.3 FDK, runtime job 17958016, $SLAB_NOTE" \
          "mbirjax 0.7.3 MBIR, runtime job 17958016, $SLAB_NOTE" \
          "mbirjax 0.7.3 IPMR (Table III settings), runtime job 17958016, $SLAB_NOTE" \
  --volumes "$SLAB/fdk.npy" "$SLAB/mbir.npy" "$SLAB/ipmr.npy"
