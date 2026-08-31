# MAR + Multi-Slice Fusion — Progress Log

## Current Status

The fusion-seeded MAR pipeline works end to end and has been run successfully
on two real Lilly datasets: Autoinjector_HighRes_Horizontal (`num_metal=1`)
and Connected_Autoinjector_Vertical (`num_metal=2`, `beta=0.02`). The second
run needed none of the fixes the first run needed, so the pipeline is stable
across datasets at the `[2, 2]` downsample it currently requires. The open
question is whether the fusion seed changes the converged MAR result for a
real reason, or partly from a sub-voxel registration artifact between
mbirtorch and mbirjax — not yet isolated.

## Log (newest first)

### 2026-08-28 to 2026-08-31 — Connected_Autoinjector_Vertical run

- Extracted `Connected_Autoinjector_Vertical.tgz` (~16 GB compressed, ~19 GB
  extracted) into `/home/li5273/Desktop/data/`.
- Checking the native recon geometry on the login node got OOM-killed, the
  same failure seen for the first dataset. Submitted a short sbatch job
  instead: native recon shape is `(1422, 1422, 1617)`, about 13.1 GB per
  volume, still far too large for MACE-3's eight-volume consensus state on
  one GPU. Reused the `[2, 2]` downsample fix from the first dataset.
- Adapted `fusion_recon.py` and `mar_recon_from_fusion.py` for this dataset
  (`num_metal=2`, `beta=0.02`, per request). Both stages succeeded on the
  first submission — no OOM, no shape mismatch, no quantile error. Recon
  shape at `[2, 2]` downsample: `(731, 731, 818)`, about 1.75 GB/volume.
  Standard recon 328 s, MACE-3 fusion loop about 98 s/iteration, MAR stage
  409 s.
- Also ran the standard (FDK-seeded) MAR recon for this dataset, matching
  `num_metal=2`/`beta=0.02`, for comparison against the fusion-seeded
  result: 515 s.
- Viewed all three Connected_Autoinjector_Vertical recons (fusion, MAR from
  fusion, standard MAR) together in `mj.slice_viewer` over ThinLinc.

### 2026-08-27 — Autoinjector_HighRes_Horizontal run

- Built the two-stage pipeline: `fusion_recon.py` (mbirtorch env: standard
  qGGMRF recon, then MACE-3 fusion with three DRUNet orientation agents) and
  `mar_recon_from_fusion.py` (mbirjax env: `recon_plastic_metal`'s
  beam-hardening loop, copied so the internal FDK init can be replaced with
  the fusion volume).
- Environment did not exist yet. Created a new `mbirtorch` conda env (kept
  separate from the jax-based `mbirjax` env), installed torch + deepinv +
  mbirtorch, and pre-downloaded DRUNet's pretrained weights from the login
  node (compute nodes may lack outbound internet).
- First submission OOM'd: at native resolution this dataset reconstructs to
  `(1880, 1880, 1365)`, about 19.3 GB/volume, and MACE-3's consensus loop
  needs eight such volumes (~154 GB) on one device. Fixed by downsampling
  both stages to `[2, 2]` (recon shape becomes `(940, 940, 692)`, about
  2.4 GB/volume).
- Second submission crashed in `torch.quantile` — real recon volumes exceed
  its roughly 16M-element cap. Fixed by switching to `np.quantile` on a
  CPU copy, and added a cache for the standard recon so a retry does not
  redo that ~7.5-minute step.
- Third submission (stage 2 only, reusing the cached fusion output) hit a
  shape mismatch: mbirtorch computed `(940, 940, 692)`, mbirjax expected
  `(940, 940, 693)`. Both frameworks use the identical `ceil()` formula and
  centering convention; a floating-point rounding difference pushed one
  across an integer boundary. Fixed by tolerating a small mismatch with
  edge-pad/crop — see rules.md for why this is only an approximate fix
  (roughly half a voxel of registration error, not exact).
- With those fixes, produced all four requested comparison recons at the
  same `[2, 2]` resolution: plain MBIR, multi-slice fusion, standard MAR
  (FDK init), and MAR from the fusion init. Also reran the fusion-seeded MAR
  with `beta=0.002` (mbirjax's default) alongside the original `beta=0` run.
- Compared the two MAR variants numerically (chunked/`mmap`, after a naive
  full-array comparison got OOM-killed on the login node): relative RMSE
  15.8%, correlation 0.987. That is a real difference, not noise, but it is
  not yet known how much of it comes from the different seed content versus
  the sub-voxel registration gap above.
- Viewed the recons in `mj.slice_viewer` over a live ThinLinc/X11 session
  (`$DISPLAY=:2.0`), after first defaulting to a static matplotlib PNG
  because the session looked headless. Downsampling each volume 2x per axis
  (via `mmap` + strided slicing) before passing multiple volumes to
  `slice_viewer` was necessary to stay under the login node's per-user
  memory cap (10 GiB, enforced by a systemd cgroup independent of the
  system's total free memory).
