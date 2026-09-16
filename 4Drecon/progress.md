# 4D Reconstruction — Progress

## Status
- 4D MACE: merged into mbirjax as `mj.MACE4DModel` (branch `4DCT_for_merging`); multi-GPU implementation, DCT dejittering integrated, null-space projection under investigation
- Single-view: literature search in progress
- MAR + multi-slice fusion: pipeline validated end to end on two real Lilly datasets; see `mar_fusion/progress.md`
- MACE4D port to mbirtorch (Greg's plan, `mbirtorch_plans/plans/features/mace4d/mace4d_migration_plan_v2.md`):
  Stages 0, 2, 3, 4, 5 done and pushed to `mace_4d_dev`; the decided questions of 2026-09-15 are being
  implemented in four increments, of which two are pushed (last commit `364e5d0`, 2026-09-16);
  Group 1 (questions 13 and 17) and Stages 6 to 8 wait for Greg's review

## Log

### 2026-09-16 (mbirtorch MACE4D port, the decided questions: increments a and b, and the cluster)
Went through the open questions in `mbirtorch_plans/plans/features/mace4d/decisions.md` with Ziyun and settled seven;
the answers and two corrections to that document are appended to it.  Corrections: the check against mbirjax cannot
pin one sigma_x through a public scalar, because mbirjax uses two values (0.003951 for XY-t volumes, 0.003823 for the
other two), so the m4d7 compare script keeps a subclass that pins per volume shape; and `nbr_weight_time` is the only
neighbor-weight knob, because a three-element `qggmrf_nbr_wts` would name x in one hyperplane volume and y in another.
Pushed to `mace_4d_dev`: `0b3eab0` (refuse a repeated GPU in a device pool, honor MBIRTORCH_NUM_DEVICES),
`1dec63b` (sigma_noise, sigma_x, sharpness, nbr_weight_time public; ONE sigma_x for the whole 4D volume, estimated
from the initial image read as a stack of frames; qggmrf_nbr_wts raises; denoiser stop threshold 0.2 -> 0.05 percent),
`364e5d0` (test fix, below).  Whole suite 1124 passed / 143 skipped on the Mac.
MEASURED, needs Greg: (i) the 0.05 threshold alone moves the m4d7 agreement from 7.045e-07 to 2.846e-03, because the
torch denoisers then run ~9.8 sweeps where mbirjax runs ~6.2; the compare script now sets the threshold back to
mbirjax's 0.2, as it already does for the partition advance and both warm starts, and the pinned variant reproduces
7.045e-07 on cpu and mps.  (ii) the single sigma_x estimated from frames is 0.00163754 against mbirjax's ~0.0039, i.e.
a 2.4x STRONGER prior (smaller sigma_x = stronger), which roughly doubles denoiser sweeps per call; with the tighter
threshold the sweeps reach the cap of 15.  Denoise dominates production runtime, so increment (a) may cost about a
factor of two in wall clock; Stage 8 must measure sigma_x, the threshold, the denoiser warm start and nbr_weight_time
together, since all four move the same quantity.  Note: nbr_weight_time 1.0 weights a frame neighbor 1.5x a spatial
one (time is in all three hyperplane volumes, each spatial direction in two); 2/3 is the isotropic point.  Verified
numerically with the library's own weight functions and checked against mbirjax's permutations.
CLUSTER (Gautschi): the `mbirtorch` conda env exists at `~/.conda/envs/mbirtorch` (python 3.11.16, torch 2.14.0+cu130,
mbirtorch installed editable against `~/PycharmProjects/mbirtorch`); the `mbirjax` conda env is GONE (deep_clean.sh
wipes ~/.conda).  Pulled `mace_4d_dev` to `364e5d0`; `greg_dev` untouched (`efeca90` before and after).  No reinstall
needed: editable install, pyproject unchanged.  FOUND: `test_fold_after_all_folds_the_agents_pieces` could never pass
on Python 3.11, because it keyed a dict by a tuple of slices and slices became hashable only in 3.12; the package
declares requires-python >= 3.11 and the Mac runs 3.14, so this surfaced only on the cluster.  CI does cover 3.11 but
runs only on pull requests into prerelease/main, and this branch has opened none.  Fixed in `364e5d0` by holding the
pieces as (region, output) pairs; the package itself never keyed anything by a region.  Suite submitted as job
16468227 on partition `ai` (script `~/mbirtorch_jobs/suite_py311.sh`).  Slurm notes: the `bouman` account has NO grant
on the `cpu` partition (AssocGrpGRES), and `ai` requires 14 CPUs per GPU.  The job points TORCHINDUCTOR_CACHE_DIR and
TRITON_CACHE_DIR at a job-scoped directory, because the caches under ~/.mbirtorch were built on 2026-08-28 by an
earlier torch and a stale cache makes the first compiled kernel fail; nothing was deleted.
NOT committed: everything in `mbirtorch_plans` stays local, since Ziyun has no push rights there.

### 2026-09-15 (mbirtorch MACE4D port, Stage 5: the tests)
Implemented from `stage5_prompt.md`, unstaged: tests/test_mace4d.py 14 -> 24 tests. Unit groups ported from mbirjax
(prior weights, device pool, construction, parameters, init cache); reconstruction group on the 3-frame run; one run
for the other settings (warm starts flipped, sigma_prox given, list prior weight, verbose); data-fit agent without a
stack; the ONE-FRAME EQUALITY GATE: 64-view Shepp-Logan 32x32x4, one full-rotation frame (fpr=1, overlap 1.0; a
21-view limited-angle frame does NOT converge: ref100 vs ref200 1.5%), reference recon(200) (vs recon(100) 3.8e-3),
start recon(30) 5.9% away, denoiser sigma = sigma_prox*sqrt(1.5) and sigma_x pinned via a test-only subclass;
NRMSE 3.0/1.6/0.82/0.45% at 10/20/30/40; Ziyun chose 40 iterations for the margin. Gate test 91 s alone.
One frame gives 1 denoiser subset by the rule, so the scan model keeps default partitions. Plan status row + review
page updated. Committed and pushed 2026-09-15 as ef13956.

### 2026-09-15 (mbirtorch MACE4D port, Stage 4 panel and fixes)
Opus panel of Stage 4 (4 reviewers, all "merge after fixes"): `mbirtorch_plans/plans/features/mace4d/stage4_panel_review.md`
+ `_reports.md`. Fixes taken one by one with Ziyun, committed and pushed 2026-09-15 as d7112b8 (mace4d.py, mace.py, test_mace4d.py):
(2) filter turns itself off with a warning when frames < period or the matrix is zero (Ziyun chose this over an error);
(3) compile-budget check is now a fresh-process test (mps: <=5 variants of 64; cpu: eager, toolchain errors only);
(5) data-fit agent adopts recon's own init image as its stack (plan 2.6 counts hold; +1 when caller supplies init);
(6) filter decided before any computation; (7) short last slab padded to the batch size (one compiled shape);
(8) `dejitter_verbose` logs "removes periods of 6, 3, 2 frames; 8 of 30 modes removed, 22 kept", also in run_info;
small items (task_log column `worker`, set_params returns nothing, pinned sigma denoiser, num_frames check first,
4 new tests) and the writing pass on code, tests, progress.md, m4d7 record.
NOT done: (1) partition redraw in denoise_stack — fix built (optional `partition` arg) then ROLLED BACK by Ziyun
(doubts about changing Stage 0 interface); decision 13 for Greg; class verified only at 1 subset/hyperplane volume.
(4) two-worker nondeterminism from prox_map partition draws on worker threads — documented as decision 17.
(6/7 small) private-attribute coupling and duplicated filter application left as is; Ziyun: filter functions stay in mace4d.py.
Whole suite rerun and m4d7 compare rerun after the fixes (see progress.md review page).

### 2026-09-14 (mbirtorch MACE4D port, Stage 4: MACE4DModel)
Implemented from `stage4_prompt.md`; on Ziyun's instruction committed as two commits and pushed to
origin/mace_4d_dev 2026-09-14: 7893f22 (filter move) and 8304b25 (MACE4DModel + tests). New `mbirtorch/mace4d.py` (MACE4DModel,
private _DataFitAgent, temporal_filter_matrix + apply_temporal_filter moved in from mace.py; mace.py keeps
a private `_filter_along_axis`), `tests/test_mace4d.py` (10 tests incl. the 3 moved filter tests), edits to
`mbirtorch/mace.py`, `mbirtorch/__init__.py` (two lazy exports now point at mace4d), `tests/test_mace.py`.
Results: 3-frame run passes on cpu+mps; two CPU workers == one worker exactly (rel 0) with one pixel subset;
data-fit filter path exact vs filtered stack; mps compiles with 3 variants of budget 64.
m4d7 mbirjax check (`plans/experiments/features/mace4d/m4d7_mace4d_check.md`): one-subset case with mbirjax's
shared XZ-t sigma_x -> 7e-7 after 3 iterations (both devices); own sigma_x -> 1.5e-3; default partitions ->
1.1e-1, which is mbirjax's own partition-redraw noise (two identical mbirjax prox calls differ by 9.3e-2 on
this 100-pixel problem).
Findings for Greg: (1) this Mac cannot compile CPU inductor kernels (clang finds no C++ std headers), so ALL CPU
tests of this repo here run eagerly; MPS compiles. (2) two worker threads on one MPS device segfault in Metal;
one worker per MPS device is fine. (3) mbirjax shares one denoiser between YZ-t and XZ-t (cache keyed by volume
shape; cone-beam frames are square in x,y), so XZ-t runs with the YZ-t sigma_x; the port computes its own.
Whole suite: 1104 passed, 143 skipped, 1 wall-clock geometry-viewer gate failed under -n 8 load (passes alone,
52 ms vs 100 ms; same flake as before the Stage 3 push).
Warm-start measurement (64-view Shepp-Logan, 3 frames, 60 iterations): prox warm start off -> loop never
converges (change stuck at 7%); denoiser warm start on -> sweeps 15 -> 3.4 iterations/volume but consensus
stalls at 0.04% change, 2.5% from the default's limit, because the 0.2% stop threshold suits a cold start.
Stage 8 experiment: tighter threshold with warm start on. Script in the session scratch dir, not a record yet.
Plan status row for Stage 4 and `progress.md` (review page) updated. Stage 5 waits for Greg's review.

