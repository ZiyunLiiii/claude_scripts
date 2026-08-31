# MAR + Multi-Slice Fusion — Rules & Guidelines

## Coding Conventions

- Two-stage pipeline, two conda envs: `fusion_recon.py` runs in the
  `mbirtorch` env (torch, deepinv) and writes `fused_init_recon.npy`;
  `mar_recon_from_fusion.py` runs in the `mbirjax` env and reads that file.
  Keep the two envs separate — installing torch and jax's CUDA packages into
  one env risks a dependency conflict, and was not tried.
- Both stages must use identical `downsample_factor`, `subsample_view_factor`,
  and `auto_crop` settings, or their sinogram shapes and recon geometries
  will not match.
- `recon_plastic_metal` (in `mbirjax.preprocess.mar`) has no `init_recon`
  parameter — it always seeds its beam-hardening loop from an internal FDK
  reconstruction. To seed it from a different volume, copy the loop body
  (see `recon_plastic_metal_seeded` in `mar_recon_from_fusion.py`) rather
  than trying to monkey-patch the function. Reuse the loop's own
  `correct_sino_plastic_metal` and `segment_plastic_metal` calls unchanged;
  only the initial `recon` value differs.

## Gotchas

- **MACE-3's consensus loop cannot span multiple GPUs.**
  `mace.py`'s consensus loop (`mbirtorch/experiments/drunet/mace.py`) keeps
  two full volumes per agent on one device at once. With the forward agent
  plus three DRUNet orientation agents, that is eight volumes on a single
  GPU, regardless of how many GPUs the job requests — the loop has no
  cross-device state distribution. A real NSI scan reconstructs to several
  GB per volume at native resolution (13-19 GB seen so far), so eight copies
  do not fit even on an 80 GB GPU. Fix used so far: request
  `downsample_factor=[2, 2]` for both stages, which cuts each volume to
  roughly 1.6-2.4 GB and comfortably fits the consensus state.
- **mbirtorch and mbirjax can compute different recon shapes for the same
  geometry.** Both use the identical formula
  `ceil((H_iso + z_travel) / delta_voxel_slice)` and the identical centering
  convention, slice `k` at `delta_voxel_slice * (k - (N-1)/2) + offset`. A
  tiny floating-point difference between numpy (mbirtorch) and jax (mbirjax)
  can still push `ceil()` across an integer boundary, so the two models can
  disagree by one slice on the axial axis even with matching settings. This
  is not a simple end-to-end offset: because of the `(N-1)/2` centering, a
  grid with `N` slices and one with `N+1` slices are centered half a voxel
  apart. Tolerate a mismatch of a few voxels by edge-padding or cropping one
  end (see the shape-check block in `mar_recon_from_fusion.py`), and expect
  it to register the volumes to within about half a voxel, not exactly.
  Given that stage 2 runs three full beam-hardening/MBIR passes against the
  real sinogram afterward, this seed-level misalignment is very unlikely to
  survive into the converged answer, but that has not been verified with a
  controlled comparison (see goal.md's first open objective).
- **`torch.quantile` caps out around 16M elements.** A real recon volume has
  several hundred million elements. Use `np.quantile` on a
  `.detach().cpu().numpy()` copy instead — it has no such limit.
- **DRUNet's pretrained weights need internet access to download.** Compute
  nodes on this cluster do not reliably have outbound internet, but the
  login node does. Pre-download once via `deepinv.models.DRUNet(...,
  pretrained='download')` from the login node before submitting a job; the
  weights are cached under `~/.cache/torch/hub/checkpoints/` and reused
  automatically after that.
- **The login node enforces a per-user memory cap independent of total
  system RAM.** `free -h` can report hundreds of GB free while a CPU-side
  numpy operation still gets killed (exit code 137). The real limit is a
  systemd cgroup: `systemctl show user-<uid>.slice -p MemoryMax` (10 GiB was
  the observed cap here), shared across every process the user runs on that
  node, including other sessions. NSI sinogram preprocessing on a full-size
  real scan, or loading more than one or two full recon volumes at once, can
  exceed it. Either use `mmap_mode='r'` plus chunked/strided processing, or
  submit a short sbatch job to do the work on a compute node instead.

## Collaborators
<!-- Add names and roles -->
