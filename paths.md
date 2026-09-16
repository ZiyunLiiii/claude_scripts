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
- Login: `ssh li5273@gautschi.rcac.purdue.edu` (BoilerKey: `PIN,push`). Connect how-to: ~/Desktop/Claude_scripts/gautschi/connect.md
- 4DCT dataset: /home/li5273/Desktop/data/Phantom_30s_Run1_Dec2024
- 4D MACE outputs: /home/li5273/Desktop/data/output/2026/0903/mace4d/
- Python environment: the `mbirjax` virtual environment (updated mbirjax installed manually)
- GPUs: request with e.g. `--gres=gpu:h100:4`; reference timings are on 4x H100

## Claude Scripts
- Local (Mac): /Users/a124601/Desktop/Claude_scripts
- Remote (Gautschi): ~/Claude_scripts
- GitHub: https://github.com/ZiyunLiiii/Claude_scripts
- Sync: git pull / git add -A && git commit -m "update" && git push
