# 4D Reconstruction — Goals

## Sponsor
Eli Lilly and Company
Proposal: /Users/a124601/Library/CloudStorage/Dropbox/Apps/Overleaf/Proposal_4D_Lilly/main.tex

---

## Sub-project 1: 4D MACE Reconstruction (Sensor-Orthogonal Recon)
- Reconstruct a 4D CBCT volume of a moving phantom using sparse-view gated sinograms
- Gate anchor points 60° apart → period-6 jitter is an artifact → remove it via DCT-I filtering
- Use MACE framework (multi-agent consensus equilibrium) with qGGMRF priors in 3 hyperplane orientations
- **Open goal**: implement null-space projection dejittering so that AX = y is preserved
- Details: see `4D_MACE.md`

## Sub-project 2: Single-View 4D Reconstruction
- Reconstruct the 4D evolution of a plume injected into pork belly tissue
- Only a single fixed-angle view is available (not a full CT scan)
- A steady-state full CBCT scan of the final plume is available as a reference
- **Open goal**: find a method (likely learning-based or model-based with strong prior) to reconstruct 4D from single-view
- Details: see `single_view_recon.md`
