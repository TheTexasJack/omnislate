# unstableNHP Server Setup (Nathan)

How to turn the Cheese Block (unstableNHP, Linux Mint 22.3) into the shared OMNISLATE workshop.  Follow it top to bottom.  Phase 1 (updates, SSH, firewall, Tailscale) is already done.

**What you end up with**

- One workshop in `/srv/omnislate` that every GM shares, so copies never drift apart.
- A build web page at `http://unstablenhp/` with a login per GM.  Each GM sees only their own campaigns.  You (admin) see everything.
- One shared drive per campaign for editing files from any computer, Windows included.
- Auto-build: a saved change rebuilds that campaign about five seconds later.
- Nothing reachable from the internet.  The firewall only accepts traffic from your Tailscale network.

---

## 1. Get the files onto unstableNHP

From Beast, copy the release zip and the Halas videos over SSH:

```bash
scp omnislate_3.3.zip lancer@unstablenhp:~
ssh lancer@unstablenhp 'unzip -q omnislate_3.3.zip -d ~'
scp /path/to/gravis-display/images/*.mp4 lancer@unstablenhp:~/omnislate/campaigns/errans-inter-astra/halas/media/
```

Replace `/path/to/...` with wherever the three Halas videos live on Beast.

## 2. Install

On unstableNHP (over SSH from Beast is fine):

```bash
cd ~/omnislate
sudo python3 server/omnictl.py install
```

It installs Samba, ACL tools, Pillow, and ffmpeg, creates the `omnibuild` service user and the `omnigm` group, copies the workshop to `/srv/omnislate`, sets permissions, writes the shared drives, and starts the build service.  It asks you for a password.  That password is for the build page and your shared drives.

Check it from Beast: open `http://unstablenhp/` and log in as `lancer`.  You should see `errans-inter-astra` with a Build button.  Press it.

## 3. Your own shared drive (Beast)

In the Files app on Beast, press Ctrl+L and type:

```text
smb://unstablenhp/omnislate-admin
```

Log in as `lancer` with the same password and bookmark it.  That is the whole workshop, writable by you.  Your campaign alone is `smb://unstablenhp/errans-inter-astra`.

## 4. Add Jarrett

1. **Invite him to your Tailscale network.**  Open the Tailscale admin console in a browser, go to **Users**, and use **Invite users** to send him a link.  He uses one of your 6 free user slots.
2. **Check MagicDNS is on** (the **DNS** page of the admin console).  It is what makes the name `unstablenhp` work on his PC.
3. **Pick his campaign folder name** with him: lowercase letters, numbers, and dashes, such as `iron-tide`.
4. **Create his account and campaign:**

   ```bash
   cd /srv/omnislate
   sudo python3 server/omnictl.py add-gm jarrett iron-tide
   ```

   It asks for his password.  His account can only use the shared drive and the build page.  It cannot log in to the desktop or use SSH.
5. **Send him `docs/GM_SERVER_GUIDE.md`** and give him his password in person or over Signal, never in the same message as the guide.

## 5. The tablet

