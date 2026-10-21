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
- 4D beam hardening correction (2026-10-19, branch 4dbhc, uncommitted): option 1a (frame copies, theta per frame, metal rays only) cuts near-metal streaks ~12% on Tella ds2 24 frames; the 3D clamp at rays without metal causes haze and a 4% plastic drop; see the 10-17 and 10-19 log entries
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

### 2026-10-20 (DCT and theta-basis filters applied to the per-frame MBIR of SimRack-1)
Ziyun asked for both filters on the per-frame MBIR of the simulation, without MACE4D, because MACE4D itself reduces
the jitter.  MBIR: the 10-05 baseline (6 fpr, 99 frames).  Filters: the 99 x 99 matrices that MACE4D used on 10-20.
Job 17148672 (ai, 1 GPU, 21 s, extract_sim_mbir.py in the mace4d_theta scripts) saved X X^t and X G^t per region and
slices; the error of each filtered MBIR then follows exactly on the Mac (compare_sim_mbir_filters.py).  RESULT
(NRMSE against the window-mean GT, mean over 99 frames, all/static/moving / turn-locked error RMS in 1e-4,
all/static/moving / non-periodic content changed / ghost in 1e-3): MBIR 0.3235/0.2259/0.2930 / 14.67/24.80/13.82 / 0
/ 0.27; DCT 0.2313/0.1913/0.2671 / 1.10/2.04/3.88 / 0.080 / 0.60; theta 0.2201/0.1867/0.2664 / 0.96/1.65/4.17 / 0.000 /
0.66.  Both remove 0.638 of the temporal variance.  The DCT error rises to as much as 0.29 in the first and last 15
frames, and theta stays at 0.22, so most of the mean difference is this end effect (frames 12-85: 0.2248 against
0.2198; moving 0.2619 both).  MBIR holds far more turn-locked content than the truth (8.93/10.11/5.83 against
0.63/0.30/0.15 at 1/2/3 cycles per turn), and the static A is 0.005 voxel or less, so the turn-locked error of MBIR
here is a limited-angle intensity pattern, not a shift.  The ghost (mean |value| at pixels empty in the GT of the frame
and filled in another frame, slices z182 and x65) more than doubles with both filters, 10% more with theta; frame 2 of
the GIF shows the rack block outline before it arrives.  Folder `Slides/2026/1020/Claude outputs/simrack1_mbir_filters/`
(README.md, compare_sim_mbir_filters.py and .json, nrmse.png, frame.png, simrack1_mbir_dct_svd_yz_xy_6fps.gif with all
99 frames).  Also on 10-20, for the real scan: GIFs of MACE4D-DCT and MACE4D-SVD alone (z364), both one above the other
as y-z x130 and x-y z364 at 3 and 6 fps, and with the per-frame MBIR of 09-17 as the top row
(mbir_mace4d_dct_svd_yz_xy_6fps.gif, 33 MB, and an 80 dpi copy), in the mace4d_theta folder (make_single_gif.py,
make_two_plane_gif.py).
2026-10-21: on Ziyun's request, all SimRack-1 numbers (filtered MBIR and the MACE4D runs) now use ground_truth_center
(the phantom at the center time of each window) instead of the window mean, with the regions taken from it (moving
195423, static 566559 voxels).  extract_compare_data.py and extract_sim_mbir.py gained --truth center; the ai job
17154781 (run_sim_center.sbatch) waited in the queue and was cancelled, and on Ziyun's instruction both scripts ran on
the Gautschi login node instead (2.5 min, output compare_center/).  The bouman account has no grant on the cpu
partition, so CPU work like this runs on the login node.  The analysis scripts read data/center/ or data/window_mean/
through TRUTH in compare_mace4d_theta.py; the window-mean results are kept in *_window_mean.json.  RESULT, center truth.
Filtered MBIR (NRMSE all/static/moving / turn-locked error 1e-4 all/static/moving / ghost 1e-3): MBIR
0.3251/0.2259/0.3117 / 14.69/24.80/14.33 / 0.58; DCT 0.2340/0.1913/0.2884 / 1.31/2.04/5.60 / 0.91; theta
0.2229/0.1867/0.2876 / 1.19/1.65/5.74 / 0.96; frames 12-85: DCT 0.2275, theta 0.2226, moving 0.2833 both.  MBIR has a
larger ghost against the center truth (0.58 against 0.27), because a frame also sees the object before and after the
center time; the filters add 0.33 (DCT) and 0.38 (theta).  MACE4D: no filter 0.1430/0.1297/0.2259, DCT
0.1424/0.1288/0.2270, theta 0.1421/0.1287/0.2258; turn-locked error static 3.94/0.58/0.31, moving 5.18/4.76/4.71.
Filters on the center truth: DCT 0.0192/0.0089/0.0520, theta 0.0136/0.0000/0.0443.  Conclusions unchanged.  Both
READMEs, figures, and the two SimRack-1 GIFs were regenerated with the center truth.

### 2026-10-20 (the theta-basis filter as a function in Ziyun's fork: d410389, pushed)
Ziyun forked mbirtorch to ZiyunLiiii/mbirtorch_ziyun_fork, cloned at `repository/mbirtorch_ziyun_fork` with upstream
cabouman/mbirtorch, and asked for the branch `svd_based_dejitter` (from main d9e8933 = prerelease).  Commit d410389,
pushed to the fork on Ziyun's go, adds two functions to mbirtorch/mace4d.py.  The first is
`view_angle_filter_matrix(frame_angles, harmonics=(1, 2, 3))`.  It returns I - Q Q^t, with Q from the mean-removed
cos(k theta) and sin(k theta) and a rank tolerance _ANGLE_CURVE_RANK_TOL = 1e-8, as a float32 CPU tensor like
temporal_filter_matrix.  The second is `frame_center_angles(angles, view_slices)`, the circular mean of the view
angles of each frame.  Both are exported from mbirtorch.  Two new tests in tests/test_mace4d.py pass, and so do the
other filter tests of that file, run with PYTHONPATH set to the fork, because the env's editable install points at
the original checkout.  The function reproduces the 10-20 experiment filters to 3e-8.  MACE4DModel is not changed.

### 2026-10-20 (full MACE4D with the theta-basis filter in place of the DCT filter: jobs submitted)
Ziyun asked for full MACE4D runs with the theta-basis filter H = I - Q Q^t in place of the DCT filter, on the real
scan Phantom_30s_Run1 and on SimRack-1 (both 6 fpr), compared with MACE4D+DCT.  Q = scipy.linalg.orth of the
mean-removed cos k theta_t, sin k theta_t, k = 1, 2, 3 (rcond 1e-8), so Q has 5 columns and H removes 5 of 99 modes.
H depends only on the frame angles, so it is computed before the MACE loop.  Wrapper `run_with_theta_filter.py` (the
10-18 pattern: the script runs unchanged through runpy): it replaces temporal_filter_matrix, and it wraps
MACE4DModel.recon to read the model and to pin sigma_noise and sigma_x from PIN_SIGMA_NOISE and PIN_SIGMA_X.
theta_t = -2.5 deg x (central view index of frame t), computed in float64.  This formula was checked against the
code.  The NSI loader puts view j at (-2.5 j) mod 360 from view 0.  construct_time_frame_models makes frames of 48
views, stride 24, from view 0.  SimRack-1 config.json holds the same angles mod 2 pi.  The wrapper also compares
theta_t with the circular mean of each frame model's angles and stops the run above 1e-4 rad.  H uses the formula
and not the float32 angles of the models.  In a test with unwrapped float32 angles, the rounding gave a sixth
singular value of 2e-7 (above the tolerance), so Q would have gained a column of noise.  Both datasets store the
angles mod 360, so the frame angles repeat exactly every 6 frames and the rank is exactly 5.  Correction to the 10-20
note above: at the central angles -60 k - 58.75 deg, sin 3 theta is not 1e-13 but 0.065 in size.  It is
proportional to cos 3 theta, because both are proportional to (-1)^k, and this is why orth drops a column.  Checks:
local test (H symmetric, idempotent, rows sum to 1, trace 94; on frames 12-85 it equals the 10-20 svd123 filter
exactly; a scan with the opposite rotation is caught); login-node preflight on the SimRack-1 model with the archived
code 010043e (angles match to 1e-8 rad, 5 columns, pinned values set, auto_regularize_flag False).
Jobs, submitted on Ziyun's go (ai; `sbatch --test-only` estimated a start on 10-28): 17144247 smoke (1 GPU, 10 min,
ds8, 12 frames, 1 it, not a dependency of the others); 17144248 real (4 GPUs, 45 min: the 10-01 DCT settings with
sigma_noise 0.005993252620100975 and sigma_x 0.0006083836196921766 pinned as in 10-18, Gautschi checkout 4D_viewer
79d9600); 17144249 SimRack-1 (4 GPUs, 35 min: run_baselines.py mace4d with the 1005 code archives, sigma_noise
0.0034316671080887318 and sigma_x 0.00041685011819936335 pinned to the DCT baseline; output renamed mace4d_theta.*).
After each recon, extract_compare_data.py saves 99 x 99 Gram matrices and center slices of the new run and of the
runs it is compared with (real: DCT 10-01, periodic 10-18, no filter 09-24; SimRack-1: DCT, no filter, ground truth,
error Gram matrices per region).  Code `~/PycharmProjects/scripts/2026/1020/mace4d_theta/` (copies in
`Slides/2026/1020/Claude outputs/mace4d_theta/scripts/`), output `~/Desktop/data/output/2026/1020/mace4d_theta/`.
Smoke 17144247 started at once by backfill and passed (h012, 1 min 38 s, exit 0, recon saved).  The frame angles of
the real NSI model match the formula to 1.0e-8 rad, Q has 5 columns, and run_info records the theta-basis filter.
The removal of its compile cache at the end failed with "Read-only file system" on h012.  The cache was removed from
the login node, where scratch is writable.  The local analysis script compare_mace4d_theta.py (in the Slides folder)
was tested on stand-in data built from the saved 6 fpr MACE4D slices: static A of MACE4D-DCT 0.022 and of no filter
0.836, as the 10-09 static_check values (0.02, 0.86).  The full jobs 17144248 and 17144249 are pending.
DONE the same day (both started early by backfill, h012, exit 0): real 17144248 27 min recon + 3 min extraction
(consensus change at it 10 1.16%; DCT 1.15%, periodic 1.16%); SimRack-1 17144249 21 min (seed 209652396, the same as
the baseline; change 0.87%, the same as the baseline).  In both runs theta_t matches the frame models to 1.0e-8 rad,
and Q has 5 columns.  RESULT, real scan (frames 12-85; RMS left in 1e-4 at 1/2/3 cycles per turn and not periodic,
full volume / static A / whole-slice A on z364 / bar shadow in 1e-3): no filter 10.6 3.8 1.6 10.7 / 0.836 / 0.870 /
0.51; DCT 0.73 0.26 0.29 10.6 / 0.022 / 0.011 / 0.78; periodic 0.68 0.25 0.29 10.5 / 0.007 / 0.026 / 0.95; theta 0.66
0.25 0.18 10.5 / 0.007 / 0.027 / 0.93.  The theta and periodic recons differ by 0.64% on z364 (two identical DCT runs
differed by 0.39% on 09-24), and theta differs from DCT by 2.4%.  The periodic H of 10-18 removes 4 curves, all in the
theta span, and theta removes one more (the curve that alternates every frame).  The DCT static shift beats and
drifts to -0.35 voxel at scan frames 84-85, and the theta shift stays within 0.07 voxel along x.  Inside MACE4D the
DCT filter works far better than after MBIR (there it left 5.1 and 4.0 and changed the non-periodic content by 122%;
here it leaves 0.73 and 0.26 with the same non-periodic RMS as the others).  A possible reason is that the data fit
restores what DCT removes by mistake; this was not tested.  The shadow stays: theta adds 0.42e-3 over no filter, and
DCT adds 0.27e-3 (the bar is about 20e-3).  SimRack-1 (NRMSE against the window-mean GT, mean over 99 frames,
all/static/moving / turn-locked error RMS in 1e-4, all/static/moving / static A): no filter 0.1375/0.1298/0.1913 /
1.40/3.94/3.70 / 0.0004; DCT 0.1369/0.1288/0.1920 / 0.53/0.58/2.75 / 0.0006; theta 0.1366/0.1287/0.1910 /
0.51/0.31/2.77 / 0.0005.  So NRMSE differs by at most 0.001 (the run-to-run spread was not measured), theta halves the
turn-locked error of the static parts against DCT, and A is at the floor because SimRack-1 has the exact offset.  Each
filter applied to the GT itself (NRMSE all/static/moving): DCT 0.0142/0.0089/0.0337, theta 0.0094/0.0000/0.0310.  DCT
changes even the static truth, because its rows do not sum to one.  Write-up `Slides/2026/1020/Claude outputs/
mace4d_theta/` (README.md, compare_mace4d_theta.py and .json, real_frame.png, real_shift.png, sim_nrmse.png,
sim_frame.png, mace4d_dct_periodic_theta_z364_3fps.gif, simrack1_gt_nofilter_dct_theta_z182_3fps.gif, and data/,
573 MB copied from Gautschi compare/).

