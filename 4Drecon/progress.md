# 4D Reconstruction — Progress

## Status
- 4D MACE: working multi-GPU implementation, DCT dejittering integrated, null-space projection under investigation
- Single-view: literature search in progress
- MAR + multi-slice fusion: pipeline validated end to end on two real Lilly datasets; see `mar_fusion/progress.md`

## Log

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
