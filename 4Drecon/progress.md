# 4D Reconstruction — Progress

## Status
- 4D MACE: merged into mbirjax as `mj.MACE4DModel` (branch `4DCT_for_merging`); multi-GPU implementation, DCT dejittering integrated. 2026-09-24: the rotating jitter of Phantom_30s_Run1 is a det_channel_offset error of -1.28 channels (confirmed by a calibration sweep); removing null-space content hurts (static test), so "null-space projection dejittering" is not the way to remove it; 2026-09-25: with no filter, correcting only the offset takes the 4D wobble from 0.720 to 0.059 voxel (nominal + DCT 0.126), with no harmonic-1 error left on static edges; write-up `offset_justification.tex` complete (no placeholders); convergence: interior consensus stable in all arms, agent states drift only with a filter in the loop, end axial slices grow in every arm (open)
- 2026-09-28 DIRECTION (Charlie): the offset is PARKED.  Charlie does not consider it an issue: the estimate is
  hacky and needs data, the current method works well, and the task is to FORMULATE the current method, not to
  improve it.  Do not propose calibration as the next step.  See the 09-28 log entry (the current filter placement
  has no equilibrium; H on the consensus point gives one, equal to the constrained minimizer).  Refined the same
  day: they are happy with what the DCT filter ACHIEVES, but the filter is hacky; the goal is to reformulate the
  theory into something more general that achieves the same.  Ziyun is sending their materials to review.
- Sensor Orthogonal Reconstruction note: rewritten 2026-09-24 (theory + three tests), see the 09-24 log entry
- Sensor Orthogonal Reconstruction -- Theory (new Overleaf project, 2026-09-28): Ziyun's handwritten notes verified and transcribed as written (nothing added, on request); see the 09-28 log entry
- Single-view: literature search in progress
- MAR + multi-slice fusion: pipeline validated end to end on two real Lilly datasets; see `mar_fusion/progress.md`
- MACE4D port to mbirtorch (Greg's plan, `mbirtorch_plans/plans/features/mace4d/mace4d_migration_plan_v2.md`):
  Stages 0, 2, 3, 4, 5 done and pushed to `mace_4d_dev`; the decided questions of 2026-09-15 are being
  implemented in four increments, of which two are pushed (last commit `364e5d0`, 2026-09-16);
  Group 1 (questions 13 and 17) and Stages 6 to 8 wait for Greg's review
- 4D viewer (mbirtorch branch `4D_viewer`): design decided 2026-09-29 (`4d_viewer/decisions.md`); step 1
  implemented the same day as the new module `mbirtorch/viewers/slice_figure4d.py` (`mbirtorch.slice_viewer4d`),
  with the 3D viewer untouched; committed as 0a9ea35 plus the Retina menu fix 9997a8d; step 2's space-time
  planes, dialog fix, and slider layout committed as 677fa51, the tighter slider block as 68130fc, Save movie as 4223797; all pushed to origin/4D_viewer on
  2026-09-29 after the full suite passed (214 passed, 92 skipped); differences in time deferred (not needed for
  now); docs committed as 3b1cff8 and be2d2d4 and pushed; three viewer fixes found in a browser window committed
  as 010043e and pushed; the Gautschi trial on two full 4D volumes is set up and waiting in the queue (job
  16761899); next: that trial, then a pull request for Greg; 2026-10-02: playback and GIF buttons on both position sliders, also in space-time planes, committed as 17cd424 and pushed;
  see the 09-29 log entries

## Log

### 2026-10-02 (4D viewer: playback and GIFs along either slider)
Ziyun asked for playback along any direction and a GIF button beside each Play button, and for playback in the
space-time planes.  The slice slider and the frame-row slider of `mbirtorch/viewers/slice_figure4d.py` now each
have Play and GIF buttons.  Play steps that slider's axis in every panel, in spatial and space-time planes, and
one row plays at a time.  GIF writes one GIF per panel that changes along the axis into a chosen folder.  "Save
movie" left the right-click menu.  `VolumeStack4D.movie_view` and `movie_frame_count` take the axis.  The design
and its reasons are in `4d_viewer/decisions.md`.  Tests: 40 4D viewer tests and the 5 3D viewer tests pass;
`slice_figure.py` is unchanged (md5 db0f0e29a14461d5c4d1af6081aa7e7a).  In a macosx window on the full-z demo
arrays, every row played at 14 to 14.5 steps per second (30 asked).  `gautschi_trial.py` now writes its test
GIFs through the GIF button code.  The docstrings of `save_data_hdf5` and `load_data_hdf5` now say that they
save and load 3D and 4D arrays (checked: 3D, 4D, and a strided 4D view round-trip exactly, and a 4D file from
`save_data_hdf5` loads in the 4D viewer as one 4D volume).  Committed on Ziyun's go as 17cd424 (viewer) and
ee0023a (docstrings), and pushed to origin/4D_viewer after the full suite passed (225 passed, 92 skipped).

### 2026-09-29 evening (4D viewer served from a Gautschi compute node)
Ziyun asked for the 4D viewer to run on Gautschi on full 4D recons.  The viewer runs on a compute node with
matplotlib's WebAgg backend, which serves the viewer window as a web page.  The Mac opens the page in a browser
through an SSH tunnel, with `ssh -J` through the login node to the node's loopback address.  No X server is
needed, and nothing is installed.  WebAgg needs tornado, which the mbirtorch environment lacks, so the job links
tornado 6.5.1 from the anaconda/2025.12 module.  That tornado's C extension was built for Python 3.13 and fails
under the environment's Python 3.11, so the job turns it off with TORNADO_EXTENSION=0.  The page sits under a
random URL prefix, so other users on the node cannot open it.
The job files are `4d_viewer/serve_viewer4d.py` and `serve_viewer4d.sbatch` (claude_scripts commit 1a1d61f).
They run from `~/PycharmProjects/scripts/2026/1001/4d_viewer_trial/` on Gautschi.  The run artifacts sit in
`~/Desktop/data/output/2026/1001/4d_viewer_trial/`: a git archive of mbirtorch 010043e, the tornado link, and
two small test volumes.
The job shows two full (99, 260, 260, 728) recons of Phantom_30s_Run1 that differ in the dejitter and in the
init.  The first is `0924/sor_stage1/4d_nominal_nofilter` (job 16674482, --no_dejitter, FDK init).  The second
is `0917/phantom_mbirtorch_full_slab2gb` (job 16484769, DCT dejitter, MBIR init).  Both used mbirtorch 7a80bbe,
10 MACE iterations, and the nominal offset.  Correction of 2026-10-02: this entry first said that the two recons
differ in the dejitter only.  The run_info of job 16674482 gives the init source as "computed (99 frames, direct
reconstruction)", and the two init files differ by 83% in relative norm on frames 0, 49, and 98.
A smoke test on a login node, with two (12, 48, 48, 24) test volumes, found three faults of the 4D viewer.
Playback blanked the panels on a canvas that cannot blit, such as the WebAgg and notebook canvases.  Drawing an
ROI and then choosing a space-time plane raised "repeated axis in transpose" on every backend.  The ROI plot's
line colors changed each time the plot was recomputed.  The fixes are commit 010043e, with one test each that
fails without its fix.  The full suite passed (216 passed, 92 skipped), and 010043e was pushed to origin/4D_viewer
on Ziyun's go.  The smoke test also found that the job's --notes option consumed the volume paths, so the volumes
became a named option.  Jobs 16761406 and 16761468 were cancelled before they started, for these fixes and for
moving the package copy out of the scripts repository.
The ai partition was fully allocated, with 239 jobs pending.  Job 16761899 (1 GPU, 14 cores, 3 hours) is pending,
and Slurm estimated a start on 2026-10-04.  The bouman account has no grant on the cpu partition.  The highmem
partition takes only jobs of more than 48 cores, smallgpu was full, and profiling is for hardware profiling.

