#!/bin/bash
# Serve the mbirtorch 4D viewer (4D_viewer branch) on two full 99-frame 4D MACE recons
# of Phantom_30s_Run1, for viewing in a browser through an SSH tunnel to the node.
# Both recons used mbirtorch 7a80bbe, 10 MACE iterations, and the nominal
# det_channel_offset.  They differ in the dejitter only: job 16674482 (2026-09-25) ran
# with --no_dejitter, and job 16484769 (2026-09-17) with the default DCT dejitter.
# The viewer needs no GPU.  The job asks for one because the ai partition runs GPU jobs.
#SBATCH --job-name=viewer4d
#SBATCH -A bouman
#SBATCH -N1
#SBATCH -n14
#SBATCH --gpus-per-node=1
#SBATCH -q normal
#SBATCH -p ai
#SBATCH -t 03:00:00
#SBATCH -o /home/li5273/PycharmProjects/scripts/2026/1001/4d_viewer_trial/slurm_logs/%j.out
#SBATCH -e /home/li5273/PycharmProjects/scripts/2026/1001/4d_viewer_trial/slurm_logs/%j.err
set -x

DIR=/home/li5273/PycharmProjects/scripts/2026/1001/4d_viewer_trial
OUTPUT=/home/li5273/Desktop/data/output
OUT=$OUTPUT/2026/1001/4d_viewer_trial
RECON=recon_4d_Phantom_30s_Run1_Dec2024_voxel_pitch_119.56um_frames_99.npy
# The mbirtorch package copy and the tornado link are run artifacts, so they sit in $OUT
# rather than in this repository.  The URL file holds the page's secret prefix, so it
# goes to the ignored slurm_logs folder in the private home folder.
echo "host $(hostname)  job $SLURM_JOB_ID  $(date)"
echo "mbirtorch copy: $(cat $OUT/mbirtorch_4dviewer/COMMIT.txt)"

# The viewer's save and load dialogs start in the current folder, so they start in $OUT.
mkdir -p "$OUT" && cd "$OUT" || exit 1
PYTHONPATH=$OUT/vendor /home/li5273/.conda/envs/mbirtorch/bin/python -u "$DIR/serve_viewer4d.py" \
  --package "$OUT/mbirtorch_4dviewer" --url-file "$DIR/slurm_logs/viewer_url_$SLURM_JOB_ID.txt" --dpi 80 \
  --title "Phantom_30s_Run1: full 4D MACE recons, 99 frames" \
  --labels "no dejitter" "DCT dejitter" \
  --notes "job 16674482, 2026-09-25: nominal offset, --no_dejitter, 10 iterations, mbirtorch 7a80bbe" \
          "job 16484769, 2026-09-17: nominal offset, DCT dejitter, 10 iterations, mbirtorch 7a80bbe" \
  --volumes "$OUTPUT/2026/0924/sor_stage1/4d_nominal_nofilter/$RECON" \
            "$OUTPUT/2026/0917/phantom_mbirtorch_full_slab2gb/$RECON"
