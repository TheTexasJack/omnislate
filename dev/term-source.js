  /* ---------- ANDIS terminal (signals) ---------- */
  // A separate retro workstation.  The players plug in the keyboard, LOAD the signal by its program
  // name, route the carriers, wait out the real-clock countdown, and read the decoded packet.
  const SIGNALS = Array.isArray(DATA.signals) ? DATA.signals : [];
  /*__FONT5__*/
  const TM = { open:false, connected:false, mode:"off", lines:[], input:"", loaded:null, busy:false,
               route:null, reveal:null, print:null, stack:[], k:1, gmSel:0, plug:{x:0, y:0}, drag:null, cols:40, rows:12 };
  const PAL = { bg:"#2B2170", text:"#A8A0F0", dim:"#7068C0", bad:"#FF8A8A", amb:"#F2C14E", ok:"#9AE29B", hi:"#EDF171" };
  const CARRIER = ["#EDF171", "#9AE29B", "#6ABFC6", "#F2A65A", "#F7A1C4"];
  const OX = 3, OY = 3;
  const SIGKEY = "omnislate-signal:" + String(CAMP.id || "").split("/")[0] + ":";
  const memSig = {};
  function sget(id){
    try{ const v = JSON.parse(localStorage.getItem(SIGKEY + id) || "null"); if (v) return v; }catch(e){}
    return memSig[id] || null;
  }
  function sset(id, v){
    memSig[id] = v;
    try{ v ? localStorage.setItem(SIGKEY + id, JSON.stringify(v)) : localStorage.removeItem(SIGKEY + id); }catch(e){}
  }
  const OUT = DATA.session.output || DATA.session.title;
  SIGNALS.forEach(s => {
    const st = s.start || {}, cur = sget(s.id);
    if (st.mode === "decoded" && (!cur || cur.s !== "decoded")) sset(s.id, { s:"decoded", seen:false, src:OUT });
    if (st.mode === "running" && (!cur || cur.src !== OUT))
      sset(s.id, { s:"running", end:Date.now() + st.left * 1000, total:Math.max(st.left, s.time) * 1000, src:OUT });
  });
  function sigNow(s){
    const v = sget(s.id);
    if (!v) return { s:"fresh" };
    if (v.s === "running" && Date.now() >= v.end){ const d = { s:"decoded", seen:false, src:v.src }; sset(s.id, d); return d; }
    return v;
  }
  const leftMs = v => v.s === "paused" ? v.left : Math.max(0, v.end - Date.now());
  function clock(ms){
    const t = Math.ceil(ms / 1000), h = t / 3600 | 0, m = (t % 3600) / 60 | 0, s = t % 60;
    return [h, m, s].map(n => String(n).padStart(2, "0")).join(":");
  }

  /* sounds: all synthesized, all follow the GM panel Sound switch */
  function tone(type, f0, f1, dur, gain, delay){
    if (!soundOn || !actx) return;
    try{
      const t0 = actx.currentTime + (delay || 0), o = actx.createOscillator(), g = actx.createGain();
      o.type = type; o.frequency.setValueAtTime(f0, t0);
      if (f1 && f1 !== f0) o.frequency.exponentialRampToValueAtTime(f1, t0 + dur);
      g.gain.setValueAtTime(gain, t0); g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
      o.connect(g); g.connect(actx.destination); o.start(t0); o.stop(t0 + dur + 0.02);
    }catch(e){}
  }
  function hiss(dur, gain, freq, delay){
    if (!soundOn || !actx) return;
    try{
      const n = Math.max(1, Math.floor(actx.sampleRate * dur)), b = actx.createBuffer(1, n, actx.sampleRate), d = b.getChannelData(0);
      for (let i = 0; i < n; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / n);
      const s = actx.createBufferSource(), f = actx.createBiquadFilter(), g = actx.createGain();
      f.type = "bandpass"; f.frequency.value = freq; g.gain.value = gain; s.buffer = b;
      s.connect(f); f.connect(g); g.connect(actx.destination); s.start(actx.currentTime + (delay || 0));
    }catch(e){}
  }
  const SFX = {
    key(){ hiss(0.02, 0.5, 3200); },
    thunk(){ tone("sine", 120, 38, 0.24, 0.5); hiss(0.07, 0.6, 700); },
    hum(){ tone("sawtooth", 60, 57, 0.5, 0.05); },
    drive(ms){ for (let t = 0; t < ms / 1000; t += 0.12) if (Math.random() < 0.75) tone("square", 170, 120, 0.03, 0.07, t);
               tone("triangle", 52, 50, ms / 1000, 0.03); },
    lock(){ tone("square", 880, 880, 0.06, 0.05); tone("square", 1320, 1320, 0.07, 0.04, 0.07); },
    buzz(){ tone("square", 110, 90, 0.25, 0.07); },
    done(){ tone("sine", 660, 660, 0.18, 0.14); tone("sine", 990, 990, 0.4, 0.12, 0.16); },
    print(ms){ const lines = Math.max(4, Math.round(ms / 190));
      for (let l = 0; l < lines; l++){ const t0 = l * ms / 1000 / lines;
        for (let k = 0; k < 9; k++) if (Math.random() < 0.8) tone("square", 1900 + Math.random() * 700, 0, 0.006, 0.045, t0 + k * 0.013);
        tone("sine", 150, 90, 0.05, 0.12, t0 + 0.13); } },
  };

  /* the pixel font */
  const GLYPHS = Object.keys(FONT5), GIDX = {};
  GLYPHS.forEach((ch, i) => { GIDX[ch] = i; });
  const atlas = {};
  function atlasFor(color){
    if (atlas[color]) return atlas[color];
    const cv = document.createElement("canvas"); cv.width = GLYPHS.length * 6; cv.height = 10;
    const x = cv.getContext("2d"); x.fillStyle = color;
    GLYPHS.forEach((ch, i) => {
      const g = FONT5[ch];
      for (let r = 0; r < g.length; r++){ const v = parseInt(g[r], 32); for (let b = 0; b < 5; b++) if (v >> (4 - b) & 1) x.fillRect(i * 6 + b, r, 1, 1); }
    });
    return (atlas[color] = cv);
  }
  // Text becomes cells.  Characters the font lacks, and combining marks, show as sensor noise.
  function cells(str){
    const out = [];
    for (const ch of String(str)){
      if (/[̀-ͯ᪰-᫿⃐-⃿]/.test(ch)){ if (out.length) out[out.length - 1].g = true; continue; }
      const c = ch === "—" || ch === "–" ? "-" : ch;
      out.push({ c, g: GIDX[c] === undefined });
    }
    return out;
  }
  function drawCell(x, cell, col, row, color){
    const px = OX + col * 6, py = OY + row * 10;
    if (cell.g){
      x.fillStyle = color;
      for (let k = 0; k < 10; k++) if (Math.random() < 0.55) x.fillRect(px + (Math.random() * 5 | 0), py + (Math.random() * 8 | 0), 1, 1);
      if (GIDX[cell.c] === undefined) return;
    }
    const i = GIDX[cell.c]; if (i === undefined || cell.c === " ") return;
    x.drawImage(atlasFor(color), i * 6, 0, 6, 10, px, py, 6, 10);
  }
  function put(x, str, col, row, color){ cells(str).forEach((c, i) => drawCell(x, c, col + i, row, color)); }
  function wrap(str, cols){
    const cs = cells(str); if (!cs.length) return [[]];
    const out = []; let line = [];
    let i = 0;
    while (i < cs.length){
      let j = i; while (j < cs.length && cs[j].c !== " ") j++;
      const word = cs.slice(i, j);
      if (line.length && line.length + 1 + word.length > cols){ out.push(line); line = []; }
      else if (line.length) line.push({ c:" ", g:false });
      while (word.length > cols){ out.push(word.splice(0, cols)); }
      line.push(...word);
      i = j + 1;
    }
    out.push(line); return out;
  }
  const COLOR = cls => ({ bad:PAL.bad, amb:PAL.amb, hi:PAL.hi, ok:PAL.ok }[cls] || PAL.text);

  /* layout: the stage is drawn at a fixed size and scaled to the screen */
  const stage = $("tmStage"), glass = $("tmGlass"), cv = $("tmCv"), plug = $("tmPlug");
  function sizeCanvas(){
    const w = Math.max(60, Math.floor(cv.clientWidth / 2)), h = Math.max(40, Math.floor(cv.clientHeight / 2));
    if (cv.width !== w || cv.height !== h){ cv.width = w; cv.height = h; }
    TM.cols = Math.floor((w - OX * 2) / 6); TM.rows = Math.floor((h - OY) / 10);
  }
  function anchors(){
    const mon = $("tmMon"), kb = $("tmKb"), jack = $("tmJack"), port = $("tmPort");
    const J = { x: mon.offsetLeft + mon.offsetWidth + 2, y: mon.offsetTop + jack.offsetTop + 9 };
    const P = { x: kb.offsetLeft + port.offsetLeft + 26, y: kb.offsetTop + port.offsetTop + 14 };
    const portrait = stage.classList.contains("port");
    const rest = portrait ? { x: mon.offsetLeft + mon.offsetWidth - 40, y: mon.offsetTop + mon.offsetHeight + 22 }
                          : { x: kb.offsetLeft + kb.offsetWidth + 38, y: kb.offsetTop + 56 };
    return { J, P, rest };
  }
  function placeWire(){
    const a = anchors(), p = TM.connected ? { x: a.P.x, y: a.P.y - 22 } : (TM.drag ? TM.plug : a.rest);
    if (!TM.drag) TM.plug = { x: p.x, y: p.y };
    const q = TM.plug;
    plug.style.left = (q.x - 12) + "px"; plug.style.top = q.y + "px";
    const d = `M${a.J.x} ${a.J.y} C ${a.J.x + 70} ${a.J.y}, ${q.x} ${q.y - 80}, ${q.x} ${q.y}`;
    $("tmCable0").setAttribute("d", d); $("tmCable1").setAttribute("d", d);
    const h = $("tmHint");
    if (stage.classList.contains("port")){ h.style.left = (a.rest.x - 150) + "px"; h.style.top = (a.rest.y - 4) + "px"; }
    else { h.style.left = (a.rest.x - 50) + "px"; h.style.top = (a.rest.y + 52) + "px"; }
  }
  function tmLayout(){
    if (!TM.open) return;
    const vw = window.innerWidth, vh = window.innerHeight, portrait = vh > vw * 1.1;
    stage.classList.toggle("port", portrait);
    const W = portrait ? 860 : 1088, H = portrait ? 1180 : 680, k = Math.min(vw / W, vh / H);
    stage.style.transform = `translate(${(vw - W * k) / 2}px, ${(vh - H * k) / 2}px) scale(${k})`;
    TM.k = k; sizeCanvas(); placeWire(); tmDraw();
  }
  window.addEventListener("resize", tmLayout);

  /* keyboard */
  const ROWS = ["1 2 3 4 5 6 7 8 9 0", "Q W E R T Y U I O P", "A S D F G H J K L \"", "Z X C V B N M , DEL", "SPACE RETURN"];
  ROWS.forEach(r => {
    const row = el("div", "tm-row");
    r.split(" ").forEach(k => {
      const b = el("button", "tm-key" + (k === "DEL" ? " w2" : k === "SPACE" ? " space" : k === "RETURN" ? " ret" : ""), k);
      b.type = "button"; b.dataset.k = k; row.append(b);
    });
    $("tmKeys").append(row);
  });
  ["F1", "F2", "F3", "F4"].forEach(k => { const b = el("button", "tm-key", k); b.type = "button"; b.dataset.k = k; $("tmFkeys").append(b); });
  function keyDown(b){ b.classList.add("down"); setTimeout(() => b.classList.remove("down"), 110); }
  stage.addEventListener("pointerdown", e => {
    const b = e.target.closest(".tm-key"); if (!b) return;
    e.preventDefault(); keyDown(b); press(b.dataset.k);
  });
  let hintTimer = 0;
  function noInput(){
    const led = $("tmLed"); led.classList.remove("blink"); void led.offsetWidth; led.classList.add("blink");
    const h = $("tmHint"); h.textContent = "NO INPUT DEVICE"; clearTimeout(hintTimer);
    hintTimer = setTimeout(() => { h.textContent = "DRAG THE CABLE TO THE PORT"; }, 1400);
  }
  function press(k){
    if (!TM.connected){ noInput(); return; }
    SFX.key();
    if (/^F\d$/.test(k)) return;
    if (TM.mode === "print"){ if (k === "RETURN") printTap(); return; }
    if (TM.mode === "media"){ if (k === "RETURN") mediaBack(); else if (k === "SPACE") mediaToggle(); return; }
    if (TM.mode === "reveal" || TM.mode === "count"){
      if (k === "RETURN"){
        if (TM.mode === "reveal" && TM.stack.length) goBack();
        else { TM.mode = "prompt"; TM.stack = []; say("READY."); tmDraw(); }
      }
      return;
    }
    if (TM.mode !== "prompt" || TM.busy) return;
    if (k === "RETURN") return enter();
    if (k === "DEL"){ TM.input = TM.input.slice(0, -1); tmDraw(); return; }
    const ch = k === "SPACE" ? " " : k;
    if (TM.input.length < Math.min(60, TM.cols * 2 - 1)){ TM.input += ch; tmDraw(); }
  }
  document.addEventListener("keydown", e => {
    if (!TM.open || e.ctrlKey || e.metaKey || e.altKey || !$("gm").hidden) return;
    let k = null;
    if (e.key === "Enter") k = "RETURN";
    else if (e.key === "Backspace") k = "DEL";
    else if (e.key === " ") k = "SPACE";
    else if (e.key === "Escape"){ e.preventDefault(); closeTerm(); return; }
    else if (/^[a-zA-Z0-9",]$/.test(e.key)) k = e.key.toUpperCase();
    if (!k) return;
    e.preventDefault();
    const b = stage.querySelector(`.tm-key[data-k='${k === '"' ? '\\"' : k}']`); if (b) keyDown(b);
    press(k);
  });

  /* the prompt */
  let srText = "";
  function say(t, cls){
    TM.lines.push([cls || "", t]); if (TM.lines.length > 240) TM.lines.splice(0, 60);
    srText = (srText + "  " + t).slice(-300); $("tmSr").textContent = t;
  }
  function enter(){
    const cmd = TM.input.trim(); say(TM.input); TM.input = "";
    if (!cmd){ tmDraw(); return; }
    const m = cmd.match(/^LOAD\s*"([^"]*)"?\s*(?:,\s*\d+\s*(?:,\s*\d+\s*)?)?$/i);
    if (m) return doLoad(m[1].trim().toUpperCase());
    if (/^RUN$/i.test(cmd)) return doRun();
    say("?SYNTAX  ERROR"); say("READY."); tmDraw();
  }
  function doLoad(name){
    if (!name){ say("?MISSING FILE NAME  ERROR"); say("READY."); tmDraw(); return; }
    TM.busy = true; say("SEARCHING FOR " + name); tmDraw();
    const sig = SIGNALS.find(s => s.program === name);
    setTimeout(() => {
      if (!TM.connected) return;
      if (!sig){ say("?FILE NOT FOUND  ERROR"); say("READY."); TM.busy = false; tmDraw(); return; }
      const ms = motion ? 2600 : 500;
      say("LOADING"); TM.mode = "loading"; glass.classList.add("load"); $("tmDrive").classList.add("on"); SFX.drive(ms); tmDraw();
      setTimeout(() => {
        glass.classList.remove("load"); $("tmDrive").classList.remove("on");
        if (!TM.connected) return;
        TM.mode = "prompt"; TM.loaded = sig; TM.busy = false; say("READY."); tmDraw();
      }, ms);
    }, motion ? 900 : 150);
  }
  function doRun(){
    if (!TM.loaded){ say("READY."); tmDraw(); return; }
    const v = sigNow(TM.loaded);
    if (v.s === "decoded") startReveal(!v.seen);
    else if (v.s === "running" || v.s === "paused"){ TM.mode = "count"; tmDraw(); }
    else if (!TM.loaded.routes) startCount(0);
    else startRoute();
  }
  function drawPrompt(x){
    const rows = [];
    TM.lines.forEach(([cls, t]) => wrap(t, TM.cols).forEach(cs => rows.push([cls, cs])));
    if (TM.mode === "prompt" && !TM.busy){
      const cur = (Date.now() / 420 | 0) % 2 ? "█" : " ";
      wrap(TM.input + cur, TM.cols).forEach(cs => rows.push(["", cs]));
    }
    rows.slice(-TM.rows).forEach(([cls, cs], r) => cs.forEach((c, i) => drawCell(x, c, i, r, COLOR(cls))));
  }

  /* signal routing: link matching carriers without crossing.  A crossed line costs time. */
  function tmRng(seed){ let a = seed >>> 0; return () => { a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function genRoute(cols, rows, k, R){
    for (let attempt = 0; attempt < 300; attempt++){
      const occ = new Array(cols * rows).fill(-1), pairs = [], sol = [];
      let ok = true;
      for (let p = 0; p < k && ok; p++){
        let made = null;
        for (let t = 0; t < 80 && !made; t++){
          const free = []; occ.forEach((v, i) => { if (v < 0) free.push(i); });
          if (!free.length) break;
          let cur = free[R() * free.length | 0]; const path = [cur], seen = new Set([cur]);
          const want = 4 + (R() * (cols - 1) | 0);
          while (path.length < want){
            const cx = cur % cols, cy = cur / cols | 0;
            const nb = [[1,0],[-1,0],[0,1],[0,-1]].map(([dx, dy]) => [cx + dx, cy + dy])
              .filter(([a, b]) => a >= 0 && b >= 0 && a < cols && b < rows).map(([a, b]) => b * cols + a)
              .filter(i => occ[i] < 0 && !seen.has(i));
            if (!nb.length) break;
            cur = nb[R() * nb.length | 0]; path.push(cur); seen.add(cur);
          }
          const a = path[0], b = path[path.length - 1];
          if (path.length >= 4 && Math.abs(a % cols - b % cols) + Math.abs((a / cols | 0) - (b / cols | 0)) >= 2) made = path;
        }
        if (!made){ ok = false; break; }
        made.forEach(i => { occ[i] = p; }); pairs.push([made[0], made[made.length - 1]]); sol.push(made);
      }
      if (ok) return { pairs, sol };
    }
    return null;
  }
  function routeGeom(){
    const portrait = stage.classList.contains("port"), cols = 8, rows = portrait ? 6 : 4;
    const top = OY + 13, bot = cv.height - 14;
    const cw = Math.floor((cv.width - 8) / cols), ch = Math.floor((bot - top) / rows);
    return { cols, rows, cw, ch, x0: Math.floor((cv.width - cw * cols) / 2), y0: top };
  }
  function startRoute(){
    const g = routeGeom(), s = TM.loaded;
    let seed = 0; for (const c of s.id + Date.now()) seed = (seed * 31 + c.charCodeAt(0)) | 0;
    const R = tmRng(seed), k = Math.min(s.routes, g.rows + 1);
    const made = genRoute(g.cols, g.rows, k, R) || genRoute(g.cols, g.rows, 2, R), pairs = made.pairs;
    TM.route = { g, pairs, sol: made.sol, paths: pairs.map(() => []), locked: pairs.map(() => false), drawing: -1, penalty: 0, msg: "" };
    TM.mode = "route"; tmDraw();
  }
  function cellAt(e){
    const r = cv.getBoundingClientRect(), g = TM.route.g;
    const nx = (e.clientX - r.left) * cv.width / r.width, ny = (e.clientY - r.top) * cv.height / r.height;
    const cx = Math.floor((nx - g.x0) / g.cw), cy = Math.floor((ny - g.y0) / g.ch);
    if (cx < 0 || cy < 0 || cx >= g.cols || cy >= g.rows) return -1;
    return cy * g.cols + cx;
  }
  function ownerAt(i){
    const R = TM.route;
    for (let p = 0; p < R.pairs.length; p++){ if (R.pairs[p].includes(i)) return { p, end: true }; if (R.paths[p].includes(i)) return { p, end: false }; }
    return null;
  }
  function routeStep(target){
    const R = TM.route, p = R.drawing; if (p < 0 || target < 0) return;
    const cols = R.g.cols, path = R.paths[p];
    let guard = 40;
    while (guard-- && path.length && path[path.length - 1] !== target){
      const last = path[path.length - 1], lx = last % cols, ly = last / cols | 0, tx = target % cols, ty = target / cols | 0;
      const dx = Math.sign(tx - lx), dy = Math.sign(ty - ly);
      const n = Math.abs(tx - lx) >= Math.abs(ty - ly) ? ly * cols + lx + dx : (ly + dy) * cols + lx;
      if (path.length > 1 && path[path.length - 2] === n){ path.pop(); continue; }
      const at = path.indexOf(n);
      if (at >= 0){ path.length = at + 1; continue; }
      const o = ownerAt(n);
      if (o && o.p !== p){
        R.penalty += TM.loaded.penalty; R.paths[p] = []; R.drawing = -1;
        R.msg = "CROSSTALK  +" + clock(TM.loaded.penalty * 1000);
        glass.classList.remove("zap"); void glass.offsetWidth; glass.classList.add("zap"); SFX.buzz();
        return;
      }
      path.push(n);
      if (o && o.p === p && o.end && n !== path[0]){
        R.locked[p] = true; R.drawing = -1; SFX.lock();
        if (R.locked.every(Boolean)){
          R.msg = "CARRIERS LOCKED"; tmDraw();
          setTimeout(() => { if (TM.mode === "route") startCount(R.penalty); }, motion ? 900 : 200);
        }
        return;
      }
    }
  }
  cv.addEventListener("pointerdown", e => {
    if (TM.mode === "print"){ printTap(); return; }
    if (TM.mode === "media"){ mediaTap(e); return; }
    if (TM.mode === "reveal"){ TM.reveal.dragY = e.clientY; TM.reveal.downY = e.clientY; TM.reveal.dragS = TM.reveal.scroll; cv.setPointerCapture(e.pointerId); return; }
    if (TM.mode !== "route") return;
    const R = TM.route, i = cellAt(e); if (i < 0) return;
    const o = ownerAt(i); if (!o) return;
    cv.setPointerCapture(e.pointerId);
    if (o.end){ R.paths[o.p] = [i]; R.locked[o.p] = false; }
    else if (!R.locked[o.p]) R.paths[o.p].length = R.paths[o.p].indexOf(i) + 1;
    else return;
    R.drawing = o.p; R.msg = ""; tmDraw();
  });
  cv.addEventListener("pointermove", e => {
    if (TM.mode === "reveal" && TM.reveal && TM.reveal.dragY != null){
      const k = cv.getBoundingClientRect().height / cv.height * 10;
      TM.reveal.scroll = TM.reveal.dragS - Math.round((e.clientY - TM.reveal.dragY) / k); clampScroll(); tmDraw(); return;
    }
    if (TM.mode !== "route" || TM.route.drawing < 0) return;
    routeStep(cellAt(e)); tmDraw();
  });
  const endDrag = () => { if (TM.route) TM.route.drawing = -1; if (TM.reveal) TM.reveal.dragY = null; };
  cv.addEventListener("pointerup", e => {
    const R = TM.reveal;
    if (TM.mode === "reveal" && R && R.dragY != null && Math.abs(e.clientY - R.downY) < 8) { endDrag(); tapRow(e); return; }
    endDrag();
  });
  cv.addEventListener("pointercancel", endDrag);
  cv.addEventListener("wheel", e => { if (TM.mode !== "reveal") return; e.preventDefault(); TM.reveal.scroll += Math.sign(e.deltaY) * 2; clampScroll(); tmDraw(); }, { passive:false });
  function drawRoute(x){
    const R = TM.route, g = R.g, done = R.locked.filter(Boolean).length;
    put(x, "SIGNAL ROUTING", 0, 0, PAL.text);
    const tag = "CARRIERS " + done + "/" + R.pairs.length; put(x, tag, TM.cols - tag.length, 0, PAL.text);
    const cen = i => [g.x0 + (i % g.cols) * g.cw + g.cw / 2, g.y0 + (i / g.cols | 0) * g.ch + g.ch / 2];
    x.fillStyle = PAL.dim;
    for (let i = 0; i < g.cols * g.rows; i++){ const [cx, cy] = cen(i); x.fillRect(cx - 1, cy - 1, 2, 2); }
    R.paths.forEach((path, p) => {
      if (path.length < 2) return;
      x.strokeStyle = CARRIER[p]; x.lineWidth = 3; x.lineJoin = "round"; x.beginPath();
      path.forEach((i, n) => { const [cx, cy] = cen(i); n ? x.lineTo(cx, cy) : x.moveTo(cx, cy); }); x.stroke();
    });
    R.pairs.forEach((pr, p) => pr.forEach(i => {
      const [cx, cy] = cen(i); x.fillStyle = CARRIER[p];
      if (R.locked[p]) x.fillRect(cx - 5, cy - 5, 10, 10);
      else { x.fillRect(cx - 5, cy - 5, 10, 2); x.fillRect(cx - 5, cy + 3, 10, 2); x.fillRect(cx - 5, cy - 5, 2, 10); x.fillRect(cx + 3, cy - 5, 2, 10); }
    }));
    const foot = R.msg || "LINK EACH PAIR.  CROSSING LINES COST TIME";
    put(x, foot.slice(0, TM.cols), 0, TM.rows - 1, R.msg.startsWith("CROSS") ? PAL.bad : R.msg ? PAL.ok : PAL.dim);
  }

  /* countdown */
  function startCount(pen){
    const s = TM.loaded, total = (s.time + pen) * 1000;
    sset(s.id, { s:"running", end: Date.now() + total, total, src: OUT });
    TM.mode = "count"; TM.route = null; tmDraw(); ringUpdate();
  }
  function drawCount(x){
    const s = TM.loaded, v = sigNow(s);
    if (v.s === "decoded"){ startReveal(true); return; }
    if (v.s === "fresh"){ TM.mode = "prompt"; say("READY."); drawPrompt(x); return; }
    const left = leftMs(v), total = v.total || s.time * 1000, frac = Math.min(1, Math.max(0, 1 - left / total));
    put(x, ("DECRYPTING " + (s.title || "SIGNAL")).toUpperCase().slice(0, TM.cols), 0, 0, PAL.text);
    put(x, ("PROGRAM " + s.program).slice(0, TM.cols), 0, 1, PAL.dim);
    const t = clock(left); put(x, "TIME REMAINING", 0, 3, PAL.text); put(x, t, TM.cols - t.length, 3, PAL.hi);
    const c = (s.corruption * left / total).toFixed(1) + "%"; put(x, "CORRUPTION", 0, 4, PAL.text); put(x, c, TM.cols - c.length, 4, PAL.text);
    const bw = TM.cols * 6 - 2, by = OY + 5 * 10 + 1;
    x.strokeStyle = PAL.text; x.lineWidth = 1; x.strokeRect(OX + 0.5, by + 0.5, bw, 7);
    x.fillStyle = PAL.text; x.fillRect(OX + 2, by + 2, Math.round((bw - 3) * frac), 4);
    if (v.s === "paused") put(x, "SIGNAL HOLD", 0, 6, PAL.amb);
    let row = 7;
    (s.encoded || []).forEach(([cls, line]) => wrap(line, TM.cols).forEach(cs => {
      if (row < TM.rows) cs.forEach((cc, i) => drawCell(x, cc, i, row, PAL.dim)); row++;
    }));
    if (motion){ x.fillStyle = PAL.text; for (let k = 0; k < 40; k++) x.fillRect(Math.random() * cv.width | 0, OY + 70 + Math.random() * (cv.height - 70) | 0, 1, 1); }
  }

  /* reveal: the decoded packet scrubs in from the noise */
  const SCRAMBLE = "ABCDEFGHJKLMNPQRSTUVWXYZ0123456789#%&@$*+=<>";
  const imgCache = {};
  function loadImg(src){
    if (!imgCache[src]){ const im = new Image(); im.onload = () => tmDraw(); im.src = src; imgCache[src] = im; }
    return imgCache[src];
  }
  const blank = act => ({ cls:"", cs: [], act });
  // An image sits in the row list as a run of empty rows, so it scrolls with the text.
  function addImage(view, src){
    view.imgAt = view.rows.length; view.imgRows = Math.max(4, TM.rows - 3); view.img = loadImg(src);
    for (let i = 0; i < view.imgRows; i++) view.rows.push(blank());
  }
  function addAttachments(rows, list){
    if (!list || !list.length) return;
    rows.push(blank()); rows.push({ cls:"amb", cs: cells("ATTACHED:") }); rows.push(blank());
    list.forEach(a => { rows.push({ cls:"hi", cs: cells(`[${a.kind}] ${a.name}`), act: a }); rows.push(blank(a)); });
  }
  function startReveal(scrub){
    const s = TM.loaded, view = { kind:"msg", rows: [], scroll: 0, dragY: null };
    s.decoded.forEach(([cls, line]) => wrap(line, TM.cols).forEach(cs => view.rows.push({ cls, cs })));
    if (s.image){ view.rows.push(blank()); view.rows.push({ cls:"amb", cs: cells("[ATTACHMENT]") }); addImage(view, s.image); }
    addAttachments(view.rows, s.attachments);
    view.chars = view.rows.reduce((n, r) => n + r.cs.length, 0);
    view.t0 = Date.now(); view.dur = scrub && motion ? Math.min(4000, 1200 + view.chars * 4) : 0; view.done = !scrub || !motion;
    TM.reveal = view; TM.stack = []; TM.mode = "reveal";
    if (view.done) finishReveal();
    tmDraw();
  }
  function finishReveal(){
    const R = TM.reveal; R.done = true;
    sset(TM.loaded.id, { s:"decoded", seen:true, src: OUT }); SFX.done(); ringUpdate();
    R.scroll = Math.max(0, R.rows.length - TM.rows + 1);
  }
  function clampScroll(){ const R = TM.reveal; R.scroll = Math.max(0, Math.min(R.scroll, Math.max(0, R.rows.length - TM.rows + 1))); }

  /* attachments: [T] text, [I] image, [D] print, [M] a folder shown as a disk directory */
  function backRows(rows){ rows.push({ cls:"hi", cs: cells("[BACK]"), act: "back" }); rows.push(blank("back")); }
  function pushView(view){ TM.stack.push(TM.reveal); view.scroll = 0; view.dragY = null; view.done = true; TM.reveal = view; TM.mode = "reveal"; tmDraw(); }
  function goBack(){ TM.reveal = TM.stack.pop() || TM.reveal; TM.mode = "reveal"; tmDraw(); }
  function tapRow(e){
    const r = cv.getBoundingClientRect(), ny = (e.clientY - r.top) * cv.height / r.height;
    const R = TM.reveal, ri = R.scroll + Math.floor((ny - OY) / 10), row = R.rows[ri];
    if (!R.done || !row || !row.act) return;
    SFX.key(); openAct(row.act);
  }
  function blocks(name){ let h = 7; for (const c of name) h = (h * 31 + c.charCodeAt(0)) % 997; return 1 + h % 38; }
  const DIRTYPE = { T:"SEQ", I:"USR", D:"PRG", A:"SND", V:"VID" };
  function openAct(a){
    if (a === "back") return goBack();
    if (a.kind === "D") return startPrint([a]);
    if (a.kind === "P") return startPrint(a.items);
    if (a.kind === "A" || a.kind === "V") return startMedia(a);
    const view = { kind: a.kind, rows: [] };
    backRows(view.rows);
    if (a.kind === "T"){
      view.rows.push({ cls:"hi", cs: cells(a.name) }); view.rows.push(blank());
      (a.text || []).forEach(([cls, line]) => wrap(line, TM.cols).forEach(cs => view.rows.push({ cls, cs })));
    } else if (a.kind === "I"){
      view.rows.push({ cls:"hi", cs: cells(a.name) });
      if (a.caption) wrap(a.caption, TM.cols).forEach(cs => view.rows.push({ cls:"", cs }));
      addImage(view, a.image);
    } else if (a.kind === "M"){
      const head = `0 "${a.name.padEnd(16)}" AN 2A`;
      view.rows.push({ cls:"hi", cs: cells(head.slice(0, TM.cols)) }); view.rows.push(blank());
      let used = 0;
      a.items.forEach(it => {
        const b = blocks(it.name); used += b;
        const line = `${String(b).padEnd(4)}${('"' + it.name + '"').padEnd(19)}${DIRTYPE[it.kind]}`;
        view.rows.push({ cls:"", cs: cells(line.slice(0, TM.cols)), act: it }); view.rows.push(blank(it));
      });
      const prints = a.items.filter(it => it.kind === "D");
      if (prints.length > 1){
        const line = `${"0".padEnd(4)}${'"PRINT ALL"'.padEnd(19)}PRG`;
        const all = { kind:"P", name:"PRINT ALL", items: prints };
        view.rows.push({ cls:"amb", cs: cells(line.slice(0, TM.cols)), act: all }); view.rows.push(blank(all));
      }
      view.rows.push({ cls:"", cs: cells(`${Math.max(0, 664 - used)} BLOCKS FREE.`) });
    }
    pushView(view);
  }

  /* audio and video: content, so they play whatever the Sound switch says (it covers effects only) */
  const mediaEls = {};
  function startMedia(a){
    stopMedia();
    const key = a.kind + ":" + a.name;
    let el = mediaEls[key];
    if (!el){
      el = document.createElement(a.kind === "A" ? "audio" : "video");
      el.preload = "auto"; el.playsInline = true; el.setAttribute("playsinline", "");
      el.addEventListener("error", () => { if (TM.media && TM.media.el === el){ TM.media.err = true; tmDraw(); } });
      el.addEventListener("ended", () => tmDraw());
      el.src = a.kind === "A" ? a.audio : a.video;
      mediaEls[key] = el;
    }
    TM.stack.push(TM.reveal);
    TM.media = { a, el, err: false, an: null };
    if (a.kind === "A" && actx){
      try{
        if (!el._an){ const src = actx.createMediaElementSource(el), an = actx.createAnalyser();
          an.fftSize = 128; src.connect(an); an.connect(actx.destination); el._an = an; }
        TM.media.an = el._an; actx.resume();
      }catch(e){}
    }
    try{ el.currentTime = 0; }catch(e){}
    el.play().catch(() => {});
    TM.mode = "media"; tmDraw();
  }
  function stopMedia(){ if (TM.media){ try{ TM.media.el.pause(); }catch(e){} TM.media = null; } }
  function mediaBack(){ stopMedia(); TM.reveal = TM.stack.pop() || TM.reveal; TM.mode = "reveal"; tmDraw(); }
  function mediaToggle(){
    const el = TM.media && TM.media.el; if (!el) return;
    if (el.ended){ el.currentTime = 0; el.play().catch(() => {}); }
    else if (el.paused) el.play().catch(() => {});
    else el.pause();
    tmDraw();
  }
  function mediaTap(e){
    const r = cv.getBoundingClientRect(), ny = (e.clientY - r.top) * cv.height / r.height;
    SFX.key();
    if (Math.floor((ny - OY) / 10) <= 1) return mediaBack();
    mediaToggle();
  }
  const mmss = t => { t = Math.max(0, Math.floor(isFinite(t) ? t : 0)); return String(t / 60 | 0).padStart(2, "0") + ":" + String(t % 60).padStart(2, "0"); };
  function drawMedia(x){
    const M = TM.media, el = M.el;
    const state = M.err ? "NO SIGNAL" : el.ended ? "ENDED" : el.paused ? "PAUSED" : "PLAYING";
    const col = M.err ? PAL.bad : (el.paused || el.ended) ? PAL.amb : PAL.ok;
    put(x, "[BACK]", 0, 0, PAL.hi);
    if (M.a.kind === "A") drawAudio(x, M, state, col); else drawVideo(x, M, state, col);
  }
  function drawAudio(x, M, state, col){
    const a = M.a, el = M.el, dur = isFinite(el.duration) ? el.duration : 0, t = el.currentTime || 0;
    const frac = el.ended ? 1 : dur ? Math.min(1, t / dur) : 0;
    put(x, a.name, 0, 1, PAL.hi);
    let row = 2;
    if (a.caption){ put(x, a.caption.slice(0, TM.cols), 0, row, PAL.text); row++; }
    const top = OY + row * 10 + 2, h = 34, bars = Math.floor(TM.cols * 6 / 4);
    let data = null;
    if (M.an && !el.paused){ data = new Uint8Array(M.an.frequencyBinCount); M.an.getByteFrequencyData(data); }
    for (let i = 0; i < bars; i++){
      const v = data ? data[Math.floor(i / bars * data.length * 0.7)] / 255
                     : el.paused ? 0.05 : 0.15 + 0.6 * Math.abs(Math.sin(i * 0.7 + Date.now() / 160)) * Math.random();
      const bh = Math.max(1, Math.round(v * h));
      x.fillStyle = i / bars <= frac ? PAL.hi : PAL.dim;
      x.fillRect(OX + i * 4, top + Math.round((h - bh) / 2), 3, bh);
    }
    row += 4;
    put(x, mmss(t) + " / " + mmss(dur), 0, row, PAL.text); put(x, state, TM.cols - state.length, row, col); row++;
    const lines = [];
    (a.transcript || []).forEach(([cls, l]) => wrap(l, TM.cols).forEach(cs => lines.push([cls, cs])));
    let show = Math.floor(lines.reduce((n, [, cs]) => n + cs.length, 0) * frac);
    const out = [];
    for (const [cls, cs] of lines){ if (show <= 0) break; out.push([cls, cs.slice(0, show)]); show -= cs.length; }
    const room = Math.max(0, TM.rows - row - 1);
    out.slice(-room || out.length).slice(0, room).forEach(([cls, cs], i) => cs.forEach((c, j) => drawCell(x, c, j, row + i, COLOR(cls))));
    put(x, el.ended ? "TAP TO REPLAY" : el.paused ? "TAP TO PLAY" : "TAP TO PAUSE", 0, TM.rows - 1, PAL.dim);
  }
  // The FMV look: CRT resolution, a dithered 64-color palette, interlace lines, about 10 frames a second.
  const vbuf = document.createElement("canvas"), vctx = vbuf.getContext("2d", { willReadFrequently: true });
  const BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5].map(v => (v / 16 - 0.5) * 40);
  let vTaint = false;
  function drawVideo(x, M, state, col){
    const el = M.el;
    put(x, M.a.name.slice(0, Math.max(0, TM.cols - 18)), 7, 0, PAL.hi);
    put(x, state, TM.cols - state.length, 0, col);
    const top = OY + 22, availW = cv.width - 2 * OX, availH = cv.height - top - 2;
    if (!el.videoWidth){ put(x, M.err ? "NO SIGNAL" : "ACQUIRING FEED...", 0, 3, M.err ? PAL.bad : PAL.dim); return; }
    const sc = Math.min(availW / el.videoWidth, availH / el.videoHeight);
    const w = Math.max(8, Math.floor(el.videoWidth * sc)), h = Math.max(8, Math.floor(el.videoHeight * sc));
    const ox = Math.floor((cv.width - w) / 2);
    if (vbuf.width !== w || vbuf.height !== h){ vbuf.width = w; vbuf.height = h; }
    vctx.drawImage(el, 0, 0, w, h);
    if (!vTaint){
      try{
        const img = vctx.getImageData(0, 0, w, h), d = img.data;
        for (let y = 0; y < h; y++){
          const dim = y & 1 ? 0.55 : 1;
          for (let xx = 0; xx < w; xx++){
            const i = (y * w + xx) * 4, b = BAYER[(y & 3) * 4 + (xx & 3)];
            for (let c = 0; c < 3; c++) d[i + c] = Math.max(0, Math.min(255, Math.round((d[i + c] + b) / 85) * 85)) * dim;
          }
        }
        vctx.putImageData(img, 0, 0);
      }catch(e){ vTaint = true; }   // a local file:// clip can't be read back, so it gets lines only
    }
    x.drawImage(vbuf, ox, top);
    if (vTaint){ x.fillStyle = "rgba(0,0,0,0.45)"; for (let y = top + 1; y < top + h; y += 2) x.fillRect(ox, y, w, 1); }
    const c0 = Math.ceil((ox - OX) / 6) + 1, r1 = Math.ceil((top - OY) / 10) + 1, r2 = Math.floor((top + h - OY) / 10) - 2;
    if (!el.paused && (Date.now() / 600 | 0) % 2) put(x, "REC", c0, r1, PAL.bad);
    const tc = mmss(el.currentTime);
    put(x, tc, Math.floor((ox + w - OX) / 6) - tc.length - 1, r2, "#f2efe6");
  }

  /* the printer: theater for the paper handout the GM slides across the table */
  const paper = $("tmPaper");
  function feedPaper(ms){
    paper.style.transition = "none"; paper.style.height = "0px"; void paper.offsetHeight;
    paper.style.transition = `height ${ms}ms steps(${Math.max(4, Math.round(ms / 190))})`; paper.style.height = "";
    paper.classList.add("out");
  }
  function startPrint(items){
    const per = items.length > 1 ? (motion ? 1600 : 300) : (motion ? 2800 : 400);
    TM.print = { items, per, i: 0, t0: Date.now(), done: false };
    TM.mode = "print"; $("tmPLight").classList.add("on");
    feedPaper(per); SFX.print(per); tmDraw();
  }
  function printFinish(){
    const P = TM.print; P.done = true; P.i = P.items.length;
    paper.style.transition = "none"; paper.style.height = ""; paper.classList.add("out");
    $("tmPLight").classList.remove("on"); tmDraw();
  }
  function printTap(){
    const P = TM.print; if (!P) return;
    if (!P.done) return printFinish();
    TM.print = null; TM.mode = "reveal"; tmDraw();
  }
  $("tmPrinter").addEventListener("click", () => { if (TM.mode === "print") printTap(); });
  function drawPrint(x){
    const P = TM.print;
    if (!P.done){
      const k = Math.floor((Date.now() - P.t0) / P.per);
      if (k >= P.items.length) printFinish();
      else if (k > P.i){ P.i = k; feedPaper(P.per); SFX.print(P.per); }
    }
    const rows = [];
    P.items.forEach((it, n) => {
      if (n < P.i) rows.push(["", `PRINTING ${it.name}... OK`]);
      else if (n === P.i && !P.done) rows.push(["", `PRINTING ${it.name}...`]);
    });
    if (P.done){ rows.push(["", ""]); rows.push(["ok", "PRINT COMPLETE."]); rows.push(["amb", "COLLECT OUTPUT."]); rows.push(["", ""]); rows.push(["hi", "TAP OR RETURN TO CONTINUE"]); }
    else { rows.push(["", ""]); rows.push(["dim", "TAP TO SKIP"]); }
    const out = []; rows.forEach(([cls, t]) => wrap(t, TM.cols).forEach(cs => out.push([cls, cs])));
    out.slice(-TM.rows).forEach(([cls, cs], r) => cs.forEach((c, i) => drawCell(x, c, i, r, cls === "dim" ? PAL.dim : COLOR(cls))));
  }
  function drawReveal(x){
    const R = TM.reveal, f = R.done ? 1 : Math.min(1, (Date.now() - R.t0) / R.dur), front = R.done ? Infinity : f * R.chars;
    let n = 0, frontRow = 0;
    R.rows.forEach((r, ri) => {
      r.cs.forEach((c, i) => {
        const real = n < front; n++;
        if (!real && c.c !== " ") r.scr = r.scr || [];
        const vr = ri - R.scroll;
        if (vr < 0 || vr >= TM.rows) return;
        if (real || c.c === " ") drawCell(x, c, i, vr, COLOR(r.cls));
        else drawCell(x, { c: SCRAMBLE[Math.random() * SCRAMBLE.length | 0], g:false }, i, vr, PAL.dim);
      });
      if (n <= front) frontRow = ri;
    });
    if (!R.done){
      R.scroll = Math.max(0, frontRow - TM.rows + 3);
      if (f >= 1) finishReveal();
    }
    const im = R.img;
    if (R.imgRows && R.done && im && im.complete && im.naturalWidth){
      const top = OY + (R.imgAt - R.scroll) * 10, maxW = TM.cols * 6, maxH = R.imgRows * 10;
      const sc = Math.min(maxW / im.naturalWidth, maxH / im.naturalHeight), w = im.naturalWidth * sc, h = im.naturalHeight * sc;
      x.imageSmoothingEnabled = true; x.drawImage(im, OX, top, w, h);
    }
    const total = R.rows.length;
    if (total > TM.rows){
      const H = cv.height - 6, bh = Math.max(8, H * TM.rows / total), by = 3 + (H - bh) * R.scroll / Math.max(1, total - TM.rows + 1);
      x.fillStyle = PAL.dim; x.fillRect(cv.width - 3, 3, 2, H); x.fillStyle = PAL.text; x.fillRect(cv.width - 3, by, 2, bh);
    }
  }

  function tmDraw(){
    if (!TM.open) return;
    const x = cv.getContext("2d"); x.imageSmoothingEnabled = false;
    x.fillStyle = PAL.bg; x.fillRect(0, 0, cv.width, cv.height);
    if (!TM.connected) return;
    if (TM.mode === "route") drawRoute(x);
    else if (TM.mode === "count") drawCount(x);
    else if (TM.mode === "reveal") drawReveal(x);
    else if (TM.mode === "print") drawPrint(x);
    else if (TM.mode === "media") drawMedia(x);
    else drawPrompt(x);
  }

  /* the cable */
  function setConnected(on){
    TM.connected = on;
    plug.classList.toggle("in", on);
    $("tmHint").hidden = on; $("tmLed").classList.toggle("on", on); $("tmPower").classList.toggle("on", on);
    $("tmKeys").classList.toggle("dead", !on); $("tmFkeys").classList.toggle("dead", !on);
  }
  function unplug(){
    stopMedia(); setConnected(false); TM.mode = "off"; TM.lines = []; TM.input = ""; TM.loaded = null; TM.busy = false;
    TM.route = null; TM.reveal = null; TM.print = null; TM.stack = []; glass.className = "tm-glass off"; $("tmDrive").classList.remove("on");
    paper.classList.remove("out"); $("tmPLight").classList.remove("on");
  }
  function plugIn(){
    setConnected(true); TM.drag = null; placeWire(); SFX.thunk();
    glass.className = "tm-glass warm";
    const pad = n => " ".repeat(Math.max(0, Math.floor((TM.cols - n) / 2)));
    const banner = "ANDIS UN.#30 COMMAND PROMPT";
    TM.lines = []; TM.mode = "boot"; tmDraw();
    setTimeout(() => {
      if (!TM.connected) return;
      glass.className = "tm-glass degauss"; SFX.hum();
      say(pad(banner.length) + banner); say(pad(16) + "3583 BYTES FREE"); say(""); say("READY.");
      TM.mode = "prompt"; tmDraw();
      setTimeout(() => { if (glass.classList.contains("degauss")) glass.className = "tm-glass"; }, 450);
    }, motion ? 800 : 50);
  }
  function stagePt(e){ const r = stage.getBoundingClientRect(); return { x: (e.clientX - r.left) / TM.k, y: (e.clientY - r.top) / TM.k }; }
  plug.addEventListener("pointerdown", e => {
    if (TM.connected) return;
    e.preventDefault(); plug.setPointerCapture(e.pointerId);
    const p = stagePt(e); TM.drag = { dx: TM.plug.x - p.x, dy: TM.plug.y - p.y }; plug.classList.add("drag");
  });
  plug.addEventListener("pointermove", e => {
    if (!TM.drag) return;
    const p = stagePt(e); TM.plug = { x: p.x + TM.drag.dx, y: p.y + TM.drag.dy };
    const P = anchors().P;
    if (Math.hypot(TM.plug.x - P.x, TM.plug.y + 17 - P.y) < 48){ plug.classList.remove("drag"); plugIn(); return; }
    placeWire();
  });
  function dropPlug(){
    if (!TM.drag) return;
    plug.classList.remove("drag");
    const from = { ...TM.plug }, to = anchors().rest, t0 = performance.now();
    const step = now => {
      const k = Math.min(1, (now - t0) / 260), e = 1 - Math.pow(1 - k, 3);
      TM.plug = { x: from.x + (to.x - from.x) * e, y: from.y + (to.y - from.y) * e }; placeWire();
      if (k < 1 && TM.drag) requestAnimationFrame(step); else TM.drag = null;
    };
    requestAnimationFrame(step);
  }
  plug.addEventListener("pointerup", dropPlug); plug.addEventListener("pointercancel", dropPlug);

  /* open, close, the top bar button */
  function openTerm(){
    unlockAudio(); TM.open = true; $("tm").hidden = false;
    const resume = TM.connected && ["route", "count", "reveal"].includes(TM.mode);
    if (!resume) unplug();
    TM.drag = null; tmLayout();
  }
  function closeTerm(){ if (TM.mode === "media") mediaBack(); TM.open = false; $("tm").hidden = true; TM.drag = null; endDrag(); }
  $("tmClose").addEventListener("click", closeTerm);
  $("bTerm").addEventListener("click", openTerm);
  function ringUpdate(){
    let frac = 0, done = false;
    const list = TM.loaded ? [TM.loaded, ...SIGNALS] : SIGNALS;
    for (const s of list){
      const v = sigNow(s);
      if (v.s === "running" || v.s === "paused"){ frac = Math.min(1, Math.max(0, 1 - leftMs(v) / (v.total || s.time * 1000))); break; }
      if (v.s === "decoded" && !v.seen) done = true;
    }
    $("bTermRing").style.strokeDashoffset = String(44 * (1 - (done ? 1 : frac)));
    $("bTerm").classList.toggle("done", done);
  }

  /* GM panel: Skip, Pause, Add time, Reset signal */
  function termGM(){
    $("gmSigBlock").hidden = !SIGNALS.length;
    if (!SIGNALS.length) return;
    const box = $("gmSigs"); box.replaceChildren();
    SIGNALS.forEach((s, i) => {
      const b = el("button", "gm-btn", s.program); b.type = "button"; b.setAttribute("aria-pressed", String(i === TM.gmSel));
      b.addEventListener("click", () => { TM.gmSel = i; termGM(); }); box.append(b);
    });
    termGMStatus();
  }
  function termGMStatus(){
    if (!SIGNALS.length) return;
    const s = SIGNALS[TM.gmSel], v = sigNow(s);
    const what = { fresh: "not started", running: "decrypting, " + clock(leftMs(v)) + " left",
                   paused: "on hold, " + clock(leftMs(v)) + " left", decoded: v.seen ? "decoded" : "decoded, not viewed yet" }[v.s];
    $("gmSigStatus").textContent = `${s.id} (LOAD "${s.program}"): ${what}`;
    $("gmSigPause").textContent = v.s === "paused" ? "Resume" : "Pause";
    $("gmSigPause").disabled = !(v.s === "running" || v.s === "paused");
    $("gmSigAdd").disabled = !(v.s === "running" || v.s === "paused");
    $("gmSigSkip").disabled = v.s === "decoded";
  }
  function gmSig(fn){ const s = SIGNALS[TM.gmSel]; if (!s) return; fn(s, sigNow(s)); termGMStatus(); ringUpdate(); tmDraw(); }
  $("gmSigSkip").addEventListener("click", () => gmSig(s => sset(s.id, { s:"decoded", seen:false, src: OUT })));
  $("gmSigPause").addEventListener("click", () => gmSig((s, v) => {
    if (v.s === "running") sset(s.id, { s:"paused", left: leftMs(v), total: v.total, src: v.src });
    else if (v.s === "paused") sset(s.id, { s:"running", end: Date.now() + v.left, total: v.total, src: v.src });
  }));
  $("gmSigAdd").addEventListener("click", () => gmSig((s, v) => {
    if (v.s === "running") sset(s.id, { ...v, end: v.end + 600000, total: v.total + 600000 });
    else if (v.s === "paused") sset(s.id, { ...v, left: v.left + 600000, total: v.total + 600000 });
  }));
  $("gmSigReset").addEventListener("click", () => gmSig(s => {
    sset(s.id, null);
    if (TM.loaded === s && ["route", "count", "reveal", "print", "media"].includes(TM.mode)){ stopMedia(); TM.stack = []; TM.print = null; TM.mode = "prompt"; TM.route = null; TM.reveal = null; say("READY."); }
  }));
  if (/[?&]omnitest\b/.test(location.search)) window.__omniTerm = TM;
  if (SIGNALS.length){
    $("bTerm").hidden = false;
    let blink = -1;
    setInterval(() => {
      ringUpdate();
      if (!$("gm").hidden) termGMStatus();
      if (!TM.open || !TM.connected) return;
      if (TM.mode === "prompt"){ const b = (Date.now() / 420 | 0) % 2; if (b !== blink){ blink = b; tmDraw(); } }
      else if (["count", "reveal", "print", "media"].includes(TM.mode)) tmDraw();
    }, 100);
  }

