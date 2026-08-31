# 4Drecon — Goals

Sponsor: Eli Lilly | Proposal: Dropbox/Apps/Overleaf/Proposal_4D_Lilly/main.tex

## Sub-project 1: 4D MACE (Sensor-Orthogonal Recon)
Reconstruct 4D CBCT of a moving phantom from sparse-view gated sinograms. Anchor points 60° apart → period-6 jitter is an artifact → remove via DCT-I filtering → MACE with qGGMRF priors reconstructs 4D.
Open goal: null-space projection dejittering so AX = y is preserved.

## Sub-project 2: Single-View 4D
Reconstruct 4D plume evolution in pork belly tissue from a single fixed-angle acquisition. Steady-state full CBCT scan available as reference/prior.
Open goal: find suitable method (learning-based or model-based).

## Sub-project 3: MAR + Multi-Slice Fusion
Metal artifact reduction for real Lilly NSI scans, seeded from a multi-slice fusion reconstruction (MACE-3 consensus over a tomographic forward model and three DRUNet denoiser agents) instead of mbirjax's standard FDK init. See `mar_fusion/goal.md`.
Open goal: isolate whether the fusion seed changes the converged MAR result for a real reason, or partly from a sub-voxel registration gap between mbirtorch and mbirjax.
