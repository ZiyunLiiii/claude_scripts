# 4Drecon — Goals

Sponsor: Eli Lilly | Proposal: Dropbox/Apps/Overleaf/Proposal_4D_Lilly/main.tex

## Sub-project 1: 4D MACE (Sensor-Orthogonal Recon)
Reconstruct 4D CBCT of a moving phantom from sparse-view gated sinograms. Anchor points 60° apart → period-6 jitter is an artifact → remove via DCT-I filtering → MACE with qGGMRF priors reconstructs 4D.
Open goal: null-space projection dejittering so AX = y is preserved.

## Sub-project 2: Single-View 4D
Reconstruct 4D plume evolution in pork belly tissue from a single fixed-angle acquisition. Steady-state full CBCT scan available as reference/prior.
Open goal: find suitable method (learning-based or model-based).