### 2026-10-20 (MBIR vs MBIR-DCT vs MBIR-SVD with cos(theta), sin(theta) as fixed bases)
Ziyun asked for the experiment on the 4D phantom MBIR.  Done on the Mac from saved data, with no job: the filter is a
74 x 74 matrix along time, so slice 364 and the full-volume Gram give exact results.  Data: the 0917 MBIR, scan
frames 12-85 (as compare_real6.py); theta_t = -2.5 deg x (24 t + 23.5); Q = orth(mean-removed [cos, sin]); filter
I - QQ^t (symmetric, idempotent, rows sum to 1, all to 1e-15).  Results (variance removed / non-periodic changed /
RMS left 1e-4 at 1, 2, 3 cycles per turn and non-periodic / static A / whole-slice A on z364): MBIR 0 / 0 /
42.0 33.6 19.9 15.7 / 1.40 / 1.52; DCT 0.839 / 1.223 / 5.1 4.0 0.1 23.0 / 0.17 / 0.19; SVD 0.499 / 0.000 /
0.0 33.6 19.9 15.7 / 0.013 / 0.055; periodic (5 bases) 0.930 / 0.001 / 0 0 0 15.7 / 0.004 / 0.031.  The MBIR row
matches the 10-19 numbers, and the DCT and periodic rows match compare_real6.json.  So cos and sin remove the
once-per-turn shift better than DCT and leave non-periodic content alone, but the 2 and 3 cycles-per-turn parts (43%
of the MBIR temporal variance) stay and are visible in the GIF.  Folder `Slides/2026/1020/Claude outputs/svd_theta/`
(compare_svd_theta.py, .json, frame and curves figures, mbir_dct_svd_z364_3fps.gif, README.md).
Then (Ziyun's request) a fourth method, MBIR-SVD with k in {1, 2, 3}: B = [cos k theta, sin k theta], Q = orth with
a relative rank tolerance 1e-8, so sin 3 theta (1e-13) is dropped and Q has 5 columns.  Result 0.930 / 0.000 /
0 0 0 15.7 / static A 0.004 / whole-slice A 0.041, the same as the periodic removal (filters differ by <= 0.0017 per
entry).  The GIF, the frame figure (2 x 4: frames, and what each filter removed; below MBIR its turn-locked part),
and the curves figure now show four methods.  Labels use "k in {...}" because make_panel_gif.py splits at the
first "=".
Bar leak (Ziyun: why are there leaking voxels at the bar location): bar_leak.py / bar_leak.png in the same folder.
The filter fits one amplitude per sinusoid to all 74 frames, and the bar's turn-locked jitter (RMS 2.21e-3) exists
only after scan frame 36 (50 of 74 frames).  So the fit finds about 50/74 of the amplitude, removes too little
after the arrival, and subtracts the same sinusoid from the empty frames before it.  Extra removal before the
arrival against a fit on those frames alone (mean |.|, 1e-3; bar level 20.4): k in {1} 0.90 (0.89 from the jitter
after the arrival, 0.18 from the step); k in {1, 2, 3} 1.21 (1.12, 0.24).  A unit step at frame 36 leaks 0.009 /
0.012 (k in {1} / {1, 2, 3}) and 0.030 for DCT.  Remedy, not run: let the amplitude vary in time (the 10-09 local
fit, h = 3 frames, cut the periodic-removal shadow from 1.46e-3 to 0.93e-3).

### 2026-10-19 (idea: fix cos(theta) and sin(theta) as temporal bases and zero them)
Ziyun's idea: put cos(theta_t) and sin(theta_t) (theta_t = center angle of frame t) among the temporal bases, fit
the rest of the SVD with that constraint, and zero the two singular values.  Analysis: the result is X (I - P_B),
where P_B is the orthogonal projection onto the span of the two curves, so the rest of the SVD does not change it.
It is a per-voxel least-squares fit of a cos(theta_t) + b sin(theta_t), and it is an Nt x Nt filter that can replace
the DCT matrix.  Check on the saved V of the real 6-frame-per-turn scan (compare_real6_filters.npz, 1017
temporal_bases folder; theta_t = 60 deg * t, both curves made orthogonal to the constant): v1 and v2 lie 99.6% and
99.8% in span{cos, sin}; v3, v4, v5 lie 0.3% or less in it and 99.99% in harmonics 1 to 3 of theta.  So cos and sin
alone remove v1 + v2 (50% of the temporal variance) and leave the period-3 and period-2 parts (43%).  With
cos 2theta, sin 2theta, cos 3theta added (sin 3theta is zero at 60 deg steps), I - P_B equals the saved periodic
filter to 0.0017 (max entry); with cos and sin only, the difference is 0.044.  Nothing run on Gautschi.

### 2026-10-19 (slide with an animation of the turn-average operator R)
Ziyun asked for one slide that shows how R works with an animation instead of the definition.  make_R_animation.py
writes R_operator.gif (19.6 s, loops, 0.35 MB): a made-up voxel curve (slow change + a pattern that repeats every turn +
noise) over 24 frames, P = 6; step 1 the curve with color and marker by position in the turn; step 2 R applied one
position at a time (dots move to the average of frames k, k+6, k+12, k+18; the matching rows of the 24 x 24 matrix R
light up); step 3 R w (turn-locked part plus the mean of w); step 4 w - R w + mean(w) against the true slow change.
make_R_slide.py builds R_operator_slide.pptx from the master and "Title Only" layout of Ziyun_26_1022.pptx (read
from a copy; the deck itself was open and is untouched): title, two lines of text, the GIF.  validate.py passes;
checked with a Quick Look render.  Folder `Slides/2026/1019/Claude outputs/R_operator/`.
Second slide (Ziyun's request): make_f_animation.py writes f_value.gif (17.8 s, loops, 0.26 MB): two made-up curves
with zero mean and unit length over 36 frames (6 turns, P = 6), curve A a pattern locked to the turn, curve B a motion
of period 9 frames (1.5 turns) plus a slow drift; R applied to both one position at a time, then a gauge per curve
with f = ||R v||^2 / ||v||^2: A 0.99, B 0.01 (0.0075; at 24 frames B would be 0.03).  make_R_slide.py now takes
--slide R|f; f_value_slide.pptx validated and checked with Quick Look.  The shared GIF code moved into save_gif and
render in make_R_animation.py; R_operator.gif is byte-identical after that change.

### 2026-10-19 (SVD of the per-frame MBIR at 4, 6 and 8 frames per rotation: done)
Ziyun asked for the SVD of the 4D MBIR recons [X0, X1, ...] at 4, 6 and 8 fpr and plots of all temporal bases.  Taken
as the real scan Phantom_30s_Run1, per-frame MBIR, full res, nominal offset, frames inside views 288-2105: 4 fpr
1008/real_span180_step90_ds1/mbir.npy (scan frames 8-56, T 49), 6 fpr the 0917 MBIR init cache (scan frames 12-85, T 74;
15-its init, older code: a confound), 8 fpr 1008/real_span90_step45_ds1/mbir.npy (16-115, T 100).  mbir_svd_fpr.py: T x T
Gram of X - E in row blocks (float64), eigh, share, periodic fraction f with P = fpr (as compare_real6.py), sign fixed so
the largest entry is positive, spatial bases of the first 12 on z364; local synthetic check matches a direct SVD to
1e-13.  plot_mbir_svd_fpr.py (tested on synthetic bases): x axis = turns of the central view, (k + 1) / P;
temporal_bases_<P>fpr.png (all bases), temporal_bases_first10.png (side by side, scaled by sqrt(T)),
temporal_bases_overview.png (share, f, spectra in cycles per turn).  Job 17119005 (ai, 1 GPU, 30 min) pending
(estimated start 13:35); a login-node run was blocked by the permission check.  Code `~/PycharmProjects/scripts/2026/
1019/mbir_svd_fpr/`, output `~/Desktop/data/output/2026/1019/mbir_svd_fpr/`, copies `Slides/2026/1019/Claude outputs/
mbir_svd_fpr/`.
DONE: job 17119005 started 10:43 (not 13:35), 1.5 min on h012.  6 fpr shares reproduce compare_real6 (25.6/24.4/16.4/
15.5/11.1%); sum of eigenvalues = trace of the Gram to 2e-16.  RESULT: in every setting exactly P - 1 bases have f = 1.00
and they are the leading ones (4 fpr 3 bases 89.4%, 6 fpr 5 bases 93.0%, 8 fpr 7 bases 93.7%); every other basis has
f = 0.00, so the period-P space is filled completely and the split is clean.  Each periodic basis is one harmonic of the
turn (cos/sin pairs at 1, 2, 3 cycles per turn, a single basis at the Nyquist harmonic).  Share by harmonic (cycles per
turn 1/2/3/4): 4 fpr 76.7/12.7; 6 fpr 49.9/32.0/11.2; 8 fpr 40.1/32.8/15.0/5.9.  Absolute RMS temporal deviation per voxel
(1e-4 recon units): harmonic 1 44.3/42.0/36.4, harmonic 2 18.0/33.6/32.9, harmonic 3 -/19.9/22.3, harmonic 4 -/-/14.0,
non-periodic 16.5/15.7/14.4 (4/6/8 fpr).  So the once-per-turn part falls slowly with the frame span (ratio 1.22:1.15:1;
offset-model MBIR A 1.70/1.48/1.39 gives 1.22:1.06:1) and the half-turn part nearly doubles from 180 to 120 deg frames,
then stays; the non-periodic content is the same in all three.  The non-periodic bases are shared across settings at the
same time: the slow trend (4 fpr comp 4, 6 fpr comp 6, 8 fpr comp 8, 0.06 cycles per turn; correlation 0.993-0.994
with 6 fpr on a common turn axis), a hump peaking near turn 8.5 (4 fpr comp 7 vs 6 fpr comp 9: 0.994), and the pair at
0.67-0.68 cycles per turn (4 fpr 5-6, 6 fpr 7-8, 8 fpr 9-10), so that pair (the 10-17 "period 8.9 frames") is fixed in
time, not in frames: an object or scanner motion of period about 1.48 turns, not a frame-construction effect.  Caveat:
6 fpr is the 0917 init (other code, 15 its), so absolute 6 fpr numbers are not strictly comparable.  Figures in the
local folder: temporal_bases_{4,6,8}fpr.png, temporal_bases_first10.png, temporal_bases_overview.png.
SVD of X without removing the mean (Ziyun's request, 6 fpr): job 17127338 (27 s) saved X^t X
(mbir_gram_uncentered.py -> mbir_gram_uncentered_6fpr.npz); plot_uncentered_6fpr.py derives both SVDs from it (centered
one matches mbir_svd_6fpr.npz to 1e-15).  The mean frame holds 74.6% of ||X||^2.  Basis 1 of X is the constant curve
(mean 0.99998; f with Pi 4e-5, with R 1.00); bases 2-12 of X match centered bases 1-11 with |cos| >= 0.99998 and means
<= 0.004 (vs 1 for the constant).  Mixing term c_t = <x_t - mean, mean> as a cosine: RMS 0.011, max 0.026 (76% of it
turn-locked).  Removal with the bases of X and f with Pi (bases 2-6): differs from the centered removal by 1.3e-4 of the
removed energy, voxel means move 0.17% RMS, max change on z364 0.7% of the slice max.  With f from R, basis 1 (the mean)
is removed too: voxel means change 100%, z364 changes up to 65% of the slice max.  So on this data centering matters
only through the f definition; the synthetic test (3% brightness term, mean 97.6% of ||X||^2) overstated the mixing.
Figure temporal_bases_uncentered_6fpr.png, numbers uncentered_6fpr.json.

### 2026-10-18 (full MACE4D with the periodic removal in place of the DCT filter: jobs submitted)
Ziyun asked for a full 4D MACE run of Phantom_30s_Run1 with the DCT filter replaced by the periodic component removal of
periodic_modes.tex.  Wrapper `run_with_periodic_removal.py` (driver unchanged, run by runpy, as the 09-24 and 10-05
wrappers): temporal_filter_matrix returns an identity placeholder; after the init is computed or loaded, H = I - V_Omega
V_Omega^t (SVD of the init minus its temporal mean, G accumulated in z slabs on cuda:0 in float64, f > 0.5, share >= 1e-3)
is written into it in place, so the data-fit outputs, the denoiser inputs and the denoiser statistics all use H; a guard
raises if the filter is used before H exists; periodic_filter.json/.npz record shares, f, Omega and checks of H.
Driver settings of the 10-01 DCT baseline (job 16664243: 99 frames, full res, nominal offset, FDK init, 10 its), with
sigma_noise 0.005993252620100975 and denoiser_sigma_x 0.0006083836196921766 pinned to that run's values, so the filter is
the only difference.  Local synthetic test passed (guard, slab gram = direct gram, H symmetric, rows sum 1, voxel means
kept).  Login-node CPU smoke test (ds8, 12 frames, 1 it) computed H (components 1-4, 99.0%, f >= 0.9999, trace 8) and
configured the denoisers, then timed out at 25 min in iteration 1 (no error).  Ziyun chose 45 min (10-01 run 28.5 min,
10-05 run 27 min end to end) and a chained GPU smoke test.  Jobs: 17081656 smoke (1 GPU, 15 min, ds8, 12 frames, 1 it;
fails unless the recon .npy is saved), 17081657 full (4 GPUs, 45 min, afterok 17081656).  Code
`~/PycharmProjects/scripts/2026/1017/mace4d_periodic/` (copies in `Slides/2026/1017/Claude outputs/mace4d_periodic/`),
output `~/Desktop/data/output/2026/1017/mace4d_periodic{,_smoke_gpu}/`.  Gautschi checkout 4D_viewer 79d9600 (recon code
equal to 157deaa except docstrings).  Not yet: displacement A of frames 12-85 against the 10-01 DCT run.
DONE: smoke 17081656 55 s (h006, recon saved); full 17081657 27 min 08 s (h011, exit 0, 10 its, change it10 1.16%, DCT
baseline 1.15%; sigma_x pinned as planned).  H from the 99-frame FDK init removed components 1-4 only (75.2% of the
temporal variance; f 0.9996-0.99996; component 5 on f <= 4e-4; trace 95; max |H - (I - Pi)| 0.012).  Harmonic split of the
FDK init: period 3 holds 45.8% (v1, v2), period 6 29.4% (v3, v4), period 2 0.0000, so H removes periods 6 and 3 fully and
keeps the period-2 curve (unlike the MBIR frames of periodic_modes.tex, where period 2 held 11.2%).  H is frozen, so any
period-2 content that the iterations create is not removed.  Recon
`recon_4d_Phantom_30s_Run1_Dec2024_voxel_pitch_119.56um_frames_99.npy` + GIFs in the output folder.  Not yet compared.
2026-10-19 viewing: ai and smallgpu estimated starts were 10-22, and highmem needs >= 96 cores for jobs that need more
memory than a standard node (this one does not), so the WebAgg route was not used.  Slices 300-427 (slice 64 = 364) of all
99 frames were cut on the login node from this recon and the 10-01 DCT recon (16-20 s each, 3.4 GB each, in
`.../mace4d_periodic/view_slab/`), copied to the Mac at 9 MB/s (12 min), and shown side by side in the 4D viewer of the
local checkout (4dbhc, macosx window, display 0-0.03).  The local slab copies were deleted on Ziyun's request.
YZ GIF (Ziyun's request): `Slides/2026/1019/Claude outputs/mace4d_periodic/mace4d_dct_vs_periodic_yz_x130_6fps.gif`
(x = 130, all 99 frames, DCT on the left, periodic removal on the right (--layout row), window 0-0.03, 6 fps at Ziyun's request (one turn per second); made on Gautschi with the 1008
make_panel_gif.py from dct_x130.npz and periodic_x130.npz in `.../mace4d_periodic/gif_yz/`).  The slice reaches 0.063
(p99.9), so dense parts saturate in the 0-0.03 window.

### 2026-10-17 (core_properties.tex)
New short note `Overleaf/Sensor Orthogonal Reconstruction -- Theory/core_properties.tex` (+ .pdf, 2 pp, compiles clean) on Ziyun's request:
setup plus five properties with short proofs: (1) 1^t v_r = 0 for sigma_r > 0; (2) X - sum_Omega s_r u_r v_r^t = X(I - V_Omega V_Omega^t)
via (X - E)v_r = s_r u_r and E V_Omega = 0; (3) H_Omega 1 = 1, mean kept; (4) H_Omega is an orthogonal projection and
||X||^2 = ||X~||^2 + sum_Omega s_r^2; (5) at most P - 1 bases with f_r = 1, and with P - 1 of them V_Omega V_Omega^t = R - 11^t/T,
X~ = X(I - R) + E (R = average over same turn position, as in periodic_modes.tex).  Checked on synthetic frames (N 400, T 74, P 6):
(1)-(4) hold to 1e-15; (5) holds to 5e-3 since f_r = 0.9999 there, not exactly 1.  The 6th basis with f > 0.999 is the sigma = 0
basis 1/sqrt(T), which eps keeps out of Omega.

### 2026-10-17 (periodic_modes.tex walked through for Ziyun)
Found while explaining it: at P = 6 the zero-mean period-6 space has dimension P - 1 = 5, and the five removed
components have f = 0.99997 (compare_real6.json; the rest <= 2e-5), so the removal there equals X (I - Pi_P) (subtract
each voxel's mean over frames at the same turn position) and tau, eps do no work.  The DCT row sums (0.968-1.017) come
from norm='ortho' in temporal_filter_matrix: the constant curve has 0.2% of its energy outside DCT-I mode 0 (0 with
norm=None).  The DCT filter keeps 9% of the energy of the period-6 space (||H Pi_P||^2 / ||Pi_P||^2).
Second walk-through (step by step): f of test curves at T = 74, P = 6: linear trend 0.002, one slow cycle
over the scan 0.003, white noise mean 0.069 (= 5/73), cosine of period 6.5 frames 0.004, so the score needs an exact
integer period.  Any artifact that depends only on the view angle lies in the range of Pi_P (rank <= P - 1) at every
order, not only to first order.
All 73 temporal bases plotted (Ziyun's request): `Slides/2026/1017/Claude outputs/temporal_bases/` (plot_temporal_bases.py,
temporal_bases_all.png, temporal_bases_overview.png; data compare_real6_filters.npz copied from the 1009 Gautschi
output).  Components 1-2 are period 6 (a cos/sin pair), 3-4 period 3, 5 period 2, so the five removed bases are the
three harmonics of the period-6 space.  6 and 9 are slow trends.  7 and 8 are a pair in quadrature with a period of 8.9
frames, not a scanner period (hypothesis: a rotating gear; not checked with u_7, u_8).  From about 20 on, the main
frequency rises with the index, and no basis after 5 has power at periods 6, 3, or 2 frames.
Harmonic split of the 93%: each of v1-v5 is >= 99.5% one harmonic; period 6 holds 49.9% of the temporal variance,
period 3 32.0%, period 2 11.2%.  The measured slab shift of the MBIR frames has turn-locked power (voxel^2 per frame)
2.237 at period 6, 0.000 at period 3, 0.061 at period 2: a shift that turns with the view flips sign after half a turn,
so it has only odd harmonics.  So v3, v4 (32%) are not a shift (u3, u4 in Fig. 1 show paired lines of both signs along
edges); hypothesis: limited-angle artifacts, which repeat after half a turn (conjugate views, same missing wedge),
consistent with SimRack-1 FDK static edges (10-08: period 3 > period 6).  v5 holds 22% of the energy of v1 + v2, while
the shift's period-2 power is 2.7% of its period-6 power, so most of v5 is not the shift either (cause not known).
Formula notes in `Slides/2026/1017/Claude outputs/svd_formulas/svd_formulas.{tex,pdf}` (dimensions, rank, zero mean,
share, Pi_P, removal as a time filter).  periodic_modes.tex: the Pi_P paragraph rewritten on Ziyun's request without the
class notation C_t: averages over frames t, t +- P, ..., minus the overall mean, with a T = 9, P = 3 example written out,
and a curve w so the entries are not confused with the bases v_r.  Compiles clean (checked in a scratchpad copy); the
note now runs to 6 pages, and page 6 holds only the Gautschi path.  Then Pi_P renamed R everywhere in the note (Ziyun
found Pi odd; R was unused, A and M are taken by the shift fit), also in svd_formulas.tex; both compile clean.
Then (Ziyun's go) R in the note is the average over frames at the same position in the turn only, without subtracting
the overall mean, so it projects onto all P-periodic curves, f = 1 for any such curve, and Q = I - R.  f_r and Q are
unchanged (checked on the saved V: differences 4e-15 and 1e-16); the code's Pi = R - 11^t/T gives the same results.
The note is back to 5 pages.  svd_formulas.tex keeps the zero-mean version of R.

### 2026-10-17 (4D beam hardening correction: options and first test, jobs submitted)
Ziyun asked for ways to bring the plastic and metal beam hardening correction (`correct_sino_plastic_metal`) into
MACE4D, on mbirtorch branch `4dbhc` (= prerelease 296f738), tested on Tella_15cP downsampled 2, partial frames.
Key fact: the 3D correction changes a ray using only its metal sinogram m and one fitted theta,
y_corr = c (y - S_m(m)) / S_p(m) + m; the plastic sinogram only enters the fit.  So in 4D, theta (spectrum and
materials) can be shared by all frames, and the 4D question is which m to use at a view.  In Tella the metal IS the
moving part: the spring stretches from rows ~100-230 (frame 0) to ~100-520 (frame 64) at full res.
Options: (1) one corrected copy of each frame's views from that frame's volume (1a theta per frame, 1b one theta);
(2) one corrected sinogram, m and p of a view = hat-weighted mean of the two frames that contain it (weights sum to 1
at overlap 2), one theta; (3) alternate correction and MACE4D, as recon_plastic_metal's 3 passes.  All arms use one
segmentation, Otsu thresholds computed once over all frames.
Code (uncommitted): `mbirtorch/preprocess/beam_hardening_4d.py` (segment_frames, frame_material_sinograms,
blend_frames_to_views, correct_sino_plastic_metal_4d; reuses the private fit and correction helpers unchanged).
Local checks: blend weights sum to 1; one-frame segmentation equals segment_plastic_metal; synthetic fit recovers
theta and corrected = p + m to 1e-5 relative.  Frame copies reach MACE4D by stacking them and resetting
mace.view_slices and mace.sinogram_shape in the script (no class change).
Gautschi: code `~/PycharmProjects/scripts/2026/1017/bhc4d/` (bhc4d_run.py, bhc4d_metrics.py, run_bhc4d.sbatch),
output `~/Desktop/data/output/2026/1017/bhc4d/`, mbirtorch copy of 4dbhc in `.../bhc4d/mbirtorch_4dbhc` on PYTHONPATH
(the cluster checkout is on 4D_viewer and has no beam_hardening.py).  24 frames, 10 its per run, seed 0, stop 0,
driver settings, DCT on, 1 GPU each.  Jobs: 17061356 smoke (6 frames, 1 it, whole chain), 17061357 base, then
17061358 control, 17061359 frame_theta, 17061360 frame_global, 17061361 blend (afterok smoke and base).
Metric: streak index = RMS of the z high-pass (sigma 2) of plastic voxels, binned by distance from metal (base masks).
Smoke and base done (base 5 min on 1 GPU; spring still in frames 0-8, moving 14-23).  Pass 1 arms done (~5 min
each).  Streak RMS (1e-4) 1-3 / 3-6 / 20+ voxels from metal: control 174.7 / 72.6 / 15.2; frame_theta 143.2 / 59.1 /
13.4; frame_global 157.9 / 62.4 / 13.5; blend 155.3 / 62.5 / 13.5.  Within 1-6 voxels, still / moving frames: control
126.4 / 134.0; frame_theta 102.2 / 110.7; frame_global 107.2 / 123.9; blend 105.1 / 122.4 (1b and 2 lose half their
gain where the spring moves).  Plastic mean -4% everywhere, metal mean -5 to -11%.  Consensus change at it 10: control
3.8% (base also levels at 3.84%), BHC arms 1.94-2.00% (possibly self-consistency: the correction adds back the
recon's own metal projection).  Theta: theta0 ~1.15 and the p*m cross term ~2.9-3.0 in every fit (positive, the
opposite of physical beam hardening); metal-only and higher terms small and unstable (per-frame std ~0.7).
PROBLEM: all BHC arms add broad bright wedges in the outer region of axial slices, static across frames (not the
120-degree limited angle), and they brighten z182 in frames 0-5 where no ray touches metal.  Cause found in code:
each frame model auto-sets sigma_y from the sinogram RMS and sigma_prox from a sinogram-based recon_std, so the
correction also changed the data-fit strength of every frame.  Rerun with --pin_regularization (regularization from
the measured sinogram in every arm; also logs what the corrected sinogram would give) in bhc4d/pinned/: jobs
17069354 control, 17069355 frame_theta, 17069357 frame_global, 17069358 blend, 17069359 metrics.
Pinned results: the corrected sinogram would have lowered sigma_y by 21% and sigma_prox by 30% (so pass 1 was
confounded), but pinning did NOT remove the wedges or the z182 brightening in frames 0-5 (mean diff +0.00066 both
ways): that hypothesis is rejected for the wedges.  Pinned streak RMS (1e-4) 1-3 voxels: control 174.7, frame_theta
151.1 (-13%), frame_global 166.5 (-5%), blend 163.6 (-6%); still / moving within 1-6: control 126.4 / 134.0,
frame_theta 110.0 / 115.2, frame_global 115.3 / 128.9, blend 113.0 / 127.4.  Plastic mean 20+ voxels -4% in all arms.
Per-frame theta (frame_theta): the p*m term is positive in EVERY frame, still ones too (2.1-2.8 still, 3.4-4.1
moving); the linear metal term ~0 throughout; m^2 positive in still frames, metal terms unstable in moving frames.  So
the odd fit is mostly not from 4D motion.  theta0 alternates with period 3 frames (180 deg) = per-frame normalization
of p.  Open hypotheses: frames 0-5 change at z182 by DCT mixing over all frames; wedges and plastic darkening by the
fit putting metal attenuation in p*m.  Next: 3D control (bhc3d_still.py: views 0-143, spring still, MBIR vs
recon_plastic_metal, theta from the same code) job 17072417; outer loop (pinned) frame_theta pass 2 17072418 and
pass 3 17072419, blend pass 2 17072420, control pass 2 17072421.
3D control done (job 17072417, 5 min): theta from the still-spring 3D MBIR [1.18, 2.94, -2.77, -0.01, 2.81, -1.36]
(same character: positive p*m, linear metal ~0).  recon_plastic_metal vs MBIR (views 0-143): streak RMS 1-3 / 6-10
/ 20+ voxels 368 -> 338 (-8%) / 60.2 -> 49.4 (-18%) / 22.8 -> 20.5 (-10%); plastic mean 20+ -6%; metal mean -7%.  So
the plastic darkening, lower metal and the odd fit belong to the BHC model on this object, not to the 4D use.  4D
frame_theta reduces streaks about as much as 3D (-13%).  Haze check (z182, window 0-0.012): control air ring (r 40-60)
mean 0.0002, frame_theta 0.0009, correlation with control structure -0.16, so it is an artifact (about 3% of plastic),
banded, and the plastic rings turn slightly wavy.  Hypothesis: correction errors on metal rays make haze in the spring
frames (12-23) and the DCT filter (acts on all 24 frames) spreads it to frames 0-5.  Test: pinned_nodct/ control and
frame_theta with --no_dejitter (17075639, 17075640, metrics 17075641).  Outer-loop metrics: pass 2 17075642, pass 3
17075643.
### 2026-10-19 (4D BHC continued: outer loop, DCT test, the clamp at rays without metal)
Outer loop (pinned) does not help: streak 1-3 voxels frame_theta pass 1/2/3 151.1 / 159.0 / 151.7 (control pass 2
174.2); moving frames 115.2 / 125.2 / 118.4; blend pass 2 170.2 (worse than pass 1 163.6).  Metal mean and near-metal
plastic keep drifting down (metal 0.125 -> 0.121, plastic 1-3 34.5 -> 33.7 at pass 3).
DCT test (no_dejitter frame_theta first run 17075640 died on node h018 with no log, signal 53; rerun 17118851 with
--exclude=h018): haze at z182 outer ring in frames 0-5 is 0.00070 with DCT off vs 0.00068 on, so the DCT filter does
NOT spread it (rejected).  No metal at z182 in frames 0-5 (max 0.016-0.023 < threshold 0.079); metal only at z 40-120
and z 320-364.  Cause in code: _correct_plastic_sinogram clamps y - S_m(m) at 0 at EVERY ray; at rays without metal the
correction is otherwise the identity, so the clamp turns negative noise of air rays into 0, a positive bias outside the
object (the 3D method does the same).  Added metal_rays_only to the 4D module (keeps the measured value where every
normalized metal sinogram is below _METAL_SUPPORT_FLOOR; logs the metal ray fraction and the mean change at the other
rays).  Local check: default sets negative non-metal rays to 0 (+0.0027 mean on the toy), metal_rays_only keeps them,
metal rays identical.  Gautschi copy updated (COPY_SOURCE.txt).  Jobs (pinned, metal_rays_only, pinned_metalonly/,
control = pinned/control): 17120788 frame_theta, 17120789 blend, 17120790 metrics.
RESULT (metal_rays_only, pinned): only 8.8-9.5% of rays meet the metal; the default clamp had changed ~30% more rays
(mean change at rays without metal +0.026).  Haze gone (z182 outer ring frames 0-5: 0.00068 -> 0.00001; RMS diff
0.00158 -> 0.00024); plastic far from metal within 0.2% of control (was -4%); consensus change at it 10 3.68% =
control (the earlier faster settling also came from the clamp).  Streak RMS (1e-4) 1-3 / 3-6 / 20+: control 174.7 /
72.6 / 15.2; frame_theta 154.4 / 63.6 / 14.9; blend 166.7 / 66.9 / 15.0; still / moving: control 126.4 / 134.0,
frame_theta 111.1 / 119.1 (-12% / -11%), blend 114.0 / 130.8.  Metal mean -7%, plastic 1-3 voxels -3.5% (correct or
not: unknown).  Recommendation: option 1a (frame copies, theta per frame) with metal_rays_only, one pass.  Write-up:
`Slides/2026/1019/Claude outputs/bhc4d/README.md` (scripts, metrics, figures).  Not committed: beam_hardening_4d.py on
4dbhc.  Open: whether the same clamp causes the 6% plastic drop of the 3D method (not tested in 3D); full resolution
and all 65 frames; 1b not rerun with metal_rays_only.

### 2026-10-09 (periodic component removal: an alternative to the DCT filter, documented)
Ziyun asked whether eSMART-RECON (Li et al., IEEE TMI 2020; summary already in the Theory folder as existing_method.tex)
offers a robust replacement for the DCT filter.  Idea taken: SVD of the mean-removed frames X - E = U S V^t, remove the
components whose temporal basis repeats every P frames (P = frames per rotation), measured by the periodic fraction
f_r = ||Pi_P v_r||^2 / ||v_r||^2 (Pi_P: average over frames at the same position in the turn, minus the mean), tau 0.5;
no soft thresholding, no DFT-peak test.  Equivalent to X (I - V_Omega V_Omega^t): a filter along time whose removed
curves come from the data.  Test (post-processing on the 64-slice slab images of frame_shift/slabs.npz, real scan,
nominal geometry): MACE4D without DCT, 4/6/8 fpr: removes 12-14% of the temporal variance (2-5 components), displacement
A 0.83/0.88/0.98 -> 0.062/0.023/0.028 voxel (MACE4D with DCT 0.059/0.015/0.090), residual 0.13-0.15 (DCT 0.18-0.36).
At 6 fpr: component 1 (83.5%, f 0.00) = rack motion, 2-3 (9.1%, 3.1%; f 0.99, 0.89) = edge images (displacement),
4 (1.7%, f 0.06) = teeth, kept.  FDK/MBIR: periodic components hold 44-92% (limited-angle artifacts too).  Noise-level
components cross the threshold (needs an energy floor).  FDK 4 fpr residual grows 0.17 -> 0.28 (unexplained).
Documented as `Overleaf/Sensor Orthogonal Reconstruction -- Theory/periodic_modes.tex` (+ .pdf, compiles clean, 4 pp),
figures/periodic_modes_fig{1_components,2_displacement}.png, code/periodic_modes/ (periodic_modes_test.py,
frame_shift.py, periodic_modes_test.json).  Gautschi output `~/Desktop/data/output/2026/1009/periodic_modes/`.
Not yet: full volumes, SimRack-1 with ground truth, inside MACE4D.
SimRack-1 4/8 fpr runs (16917513-20) all done 10-08 night; sim_frame_shift (16917521): static-mask displacement A
~0 for MBIR (0.005/0.005/0.028 at 4/6/8 fpr) and both MACE4D (<= 0.001); FDK 0.058/0.028/0.557.  The whole-image
registration gives 0.8-1.2 voxel for every method incl. MACE4D+DCT on the SimRack slab, so it fails there (sparse slice,
as the 10-05 note found); only the static measure counts in simulation.
Then Ziyun asked: apply DCT and the new method to the MBIR recons, compare, and replace the experiment in the note.
`compare_dejitter.py` (job 16924053, ai 1 GPU 1.5 h, code from the 1005 archives): both methods as T x T matrices
along time on full MBIR volumes (periodic: f > 0.5 and variance share >= 0.001); parts gt (window-mean GT of SimRack-1
frames at 4/8 fpr via scan_simulation.ground_truth_frames, saved as ground_truth_window_mean.npy in simrack1_fpr/fpr4,
fpr8), sim (NRMSE all/static/moving, periodic and other error RMS, static-slab A, removed variance and non-periodic
share), real (A, residual, removed shares; 6 fpr MBIR = 0917 init).  Output `~/Desktop/data/output/2026/1009/compare_dejitter/`.
Scripts `~/PycharmProjects/scripts/2026/1009/compare_dejitter/`.
Ziyun narrowed it: only the 4D phantom, 6 fpr, MBIR ("we have not gone that far").  16924053 cancelled after the GT part
and SimRack-1 4 fpr (printed: NRMSE all none ?/dct 0.2076/periodic 0.2114, moving 0.2641 vs 0.2842; not used).
`compare_real6.py` (job 16924075, 44 s): MBIR of 09-17, scan frames 12-85, full volumes, filters as T x T matrices.
Components: first five periodic fraction 1.00 hold 93.0% (25.6/24.4/16.4/15.5/11.1%), sixth 1.2% f 0.00 = rack (kept).
none A 1.480 residual 0.328; DCT A 0.181 residual 0.594, removed variance 0.839, change to the non-periodic part 1.223;
periodic A 0.007 residual 0.215, removed 0.930, non-periodic 0.001.  DCT rows do not sum to one (0.968 first frame);
its displacement curve beats (period 6 falls between DCT-I modes 24 and 25 at T = 74).  The experiment section of
periodic_modes.tex replaced with this (5 pp, compiles clean); figures periodic_modes_fig{1_components,2_displacement,
3_frame}.png; code/periodic_modes: compare_real6.py, make_figures_real6.py, frame_shift.py, compare_real6.json (the
old test files removed).
GIFs (z364, frames 12-85, 3 fps, window 0-0.03): `Slides/2026/1009/Claude outputs/dct_vs_periodic/`
mbir_dct_periodic_z364_3fps.gif (side by side) and mbir{,_dct,_periodic}_6fpr_z364.gif.  Rack bar region (1349 pixels,
empty before scan frame 36, about 0.021 after): before arrival MBIR 0.0001-0.0003, DCT +-0.0008 alternating, periodic
0.0000-0.0007 alternating, i.e. both filters leak about 3% of the bar into earlier frames; the arrival at frame 36
(0.0155) is kept by both.
Shadow (Ziyun: reduce it by tuning).  Cause: the jitter at the bar pixels exists only after the bar arrives, and the
global model removes it with constant strength from all frames.  Tests on slice 364 (shadow_test{,2,3}.py, in the
dct_vs_periodic folder; shadow = mean |value| of the bar region before scan frame 36; jitter = RMS of Pi_P over the
object; A, residual of slice 364): MBIR 0.52e-3 / 3.29e-3 / 1.52 / 0.61; DCT 1.16 / 0.49 / 0.19 / 0.84; global periodic
1.46 / 0.017 / 0.031 / 0.54; pixel gate alone removes the shadow but leaves A 0.15-0.41; running-median detrend does not
help (1.40); LOCAL removal (per frame, Gaussian-weighted LS over nearby frames with columns [V, 1, s - t], a T x T
matrix) h = 3 frames: 0.93 / 0.14 / 0.008 / 0.31; h = 3 + pixel gate 0.02-0.1: 0.56 (= MBIR) / 0.52 / 0.047 / 0.35.
GIF mbir_shadow_variants_z364_3fps.gif (5 panels).  Tuned and tested on the same slice only; not yet in the note.
Jitter table for Ziyun's slide (4 methods x 3 settings): `Slides/2026/1008/Claude outputs/frame_shift/jitter_table.py`
-> jitter_table.csv: per axis, the shift averaged over frames at the same position in the turn (one curve over a
turn), peak-to-peak and RMS.  Peak-to-peak (x, y) voxels: FDK (2.54, 2.25) / (2.38, 2.03) / (2.27, 1.69) at 4/6/8 fpr;
MBIR (2.64, 4.17) / (2.67, 3.46) / (2.50, 2.84); MACE no DCT (1.27, 2.02) / (1.67, 1.77) / (1.82, 2.04); MACE DCT
(0.04, 0.21) / (0.09, 0.03) / (0.26, 0.12).  6 fpr MBIR = 0917 init (older code).
Better display (jitter_loops.py -> jitter_loops.png, jitter_diameter.csv): per method, the (x, y) shift averaged over
frames at the same position in the turn, joined into a closed path over one turn; one panel per setting; size =
diameter (largest distance between two positions).  Diameter voxels 4/6/8 fpr: FDK 2.59/2.43/2.46; MBIR 4.25/3.48/2.96;
MACE no DCT 2.04/2.02/2.26; MACE DCT 0.21/0.09/0.28.
(jitter_loops.py later gained a --static mode outside this session; legends now show method names only.)
SimRack-1 slide set (Ziyun: GIFs and x-shift plots, 4 methods x 3 settings): `Slides/2026/1009/Claude outputs/simrack1_fpr/`
sim_<method>_<fpr>fpr_<span>deg.gif (z182, window 0-0.03, fps fpr/2; 6 fpr = 1005 baselines frames 12-85 from the 1007
slices) and sim_<method>_shift_x_<fpr>fpr.png (plot_sim_shift_x.py; static-parts registration from sim_frame_shift.json,
y axis +-1 voxel of 0.2391 mm).  Max |x shift|: MBIR 0.19/0.14/0.30, MACE no DCT 0.13/0.05/0.08, MACE DCT 0.12/0.04/0.05,
FDK 0.24/0.52 at 4/6 fpr.  FDK 8 fpr: the static registration fails on 59 of 100 frames (90-degree FDK streaks; more
smoothing and a bounded step, fdk8_static.py, do not help); failed frames are omitted and counted in the plot.
Then (Ziyun's suggestion) displacement against the GROUND TRUTH instead: gt_shift.py (job 16924562, 27 s; output
`~/Desktop/data/output/2026/1009/gt_shift/gt_shift.json`): each frame's 32-slice slab at z182 registered to its own
window-mean GT slab, whole image, cross correlation (and least squares).  GT of 4/8 fpr frames = the files saved by the
cancelled 16924053 gt part (fpr4/fpr8/ground_truth_window_mean.npy); frame NRMSE matches the baselines (6 fpr FDK 0.614,
MBIR 0.322, MACE 0.137), so frames and GT correspond.  Works for every stack incl. FDK 8 fpr.  Max |x shift| (SimRack
voxels, 0.2391 mm) 4/6/8 fpr: FDK 0.08/0.21/0.28, MBIR 0.12/0.31/0.33, MACE no DCT 0.07/0.05/0.07, MACE DCT
0.06/0.04/0.07; A <= 0.075.  The 12 sim_<method>_shift_x_<fpr>fpr.png redrawn from it (plot_sim_shift_x.py); the
static-mask version is replaced.
SimRack-1 loop plot (sim_jitter_loops.py, from gt_shift.json xcorr, mean subtracted as for the real scan):
sim_jitter_loops.png (own scale, +-0.146 voxel) and sim_jitter_loops_mm.png (--real_scale: mm on the real figure's
range +-0.287 mm, where all sim loops are dots).  Largest loops: FDK/MBIR at 8 fpr, about 0.1 voxel (0.03 mm) from the
center, a small turn-locked pattern; MACE runs about 0.01 voxel.  The 12 x-shift plots redrawn at +-0.4 voxel.
Center y-z slice (x65) GIFs of the same 12 stacks: sim_<method>_<fpr>fpr_<span>deg_yz.gif (make_panel_gif.py --plane x).
Everything (12 axial GIFs, 12 y-z GIFs, 12 x-shift plots, 2 loop plots) in simrack1_slides.zip in the same folder.
Ziyun: why is the sim shift "weird" / "but there is shift estimated".  Causes: spike at ~1800 deg in every method =
the rack's front end inside the slab (enters z = -3.7 mm at ~1520 deg, t 7.6 s; at z -2.2 mm at 1800 deg); later
growth = limited-angle streaks around the rack (non-rigid error read as a shift), worst at 8 fpr.  Test: gt_shift.py
gained 'static' (least squares on the static mask against GT; rerun 39 s).  Turn-locked part A on static pixels: MACE
0.000-0.001, MBIR 0.005/0.005/0.013 voxel; per-frame max 0.04-0.21 (scatter of a 376-pixel mask); FDK 8 fpr and MBIR 8
fpr static fails (max 25 / 3.4).  Real MBIR A 1.48 real voxels = 0.74 SimRack voxels, about 150x the sim static A.
Ziyun: estimate from one slice, do not average slices.  jitter_slice364.py (same folder; uses the z364 slices saved for
the slide GIFs; Gaussian 1.5 smoothing and cross-correlation to the stack mean kept) -> frame_shift_z364.json,
jitter_diameter_z364.csv, jitter_loops_z364.png.  Diameter voxels 4/6/8 fpr: FDK 2.02/2.08/2.24; MBIR 4.03/3.39/3.09;
MACE no DCT 2.01/2.02/2.16; MACE DCT 0.20/0.11/0.29 (slab values within 0.1-0.4 except FDK, which drops 0.2-0.6).
Ziyun questioned MBIR > FDK.  The difference was along y only and came from the whole-image registration.  Static-only
registration (static_check.py: static mask = object pixels with low temporal std in MACE4D+DCT, moving region dilated 4;
least-squares translation on the mask; -> static_shift.json; jitter_loops.py --static -> jitter_loops_static.png,
jitter_diameter_static.csv).  Diameter voxels 4/6/8 fpr: FDK 3.84/3.26/4.68; MBIR 3.86/3.33/3.25; MACE no DCT
1.88/1.87/1.96; MACE DCT 0.20/0.09/0.26.  FDK = MBIR at 4 and 6 fpr (4 fpr paths coincide); FDK 8 fpr irregular and
larger (90 deg FDK streaks; SimRack FDK 8 fpr static A was also spurious, 0.557).  Static-only numbers are the ones to
report; whole-image FDK was biased low.
Ziyun: the static loops go back and forth.  Cause: per-frame streaks in the static region also repeat every turn,
so turn-averaging keeps them.  Robust measure: A, the circular part of the fit against the central view angle.
Static-only A voxels 4/6/8 fpr: FDK 1.64/1.42/1.33, MBIR 1.64/1.47/1.38, MACE no DCT 0.77/0.86/0.92, MACE DCT
0.05/0.02/0.09; direction -85 to -100 deg; MBIR and MACE A nearly equal for both registrations.  Zigzag (turn-averaged
minus circle, RMS) static: FDK 0.63/1.40 at 6/8 fpr, MBIR 0.55 at 8.  Figure jitter_circles.png (fitted circles solid,
turn-averaged positions faint), jitter_circles.csv, jitter_circles.py.

### 2026-10-08 night (SimRack-1 at 4 and 8 frames per rotation: jobs submitted)
Context: Ziyun disagreed that the overlay of the real-scan displacement curves argues against Charlie's synergy view (any
effect tied to a frame's coverage repeats every turn; I conceded the overlay only fits the angle-locked view, it does not
exclude synergy).  Ziyun asked for SimRack-1 at 8 (and 4) fpr, the same frame settings as the real scan.  Folders
`~/Desktop/data/output/2026/1008/simrack1_fpr/fpr{4,8}/` (sinogram.npy -> SimRack-1 sinogram_noisy.npy, config.json =
the dataset's model params); real_frames.py (same file as the real runs) with --frames_per_rotation, views 288-2105.
Jobs per fpr: fdk (1 GPU, 15 min), mbir, mace4d_nofilter, mace4d (2 GPUs, 1 h): fpr4 16917513-16; fpr8 16917517-20.
Measurement 16917521 (afterany): sim_frame_shift.py, slab of 32 slices around z182 (= 64 full-res slices), 4/6/8 fpr
(6 = the 1005 baselines, frames 12-85), two registrations: whole image (as the real scan) and least squares on the
static mask only (GT slab never changes over 99 windows, moving region dilated 3 px, near material); synthetic test:
static registration recovers a planted 0.8-voxel turning shift exactly while a moving blob biases the whole-image one
to 0.67.  Output `.../simrack1_fpr/shift/` (sim_frame_shift.json, static_mask.npy).  Scripts
`~/PycharmProjects/scripts/2026/1008/simrack1_fpr/`, copies in `Slides/2026/1008/Claude outputs/simrack1_fpr/`.

### 2026-10-08 (real scan with 90 deg frames, 45 deg step, nominal offset: jobs submitted)
Ziyun asked for FDK, MBIR and both MACE4D runs on Phantom_30s_Run1 with frames of 90 deg starting every 45 deg (8 per
turn), nominal channel offset, resources like the SimRack-2 jobs.  Binning 2 x 2 (grid 130 x 130 x 364, as SimRack and
the dl4dct real partial recons); 132 frames of 36 views, step 18 views; the DCT filter period is frames_per_rotation, so
it removes periods 8, 4, 8/3, 2.  `real_frames.py` (stages prep, fdk, mbir, mace4d, mace4d_nofilter; settings of the
SimRack baselines / driver defaults; prep loads the NSI scan once from /depot, saves sinogram.npy + config.json and
checks that the rebuilt model gives the same FDK of frame 0); `run_real_frames.sbatch` (ai, resources at submission).
Code from the 1005 archives (dl4dct f26a4c1, MBIRTorch 010043e).  Scripts `~/PycharmProjects/scripts/2026/1008/
real_span90_step45/`, output `~/Desktop/data/output/2026/1008/real_span90_step45/` (<stage>.npy,
<stage>_center_slices.npz, <stage>_info.json); copies in `Slides/2026/1008/Claude outputs/real_span90_step45/`.
Jobs: 16909352 prep (1 GPU, 15 min), 16909353 fdk (1 GPU, 15 min), 16909354 mbir, 16909355 mace4d_nofilter, 16909356
mace4d (2 GPUs, 1 h each), all afterok prep.
UPDATE: binning 2 was my choice (to match SimRack); Ziyun asked for full resolution so the runs compare with the 120 deg
full-res runs (FDK 1001 init cache, MBIR 0917 init cache, no filter 0924 sor_stage1/4d_nominal_nofilter, DCT 1001).
Binned jobs cancelled (prep and fdk had finished; folder renamed `real_span90_step45_ds2_cancelled`).  BINNING = 1 now;
output `~/Desktop/data/output/2026/1008/real_span90_step45_ds1/`.  Jobs: 16909390 prep (1 GPU, 15 min), 16909391 fdk
(1 GPU, 15 min), 16909392 mbir (1 GPU, 2 h: Ziyun suggested 1 GPU 1 h; Tella full-res per-frame MBIR took 13 min on 4
GPUs for 65 frames of 48 views, so 132 frames here is about 1.5 GPU-hours), 16909393 mace4d_nofilter and 16909394 mace4d
(4 GPUs, 1.5 h; the 1001 99-frame run took 0.46 h of recon).
Prep 16909390 done (26 s): sinogram (2400, 728, 260), grid (260, 260, 728), offset -1.33845 (nominal), rebuilt-model FDK
of frame 0 matches to 2.1e-7.  Then, on Ziyun's request, only the center 100 of the 132 frames: frames 16-115 (views
288-2105, starting at 720 deg, so the turn phase is unchanged); real_frames.py updated (center_frames, info records
scan_frames/scan_views) before the four recon jobs started, so they run the new version; time limits unchanged.
8-per-turn status 17:20: fdk 16909391 done (47 s); mbir, nofilter, dct running.
4 frames per rotation (180 deg frames, 90 deg step) on Ziyun's request: real_frames.py now takes --frames_per_rotation
and keeps the frames inside views 288-2105 (at 8 per turn exactly frames 16-115 as before; the 8-per-turn version that
is running is saved as real_frames_v1_8perturn.py); at 4 per turn that is frames 8-56 of 65, 49 frames of 72 views,
step 36, views 288-2087; the DCT filter removes periods 4 and 2.  run_real_frames.sbatch takes FPR (default 8) and writes
to real_span<span>_step<step>_ds1.  Output `~/Desktop/data/output/2026/1008/real_span180_step90_ds1/` (sinogram.npy and
config.json linked to the 90-deg folder, no new prep).  Jobs 16909494 fdk (1 GPU, 15 min), 16909495 mbir (1 GPU, 2 h),
16909496 mace4d_nofilter, 16909497 mace4d (4 GPUs, 1.5 h).  Offset model prediction: frame shift beta * delta with
beta = 2 sin a / (a + sin a cos a), a = half span: 1.170 (120 deg), 1.100 (90 deg), 1.273 (180 deg).
ALL DONE by 17:52, exit 0.  90 deg (frames 16-115): fdk 0.6 min, mbir 17.5 min (1 GPU), nofilter 24.9 min, dct 24.5 min
(4 GPUs, 10 its each).  180 deg (frames 8-56): fdk 0.5, mbir 10.4, nofilter 12.2, dct 12.4 min.  Each folder has
<stage>.npy, <stage>_center_slices.npz (x, y, z center), <stage>_info.json.  Not yet looked at.
GIFs (made on the login node, `~/Desktop/data/output/2026/1008/real_frames_gifs/`, copied to `Slides/2026/1008/Claude
outputs/real_frames/`): real_span{90,180}_{z,yz,xz}_4fps.gif, panels FDK, MBIR, MACE4D no DCT, MACE4D DCT, center slices
z364 / x130 / y130, window 0-0.03 (MACE max 0.027, FDK p99.9 0.034-0.044), title gives the scan frame and turn.
make_panel_gif.py gained --frames_per_turn and --first_frame (the turn number was hardcoded to 6 frames per turn).
Jitter measurement (Ziyun's go): `frame_shift.py` on the 64-slice axial slab around z364 (smoothed 1.5, registered to the
stack mean) of frames inside views 288-2105 for 90 deg (scan frames 16-115), 120 deg (12-85; FDK = 1001 init cache, MBIR =
0917 init cache (15-its MBIR init, older code), no filter = 0924 sor_stage1/4d_nominal_nofilter, DCT = 1001 final) and
180 deg (8-56).  Fit s(k) = s0 + M [cos, sin](central view angle): radius A (circular part), direction phi from the
central view, anticircular part, residual; plus half-turn displacement and wobble; ratios to 120 deg vs the offset model
(0.940 for 90, 1.088 for 180).  Synthetic check recovers A, phi and 2A exactly.  Job 16916556 (ai, 1 GPU, 1 h), output
`~/Desktop/data/output/2026/1008/frame_shift/` (frame_shift.json, slabs.npz, fig_frame_shift.png); script copies in
`Slides/2026/1008/Claude outputs/frame_shift/`.
RESULT (job 16916556, 1.7 min): radius A (voxels) 90/120/180 deg: FDK 1.034/1.096/1.208 (ratios to 120: 0.943, 1.102;
offset model 0.940, 1.088); MBIR 1.391/1.480/1.703 (0.940, 1.151); MACE no filter 0.981/0.883/0.830; MACE DCT 0.090/
0.015/0.059.  Direction phi -84 to -97 deg for every span and per-frame method (constant, as the offset model predicts).
FDK half-turn 2.851/2.912/3.293 (120 deg reproduces the 09-24 sweep's 2.91).  Anticircular 0.2-0.57, residual 0.17-0.45:
the shift is not a pure sinusoid of the view angle (rows rise fast and fall slowly), with the SAME shape at every span.
Conclusion: the 90 deg frames jitter as an offset-like (fixed sideways, lab-frame) displacement predicts; not a
frame-setting effect.  The wobble metric is not comparable across spans (FDK 120 deg 0.21 is out of line with its A).
MACE without the filter keeps 60-90% of the per-frame A and its A falls with the span.  Figure fig_frame_shift.png and
frame_shift.json copied to `Slides/2026/1008/Claude outputs/frame_shift/`.
Slide GIFs for Ziyun's "Comparison: FDKs" slide (Charlie's synergy question): `Slides/2026/1008/Claude outputs/fdk_fpr/`
fdk_{4fpr_180deg,6fpr_120deg,8fpr_90deg}.gif, center axial z364, views 288-2105 (scan frames 8-56 / 12-85 / 16-115;
6 fpr = the 1001 FDK init from 0924 analysis/baseline_init_z.npz), window 0-0.04 (p99.5 of all three 0.036), fps =
fpr / 2 so one turn is 2 s in each; make_fdk_gif.py and the slices (fpr*_z.npz) there.
Shift curves for the same slide: fdk_shift_curve.png (whole range) and fdk_shift_curve_zoom.png (2160-2880 deg), x and y
shift of each FDK frame vs the turned angle of its central view, three settings, from frame_shift.json; data in
fdk_shift_curve.csv; script plot_fdk_shift.py (palette checked with the dataviz validator; markers differ per series).
Per-setting x-shift plots (Ziyun's request): fdk_shift_x_{4,6,8}fpr.png, shared axis limits, script plot_fdk_shift_x.py.
y label changed to 'displacement (voxels)'.  Same set for MBIR in `Slides/2026/1008/Claude outputs/mbir_fpr/`:
mbir_{4fpr_180deg,6fpr_120deg,8fpr_90deg}.gif (z364, window 0-0.03, p99.5 0.027; 6 fpr = the 0917 MBIR init cache, frames
12-85, extracted on the login node) and mbir_shift_x_{4,6,8}fpr.png; scripts make_frame_gif.py (--method) and
plot_shift_x.py (--method fdk|mbir|mace4d_nofilter|mace4d).
Same set for both MACE4D runs in `Slides/2026/1008/Claude outputs/mace_fpr/`: mace_{nofilter,dct}_{4fpr_180deg,
6fpr_120deg,8fpr_90deg}.gif (z364, window 0-0.03; 6 fpr no filter = 0924 4d_nominal_nofilter center slices, DCT = 0924
analysis/baseline_final_z.npz (the 1001 run), frames 12-85) and mace4d{_nofilter,}_shift_x_{4,6,8}fpr.png on a shared
+-1.5 voxel axis (plot_shift_x.py gained --ylim).  The DCT runs drift at the first and last turn (up to 1 voxel at 8 fpr).

### 2026-10-08 (SimRack-2: the rack motion tilted 10 deg from the rotation axis; jobs submitted)
Context: the scanner team confirmed the channel offset, and Ziyun and Charlie asked whether the jitter could come from
the scanner motion combined with an object motion that is not parallel to the rotation axis.  My answer in chat: unlikely
for the real scan (its static edges and its FDK frames carry the once-per-turn shift, which an object motion cannot
make, and a parallel-beam view and its conjugate view make a steady motion in any direction repeat every 3 frames, not
6); the test below checks it.  SimRack-1 already shows the period split: FDK static edges k2 (period 3) 0.0074 vs k1
(period 6) 0.0025; MACE4D no filter k1 0.00045 vs k2 0.00015.
dl4dct, uncommitted: `RackPhantom` motion parameter `tilt_deg` (bar and its motion turned from z toward x about the
line x = bar x, z = 0; the frame slot follows; absent = 0, bit-identical to SimRack-1 at t = 0, 13.7, 29.9 s on the
full grid); `DATASETS['SimRack-2']` (SimRack-1 with tilt_deg 10); README table row; test
`test_tilted_bar_lies_along_its_tilt`; 45 tests pass.  Tilted bar stays within 13.95 mm of the axis (grid half
width 15.54).  Figure `Slides/2026/1008/Claude outputs/simrack2/simrack2_phantom_xz.png`.
Gautschi: scripts `~/PycharmProjects/scripts/2026/1008/simrack2/` (run_make, run_recon, run_analysis sbatch,
analyze_jitter.py), output `~/Desktop/data/output/2026/1008/simrack2/`.  Make job from `code_make/` (dl4dct 6da9aa5 +
tilt.patch, MBIRTorch d75f13e as SimRack-1); recons with the 1005 baseline archives (dl4dct f26a4c1, MBIRTorch 010043e).
Jobs: 16906463 make (smallgpu), 16906464 fdk + mace4d_nofilter, 16906465 mace4d (ai, afterok), 16906478 analysis
(smallgpu, afterany; the bouman account cannot use the cpu partition).  analyze_jitter.py: error = recon -
window-mean GT over frames 0-95, temporal mean removed, RMS amplitude at periods 6/3/2 frames on static edges,
static near the object, and moving (dilated by 2 voxels) regions; run on SimRack-1 (1005 recons) and SimRack-2 with
the same definition; checked on a synthetic array (recovers the planted amplitudes exactly).  Prediction: the tilt
changes period-3 content, little period-6, and no once-per-turn shift of static edges.
UPDATE: committed as 1c6e308 on dl4dct main and pushed on Ziyun's go; Gautschi clone pulled; code_make/DL4DCT_COMMIT
now names 1c6e308.  Ziyun asked for MBIR as well: job 16906489 (mbir, ai, 30 min, afterok make).  Analysis 16906478
cancelled; 16906490 now also measures mbir (SimRack-1 mbir from 1005), afterany 16906464/65/89.
Offset estimator test (Ziyun asked whether a tilted motion biases the conjugate-view estimate): `estimate_offset.py`
runs `estimate_det_channel_offset` per full turn (144 views, 16 turns) as the 09-24 calibration did, on the clean and
the noisy sinogram; bias = estimate - model offset (exact in SimRack), in native 0.254 mm channels, with the bar speed
and front end per turn.  Local check: recovers a known offset to 0.0006 channels.  Jobs 16906510 (SimRack-1, now) and
16906511 (SimRack-2, afterok make), smallgpu, code from the 1005 archives; output offset_estimate_<name>_<clean|noisy>.json.
My bound in chat: bias <= f * d_perp / 2, d_perp ~1.6 channels at 10 deg over half a turn, so <= 0.8 f channels, far
from 1.28.  Real per-turn estimates: turns 0-7 flat at -1.24..-1.29, turns 8-15 scatter -1.26..-1.45 (possibly the
motion effect, the size the bound allows).
UPDATE 12:15, on Ziyun's request: SimRack-2 recons moved to 2 H100, 1 h (-n28): 16906464/65/89 and analysis 16906490
cancelled; now 16907863 (fdk mace4d_nofilter), 16907864 (mace4d), 16907865 (mbir), all afterok 16906463; analysis
16907866 afterany those three.  At 4 GPUs MACE4D took 20 min on SimRack-1, so 2 GPUs should take about 40 min.
Then FDK split off on Ziyun's request (1 GPU, 15 min, -n14): 16907863 and 16907866 cancelled; now 16907874 fdk,
16907875 mace4d_nofilter (2 GPUs, 1 h), with 16907864 mace4d and 16907865 mbir; analysis 16907876 afterany all four.
Then the make job moved to ai on Ziyun's request (1 H100, 15 min, -n14): new 16907878; the dependencies of 16907864,
16907865, 16907874, 16907875 and 16906511 repointed to it with scontrol update; 16906463 cancelled.  SimRack-1's make
took 11 min on an L40S including the smoke run, so 15 min is tight.
Estimator and analysis jobs also moved to ai (1 H100, -n14) on Ziyun's go: 16906510, 16906511, 16907876 cancelled;
now 16907889 estimate SimRack-1 (15 min), 16907890 estimate SimRack-2 (15 min, afterok 16907878), 16907891 analysis
(30 min, afterany 16907874/75/64/65).  Make job 16907878 started 13:32 on ai.
ALL DONE 2026-10-08 by 14:12 (make 5 min on ai; fdk 27 s, mace4d 16 min, mbir 15 min, nofilter 16 min on 2 H100;
estimates 20-30 s each; analysis 2 min).  Slides: slices x65 (y-z), z182 (axial), y95 (x-z through the bar, the tilt
plane) extracted to `<out>/slides/` and copied with GIFs to `Slides/2026/1008/Claude outputs/simrack2/`:
simrack2_all_{xz,yz,z}_4fps.gif (GT, FDK, MBIR, MACE4D no DCT, MACE4D DCT; 99 frames, window 0-0.03);
make_panel_gif.py there is the 1007 script plus --plane y and room for the suptitle.  Results JSONs not yet read.

### 2026-10-07 (SimRack-1 with the true offset, reconstructed with the nominal one: jobs submitted)
Ziyun asked for one example: forward project SimRack-1 with the real-scan offset and run MACE4D with the nominal one,
with and without DCT.  `simulate_true_offset.py`: SimRack-1 recipe with det_channel_offset -1.66393 mm (09-24 estimate;
nominal -1.33845, -1.28 native channels), code archives of SimRack-1 (dl4dct 3f4e660, MBIRTorch d75f13e), data in
`<out>/SimRack-1-true-offset/` (no zip), checks GT equals SimRack-1 and the sinogram difference.  `run_mace.sbatch`:
folder `<out>/nominal/` = SimRack-1 config.json (nominal offset) + links to the new sinogram and GT, then
run_baselines.py with the 1005 baseline archives (dl4dct f26a4c1, MBIRTorch 010043e), so the settings equal the
baselines.  Code `~/PycharmProjects/scripts/2026/1007/simrack1_offset/`, output `~/Desktop/data/output/2026/1007/simrack1_offset/`.
Jobs: 16899305 sim (smallgpu, 40 min), 16899306 mace4d DCT, 16899307 mace4d_nofilter (ai, 4 GPUs, 45 min, afterok sim).
16899305 DONE 2026-10-08 11:11-11:21, exit 0: GT identical to SimRack-1 (max diff 0), sinogram differs by 5.2% relative
(clean and noisy); data in `<out>/SimRack-1-true-offset/`.  MACE jobs now waiting for ai (estimated start 14:05, 14:55).
MACE jobs 16899306 (DCT) and 16899307 (no filter) DONE 12:37-13:19 (about 20 min each, 10 its).  NRMSE vs GT center,
mean over frames: no filter 0.198 wrong offset vs 0.143 correct (1005 baseline); DCT 0.174 vs 0.142.  Slides: x65/z182
slices in `<out>/slides/`; GIFs simrack1_offset_{yz,z}_4fps.gif (GT, MACE4D no DCT correct/wrong, MACE4D DCT
correct/wrong; correct = the 1005 SimRack-1 baselines) in `Slides/2026/1008/Claude outputs/simrack1_offset/`.
No FDK or MBIR was run on the wrong-offset data.

### 2026-10-07 (SimRack-1 slide GIFs)
Ziyun asked for slide GIFs of the SimRack-1 recons (GT, per-frame FDK, per-frame MBIR, MACE4D no DCT, MACE4D DCT; the
1005 baselines).  Center slices extracted on Gautschi to `~/Desktop/data/output/2026/1007/simrack1_slides/` and copied to
`Slides/2026/1007/Claude outputs/simrack1/`: per method z182 axial and x65 y-z GIFs, `simrack1_all_z_4fps.gif` (five in a
row), `simrack1_gt_fdk_mbir_yz_4fps.gif`, `simrack1_gt_mace_nofilter_dct_yz_4fps.gif`; 99 frames, 4 fps, shared window
0-0.03 (GT max 0.023); script `make_panel_gif.py` (any number of LABEL=npz panels, column or row).
Also pair GIFs without GT: `simrack1_fdk_mbir_yz_4fps.gif`, `simrack1_mace_nofilter_dct_yz_4fps.gif`.
NRMSE by region (`nrmse_static_dynamic.py`/.json, same folder and the Gautschi folder): dynamic = GT changes in any frame
(136089 voxels, 2.2%), static = the rest (6015511, of which 460144 object).  Mean [min, max] over 99 frames, static /
dynamic: FDK 0.632 / 0.459, MBIR 0.329 / 0.295, MACE no DCT 0.133 [0.128, 0.151] / 0.230 [0.167, 0.341], MACE DCT
0.132 [0.129, 0.137] / 0.231 [0.164, 0.334].  "All" reproduces the baseline NRMSEs.
The 10-06 jitter_metrics.json script was never saved (run inline over ssh); recovered from the transcript as
`jitter_metrics.py` in the same slides folder.  Its share_k123 sums rfft bins without doubling the non-Nyquist bins.

### 2026-10-06 night (run 4 on the real scan: started, then stopped)
Started run 4 (xy, last.pt epoch 30) on the real frames on the login node; Ziyun stopped it ("it seems that it is
overfitting").  The process was killed before it wrote anything; `output/2026/1006/real_apply/xy_last/` was left empty
and removed on Ziyun's request.  Note: a pkill -f pattern that appears in the ssh command line also kills that ssh shell; use the [a]pply trick.

### 2026-10-06 night (Desktop real-scan record reorganized by run)
On Ziyun's request, `DL4DCT/Experiment/version0_2dunet/2026-10-06_real_scan/` now has real_partial_recons/
(frames.json), run1_yz_seed0/ and run3_yz_context2/ (apply_info.json, fig_frames_x65.png, two zooms, movie_x65.gif small
and large, slices_x65.npz each; run 3's zooms and small GIF made for it), run1_vs_run3/ (three side-by-side figures),
scripts/.  README: folder table at the top, paths and commands updated (checked one command).  The repo record got the
same layout on Ziyun's request (git mv, run 3's own figures and small GIF added, README updated), pushed as the commit
after 120ee18.

### 2026-10-06 night (run 3 on the real scan)
Ziyun asked for run 3 (yz_context2, 5 slices per frame, best epoch 27) on the real scan.  Applied on the Gautschi login
node CPU (10 min) with apply_to_real.py and the saved real frames; output `output/2026/1006/real_apply/yz_context2/`.
Merged with the run 1 slices and drawn with plot_real_slices.py (scratchpad real_run3/).  Run 3 output close to run 1
(relative difference 0.10 on slice x = 65).  Air noise above the object (rows 2-15): input std 0.00030, run 1 0.00019,
run 3 0.00013, MACE4D 0.00007.  Neither corrects the gear rotation blur; run 3 keeps a little more streak texture
inside the moving middle gear and the rack at frame 98.  Added on Ziyun's request as Section 5 of the real-scan
record (figures redrawn with plot_real_slices.py, which now takes several slice files and --rows; apply_info files
named by run), both in the repo (commit 120ee18, pushed) and in the Desktop copy (with run 3's large GIF and slices).

### 2026-10-06 night (real scan result documented and pushed)
Ziyun: as a proof of concept the real-scan result is good (the network does not invent shapes).  Documented in
`dl4dct/experiments/version0_2dunet/2026-10-06_real_scan/` (README: why the frames were remade at binning 2, the real
partial recons, the use of the network, results, reading, next steps, files; figures, small GIF, apply_info.json, real
frames.json) and `experiments/real_data/README.md`; plan.md gained "8. Results so far" and new next steps.  New
`analysis/plot_real_slices.py` reproduces the zoom figures.  Local copy with the large GIF, slices npz, and scripts:
`/Users/a124601/Desktop/Research_Purdue/DL4DCT/Experiment/version0_2dunet/2026-10-06_real_scan/`.  On Ziyun's request
committed and pushed: 5404f7b (restore_frames, analysis scripts, real_data scripts), 1b6fe0e (first runs record),
c25b642 (real scan record, version0 README, plan).  The code that ran the real job is byte-identical to 5404f7b.

### 2026-10-06 night (run 1 on the real scan: result)
Job 16887939 done (17 min 49 s; the network itself 15 s for 99 frames).  Real partial recons at binning 2 with the
corrected offset saved in `~/Desktop/data/dl4dct/real/Phantom_30s_Run1/partial_recons/span120_step60_start0/`
(fdk, mbir, frames.json, geometry.json); network output `output/2026/1006/real_apply/yz_seed0/` (restored.npy, figure,
GIF, slices npz).  Visual result (YZ x = 65, zooms on the left gears and the middle gear): no SimRack shapes imposed;
the network removes part of the noise and streaks, much less than on SimRack-1; it stays as sharp as the MBIR input and
sharper than MACE4D on static parts (gear teeth, blocks, rack edges); it does not resolve the rotation blur of the
moving gears (teeth smeared as in the input and in MACE4D); the axial edge artifact at z < 40 remains.  Domain gap:
gears, real noise, scatter.  Figures in the scratchpad real_apply/.

### 2026-10-06 night (version 0 run 1 applied to the real scan: job submitted)
Ziyun asked to apply run 1 to the real 4D phantom.  Array size is no problem (fully convolutional, padding), but the
scale is: the real MACE4D recons are at 0.12 mm, the network learned 0.239 mm (binning 2), 120/60 deg frames, MBIR
with the driver settings, values / 0.023.  So: new `experiments/real_data/make_real_partial_recons.py` (real scan at
binning 2 with the corrected offset -1.66393, frames and MBIR settings of dl4dct.partial_recons; writes fdk.npy,
mbir.npy, frames.json, geometry.json to `~/Desktop/data/dl4dct/real/Phantom_30s_Run1/partial_recons/span120_step60_start0/`),
`analysis/apply_to_real.py` (groups of 6, last group 93-98 keeps frames 96-98; restored.npy; YZ slice x = 65 of input,
network, and MACE4D corrected DCT binned 2x2x2: figure, GIF, npz), `run_real_apply.sbatch`.  restore_frames moved into
version0_2dunet/utilities.py (volume_compare.py uses it; new test; 44 tests pass).  Smoke test at binning 8, 6 frames on
the login node passed (fixed a float32 JSON bug).  Job 16887939 (ai, 1 H100, RUN=yz_seed0) pending; outputs
`~/Desktop/data/output/2026/1006/real_apply/yz_seed0/`.  Not committed.

### 2026-10-06 night (version 0 first runs: comparisons and the record)
3D comparison on the same test voxels (4 groups, analysis/volume_compare.py): whole / moving / static: run 1 (yz)
0.138 / 0.268 / 0.060 at epochs 29 and 30; run 4 (xy) epoch 9 0.199 / 0.383 / 0.084, epoch 30 0.098 / 0.300 / 0.049;
MBIR 0.318 / 0.442 / 0.205; mean of 6 0.231 / 0.641 / 0.161; MACE4D 0.149 / 0.381 / 0.119.  XY better on static, YZ on
moving; run 1 never trained on YZ slices outside the object (skip_empty), which raises its whole-volume error.
Paired run 1 vs run 3 (analysis/paired_compare.py): run 3 better on moving (71-75% of samples), worse on static
(93-97%), in both splits; run 3 better at frame positions 1 and 4 only (not explained).  Zoomed figures of test sample
x = 58, frames 93-98 (analysis/plot_two_runs.py): moving parts in place, errors on moving edges, frame 98 smears the bar end.
Record written on Ziyun's request in `dl4dct/experiments/version0_2dunet/2026-10-06_first_runs/` (README with all
results and findings, runs/<run>/ small outputs, comparisons/) and copied, with configs and analysis scripts, to
`/Users/a124601/Desktop/Research_Purdue/DL4DCT/Experiment/version0_2dunet/2026-10-06_first_runs/`.  The analysis scripts
reproduce the numbers exactly (checked on Gautschi, output/2026/1006/version0/analysis_check/).  Not committed.

### 2026-10-06 evening (version 0: first four runs done)
Jobs 16887641-44 done (3-5 min each, 30 epochs x 315 steps, H100).  Test NRMSE (whole / moving / static), best
checkpoint by validation L1: yz_seed0 0.119 / 0.268 / 0.060 (best epoch 29); yz_seed1 0.144 / 0.303 / 0.093 (24);
yz_context2 0.124 / 0.253 / 0.066 (27); xy 0.170 / 0.383 / 0.084 (best epoch 9).  Baselines on YZ test slices: input
0.286 / 0.442 / 0.205, mean of 6 0.223 / 0.641 / 0.161, MACE4D 0.149 / 0.381 / 0.119 (moving and static masks cover the
same voxels in both planes, so those columns compare across planes).  Findings: (1) yz_seed0 beats MACE4D on all three;
(2) seed spread 0.119 vs 0.144 is larger than the context effect, so one seed per setting cannot rank settings;
(3) xy: validation L1 lowest at epoch 9 and rising, validation NRMSE falling to 0.098 at epoch 30 (best of all runs),
so selecting by L1 tested xy at a poor epoch; (4) train L1 0.003 vs valid 0.008-0.015: a generalization gap.
Figures in the scratchpad version0_results/; outputs on Gautschi output/2026/1006/version0/.

### 2026-10-06 night (version 0 cleaned up: utilities.py)
On Ziyun's request: new `dl4dct/version0_2dunet/utilities.py` (pick_device, count_parameters, load_config(path,
known_keys), take_slices, plot_losses, save_sample_figure); train.py keeps the options, make_data, evaluate,
train_epoch (the epoch loop, split out of main), and main in three commented parts; count_parameters left model.py.
Check: a deterministic CPU run before and after gives identical metrics.json, history.json, and checkpoint weights.
41 tests pass, docs clean, no unused imports.  The pending Gautschi jobs 16887641-44 still run the copy made before the
cleanup (same behavior).  Committed and pushed on Ziyun's go as 0ef373b (package: tracking, JSON configs, utilities.py)
and 681f967 (experiments/version0_2dunet: configs, sbatch, compare_runs.py, README).

### 2026-10-06 night (version 0: tracking, JSON configs, four training runs submitted)
train.py now logs the training L1 every 50 steps, the validation L1 and NRMSE (whole, moving, static) each epoch,
redraws fig_losses.png each epoch (baseline lines added at the end), and takes --config <json> (keys = option names;
"_" keys are notes; unknown keys refused; flags override; each run saves config.json, reloadable, plus run_info.json).
experiments/version0_2dunet/: configs/{yz_seed0, yz_seed1, yz_context2, xy}.json, run_version0.sbatch (RUN = config
name, 1 H100, -n14, 1 h), compare_runs.py (losses of all runs, summary.md test table), README.  40 tests pass, docs
clean.  A 4-GPU job was estimated to start 2026-10-24, and so was a 1-GPU job; four 1-GPU jobs submitted (single GPU
jobs started early before).  First four jobs 16887620-23 (flags) cancelled for the configs; jobs 16887641 (yz_seed0),
42 (yz_seed1), 43 (yz_context2), 44 (xy) pending.  Code copy: 89209eb + uncommitted train.py (md5 e602c57b...) and
experiments/version0_2dunet.  Outputs `~/Desktop/data/output/2026/1006/version0/<run>/`.  Not committed.  A watcher on
the Mac waits for the jobs, runs compare_runs.py, and copies the figures to the scratchpad (version0_results/).

### 2026-10-06 night (dl4dct: version 0, a 2D U-Net that fuses 6 frames)
Discussed models: recommended a residual 2D U-Net with frames as channels first, then a 3D U-Net over (t, y, z), then a
small Restormer after more datasets; not flow-based alignment (RAFT followed streaks) or diffusion.  Ziyun asked for
the first version under `dl4dct/dl4dct/version0_2dunet/`: model.py (UNet2D: GroupNorm+SiLU blocks, pads to 2^depth,
zero-initialized head; FrameFusionUNet: 6 frames x (slices + sin/cos of the start angle) as channels, output added to
the input slice), data.py (ScaledSamples: divide by 0.023, clip, random patches, z flips; no y flips because the angles
would need mirroring), train.py (AdamW + OneCycle, L1, bf16 on CUDA, best/last checkpoints, history, metrics vs
input / mean_of_6 / --compare arrays, over all, moving (target std > 0.02 across the group) and static voxels, sample
figure).  6 tests (37 total pass); docs clean; no MBIRTorch import.  Smoke run on the login node CPU with the real
recons (`output/2026/1006/version0_smoke/`, 6 steps): 7.77 M parameters; test NRMSE on YZ slices: input 0.286 (moving
0.442, static 0.205), mean of 6 0.223 (0.641, 0.161), MACE4D 0.149 (0.381, 0.119).  Committed and pushed as 89209eb on Ziyun's go.

### 2026-10-06 evening (SimRack-1 cleanup and zip of the partial recons)
On Ziyun's go, deleted: datasets/SimRack-1.zip (stale, made before the partial recons), output/2026/1003/sim_dataset_v1,
output/2026/1003/datasets/SimRack-1-smoke, output/2026/1006/slice_data_check.  Kept the code archives
(output/2026/1003/datasets/code, output/2026/1006/partial_recons/code).  Zipped the training folder as
`SimRack-1/partial_recons/span120_step60_start0.zip` (2.3 GB from 9.7 GB, 2 min, unzip -t clean).  A zip command that
Ziyun rejected had already run (datasets/SimRack-1_partial_recons.zip, same content); deleted with its log on Ziyun's
go.  Training needs from the setting folder: frames.json, mbir.npy, ground_truth_center.npy (fdk.npy and
ground_truth_window_mean.npy optional).

### 2026-10-06 later (Tella_15cP: per-frame FDK, per-frame MBIR, MACE4D with and without DCT, jobs submitted)
Ziyun asked for the same four recons on `~/Desktop/data/Tella_15cP_Run3_April2024/` (used before only in the 09-24
offset survey and FDK sweep).  Scan: 1600 views, 2.5 deg apart, continuous, 4000 deg (11.1 turns); radiographs intact.
120 deg frames = 48 views, stride 24 (exactly 60 deg), 65 frames.  Full resolution, nominal offset, driver defaults, as
for the 4D phantom.  Jobs (ai, 4 GPUs, 1 h 15 min each): 16887252 dct (driver; its FDK init cache is the per-frame FDK),
16887253 nofilter (driver --no_dejitter), 16887254 mbir (per_frame_mbir.py: 15 its, stop 0.02, the old MBIR-init
settings).  Code `~/PycharmProjects/scripts/2026/1006/tella_15cP/`, output `~/Desktop/data/output/2026/1006/tella_15cP/`.
Also on 10-06: slide comparison GIFs (4 fps) and viewers for FDK, MBIR, MACE no DCT, MACE DCT, and 4D-DCT vs static
no-DCT; deck `Slides/2026/Ziyun_26_1008.pptx` reviewed; email to Charlie and Greg drafted (Ziyun wrote a short one).
Tella jobs all done (dct 19 min, nofilter 18 min, mbir 13 min; dct consensus change 51% -> 1.86% at it 10).  GIFs of
the center axial slice z364, 65 frames, 4 fps, shared window 0-0.05 (a small dense part reaches 0.16-0.27 and saturates):
`Slides/2026/1006/Claude outputs/tella_15cP/` (tella_{fdk,mbir,mace_nofilter,mace_dct}_4fps.gif, make_gif.py, slices).

### 2026-10-06 afternoon (SimRack-1 partial recons done)
Job 16886735 (ai, 1 H100, started 15:53, 17 min 50 s, exit 0; MBIRTorch d75f13e, dl4dct 4720b3f): FDK 0.1 s and MBIR
10 s per frame.  NRMSE vs center GT: FDK 0.617 (0.597-0.643), MBIR 0.325 (0.304-0.350), equal to the baselines.  GT in
the folder identical to the dataset GT; FDK identical to the baseline FDK; MBIR differs from the baseline MBIR (010043e)
by ~2% relative.  torch dynamo hit its recompile limit in qggmrf_gradient_and_hessian_at_indices (falls back, speed
fine).  plan.md and experiments/partial_recons/README.md updated; committed and pushed as 5a2468d on Ziyun's go.

### 2026-10-06 (dl4dct: data loader for the stage 2 network, split by time)
Ziyun's plan: train on slices, 6 slices at 6 consecutive frames as input, the same slices of the ground truth as target,
YZ first; split frames 1-80 / 81-90 / 91-99.  Raised: YZ holds the whole motion of this phantom (bar along z,
bipyramid about x) but the limited-angle wedge lies in XY (suggested neighbor x slices as channels); the time split
tests extrapolation on one phantom (static parts shared, faster bar in test, 5 and 4 groups only, shared views at the
boundaries); suggested more SimRack datasets split by dataset.  Ziyun chose the split with the boundary frames dropped.
New `dl4dct/slice_data.py` (no MBIRTorch): SliceGroupDataset(recon_dir, split, plane yz/xz/xy, method, target,
frames_per_group 6, group_stride 1, context, skip_empty, preload, splits); DEFAULT_SPLITS train (0, 79), valid (80, 89),
test (90, 99), half-open, frames 79 and 89 unused.  Tests 8 (all 31 pass), docs clean.  Checked on Gautschi with the
baseline mbir.npy and the dataset GT through links (`output/2026/1006/slice_data_check/`): train 5032 samples (74 groups
x 68 non-empty x slices 31-98), valid 272, test 272; batch input (8, 6, 1, 130, 364); 52 samples/s with 4 workers; MBIR
inputs reach 0.112 (5 x plastic).  Not committed.  The plan of the first experiment is written in
`dl4dct_plans/idea_ziyun/plan.md` (decisions, data, samples, split, loader, limits, next steps); formulation.md points to it.
Committed and pushed on Ziyun's go: 9143297 (loader, tests, docs, CLAUDE.md), 0c987d9 (plan), 1b14f0d (README job number).  Partial recon job 16886735 (ai) est. start 2026-10-07 02:50.

### 2026-10-06 (dl4dct: stage 1 partial recons of SimRack-1, 120 deg frames, 50% overlap)
Found: SimRack-1 job 16850958 done 2026-10-04 (11 min); dataset moved by Ziyun to
`~/Desktop/data/dl4dct/datasets/SimRack-1/`; Ziyun's commits f26a4c1 (load_scan), b35d998/ea1a4a2 (baselines FDK/MBIR/
MACE4D on SimRack-1 with MBIRTorch 010043e, outputs output/2026/1005/simrack1_baselines/; MBIR NRMSE 0.325, MACE4D 0.142).
Ziyun asked for per-frame FDK and MBIR (120 deg, 50% overlap) saved in the dataset folder with the frame setting
labeled, for training the fusion network; more settings later.  New `dl4dct/partial_recons.py`: FrameSetting
(frames_per_rotation, overlap, start_view; label span120_step60_start0), frame_models (construct_time_frame_models with
a start offset), reconstruct_frames (sequential; MBIR seed = frame index, via rng or np.random.seed on d75f13e which has
no rng), make_partial_recons (writes <dataset>/partial_recons/<label>/ fdk.npy, mbir.npy, ground_truth_center.npy,
ground_truth_window_mean.npy, frames.json with views, rotation_deg, center times, recon settings, NRMSE); driver
settings sharpness 1.0, positivity, transmission_root, 15 its.  `experiments/partial_recons/` (script, sbatch, README).
tests/conftest.py gained a session tiny_dataset; 23 tests pass on both MBIRTorch 79d9600 and d75f13e; docs clean.
Committed and pushed as 4720b3f on Ziyun's go; the job's code copy matches 4720b3f byte for byte, and its DL4DCT_COMMIT now reads 4720b3f.  Job 16886486 (smallgpu) cancelled on Ziyun's request;
job 16886735 on ai (1 H100, -n14, 2 h, flags given on the sbatch command line; MBIRTorch d75f13e) pending.

### 2026-10-06 (static phantom jitter test: 60 deg frames, per-frame MBIR and MACE4D, job 16883322 submitted)
Ziyun asked whether a STATIC object jitters frame to frame: the NSI artifact phantom (JB-033, no metal) cut into 60 deg
frames with 50% overlap, MBIR of each frame on its own, plus MACE4D on the same frames; downsampling 2 and 1/4 of the views.
Data: `/depot/bouman/data/Lilly/demo_nsi_vert_no_metal_all_views.tgz` (1800 views, 0.2 deg, one 360 deg step scan, 1536 x
1920 detector), extracted to `~/Desktop/data/demo_nsi_vert_no_metal_all_views/` (the 200-view demo_data_nsi is too sparse).
At 1/4: 450 views, 0.8 deg apart; frames = MACE4DModel(frames_per_rotation=12, overlap 2): 75 views per frame, stride 38
views (30.4 deg; 37.5 rounds up), 10 frames in one turn.  10 frames < the filter period 12, so MACE4D runs with the
temporal filter off.  Model settings as the Lilly driver (sharpness 1, positivity, transmission_root weights).
`static_jitter_recon.py`: per-frame MBIR (default recon, one frame per GPU), full-turn MBIR reference, MACE4D (10 its).
`static_jitter_analysis.py`: each frame registered to the reference by 3D cross-correlation over the central 128
slices (Gaussian peak fit; recovers a known 1.5-voxel turning shift as 1.45 in a local test), first-harmonic fit
against the frame center angle, half-turn pair differences, figures.  Both scripts tested locally on a synthetic
cone-beam scan.  The login node kills the NSI loader at this size (memory), so there was no login-node smoke test.
Code `~/PycharmProjects/scripts/2026/1006/static_jitter/`, output `~/Desktop/data/output/2026/1006/static_jitter/`.
UPDATE: Ziyun asked for MACE4D with AND without the DCT filter.  One turn gives 10 frames, below the period 12, so
the turn is now used twice (copy at +360 deg; static object, same noise): 900 views, 22 frames, used by all three
reconstructions; reference = MBIR of the one real turn.  Job 16883322 cancelled before it started.  Jobs: 16883458
(--stage mbir: per-frame MBIR + reference), 16883459 (MACE4D nofilter), 16883460 (MACE4D dct), 16883461 (analysis,
afterany).  Output names: mbir_frames, mace4d_nofilter, mace4d_dct, reference (.npy, _center_slices.npz, _z.gif),
shifts.csv/png, frames_z.png.  Local synthetic test of all stages passed (DCT run: 'removes periods of 12, 6, 4, 3,
2.4, 2 frames').  Note: the stride rounds 37.5 to 38 views, so 12 frames span 364.8 deg (4.8 deg drift per turn).
UPDATE 2: Ziyun changed the frames to 120 deg with 50% overlap (frames_per_rotation 6) and asked for 8x view and 8x
detector downsampling.  Jobs 16883458-61 cancelled before start.  Now 225 views per turn (1.6 deg), two turns, frames of
75 views, stride 38 (37.5 rounded, 4.8 deg drift per turn), 10 frames; 1 GPU per job, 1 h.  Jobs: 16883982 (mbir),
16883983 (nofilter), 16883984 (dct), 16883985 (analysis).  Local test: with 11 frames at period 6 the DCT filter keeps
only 3 of 11 temporal modes, so the dct arm is close to a time average.
Ziyun keeps two turns (no 17-turn repeat).  Added stage fdk (per-frame recon_direct): job 16884275; analysis 16883985 now
also waits for it and measures fdk_frames.  Slide plan (Ziyun_26_1008, slide 3): rows FDK / per-frame MBIR / MACE no DCT /
MACE DCT, columns 4D phantom / static.  4D sources: FDK = output/2026/1001/init cache; MBIR = 0917
phantom_mbirtorch_full_slab2gb init cache (15 its); no DCT = 0924/sor_stage1/4d_nominal_nofilter; DCT = 1001.  Open: stride
at every 8th view is 38 views = 60.8 deg (not 60); every 12th view (2.4 deg, stride 25) would match exactly; asked Ziyun.
UPDATE 3 (final settings, on Ziyun's go): view downsampling 12 (150 views per turn, 2.4 deg; frames 50 views = 120 deg,
stride 25 views = 60 deg exactly, so 6 frames = 360 deg as in the 4D phantom), detector downsampling 8, THREE turns (450
views, 17 frames).  Jobs 16883982-85 and 16884275 cancelled before start.  New jobs: 16884363 fdk, 16884364 mbir,
16884365 nofilter, 16884366 dct, 16884367 analysis (afterany all four).  Lesson: when a view factor is chosen, check that
the frame stride is a whole number of views before submitting, and say so if it is not.
RESULTS (all jobs done 2026-10-06, 38 s to 4 min each): static geometry magnification 3.479, detector 0.127 mm, so the
ds8 voxel is 0.292 mm (4D phantom: 0.1196 mm).  Shift of each frame against the one-turn MBIR (voxels; mm):
FDK mean 0.217 (0.063 mm), first harmonic 0.21, half-turn pairs 0.31-0.52 (not a pure harmonic; FDK streaks bias the
registration); per-frame MBIR mean 0.056 (0.016 mm), first harmonic 0.055/0.057 (clear but tiny turning shift),
half-turn pairs 0.08-0.15 (0.02-0.04 mm); MACE4D no filter 0.012, DCT 0.010.  For scale, the 4D phantom's per-frame
shift at the nominal offset was 1.3-1.7 voxels (0.16-0.20 mm) and its FDK half-turn displacement 2.91 voxels (0.35 mm),
measured with other estimators.  So the static object with its own geometry barely jitters.  Slide GIFs and viewer:
`Slides/2026/1006/Claude outputs/static_jitter/` (side_by_side_{fdk,mbir}*.gif, make_side_by_side_gif.py, shifts.png,
frames_z.png); viewer runs on login06 from the Mac terminal panel (serve_viewer4d.py --frames 96, ports 28417/28418,
repeated static volumes static_{fdk,mbir}_first12_x8.npy in output/2026/1006/viewer/).

### 2026-10-05 (dl4dct: SimRack-1 baselines submitted)
Ziyun asked for FDK, MBIR and MACE4D baselines on SimRack-1 with the binning of the real MACE4D runs.  The real runs
(1001, 1005) used detector downsampling 1 and frames of 48 views, stride 24 (6 per rotation, overlap 2); SimRack-1 exists
only at detector binning 2, so "binning" was taken as the view binning, which equals the dataset's 99 windows.
dl4dct cloned on Gautschi at `~/PycharmProjects/dl4dct` (SSH remote; HTTPS needs a login).  New, uncommitted:
`dl4dct/experiments/simrack_baselines/run_baselines.py` (methods fdk, mbir, mace4d, mace4d_nofilter; the driver's
settings: sharpness 1.0, positivity, transmission_root, MACE4D driver defaults with the DCT filter, 10 its; FDK and MBIR
frames dealt to all visible GPUs, MBIR of frame k seeded with k; NRMSE per frame against both ground truths) and
`run_baselines.sbatch` (ai, 4 H100, METHODS env).  Code from archives dl4dct f26a4c1 + mbirtorch 010043e (the real runs'
recon code, FDK init) in `~/Desktop/data/output/2026/1005/simrack1_baselines/code/`; outputs `<method>.npy` and
`metrics_<method>.json` in that folder.  Ziyun declined the smoke tests.  Jobs 16872575 (fdk mbir, 0.5 h) and 16872576
(mace4d, 0.75 h) pending; ai had ~400 jobs pending.  Job 16872608 (mace4d_nofilter, 0.75 h) added on Ziyun's go.
Ziyun's correction: the limited angle of each frame also causes the period-6 jitter, so SimRack-1 has jitter even
with the exact offset (the 10-03 note that SimRack-1 lacks the jitter was wrong).
Results (all four jobs ran on h011 2026-10-05 19:56-20:56, exit 0).  NRMSE against ground_truth_center, mean [min, max]:
FDK 0.617 [0.597, 0.643] (0.4 min); MBIR 0.325 [0.304, 0.351] (16.4 min on 4 GPUs); MACE4D with DCT filter 0.142
[0.135, 0.154] (20.2 min, 10 its, change 0.87% at the end); MACE4D no filter 0.143 [0.136, 0.154] (20.1 min, change
1.03%).  Against window_mean, MACE4D 0.137/0.138.  The period-6 amplitude of the per-frame NRMSE (frames 6-92) is 0.0009
FDK, 0.0010 MBIR, 0.0011 MACE4D no filter, 0.0003 MACE4D with filter.  Neither MACE4D run reached the 0.2% stop.
Figures fig_nrmse.png and fig_slices_x65.png in the output folder: MACE4D smooths the rack teeth and loses the ball's
inserts.  A `smoke/` folder (FDK on SimRack-1-smoke, 16:17) exists although that tool call was rejected.
Committed with a README (results table) as b35d998 on dl4dct main, pushed on Ziyun's go; Gautschi clone pulled.
GIFs baselines_x65.gif and baselines_z182.gif (GT, FDK, MBIR, MACE4D filter, no filter, stacked; 99 frames) in the output folder.
Jitter on SimRack-1 (`jitter_metrics.json` in the output folder; x65 pixels that never change in the GT, first 96 frames):
temporal RMS on static edges FDK 0.0059 /mm (89% at harmonics 1-3, mostly k2 0.0074 amplitude, k1 0.0025), MBIR 0.0027
(67%), MACE4D no filter 0.00059 (32%, k1 0.00045), MACE4D DCT 0.00053 (2%, k1 0.00006).  Consecutive-frame wobble on z182
<= 0.024 voxel (0.006 mm) for every method: the limited-angle jitter is an intensity pattern, not a displacement.  Real
data, nominal offset, MACE4D no filter: 0.720 voxel at ds1 = 0.086 mm.  The shift-against-mean (first-harmonic shift)
metric fails on z182 (sparse slice, cross-correlation locks onto wrong peaks), so it is not reported.

### 2026-10-05 (full-res MACE4D with a one-turn FDK init, job 16872253 submitted)
Ziyun asked for a full-resolution MACE4D run on Phantom_30s_Run1 whose init uses more data: the MACE model keeps each
frame's 120 deg sinogram and projector, but frame t is initialized by FDK on the 144 views (360 deg) centered on the
frame's center view, cut at the scan ends (frame 0: 96 views, 240 deg; frame 1: 120 views, 300 deg; same at the end).
The aim is to put useful content in the null space of each frame.  Wrapper `run_with_fdk360_init.py` replaces only
`MACE4DModel._compute_init_recon`; driver defaults otherwise (nominal offset, DCT filter, 10 its).  Denoiser sigma_noise
and sigma_x pinned to the values of the 120 deg FDK baseline (job 16664243, output/2026/1001: 0.005993252620100975,
0.0006083836196921766), so the init is the only difference.  Gautschi checkout 4D_viewer 010043e (same recon code as
157deaa).  mbirtorch FDK has no short-scan weighting, so the cut end frames carry some streaks.  Smoke test on the login
node (ds8, 12 frames, 1 it, CPU) passed.  Code `~/PycharmProjects/scripts/2026/1005/fdk360_init/`, output
`~/Desktop/data/output/2026/1005/mace4d_fdk360_init/` (frame_windows.csv, init_center_slices.npz, init cache, recon).
Job 16872253 DONE 18:04 (h003, 0.44 h, 10 its).  Init: 18 s, range -0.54 to 0.37 (120 deg FDK: to -1.07), visibly
cleaner (no limited-angle streaks).  Consensus change it1 20.8% (baseline 57.5%), it5 2.9% (3.5%), it10 1.13% (1.15%).
Finals vs the 1001 baseline (`compare_with_baseline.py`, center slices): relative RMS difference median 0.76% (x130),
0.69% (y130), 0.89% (z364); end frames 0.7-1.2%; difference images show only faint edge residue.  For scale, two runs
with the same 120 deg init differed by 0.39%/0.36% (09-24 vs 09-23).  So after 10 iterations the init's extra content
is mostly gone: the final is set by the 120 deg data and the priors, not by the start.  Figures, CSVs and scripts copied
to `Lilly/4DCT/Slides/2026/1005/Claude outputs/fdk360_init/`.

### 2026-10-05 (dl4dct: SimRack-1 made)
Job 16850958 ran on g003 (L40S) 2026-10-04 03:20-03:31, exit 0; smoke run first, then the full dataset in 571 s.
`~/Desktop/data/output/2026/1003/datasets/SimRack-1/` (5.4 GB: sinograms 2400 x 364 x 130, ground truth
99 x 130 x 130 x 364, config, README, checks, fig_checks.png) and `SimRack-1.zip` (0.44 GB).  Checks: per-view vs batched
7.3e-8; reprojection residual of the GT against the clean sinogram 0.058-0.062 (0.097-0.102 with the channel offset moved
by one channel); single-window MBIR NRMSE 0.338 (window 0) and 0.314 (window 49), 15 iterations each.  Not yet uploaded to Box.
Moved on Ziyun's request (same day) to `~/Desktop/data/dl4dct/datasets/SimRack-1/` and `.../SimRack-1.zip`; smoke,
code archives and Slurm logs stay in the job's output folder.
`dl4dct.datasets.load_scan(sinogram_path, config_path)` -> (memory-mapped sinogram, model), shape-checked; verified that
`mbirtorch.utilities.construct_time_frame_models` (defaults 6, 2.0; not exported at top level) gives 99 frames equal to the
99 windows on the GT grid.  Committed f26a4c1 on dl4dct main and pushed on Ziyun's go (18 tests pass, docs clean).

### 2026-10-03 night (dl4dct: Ziyun's formulation of the fusion network)
`dl4dct/dl4dct_plans/idea_ziyun/formulation.md`, committed and pushed as 6148013.  Ziyun's idea: a network takes 6
consecutive partial reconstructions (120 deg, 50% overlap, together a full turn) with their angle ranges and returns 6
jitter-free, motion-corrected frames; frames split into consecutive groups of 6, no combining; trained on simulated 4D
data with every start angle; initial design processes 2D (x, y) slices one z at a time; padding (same voxel size,
symmetric so the axis stays centered) for other (x, y) sizes; later, more output frames than input frames.  Raised in
chat, not in the doc: the real motion (rack along z, gears about x) is out of the (x, y) plane, so a 2D slice network
cannot move content along z (suggested a few neighboring z slices as channels); seams between groups; frame counts
not a multiple of 6; the real jitter is mostly the channel-offset rotating shift, absent from SimRack-1.

### 2026-10-03 (4D viewer: checked for a pull request into prerelease)
Greg merged prerelease into 4D_viewer (79528af); the branch merges cleanly into prerelease, the PR target per the CI
config.  On the merged branch: full suite 226 passed, 92 skipped; docs build without warnings, with the three 4D viewer
sections intact; TkAgg drove both rows in x-y and t-y (8 steps per second, 20 asked) and wrote GIFs with no errors.  Qt
is untested (no Qt bindings installed).  Two faults fixed and pushed on Ziyun's go: the GIF folder dialog let a
FileExistsError escape when the path named an existing file (c601c29, with a test), and the docs figures lacked the
GIF buttons that the text describes (79d9600).  Left before opening the PR: one click on the GIF button's macOS
folder panel in a real window, Ziyun's decision on the space-time GIF aspect, and the PR description (with the two
3D viewer faults that the 4D viewer works around: the Retina menu position and dialogs in figures taller than 8 in).

### 2026-10-03 night (dl4dct: SimRack-1 named; dataset code in the package, committed)
Ziyun asked for a dataset name allowing easier or harder datasets later, and for the dataset code to be committed.
Name: SimRack-1 (family SimRack; each later dataset described by how it differs from SimRack-1; a recipe in use is never
changed).  Package: `dl4dct/phantoms.py` (RackPhantom from a parameter dict, torch only, shipped in each dataset),
`dl4dct/scan_simulation.py` (model_params/select_params/build_model/binned_params, view_schedule,
simulate_transmission, bin_and_add_noise, ground_truth_frames, checks), `dl4dct/datasets.py` (DatasetSpec, DATASETS,
make_dataset, load_model, window_views, dataset_readme), `dl4dct/dataset_load_example.py`; `experiments/datasets/`
(make_dataset.py with --smoke, run_make_dataset.sbatch with NAME, README with the dataset table); tests (18 pass, 19 s),
docs build clean.  The package reproduces the earlier script bit for bit.  Committed 5f71a95 and 3f4e660 (import check
compares resolved paths: ~/Desktop/data links to /scratch) on dl4dct main, pushed to origin/main on Ziyun's go.  Job 16850863 cancelled; job
16850958 (smallgpu, NAME=SimRack-1, code from git archives dl4dct 3f4e660 + mbirtorch d75f13e in
`~/Desktop/data/output/2026/1003/datasets/code/`) pending.  Output `~/Desktop/data/output/2026/1003/datasets/SimRack-1/`
and `SimRack-1.zip`.  The old folder output/2026/1003/sim_dataset_v1 holds only an unused MBIRTorch archive.

### 2026-10-03 evening (dl4dct: simple moving phantom and simulated dataset v1)
Ziyun asked for a simple moving phantom with structure comparable to the real scan, then a dataset made with MBIRTorch on
Gautschi, with a config that builds the CBCT model, zipped for Box.  Phantom (`dl4dct/experiments/sim_dataset_v1/phantom4d.py`,
torch, signed distances with partial-volume edges): toothed bar moving along z like the measured rack (0.98 -> 1.43 mm/s,
35.6 mm), a triangular bipyramid with an off-center hole turning about x (pitch radius 5 mm), a static frame cylinder
r 8 mm with slot and pocket (the pocket overlaps the slot by 1 mm; a shared face left a half-value line, fixed), three
0.6 mm plates at 0/60/120 deg, a ball with an air hole and a 0.019 insert.  GIFs in ~/Downloads/sim_phantom_gifs/.
`make_dataset.py`: real geometry (Step 0 geometry_ds1.json, nominal offset), 2400 views, each the mean transmission over 5
sub-angles at their own times, moving parts projected one view at a time (forward_project_differentiable with one-view
copies), static parts once, native detector and full-res grid padded 3.2 mm in z, binned 2 x 2 like the loader; Poisson
I0_native 11000 (matches real ds2 air variance 2.27e-5); GT at window centers and window means, 99 x 130 x 130 x 364.
config.json: model (binned) and model_full_resolution as build_model params, schedule, windows, noise, phantom.  Local
test (96 views at ds4, CPU): per-view = batched exactly; reprojection residual 5.7% vs 14-15% with a one-channel offset
error; single-window MBIR NRMSE 0.30-0.33.  Job 16850863 (smallgpu, 1 L40, -n64 required, 1.5 h; MBIRTorch d75f13e from
a git archive in the output folder) pending, est. start 2026-10-04 night.  Output
`~/Desktop/data/output/2026/1003/sim_dataset_v1/` (sim_4dct_phantom_v1/ and .zip).  Not committed.

### 2026-10-03 later (dl4dct simulation Step 0 written and submitted)
Plan pushed to dl4dct main (c1d7b27, a5fe3be: ground truth described as a 4D array kept as a recipe, sampled at every
view time).  Step 0 (`dl4dct/experiments/sim_step0/`, commit 4305bc6): `measure_real_scan.py` measures from the 0924
`4d_corrected_nofilter` recon (job 16672779) the moving parts, rack ends and speed, tooth pitch, gear angles (tooth
harmonic phase, rack band excluded) with a mesh check, I0 from views one turn apart, and saves the geometry JSON.
Synthetic checks passed (rack speed 0.593/0.878 vs 0.602/0.873, pitch 11.95 vs 12, gear angle -194.1 vs -194.2, mesh
ratio 0.996, I0 4932 vs 5000).  Prototype on x130: THREE gears move; the middle gear (z~400, 12 teeth) starts turning
near frame 40 when the rack end reaches it; rack speed by one-turn steps 1.09 -> 1.49 mm/s; all gear angles dip in
frames 80-90 (rack does not slow; to be tested by the mesh check).  Job 16850200 (cpu partition, standby QOS, accepted),
code copy `~/PycharmProjects/scripts/2026/1003/sim_step0/`, outputs `~/Desktop/data/output/2026/1003/sim_step0/`.

### 2026-10-03 (dl4dct: plan for simulated 4D scans)
Ziyun asked for the basic facts of the real scan (`Phantom_30s_Run1`, `.nsipro` copy in `Slides/2026/0820/`) and a plan
to simulate scans with MBIRTorch for training the dl4dct stage 2 model.  Plan written to
`dl4dct/dl4dct_plans/simulation_plan.md` (not committed).  Facts: 2400 views, 2.5 deg each, 80 fps, 12.5 ms integration
(the full frame period, so 2.5 deg rotation smear per view: 5.5 voxels at r = 15 mm), 30 s, 16.67 turns, 1.8 s per turn;
SDD 698.2, SID 328.7, magnification 2.124, voxel 0.1196 mm, recon 260 x 260 x 728 (728 = rotation axis); object is a rack
and pinion phantom of one plastic (~0.023 /mm).  Rack speed measured from the x130 GIF of the corrected no-filter MACE4D
run: 1.20 mm/s on average, 0.97 rising to 1.43 mm/s, about 35 mm over the scan.  Default design: random rack and pinion
phantoms on the full-res grid, per-view projection of the moving part with 5 sub-angles, Poisson noise matched to the
real I0, stage 1 at downsampling (2, 2) with 48-view windows and step 24, true frames at window center times.

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

### 2026-09-30 (GOAL stated by Ziyun: find the jitter frequency blindly)
Ziyun's goal for the theory work: detect the irregular (jitter) frequency from the reconstructed frame stack by computing
something, WITHOUT using the known period of 6 frames.  This is the main difference from the DCT filter, which is built on
knowing the period.  Findings so far that bear on it (36 frame fan beam stack, scratchpad plots, not in exp.tex): with no
frequency marked, the diagonal of Lambda_hat shows exactly 6 nonzero bins spaced 6 apart (k = 0, +-6, +-12, -18); the block
pattern of Lambda_hat and the frame correlation x_t^t x_t' (6 x 6 tiles, lag 6 correlation 1 after removing the mean) show the
same period; a moving object makes the frame correlation smooth, not tiled (cyclostationary signature of the jitter).

### 2026-09-30 (36 frames over 6 turns: the period 6 harmonics fall on DFT bins)
`frame_svd36.py` in `Slides/2026/1001/Claude outputs/frame_svd/` (README section): 120 deg frames, stride 60 deg (50% shared),
2220 views (6 turns give 35 frames, so plus 60 deg) -> 36 frames.  n/6 cycles/frame = bins 6, 12, 18 exactly (36 is a multiple
of 6).  Static X: all energy at 0 and on those bins (1e-15 elsewhere); fan 0.919 / 0.030 / 0.041 / 0.0095, parallel 0.934 / 0 /
0.065 / 0; ranks 3 and 6 as before.  Moving disk (one cycle in 36 frames): 3.3% of the energy off those bins; in fan beam some
modes mix the motion and the frame artifact (v_2: 0.75 at 2/6, 0.10 at 1/36).
- exp.tex (Theory project, 4 pp) holds ONE experiment only, on Ziyun's request: fan beam, static Shepp-Logan, 36 frames
  (figures `exp_fig1_overview.png`, `exp_fig2_spectra.png`: two-sided DFT of all 36 bases, jitter bases v2..v6 in red; the pinv write-up, parallel and moving cases removed from the doc and the project
  figures; frame_svd36.py now runs only this case).  Content: rank 6, energy 0.919 / 0.030 / 0.041 / 0.0095 at 0, 1/6, 2/6, 3/6;
  v4, v5 carry mostly 1/6 (0.88, 0.76) but all of v2..v6 overlap it; the index ranks energy, not frequency; neighboring harmonic
  images not orthogonal (0.13-0.18), so the SVD mixes them; the DFT of X over frames at bins 6, 12, 18 isolates the jitter.

### 2026-09-30 (temporal frequencies of the SVD of a stack of 18 frame reconstructions)
Ziyun asked: 3-turn scan split by `construct_time_frame_models` into 18 frames, per-frame pinv reconstructions stacked as
X (N x 18), SVD, DFT of the 18 columns of V.  `Slides/2026/1001/Claude outputs/frame_svd/` (README, 5 min, 48 x 48).  With 1080
views the default 120 deg frames give 17 frames, so two cases: 1080 views with 60 deg frames (overlap 1) and 1140 views with
the default 120 deg frames.  Static object: X has rank 3 in parallel beam (P_(t+3) = P_t) with energy only at 0 and 2
cycles/turn, and rank 6 in fan beam (magnification 2.124) with energy at 0, 1, 2, 3 cycles/turn (1e-28 elsewhere); modes come in
cos/sin pairs.  The 1 cycle/turn (period 6) content appears in fan beam with a correct geometry, from the frame construction
alone: 3.0% of the static X energy (120 deg frames), 4.3% (60 deg).  A moving disk (one cycle over the scan) makes X full rank
and fills the non-integer frequencies.

### 2026-09-30 (numerical checks of the Theory note on a small Shepp-Logan phantom)
Ziyun asked for simple experiments on the quantities of `Sensor Orthogonal Reconstruction -- Theory/main.tex`.  Script,
four figures and README in `Slides/2026/1001/Claude outputs/theory_pinv/` (5 s, numpy only; 32 x 32 image, disk field of
view of radius 15, 12 parallel views, M = 336, N = 1024).  Every identity of the note holds to 1e-13 (xhat = Px, A xtilde = 0,
P symmetric and idempotent, orthogonal split, the two Lambda_hat expressions); R_xhat = P R_x P^t confirmed by Monte Carlo
with 1/sqrt(n) error.  Shepp-Logan keeps 0.92 of its energy in Range(A^t); diag(F P F^H) is the star of the view angles plus
a low-frequency disk.  Lambda_hat has 42% of its energy off the diagonal, but P = D (field of view only) already gives 41%,
so the views mainly remove diagonal energy; the off-diagonal share of F P F^H itself is 0.30 for D and up to 0.54 at 8 views.
Circulant P (Fourier rows) gives a diagonal Lambda_hat.  Without the field-of-view cut, A A^t is singular (cond 4.6e18,
corner-grazing rays); with it, cond(A A^t) still grows from 1e2 (2 views) to 2e9 (24 views): no gap in the singular values.
Was written up in exp.tex, then removed on Ziyun's request (exp.tex holds only the 36 frame experiment).

### 2026-09-30 (GIF of the MACE4D scheduler)
- Made `mace4d_queue_iter4.gif` in `Slides/2026/1001/Claude outputs/mace4d_queue_gif/`. It replays iteration 4 of the task log of the 0924 `sor_stage1/4d_corrected_dct` run (99 frames, 4 H100s), which ran the current `MACE._run_threaded` scheduler. `make_queue_gif.py --iteration N` renders any other iteration.
- The log shows a critical path. The worker that finishes the last data-fit frame also runs the temporal filter and fold, which took about 17 s in iteration 4. That worker took no slabs, and the step ended with the filter at 169.5 s, 0.7 s after the last slab ended.

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
