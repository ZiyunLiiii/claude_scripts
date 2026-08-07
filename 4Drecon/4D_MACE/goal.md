# 4D MACE — Goal

Sensor-orthogonal CBCT recon. Sinogram gated at 60° intervals → period-6 jitter is an acquisition artifact. Remove via DCT-I filtering, then MACE reconstructs the 4D volume.

## Open objectives
- [ ] Validate DCT-I dejittering on phantom data
- [ ] Null-space projection: `x + (I - A⁺A)(Px - x)` — dejitter only the null-space component so AX = y is preserved
- [ ] Write up for Lilly proposal

## Paths
- Data: `/depot/bouman/data/Lilly/4DCT/Phantom_30s_Run1_Dec2024`
- Output: `/home/li5273/Desktop/data/output/2026/0730/phantom_version6`
- Init image: `/home/li5273/Desktop/data/output/2026/4D_shared/48_24_init/phantom_init_image.npy`
- Params: `views_per_bin=48`, `stride=24`, `sharpness=1.0`, `prior_weight=0.5`, `max_mace_itr=10`
