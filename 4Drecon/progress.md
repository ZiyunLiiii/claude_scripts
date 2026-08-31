# 4D Reconstruction — Progress

## Status
- 4D MACE: merged into mbirjax as `mj.MACE4DModel` (branch `4DCT_for_merging`); multi-GPU implementation, DCT dejittering integrated, null-space projection under investigation
- Single-view: literature search in progress
- MAR + multi-slice fusion: pipeline validated end to end on two real Lilly datasets; see `mar_fusion/progress.md`

## Log

### 2026-08-31
- Merged the 4D MACE code into mbirjax, following `4DCT/plans/mbirjax_merge_plan.md`
  - `mbirjax/mace4d.py`: `MACE4DModel(ParameterHandler)`. Constructor takes `ct_model` + frame
    params (no data); `recon(sinogram, weights=None, init_recon=None, max_iterations=10,
    stop_threshold_change_pct=0.2, init_dir=None, log_dir=None)` returns `(recon, recon_dict)`
  - `mbirjax/utilities.py`: `construct_time_frame_models` (model-only primitive) and
    `construct_time_frames` (wrapper that also slices the sinogram); `save_volume_as_gif` gained
    `titles` and `fps`
  - `mbirjax/parameter_handler.py`: loggers are now per instance, not per class — fixes a real
    race when models run concurrently in threads. Replaces the old `_silence_model_logging` hack
  - `weight_type` is gone from the model: `weights=None` means unit weights, and
    `transmission_root` is applied by the caller with one `gen_weights` call
  - 41 CPU tests added across `test_mace4d.py`, `test_utilities.py`, `test_logging.py`
  - 4DCT `recon_4d.py` now drives `mj.MACE4DModel`; `--max_mace_itr` renamed to
    `--max_iterations`, and `--weight_type` added (default `transmission_root`)
- Two defects found by the port: a constant `init_recon` divided by zero inside the qGGMRF
  setup (now reports the cause), and the pre-merge prior-weight test compared floats exactly
- Still unverified: multi-GPU concurrency (tested only on 2 virtual CPU devices), agreement
  with a pre-merge full-resolution reference, and whether the new default
  `stop_threshold_change_pct=0.2` stops a production run before 10 iterations
- Sphinx docs plan written to `4DCT/plans/mbirjax_docs_plan.md`; not yet implemented

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
