# 4D Reconstruction — Progress

## Status
- 4D MACE: merged into mbirjax as `mj.MACE4DModel` (branch `4DCT_for_merging`); multi-GPU implementation, DCT dejittering integrated, null-space projection under investigation
- Single-view: literature search in progress
- MAR + multi-slice fusion: pipeline validated end to end on two real Lilly datasets; see `mar_fusion/progress.md`

## Log

### 2026-09-01
Validated the mbirjax merge on real data and real GPUs. **The merge is sound: the
reconstruction is numerically unchanged and there is no performance regression.** The one
thing still not established is voxel-level agreement with the pre-merge output.

**What passed.** mbirjax's own tests (58, on CPU); the real NSI preprocessing path at
25 frames on one H100; multi-GPU concurrency at 25 frames on four H100s (`task_log.csv`
shows 4 distinct devices with work spread 12/16/14/14 over 56 tasks, no hang); and full
resolution, 99 frames, 10 iterations.

**The performance scare was node contention, not code.** Three full-resolution runs of the
same commit gave steady-state denoise times of 421 s (`h004`), 752 s (`h013`, sharing the
node with four other jobs), and 312-329 s (`h011`, `--exclusive`) against the Aug-25
reference's 272 s. `prox` stayed flat at 194-206 s across all of them, and within the
contended run denoise swung 594-1188 s while prox held to a 2% spread — a variation no
source-level difference can produce. On the exclusive node the run finished in 1:04:37
against the reference's 1:00:34, with makespan 147-158 s against 152-160 s. Denoise is the
phase exposed to a shared node because of its memory traffic; prox stays resident on its
own GPU.

A code audit agreed independently: `qggmrf.py` and `tomography_model.py` are untouched
since v0.7.1, and comparing the two `mace4d.py` files at AST level (docstrings stripped)
found the entire denoise path and task scheduler byte-identical — 11 functions including
`_get_qggmrf_denoiser`, `_configure_denoiser`, `_batched_hyperplane_denoise`,
`_denoiser_wrapper`, `_run_denoise_task`, `_run_task_set`, `_assign_tasks`. The 13
functions that do differ differ only in accessor style (`self.x` -> `get_params('x')`),
renames, and the sinogram-at-`recon()` API split.

**Frame count differs from the reference: 99 now, 97 then.** Both from the same 2400-view
sinogram. The scanner metadata (`.nsipro`: `angleStep 2.5`, `Rotation range 6000`,
`Number of projections 2400`) gives 2.5 deg/view over 16.7 revolutions, so
`frames_per_rotation=6` + `frame_overlap_factor=2.0` is a 120 deg / 48-view frame and 99
frames. 97 frames requires 96 views/frame, i.e. an effective overlap factor of 4.0 — a
240 deg frame. **2.0 is the value consistent with the scanner geometry and with both
drivers' defaults; the reference run's 97 remains unexplained**, since its own
`run_info.txt` recorded a 120 deg span and the frame-construction arithmetic is identical
in every version of the code. Consequence: the two recons cannot be differenced, so the
NRMSE comparison against the pre-merge output was never done.

**Still open**
- Voxel-level agreement with the pre-merge recon (needs matched frame geometry).
- Which overlap factor is intended for production — 2.0 halves the temporal integration
  window relative to the Aug-25 reference. This is a modelling decision, not a bug.
- Full-resolution peak RSS is ~484 GiB against a 503 GiB limit at 56 CPUs (~4% headroom),
  measured on two completed runs. More frames or less `auto_crop` will OOM, hours in.

### 2026-08-31
Merged the 4D MACE code into **mbirjax**, following `4DCT/plans/mbirjax_merge_plan.md`.
mbirjax branch `4DCT_for_merging` (6 commits, `ba42ee6`..`a9e13e8`); 4DCT branch
`refactor_for_mbirjax` (7 commits, `1f07db6`..`d76fd42`).

**What moved**
- `mbirjax/mace4d.py`: `MACE4DModel(ParameterHandler)`. Operator in the constructor
  (`ct_model` + `frames_per_rotation`, `frame_overlap_factor`, `num_frames`), data at
  `recon(sinogram, weights=None, init_recon=None, max_iterations=10,
  stop_threshold_change_pct=0.2, init_dir=None, log_dir=None)` -> `(recon, recon_dict)`.
  `configure_devices()` replaces the old `devices=` argument to `recon`.
- `mbirjax/utilities.py`: `construct_time_frame_models(model, ...)` (model-only primitive,
  returns models + view slices) and `construct_time_frames(sinogram, model, ...)` (wrapper
  that also slices the sinogram, as NumPy views).