### 2026-09-29 (4D viewer: design decided, step 1 implemented)
Ziyun and I went through the fifteen choices and the design; every decision, alternative, and reason is in
`4d_viewer/decisions.md`.  Ziyun's rule: the 3D viewer is kept as it is, so the 4D viewer is a new module,
`mbirtorch/viewers/slice_figure4d.py`, that subclasses `VolumeStack` and `SliceViewer` (`VolumeStack4D`,
`SliceViewer4D`, entry point `slice_viewer4d`, exported as `mbirtorch.slice_viewer4d`).  Step 1: 4D input
`(t, x, y, z)`, a frame slider with Play (space; comma and period step), a plot of the ROI mean against frame,
3D volumes fixed in time, frame index mapping with a shorter volume holding its last frame, whole-volume differences
including 4D minus 3D, and Load of a 4D file as one volume.  Checks: `slice_figure.py` byte-identical; 13 new tests
and the 5 existing viewer tests pass; every name in `mbirtorch.__all__` resolves.  A real `macosx` window played two
260 x 260 panels at 15.2 fps (30 requested; default 5), with the images kept in the drawn buffer.  Committed as
0a9ea35 on Ziyun's go.  Ziyun then found that the right-click menu opened away from the cursor on a Retina
screen.  The inherited in-figure menu divides the click position in physical pixels by the canvas size in
logical pixels, so at a device pixel ratio of 2 it opened at twice the click's distance from the corner.
Fixed in the 4D viewer only (commit 9997a8d, with a test).  The 3D viewer has the same bug and is left for
Greg.  Neither commit is pushed.
Later the same day: step 2's space-time planes (677fa51, with the dialog layout fix and the slider layout),
the tighter slider block (68130fc), and Save movie (4223797).  For the demo, the init slab's mean over its 24
frames was saved as `init_mean_f0-23_z332-396.npy` next to the slabs in
`Slides/2026/0924/Claude outputs/wedge_experiment/real_data/` (README section added; that folder is not in git).
All five commits were pushed to origin/4D_viewer after the full suite passed on the Mac (214 passed, 92 skipped,
2 min 50 s).
Docs: 3b1cff8 (pages, and the Play sentence in the docstrings) and be2d2d4 (figures drawn at build time), pushed
after the full suite passed again (214 passed, 92 skipped).  While rebuilding those two commits, .git/index went
missing, with a stale index.lock left and slice_figure4d.py on disk reverted to the 3b1cff8 version.  PyCharm had
the project open, which is the likely cause.  Repaired with the lock moved aside, `git reset`, and the file restored
from HEAD.  Nothing was lost, and the commits were correct throughout.  Step 2 (space-time planes, differences in time, Save movie) is not started.

