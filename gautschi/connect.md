# Connecting to Gautschi from a Local Terminal

Skill doc for logging in to Purdue RCAC's **Gautschi** community cluster from a Mac terminal.

- **User:** `li5273`
- **Login host:** `gautschi.rcac.purdue.edu`
  (This name load-balances across 8 front-ends, `login00.gautschi`–`login07.gautschi`; each login lands on a random one. Files/home are shared across all of them, so it doesn't matter which one you get.)
- **Scheduler:** Slurm. Login nodes are for editing/compiling/light work only — run real work through `sbatch`/`salloc` (see the job-submission doc).

---

## 1. Quick start (BoilerKey / Duo)

```bash
ssh li5273@gautschi.rcac.purdue.edu
```

When prompted for a password, type your **BoilerKey PIN followed by `,push`**:

```
Password: <your-PIN>,push
```

Your Duo/Purdue Login app then gets a push notification — approve it and you're in.

- Format is `PIN,push` (PIN, a comma, then the literal word `push`). No space.
- Password-only login is **not** supported on RCAC community clusters — it's BoilerKey/Duo or an SSH key, nothing else.
- Other second factors work too: `,sms` or `,phone`, but `,push` is easiest.

---

## 2. Recommended: SSH key (skip the 2FA prompt each time)

Set this up once and logins become passwordless. Rsync in particular **requires** an SSH key.

**a. Generate a key on the Mac** (if you don't already have one):
```bash
ls ~/.ssh/id_ed25519.pub    # check if a key already exists
ssh-keygen -t ed25519 -C "li5273@purdue.edu"   # if not, make one; accept defaults
```

**b. Install the public key on Gautschi.** The clean way is to append your `~/.ssh/id_ed25519.pub` to `~/.ssh/authorized_keys` on Gautschi. Because password auth is off, do it during a BoilerKey session:
```bash
ssh li5273@gautschi.rcac.purdue.edu   # log in with PIN,push
mkdir -p ~/.ssh && chmod 700 ~/.ssh
# paste your local id_ed25519.pub contents into ~/.ssh/authorized_keys, then:
chmod 600 ~/.ssh/authorized_keys
exit
```
To grab the local key text quickly: `pbcopy < ~/.ssh/id_ed25519.pub` (copies it to the clipboard).

> **Off-campus note:** SSH key login to RCAC clusters generally works from anywhere, but if a key is ever refused from off-campus, connect to Purdue's **WebVPN/GlobalProtect VPN** first, then retry. SMB (drive-mount) access always needs the VPN.

---

## 3. Make it one word: `~/.ssh/config`

Add this block to `~/.ssh/config` on the Mac so you can just type `ssh gautschi`:

```
Host gautschi
    HostName gautschi.rcac.purdue.edu
    User li5273
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
    ServerAliveCountMax 30
```

Then:
```bash
ssh gautschi
```
`ServerAliveInterval`/`ServerAliveCountMax` keep long idle SSH sessions from dropping.

---

## 4. Graphical apps (X11 forwarding)

To run GUI tools (e.g. a plot window, `slice_viewer`) over SSH:
```bash
ssh -Y gautschi        # or -X for stricter/safer forwarding
```
Requires **XQuartz** installed on the Mac (`brew install --cask xquartz`, then log out/in once). For heavy interactive graphics, prefer OnDemand desktop (below) over X11.

---

## 5. Transferring files

**scp** (single files / small trees):
```bash
# local -> Gautschi
scp ./run.py gautschi:~/Claude_scripts/
# Gautschi -> local
scp gautschi:/home/li5273/Desktop/data/output/2026/0903/mace4d/recon.npy ./
```

**rsync** (large trees, resumable, only copies diffs — needs SSH key):
```bash
# push a folder up, mirroring
rsync -avz --progress ./localdir/ gautschi:~/remotedir/
# pull results down
rsync -avz --progress gautschi:/home/li5273/Desktop/data/output/ ./output/
```

With the `~/.ssh/config` alias above, `scp`/`rsync` reuse the `gautschi` host automatically.

For very large or long-running transfers, RCAC also supports **Globus** (`data.rcac.purdue.edu` / Gautschi Globus endpoint) — best for multi-GB datasets.

---

## 6. Browser fallback: OnDemand / gateway

No terminal needed — log in with BoilerKey at:

**https://gateway.gautschi.rcac.purdue.edu**

From there: **Clusters → Gautschi Shell Access** gives an in-browser terminal, and the menus also offer file management, job submission, and interactive desktop/Jupyter sessions. Handy from a machine where you can't set up SSH.

---

## 7. My environment on Gautschi (quick reference)

- **Python env:** the `mbirjax` virtual environment (updated mbirjax installed manually).
- **Data:** `/home/li5273/Desktop/data/Phantom_30s_Run1_Dec2024`
- **4D MACE outputs:** `/home/li5273/Desktop/data/output/2026/0903/mace4d/`
- **Claude scripts (remote):** `~/Claude_scripts` — sync with `git pull` / `git add -A && git commit -m "update" && git push` (repo: https://github.com/ZiyunLiiii/Claude_scripts).
- **GPUs:** request e.g. `--gres=gpu:h100:4`; reference timings are on 4× H100.

---

## 8. Troubleshooting

| Symptom | Fix |
|---|---|
| `Permission denied (publickey,password)` | You typed the PIN wrong, or key not installed. Retry with `PIN,push`, or re-check `~/.ssh/authorized_keys` on Gautschi. |
| Duo push never arrives | Use `,sms` or `,phone` instead of `,push`, or open the Duo app and generate a passcode: `PIN,<6-digit-code>`. |
| Key refused from home | Connect Purdue GlobalProtect/WebVPN first, then `ssh gautschi`. |
| Session freezes/drops when idle | Add the `ServerAlive*` lines in §3. |
| `ssh gautschi` unknown host | The `~/.ssh/config` block isn't saved, or has a typo in `Host gautschi`. |

---

### Sources
- [Gautschi User Guide — Logging In](https://www.rcac.purdue.edu/knowledge/gautschi/accounts/login?all=true)
- [Gautschi User Guide — Purdue Login (BoilerKey)](https://www.rcac.purdue.edu/knowledge/gautschi/accounts/login/purdue_login)
- [Gautschi User Guide — SSH Keys](https://www.rcac.purdue.edu/knowledge/gautschi/accounts/login/sshkeys)
- [Gautschi User Guide — SSH Client Software](https://www.rcac.purdue.edu/knowledge/gautschi/accounts/login/sshclient)
- [Gautschi User Guide — File Transfer (SCP / Rsync)](https://www.rcac.purdue.edu/index.php/knowledge/gautschi/storage/transfer?all=true)
