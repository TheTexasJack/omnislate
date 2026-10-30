# OMNISLATE on unstableNHP: GM Guide (Windows)

Your campaign lives on Nathan's OMNISLATE server, unstableNHP.  You edit text files from your own PC, press Build in a web page, and open the finished session pages in any browser.  Nothing to install except Tailscale.

You need three things from Nathan: a **Tailscale invite link**, your **campaign folder name** (for example `iron-tide`), and your **password**.

---

## 1. Join the network (once)

1. Download **Tailscale for Windows** from tailscale.com/download and install it.
2. Open Nathan's invite link and sign in.  Tailscale shows a small icon by the clock when connected.
3. Test it: open a browser and go to `http://unstablenhp/`.  A login box means it works.

## 2. Map your campaign drive (once)

1. Open **File Explorer**, right-click **This PC**, and choose **Map network drive**.
2. **Drive:** any free letter, such as `O:`.
3. **Folder:** `\\unstablenhp\iron-tide` (use your own campaign name).
4. Tick **Reconnect at sign-in** and **Connect using different credentials**, then Finish.
5. User name: `jarrett`.  Password: the one Nathan gave you.  Tick **Remember my credentials**.

Optional: map `\\unstablenhp\omnislate` the same way.  It is a read-only reference copy of the whole workshop: README files, the shared world pool, and the starter example.

## 3. Edit

Your drive already holds a working sample campaign.  Open `README.md` in your campaign folder first.  It walks through every file.

- Edit `.md` files with **Notepad** (or any text editor).  Save normally.
- **Videos and pictures:** drag them into a chapter's `media/` (drone feed videos) or `images/` (world maps and stills).  Put them in the campaign folder's own `media/` or `images/` instead to share them with every chapter.  Name them after the world, such as `kestrel-surface.mp4`.
- Your folder is yours.  Nobody else's campaign shows up, and nobody else can open yours, apart from Nathan as server admin.

### Chapters

Your campaign folder holds one folder per **chapter**: a story arc, a season, or a separate group of players.  It starts with `chapter-1`.  Settings in the campaign folder (crest, skins, triggers, worlds, sounds) are shared by every chapter.  Each chapter keeps its own sessions, briefs, and videos.

To add a chapter:

1. In your campaign folder, right-click `_template`, choose **Copy**, then right-click an empty spot in the same folder and choose **Paste**.
2. Windows names the copy `_template - Copy`.  Right-click it, choose **Rename**, and give it a name in lowercase letters, numbers, and dashes, such as `season-2`.  (Until you rename it, the build skips it and the report says so.)
3. Open `campaign.md` inside it in Notepad and set `Name:`.

A few seconds later the chapter shows up on the build page with its own list of session files.  Renaming `chapter-1` works the same way.

## 4. Build

1. Go to `http://unstablenhp/` and log in.
2. Press **Build** for your campaign.  The report appears a few seconds later.
3. Lines in **green** built fine.  **Amber** `Warn` lines are small data problems, shown at the table as sensor glitches.  Fix them when you can.  **Red** `FAILED` lines name the file and line to fix.
4. Session links (ending in `.html`) are listed under each chapter's name.  Click one to open it.

Auto-build is usually on, so a saved file rebuilds by itself about five seconds later.  Refresh the build page to see the new report.

## 5. At the table

- **Laptop or tablet on Tailscale:** open the session link from the build page.  Videos play straight from the server.
- **No network at the table:** on the build page, right-click a session link and choose **Save link as**.  Copy that file plus the chapter's `media/` videos into one folder on the device and open the file from there.  (Use Save link as.  Saving an already open page with Ctrl+S can save a half-run copy.)

GM panel: hold the round badge in the top-left corner for one second, or press Ctrl+Shift+G.

ANDIS terminal: a session that lists signals has an ANDIS button in the top bar.  The players plug in the cable and type `LOAD "NAME",8,1`.  The sample is `signals/example.md` in your campaign folder, LOAD "BEACON".  Its timer keeps running between game nights, and the GM panel can skip, pause, or add time.

## 6. If something goes wrong

| Problem | Fix |
|---|---|
| `unstablenhp` will not load | Check Tailscale is connected (icon by the clock) |
| Drive will not connect after a password change | Open Command Prompt and run `net use * /delete`, then map the drive again |
| Login box keeps coming back | Five wrong passwords lock your PC out for one minute.  Wait, then try again |
| Build report says FAILED | It names the file and line.  Fix it, save, and build again |
| New chapter does not show up | Its name has spaces or capitals, or it still starts with `_`.  Rename it, such as `season-2` |
| Session page says "Sensor suite offline" | The browser or an ad or script blocker is blocking JavaScript.  Allow scripts for unstablenhp and reload |
| Anything else | Screenshot the build page and send it to Nathan |

Rules of the road: keep your files inside your campaign folder, keep the campaign folder's name as it is, and leave each `campaign.md` in place.  Chapter folders are yours to add and rename.  Everything else is yours to play with.
