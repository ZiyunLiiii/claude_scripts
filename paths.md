# Paths & Locations

## Dropbox
- Root: /Users/a124601/Library/CloudStorage/Dropbox
- Overleaf projects: /Users/a124601/Library/CloudStorage/Dropbox/Apps/Overleaf

## Notable Projects
- Lilly Proposal (LaTeX): /Users/a124601/Library/CloudStorage/Dropbox/Apps/Overleaf/Proposal_4D_Lilly/main.tex
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

## Cluster (NCSA Delta)
- ACCESS project ELE260090 (Charlie's): about 3,000 GPU-hours on Delta, 2026-10-12 to 2027-10-11,
  shared by everyone on the project. NCSA login `zli98`. Host `login.delta.ncsa.illinois.edu`.
- Setup guide from Charlie (2026-10-14) and his login scripts (`scripts/delta.sh`, `scripts/nersc.sh`):
  /Users/a124601/Desktop/Research_Purdue/Delta_scripts
- Login needs the NCSA password and an NCSA Duo push (Duo Mobile on a phone; a YubiKey fails for ssh).
  Claude works through a shared SSH connection (`ControlMaster`, 4 h) that Ziyun opens.

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