1. Install the **Tailscale** app on the tablet and sign in with your account.
2. In Firefox open `http://unstablenhp/`, log in, and bookmark it.
3. Session links on the build page open straight on the tablet, videos included.
4. For game night, long-press a session link and download it (plus the campaign's videos) so it runs with no network at all.  Local files stay the safest choice at the table.

## 6. Day-to-day commands

Run these from `/srv/omnislate`:

| Task | Command |
|---|---|
| Health check: GMs, campaigns, sizes, services | `sudo python3 server/omnictl.py status` |
| Change a password (build page and drives) | `sudo python3 server/omnictl.py passwd jarrett` |
| Another campaign for an existing GM | `sudo python3 server/omnictl.py add-gm jarrett second-campaign` |
| Turn auto-build off or on | `sudo python3 server/omnictl.py autobuild off` |
| Space limit per campaign (shown on the build page) | `sudo python3 server/omnictl.py limit 20` |
| Reapply permissions after moving files around | `sudo python3 server/omnictl.py fix-perms` |

## 7. Installing a new OMNISLATE release

```bash
unzip -q omnislate_3.3.zip -d ~/omnislate-new
sudo python3 ~/omnislate-new/omnislate/server/omnictl.py update
```

Adjust the path to wherever the unzipped `omnislate` folder lands.  Update backs up the current engine to `/srv/omnislate-backups/<date>/`, installs the new `app/`, `build.py`, `server/`, docs, and starter, and leaves every campaign and `dist/` alone.  The shared world pool (`library/`) stays untouched unless you add `--library`.  Auto-build refreshes session files a few seconds later.

## 8. Moving to 3.3 chapters (one time)

The server's `errans-inter-astra` folder is still the flat 3.2 layout.  3.3 turns it into the umbrella with `halas`, `remnant`, and `regulators` inside.  The zip carries the new layout, so this swaps it in and keeps your videos.  From Beast:

```bash
scp omnislate_3.3.zip lancer@unstablenhp:~
ssh lancer@unstablenhp
```

Then on unstableNHP:

```bash
unzip -q omnislate_3.3.zip -d ~/omnislate-3.3
sudo python3 ~/omnislate-3.3/omnislate/server/omnictl.py update

sudo systemctl stop omnislate-web          # pause auto-build during the swap
C=/srv/omnislate/campaigns
sudo mv $C/errans-inter-astra ~/errans-3.2-backup
sudo cp -r ~/omnislate-3.3/omnislate/campaigns/errans-inter-astra $C/
sudo cp ~/errans-3.2-backup/media/*.mp4 $C/errans-inter-astra/halas/media/
sudo python3 /srv/omnislate/server/omnictl.py fix-perms
sudo systemctl start omnislate-web

sudo diff -r ~/errans-3.2-backup/sessions $C/errans-inter-astra/halas/sessions
```

The last line shows anything you changed in the Halas session files on the server since 3.2 (an `Atlas:` line, say).  No output means nothing was lost.  Copy any change across through `smb://unstablenhp/errans-inter-astra`, where Halas now lives in the `halas` folder.  Do the same check for `notes` if you wrote any there.

The build page lists Halas, Remnant, and The Regulators under Errans Inter Astra a few seconds later.  The first build also clears the old flat files out of `dist/errans-inter-astra/`.  Delete `~/errans-3.2-backup` once you are happy.

Jarrett's campaign is unaffected.  Anyone added with `add-gm` from now on starts with `chapter-1` and `_template`.

## 9. Moving to 3.4 (the ANDIS terminal)

1. Install the engine the usual way (section 7).  That also brings the new starter, with its BEACON sample, for future GMs.
2. Campaigns are never touched by `update`, so bring the Proxima Prime signal over by hand.  On Beast, open `smb://unstablenhp/errans-inter-astra/remnant/`, make a `signals` folder, and drag in `remnant-buoy.md` from the unzipped `campaigns/errans-inter-astra/remnant/signals/`.
3. Open `remnant/sessions/remnant-session-1.md` on the drive and add one line: `Signals: remnant-buoy`
4. Save.  Auto-build picks it up, and Remnant session 1 gets the ANDIS button.

## 10. Moving to 3.5 (ANDIS attachments)

1. Install the engine the usual way (section 7).
2. **First, the session line.**  Open `regulators/sessions/` on the drive and add `Signals: northwatch-records` to the session that has the jailbreak.  Without this line the hack never appears, even with the file in place.
3. On Beast, make a `signals` folder inside `regulators` on the drive and drag in `northwatch.md` from the unzipped `campaigns/errans-inter-astra/regulators/signals/`.
4. Save.  The build report shows a `Signal  northwatch-records` line and an `Attach` line.  If they are missing, step 2 is the one to check.

## 11. Moving to 3.6 (ANDIS audio and video)

Engine only.  Install it the usual way (section 7).  Nothing to copy by hand.  To add a voice log or a clip to a signal later: audio files and their `.txt` transcripts go in the chapter's `signals/` folder, videos go in its `media/` folder, and each gets a line under `### Attachments`.

## 12. Troubleshooting

| Symptom | Check |
|---|---|
| Build page does not load | `systemctl status omnislate-web` and `journalctl -u omnislate-web -n 50` |
| Shared drive refuses to connect | `systemctl status smbd`, then `testparm -s` |
| Name `unstablenhp` does not resolve | Use the address from `tailscale ip -4` instead, and check MagicDNS |
| Login page keeps coming back | Five wrong passwords lock that device out for one minute |
| GM cannot see a campaign | `sudo python3 server/omnictl.py status` shows who has what |
| New chapter missing from the build page | Its folder name has spaces or capitals, or starts with `_`.  The build report names it |
| Anything else | `sudo ufw status` should show only `tailscale0` rules |

## How it is locked down

- **Firewall:** ufw denies all incoming traffic except on `tailscale0`.  The build page also refuses any address outside the Tailscale range.
- **Accounts:** GMs get no-login accounts.  The build service runs as `omnibuild`, which has no shell, can only write `dist/` and its own state folder, and starts nothing except `build.py`.
- **Folders:** each campaign belongs to its GM.  You (admin) and `omnibuild` get access through ACLs.  Other GMs cannot open it, over the drive or the web.  The engine, library, and starter are read-only for GMs.
- **Overrides:** anything locked can be changed with `sudo` on the box.  Run `omnictl.py fix-perms` afterward, because root-owned files block the build service.  The full table of who can change what is in `README.md`.
- **Passwords:** stored as salted PBKDF2 hashes in `/etc/omnislate/gms.json` (readable by root and `omnibuild` only).  The same password is set for Samba.
- **Build button:** only accepts campaign names from that GM's own list, and passes them to `build.py` without a shell.

Tested in a sandbox: the build page (logins, campaign scoping, path tricks, cross-site posts, video range requests, auto-build, lockout) and every `omnictl` step.  Samba and ACL commands were simulated there, so this box is their first real run.  `omnictl` runs `testparm` before restarting Samba and stops if the share settings are rejected.