### 2026-09-28 (4D viewer: five designs built on the slice viewer)
Ziyun asked for ways to build a 4D viewer from `mbirtorch/viewers/slice_figure.py`, design first.  Nothing was
written in the repository.  Facts found:
(1) The viewer has one shared slice position, so it cannot hold a time position and a space position at once.
(2) `VolumeStack.load_array` splits a 4D array along its LAST axis into separate volumes.  MACE4D returns
`(num_frames, nx, ny, nz)` with time first, so loading one through the menu gives one `(T, nx, ny)` volume per z.
(3) The full recon (99, 260, 260, 728) float32 is 19.5 GB and the Mac has 16 GB of RAM, so on the Mac only slices,
slabs, or a memory-mapped file.  All six planes of a 1.7 GB in-RAM slab (64 z) extract in under 10 ms (t-x slowest, 7 ms).
(4) Agg timing on the Mac (scratch scripts, not saved): one frame step of the current viewer costs 35 / 55 / 80 ms for
1 / 2 / 3 panels, and the partial redraw is no faster, because every panel changes.  Drawing only the two image artists
costs 10 ms at dpi 100 and 20 ms at dpi 200.  The viewer uses its partial redraw only on Agg and TkAgg, so on-screen
playback speed on `macosx` is untested.
(5) Today's viewer already shows a space-time image: on a `(T, nx, ny)` stack, slice axis 1 or 2 displays (t, y) or
(t, x).  Checked on a synthetic square shifting +-2 px with period 6; the edges show the zigzag.
Designs: 1 linked windows plus playback on the current npz slices; 2 a frame slider in `slice_viewer`; 3 any two axes
of a 4D array, with a slider per hidden axis (space-time planes); 4 orthogonal views over time, as a new module; 5
napari (not installed).  Recommended: 1 now, then 3 or 4.  Open for Ziyun: where the viewer runs, 3 or 4, package
feature (Greg's review) or research tool, frame mapping between runs, and the meaning of Load for 4D files.

### 2026-09-28 (Theory note: Ziyun's handwritten notes verified and transcribed)
New Overleaf project `Sensor Orthogonal Reconstruction -- Theory/main.tex` (was the empty template).  Ziyun asked to
verify two pages of handwritten notes and write them down with nothing extra.  Content: y = Ax (A is M x N, M << N);
xhat = A^t (A A^t)^-1 y; xhat = P x, xtilde = P^perp x; R_xhat = P R_x P^t; with F the unitary DFT,
Lambda = F R_x F^H and Lambda_hat = F R_xhat F^H = F P F^H Lambda F P^t F^H.  All steps correct (numpy check in the
session scratchpad, not saved: pinv identity, P symmetric and idempotent, R_xhat by Monte Carlo, the two Lambda_hat
expressions agree).  Added only the definitions P = A^t (A A^t)^-1 A, P^perp = I - P and "F unitary DFT"; F^* is
written F^H throughout.  Raised with Ziyun, not in the note: A^t (A A^t)^-1 needs full row rank (else A^+); Lambda is
diagonal only for a circulant R_x; Lambda_hat is not diagonal in general (random A: 90% of its energy off the
diagonal) and is diagonal only when Range(A^t) is spanned by Fourier vectors (P circulant).

### 2026-09-28 (offset parked on Charlie's direction; the current filter placement has no equilibrium)
Ziyun relayed Charlie's view: the offset is not an issue (the estimate is hacky and needs data), what we have works,
and what is needed is to formulate it, not to improve it.  Ziyun's argument: even if the jitter comes from the
offset, the general formulation would solve it.  Assessment given: right about the jitter, because the constraint
X in S^perp removes a first-harmonic shift whatever its cause; the cost under a wrong axis is a blur instead of a
shift, and it is small here (z364 sharpness of frame 0, corrected/nominal: 1.014 with DCT, 1.008 with no filter;
the DCT filter itself costs about 5%: nominal no filter 1.051 of nominal DCT).
New check `.../0924/Claude outputs/theory_checks/placement/` (README): linear MACE models with three denoisers whose
space-time coupling differs.  Current placement (H o F, G_k o H): no equilibrium in 300/300, spectral radius > 1 in
293/300.  Reason: with H before a denoiser, an equilibrium needs that prior's gradient to have no Null(H) component,
one condition per denoiser on one unknown.  The parts of the denoiser states that H removes never reach the
denoisers, so they can grow without changing the consensus, which matches the 09-25 drift.  H applied once to the
consensus point (W_k += 2 rho (H z - X_k)): equilibrium in 300/300, equal to argmin over S^perp of
mu_0 D + sum mu_k R_k to 1e-11.  Also: the DCT filter's range excludes every static stack, so the formulation
needs H_per.  Proposed to Ziyun (not started): a short formulation note (new file, main.tex untouched), and two
wrapper runs at the nominal offset (convergence arm, 99-frame run) with H on the consensus point.

### 2026-09-25 11:40 (where the nominal offset comes from: the Geometry Report replacement)
The nominal det_channel_offset is not a field of the .nsipro file: `nsi.load_scans_and_params` computes it from the
.nsipro geometry after replacing the first-detector-pixel coordinate r_r[0:2] with the Geometry Report value
(offset_correction=True, the default; nsi.py:197).  `offset_sources.py` (geometry + two radiographs, login node):
Phantom_30s_Run1 report on -1.33845 ALU (r_r x 36.637), report off -1.65645 ALU (r_r x 36.319) -> the .nsipro-only
value is within 0.03 channel of the data estimate -1.66393; the report replacement moves it 1.25 channels (0.318 mm).
Static demo scan: report on -1.79391, off -1.66690 (1.0 native channel apart); the data estimate agrees with the
report-on value (0.2 native channel).  So neither file is reliable alone; estimate from the data.  Also checked for
Ziyun: the corrected-offset runs differ from the nominal ones ONLY in det_channel_offset (set after
get_sino_and_model; set_params stores it and rebuilds the projectors; sinogram (2400, 728, 260) and grid identical;
the FDK init does not depend on the filter: baseline and control nominal inits identical).  For the MBIR, the denoiser
sigma_x estimated from the init differs as a consequence (0.000592 nominal vs 0.000620 corrected).  Opened
slice_viewer on the FDK results (`view_fdk_offset.py`).  Not yet in offset_justification.tex.

### 2026-09-25 08:30 (control run done: the offset alone removes the rotating shift)
Job 16674482 (nominal offset, no filter, 27 min, confirmed in its log: offset -1.33845, FILTER none, --no_dejitter).
Final: wobble 0.720, first-harmonic shift 1.220 (init 1.29: MACE keeps the shift); every frame ~1 voxel from the mean
in every turn; static-edge line ratios k1 244, k2 5.2, k3 22 (k3 absent in the init).  Against corrected no filter
(0.059, 0.020; k1 1.3, k2 3.9, k3 0.9): wobble 12x, first-harmonic shift 61x lower with only the offset changed.
Sharpness 1.051 vs 1.059.  offset_justification.tex: control written into Section 8 (new first paragraph of "The
finals", table row, moving-parts sentence), abstract and summary now quote 0.720 -> 0.059; no \pending left; synced to
Overleaf (12 pp).  Outputs folder and README updated.

### 2026-09-25 07:00 (interior convergence reruns done: the filter placement question answered)
Jobs 16674461/62/63 (62-64 min each, started early).  Interior = axial slices without the first/last 10%.  Consensus
image interior norm stable in all arms (31.2-31.6 from iteration 10 to 150).  Agent states W interior: DCT 65.5 ->
174.3 (2.7x, accelerating), cycle-avg 64.3 -> 84.2 (1.3x), no filter 65.7 -> 67.1 (flat).  So with a filter inside the
loop (H o F, G_k o H) W drifts although the consensus does not; without a filter W has a fixed point in the interior
(matches the theory note's warning).  End slices of the consensus grow in every arm, ~linearly with no filter (8 ->
150); all of the no-filter whole-volume growth is there.  dW_interior floor ~1 after iteration 100 even with no filter:
the data-fit agent draws a new random VCD subset order per iteration (`rng_for(iteration)`, mace.py:739) and warm-starts
from its own previous output, so it is not a fixed map.  Figure `results/convergence/fig_convergence_interior.png`
(`plot_convergence.py`), copied to `Claude outputs/sor_stage1/`.  Not yet written into experiment_status.tex.

### 2026-09-25 later morning (offset justification Section 8 filled; Stage 1 results saved)
Analysis job 16672782 ran early (04:19).  Nominal DCT baseline 16664243 on z364: wobble 0.126, first-harmonic shift
0.140; corrected DCT 0.076 / 0.021; cycle-avg 0.029 / 0.013; no filter 0.059 / 0.020.  FDK init first-harmonic shift
1.29 -> 0.125.  New measurement (`justify/justify_4d.py`): temporal spectra over two masks (static edges, moving parts;
from the cycle-avg final).  Init static edges: harmonic-1 line ratio 296 -> 2.7, harmonic-2 line 238 vs 253 (unchanged
= frame construction, offset-independent).  Finals static edges: energy at 0.8-1.2 cycles/turn 0.065 (corrected DCT)
and 0.082 (corrected, no filter) of the nominal DCT; corrected no filter has no harmonic-1 line (1.3) and a small
harmonic-2 line (3.9).  Moving parts: continuous spectrum = object motion; filters remove part of it (cycle-avg 0.64,
DCT 1.09, no filter 1.45 of nominal DCT).  Nominal DCT keeps a rotating shift up to 0.65 voxel in the first turn (DCT
end effect); corrected runs within 0.07.  Sharpness corrected/nominal 1.012-1.059.  Harmonic shares now computed inside
a disc of radius 0.45 N (corners of FDK frames have large artifacts): FDK init k1 12% -> 1.6%, k2 83% -> 92% (demo
static 5.9/94).  offset_justification.tex updated (12 pp, Section 8 + table + 3 figures, abstract, summary; the
control row is a red \pending) and synced to Overleaf.  Results saved in `4DCT/Slides/2026/0924/Claude outputs/sor_stage1/`
(README).  Still queued: control 16674482 (est. 09-27), interior convergence reruns 16674461/62/63.

### 2026-09-25 morning (4D runs at the corrected offset done; convergence growth is in the end slices)
Jobs 16672777/78/79 done (27, 26, 26 min).  Preliminary metrics on the center axial slice z364 of the corrected runs
(`analysis_prelim/metrics_z_corrected.json`, script `prelim_z.py`): wobble DCT 0.076, cycle-averaging blocks of 12 0.029,
no filter 0.059 voxel.  At the nominal offset the earlier runs gave DCT 0.129 and block H_per 0.063, so the offset
correction ALONE (no filter) leaves less wobble than any filter at the nominal offset.  First-harmonic shift of the finals
0.021 / 0.013 / 0.020; of the corrected FDK init 0.125 (the 24-frame sweep at the nominal offset gave 1.69).  The baseline
job 16664243 z slice is not yet read: the analysis job 16672782 (ai partition; cpu/highmem/smallgpu closed to the
account) was expected to start 07:18.  Vertical slices x130/y130 (`prelim_xy.py`, baseline slices exist): in-plane x
first harmonic of the final 0.133 (nominal DCT) -> 0.006 (corrected DCT) / 0.006 (no filter) / 0.001 (cycle-avg); the
in-plane y component and the axial one keep ~1 voxel of half-turn displacement on x130, which the local real motion of the
phantom explains (it is not a rotating shift; y130 does not show it).
Convergence: the growth of ||W|| in all three arms (dct, cycleavg12, nofilter_full = job 16673975, 62 min) sits in the end
axial slices z=0 and z=181 (z=0 RMS 0.135 DCT, 0.095 cycle-avg, 0.282 no filter, vs 0.064 in the init; max 2-3.7);
interior slices stable, center-slice mean ~0.003 in all arms.  Independent of the filter placement.  The wrapper now also
logs interior-slice norms (INTERIOR_MARGIN 0.1); reruns 16674461/62/63 (RUN=dct/cycleavg12/nofilter, SUFFIX=_interior,
1 GPU each, parallel).
ALSO: all arms drop sharply at iteration 100.  Cause: the data-fit agent starts its 3 VCD iterations at entry
floor(iteration * prox_partition_advance) of the model's partition_sequence (default `[2,4,6] + [7,8,9,10]*25`, 103
entries, `mbirtorch/_utils.py:95`); beyond the end the last entry repeats.  So up to iteration ~100 F cycles through
four 128-subset partitions (a different map each iteration, the residual cannot go to zero), and from ~101 it is one
fixed map.  Only iterations 101-150 test the fixed point of a stationary operator; there DCT dW rises 3.5 -> 4.4,
no filter flat 3.66, cycle-avg 2.7 -> 3.0.  A clean test would set prox_partition_advance = 0 (not a driver option;
would need the wrapper) -- not submitted, to discuss with Ziyun.
Control added: job 16674482, 99-frame run at the NOMINAL offset with no filter (4d_nominal_nofilter), so that the
offset is the only difference to 4d_corrected_nofilter.  analyze_stage1.py updated to include it, the nofilter_full
arm and the interior reruns; figure script for the justification doc Section 8: `scratchpad/justify/justify_4d.py`
(harmonic-1/2 amplitude maps over 96 frames, shift traces, numbers_4d.json).

### 2026-09-25 early (FDK sweep done; first convergence arm shows drift)
FDK offset sweep job 16673415 (2.5 min): V fit h = sqrt((s(d-d0))^2 + c^2) over d = -3..+3 channels, first 24 frames:
phantom d0 -1.28 (s 2.24, floor 0.46), Kwikpen_4D_2mms -0.58 (2.29, 0.13), Tella_15cP -0.34 (2.31, 1.00; view comparison
said -0.84, biased by motion; harmonic-1 shift 0.70 -> 0.23 at -0.5), Tella_30cP -0.43 (2.31, 0.54).  All four scans have
a nonzero offset error; slopes within 5% of 2beta = 2.34.  Added to offset_justification.tex (figure justify_offset_sweep.png).
Convergence job 16672780: DCT arm (binning 4, 24 frames, corrected offset, 150 its, 65 min) does NOT converge: ||W|| grows
79 -> 276, ||xbar|| 38 -> 70, per-iteration change stays 1.7-5.5 %, dW plateau ~7 then ~4.  cycleavg12 arm running; the
nofilter arm would be cut by the 2.5 h limit, so it was resubmitted alone as job 16673975 (convergence/nofilter_full).
4D run 16672777 (corrected, DCT) started 02:06.

### 2026-09-25 (offset justification draft in Overleaf; survey done; FDK sweep submitted)
Survey job 16672781 done: offset estimate minus nominal (channels) phantom -1.28 (FDK half-turn 2.91->0.15), Kwikpen_4D_2mms
-0.56 (consistent over 27 turns; 1.28->0.10), Tella_15cP -0.84 but unreliable (outlier turns -12; FDK 1.30->1.54 worse),
Tella_30cP -0.40 unreliable (outliers -19/+2.9; 1.15->0.42).  Tella_30cP restored from depot tgz.  Kwikpen/Tella folders
have no Geometry Report (loader skips the report's offset correction, as the driver does).  On Ziyun's suggestion added an
FDK-only offset sweep (-3..+3 channels, job 16673415, `offset_sweep.py`, V-fit h = sqrt((s(d-d0))^2 + c^2)).
New doc `offset_justification.tex` in the Overleaf folder (DRAFT, red placeholders for the sweep and the 4D runs), framed
per Ziyun as: frame construction = direct cause of the period-6 jitter, axis offset = fundamental cause; NO null-space
wording (Ziyun: "dont mention anything about null yet").  New figures justify_{jitter_pattern,patterns,harmonics}.png
(script `scratchpad/justify/justify_figs.py`; copy to static_tests when finalizing).  Key numbers: frames t and t+3
deviation correlation +0.89 (static demo, correct geometry) vs -0.46 (moving phantom); harmonic-1 share 0.0% (Shepp-Logan),
5.8% (demo FDK), 72.7% (moving-phantom MBIR init, slab mean); rigid shift 1.3-1.7 voxels (slab-mean estimate).

### 2026-09-24 late (Stage 1 of the sensor-orthogonal plan submitted, on Ziyun's go-ahead)
Items 1-3 of Stage 1.  Code `~/PycharmProjects/lilly_exp/nsi/2026/0924/sor_stage1/` (wrapper `run_4d_stage1.py` sets
det_channel_offset via a patched get_sino_and_model, swaps the filter for H_per blocks of 12, records ||W_i - W_(i-1)|| by
patching MACE.step, and saves center slices of every saved 4D array; nothing in mbirtorch or mbirtorch_applications
changed).  Outputs `~/Desktop/data/output/2026/0924/sor_stage1/` (one folder per run + analysis/ + slurm_logs/).
Corrected offset -1.66393 ALU (nominal -1.33845).  Jobs: 16672776 smoke test (binning 8, 12 frames, 2 its); 16672777/78/79
full 99-frame 4D runs at the corrected offset with DCT / cycle-averaging blocks of 12 / no filter (branch fdk_init_4dmace,
driver defaults, baseline = job 16664243 at the nominal offset with DCT, same code); 16672780 convergence check (binning 4,
24 frames, 150 its, three filters); 16672781 offset survey (phantom_30s, Kwikpen_4D_2mms, Tella_15cP, Tella_30cP restored
from depot; Kwikpen_4D_0.5mms skipped: no archive on depot 4DCT); 16672782 analysis (afterany).  Full runs and
convergence depend afterok on the smoke test.

### 2026-09-24 (Sensor Orthogonal Reconstruction note rewritten; axis-offset cause of the jitter confirmed; static null-space test)
UPDATE: on Ziyun's request added `experiment_status.tex` (18 pp) to the same Overleaf folder: 13 experiments E1-E13 (wedge parts 1-5, real-data diagnosis, 99-frame filters, full 4D runs, calibration sweep, static per-frame and MACE4D null tests, numpy checks, linear MACE models), each with What / Purpose / What we learned / Supporting figure / Status and files, plus a summary table and the list of experiments not yet run.  New figures in `figures/`: realdata_shift, part5_center_offset, final_dct_vs_cycleavg (relabeled from final_dct_vs_tsa by `real_data/full99/compare_finals_cycleavg.py`), init_comparison_fdk_vs_mbir, theory_checks_harmonics.  A numbers/clarity check led to two corrections in main.tex too: the constraint-inside-prox convergence holds only with plain denoisers (with G_k o H kept: no fixed point in 200/200), and the demo axis offset is 0.025 mm at the detector.
Ziyun asked for a full rewrite of `Overleaf/Sensor Orthogonal Reconstruction/` around the idea "x independent of the sensor
and the system matrix": status/settings/frames first, then the DCT filter and the cycle-averaging dejitter (H_per.tex
merged in), then theory incl. what A and A^T give, then formulations/methods; plus a static-object test of null-space
removal (demo data; `/depot/bouman/data/Lilly/demo_data_nsi.npz` does not exist, the `.tgz` of 200 radiographs of the
static JB-033 artifact phantom was used).  New main.tex (24 pp) + figures `static_nullspace.png`, `calib_sweep.png`; copies of the test outputs, job and plot scripts in `4DCT/Slides/2026/0924/Claude outputs/static_tests/` (README there).
Backups of the old main.tex and H_per.tex in the session scratchpad (`backup_2026-09-24`).  H_per.tex left in place.
THEORY (all propositions checked in independent numpy models, `.../0924/Claude outputs/theory_checks/`): exact error
split xhat-x = A+Ex (mismatch) + A+n - A+r (residual) + Q(xhat-x) (null); sensor independence + data consistency needs
frame coupling; removal of the null component helps iff the null fill is worse than zero; data-preserving maps
(P xhat + Q z, McKinnon-Bates) cannot remove a range-space jitter; axis error delta -> each 120-deg frame shifted by
beta*delta along its central view, beta = 1.170 (explains 97% in the continuous model), pure first harmonic; parallel-beam
parity: null term even harmonics, odd-order mismatch odd harmonics (at delta~1 the even part of the mismatch is 30-60%);
space-time sampling (Willis-Bresler): per-direction Nyquist = turn frequency.  H o F and G o H are NOT firmly nonexpansive:
in small linear models of the MACE loop the current placement diverged slowly in 82% of instances / no fixed point in
75/200; constraint inside the prox converged always (a warning, not a prediction for production).  The earlier
"1.7-voxel full-turn shift" of wedge part 5 is most likely a cross-correlation estimator artifact (ring-shaped peak).
TESTS (Gautschi, code `~/PycharmProjects/lilly_exp/nsi/2026/0924/static_nullspace/`, outputs `~/Desktop/data/output/2026/0924/`):
(1) static per-frame test, jobs 16665554 (ds8+ds4, 12 min): per-frame MBIR null fill error = 0.83 of zero fill (central
slab); removing it 0.172 -> 0.208 NRMSE; FDK frames have ~no null content; null from the frame mean 0.076.
(2) static MACE4D test, job 16666651 (ds8, 3 identical turns, 17 frames): null fill error 0.24-0.26 of zero fill in the
central slab (caveat: the reference x_ref shares data, noise and prior with the frames); removing it 0.083/0.067 -> 0.205/0.195; no filter beat the DCT
filter on this static case (0.067 vs 0.083; frame deviation 4.8% vs 6.4%).
(3) calibration, job 16665608: estimate_det_channel_offset per turn on Phantom_30s_Run1 = -1.24..-1.45 channels from the
nominal -1.3385 ALU (median -1.281; channel 0.254, magnification 2.124, 1 channel = 1.00 voxel at iso); FDK sweep of 24
frames: half-turn displacement 2.91 -> 0.15 voxels, first-harmonic shift 1.69 -> 0.13 at the estimate, slope 2.1-2.2
vs predicted 2.34.  Demo data offset is fine (-0.10 channel).  The 4D run with the corrected offset has NOT been done.
Reviews: three review workflows (technical/numbers/style/completeness); fixes applied (the '3/4 recovered' wording, the 1.65/1.23 ratio inference and the H_per sinusoid claim were corrected).  Runs table now includes job 16664243.  Mac MPS debug run caught a
get_params('angles') bug before the cluster jobs ran.  NOTE: the literature subagent sent Ziyun's email once as the
Crossref 'mailto' parameter (reported to Ziyun).

### 2026-09-24 (Gautschi: branch fdk_init_4dmace checked out, job 16664243 submitted)
Gautschi checkout `~/PycharmProjects/mbirtorch` switched from `mace_4d_dev` (7a80bbe, clean) to `fdk_init_4dmace` (157deaa);
editable install imports the recon_direct init.  Job 16664243 (ai, 4 H100, 1.5 h,
`~/PycharmProjects/scripts/2026/1001/submit_fdk_init_branch.sbatch`): part 1 the full-size 99-frame run of Phantom_30s_Run1
with the unmodified driver (mbirtorch_applications 4dct_script 9a965ed, defaults, downsampling 1, 10 iterations); part 2
`pytest tests` serially.  Recon first so the suite cannot cost it the time limit.  Output, logs, init cache, pytest log and
slurm logs all in `/home/li5273/Desktop/data/output/2026/1001/` (new, so the FDK init is computed there).  CAUTION: the
package on this branch differs from 7a80bbe in 43 files (main/prerelease changes, ~450 changed lines in mace4d.py/mace.py),
so this is NOT a one-factor comparison with job 16626806 (09-23).  Previous suite: 38 min on 1 GPU at 7a80bbe.
DONE 17:35 (47 min, h001, exit 0).  Recon 0.46 h: FDK init computed in 28.8 s, 'init source = computed (99 frames, direct reconstruction)'; init BIT-IDENTICAL to the 09-23 wrapper's FDK init (x130 and y130 slices, max diff 0); sigma 0.005993, sigma_x 0.000608 (same as 09-23); 10 iterations, change 57.5% -> 1.15%, steady iterations 160-190 s.  Final vs 09-23 final: 0.39% (x130) and 0.36% (y130) relative RMS, max abs 0.0036; cause not separated (different seed and the 43-file package difference).  pytest: 277 passed in 17.9 min on 4 GPUs, 0 failed.  Figures fdk_init_vs_final_{x130,y130}.png and center_slices_x130_y130.npz (539 MB) in the 1001 folder.  Gautschi checkout still on fdk_init_4dmace.

### 2026-09-24 (mbirtorch branch fdk_init_4dmace: the computed 4D init is now a direct reconstruction)
On Ziyun's request, `MACE4DModel._compute_init_recon` now calls `agent.model.recon_direct(agent.sinogram)` per frame
(FDK for cone beam, FBP for parallel beam) in place of `recon(..., max_iterations=15)`.  Caching (`init_dir/init_recon.npy`,
same name, option (a): an existing cache of either kind is loaded), worker grouping and the rest of recon unchanged.
`_INIT_ITERATIONS` removed; run_info 'init source' now 'computed (N frames, direct reconstruction)'; weights unused by the init.
Ziyun's reason: FDK and MBIR inits give the same final recon (09-23 comparison, 1.3% RMS), FDK is much faster.
New test `test_computed_init_is_the_direct_reconstruction_of_each_frame`; tests/test_mace4d.py 7 passed on cpu+mps.
`prox_stop_threshold` kept as an accepted no-effect parameter (docstring says so, dropped from run_info), because the Lilly driver in mbirtorch_applications (4dct_script, 9a965ed; same on Gautschi and in mbirtorch_applications_4dct) always passes it and Ziyun does not want that repo touched; deleting it would make set_params raise.  Driver's set_params call verified; tests 7 passed.  Committed and pushed as 157deaa to origin/fdk_init_4dmace.

### 2026-09-23 (deck: the filter is now the Turn-Matched Dejitter, TMD; slide 5 introduces the block form directly)
Ziyun simplified the deck to 12 slides (port slides removed, serif body font) and asked slide 5 to introduce the block
form and to rename the filter again.  New name: Turn-Matched Dejitter (TMD): frames matched by their position in the turn,
the matched pair's mean is what is subtracted; blocks of two turns.  Slide 5 rewritten in their Times New Roman 14/13 pt;
"TSA" -> "TMD" in 20 runs on the other slides.  Backup of their version in the scratchpad (Ziyun_26_0924_user_v1_backup).
Ziyun rejected TMD; FINAL NAME (Ziyun's choice): the cycle-averaging dejitter, written out, no acronym (CAD is taken);
'cycle averaging' as the short form in running text.  Applied through the deck (12 runs) on top of Ziyun's concurrent
edits (deck now 10 slides, their simplified wording on slides 5 and 6).  Backups in the scratchpad: _user_v1 (before TMD),
_tmd (before the final rename).  Names so far: H_per (notes, code, legends) = TSA = TMD = cycle-averaging dejitter.
H_per.tex still says H_per; the 99-frame slide's last bullet still says 'now running' and should carry the 09-22 result.

### 2026-09-23 (FDK-initialized full run submitted, for comparing initializations)
Job 16626806 (ai, 4 H100, 2 h): `scripts/2026/0923/submit_4dmace_fdk_init.sbatch` runs `run_with_fdk_init.py`, which replaces
`MACE4DModel._compute_init_recon` with a copy whose per-frame call is `model.recon_direct(agent.sinogram)` (FDK) instead of
`model.recon(..., max_iterations=15)`; caching, worker grouping, the DCT filter and every driver default unchanged, so
against job 16484769 (09-17) the ONLY difference is the initialization.  Own init dir (no symlink): the FDK init is
computed and cached at `output/2026/0923/phantom_mbirtorch_fdk_init/init/.../init_recon.npy` for later comparison with the
MBIR init of 09-17.  Package tree untouched (7a80bbe).
DONE 16:07: FDK init computed in 31 s (values -1.07 to 0.71, so negatives from the 120-degree FDK), denoiser sigma
0.00599 and sigma_x 0.000608 (MBIR init gave 0.00713 and 0.000200), 10 iterations 108-156 s each, final change 1.15%
(DCT/MBIR-init 0.99%, cycle-avg/MBIR-init 0.95%), 0.4 h.  Center slices of the FDK init and this final copied to
`real_data/full99/center_slices_fdk.npz`; GIFs `final_fdkinit_dct_{x130,y130,z364}.gif`.
COMPARISON (`compare_inits.py`, `init_comparison_fdk_vs_mbir.png`, z364): the two DCT finals differ by 1.3% RMS; wobble
0.129 (MBIR init) vs 0.126 (FDK init), other shift 0.31 vs 0.32, sharpness 0.572 vs 0.581, intensity swing equal,
negative voxels 24% vs 18%.  The initialization barely matters after 10 iterations; the filter matters more (cycle-avg
final differs by 6.5% and halves the wobble).  FDK init: 32% negative voxels (120-degree short-scan FDK), values to -1.07,
8.7x the gradient energy (noise).  CAUTION on the estimator: the adjacent-frame cross-correlation shift read 0.004 voxels
on the raw FDK frames (noise/streaks dominate the correlation of neighbors); with smoothing + object mask it reads 1.1, and
half-turn pairs read 2.9 voxels for FDK against 3.0 for MBIR, so the rotating shift IS in the FDK init and the axis-offset
hypothesis stands.  The wobble is not created by the MBIR iterations.

### 2026-09-23 (one-period variant submitted: TSA with blocks of 6 frames)
Job 16625309 (`scripts/2026/0922/submit_4dmace_hper_block6.sbatch`, HPER_BLOCK=6, output
`output/2026/0922/phantom_mbirtorch_hper_block6/`, same init symlink and settings as the block-12 run).  With one turn per
block each group has one frame, so the filter replaces every frame by the mean of its turn: a block average, temporal
resolution one turn, steps at block boundaries.  Told Ziyun before submitting; it is a reference point, not a dejitter.
CANCELLED by li5273 at 10:50, 46 s after submission, before it ran; no logs, no output.  Not resubmitted.

### 2026-09-22 (full-resolution 4D MACE run with H_per block-12 in place of the DCT filter, submitted)
Job 16612533 on Gautschi (ai, 4 H100, 2 h): `~/PycharmProjects/scripts/2026/0922/submit_4dmace_hper_block12.sbatch` runs
`run_with_hper.py`, a wrapper that sets `mbirtorch.mace4d.temporal_filter_matrix` to the block-12 H_per (same signature,
extra args ignored) and then runs `mbirtorch_applications/nsi_4d/Lilly_recon_4d.py` with the 0917 defaults (99 frames,
10 iterations, downsampling 1).  The mbirtorch tree stays at 7a80bbe, unmodified.  Init read through a symlink
`output/2026/0922/phantom_mbirtorch_hper_block12/init` -> the 0917 cached init, so the ONLY difference from job 16484769
(phantom_mbirtorch_full_slab2gb, 26 min) is the filter.  Output dir `output/2026/0922/phantom_mbirtorch_hper_block12/`,
Slurm logs in `scripts/2026/0922/slurm_logs/`, run_info in `scripts/2026/0922/logs/`.  DONE 2026-09-22 23:04: 0.44 h, 10 iterations, change 49% -> 0.95%, log confirms "H_per in blocks of 12 frames ... dims kept 59".
Compared with the 0917 DCT final on the z364 slice (`real_data/full99/compare_finals.py`, `final_dct_vs_tsa.png`,
`final_center_slices.npz` has z364/x130/y130 of both finals): wobble (period-6 part of the frame-to-frame shift)
init 1.30 -> DCT final 0.129 -> TSA final 0.063 voxels; non-periodic frame-to-frame shift 0.31 -> 0.16; sharpness of
frame 0 identical (0.57 of the init, the loop's prior smooths both); the two finals differ by 6.5% RMS; total slice
intensity swings 22% in both (real motion), with the DCT final 0.4% low at multiples of 6 and the TSA final 0.4% high
there (block starts at 12k are a candidate; not yet separated).  New GIFs `final_tsa_block12_{x130,y130,z364}.gif`.

### 2026-09-22 (the 09-24 deck: ten slides on the jitter and the TSA filter, single column)
`Lilly/4DCT/Slides/2026/Ziyun_26_0924.pptx` modified in place (six-slide original backed up in the session scratchpad as
Ziyun_26_0924_original_backup.pptx; `scratchpad/deck/build_slides2.py` rebuilds from it).  NAME: Ziyun asked for a real
name; the filter is now the Turn-Synchronous Average (TSA) filter in the slides (H_per stays as the symbol in the notes
and in plot legends, which the slides point out).  Ziyun's rules: one column top to bottom, bullets fine, under every plot
say what each line/image is, what is compared, and the conclusion; method first, then what the DCT filter does not
guarantee; the missing-wedge slide dropped ("everyone knows the missing wedge").  Slides 7-16: what we see; what we
assume; the TSA idea; what DCT does not guarantee and TSA does (text); the constant-sequence plot; result 1 static
phantom; result 2 real 24 frames; the real jitter is a rigid shift; an axis offset reproduces it; all 99 frames and the
block form.  QA through PowerPoint's AppleScript PDF export (quit PowerPoint between exports).  H_per.tex not renamed yet.

### 2026-09-22 (H_per.tex: locality section added)
New Section 5 "Averaging over a shorter span: the block form" in `Overleaf/Sensor Orthogonal Reconstruction/H_per.tex`:
why whole-scan averaging leaks the object's motion at the turn period as a displaced copy (99 frames, phantom moves tens of
voxels), Definition of the block form (H_per inside consecutive blocks of B frames, B a multiple of P, last block takes the
leftovers), its inherited properties (orthogonal projection, passes constants, removes P-1 dims per block; 59 of 99 kept at
B = 12), the choice of B (B = 2P smallest useful), the sliding form as a diagnostic only (not symmetric), and the unmeasured
seam.  Measurements section gained the 99-frame paragraph with the wobble numbers (1.30 / 0.26 / 0.14 / 0.08 voxels) and
Figure fig:ghost = figures/full99_variants.png (copied into the Overleaf figures folder).  Abstract and implementation
updated.  graphicx added to the preamble.  v2 kept in the scratchpad.

### 2026-09-22 (Gautschi: DCT and H_per on all 99 init frames; motion ghosts; local H_per)
Slurm job 16595683 (ai, 1 GPU, 7 min after fixing the slab axis; first try 16592987 cancelled: slabs along the fastest
axis made 6.7M small reads per slab) applied temporal_filter_matrix(99,6) and H_per to the whole init
(99,260,260,728) -> `~/Desktop/data/output/2026/0922/dejitter_init_compare/` (two 19 GB .npy, GIFs x130/y130/z364 with
init|DCT|H_per, montage, summary).  FINDING: over 30 s the phantom moves by tens of voxels; the turn-period content of
that real motion is put back as a GHOST (displaced copy of the object) by any filter averaging over all 99 frames:
clear for full H_per, fainter for DCT.  Fix: form the groups locally.  On the z364 slice, wobble left (period-6 part of
frame-to-frame shift; init 1.30 voxels): DCT 0.26, H_per all 0.14 (ghost), H_per sliding ±6 0.10 (no ghost, not a
projector), H_per in blocks of 12 frames 0.08 (no ghost, orthogonal projector, passes constants).  Recommendation: block
H_per over two turns; check block seams.  H_per.tex not yet updated with this (needs a "locality" section).
Also answered: Slurm charges elapsed time x allocation for batch and interactive alike; batch ends when the script ends.
Job 16598843 (9 min, limit cut to 30 min with scontrol) added the block-12 stack and remade the movies with
mbirtorch.save_volume_as_gif (Ziyun found my side-by-side GIFs weird): 12 GIFs, 4 stacks x 3 axes, copied to
`real_data/full99/`.  main.tex Section 3.3: 'window operator' (my term) replaced by a sentence defining R_Theta first.

### 2026-09-22 (H_per.tex: the residue class projector as a standalone formulation)
Wrote `Overleaf/Sensor Orthogonal Reconstruction/H_per.tex` (5 pages, compiles alone with the note's preamble): setting and
the periodicity A_{t+P} = A_t; Definition of H_per = I - E(E^T E)^{-1}E^T + 11^T/T; Propositions with proofs (orthogonal
projector removing P-1 dims, constants pass, every zero-mean period-P sequence removed incl. harmonics, non-harmonic
frequencies pass when P | T, nonexpansive); relation to S_T and S_G; comparison with the DCT filter (leakage counts,
constant response numbers at T=12 and 25, parameters); use in the Mann loop (drop-in matrix for apply_temporal_filter);
what it cannot do (gantry-locked motion; non-multiple views per turn); evidence tables (phantom T=12, real init T=24,
production dips at T=99); implementation snippet (requires T >= P, refuse otherwise).  Not yet in the note's main.tex;
Ziyun may merge or keep separate.  paths.md not changed (same Overleaf folder).
Rewritten the same day in plain language per writing_style_charlie.md on Ziyun's request: no 'trace' (now 'the sequence of
a voxel'), no 'residue class' (frames sorted into P 'groups' by t mod P), no 'nonexpansive'/'leakage' (said in words); title
'The filter H_per: removing the gantry period from a 4D reconstruction'; 6 pages, compiles clean.  v1 kept in the scratchpad.

### 2026-09-22 (real data: what the 4D init jitter actually is)
Ziyun asked for a real-data comparison of frame-axis filters on the jittered init of the 0917 run (24 frames, 64-slice
slab around z=364; slabs cut on Gautschi at `~/Desktop/data/output/2026/0921/wedge_realdata/`, analysed on the Mac in
`mbirtorch/Claude outputs/wedge_experiment/real_data/`, README there).  FINDING: the jitter is NOT a missing-wedge
pattern.  It is a rigid shift of every frame by 1.2-1.6 voxels (0.17 mm) in a direction rotating 60 deg per frame,
period-6 fraction 1.00; frames half a turn apart differ more than adjacent ones.  Part 5 simulation: a det_channel_offset
error of 1.5 channels reproduces a rotating per-frame shift of 1.8 voxels with period 6.  Likely cause: a center of
rotation error of about one detector pixel in the reconstruction geometry -> check with the calibration tools.
The final MACE recon still wobbles 0.2 voxels and its total intensity dips 2% at t = 0, 6, 12, 18: the DCT filter's
constant-response defect in production output.  Method table in the README: DCT baseline leaves 0.44 voxel shift, blurs
12%, and changes frame intensities by 16% at T=24; H_per removes the wobble exactly (0.04 voxel) with 6% blur; wedge
projectors do nothing (jitter not in the wedge); 3-frame blends smear; register + H_per is sharpest (0.98) with no
periodic residual.  Open: what the phantom really does (any real period-6 motion is indistinguishable from the
artifact by a filter); the unexplained full-turn shift in the part 5 simulation; run the geometry calibration.

### 2026-09-21 (Sensor Orthogonal Reconstruction note: the wedge experiment written into the Overleaf note)
On Ziyun's request the experiment is now in the note itself (`Overleaf/Sensor Orthogonal Reconstruction/main.tex`,
20 pages): a paragraph in Section 5.3 (labelled `sec:temporal_projector`) on the transform filter not passing a
constant sequence (0.79 at the end frames at T = 12; 0.914 at t = 6, 12, 18 at T = 25; 3.8 percent RMS), one sentence
in the Summary, a closing note in Appendix B saying which checks were run, and a new Appendix C "The wedge experiment"
(`app:experiment`) with four subsections, Table tab:part3 (the three filters), Table tab:part4 (the operator metric
r_k by geometry and fan angle), and the four figures.  Figures copied to `Sensor Orthogonal Reconstruction/figures/`
(part1_wedges, part2_jitter, part3_filters, part4_multiturn; 6 MB total).  Section 3.6 now points at the appendix.
Compiled three passes, no errors, no undefined references, no overfull lines.  Backup `main.tex.before_2026-09-21_appendix`
in the session scratchpad.  Overleaf sync is through Dropbox; if the link still misbehaves, main.tex AND the figures
folder must be uploaded by hand.

### 2026-09-21 (wedge experiment part 4: the wedge across turns with the real scan's angles)
Added `wedge_part4.py` and `wedge_part4_checks.py` to `mbirtorch/Claude outputs/wedge_experiment/` (README has
the numbers).  Angles as `nsi.py` stores them for Phantom_30s_Run1: (j x -2.5 deg) mod 360, 2400 views.
`construct_time_frame_models` gives 99 frames / 48 views / stride 24 on them, as the note now states.
Parallel slab, 13 frames (2.3 turns): the wedge axis measured from the spectrum is within 1 deg of the
accumulated-angle prediction in every frame, including frames 0, 5, 6, 11, 12 where the stored angle restarts;
||Q_{t+3} d - Q_t d||/||Q_t d|| and the k = 6 value are 1e-3 to 5e-3, equal to the floor from solving one frame
twice (MPS kernels nondeterministic, CG amplifies), so the half-turn symmetry is exact to measurement.
Cone beam (64 ch x 32 rows, source 128 from the axis, fan half angle 7.2 deg at the field edge): the
difference-of-estimates metric read 0.70 even in the midplane, but that was CG convergence error plus empty end
slices.  The operator metric r_k = ||A_k q||/||A_k d|| (q = Q_0 d) gives: parallel r_3 = floor; cone r_3 = 3.6%
(7.2 deg), 1.3% (1.8 deg), 0.7% (0.4 deg) over a 0.5% floor, adjacent frames 10 to 12%.  So the half-turn symmetry
fails in cone beam by an amount roughly proportional to the fan angle, midplane included.
NOTE CORRECTED (Section 3.6): "except in the midplane" was wrong; the two fans share only the central ray, a ray at
fan angle gamma is seen again from the source pi + 2 gamma farther on, and the sliver argument plus the measured
numbers are now in the note.  Backup `main.tex.before_2026-09-21_conebeam` in the session scratchpad; compiled OK.
Also: an energy-weighted wedge-axis estimator is biased 3 deg toward the vertical by the horizontal skull ellipse;
dividing by the phantom spectrum fixes it.  Runtime: the first part 4 run took 1 h 38 min (kernel compilation for 20
frame models, 12 s per cone projection pair during the run vs 0.02 s after); WEDGE_REPLOT=1 redraws from arrays.

### 2026-09-21 (Sensor Orthogonal Reconstruction note: the scan description corrected)
Ziyun flagged "the angle is a monotone function of the view index" as wrong, since a 4D scan takes many turns.
Checked the dataset on Gautschi (`~/Desktop/data/Phantom_30s_Run1_Dec2024`, key login works without BoilerKey):
2400 radiographs, angleStep 2.5 deg, Rotation range 6000 deg (16.7 turns), continuous, 80 fps, 12.5 ms integration,
counter-clockwise, 30 s total (mtimes 16:32:25 to 16:32:57), 144 views per turn, no per-view angle in the .nsipro.
`preprocess/nsi.py:335` assigns angles = (j * angle_step) % 360 with the step sign flipped for counter-clockwise, so the
stored angle is a decreasing sawtooth restarting every 144 views.  With P = 6, overlap 2: stride 24 views (0.3 s), span
48 views (0.6 s), 99 frames available, the runs so far used 25; 144 = 6 x 24 so Q_{t+6} = Q_t is exact in angle.
Rewrote Section 2.1 of the note: the NSI table rotates (not a gantry; the note keeps "gantry" for the rotation seen from
the object), accumulated angle vartheta_j = j Delta theta vs stored angle theta_j = vartheta_j mod 2pi (new eq:wrapped),
frames defined by view index J_t with s and v rounded from the angles (eq:window), Theta_t as the stored angles of J_t,
the dataset numbers, and a paragraph stating that Q_{t+P} = Q_t is exact only when views per turn is a multiple of P.
Two downstream sentences fixed: the Section 3.2 window is contiguous modulo 2pi; Section 3.5 rotates by t s Delta theta.
Backup of the previous main.tex in the session scratchpad.  Compiled with pdflatex, no errors, no undefined references.
"gantry" still appears throughout (harmonics, period, locked to); a global rename to "turn" or "view direction" is
Ziyun's call.

### 2026-09-21 (Sensor Orthogonal Reconstruction note: the wedge experiment)
Built a three-part phantom experiment on the missing wedge of the note
(`Overleaf/Sensor Orthogonal Reconstruction/main.tex`), in `mbirtorch/Claude outputs/wedge_experiment/`
(scripts, arrays, figures, README; untracked in git; nothing in the package changed).  Setting: parallel beam,
360 views per rotation, 128x128x4 Shepp-Logan, P = 6, overlap 2, MPS.
Part 1 splits the phantom into P_t d = A_t^+ A_t d (60 CG iterations) and Q_t d per frame: 94 to 96 percent of
the spectrum energy of Q_t d lies in the predicted missing wedge (29 to 36 percent of the plane); in image space
Q_t d is the two skull arcs tangent to the missing directions; the wedge repeats after 3 frames (parallel beam).
Part 2 reconstructs a static phantom frame by frame (12 frames, init = full-scan recon, 15 iterations): the
frame deviation is 8.3 percent of the static part, with its temporal spectrum peaked at period 3 only, as the
note predicts for parallel beam (period 6 needs cone beam).
Part 3 FINDING: `temporal_filter_matrix` does not pass a constant sequence.  Its orthonormal DCT-I weights the
end frames by sqrt(2), so a constant has components in the removed modes.  At T = 12 the filtered constant is
0.79 at the end frames; at T = 25 it dips to 0.914 at t = 6, 12, 18 and 0.939 at t = 0, 24 (3.8 percent RMS).
The filter's range contains no static stack.  mbirjax `_dejitter_4d_dct` and the 4DCT original share the
normalization.  On the part 2 stack the mace4d filter (band 1) left 15 percent of the jitter but changed the
static part by 1.23x the jitter norm (frames 0 and 11 at NRMSE 0.26); the note's residue-class projector H_per
left 3 percent of the jitter, changed the static part by zero, and cut the per-frame NRMSE from 0.115 to 0.084
in every frame.  T = 12 is also a leakage case (2(T-1)/P = 3.67 not an integer; 8 of 12 modes removed).
Open: measure whether the production consensus shows the dips at t = 0, 6, 12, 18, 24 (mean attenuation of a
static region against t on an existing Gautschi recon); consider H_per in place of the DCT filter (needs Greg).

### 2026-09-18 (mbirtorch MACE4D port, API deck revised after Greg's comments)
Revised the Overleaf deck (`MBIRTorch_4DCT_API/main.tex`, now 22 frames) after Greg's 11 comments. Slide
changes: a new slide "Devices, workers, and tasks: what they are and who owns them" (definitions plus a
made-by/owned-by/lives-for table), the step-distribution slide reworded, "What an agent is" rewritten to
explain tasks and fold_after_all in plain words, a new example slide with a SlabDenoiser agent that provides
tasks, Sphinx-style signature boxes (tcolorbox) for MACE, Task, the three agents, MACE4DModel, and recon,
the recon diagram's consensus box now spans all four agents, parameters shown as name=default, Pygments
default colors for code, "makespan" defined on the log slide, band_width and the mirrored ends of the DCT-I
filter explained, titles now say m4d.recon, imports as grouped bullets. Items 2 (coarse-to-fine partition
setting) and 3 (jax vs torch memory) are discussion questions, not slide fixes; not addressed in the deck.
Overleaf's Dropbox link misbehaved on 09-17 (upload then file removed); Ziyun uploads main.tex by hand.
Later the same day: the deck gained a closing status slide with the 2026-09-17 timing on Phantom_30s_Run1 (25 frames,
four H100s, 10 iterations): mbirtorch 25.8 min against mbirjax 68.0 min, 2.64x FASTER (earlier in this session I had
read the other session's title as "2.6x over mbirjax" meaning slower; that was wrong). Per steady-state iteration:
total 172.5 s vs 387.2 s, makespan 170.2 vs 201.6, denoise worker time 67.6 vs 421.8 (6.2x less), data-fit worker
time 609.2 vs 202.4 (3x more), non-task overhead 2.3 s vs 185.6 s. Numbers from Ziyun's screenshot of the other
session's summary. To-do on the slide is now docs and a demo only; Ziyun dropped the timing study for now.

### 2026-09-17 (mbirtorch MACE4D port, API summary deck)
Wrote a 19-frame beamer deck summarizing the MACE and MACE4DModel API, at
`~/Library/CloudStorage/Dropbox/Apps/Overleaf/MBIRTorch_4DCT_API/main.tex` (Overleaf project, synced by
Dropbox; pdfLaTeX, metropolis theme, same look as Greg's September update deck). Part 1: the consensus idea,
the MACE class (two slides), what an agent is and the Task class, the three agents, the device pool, and two
examples (one-call form; class form with a pool and a checkpoint). Part 2: the 4D problem, MACE4DModel
(constructor and methods, two slides), the seven steps inside recon, the set_params table, a two-GPU
example, the return value and log files, and the two filter functions. Every fact is from the docstrings on
`mace_4d_dev` at 7a80bbe; no figures, tikz only. Compiled locally with no errors; each slide checked as an
image. The user has not yet reviewed it.

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
