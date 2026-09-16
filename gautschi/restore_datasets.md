# Restoring Purged Datasets from Depot with `download_and_extract`

Scratch is not backed up and **is purged by access time**. The purge does not delete a
dataset — it eats it from the inside, removing the radiograph `.tif` files that no recent
job touched while leaving the folder skeleton and the `.nsipro` metadata in place. A run
started against a half-eaten dataset does not crash; it reconstructs from whatever views
survived.

`mbirtorch.download_and_extract` is the utility that repopulates scratch from
`/depot/bouman/data/Lilly`. **It will not do that on its own**, for the reason in §2.
Read that section before anything else.

- Authoritative copies: `/depot/bouman/data/Lilly/` (10 TB, backed up, read-mostly)
- Working copies: `/scratch/gautschi/li5273/data/` = `~/Desktop/data` = `…/lilly_exp/nsi/demo_data`
- Env: `module load conda && conda activate mbirtorch` (editable install of
  `~/PycharmProjects/mbirtorch`)

See [storage_layout.md](storage_layout.md) for why the tree is arranged this way.

---

## 1. Check before you submit

```bash
~/Desktop/claude_scripts/gautschi/check_datasets.sh          # all datasets
~/Desktop/claude_scripts/gautschi/check_datasets.sh /home/li5273/Desktop/data
```

It applies three tests per dataset and costs seconds — it stats metadata, it never reads
a 16 GB tarball:

| Test | Signal | Status |
|---|---|---|
| scratch tarball size vs. the depot original | differs | `TRUNCATED_TARBALL` |
| extracted tree present | absent | `NOT_EXTRACTED` |
| extracted bytes vs. compressed tarball bytes | **ratio < 1.0** | `PARTIAL_EXTRACT` |
| `.tif` count vs. `<Number of projections>` in the `.nsipro` | fewer | `MISSING_VIEWS` |

The ratio test is exact, not a heuristic: gzip never expands, so a complete extraction is
always **at least** as large as its tarball. Anything under 1.0 is missing files.

Run on 2026-09-16, **9 of 15 datasets were incomplete**:

```
DATASET                                     TGZ  EXTRACTED  RATIO    TIFS  EXPECT  STATUS
Autoinjector_HighRes_Horizontal          15.62G     10.19G   0.65     926    1800  PARTIAL_EXTRACT,MISSING_VIEWS
Connected_Autoinjector_Horizontal        15.76G      9.92G   0.63     902    1800  PARTIAL_EXTRACT,MISSING_VIEWS
Connected_Autoinjector_Vertical          14.85G     18.71G   1.26    1761    1600  OK
D01788                                   15.75G      0.00G   0.00       0    1800  PARTIAL_EXTRACT,MISSING_VIEWS
demo_nsi_vert_metal_all_views            15.75G      9.92G   0.63     902    1800  PARTIAL_EXTRACT,MISSING_VIEWS
Dry_Powder_Inhaler_Feb                    9.14G      4.70G   0.51     853    1700  PARTIAL_EXTRACT,MISSING_VIEWS
Hearing_Aid                              13.46G     17.23G   1.28    1567    1500  OK
Horizontal_Elec_Board_1800                9.55G      4.97G   0.52     902    1800  PARTIAL_EXTRACT,MISSING_VIEWS
Kwikpen_4D_2mms                           1.60G      1.72G   1.08    4002    4000  OK
Kwikpen_Savvio                            9.49G      4.96G   0.52     901    1800  PARTIAL_EXTRACT,MISSING_VIEWS
NSI_sample_1                              2.93G      0.00G   0.00      NA      NA  TRUNCATED_TARBALL,NOT_EXTRACTED
Phantom_30s_Run1_Dec2024                  0.99G      1.07G   1.08    2468    2400  OK
Tella_15cP_Run3_April2024                 0.68G      0.69G   1.02    1602    1600  OK
Tella_30cP_Run3_April2024                 0.66G      0.00G   0.00       0    1600  PARTIAL_EXTRACT,MISSING_VIEWS
Vertical_Elec_Board_1800                  9.47G      5.06G   0.53     918    1800  PARTIAL_EXTRACT,MISSING_VIEWS
```

Both tests were checked against ground truth: reading the real manifest of
`Kwikpen_Savvio.tgz` off depot (`tar -tzvf`) lists **1868 `.tif` totalling 10.64 GB
uncompressed**, against **901 tifs / 4.96 GB** on scratch. The `TIFS` and `RATIO` columns
agreed with the manifest, and on every row of the table the two tests agree with each
other.

`Connected_Autoinjector_Vertical` and `Hearing_Aid` show more tifs than `EXPECT` because
those trees hold a second radiograph set (gain/offset frames); ratio > 1.0 is the
governing signal there.

---

## 2. The reason a rerun does not fix anything

`download_and_extract(download_url, save_dir)` decides everything from **one test** —
does the tarball exist in `save_dir`:

```python
file_path = os.path.join(save_dir, filename)
if os.path.exists(file_path):
    is_download = False        # <- and extraction lives INSIDE `if is_download:`
```

So when the purge takes the extracted tree but leaves `Dataset.tgz` behind — the common
case — the function copies nothing, extracts nothing, and **returns a path that does not
exist**, with no error and no warning:

