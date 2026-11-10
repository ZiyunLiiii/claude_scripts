# Paths & Locations

## Dropbox
- Root: /Users/a124601/Library/CloudStorage/Dropbox
- Overleaf projects: /Users/a124601/Library/CloudStorage/Dropbox/Apps/Overleaf

## Notable Projects
- Lilly Proposal (LaTeX): /Users/a124601/Library/CloudStorage/Dropbox/Apps/Overleaf/Proposal_4D_Lilly/main.tex
- IPMR paper (plastic-metal BHC, LaTeX, Overleaf via Dropbox): /Users/a124601/Library/CloudStorage/Dropbox/Apps/Overleaf/Iterative Plastic Metal Reconstruction (submitted version in original-submission-backup/). Simulation repo: /Users/a124601/Desktop/Research_Purdue/repository/IPMR_simulation. Figure and metric scripts: /Users/a124601/Desktop/Research_Purdue/Lilly/MAR/IPMR_paper/Figures/v2_code (simulation_2_metal.py / simulation_6_metal.py compute Table IV; plot_simulation_*_metal.py make Figs 3-4; spectrum.py plots the spekpy 95 kVp, 12 deg, 2.5 mm Al source spectrum with its mean and std, shown with plt.show() and saved by hand as Figures/v2/IPMR_simulation/simulation_spectrum.pdf; plot_mass_attenuation.py plots mu/rho from material_attenuation.yaml; the same spectrum code lives in repository/IPMR_simulation/simulation_spectrum.py and utilities.gen_spectrum). Revision figure scripts (2026-11-06, PyCharm project): /Users/a124601/Desktop/Research_Purdue/Lilly/MAR/IPMR_paper/Revision_codes, output PDFs in /Users/a124601/Desktop/Research_Purdue/Lilly/MAR/IPMR_paper/Revision_figures; the paper includes Figures/simulation/simulation_spectrum.pdf inside the Overleaf folder. Saved simulation volumes (256^3): /Users/a124601/Desktop/Research_Purdue/Lilly/MAR/IPMR_paper/data_for_MAR_paper/simulation/{two_rods,six_rods}
  NSI phantom (JB-033) plastic-volume analysis from Lilly (VGStudio, source of Table V): /Users/a124601/Desktop/Research_Purdue/Lilly/MAR/IPMR_paper/MBIR VS other methods volume quantification_Lilly.pptx and MBIR_Object_Volume_Executive_Summary.pdf in the same folder. Half-resolution NSI recons (748x748x804, incl. no-metal MBIR): .../IPMR_paper/data_for_MAR_paper/demo/. Response letter: <Overleaf IPMR folder>/revision-v1/response_letter.tex
  IPMR parameter sensitivity on the single-metal simulation (2026-11-04; order, beta, alpha, gamma, passes): scripts, README, and later the metrics and figures in /Users/a124601/Desktop/Research_Purdue/Lilly/MAR/IPMR_paper/sensitivity; Delta folder /work/nvme/bjda/zli98/ipmr_sensitivity/ (out/<knob>/ holds the volumes)
  IPMR revision (2026-11-08): NMAR volumes /Users/a124601/Desktop/Research_Purdue/Lilly/MAR/IPMR_paper/Revision_data/nmar_baseline/; revised figure scripts .../IPMR_paper/Revision_codes; revised figure panels .../IPMR_paper/Revision_figures (previews/ has one PNG per figure)
  NMAR baseline for the IPMR paper (2026-11-05): repo /Users/a124601/Desktop/Research_Purdue/repository/NMAR_reproduction (GitHub ZiyunLiiii/NMAR_reproduction; method/nmar_pseudocode.md, package nmar/, tests/, experiments/run_simulation.py), run with ~/anaconda3/envs/nmar/bin/python (mbirjax 0.7.3, jax 0.12, spekpy 2.5.4, scikit-image; made 2026-11-05). The paper: /Users/a124601/Desktop/Research_Purdue/papers/MAR/NMAR.pdf
  MBIR-BHC paper (Jin, Bouman, Sauer, IEEE TCI 2015; a second baseline for the IPMR paper, 2026-11-09): /Users/a124601/Desktop/Research_Purdue/papers/MAR/tci03.pdf
  MBIR-BHC baseline for the IPMR paper (2026-11-09): repo /Users/a124601/Desktop/Research_Purdue/repository/MBIR-BHC_reproduction (GitHub ZiyunLiiii/MBIR-BHC_reproduction; method/mbir_bhc_method.md, package mbir_bhc/, tests/, experiments/small_phantom/run_small_phantom.py), on the mbirtorch projectors; run with ~/anaconda3/envs/mbirtorch/bin/python from the repo root (the package is not installed in that env). Charlie's blueprint for it: https://claude.ai/artifact/KkFcGjkMhvdDfW5XSM5um9 (index, theory.html, software-architecture.html, user-api.html)
  MBIR-BHC 2D check against the 2015 paper (2026-11-09): experiments/paper_2d/ in that repo (README.md, make_spectrum_and_materials.py run with ~/anaconda3/envs/nmar/bin/python for spekpy, spectrum_and_materials.json, run_paper_2d.py, ideal_coefficients.py, delta/). On Delta: code /u/zli98/mbir_bhc/code/{mbirtorch (git archive of 296f738), MBIR-BHC_reproduction}, copied with experiments/paper_2d/delta/copy_to_delta.sh; Slurm logs /u/zli98/mbir_bhc/slurm_logs/<case>_<job>.out; results /u/zli98/mbir_bhc/out/paper_2d/<case>/ (results.json, images.npz); conda env mbirtorch of Delta; local copy of the results with summary.md and figures (made by experiments/paper_2d/summarize_paper_2d.py in the nmar env): /Users/a124601/Desktop/Research_Purdue/Lilly/MAR/IPMR_paper/mbir_bhc_baseline/paper_2d/
  MBIR-BHC on the IPMR datasets (2026-11-09 night): scripts experiments/ipmr_simulation/ and experiments/nsi_scans/ in that repo. On Delta: simulation data /u/zli98/mbir_bhc/data/ipmr_simulation/<two_rods|six_rods>/ (sino.npy, gdt.npy, settings.json, mbirjax fdk.npy and mbir.npy from the NMAR run), simulation results /u/zli98/mbir_bhc/out/ipmr_simulation/<case>/, measured-scan volumes /work/nvme/bjda/zli98/mbir_bhc/out/nsi_scans/<circuit_board|nsi_phantom>/ with results.json copied to /u/zli98/mbir_bhc/out/nsi_scans/<case>/
  IPMR run-time study for the reviewers (2026-11-05; FDK, MBIR, IPMR of the full-size NSI phantom and circuit board with the time of every IPMR step, GPU memory, and the two simulation phantoms): scripts and README in /Users/a124601/Desktop/Research_Purdue/Lilly/MAR/IPMR_paper/timing; Gautschi code ~/PycharmProjects/scripts/2026/1105/ipmr_timing/ (venv ~/venvs/mbirjax, mbirjax 0.7.3), outputs ~/Desktop/data/output/2026/1105/ipmr_timing/<run>/
  IPMR segmentation robustness test for Reviewer 3 comment 1 (2026-11-09; IPMR with a changed segmentation on the single-metal simulation and on the NSI phantom at the downsampling of the paper's figures): scripts and README in /Users/a124601/Desktop/Research_Purdue/Lilly/MAR/IPMR_paper/segmentation_robustness; Gautschi code ~/PycharmProjects/scripts/2026/1109/ipmr_segmentation/ (venv ~/venvs/nmar, mbirjax 0.6.15; code/IPMR_simulation at 14e7913), outputs ~/Desktop/data/output/2026/1109/ipmr_segmentation/<sim|nsi>/<ref|morph|method|threshold>/ (smoke/ holds the smoke test)
  NMAR baseline on Gautschi (2026-11-05): code ~/PycharmProjects/NMAR_reproduction (rsync of the Mac repo; experiments/gautschi/submit_nmar.sbatch takes DATASET=smoke|two_rods|six_rods|nsi_phantom|circuit_board), job folder ~/PycharmProjects/scripts/2026/1105/nmar_baseline/ (slurm_logs/, IPMR_simulation/ at 14e7913, README.md), outputs ~/Desktop/data/output/2026/1105/nmar_baseline/<dataset>/, venv ~/venvs/nmar (python of /apps/external/conda/2025.09, jax cuda12, mbirjax 0.6.15, spekpy; built with the proxy variables unset because squid was down and the conda cache was corrupted)
  NMAR baseline on Delta (2026-11-05): code /u/zli98/nmar_baseline/code/{NMAR_reproduction,IPMR_simulation} (tar over ssh from the Mac; experiments/delta/submit_nmar.sbatch, submit_nmar.sh, extract_scans.sh), scans extracted by extract_scans.sh into /u/zli98/nmar_baseline/data/ (tarballs symlinked from /work/nvme/bjda/zli98/ipmr_timing/data/, marker files <name>.EXTRACTED), Slurm logs /u/zli98/nmar_baseline/slurm_logs/, outputs /work/nvme/bjda/zli98/nmar_baseline/out/<dataset>/, env /work/nvme/bjda/zli98/ipmr_six_rods_pet/env (mbirjax 0.6.15, the one of the sensitivity sweeps) with the repo on PYTHONPATH; local copy of the results /Users/a124601/Desktop/Research_Purdue/Lilly/MAR/IPMR_paper/nmar_baseline/ (README.md with the tables and the comparison with IPMR, <dataset>/ metrics, settings, slices.png and logs, scripts/, delta_report/); the volumes are only on Delta
  Paper real-data volumes on Gautschi: NSI phantom 748x748x804 in ~/Desktop/data/output/2026/0319/demo/ (recon_demo_fdk, mbir_recon_demo, recon_3_1_demo_alpha1_beta0_gamma0.1; the local demo/ copies), circuit board 363x363x251 in ~/Desktop/data/output/2026/data_for_MAR_paper/circ/circ_stable/ (made with scripts/2026/0611/mar_recon.py settings: downsample [4,4], every 4th view, auto crop). Datasets demo_nsi_vert_metal_all_views and Horizontal_Elec_Board_1800 were restored from depot on 2026-11-05 (tarballs now symlinks to depot)
- MACE/MACE4D API deck (beamer, Overleaf via Dropbox): /Users/a124601/Library/CloudStorage/Dropbox/Apps/Overleaf/MBIRTorch_4DCT_API/main.tex
- Sensor Orthogonal Reconstruction note (LaTeX, Overleaf via Dropbox): /Users/a124601/Library/CloudStorage/Dropbox/Apps/Overleaf/Sensor Orthogonal Reconstruction/main.tex
- Wedge experiment for that note (scripts, arrays, figures, README): /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT/Slides/2026/0924/Claude outputs/wedge_experiment — moved there from mbirtorch/Claude outputs (no longer in the repo); run with the mbirtorch env from that directory
- Theory checks for that note (numpy exact-SVD parallel-beam checks, 2026-09-24): /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT/Slides/2026/0924/Claude outputs/theory_checks
  (subfolder `placement/`, 2026-09-28: where the filter H belongs in the MACE loop; README there)
- Static-object and calibration tests for that note (copies of outputs, job scripts, plotting scripts, README): /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT/Slides/2026/0924/Claude outputs/static_tests
- Static-object null-space test and calibration sweep for that note (Gautschi): code `~/PycharmProjects/lilly_exp/nsi/2026/0924/static_nullspace/`, outputs `~/Desktop/data/output/2026/0924/static_nullspace/` and `.../0924/calib_offset/`; static data extracted to `~/Desktop/data/demo_data_nsi/` (from /depot/bouman/data/Lilly/demo_data_nsi.tgz — there is no .npz; 200 radiographs of the static JB-033 artifact phantom, one turn)
- Offset justification doc (the period-6 jitter: frame construction direct cause, axis offset fundamental cause): /Users/a124601/Library/CloudStorage/Dropbox/Apps/Overleaf/Sensor Orthogonal Reconstruction/offset_justification.tex (experiment log: experiment_status.tex in the same folder)
- Offset slides (beamer, 3 slides with animate-package animations of the x130 slice): /Users/a124601/Library/CloudStorage/Dropbox/Apps/Overleaf/Sensor Orthogonal Reconstruction/offset_slides.tex (frames in figures/anim/; set it as the main document in Overleaf to compile)
- Stage 1 of the sensor-orthogonal plan (corrected-offset 4D runs, survey, sweep, convergence): code on Gautschi `~/PycharmProjects/lilly_exp/nsi/2026/0924/sor_stage1/`, outputs `~/Desktop/data/output/2026/0924/sor_stage1/`; copies of small outputs, scripts and README: /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT/Slides/2026/0924/Claude outputs/sor_stage1
- Sensor Orthogonal Reconstruction -- Theory (LaTeX, Overleaf via Dropbox; Ziyun's own theory notes, started 2026-09-28): /Users/a124601/Library/CloudStorage/Dropbox/Apps/Overleaf/Sensor Orthogonal Reconstruction -- Theory/main.tex
- SOR blueprints (Ziyun's newest formulation, 2026-10-27; index with Theory, Theory 2, Software Architecture pages): https://claude.ai/artifact/648swpno4LjUtjvxwcf8jS
- SOR random-center-angle test (2026-10-27; per-frame MBIR of SimRack-1 arc datasets with periodic, shuffled and random frame centers): code on Gautschi `~/PycharmProjects/scripts/2026/1027/sor_random_angle/`, datasets `/home/li5273/Desktop/data/sor/datasets/SimRack-1-arcs-{periodic,shuffled6,random}/` (scratch), output `~/Desktop/data/output/2026/1027/sor_random_angle/`; local README and scripts: /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT/Slides/2026/1027/Claude outputs/sor_random_angle
- SOR, 60 degree frames cut from the SimRack-1 scan (2026-10-29; periodic only, 199 frames of 24 views): dataset `/home/li5273/Desktop/data/sor/datasets/SimRack-1-frames-periodic-fpr12-arc60/`, results `~/Desktop/data/output/2026/1027/sor_random_angle/arc60/` on Gautschi (job scripts/run60.sbatch in the same scripts folder; Delta copy in /work/nvme/bjda/zli98/sor_random_angle/arc60/ if it runs there)
- SOR, FDK and MACE4D (DCT, SOR p = 6) of the 60 degree frames (2026-11-04, Delta): `/work/nvme/bjda/zli98/sor_random_angle/arc60/` (fdk/, mace_dct/, mace_sor_p6/, smoke_mace/), dataset `/work/nvme/bjda/zli98/sor_random_angle/datasets/SimRack-1-frames-periodic-fpr12-arc60/`; scripts run_mace60.py, prep60_delta.sbatch, mace60_delta.sbatch in the sor_random_angle scripts folder
- Measured phantom Phantom_30s_Run1 in 60 degree frames (2026-11-04, Delta, full resolution; FDK, MBIR, MACE-DCT, MACE-SOR p = 6): `/work/nvme/bjda/zli98/real60/` (scan/ = copy of the NSI scan, prep/, fdk/, mbir/, mace_dct/, mace_sor_p6/, smoke_*/, slurm_logs/); scripts run_real60.py, real60_prep_delta.sbatch, real60_delta.sbatch in the sor_random_angle scripts folder
- SOR, 60 degree arc datasets in three orders (2026-10-29, forked session; 199 frames of 24 views at 12 fpr, periodic, shuffled, random; SOR p = 3 and 8): code on Gautschi `~/PycharmProjects/scripts/2026/1029/sor_arc60/` (its own snapshot of the 10-27 scripts), datasets `/home/li5273/Desktop/data/sor/datasets/arc60_orders/`, output `~/Desktop/data/output/2026/1029/sor_arc60/`; Delta fallback `/work/nvme/bjda/zli98/sor_arc60/`; local README and scripts: /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT/Slides/2026/1029/Claude outputs/sor_arc60
- SOR prior-art literature search (2026-11-05; review README.md with verification levels and prior_art.bib of about 110 entries): /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT/Slides/2026/1105/Claude outputs/sor_literature/
- FuSe2 workshop deck on 4D CT (2026-10-31, 12 slides): current version /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT_FuSe2_v7.pptx (earlier versions 4DCT_FuSe2.pptx and _v2 to _v6 beside it); speaker notes in scripts/speaker_notes.py; GIFs, figures, scripts, README, and a copy of the template 4DCT_presentation.pptx in template/: /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT/Slides/2026/1031/Claude outputs/fuse2_deck (build_deck.py rebuilds 4DCT_FuSe2_v7.pptx and overwrites it)
- Core properties of the periodic removal (zero mean of the temporal bases, the two forms X - sum s_r u_r v_r^t = X(I - V_Omega V_Omega^t), mean kept, orthogonal projection, at most P - 1 periodic components; 2026-10-17): /Users/a124601/Library/CloudStorage/Dropbox/Apps/Overleaf/Sensor Orthogonal Reconstruction -- Theory/core_properties.tex (+ .pdf; set it as the main document in Overleaf to compile). The earlier periodic_modes_derivation.tex is no longer in the folder; its numerical check code/periodic_modes/check_projection.py is still there
- Numerical checks of the old Theory note, whose theory was replaced on 2026-10-21 (pseudo-inverse split, P, R_xhat, Lambda_hat on a 32 x 32 Shepp-Logan, 2026-09-30; script, figures, README): /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT/Slides/2026/1001/Claude outputs/theory_pinv
- SVD of a stack of 18 frame reconstructions and the DFT of its temporal bases (parallel and fan beam, 2026-09-30; script, figures, README): /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT/Slides/2026/1001/Claude outputs/frame_svd
- MACE4D scheduler GIF (one consensus step replayed from the 0924 sor_stage1/4d_corrected_dct task log; script, log copy, GIF): /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT/Slides/2026/1001/Claude outputs/mace4d_queue_gif
- Diffusion tutorial (LaTeX, Overleaf via Dropbox; organizes and explains the MIT 6.S184 flow/diffusion lectures, started 2026-09-30): /Users/a124601/Library/CloudStorage/Dropbox/Apps/Overleaf/Diffusion/main.tex (preamble.tex, sections/00-13, figures/; regenerate figures with `python scripts/make_figures.py`, test the closed forms with `python scripts/test_toys.py`). Source slides (5 PDFs, Lectures 1-5): /Users/a124601/Desktop/Research_Purdue/misc/Diffusion/
- Diff Transformer notes (LaTeX, Overleaf via Dropbox; study-group summary of Ye et al., "Differential Transformer", ICLR 2025, started 2026-09-30): /Users/a124601/Library/CloudStorage/Dropbox/Apps/Overleaf/Diff Transformer/main.tex. Paper PDF: /Users/a124601/Desktop/Research_Purdue/Study_Group/2410.05258v2.pdf (the Study_Group/ folder holds the study-group papers). Q&A note (ten questions, 2026-10-01): /Users/a124601/Library/CloudStorage/Dropbox/Apps/Overleaf/Diff Transformer/qa.tex (set it as the main document in Overleaf to compile; figures/ holds its five PNGs; regenerate them from that folder with `python scripts/make_figures.py <example|temperature|rmsnorm|swiglu|fit_replot>`)
- Code Review Schedule (website): /Users/a124601/Desktop/Code_review/code-review-schedule (a stale copy from 2026-08-31 sits at ~/Desktop/Misc/code-review-schedule; ignore it) — React+Vite+TS, remote git@github.com:ZiyunLiiii/code-review-schedule.git, live at https://ziyunliiii.github.io/code-review-schedule/ (GitHub Pages via Actions). Manages weekly Fri 3:30 PM Code Review meetings; semester config in src/utils/persistence.ts (DEFAULT_SEMESTER_CONFIG).

## 4DCT / mbirjax repos
- 4DCT (Mac): /Users/a124601/Desktop/Research_Purdue/repository/4DCT — branch `refactor_for_mbirjax`, remote git@github.com:cabouman/4DCT.git
- mbirjax (Mac): /Users/a124601/Desktop/Research_Purdue/repository/mbirjax — branch `4DCT_for_merging`, remote git@github.com:cabouman/mbirjax.git
- Local test env: `~/anaconda3/envs/mbirjax_test/bin/python`. mbirjax is installed there
  NON-editable, so run pytest from the mbirjax repo root, and set
  `PYTHONPATH=/Users/a124601/Desktop/Research_Purdue/repository/mbirjax` for scripts run from
  anywhere else — otherwise the stale site-packages copy is imported silently.

## dl4dct
- dl4dct (Mac): /Users/a124601/Desktop/Research_Purdue/repository/dl4dct — plans in `dl4dct_plans/`
  (simulation plan: `simulation_plan.md`, 2026-10-03)
- dl4dct simulated datasets (SimRack-1, ...): code in the dl4dct package (`phantoms.py`, `scan_simulation.py`, `datasets.py`)
  and `experiments/datasets/`; finished datasets on Gautschi in `~/Desktop/data/dl4dct/datasets/` (`<name>/`, `<name>.zip`;
  SimRack-1 moved there 2026-10-05); the job still writes to `~/Desktop/data/output/2026/1003/datasets/`, which keeps
  `code/` (git archives), `slurm_logs/` and `SimRack-1-smoke/`; Step 0 outputs `~/Desktop/data/output/2026/1003/sim_step0/`
- SimRack-1 slide GIFs (GT, FDK, MBIR, MACE4D no DCT / DCT; slices npz, make_panel_gif.py): /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT/Slides/2026/1007/Claude outputs/simrack1
- SimRack-2 (rack motion tilted 10 deg from the axis, 2026-10-08): scripts on Gautschi `~/PycharmProjects/scripts/2026/1008/simrack2/`, output `~/Desktop/data/output/2026/1008/simrack2/` (dataset `SimRack-2/`, recons, jitter_spectrum_simrack{1,2}.json); phantom figure /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT/Slides/2026/1008/Claude outputs/simrack2
- SVD of the per-frame MBIR of Phantom_30s_Run1 at 4, 6 and 8 frames per rotation (2026-10-19): code on Gautschi `~/PycharmProjects/scripts/2026/1019/mbir_svd_fpr/`, output `~/Desktop/data/output/2026/1019/mbir_svd_fpr/`; copies and plots /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT/Slides/2026/1019/Claude outputs/mbir_svd_fpr
- Slide with an animation of the turn-average operator R (2026-10-19; GIF, one-slide .pptx, scripts): /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT/Slides/2026/1019/Claude outputs/R_operator
- MBIR vs MBIR-DCT vs MBIR-SVD with cos(theta), sin(theta) as fixed temporal bases (2026-10-20; script, numbers, figures, GIF, README; run on the Mac from saved data): /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT/Slides/2026/1020/Claude outputs/svd_theta
- SimRack-1 at 4 and 8 frames per rotation (2026-10-08): scripts on Gautschi `~/PycharmProjects/scripts/2026/1008/simrack1_fpr/`, output `~/Desktop/data/output/2026/1008/simrack1_fpr/` (fpr4/, fpr8/, shift/); copies /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT/Slides/2026/1008/Claude outputs/simrack1_fpr
- Real scan Phantom_30s_Run1 with 90 deg frames, 45 deg step, nominal offset, full resolution (2026-10-08): scripts on Gautschi `~/PycharmProjects/scripts/2026/1008/real_span90_step45/`, output `~/Desktop/data/output/2026/1008/real_span90_step45_ds1/` (a cancelled binning-2 start is in `..._ds2_cancelled/`); 4 frames per rotation (180 deg frames): `~/Desktop/data/output/2026/1008/real_span180_step90_ds1/`; copies /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT/Slides/2026/1008/Claude outputs/real_span90_step45
- dl4dct checkout on Gautschi: `~/PycharmProjects/dl4dct` (main, remote git@github.com:SSRSSowmya/dl4dct.git; cloned 2026-10-05)
- SimRack-1 baselines (FDK, MBIR, MACE4D): script `dl4dct/experiments/simrack_baselines/`; Gautschi output
  `~/Desktop/data/output/2026/1005/simrack1_baselines/` (`<method>.npy`, `metrics_<method>.json`, `code/`, `slurm_logs/`)
- dl4dct experiment records (Mac, outside git): /Users/a124601/Desktop/Research_Purdue/DL4DCT/Experiment/<version>/<date>_<name>/ ;
  the same records in the repository: dl4dct/experiments/<version>/<date>_<name>/ ; version 0 outputs on Gautschi: ~/Desktop/data/output/2026/1006/version0/
- Gautschi GPU partitions: smallgpu (L40) needs 64 CPUs per GPU (-n64); `--mem` makes an ai request fail; standby QOS is not allowed on either
- Local copy of the Phantom_30s_Run1 config: /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT/Slides/2026/0820/3014053-D00087-009_Test1_30s_400delay.nsipro
  (a copy also sits in ~/Downloads; Claude can read ~/Downloads as of 2026-10-21)

## mbirtorch repos (MACE4D port)
- mbirtorch (Mac): /Users/a124601/Desktop/Research_Purdue/repository/mbirtorch — branch `mace_4d_dev`
- Ziyun's fork of mbirtorch (Mac, cloned 2026-10-19): /Users/a124601/Desktop/Research_Purdue/repository/mbirtorch_ziyun_fork —
  origin git@github.com:ZiyunLiiii/mbirtorch_ziyun_fork.git, upstream https://github.com/cabouman/mbirtorch.git
- mbirtorch_plans (Mac): /Users/a124601/Desktop/Research_Purdue/repository/mbirtorch_plans — plans in
  `plans/features/mace4d/` (initial_prompt.md, mace4d_migration_plan_v2.md is the plan of record),
  measurement scripts and records in `plans/experiments/features/mace4d/`, writing rules in `.claude/writing_style.md`
- mbirjax (Mac, read-only reference): /Users/a124601/Desktop/Research_Purdue/repository/mbirjax — branch `main` (v0.7.3)
- Torch env: `~/anaconda3/envs/mbirtorch/bin/python` (from mbirtorch/environment.yml; mbirtorch installed
  editable; Python 3.14, torch 2.14, cpu + mps). Run tests from the repo root with `python -m pytest tests`
  or `cd dev_scripts && bash run_tests.sh`.
- mbirjax check env: `~/anaconda3/envs/mbirjax_ref/bin/python` (`pip install mbirjax` 0.7.3, CPU only). Used
  only for the mace4d plan's Section 5 checks against mbirjax; nothing else.
- Workflow protocol for these repos: stage by explicit filename only, never `git add -A`, never commit
  (Greg commits from PyCharm). Each stage stops for Greg's review.

## Cluster (Gautschi)
- Login: `ssh li5273@gautschi.rcac.purdue.edu` (BoilerKey: `PIN,push`). Skill docs in `claude_scripts/gautschi/`:
  `connect.md` (logging in), `submit_jobs.md` (Slurm), `storage_layout.md` (where files go).
- Slurm: account `bouman`, partition `ai` (20 nodes, 8x H100 + 112 cores each -> 14 cores per GPU),
  QOS `normal`. A 4-GPU job asks for `-N1 -n56 --gpus-per-node=4`.
- Experiment code: /home/li5273/PycharmProjects/scripts/<year>/<MMDD>/ (home fs, 25 GB quota --
  code and small logs only). Own repo, remote git@github.com:ZiyunLiiii/scripts.git, branch `main`.
  Weekly dirs sit at the repo root; run from there so `import mar_utils` resolves. Run artifacts
  (`logs/`, `slurm_logs/`, `*.err`, `*.out`, `*.npy`, images) are gitignored -- on disk, never committed.
  Moved out of cabouman/lilly_exp on 2026-09-17, where it had been untracked, and the `nsi/` level
  was dropped in the move.
- Demo data: /home/li5273/PycharmProjects/lilly_exp/nsi/demo_data stayed behind in lilly_exp. It is a
  symlink to /scratch/gautschi/li5273/data, so no data moved, but ~400 scripts hardcode that absolute
  path. It is the only remaining coupling between the two repos -- do not delete lilly_exp.
- Outputs: /home/li5273/Desktop/data/output/<year>/<MMDD>/<run_name>/ -- `Desktop/data` is a symlink to
  /scratch/gautschi/li5273/data (200 TB, not backed up). All .npy/.h5 volumes go here.
- Shared reusable volumes (init images, FDK recons): /home/li5273/Desktop/data/output/2026/4D_shared/
- Source datasets: /depot/bouman/data/Lilly/ (e.g. 4DCT/Phantom_30s_Run1_Dec2024)
- Scratch copies of those datasets get partially purged (the purge goes by access time and eats
  the .tif radiographs, leaving the folder). Check with `claude_scripts/gautschi/check_datasets.sh`;
  repair per `gautschi/restore_datasets.md`. Rerunning `download_and_extract` does NOT repair it.
- 4D MACE outputs: /home/li5273/Desktop/data/output/2026/0903/mace4d/
- Static phantom, all 1800 views (no metal): extracted at ~/Desktop/data/demo_nsi_vert_no_metal_all_views/
  (from /depot/bouman/data/Lilly/demo_nsi_vert_no_metal_all_views.tgz); jitter test 2026-10-06: code
  ~/PycharmProjects/scripts/2026/1006/static_jitter/, output ~/Desktop/data/output/2026/1006/static_jitter/
- MACE4D with the theta-basis filter in place of the DCT filter (2026-10-20, real scan and SimRack-1): code
  ~/PycharmProjects/scripts/2026/1020/mace4d_theta/, output ~/Desktop/data/output/2026/1020/mace4d_theta/ (real_smoke/,
  real/, simrack1/, compare/ with the extracted Gram matrices and slices); local copies and write-up:
  /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT/Slides/2026/1020/Claude outputs/mace4d_theta/
  The same filters applied to the per-frame MBIR of SimRack-1 (no MACE4D): write-up
  /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT/Slides/2026/1020/Claude outputs/simrack1_mbir_filters/ (input
  compare/sim_mbir.npz from job 17148672)
- 4D beam hardening correction test (2026-10-17, mbirtorch branch 4dbhc): code ~/PycharmProjects/scripts/2026/1017/bhc4d/,
  output ~/Desktop/data/output/2026/1017/bhc4d/ (base/, <arm>/pass<k>/, compare_pass<k>/, mbirtorch_4dbhc/ code copy;
  variants pinned/, pinned_nodct/, pinned_metalonly/, still3d/); write-up, scripts, metrics, figures:
  /Users/a124601/Desktop/Research_Purdue/Lilly/4DCT/Slides/2026/1019/Claude outputs/bhc4d/README.md
- Tella_15cP four-recon comparison (2026-10-06): code ~/PycharmProjects/scripts/2026/1006/tella_15cP/, output
  ~/Desktop/data/output/2026/1006/tella_15cP/{dct,nofilter,mbir}/
- One-turn FDK init MACE4D run (2026-10-05): code ~/PycharmProjects/scripts/2026/1005/fdk360_init/, output
  ~/Desktop/data/output/2026/1005/mace4d_fdk360_init/; baseline (120 deg FDK init) is output/2026/1001
- Python environment (mbirtorch): `/home/li5273/.conda/envs/mbirtorch/bin/python` -- Python 3.11.16,
  torch 2.14.0+cu130, mbirtorch installed EDITABLE against `~/PycharmProjects/mbirtorch`.
  Created 2026-09-16 with `module load conda` (conda 26.1.0). Rebuild with
  `dev_scripts/clean_install_all.sh`, which removes and recreates the env of the same name.
- Repo checkout: `/home/li5273/PycharmProjects/mbirtorch`, branch `mace_4d_dev`, remote
  `https://github.com/cabouman/mbirtorch.git` (HTTPS). `~/PycharmProjects/mbirjax` is on `main` at v0.7.3.
- The `mbirjax` CONDA ENV no longer exists on Gautschi; `dev_scripts/deep_clean.sh` wipes `~/.conda`,
  and `~/.conda/envs` now holds only `mbirtorch`. jax and mbirjax are not installed anywhere there,
  so the opt-in `goldens` parity tests cannot run on the cluster.
- The `bouman` account has NO grant on the `cpu` partition: a job submitted there is refused with
  `AssocGrpGRES`, with or without `--gres=hp_cpu`. Even a CPU-only run goes on `ai` with a GPU.
- SSH key login works without a prompt: `ssh -o BatchMode=yes li5273@gautschi.rcac.purdue.edu`. A compute
  node that runs one of your jobs is reachable with `ssh -J li5273@gautschi.rcac.purdue.edu li5273@<node>`.
  The nodes' host key is the ed25519 key under `# Gautschi` in the login node's /etc/ssh/ssh_known_hosts
  (it covers h???, a???, and login??).
- GUI windows from a compute node: matplotlib's WebAgg backend and an SSH tunnel to the node, as in
  `claude_scripts/4Drecon/4d_viewer/serve_viewer4d.py`. tornado comes from
  /apps/external/anaconda/2025.12/lib/python3.13/site-packages/tornado, linked into a folder on PYTHONPATH,
  with TORNADO_EXTENSION=0 (its C extension fails under Python 3.11).
- 4D viewer trial (2026-09-29): job files `~/PycharmProjects/scripts/2026/1001/4d_viewer_trial/`
  (the viewer URL goes to its ignored `slurm_logs/viewer_url_<job>.txt`); run artifacts
  `~/Desktop/data/output/2026/1001/4d_viewer_trial/` (package copy `mbirtorch_4dviewer/`, `vendor/tornado`
  link, `smoke/` test volumes).

- Since at least 2026-11-05 the bouman account is capped at 3 H100 GPUs in total for the whole group (`sacctmgr show assoc account=bouman` shows GrpTRES gres/gpu=3); a 4-GPU sbatch is rejected with AssocGrpGRES. Login nodes reach PyPI and conda-forge only with the proxy variables unset (the squid proxy times out). Python environments: ~/.conda/envs/mbirtorch (torch 2.14+cu130) and the venv ~/venvs/mbirjax (mbirjax 0.7.3, jax[cuda12] 0.12.0.1, spekpy, PyYAML; made 2026-11-05 by scripts/2026/1105/ipmr_timing/make_env.sh after conda create failed on a corrupted readline package in ~/.conda/pkgs).

## Cluster (NCSA Delta)
- ACCESS project ELE260090 (Charlie's): about 3,000 GPU-hours on Delta, 2026-10-12 to 2027-10-11,
  shared by everyone on the project. NCSA login `zli98`. Host `login.delta.ncsa.illinois.edu`.
- Setup guide from Charlie (2026-10-14) and his login scripts (`scripts/delta.sh`, `scripts/nersc.sh`):
  /Users/a124601/Desktop/Research_Purdue/cluster_script/Delta_scripts (moved there from Research_Purdue/Delta_scripts)
- Login needs the NCSA password and an NCSA Duo push (Duo Mobile on a phone; a YubiKey fails for ssh).
  An SSH key cannot replace them. The server offers only `gssapi-with-mic,password` (checked 2026-10-28).
- One-command login (Charlie's setup, working since 2026-10-28): Ziyun runs `delta` (~/bin/delta, on the PATH
  through ~/.zshrc) and taps Approve on the phone. The script reads the password from the Keychain (item
  `delta-password`, account `zli98`), answers Duo with `1` (push), and opens a shared SSH connection.
  ~/.ssh/config has `Host delta login.delta.ncsa.illinois.edu` (User zli98, ControlMaster auto,
  ControlPath ~/.ssh/cm/%r@%n:%p, ControlPersist 4h, ServerAliveInterval 60). The config from before that
  entry is backed up at ~/.ssh/config.bak-20261028.
  Claude runs `ssh delta <cmd>`, `scp ... delta:...` and `rsync` with no prompts, and checks the
  connection with `ssh -O check delta`. The connection closes after 4 h with nothing using it, and
  then Ziyun runs `delta` again. The old `~/.ssh/cm-delta` path is no longer used.
  Delta drops a login prompt left unanswered for about 2 minutes. The host key is in known_hosts (2026-10-27).
  2026-10-29: login.delta round-robins over the login nodes dt-login01 to 04 (141.142.140.194, .195, .196, .205).
  dt-login04 hung after the password and timed out, with no Duo request sent, and dt-login01 did not answer on
  port 22 at 11:00.  Since 2026-10-29 11:00 the `delta` script tries the nodes in the order 02, 03, 04, 01 and
  moves to the next node when one does not ask for Duo within 30 s (`delta 03 04` picks the nodes).  It stops at
  once if the password is rejected, so that it does not lock the account.  Nodes 02 to 04 have the host key of
  login.delta, and the script checks each node's key against that known_hosts entry (HostKeyAlias).  The
  ControlPath uses the name typed (%n), so the shared connection is `~/.ssh/cm/zli98@delta:22` for every node,
  and plain `ssh delta` and `ssh -O check delta` find it.  Always pass `-o BatchMode=yes` in Claude's commands,
  so that ssh never tries a password when the connection is closed (failed tries count against the account).
  The versions from before this change are ~/bin/delta.bak-20261029 and ~/.ssh/config.bak-20261029.
- Public datasets on datadepot: the RP2040 board tarballs are at https://www.datadepot.rcac.purdue.edu/bouman/data/elec_board/data/<Horizontal|Vertical>_Elec_Board_<600|1200|1800>.tgz (the dataset page links /bouman/elec_board/..., which returns 404, checked 2026-11-05); the plastic phantom at https://www.datadepot.rcac.purdue.edu/bouman/data/demo_nsi_vert_{metal,no_metal}_all_views.tgz. The server omits its InCommon intermediate certificate, so wget/curl need it as an extra CA (IPMR_paper/timing/scripts/delta/datadepot_ca.pem). MD5 of the depot copies: demo_nsi_vert_metal_all_views.tgz 29ea84bce9377855abd7318380267852, Horizontal_Elec_Board_1800.tgz fc131f530192a355930892b874d4fbd4.
- 2026-11-05: the `Host delta` block got `ServerAliveCountMax 30` (backup ~/.ssh/config.bak-20261105), because the shared connection dropped three times that evening while the login node dt-login02 stalled on /work/nvme I/O (the default count of 3 ends the master after a 3 min stall).
- IPMR timing study on Delta (2026-11-05): scripts, simulation code, the conda env (mbirjax 0.7.3, jax[cuda12]), the extracted datasets and the Slurm logs in /u/zli98/ipmr_timing/ (scripts/, scripts/delta/, code/IPMR_simulation/, env/, data/, slurm_logs/, make_env.log); the tarballs and the outputs in /work/nvme/bjda/zli98/ipmr_timing/ (data/, out/<run>/, get_datasets.log). The full-size phantom and board runs use 4 H200 on partition gpuH200x8 (open to the project, billed 3x an A100); the smoke test (gpuA100x4-interactive, 1 h maximum, one job per user) and the simulation job (gpuA100x4) use one A100. `scripts/delta/bootstrap_from_mac.sh` on the Mac copies the code and starts the env build and downloads; `scripts/delta/submit.sh` on a login node submits the chain. When dt-login02 answers "Cannot send after transport endpoint shutdown" for a file on /work/nvme, `ssh dt-login01 cat <file>` from inside Delta reads it (host-based auth, no password).
- Web portal (Open OnDemand): https://openondemand.delta.ncsa.illinois.edu/ (CILogon with the NCSA login and
  NCSA Duo). Apps: Shell Access, JupyterLab, Code Server (VS Code), TensorBoard, Desktop.
- Slurm account `bjda-delta-gpu` (2,999 GPU-hours deposited, 2,973 left on 2026-10-27). `quota` lists storage,
  `accounts` the balance, `jobcharge -a bjda-delta-gpu -d <days> --detail` the charges per job.
- GPU partitions (2-day limit; `-interactive` versions 1 h, one job per user): gpuA100x4 (default; 4x A100 40 GB,
  64 cores, 256 GB), gpuA40x4 (4x A40 48 GB), gpuA100x8, gpuH200x8 (8x H200 141 GB, 96 cores, 2 TB, one node per job).
  Charge per GPU-hour: A40 0.5, A100x4 1, A100x8 1.5, H200 3; interactive 2x, `-preempt` 0.5x (for checkpointed jobs).
  Slurm bills the largest of the GPU, CPU and memory shares (PriorityFlags=MAX_TRES). The share of one A100x4 GPU is
  16 cores and 62.5 GB, so 1 GPU with --mem=200G is billed as 3.2 GPUs. Default memory is 1 GB per CPU, so set --mem.
- mbirtorch on Delta (2026-10-27): repo ~/PycharmProjects/mbirtorch (main, HTTPS clone); conda env `mbirtorch`
  at /u/zli98/.conda/envs/mbirtorch (Python 3.11.18, torch 2.14.0+cu130, mbirtorch editable). Activate with
  `module load miniforge3-python; source "$(conda info --base)/etc/profile.d/conda.sh"; conda activate mbirtorch`.
  The A100 nodes run driver 595.71.05. The 1-GPU test job and its script are in ~/delta_test/ (job 23256558 passed).
- Other software: modules pytorch-conda/2.8 and 2.12, cudatoolkit/26.5_13.2; apptainer is installed, and NGC
  containers are in /sw/external/NGC. RHEL 9.6.
- Storage (2026-10-27): home /u/zli98 (100 GB soft, 4 KB used); project allocation `bjda`, shared by the
  project: /projects/bjda (500 GB soft), /work/nvme/bjda (500 GB soft, fast), /work/hdd/bjda (1,000 GB soft,
  126.9 GB used by others on the project).
- SOR random-angle test on Delta (2026-10-28): /work/nvme/bjda/zli98/sor_random_angle/ with code/mbirtorch_fork,
  scripts/ (a copy of the Gautschi scripts plus filter12_p6_delta.sbatch), datasets/ (ground truth of the 12 fpr
  datasets), fpr12/<order>/ (mbir.npy and grams.npz copied from Gautschi), and slurm_logs/. Copying 29.5 GB from
  Gautschi through the Mac (3 zstd streams) ran at about 35 MB/s.

## MBIRTorch MCP server
- Code repository (private): git@github.com:ZiyunLiiii/mcp_sandbox.git, branch main; created 2026-11-03
  - Mac clone: /Users/a124601/Desktop/Research_Purdue/repository/mcp_sandbox
  - Gautschi clone (the copy Claude Code runs): /home/li5273/PycharmProjects/mcp_sandbox
- Project notes (goal, progress): /Users/a124601/Desktop/Claude_scripts/mbirtorch_mcp
- Server Python on Gautschi: /home/li5273/venvs/mbirtorch_mcp/bin/python
  (anaconda 2025.12 Python 3.13.9 plus mcp 2.3.0; no torch, does not need scratch)
- Test volumes on Gautschi: ~/mbirtorch_mcp_test/rack4d.{h5,npy} (4D, from tests/make_rack4d.py); 3D test file
  /depot/bouman/data/Translation/TCT_BGA_recon/MBIR_recon.h5
- Claude Code registration: `mbirtorch-gautschi`, local scope, for the mbirtorch repo folder (in ~/.claude.json)

## Claude Scripts
- Local (Mac): /Users/a124601/Desktop/Claude_scripts
- Remote (Gautschi): /home/li5273/Desktop/claude_scripts
- GitHub: git@github.com:ZiyunLiiii/claude_scripts.git
- Sync: git pull / git add -A && git commit -m "update" && git push

## Undergrad (XJTLU) archive
- /Users/a124601/Desktop/XJTLU — layout Y1..Y4/Y<n>S<m>/<MODULE> (e.g. Y3/Y3S1/CAN207, Y4/Y4S2/MEC304), Y4/FYP, plus GRE, 雅思, 实习, 科研, Graduation.
  XJTLU/XJTLU holds non-course material in four subfolders (2026-10-21): Programme_specs, Registry_admin,
  Transcripts_and_GPA, Grad_applications (the C2214049 application bundle, CV, PS, visa appointments); _junk_to_review holds an apk. 266 course files were
  moved there from ~/Downloads on 2026-10-21 (script: sort_xjtlu.py in that day's Claude scratchpad; collisions got a
  " (from Downloads)" suffix). Known module names: EEE103/109/104/108/116/118, EAP028/111, MTH101/102/201, CAN207/202/310,
  EEE201/211/205/339/340, MEC201/202/208/301/304, CPT210.
