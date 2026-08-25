# 4D MACE — Progress Log

## Current Status
Repo refactored to NSI-style structure with MACE4DModel class. Lilly production scripts ready. Multi-GPU implementation fully preserved. Null-space projection under investigation.

## Log (newest first)

### 2026-08-25

- Found and fixed a correctness bug in the refactored `mace4d.py`: the batched
  qGGMRF denoiser could produce an all-NaN reconstruction at full resolution.
  Cause: `_configure_denoiser` called mbirjax's `auto_set_regularization_params()`
  unchanged, which subsamples down to the first `nt` "views" of whatever array
  it is given. For the merged multi-hyperplane batch this code passes it, that
  silently used only the first hyperplane instead of the whole batch. For the
  YZ-t and XZ-t orientations, that first hyperplane sits outside the phantom,
  so `sigma_x` collapsed to zero and the qGGMRF solver produced NaN for the
  whole batch. Fix: compute `sigma_x`/`sigma_y` directly on the full batch and
  floor `sigma_x` at `1e-6`. Verified on an isolated repro (100% NaN to 0) and
  the full 97-frame production run (0 NaN across 4.77B voxels). Committed to
  the `refactor` branch (`0433fcb`), not yet merged to `main`.
- Measured the task-queue refactor's real speedup on the full-resolution
  phantom (97 frames, no downsampling, 4 H100s): 2.91x per-iteration speedup
  over the old fixed-agent-per-GPU script (1238 s to 425 s), well short of
  the roughly 9x seen at smoke scale. Direct profiling found the cause:
  dejitter and the ADMM consensus update run single-threaded on the CPU,
  after a barrier on all 4 GPUs, and cost roughly 210 s per iteration
  regardless of GPU scheduling. That cost was small at smoke scale and
  dominates at full scale. Not yet fixed.
- Tried recalibrating the scheduler's `_DENOISE_COST_PER_PLANE` constant from
  a flat `0.015` to measured per-orientation values (`0.082`/`0.149`/`0.149`).
  The change made iteration time worse, not better: denoise tasks ran roughly
  1.7-2x slower than their own calibration baseline, for a reason not yet
  understood (candidates: GPU memory/batch-size effects from
  `_auto_batch_size`, or node-to-node hardware variance). Reverted; the
  committed scheduler still uses the flat `0.015`.
- Lesson learned the hard way: never reuse one `OUTPUT_PATH` across
  differently-configured test runs. `recon()` truncates `timing_log.csv` and
  `task_log.csv` on every run, so a later run silently destroys an earlier
  run's logs. Now use one output directory per run.
- Full writeups, with data and figures, are in the 4DCT repo output directory:
  `run_notes.md`, `sigma_x_problem.md`, and `parallelization_report.md` under
  `/home/li5273/Desktop/data/output/2026/0827/test_4D_repo/`.

### 2026-08-14
- Refactored 4DCT repo to mirror mbirjax_applications/nsi layout
- New top-level files: `utils.py`, `model_4d.py`, `lilly_recon.py`, `dev_recon.py`, `run_lilly.sh`
- `MACE4DModel` class wraps serial and parallel MACE; single `recon(parallel=True/False)` entry point
- All multi-GPU threading code (ThreadPoolExecutor, configure_devices, W_snap, thread-local cache) preserved verbatim in `_recon_parallel`
- `lilly_recon.py`: argparse CLI with 8 flags; algorithmic hyperparameters hard-coded; `--resume` loads saved init_image
- `dev_recon.py`: all params as Python variables; `USE_SAVED_INIT_IMAGE`, `time_range`, `parallel`, `device_indices` all exposed
- `run_lilly.sh`: edit `DATA_PATH`, run `bash run_lilly.sh` — Lilly operator entry point
- `plans/refactor_plan.md`: full design doc with interface discussion (what to expose vs. hard-code)
- Old `4DMACE_serial/` and `4DMACE_multi_threads/` kept untouched as reference

### 2026-08-07
- Shared full multi-GPU MACE script
- DCT-I dejittering (period=6, harmonics=True) applied in forward agent and all prior agents
- Identified issue: direct dejitter may violate AX = y
- New idea: null-space projection — x + (I - A⁺A)(Px - x) — not yet implemented
