# Paths & Locations

## Dropbox
- Root: /Users/a124601/Library/CloudStorage/Dropbox
- Overleaf projects: /Users/a124601/Library/CloudStorage/Dropbox/Apps/Overleaf

## Notable Projects
- Lilly Proposal (LaTeX): /Users/a124601/Library/CloudStorage/Dropbox/Apps/Overleaf/Proposal_4D_Lilly/main.tex
- Code Review Schedule (website): /Users/a124601/Desktop/code-review-schedule — React+Vite+TS, remote git@github.com:ZiyunLiiii/code-review-schedule.git, live at https://ziyunliiii.github.io/code-review-schedule/ (GitHub Pages via Actions). Manages weekly Fri 3:30 PM Code Review meetings; semester config in src/utils/persistence.ts (DEFAULT_SEMESTER_CONFIG).

## 4DCT / mbirjax repos
- 4DCT (Mac): /Users/a124601/Desktop/Research_Purdue/repository/4DCT — branch `refactor_for_mbirjax`, remote git@github.com:cabouman/4DCT.git
- mbirjax (Mac): /Users/a124601/Desktop/Research_Purdue/repository/mbirjax — branch `4DCT_for_merging`, remote git@github.com:cabouman/mbirjax.git
- Local test env: `~/anaconda3/envs/mbirjax_test/bin/python`. mbirjax is installed there
  NON-editable, so run pytest from the mbirjax repo root, and set
  `PYTHONPATH=/Users/a124601/Desktop/Research_Purdue/repository/mbirjax` for scripts run from
  anywhere else — otherwise the stale site-packages copy is imported silently.

## mbirtorch repos (MACE4D port)
- mbirtorch (Mac): /Users/a124601/Desktop/Research_Purdue/repository/mbirtorch — branch `mace_4d_dev`
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
- Experiment code: /home/li5273/PycharmProjects/lilly_exp/nsi/<year>/<MMDD>/ (home fs, 25 GB quota --
  code and small logs only)
- Outputs: /home/li5273/Desktop/data/output/<year>/<MMDD>/<run_name>/ -- `Desktop/data` is a symlink to
  /scratch/gautschi/li5273/data (200 TB, not backed up). All .npy/.h5 volumes go here.
- Shared reusable volumes (init images, FDK recons): /home/li5273/Desktop/data/output/2026/4D_shared/
- Source datasets: /depot/bouman/data/Lilly/ (e.g. 4DCT/Phantom_30s_Run1_Dec2024)
- Scratch copies of those datasets get partially purged (the purge goes by access time and eats
  the .tif radiographs, leaving the folder). Check with `claude_scripts/gautschi/check_datasets.sh`;
  repair per `gautschi/restore_datasets.md`. Rerunning `download_and_extract` does NOT repair it.
- 4D MACE outputs: /home/li5273/Desktop/data/output/2026/0903/mace4d/
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

## Claude Scripts
- Local (Mac): /Users/a124601/Desktop/Claude_scripts
- Remote (Gautschi): /home/li5273/Desktop/claude_scripts
- GitHub: git@github.com:ZiyunLiiii/claude_scripts.git
- Sync: git pull / git add -A && git commit -m "update" && git push
