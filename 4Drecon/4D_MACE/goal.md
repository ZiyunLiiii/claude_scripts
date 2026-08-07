# 4D MACE — Goal

## Core Idea: Sensor-Orthogonal Recon
- Dataset: CBCT scan of a moving phantom
- Sinogram gated so each anchor point is **60 degrees apart**
- Creates period-6 jitter (360/60 = 6) in sparse-view recon — this is an artifact, not real motion
- Remove this frequency component, then run MACE to smooth and reconstruct 4D data

## Objectives
- [ ] Validate DCT-I dejittering approach on phantom data
- [ ] Implement null-space projection dejittering: `x + (I - A⁺A)(Px - x)` so AX = y is preserved
- [ ] Write up results for Lilly proposal

## Dataset
- Raw: `/depot/bouman/data/Lilly/4DCT/Phantom_30s_Run1_Dec2024`
- Output: `/home/li5273/Desktop/data/output/2026/0730/phantom_version6`
- Init image: `/home/li5273/Desktop/data/output/2026/4D_shared/48_24_init/phantom_init_image.npy`
- Params: `views_per_bin=48`, `stride=24`, `sharpness=1.0`, `prior_weight=0.5`, `max_mace_itr=10`

## Proposal
/Users/a124601/Library/CloudStorage/Dropbox/Apps/Overleaf/Proposal_4D_Lilly/main.tex
