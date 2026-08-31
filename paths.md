# Paths & Locations

## Dropbox
- Root: /Users/a124601/Library/CloudStorage/Dropbox
- Overleaf projects: /Users/a124601/Library/CloudStorage/Dropbox/Apps/Overleaf

## Notable Projects
- Lilly Proposal (LaTeX): /Users/a124601/Library/CloudStorage/Dropbox/Apps/Overleaf/Proposal_4D_Lilly/main.tex

## 4DCT / mbirjax repos
- 4DCT (Mac): /Users/a124601/Desktop/Research_Purdue/repository/4DCT — branch `refactor_for_mbirjax`, remote git@github.com:cabouman/4DCT.git
- mbirjax (Mac): /Users/a124601/Desktop/Research_Purdue/repository/mbirjax — branch `4DCT_for_merging`, remote git@github.com:cabouman/mbirjax.git
- Local test env: `~/anaconda3/envs/mbirjax_test/bin/python`. mbirjax is installed there
  NON-editable, so run pytest from the mbirjax repo root, and set
  `PYTHONPATH=/Users/a124601/Desktop/Research_Purdue/repository/mbirjax` for scripts run from
  anywhere else — otherwise the stale site-packages copy is imported silently.

## Cluster (Gautschi)
- 4DCT dataset: /home/li5273/Desktop/data/Phantom_30s_Run1_Dec2024
- 4D MACE outputs: /home/li5273/Desktop/data/output/2026/0903/mace4d/
- Python environment: the `mbirjax` virtual environment (updated mbirjax installed manually)
- GPUs: request with e.g. `--gres=gpu:h100:4`; reference timings are on 4x H100

## Claude Scripts
- Local (Mac): /Users/a124601/Desktop/Claude_scripts
- Remote (Gautschi): ~/Claude_scripts
- GitHub: https://github.com/ZiyunLiiii/Claude_scripts
- Sync: git pull / git add -A && git commit -m "update" && git push