### 2026-09-14 (mbirtorch MACE4D port, Stage 3: the shared MACE module)
Implemented from `stage3_prompt.md`: new `mbirtorch/mace.py` (temporal_filter_matrix + apply_temporal_filter,
resolve_device_pool, Task protocol, MACE class with the folding update / one worker thread per pool device /
shared queue / fold_after_all / state_dict-load_state_dict / context manager, `mace` wrapper, ForwardProxAgent
with device + partition_advance + use_warm_start, QGGMRFDenoiserAgent, HyperplaneAgent with per-worker stack
denoisers). Lazy exports added in `__init__.py` (module `mace` + 7 names; the wrapper stays `mbirtorch.mace.mace`
because the module takes the package attribute). `experiments/drunet/mace.py` and `agents.py` now re-export
from the package (DRUNetAgent stays there, its __call__ gained `iteration=0`). 29 tests in `tests/test_mace.py`
pass on cpu+mps (folding vs plain formulas 6e-7 on W; checkpoint round trip exact; two workers verified);
`run_qggmrf_gate.py` passes from the package at 0.00647 (unchanged value). Key finding while sizing the gate
test: a 30-iteration `recon` is 2.5% from a 100-iteration one on the 64-size problem and MACE overtakes it, so
the test uses a 100-iteration reference and starts from recon(30) -> 0.60% after 30 MACE iterations (~50 s).
Old drunet loop and new loop agree to 4 digits on the same problem. Defaults taken: denoise_stack's compiled
instance key left as is (Greg's ruling pending; the ['cpu','cpu'] tests ran without incident), one stack
denoiser per worker (keyed by thread+device), batch_size None = one task per orientation, change = inf at a
zero previous average, state_dict saves x_bar only (the accumulation buffer is zero between steps; deviation
from the plan's "two buffers", noted). Plan status row updated; nothing staged or committed.
Opus panel on Stage 3 (4 reviewers): all "merge after fixes". Five confirmed defects, all fixed the same day
with tests: run() handed out the average buffer that the next step zeroed (now copied into stable storage);
a failed step left the state corrupt (now marked inconsistent; step/state_dict raise until load_state_dict);
HyperplaneAgent warm start passed zeros on the first call with several tasks (flag set when the last task of
a call completes); the spread term allocated two region-sized temporaries under the lock (now chunked
outside it); multi-device model output crashed the agents (now refused by name). Also: denoise_stack
compile key changed to id(self) (the Stage 3 prompt default), Task exported, canonical devices, filter
refuses 1 frame, flaky two-worker denoiser test fixed. After fixes: 35 tests in test_mace.py, suite with
-n 8: 1099 passed. Synthesis `stage3_panel_review.md`, raw reports `stage3_panel_review_reports.md`, gate
log `results/stage3_qggmrf_gate_from_package.txt` (all untracked). Two decisions for Greg: auto_batch_size
in HyperplaneAgent vs explicit size in Stage 4; warn on mu/rho mismatch at resume.
Ziyun decided the first: MACE4DModel computes the batch size once per orientation from that orientation's
configured denoiser (`auto_batch_size()` on the pool's first device) and passes it to HyperplaneAgent;
the agent keeps None = one task per orientation (docstring now says so). Goes into the Stage 4 prompt.
Ziyun decided 2026-09-14: both `temporal_filter_matrix` and `apply_temporal_filter` move to mace4d.py
in Stage 4 (HyperplaneAgent keeps `filter_matrix`, applies it with a private helper); Greg to confirm.
Stage 4 prompt written 2026-09-14: `mbirtorch_plans/plans/features/mace4d/stage4_prompt.md` (untracked,
not staged). Step 0 is the filter move; steps 1-8 build MACE4DModel, the exit checks in tests/test_mace4d.py,
and the advisory m4d7 mbirjax check. Stage 4 implementation waits for Greg's review of Stages 0-3.
A review page for Greg summarizing Stages 0-3 (deliverables, test values, design choices, open decisions,
follow-ups) is at `mbirtorch_plans/plans/features/mace4d/progress.md` (untracked).
Docstrings shortened per Charlie's writing guide (mechanism removed from MACE, HyperplaneAgent,
ForwardProxAgent, temporal_filter_matrix, module docstring); 76 tests in the three affected files pass.
On Ziyun's instruction Stage 3 was committed as two commits and pushed to origin/mace_4d_dev:
42e0991 (module, tests, exports, drunet shims) and 2763640 (denoise_stack compile key by denoiser object).
Full suite before push: 1098 passed, 143 skipped, 1 failure = the geometry-viewer slider timing gate
(113 ms vs 100 ms) under the load of two concurrent runs; alone it passed at 50.6 ms; unrelated to Stage 3.
Second decision: load_state_dict warns (UserWarning) when saved mu/rho differ from the loop's and keeps
the loop's; tested. Third: keep the new trace definitions in the `mace` wrapper (spread and change
against the previous average); dated notes added to plans/nn_priors/mace_poc_findings.md and
multi_slice_fusion_findings.md saying pre-move traces are not comparable.

### 2026-09-14 (mbirtorch MACE4D port, Stage 2: frame construction and device helpers)
Implemented from `stage2_prompt.md`. `construct_time_frame_models` in `mbirtorch/utilities.py` (median
angle step, int(round()) span/stride, trailing views discarded, four ValueErrors, plus a clear refusal of
models without a 1D angle vector: MultiAxis, Translation); `gpu_devices`/`cpu_devices`/`default_devices`
beside `_resolve_device` in tomography_model.py. Tests in `tests/test_utilities.py`: 24-view case, a
parametrized pinned-literal test (240 views at 2.5 deg wrapped mod 360 AND monotonic -> same 9 frames;
36 views fpr=4 fof=1.5 -> [(0,14),(9,23),(18,32)]; 100 views fpr=5 fof=3 -> 3 frames of 60), error
paths, device helpers. Literals from the m4d5 generator run in mbirjax_ref
(`plans/experiments/features/mace4d/m4d5_time_frames_check.{py,md}`, results txt); torch reproduced all
five cases exactly. Defaults taken: no verbose suppression (mbirtorch prints nothing at construction),
helpers ignore MBIRTORCH_NUM_DEVICES, no package export. Surprises: fpr=48 on 15-deg views sits on a
0.5 rounding boundary and gives 24 one-view frames in both libraries; at default overlap a sub-view
stride is reported as a sub-view span (span check first). Plan status row updated. On Ziyun's
confirmation the three mbirtorch files were committed as 3c6236a and pushed to origin/mace_4d_dev. The
plans-repo files (m4d5 script, record, txt, plan status row, stage2_prompt.md) stay untracked for Ziyun/Greg.

### 2026-09-14 (mbirtorch MACE4D port, Stage 0 follow-up: sigma_x from whole volumes)
Greg's ruling on the 09-13 sigma_x finding: `denoise_stack` now sets its regularization parameters with a
new `QGGMRFDenoiser.auto_set_regularization_params_from_stack(stack)`: ~20 whole volumes chosen by the
`subsample_views` rule (all volumes up to 39, every P//20-th above), merged, estimator at stride one,
sigma_x floored at 1e-6 inside the method (Stage 4 applies no floor of its own). `denoise` keeps its row
subsample (golden test). 8 new tests; 41 pass in test_denoiser.py on cpu+mps; full suite passes.
m4d4 rerun with a 4th case (60 volumes of (6,16,16)): torch's own sigma_x now equals mbirjax's exactly for
P<=39 and the result difference at it fell from 4.6-7.9% to ~1e-7; for 60 volumes the 20-volume sample
gives sigma_x 0.32% low and a 2.8e-4 result difference. New outputs in `results/*_20260914.txt`; the
09-13 outputs kept. Plan v2 updated (Sections 2.1 with a dated note, 3.2, Stage 4, Section 5, status
table). Everything staged by name in both repos; nothing committed. Stage 0 still awaits review.
Later the same day, on Ziyun's instruction: committed and pushed. mbirtorch `mace_4d_dev`: 79d5321 (Stage 0)
and b80f6f5 (sigma_x follow-up), pushed to origin. mbirtorch_plans `main`: ef24e89 (Stage 0 record) and
47e39ef (follow-up record + plan), committed locally but NOT pushed: `ZiyunLiiii` has no write permission
on cabouman/mbirtorch_plans (403). Those two commits were UNDONE on Ziyun's instruction (git reset to the
base, files kept unstaged in the working tree; recoverable from the reflog), and main was fast-forwarded to
origin d23fad2. Rule from now on: Claude never commits in mbirtorch_plans; the mace4d files sit there as
one modified (plan v2) and ten untracked files for Ziyun/Greg to handle.
Opus panel (4 reviewers: correctness, design, tests, style) reviewed the pushed Stage 0. All four: "merge
after fixes"; no numerical defect. Synthesis in `mbirtorch_plans/plans/features/mace4d/stage0_panel_review.md`,
raw reports in `stage0_panel_review_reports.md` (both untracked, not staged). Three decisions for Greg:
(1) the whole-volume statistics have no point cap and peak at ~16x their input in host memory (measured
390 MB for a 24 MB stack; ~10 GB per orientation at 30 frames of 512^3; the shared estimator's np.where +
gather is the cause); (2) `maybe_compile(..., instance_key=str(device))` shares one compiled instance among
all denoisers on a device, which two workers on `['cpu','cpu']` will hit in Stages 3/4; (3) a denoiser
object cannot serve two workers (set_params on every call) -> Stage 3 needs one denoiser per worker.
Follow-up fixes: tests for sigma_noise=None and for the auto_batch_size sizing branch (reachable on CPU by
patching device_budget_bytes), stale row-subsample wording in the record's first section and compare.py:104,
stack_ell1 exact only below one chunk (docstring says "equals"), ~12 long sentences, nits.
Also wrote the Stage 2 prompt, `mbirtorch_plans/plans/features/mace4d/stage2_prompt.md` (untracked; Ziyun
stages and commits on their own decision):
frame construction (`construct_time_frame_models` in utilities.py) and the device helpers, with the m4d5
view-slice check against mbirjax. Open points it carries with defaults: drop the verbose suppression
(mbirtorch prints nothing at construction), gpu_devices ignores MBIRTORCH_NUM_DEVICES, no package export yet.

### 2026-09-13 (mbirtorch MACE4D port, Stage 0)
Implemented Stage 0 of the v2 plan on mbirtorch branch `mace_4d_dev`: `qggmrf_gradient_and_hessian_batched`,
`vcd_subset_denoiser_batched`, `QGGMRFDenoiser.auto_batch_size`, `QGGMRFDenoiser.denoise_stack`, plus
`stack_ell1` and the batch-size rule in `_memory_ledger.py`; 15 new tests in `tests/test_denoiser.py`.
Results: `denoise_stack` vs a loop of `denoise` agrees to 5.9e-8 (gate 1e-6) on cpu and mps with equal
per-volume iteration counts; whole suite 1051 passed, 143 skipped. Check against mbirjax 0.7.3
(`plans/experiments/features/mace4d/m4d4_denoise_stack_check.md`): worst 2.0e-7 against a gate of 1e-3,
partitions and iteration counts identical.
Two findings raised for Greg: (1) CPU float rounding in the elementwise qGGMRF chain differs between a 3D
and a 2D tensor when the element count is not a multiple of 8 (about 5e-8), so exact CPU equality is not
achievable; MPS is bitwise. (2) The row-subsampled `sigma_x` path the plan specifies for the hyperplane
agents gives 1.6-2.2x mbirjax's whole-stack `sigma_x` on the test ramp, moving the denoiser output by 5-8%.
The estimator itself matches mbirjax exactly on the whole stack; only the rows differ. This affects the
Stage 4 expected agreement (plan says 1e-3 to 1e-2). Interface decisions to confirm: `auto_batch_size`
returns None on cpu/mps (whole stack) and has an `init_supplied` flag.
Files staged by name in both repos; nothing committed.

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

### 2026-09-03 (Opus panel review of the two PRs)
Three-member Opus panel reviewed mbirjax PR #228 (4DCT_for_merging -> prerelease) and
mbirjax_applications PR #49 (adding_4d_script -> prerelease). All 35 tests pass; no BLOCKERs.
Correctness reviewer: merge-ready. API reviewer: merge after fixes — wants a maintainer decision
on `set_device_pool` vs `configure_devices` naming, and explicit acknowledgment that
`save_volume_as_gif` breaks positional callers (`(vol, name, 0, 1)` now means frame_axis=0,
slice_axis=1). Tests reviewer: `_dejitter_4d_dct` has zero coverage and its imports in
test_mace4d.py are dead (lines 15, 24); constant-init and num_frames<1 error paths untested.
Other notables: dejitter with small num_frames can zero the whole spectrum silently (no guard);
MACE4DModel uses print() instead of the per-instance logger this PR adds. PR #49: merge-ready
(nits: ./logs cwd-relative, ".tgz" help text). Cross-PR check: driver runs against clean
prerelease+#228, no dependence on other local branches.

Ziyun's decisions on the panel findings (2026-09-04): no dejitter tests and no small-num_frames
guard — a better dejitter is in the works, so don't over-invest in something that may be replaced;
`set_device_pool` name stays (deliberately different from `configure_devices` to avoid conflating
task dispatch with array sharding). Do NOT re-raise these. Both remaining items done 2026-09-04: dead imports removed from
tests/test_mace4d.py (commit a2d9488, 17 tests pass, pushed), and the PR #228 description's
save_volume_as_gif bullet expanded (via Chrome) to spell out the positional-arg break, the
vmin/vmax default change, and the 3D layout change. PR #228 has cabouman and gbuzzard as
requested reviewers; panel follow-ups are complete.
### 2026-09-02 (dejitter output silenced)
`MACE4DModel._dejitter` passed `verbose` to `_dejitter_4d_dct`, not `dejitter_verbose`.
`dejitter_verbose` was declared in the param list and defaulted to 0 but never read -- dead since
the merge. Since `_dejitter` runs once on the prox stack plus once per prior orientation every
iteration, a driver running at the normal `verbose=1` reprinted the same mode list four times per
iteration, burying the iteration progress. Now keyed to `dejitter_verbose`, so the default is
silent and the detail is still reachable with `set_params(dejitter_verbose=1)`.
Measured on a 2-iteration toy recon: 16 dejitter lines out of 53 total before, 0 out of 13 after.

### 2026-09-02 (nt -> num_frames)
Renamed the `MACE4DModel.nt` attribute to `num_frames` (Ziyun: "i dont like the name nt").
It now shares a name with the constructor argument, which reads as request vs. result: the
argument asks for at most N frames (or None for all), the attribute reports how many there are.
The docstring says so explicitly so the two are not conflated.
Also renamed the `(nt, nx, ny, nz)` shape notation in mace4d.py docstrings/comments, since `nt`
would otherwise have no referent, and dropped the now-redundant parenthetical from the
`run_info.txt` key `time frames (nt)` -> `time frames`.
NOT renamed: `save_volume_as_gif` still documents `(num_times, nx, ny, nz)`, its own convention.
Call sites updated: `tests/test_mace4d.py` (2), `mbirjax_applications/nsi_4d/Lilly_recon_4d.py`
(3), `4DCT/recon_4d.py` (2), `4DCT/README.md` shape line.
Verified: 27 replacements in mace4d.py, no bare `nt` left in any touched file,
`pytest tests/test_mace4d.py tests/test_utilities.py` = 31 pass, and the Lilly driver runs end to
end against the stub, writing the recon and all three plane GIFs.

### 2026-09-02 (Sphinx docs for MACE4DModel)
Added `docs/source/usr_mace4d.rst` and registered it, following the brief half of
`4DCT/plans/mbirjax_docs_plan.md` (Ziyun asked for brief and compact, so the demo script,
`usr_parameters.rst` section, `usr_multi_gpu.rst` subsection, index feature bullet and release
notes from that plan are NOT done). Modeled on `usr_denoising.rst`: prose only where autodoc
cannot generate it, then autoclass/automethod.

The prose covers the three things no docstring says: the frame decomposition and that `nt`
follows from scan length rather than being set; the agent structure (one prox_map per frame plus
three batched qGGMRF denoisers on the XY-t/YZ-t/XZ-t hyperplanes) and the DCT-I dejitter; and a
note that `weights=None` means unit weights while `transmission_root` is the validated choice,
which is the trap a reader would otherwise hit.

Also fixed the stale `save_volume_as_gif` sentence in `usr_utilities.rst`, which still described
the pre-redesign fixed-axis behavior. `construct_time_frames` / `construct_time_frame_models` are
documented on the 4D page only, not also under Utilities, to avoid duplicate autodoc targets.

**Not verified by a Sphinx build**: no environment on this Mac has sphinx plus the mbirjax docs
extras, and installing them was not mine to do. Checked instead by script: all 7 autodoc/role
targets import and resolve, no broken `:ref:` anywhere in `docs/source`, both cite keys exist in
`refs.bib`, page in the toctree and bullet list exactly once. Still open: whether the build emits
an unresolved-reference warning for `MACE4DParamNames` (plan section 1). It should not, since
`autoclass` without `:members:` never renders the `get_params` overload, but only a build proves
it. To check: `pip install -e ".[docs]"` then `cd docs && make clean html`.

### 2026-09-02 (gif writer redesign)
Redesigned `save_volume_as_gif` in `mbirjax/utilities.py` to take `frame_axis` (3D and 4D) plus
`slice_axis` / `slice_index` (4D only), reversing part of the same-day cut to dispatch-on-ndim.
The cut's premise was that a caller could index and transpose before calling; that fails for 4D
because the frame titles are generated inside the function and cannot be recovered by
pre-transposing. `titles` and `cmap` stayed out: expose what to show, not how to style it.

**Design points**
- Reduction is `volume[..., slice_index, ...]` then `np.moveaxis(frame_axis -> 0)`. Both are
  views, so the ~19 GB Lilly 4D recon is never copied. No transpose of the displayed pair.
- Dropping one axis and moving another to the front leaves the surviving two in ascending order
  automatically, so the `slice_viewer` layout rule holds for free in all 12 axis combinations.
- `frame_axis` is given in the ORIGINAL numbering, so it must shift down by one when it sits
  above `slice_axis`. That renumbering is the only real trap; it lives in one expression.
- `frame_axis` cannot default to a literal 0: `slice_axis=0` (fix time, walk the volume of one
  time frame, the x-y-z case) would collide. It defaults to 0, or 1 when axis 0 is held fixed.
  Ziyun tried the literal 0 and it made the x-y-z case raise; restored.
- No range/type checking helper: numpy already raises for an out-of-range axis or index, so those
  checks were redundant (Ziyun: "too safe"). The one thing worth keeping is wrapping an in-range
  NEGATIVE axis, since the equality check, the renumbering and the title lookup all assume a
  non-negative number. Without it `slice_axis=-1` silently looped y while the title said t.
  Wrap by adding ndim, never a modulo, so an out-of-range axis stays out of range for numpy.
- The frame writer is nested inside `save_volume_as_gif`; it closes over nothing, so this is
  organizational only.
- `slice_axis` defaults to 1, which is what keeps the two existing 4D callers byte-identical.
- 3D with `slice_axis` raises; it would leave a single image, not a movie.

**Behavior change**: 3D output now carries a frame title (e.g. `x = 12`) where it had none, since
a selectable frame axis makes an untitled movie ambiguous. 4D titles are unchanged.

**Verification** (no tests added -- commit `b9db9c8` had removed the four GIF tests, so the
prerelease branch has none, and Ziyun's rule is not to add retroactive coverage): sha256 equality
against the pre-change writer for the 4D default in both the pinned and auto vmin/vmax paths; all
12 axis combinations give the right frame count; default resolution for `slice_axis=0`; negative
axes; view-not-copy assertion; six error paths. `pytest tests/test_utilities.py tests/test_mace4d.py`
= 31 pass.

### 2026-09-02 (device pool rename)
Renamed `MACE4DModel.configure_devices` -> `set_device_pool` in mbirjax (`4DCT_for_merging`).
Ziyun's reasoning: `MACE4DModel` is a `ParameterHandler`, not a `TomographyModel`, so the shared
name was a coincidence with no base-class contract, and the two mechanisms differ (sharding one
array vs. dispatching whole tasks to a pool of devices, one worker thread each). "Pool" over
"list" because the method describes the role, not the container, and callers pass ints or
platform strings more often than lists. The argument forms are unchanged and the docstring says
so. The per-frame `ConeBeamModel` / `QGGMRFDenoiser` pinning calls keep `configure_devices`
(those are real `TomographyModel` methods). Updated: `tests/test_mace4d.py`,
`mbirjax_applications/nsi_4d/Lilly_recon_4d.py`, `4DCT/recon_4d.py`, `4DCT/README.md`,
`4DCT/plans/mbirjax_docs_plan.md`. Left as historical record: `4DCT/plans/mbirjax_merge_plan.md`,
dead `4DCT/mace4d.py`. `pytest tests/test_mace4d.py`: 17 pass.

### 2026-09-02 (later)
Renamed `mbirjax_applications/nsi_4d/Lilly_recon.py` -> `Lilly_recon_4d.py` (commit 22f0f89) and
aligned its outputs with the 3D `nsi/Lilly_recon.py` so Lilly finds the 4D recons the same way:
- `--output_path` defaults to `./output/lilly`; logs go to `./logs/<stem>/` (run_info, timing, task csv).
- One stem names everything: `recon_4d_<dataset_tag>_voxel_pitch_<um>um_frames_<nt>` (Ziyun chose
  to always append the frame count rather than only on truncation). Recon `<stem>.npy`,
  GIF `<stem>.gif`, init cache `output/lilly/init/<stem>/init_recon.npy`. Wall time dropped from the
  filename (still in run_info.txt).
- Init cache keyed by stem fixes a latent hazard: `_load_cached_init` checks shape only, so two
  datasets with the same geometry shared one `output/init/init_recon.npy`.
- `Lilly_recon_4d.py` now writes ALL THREE spatial planes as GIFs by default, each playing over
  time. Rationale: the recon takes hours, the GIFs take seconds, and picking a single plane up
  front means paying for another full run to see a different one. `--gif_slice_axis` (0=t, 1=x,
  2=y, 3=z) narrows it to one and can fix time instead, which walks one frame's volume;
  `--gif_slice_index` (default middle) needs that flag and argparse-errors without it.
  The fixed axis and index go in the GIF name (`<stem>_x130.gif`), so runs differing only in the
  plane shown do not overwrite each other. The index is resolved in the driver rather than left
  to the library default, because the name needs it. Both flags are hidden from the shell script
  and listed in its Advanced comment.
- Shell script: tee log moved to `~/mbirjax_notes/Lilly_4d_ds1_run.log`; `--output_path` hidden (still a Python flag, listed in the Advanced comment); the `cd "$(dirname ...)"` line removed, so like the 3D scripts it runs from the script's directory and writes `./output/lilly` and `./logs` there.
- Recon stays `.npy`: `mj.export_recon_hdf5` is 3D-only (unpacks 3 dims, fixed (2,1,0) transpose).
  Extending it to 4D is a possible follow-up if Lilly wants `.h5` parity.
- Not touched: `4DCT/recon_4d.py` and `4DCT/plans/lilly_interface.md` still describe the old
  `output/recon_4d_<time>h.npy` layout; `nsi_4d/simplify_cli_plan.md` lines 1, 19, 157 still say
  `Lilly_recon.py`. Verified with a stubbed end-to-end run (three argv cases), not on real data.

### 2026-09-02
Merged the two GIF writers in `mbirjax/utilities.py` into one.  `save_4d_volume_as_gif` is gone;
`save_volume_as_gif(volume, filename, vmin=None, vmax=None, fps=5)` dispatches on `ndim` and
takes no axis arguments: a 3D volume steps over axis 0, and a 4D volume plays over time at the
middle slice of axis 1, titled with the slice and time index.

**Why the 2026-08-31 split was wrong.**  That decision held that a 3D and a 4D writer cannot
share a function because axis 0 means different things in each.  The real conflict was narrower.
For the same physical plane, `save_4d_volume_as_gif` and `slice_viewer` both display the two
surviving axes in ascending order (lower axis vertical); only `save_volume_as_gif` transposed
them.  `slice_viewer`'s `_get_perm_from_slice_ind` is `list({0,1,2} - {s}) + [s]`, which is that
same ascending rule.  So the outlier was the older 3D writer, not the 4D semantics.  Once 3D
adopts the ascending order the two cases share one display path, and the split has no reason to
exist.

Merging was cheap only because `save_4d_volume_as_gif` had never reached `main` -- it existed
only on `4DCT_for_merging`, with callers we own.  After that branch lands it would have been a
public name.  `save_volume_as_gif` has been public since v0.6.5 but had no callers anywhere in
mbirjax (either branch), its docs, mbirjax_applications, or 4DCT.

**Keep the interface small.**  The first version exposed `frame_axis`, `slice_axis`,
`slice_index`, `titles` and `cmap`, which was more surface than the two call sites need.  Cut
back to dispatch-on-`ndim`; anyone wanting a different slice or axis order transposes or indexes
the array before calling.

**Behavior changes**
- 3D output is transposed relative to before (now ascending, matching `slice_viewer`).
- `vmin`/`vmax` default to the range of the frames actually shown, not a fixed (0, 1), which was
  a poor window for attenuation data around 0.01-0.1.  Computed once over the whole stack, so
  intensity changes along the movie stay visible, and a hot voxel outside the displayed slice
  cannot darken it.  Guarded: NaNs ignored, no finite values falls back to (0, 1), and a
  zero-width range widens as `slice_viewer` does.
- 4D output is byte-identical to the old writer -- verified by sha256 against the pre-merge
  function reconstituted from git, with `vmin`/`vmax` pinned.

**Fixed in passing**
- Dropped the `try/except ImportError` around `imageio`.  It is a declared dependency as of
  `f6262ca`, and the guard is what turned a missing install into a run that finished normally
  and silently wrote no GIF.
- `mimsave` now gets `duration=1000/fps`; `fps=` is deprecated in imageio 2.28+ (confirmed on
  2.37.4).  It still produced correct 200 ms frames, so this was a warning, not a live bug.
- One figure reused across frames instead of one per frame: 6.2 -> 4.1 ms/frame measured, and it
  guarantees every frame is the same size, which a GIF requires.  The RGBA buffer is reused on
  each draw, so frames must be copied out, not viewed.

**Callers updated**: `mbirjax_applications/nsi_4d/Lilly_recon.py:174` and `4DCT/recon_4d.py:186`
drop `slice_axis=1`, which is now automatic; the `hasattr` check in
`4DCT/plans/cluster_test_prompt.md`; the Step 4 note in `4DCT/plans/mbirjax_merge_plan.md`.
`save_volume_as_gif` added to `docs/source/usr_utilities.rst`, where neither writer had appeared.

**Tests**: `TestSave4DVolumeAsGif` -> `TestSaveVolumeAsGif`, held at the same four tests, each a
successor to one that existed or a pin on behavior changed here: both shapes write a file and the
3D layout is ascending, not transposed; a 4D volume reads only the middle x slice (changing a
hidden slice leaves the GIF identical, changing the shown one does not); the data-range defaults
including a constant volume; bad arguments raise.  No retroactive coverage was added for the
previously untested 3D writer, per Ziyun's rule that an untested function was a deliberate
developer choice -- noting against it that `f6262ca` records that same gap as why the 3D writer's
silent no-op went unnoticed.  Verification was `pytest tests/test_utilities.py` (25 pass) plus the
sha256 comparison against the pre-merge writer, not a full-suite run.

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
