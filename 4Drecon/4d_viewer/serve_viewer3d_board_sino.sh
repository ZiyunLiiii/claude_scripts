#!/bin/bash
# Serve the mbirtorch 3D slice viewer on the circuit board sinogram at downsampling 2 with every 4th view
# (450 x 748 x 940), before and after the automatic crop of mbirjax 0.6.15 (auto_crop_sino_conebeam).
# show_auto_crop.py saved both.  The slider moves through the views.  The sinograms hold 2.5 GB, so this
# script runs on a login node:
#     bash serve_viewer3d_board_sino.sh
# The script writes the node, the port, and the URL to viewer_logs/viewer_url_sino.txt.
# Stop the viewer with pkill -f 'serve_viewer3d[.]py' on the same login node.

DIR=/home/li5273/PycharmProjects/scripts/2026/1111/board_viewer
SINO=/home/li5273/Desktop/data/output/2026/1105/ipmr_timing/methods/auto_crop/board_x2
OUTPUT=/home/li5273/Desktop/data/output
# The tornado link of the 4D viewer trial and the mbirtorch copy of the MBIR-BHC runs are reused.
VENDOR=$OUTPUT/2026/1001/4d_viewer_trial/vendor
PACKAGE=/home/li5273/PycharmProjects/scripts/2026/1110/mbir_bhc/code/mbirtorch
# The gray window, a little above the largest sinogram value of 99.9 % of the pixels (1.85).
WINDOW_MAX=2.0
# The first port WebAgg tries.  The Mac's tunnel must point at the port in the URL file.
PORT=8992
echo "host $(hostname)  $(date)"

cd "$SINO" || exit 1
mkdir -p "$DIR/viewer_logs"
rm -f "$DIR/viewer_logs/viewer_url_sino.txt"
PYTHONPATH=$VENDOR /home/li5273/.conda/envs/mbirtorch/bin/python -u "$DIR/serve_viewer3d.py" \
  --package "$PACKAGE" --url-file "$DIR/viewer_logs/viewer_url_sino.txt" --dpi 70 --port $PORT \
  --vmin 0 --vmax $WINDOW_MAX --slice-axis 0 \
  --title "Circuit board sinogram, downsampling 2, every 4th view: before and after the automatic crop" \
  --labels "View" "View" \
  --notes "before auto_crop_sino_conebeam (the loader already removed its 20-pixel border)" \
          "after auto_crop_sino_conebeam: crop 0 on every side" \
  --volumes "$SINO/sino_before_crop.npy" "$SINO/sino_after_crop.npy"
