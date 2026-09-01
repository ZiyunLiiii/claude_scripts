# 4D MACE — Rules & Guidelines

## Coding Conventions
- Language: Python, JAX
- Always pin models/denoisers to a single GPU via configure_devices([device])
- The repo is now `mace4d.py` (the `MACE4DModel` class and all 4D helpers, one
  functional block) plus `recon_4d.py` (the CLI driver). The older
  `model_4d.py`/`utils.py`/`dev_recon.py` layout no longer exists.
- `_dejitter_4d_dct` (inside `mace4d.py`) is the canonical dejitter function —
  modify carefully.

## Things to Check Before Changing the Script
- Never reuse one `OUTPUT_PATH` across differently-configured test runs.
  `recon()` truncates `logs/timing_log.csv` and `logs/task_log.csv` at the
  start of every run, so an earlier run's logs get silently destroyed by a
  later one. Use one output directory per run; it is fine to copy a matching
  cached `init/init_image.npy` into a new directory to skip recomputing it.
- `sigma_noise` and `sigma_x` are not interchangeable and must not be
  estimated the same way. `sigma_noise` should come from a global estimate
  (the whole reconstruction); `sigma_x`, if estimated per orientation batch,
  must be computed on the *full* batch array — never pass a merged
  multi-hyperplane batch into mbirjax's `auto_set_regularization_params()`
  unchanged, since its internal `subsample_views(..., num_real_views=
  sinogram_shape[0])` silently truncates to the first hyperplane instead of
  the whole batch (`sinogram_shape[0]` is `nt`, not the batch size). This
  caused an all-NaN full-resolution reconstruction; see 4D_MACE progress.md,
  2026-08-25.

- Never benchmark on a shared node. The `ai` partition packs several jobs per node, and a
  4-GPU request lands on GPUs interleaved with someone else's work. Measured 2026-09-01:
  the same commit and configuration gave steady-state denoise of 272/421/752/312-329 s on
  four different nodes, while `prox` held at 194-206 s throughout. Any timing taken on a
  shared node is noise. Use `sbatch --exclusive`, and note that `--exclusive` makes all 8
  GPUs visible even when you asked for 4, so pin with `CUDA_VISIBLE_DEVICES` if the device
  count matters for the comparison. Check `SLURM_JOB_GPUS` and `squeue -w <node>` in the
  job log before trusting any number.
- Smoke tests need at least 25 time frames. Below that the dejitter's `[6, 3, 2]` bands
  overlap and zero the whole temporal spectrum: `--num_frames 5` or fewer returns an
  identically zero reconstruction that still completes, has the right shape, is all finite,
  and writes every log and the GIF. 12 frames keeps only 4 of 12 DCT coefficients. Check
  `min`/`max`/`nonzero` of the recon, not just `isfinite`, or pass `--no_dejitter`.

## Collaborators
<!-- Add names and roles -->
