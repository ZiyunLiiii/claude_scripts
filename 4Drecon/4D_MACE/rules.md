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

## Collaborators
<!-- Add names and roles -->
