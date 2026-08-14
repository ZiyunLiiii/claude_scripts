# 4D MACE — Progress Log

## Current Status
Repo refactored to NSI-style structure with MACE4DModel class. Lilly production scripts ready. Multi-GPU implementation fully preserved. Null-space projection under investigation.

## Log (newest first)

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
