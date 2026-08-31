# MAR + Multi-Slice Fusion — Goal

Metal artifact reduction (MAR) for real Lilly NSI scans, seeded from a
multi-slice fusion reconstruction instead of the standard FDK init.

## Background

`mbirjax.preprocess.recon_plastic_metal` reduces metal artifacts by
alternating beam-hardening correction with MBIR reconstruction. It always
starts from an FDK reconstruction it computes internally. The question this
sub-project investigates: does seeding that loop from a better initial
volume — one denoised and consensus-fused across three slice orientations —
change the converged result?

The fusion method is MACE-3 multi-slice fusion: a standard qGGMRF
reconstruction, refined by a PnP-ADMM consensus loop over four agents (the
tomographic forward-model proximal map, plus a pretrained DRUNet denoiser
applied along each of the three slice axes). It comes from
`mbirtorch/experiments/drunet/run_fusion_initial.py`, which had only been
run on a synthetic phantom before this sub-project adapted it to real data.

## Open objectives

- [ ] Isolate whether the fusion-seeded and FDK-seeded MAR results differ
      because of the fusion seed's content, or partly because of the
      sub-voxel grid misalignment between mbirtorch and mbirjax (see
      rules.md). Rerun standard MAR seeded from a shape-corrected FDK volume
      as a control.
- [ ] Sweep `beta` (plastic-metal ridge regularization strength) beyond the
      two values tried so far (0, 0.002 default, 0.02).
- [ ] Test at native resolution once mace.py supports distributing its
      consensus state across multiple GPUs (currently it cannot — see
      rules.md), so the `[2, 2]` downsample workaround is no longer needed.
- [ ] Test on more of the Lilly datasets under `/home/li5273/Desktop/data/`.

## Paths

- Datasets: `/home/li5273/Desktop/data/<name>/` (extracted from the matching
  `<name>.tgz`; see `Autoinjector_HighRes_Horizontal` and
  `Connected_Autoinjector_Vertical` for the layout).
- Fusion code (reused, not duplicated):
  `/home/li5273/PycharmProjects/mbirtorch/experiments/drunet/{agents.py,mace.py}`
- Conda envs: `mbirtorch` (torch, deepinv, mbirtorch — the fusion stage) and
  `mbirjax` (the MAR stage), both under `/home/li5273/.conda/envs/`.
- Run 1 — Autoinjector_HighRes_Horizontal (`num_metal=1`): scripts, sbatch
  launchers, and recons in
  `/home/li5273/Desktop/data/output/2026/0903/`. Four recons compared: plain
  MBIR, multi-slice fusion, standard MAR (FDK init), MAR from fusion init
  (`beta=0` and `beta=0.002`).
- Run 2 — Connected_Autoinjector_Vertical (`num_metal=2`, `beta=0.02`): same
  structure in `/home/li5273/Desktop/data/output/2026/0828/`.
