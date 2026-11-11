#!/bin/bash
# Serve the mbirtorch 3D slice viewer on the circuit board (Horizontal_Elec_Board_1800):
# MBIR-BHC at 20, 40, and 60 iterations, and the IPMR image of the paper.
# The MBIR-BHC runs are 470 x 470 x 253 (mbirtorch), and the IPMR volume is 363 x 363 x 251
# (mbirjax), because the two libraries crop the sinogram differently.  The folder ipmr_grid
# holds the MBIR-BHC volumes cropped to the IPMR grid: 363 rows from row 53, 363 columns
# from column 54, and 251 slices from slice 2.  The two MBIR volumes gave these offsets.
# The cropped grid is still half a voxel from the IPMR grid in rows and columns.
# The viewer needs no GPU, and the four volumes hold 0.5 GB, so this script runs on a
# Gautschi login node:
#     nohup bash serve_viewer3d_board.sh > viewer_logs/viewer.out 2>&1 < /dev/null &
# The script writes the node, the port, and the URL to viewer_logs/viewer_url.txt.
# Stop the viewer with pkill -f 'serve_viewer3d[.]py' on the same login node.

DIR=/home/li5273/PycharmProjects/scripts/2026/1111/board_viewer
OUTPUT=/home/li5273/Desktop/data/output
BHC=$OUTPUT/2026/1110/mbir_bhc/nsi_scans/circuit_board/ipmr_grid
IPMR=$OUTPUT/2026/data_for_MAR_paper/circ/circ_stable/recon_3_2_horiz_mar_1800_alpha1_beta0.002_gamma0.1.npy
# The tornado link of the 4D viewer trial and the mbirtorch copy of the MBIR-BHC runs are reused.
VENDOR=$OUTPUT/2026/1001/4d_viewer_trial/vendor
PACKAGE=/home/li5273/PycharmProjects/scripts/2026/1110/mbir_bhc/code/mbirtorch
# The upper end of the gray window of the circuit board figures, in 1/mm.
WINDOW_MAX=0.0541
CROP_NOTE="cropped to the IPMR grid (rows from 53, columns from 54, slices from 2)"
echo "host $(hostname)  $(date)"

# The viewer's save and load dialogs start in the current folder.
cd "$BHC" || exit 1
rm -f "$DIR/viewer_logs/viewer_url.txt"
PYTHONPATH=$VENDOR /home/li5273/.conda/envs/mbirtorch/bin/python -u "$DIR/serve_viewer3d.py" \
  --package "$PACKAGE" --url-file "$DIR/viewer_logs/viewer_url.txt" --dpi 80 --vmax $WINDOW_MAX \
  --title "Circuit board: MBIR-BHC at 20, 40, 60 iterations, and IPMR" \
  --labels "MBIR-BHC 20" "MBIR-BHC 40" "MBIR-BHC 60" "IPMR" \
  --notes "mbirtorch, iteration 20 (job 18231583), $CROP_NOTE" \
          "mbirtorch, iteration 40 (job 18274909), $CROP_NOTE" \
          "mbirtorch, iteration 60 (job 18274909), $CROP_NOTE" \
          "mbirjax IPMR of the paper, 363 x 363 x 251" \
  --volumes "$BHC/bhc_20.npy" "$BHC/bhc_40.npy" "$BHC/bhc_60.npy" "$IPMR"