- `mbirjax/utilities.py`: new `save_4d_volume_as_gif(volume, filename, slice_axis=1,
  slice_index=None, ...)`. Axis 0 is time; `slice_axis` picks the fixed spatial plane.
  `save_volume_as_gif` is left **unchanged** — its axis 0 is spatial and shown transposed,
  so folding the 4D behavior into it would have misled existing 3D callers. This reversed
  Step 4 of the merge plan.
- `mbirjax/parameter_handler.py`: model loggers are now per instance, not per class. Fixes a
  real race — concurrent models rebuilt each other's handlers, and one thread could close a
  log file another was writing to. Replaces the old `_silence_model_logging` hack.

**Interface changes that break old commands**
- `--max_mace_itr` -> `--max_iterations`; new `--stop_threshold_change_pct` (default 0.2, so
  a run can now stop before 10 iterations — pass 0 to force all of them).
- `weight_type` is gone from the model: `weights=None` means unit weights, as in
  `TomographyModel.recon`. The driver applies `transmission_root` itself via the new
  `--weight_type` flag, so defaults reproduce the old behavior.
- Init cache renamed `init_image.npy` -> `init_recon.npy`. An old cache is not found and is
  recomputed (15-20 min) unless renamed.

**Defects found by the port**
- A constant `init_recon` (e.g. all zeros) gave a zero noise estimate that divided through to
  the qGGMRF forward-model constant — surfaced as `ZeroDivisionError` three calls deep.
  `recon` now checks and names the cause.
- The pre-merge prior-weight test compared floats exactly; `[0.1, 0.2, 0.3]` normalizes to
  `0.3999999999999999`.
- `num_frames=0` emptied the frame list and failed later on `model_list[0]`. Rejected at
  construction now.

**Verification**
- 44 new CPU tests; 58 pass across `test_mace4d.py` (29), `test_utilities.py` (25, 11 new),
  `test_logging.py` (4).
- Threaded multi-device path runs on 2 virtual CPU devices, asserting both devices ran tasks.
- `recon_4d.py`'s `main()` runs end to end against a stubbed NSI preprocessor.
- Full mbirjax suite: 394 pass, 4 fail. The 4 failures (`test_qggmrf` alpha_derivative /
  loss_and_gradient, `test_pallas_kernels` cone_fwd_matches_xla x2) reproduce identically at
  base commit `b74ffc8` — pre-existing, not from this work.

**Still unverified** — see `4DCT/plans/cluster_test_prompt.md` for the staged cluster plan
- Multi-GPU concurrency: only 2 virtual CPU devices tested, and the deadlock that the device
  pinning prevents cannot occur on CPU.
- Agreement with a pre-merge full-resolution reference recon.
- Whether the new default `stop_threshold_change_pct=0.2` ends a production run early.

**Docs**
- `4DCT/plans/lilly_interface.md` updated to the merged interface (it still described
  `--max_mace_itr`, `init_image.npy`, and a weighting fixed inside the model).
- Sphinx docs plan written to `4DCT/plans/mbirjax_docs_plan.md`; **not yet implemented**.
- `4DCT/mace4d.py` and `4DCT/tests/` are now dead code, kept and labeled in the README;
  deletion is an open decision.

### 2026-08-27 to 2026-08-31
- Built and validated the MAR + multi-slice fusion pipeline (new sub-project) on `Autoinjector_HighRes_Horizontal` and `Connected_Autoinjector_Vertical`. Full log, gotchas, and open questions in `mar_fusion/{progress,rules,goal}.md`.

### 2026-08-17
- Added `compute_bin_params(data_path, angle_span_per_recon, angle_overlapping)` to `utils.py`
  - Finds the `.nsipro` file via glob, parses `<angleStep>` from `<Object Radiograph>` section (same approach as mbirjax NSI preprocess)
  - Returns `views_per_bin = round(span/step)`, `stride = round((span-overlap)/step)`
  - Replaces hardcoded `views_per_bin=48, stride=24` in both `Lilly_recon.py` and `dev_recon.py`
  - Validated: 120° span, 60° overlap, 2.5°/view → views_per_bin=48, stride=24 ✓

### 2026-08-07
- 4D MACE script shared; DCT-I dejittering (period=6, harmonics) applied in forward + prior agents
- Issue identified: direct dejitter may violate AX = y → null-space projection idea: x + (I - A⁺A)(Px - x)
- Single-view project scoped: plume in pork belly, fixed-angle + steady-state CBCT reference
- Created Claude_scripts/4Drecon tracking folder; Lilly proposal draft started in Overleaf