```python
d = mbirtorch.download_and_extract('/depot/.../MyData.tgz', save)   # fresh
#   -> save/MyData        exists: True
shutil.rmtree(d)                                                    # purge
d = mbirtorch.download_and_extract('/depot/.../MyData.tgz', save)   # rerun
#   -> save/MyData        exists: False        <- silent
```

Three consequences worth holding onto:

- There is no `force=` or `overwrite=` argument. The signature is exactly
  `(download_url, save_dir)`.
- The existence test is on the **tarball**, never on the extracted tree, so a dataset
  eaten hollow by the purge always looks done.
- The tarball is never validated. `NSI_sample_1.tgz` on scratch is a truncated 2.93 GB of
  a 5.63 GB depot file — `tarfile` raises `EOFError: Compressed file ended before the
  end-of-stream marker was reached` — yet `get_top_level_tar_dir` still returns
  `'NSI_sample_1'`, because it reads only the first member (`max_entries=1`). The bad
  tarball produces a confident, wrong path.

**To make the utility redo the work you must delete the tarball, not the folder.**

---

## 3. Repair

### Preferred: extract straight from depot, symlink the tarball (zero copy)

```bash
cd /home/li5273/Desktop/data                         # -> scratch
DS=Kwikpen_Savvio
SRC=/depot/bouman/data/Lilly/$DS.tgz                 # 4DCT sets: .../Lilly/4DCT/$DS.tgz

rm -rf  "$DS" "$DS.tgz"
tar -xzf "$SRC" -C .
ln -s "$SRC" "$DS.tgz"                               # 122 bytes, not 9.5 GB

~/Desktop/claude_scripts/gautschi/check_datasets.sh | grep "$DS"
```

The symlink is what makes this compose with existing scripts: `os.path.exists` follows
it, so the next `download_and_extract` short-circuits on the **first** test and returns
the correct extracted path immediately, having copied nothing. `check_datasets.sh` uses
`stat -L`, so the size test still compares against depot and still passes.

Verified end to end: after this sequence `download_and_extract` returned the real
directory with the full file list, and the tarball entry on scratch cost 122 bytes.

### Plain Python, when you would rather not touch the shell

```python
import os, shutil, mbirtorch

src      = '/depot/bouman/data/Lilly/4DCT/Tella_30cP_Run3_April2024.tgz'
save_dir = '/home/li5273/Desktop/data'
name     = os.path.basename(src)[:-4]

shutil.rmtree(os.path.join(save_dir, name), ignore_errors=True)
if os.path.exists(os.path.join(save_dir, name + '.tgz')):
    os.remove(os.path.join(save_dir, name + '.tgz'))   # the line that matters

dataset_dir = mbirtorch.download_and_extract(src, save_dir)
assert os.path.isdir(dataset_dir)
```

Correct, but it `shutil.copy2`s the tarball to scratch **before** extracting — 15.75 GB
copied and 15.75 GB of scratch held for `D01788`, against 0 for the symlink route. Use it
for the small 4DCT sets; prefer §3.1 for the 10–16 GB ones.

### Guard at the top of a job script

Cheap, and it converts a silently-degraded reconstruction into a job that refuses to
start:

```python
import os, glob, mbirtorch

def dataset_or_die(depot_tgz, save_dir):
    d = mbirtorch.download_and_extract(depot_tgz, save_dir)
    if not os.path.isdir(d):
        raise FileNotFoundError(f'{d} missing -- purged tree, stale tarball. See restore_datasets.md')
    n = len(glob.glob(os.path.join(d, '**', '*.tif'), recursive=True))
    pro = glob.glob(os.path.join(d, '*.nsipro'))
    if pro:
        want = int(open(pro[0], errors='ignore').read().split('<Number of projections>')[1].split()[0])
        if n < want:
            raise RuntimeError(f'{d}: {n} of {want} views on disk -- partially purged.')
    return d
```

---

## 4. Keeping it from happening again

- **Touch what you intend to keep.** The purge goes by access time, which is why these
  trees lose exactly the views no recent job read. `find $DS -name '*.tif' -exec touch -a {} +`
  before a long campaign, or run `check_datasets.sh` as the first line of the sbatch.
- **Never put the only copy on scratch.** Everything in the table above was recoverable
  because depot holds it. A dataset you generate yourself and care about goes to depot too.
- **Symlink rather than copy.** Nine of these datasets are byte-identical duplicates of
  depot files sitting on scratch — ~100 GB of scratch spent on the privilege of having
  `download_and_extract` skip a check.
- **Check `.tgz` size against depot after any transfer.** `NSI_sample_1.tgz` is what an
  interrupted copy leaves behind, and nothing downstream notices.

---

Facts here were read off Gautschi on 2026-09-16: the `download_and_extract` source in
`~/PycharmProjects/mbirtorch/mbirtorch/utilities.py` (editable install, the code that
actually runs), the real state of `/scratch/gautschi/li5273/data`, and the manifest of
`Kwikpen_Savvio.tgz` on depot. The silent-wrong-path behaviour and both repair recipes
were reproduced against the installed package.
