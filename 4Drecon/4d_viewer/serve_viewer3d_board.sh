#!/bin/bash
# Serve the mbirtorch 3D slice viewer on the circuit board (Horizontal_Elec_Board_1800):
# MBIR-BHC at 20, 40, and 60 iterations, and the IPMR image of the paper.
# The MBIR-BHC volumes are 470 x 470 x 253 (mbirtorch), and the IPMR volume is
# 363 x 363 x 251 (mbirjax with auto crop), so the IPMR panel covers a smaller region.
# The viewer needs no GPU, and the four volumes hold 0.8 GB, so this script runs on a
# Gautschi login node:
#     nohup bash serve_viewer3d_board.sh > viewer_logs/viewer.out 2>&1 < /dev/null &
# The script writes the node, the port, and the URL to viewer_logs/viewer_url.txt.
# Stop the viewer with pkill -f 'serve_viewer3d[.]py' on the same login node.

DIR=/home/li5273/PycharmProjects/scripts/2026/1111/board_viewer
OUTPUT=/home/li5273/Desktop/data/output
BHC=$OUTPUT/2026/1110/mbir_bhc/nsi_scans/circuit_board
IPMR=$OUTPUT/2026/data_for_MAR_paper/circ/circ_stable/recon_3_2_horiz_mar_1800_alpha1_beta0.002_gamma0.1.npy
# The tornado link of the 4D viewer trial and the mbirtorch copy of the MBIR-BHC runs are reused.
VENDOR=$OUTPUT/2026/1001/4d_viewer_trial/vendor
PACKAGE=/home/li5273/PycharmProjects/scripts/2026/1110/mbir_bhc/code/mbirtorch
# The upper end of the gray window of the circuit board figures, in 1/mm.
WINDOW_MAX=0.0541
echo "host $(hostname)  $(date)"

# The viewer's save and load dialogs start in the current folder.
cd "$BHC" || exit 1
PYTHONPATH=$VENDOR /home/li5273/.conda/envs/mbirtorch/bin/python -u "$DIR/serve_viewer3d.py" \
  --package "$PACKAGE" --url-file "$DIR/viewer_logs/viewer_url.txt" --dpi 80 --vmax $WINDOW_MAX \
  --title "Circuit board: MBIR-BHC at 20, 40, 60 iterations, and IPMR" \
  --labels "MBIR-BHC 20" "MBIR-BHC 40" "MBIR-BHC 60" "IPMR" \
  --notes "mbirtorch, 470 x 470 x 253, 450 views, iteration 20 (job 18231583)" \
          "mbirtorch, 470 x 470 x 253, 450 views, iteration 40 (job 18274909)" \
          "mbirtorch, 470 x 470 x 253, 450 views, iteration 60 (job 18274909)" \
          "mbirjax IPMR of the paper, 363 x 363 x 251, auto crop" \
  --volumes "$BHC/bhc_20.npy" "$BHC/bhc_40.npy" "$BHC/bhc_60.npy" "$IPMR"
