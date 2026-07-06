# Tenant-Radar
Tenant Radar is used to push notifications about tenants with rental needs.
<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>租客雷達 — 自動找租客，即時推播給您</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Sans+TC:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:      #0d0f12;
  --surface: #13161b;
  --panel:   #1a1e25;
  --border:  #252a33;
  --border2: #2e3440;
  --green:   #00e87a;
  --green-d: #00b85f;
  --green-bg:#00e87a0d;
  --amber:   #ffb020;
  --amber-bg:#ffb0200d;
  --red:     #ff4d4d;
  --red-bg:  #ff4d4d0d;
  --blue:    #4da6ff;
  --blue-bg: #4da6ff0d;
  --text:    #e8ecf2;
  --muted:   #6b7584;
  --dim:     #3d4553;
}

body {
  font-family: 'Noto Sans TC', sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  font-size: 14px;
  line-height: 1.5;
}

/* ── SCANLINE AMBIENCE ── */
body::after {
  content: '';
  position: fixed;
  inset: 0;
  background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,.04) 2px, rgba(0,0,0,.04) 4px);
  pointer-events: none;
  z-index: 9999;
}

/* ── TOP BAR ── */
.topbar {
  height: 52px;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
  gap: 1rem;
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: 'IBM Plex Mono', monospace;
  font-weight: 600;
  font-size: 15px;
  letter-spacing: .02em;
}

.logo-dot {
  width: 10px; height: 10px;
  border-radius: 50%;
  background: var(--green);
  box-shadow: 0 0 10px var(--green);
  animation: throb 2s ease-in-out infinite;
}

@keyframes throb {
  0%,100% { box-shadow: 0 0 6px var(--green); }
  50%      { box-shadow: 0 0 18px var(--green), 0 0 32px var(--green-d); }
}

.logo-name { color: var(--text); }
.logo-tag  { color: var(--muted); font-weight: 400; font-size: 12px; }

.topbar-right {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.clock {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 13px;
  color: var(--muted);
}

.status-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-family: 'IBM Plex Mono', monospace;
  border: 1px solid;
}
.status-pill.on  { border-color: var(--green-d); color: var(--green); background: var(--green-bg); }
.status-pill.off { border-color: var(--border2); color: var(--muted); background: transparent; }

.pill-dot { width: 6px; height: 6px; border-radius: 50%; }
.on  .pill-dot { background: var(--green); animation: throb 1.5s infinite; }
.off .pill-dot { background: var(--dim); }

.toggle-radar-btn {
  padding: 5px 14px;
  border: 1px solid var(--border2);
  border-radius: 6px;
  background: transparent;
  color: var(--muted);
  font-size: 12px;
  cursor: pointer;
  font-family: 'IBM Plex Mono', monospace;
  transition: all .15s;
}
.toggle-radar-btn:hover {
  border-color: var(--red);
  color: var(--red);
}

/* ── LAYOUT ── */
.shell {
  display: grid;
  grid-template-columns: 260px 1fr 300px;
  grid-template-rows: auto 1fr;
  min-height: calc(100vh - 52px);
}

/* ── STAT BAR ── */
.statbar {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  border-bottom: 1px solid var(--border);
}

.stat {
  padding: 1rem 1.5rem;
  border-right: 1px solid var(--border);
}
.stat:last-child { border-right: none; }

.stat-label {
  font-size: 11px;
  font-family: 'IBM Plex Mono', monospace;
  color: var(--muted);
  letter-spacing: .08em;
  text-transform: uppercase;
  margin-bottom: 6px;
}

.stat-value {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 28px;
  font-weight: 600;
  line-height: 1;
  margin-bottom: 4px;
}
.stat-value.g { color: var(--green); }
.stat-value.a { color: var(--amber); }
.stat-value.b { color: var(--blue); }

.stat-delta {
  font-size: 11px;
  color: var(--muted);
  font-family: 'IBM Plex Mono', monospace;
}
.stat-delta.up { color: var(--green); }

/* ── LEFT SIDEBAR ── */
.sidebar {
  background: var(--surface);
  border-right: 1px solid var(--border);
  padding: 1.25rem 0;
  overflow-y: auto;
}

.sidebar-section { margin-bottom: 1.75rem; }

.sidebar-heading {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 10px;
  letter-spacing: .12em;
  color: var(--muted);
  text-transform: uppercase;
  padding: 0 1.25rem;
  margin-bottom: .75rem;
}

/* ── CHANNEL ITEMS ── */
.channel {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: .6rem 1.25rem;
  cursor: pointer;
  transition: background .15s;
  position: relative;
}
.channel:hover { background: var(--panel); }
.channel.active { background: var(--panel); }
.channel.active::before {
  content: '';
  position: absolute;
  left: 0; top: 20%; bottom: 20%;
  width: 2px;
  background: var(--green);
  border-radius: 0 2px 2px 0;
}

.ch-icon {
  width: 32px; height: 32px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}
.ch-fb     { background: #1877f21a; }
.ch-ptt    { background: #3cba541a; }
.ch-dcard  { background: #ff65651a; }
.ch-591    { background: #ff8c001a; }
.ch-line   { background: #06c7551a; }

.ch-info { flex: 1; min-width: 0; }
.ch-name { font-size: 13px; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.ch-sub  { font-size: 11px; color: var(--muted); }

.ch-badge {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 11px;
  padding: 2px 7px;
  border-radius: 10px;
  background: var(--green-bg);
  color: var(--green);
  border: 1px solid var(--green-d);
  flex-shrink: 0;
}
.ch-badge.off { background: transparent; color: var(--muted); border-color: var(--border2); }

/* ── TOGGLE ── */
.toggle-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: .5rem 1.25rem;
  font-size: 12px;
  color: var(--muted);
}

.toggle {
  position: relative;
  width: 34px; height: 18px;
  cursor: pointer;
}
.toggle input { opacity: 0; width: 0; height: 0; }
.toggle-track {
  position: absolute;
  inset: 0;
  border-radius: 9px;
  background: var(--border2);
  transition: background .2s;
}
.toggle input:checked + .toggle-track { background: var(--green-d); }
.toggle-thumb {
  position: absolute;
  top: 2px; left: 2px;
  width: 14px; height: 14px;
  border-radius: 50%;
  background: var(--muted);
  transition: transform .2s, background .2s;
}
.toggle input:checked ~ .toggle-thumb { transform: translateX(16px); background: #fff; }

.my-properties-container {
  padding: 0 1.25rem; 
  display: flex; 
  flex-direction: column; 
  gap: 6px;
}
.property-item {
  padding:8px 10px;
  background:var(--panel);
  border:1px solid var(--border2);
  border-radius:6px;
  font-size:12px;
}
.property-status {
  font-family:'IBM Plex Mono',monospace;
  font-size:11px;
  margin-bottom:3px;
}
.property-status.renting { color: var(--green); }
.property-status.soon { color: var(--amber); }
.property-meta { color:var(--muted); font-size:11px; }

/* ── MAIN FEED ── */
.feed {
  background: var(--bg);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.feed-header {
  padding: 1.25rem 1.5rem .75rem;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  background: var(--bg);
  z-index: 10;
}

.feed-title {
  font-size: 13px;
  font-family: 'IBM Plex Mono', monospace;
  color: var(--muted);
}

.feed-title strong { color: var(--text); }

.feed-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.ctrl-btn {
  padding: 5px 12px;
  border: 1px solid var(--border2);
  border-radius: 6px;
  background: transparent;
  color: var(--muted);
  font-size: 12px;
  font-family: 'IBM Plex Mono', monospace;
  cursor: pointer;
  transition: all .15s;
}
.ctrl-btn:hover { border-color: var(--green-d); color: var(--green); }
.ctrl-btn.active { border-color: var(--green-d); color: var(--green); background: var(--green-bg); }

/* ── LEAD CARDS ── */
.lead-list { padding: 1rem 1.25rem; display: flex; flex-direction: column; gap: 10px; }

.lead-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  transition: border-color .15s, transform .15s;
}
.lead-card:hover { border-color: var(--border2); transform: translateY(-1px); }
.lead-card.hot   { border-color: var(--green-d); }
.lead-card.sel   { border-color: var(--green); background: var(--panel); }

.lead-top {
  padding: 12px 14px;
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.lead-src-icon {
  width: 36px; height: 36px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
  margin-top: 1px;
}

.lead-body { flex: 1; min-width: 0; }

.lead-meta-row {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 5px;
  flex-wrap: wrap;
}

.lead-src-name {
  font-size: 11px;
  font-family: 'IBM Plex Mono', monospace;
  color: var(--muted);
}

.lead-time {
  font-size: 11px;
  font-family: 'IBM Plex Mono', monospace;
  color: var(--dim);
}

.score-bar {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
}

.score-num {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 12px;
  font-weight: 600;
}
.score-num.hi  { color: var(--green); }
.score-num.mid { color: var(--amber); }
.score-num.lo  { color: var(--muted); }

.score-ring {
  width: 28px; height: 28px;
  position: relative;
}
.score-ring svg { transform: rotate(-90deg); }

.lead-text {
  font-size: 13px;
  line-height: 1.55;
  color: var(--text);
  margin-bottom: 8px;
}

.lead-text .hl { color: var(--green); font-weight: 500; }

.lead-chips {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}

.lchip {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-family: 'IBM Plex Mono', monospace;
  background: var(--panel);
  border: 1px solid var(--border2);
  color: var(--muted);
}
.lchip.match { background: var(--green-bg); border-color: var(--green-d); color: var(--green); }

.lead-bottom {
  padding: 8px 14px;
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 8px;
}

.notify-btn {
  flex: 1;
  padding: 7px;
  border: 1px solid var(--green-d);
  border-radius: 6px;
  background: var(--green-bg);
  color: var(--green);
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  font-family: 'IBM Plex Mono', monospace;
  transition: all .15s;
  text-align: center;
}
.notify-btn:hover { background: var(--green); color: #000; }

.skip-btn {
  padding: 7px 12px;
  border: 1px solid var(--border2);
  border-radius: 6px;
  background: transparent;
  color: var(--muted);
  font-size: 12px;
  cursor: pointer;
  font-family: 'IBM Plex Mono', monospace;
  transition: all .15s;
}
.skip-btn:hover { border-color: var(--red); color: var(--red); }

.new-tag {
  padding: 1px 6px;
  border-radius: 3px;
  font-size: 10px;
  font-family: 'IBM Plex Mono', monospace;
  font-weight: 600;
  background: var(--green);
  color: #000;
  letter-spacing: .04em;
}

/* ── RIGHT PANEL ── */
.rpanel {
  background: var(--surface);
  border-left: 1px solid var(--border);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.rp-section {
  padding: 1.25rem;
  border-bottom: 1px solid var(--border);
}

.rp-title {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 10px;
  letter-spacing: .1em;
  color: var(--muted);
  text-transform: uppercase;
  margin-bottom: .875rem;
}

/* ── KEYWORD CONFIG ── */
.kw-list { display: flex; flex-direction: column; gap: 6px; margin-bottom: 10px; }

.kw-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  background: var(--panel);
  border: 1px solid var(--border2);
  border-radius: 6px;
  font-size: 12px;
  font-family: 'IBM Plex Mono', monospace;
}

.kw-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.kw-dot.g { background: var(--green); }
.kw-dot.a { background: var(--amber); }

.kw-text { flex: 1; color: var(--text); }
.kw-cnt  { color: var(--muted); font-size: 11px; }

.kw-rm {
  color: var(--dim);
  cursor: pointer;
  font-size: 14px;
  line-height: 1;
  background: none;
  border: none;
  padding: 0 2px;
}
.kw-rm:hover { color: var(--red); }

.add-kw-row {
  display: flex;
  gap: 6px;
}

.kw-input {
  flex: 1;
  padding: 6px 10px;
  background: var(--panel);
  border: 1px solid var(--border2);
  border-radius: 6px;
  font-size: 12px;
  font-family: 'IBM Plex Mono', monospace;
  color: var(--text);
  outline: none;
}
.kw-input:focus { border-color: var(--green-d); }
.kw-input::placeholder { color: var(--dim); }

.kw-add-btn {
  padding: 6px 12px;
  background: var(--green-bg);
  border: 1px solid var(--green-d);
  border-radius: 6px;
  color: var(--green);
  font-size: 12px;
  font-family: 'IBM Plex Mono', monospace;
  cursor: pointer;
  transition: all .15s;
}
.kw-add-btn:hover { background: var(--green); color: #000; }

/* ── NOTIFY CONFIG ── */
.notify-config { display: flex; flex-direction: column; gap: 8px; }

.nc-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 10px;
  background: var(--panel);
  border: 1px solid var(--border2);
  border-radius: 6px;
  font-size: 12px;
}

.nc-left { display: flex; align-items: center; gap: 8px; }
.nc-icon { font-size: 16px; }
.nc-label { color: var(--text); }
.nc-sub { font-size: 10px; color: var(--muted); }

.nc-status { font-family: 'IBM Plex Mono', monospace; font-size: 11px; }
.nc-status.on  { color: var(--green); }
.nc-status.off { color: var(--muted); }

.test-notify-btn {
  width:100%;
  padding:8px;
  border:1px solid var(--green-d);
  border-radius:6px;
  background:var(--green-bg);
  color:var(--green);
  font-size:12px;
  cursor:pointer;
  font-family:'IBM Plex Mono',monospace;
  transition:all .15s;
}
.test-notify-btn:hover {
  background: var(--green);
  color: #000;
}

/* ── ACTIVITY LOG ── */
.log-list { display: flex; flex-direction: column; gap: 0; }

.log-item {
  display: flex;
  gap: 10px;
  padding: 8px 0;
  border-bottom: 1px solid var(--border);
  font-size: 12px;
  align-items: flex-start;
}
.log-item:last-child { border-bottom: none; }

.log-time { font-family: 'IBM Plex Mono', monospace; color: var(--dim); flex-shrink: 0; width: 44px; font-size: 11px; margin-top: 1px; }
.log-dot  { width: 6px; height: 6px; border-radius: 50%; margin-top: 5px; flex-shrink: 0; }
.log-dot.g { background: var(--green); }
.log-dot.a { background: var(--amber); }
.log-dot.b { background: var(--blue); }
.log-msg  { color: var(--muted); line-height: 1.5; }
.log-msg strong { color: var(--text); }

/* ── SCANNING ANIMATION ── */
.scan-line-wrap {
  padding: .75rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
  font-family: 'IBM Plex Mono', monospace;
  color: var(--muted);
  border-bottom: 1px solid var(--border);
  background: var(--surface);
}

.scan-track {
  flex: 1;
  height: 3px;
  background: var(--border2);
  border-radius: 2px;
  overflow: hidden;
}

.scan-bar {
  height: 100%;
  background: linear-gradient(90deg, transparent, var(--green), transparent);
  width: 40%;
  border-radius: 2px;
  animation: scan 2.5s ease-in-out infinite;
}

@keyframes scan {
  0%   { transform: translateX(-100%); }
  100% { transform: translateX(350%); }
}

.scan-src { color: var(--green); }

/* ── TOAST ── */
.toasts {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  z-index: 9998;
  display: flex;
  flex-direction: column;
  gap: 8px;
  pointer-events: none;
}

.toast {
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 13px;
  font-family: 'IBM Plex Mono', monospace;
  display: flex;
  align-items: center;
  gap: 10px;
  max-width: 340px;
  pointer-events: auto;
  animation: toastIn .3s ease;
  border: 1px solid;
}

@keyframes toastIn {
  from { transform: translateX(100%); opacity: 0; }
  to   { transform: translateX(0); opacity: 1; }
}

.toast.new-lead {
  background: #0d1a12;
  border-color: var(--green-d);
  color: var(--text);
}
.toast-icon { font-size: 18px; flex-shrink: 0; }
.toast-body { flex: 1; }
.toast-title { font-weight: 600; color: var(--green); margin-bottom: 2px; font-size: 12px; }
.toast-desc  { font-size: 11px; color: var(--muted); line-height: 1.4; font-weight: 400; }

/* ── EMPTY STATE ── */
.empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--dim);
  gap: .75rem;
  padding: 3rem;
  text-align: center;
}
.empty-icon { font-size: 2.5rem; opacity: .4; }
.empty-msg  { font-size: 13px; line-height: 1.6; }

/* ── SCROLLBARS ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }

/* ── RESPONSIVE ── */
@media (max-width: 900px) {
  .shell { grid-template-columns: 1fr; }
  .sidebar, .rpanel { display: none; }
  .statbar { grid-template-columns: repeat(2, 1fr); }
}
</style>
</head>
<body>

<!-- TOP BAR -->
<div class="topbar">
  <div class="logo">
    <div class="logo-dot"></div>
    <span class="logo-name">租客雷達</span>
    <span class="logo-tag">/ TENANT RADAR</span>
  </div>
  <div class="topbar-right">
    <div class="clock" id="clock">--:--:--</div>
    <div class="status-pill on" id="radar-status">
      <div class="pill-dot"></div>
      <span id="radar-label">掃描中</span>
    </div>
    <button onclick="toggleRadar()" class="toggle-radar-btn" id="toggle-btn">暫停</button>
  </div>
</div>

<div class="shell">

  <!-- STAT BAR -->
  <div class="statbar">
    <div class="stat">
      <div class="stat-label">今日偵測到</div>
      <div class="stat-value g" id="stat-today">0</div>
      <div class="stat-delta up" id="stat-today-d">↑ 持續增加中</div>
    </div>
    <div class="stat">
      <div class="stat-label">高度匹配</div>
      <div class="stat-value g" id="stat-hot">0</div>
      <div class="stat-delta">符合率 ≥ 80%</div>
    </div>
    <div class="stat">
      <div class="stat-label">已推播通知</div>
      <div class="stat-value b" id="stat-notified">0</div>
      <div class="stat-delta">LINE / 簡訊 / Email</div>
    </div>
    <div class="stat">
      <div class="stat-label">成功聯繫</div>
      <div class="stat-value a" id="stat-converted">0</div>
      <div class="stat-delta">本月</div>
    </div>
  </div>

  <!-- LEFT SIDEBAR -->
  <aside class="sidebar">
    <div class="sidebar-section">
      <div class="sidebar-heading">監控頻道</div>

      <div class="channel active" onclick="filterSrc('all', event)">
        <div class="ch-icon ch-fb">📡</div>
        <div class="ch-info">
          <div class="ch-name">全部來源</div>
          <div class="ch-sub">5 個頻道</div>
        </div>
        <div class="ch-badge" id="badge-all">0</div>
      </div>

      <div class="channel" onclick="filterSrc('fb', event)">
        <div class="ch-icon ch-fb">📘</div>
        <div class="ch-info">
          <div class="ch-name">Facebook 社團</div>
          <div class="ch-sub">租屋/找屋/台北租屋...</div>
        </div>
        <div class="ch-badge" id="badge-fb">0</div>
      </div>

      <div class="channel" onclick="filterSrc('ptt', event)">
        <div class="ch-icon ch-ptt">💬</div>
        <div class="ch-info">
          <div class="ch-name">PTT 租屋版</div>
          <div class="ch-sub">rent 版 / 北部租屋</div>
        </div>
        <div class="ch-badge off" id="badge-ptt">0</div>
      </div>

      <div class="channel" onclick="filterSrc('dcard', event)">
        <div class="ch-icon ch-dcard">🃏</div>
        <div class="ch-info">
          <div class="ch-name">Dcard</div>
          <div class="ch-sub">租屋日記</div>
        </div>
        <div class="ch-badge off" id="badge-dcard">0</div>
      </div>

      <div class="channel" onclick="filterSrc('591', event)">
        <div class="ch-icon ch-591">🏠</div>
        <div class="ch-info">
          <div class="ch-name">591 找房留言</div>
          <div class="ch-sub">求租板塊</div>
        </div>
        <div class="ch-badge off" id="badge-591">0</div>
      </div>

      <div class="channel" onclick="filterSrc('line', event)">
        <div class="ch-icon ch-line">💚</div>
        <div class="ch-info">
          <div class="ch-name">LINE 社群</div>
          <div class="ch-sub">需授權加入社群</div>
        </div>
        <div class="ch-badge off" id="badge-line">0</div>
      </div>
    </div>

    <div class="sidebar-section">
      <div class="sidebar-heading">自動過濾</div>
      <div class="toggle-row">
        <span>僅高匹配（≥80%）</span>
        <label class="toggle">
          <input type="checkbox" id="toggle-hot" onchange="applyFilter()">
          <div class="toggle-track"></div>
          <div class="toggle-thumb"></div>
        </label>
      </div>
      <div class="toggle-row">
        <span>符合預算範圍</span>
        <label class="toggle">
          <input type="checkbox" checked onchange="applyFilter()">
          <div class="toggle-track"></div>
          <div class="toggle-thumb"></div>
        </label>
      </div>
      <div class="toggle-row">
        <span>排除已聯繫</span>
        <label class="toggle">
          <input type="checkbox" checked onchange="applyFilter()">
          <div class="toggle-track"></div>
          <div class="toggle-thumb"></div>
        </label>
      </div>
    </div>

    <div class="sidebar-section">
      <div class="sidebar-heading">我的物件</div>
      <div class="my-properties-container">
        <div class="property-item">
          <div class="property-status renting">● 待租中</div>
          <div>信義區精品2房公寓</div>
          <div class="property-meta">$38,000 / 月</div>
        </div>
        <div class="property-item">
          <div class="property-status soon">◐ 即將空出</div>
          <div>南港展覽館旁套房</div>
          <div class="property-meta">$28,000 / 月</div>
        </div>
      </div>
    </div>
  </aside>

  <!-- MAIN FEED -->
  <main class="feed">
    <!-- SCANNING BAR -->
    <div class="scan-line-wrap">
      <span>掃描中</span>
      <span class="scan-src" id="scan-src">Facebook · 台北租屋生活圈</span>
      <div class="scan-track"><div class="scan-bar"></div></div>
      <span id="scan-count">0 筆</span>
    </div>

    <!-- FEED HEADER -->
    <div class="feed-header">
      <div class="feed-title">偵測到 <strong id="feed-count">0</strong> 筆租屋需求</div>
      <div class="feed-controls">
        <button class="ctrl-btn active" id="btn-all" onclick="setView('all',this)">全部</button>
        <button class="ctrl-btn" id="btn-hot" onclick="setView('hot',this)">🔥 高匹配</button>
        <button class="ctrl-btn" id="btn-new" onclick="setView('new',this)">🆕 最新</button>
      </div>
    </div>

    <!-- LEAD LIST -->
    <div class="lead-list" id="lead-list">
      <div class="empty">
        <div class="empty-icon">📡</div>
        <div class="empty-msg">雷達啟動中，正在掃描各平台…<br>通常 10–30 秒後開始出現租屋需求</div>
      </div>
    </div>
  </main>

  <!-- RIGHT PANEL -->
  <aside class="rpanel">

    <!-- KEYWORDS -->
    <div class="rp-section">
      <div class="rp-title">搜尋關鍵字</div>
      <div class="kw-list" id="kw-list"></div>
      <div class="add-kw-row">
        <input class="kw-input" type="text" id="kw-input" placeholder="新增關鍵字…" onkeydown="if(event.key==='Enter')addKeyword()">
        <button class="kw-add-btn" onclick="addKeyword()">＋</button>
      </div>
    </div>

    <!-- NOTIFY CHANNELS -->
    <div class="rp-section">
      <div class="rp-title">推播設定</div>
      <div class="notify-config">
        <div class="nc-row">
          <div class="nc-left">
            <span class="nc-icon">📱</span>
            <div>
              <div class="nc-label">LINE 通知</div>
              <div class="nc-sub">即時推播到您的 LINE</div>
            </div>
          </div>
          <div>
            <div class="nc-status on">已啟用</div>
          </div>
        </div>
        <div class="nc-row">
          <div class="nc-left">
            <span class="nc-icon">💬</span>
            <div>
              <div class="nc-label">簡訊通知</div>
              <div class="nc-sub">每則 $2，高匹配才發送</div>
            </div>
          </div>
          <div>
            <div class="nc-status on">已啟用</div>
          </div>
        </div>
        <div class="nc-row">
          <div class="nc-left">
            <span class="nc-icon">📧</span>
            <div>
              <div class="nc-label">Email 匯總</div>
              <div class="nc-sub">每天早上 8:00 發送</div>
            </div>
          </div>
          <div>
            <div class="nc-status off">未設定</div>
          </div>
        </div>
        <div class="nc-row">
          <div class="nc-left">
            <span class="nc-icon">🔔</span>
            <div>
              <div class="nc-label">瀏覽器通知</div>
              <div class="nc-sub">需允許通知權限</div>
            </div>
          </div>
          <div>
            <div class="nc-status on">已啟用</div>
          </div>
        </div>
        <button onclick="requestNotify()" class="test-notify-btn">測試推播通知</button>
      </div>
    </div>

    <!-- ACTIVITY LOG -->
    <div class="rp-section" style="flex:1">
      <div class="rp-title">系統紀錄</div>
      <div class="log-list" id="log-list"></div>
    </div>

  </aside>
</div>

<!-- TOAST CONTAINER -->
<div class="toasts" id="toasts"></div>

<script>
// ── STATE ──
let isRunning = true;
let allLeads  = [];
let viewMode  = 'all';
let filterSrc_ = 'all';
let todayCount = 0, hotCount = 0, notifiedCount = 0, convertedCount = 3;
let scanInterval, toastInterval;

// ── KEYWORDS ──
let keywords = [
  { text: '找房 台北', cnt: 12, tier: 'g' },
  { text: '租屋 信義區', cnt: 8, tier: 'g' },
  { text: '找租 大安', cnt: 5, tier: 'a' },
  { text: '求租 台北', cnt: 19, tier: 'g' },
  { text: '想租 套房', cnt: 3, tier: 'a' },
];

// ── MOCK LEAD GENERATOR ──
const SOURCES = [
  { id: 'fb', name: 'Facebook 社團', icon: '📘', class: 'ch-fb' },
  { id: 'ptt', name: 'PTT 租屋版',  icon: '💬', class: 'ch-ptt' },
  { id: 'dcard', name: 'Dcard',     icon: '🃏', class: 'ch-dcard' },
];

const SCAN_SRCS = [
  'Facebook · 台北租屋生活圈',
  'Facebook · 信義大安租屋情報',
  'PTT · rent 版',
  'PTT · 北部租屋',
  'Dcard · 租屋日記',
  'Facebook · 北台灣租屋找屋',
];

const LEAD_TEMPLATES = [
  { area:'信義區', budget:'30,000–45,000', type:'2房', extra:'含家具、可養貓', score:96 },
  { area:'大安區', budget:'25,000–35,000', type:'1房', extra:'近捷運、長期租約', score:88 },
  { area:'內湖區', budget:'18,000–28,000', type:'套房', extra:'上班族、安靜環境', score:72 },
  { area:'中山區', budget:'20,000–30,000', type:'1或2房', extra:'女性、整潔', score:65 },
  { area:'南港區', budget:'25,000–32,000', type:'套房', extra:'近展覽館、可短租', score:91 },
  { area:'松山區', budget:'22,000–35,000', type:'1房', extra:'近捷運、含車位', stroke:55, score:55 },
  { area:'台北市', budget:'40,000–60,000', type:'3房', extra:'全家入住、停車位', score:48 },
];

const NAMES = ['小陳','阿明','Jenny','王小姐','林先生','阿偉','Emma','小雅','James','Amy'];
const TIMES = ['剛剛','1 分鐘前','3 分鐘前','5 分鐘前','8 分鐘前','12 分鐘前'];

let leadId = 0;

function makeLead() {
  const tpl = LEAD_TEMPLATES[Math.floor(Math.random() * LEAD_TEMPLATES.length)];
  const src = SOURCES[Math.floor(Math.random() * SOURCES.length)];
  const name = NAMES[Math.floor(Math.random() * NAMES.length)];
  return {
    id: ++leadId,
    src: src.id,
    srcName: src.name,
    srcIcon: src.icon,
    srcClass: src.class,
    name,
    area: tpl.area,
    budget: tpl.budget,
    type: tpl.type,
    extra: tpl.extra,
    score: tpl.score + Math.floor(Math.random() * 6 - 3),
    time: TIMES[0],
    isNew: true,
    notified: false,
  };
}

// ── MY PROPERTIES (for matching) ──
const MY_PROPS = [
  { area: '信義區', price: 38000, type: '2房', tags: ['含家具', '近捷運', '可養寵物'] },
  { area: '南港區', price: 28000, type: '套房', tags: ['近捷運'] },
];

function getMatchProp(lead) {
  return MY_PROPS.find(p => p.area.includes(lead.area) || lead.area.includes(p.area.replace('區','')));
}

// ── RENDER ──
function renderLeads() {
  const list = document.getElementById('lead-list');
  let filtered = [...allLeads];

  // 根據自動過濾的開關狀態來過濾
  const onlyHot = document.getElementById('toggle-hot').checked;
  if (onlyHot) filtered = filtered.filter(l => l.score >= 80);

  if (viewMode === 'hot') filtered = filtered.filter(l => l.score >= 80);
  if (viewMode === 'new') filtered = filtered.filter(l => l.isNew);
  if (filterSrc_ !== 'all') filtered = filtered.filter(l => l.src === filterSrc_);

  if (filtered.length === 0) {
    list.innerHTML = `<div class="empty"><div class="empty-icon">🔍</div><div class="empty-msg">目前沒有符合條件的租屋需求<br>雷達持續掃描中…</div></div>`;
    return;
  }

  list.innerHTML = filtered.map(l => {
    const scoreClass = l.score >= 80 ? 'hi' : l.score >= 60 ? 'mid' : 'lo';
    const hot = l.score >= 80;
    const matchProp = getMatchProp(l);
    const r = 11; const circ = 2 * Math.PI * r;
    const dash = (l.score / 100) * circ;
    const scoreColor = l.score >= 80 ? 'var(--green)' : l.score >= 60 ? 'var(--amber)' : 'var(--dim)';

    return `
    <div class="lead-card ${hot ? 'hot' : ''}" id="lc-${l.id}">
      <div class="lead-top">
        <div class="ch-icon ${l.srcClass}">${l.srcIcon}</div>
        <div class="lead-body">
          <div class="lead-meta-row">
            <span class="lead-src-name">${l.srcName}</span>
            <span style="color:var(--dim)">·</span>
            <span class="lead-time">${l.time}</span>
            ${l.isNew ? '<span class="new-tag">NEW</span>' : ''}
            <div class="score-bar">
              <span class="score-num ${scoreClass}">${l.score}%</span>
              <div class="score-ring">
                <svg width="28" height="28" viewBox="0 0 28 28">
                  <circle cx="14" cy="14" r="${r}" fill="none" stroke="var(--border2)" stroke-width="2.5"/>
                  <circle cx="14" cy="14" r="${r}" fill="none" stroke="${scoreColor}" stroke-width="2.5"
                    stroke-dasharray="${dash.toFixed(1)} ${circ.toFixed(1)}" stroke-linecap="round"/>
                </svg>
              </div>
            </div>
          </div>
          <div class="lead-text">
            <strong>${l.name}</strong> 在 ${l.srcName} 發文找租：
            <span class="hl">${l.area}</span>、<span class="hl">${l.type}</span>，
            預算 <span class="hl">$${l.budget}/月</span>。${l.extra}。
          </div>
          <div class="lead-chips">
            <span class="lchip">📍 ${l.area}</span>
            <span class="lchip">🛏 ${l.type}</span>
            <span class="lchip">💰 $${l.budget}</span>
            ${matchProp ? `<span class="lchip match">✓ 符合您的物件</span>` : ''}
          </div>
        </div>
      </div>
      <div class="lead-bottom">
        <button class="notify-btn" onclick="notifyLead(${l.id}, event)">
          ${l.notified ? '✓ 已推播' : '📲 立即推播通知給我'}
        </button>
        <button class="skip-btn" onclick="skipLead(${l.id}, event)">略過</button>
      </div>
    </div>`;
  }).join('');
}

function notifyLead(id, e) {
  e.stopPropagation();
  const lead = allLeads.find(l => l.id === id);
  if (!lead || lead.notified) return;
  lead.notified = true;
  notifiedCount++;
  document.getElementById('stat-notified').textContent = notifiedCount;
  showToast(lead);
  addLog('g', `推播：<strong>${lead.name}</strong> 的租屋需求（${lead.area}、${lead.type}）`);
  renderLeads();
}

function skipLead(id, e) {
  e.stopPropagation();
  allLeads = allLeads.filter(l => l.id !== id);
  updateBadges();
  renderLeads();
}

// ── SOURCE FILTER ──
function filterSrc(src, e) {
  filterSrc_ = src;
  document.querySelectorAll('.channel').forEach((el) => {
    el.classList.remove('active');
  });
  e.currentTarget.classList.add('active');
  renderLeads();
}

// ── VIEW MODE ──
function setView(mode, btn) {
  viewMode = mode;
  document.querySelectorAll('.ctrl-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderLeads();
}

function applyFilter() { renderLeads(); }

// ── BADGES ──
function updateBadges() {
  const counts = { all: allLeads.length, fb: 0, ptt: 0, dcard: 0, '591': 0, line: 0 };
  allLeads.forEach(l => { if (counts[l.src] !== undefined) counts[l.src]++; });
  Object.entries(counts).forEach(([src, n]) => {
    const el = document.getElementById('badge-' + src);
    if (el) el.textContent = n;
  });
  document.getElementById('feed-count').textContent = allLeads.length;
  document.getElementById('scan-count').textContent = allLeads.length + ' 筆';
}

// ── STATS ──
function updateStats() {
  hotCount = allLeads.filter(l => l.score >= 80).length;
  document.getElementById('stat-today').textContent = todayCount;
  document.getElementById('stat-hot').textContent   = hotCount;
}

// ── TOAST ──
function showToast(lead) {
  const container = document.getElementById('toasts');
  const t = document.createElement('div');
  t.className = 'toast new-lead';
  t.innerHTML = `
    <div class="toast-icon">🔔</div>
    <div class="toast-body">
      <div class="toast-title">新租客需求推播</div>
      <div class="toast-desc">${lead.name} · ${lead.area} · ${lead.type}<br>預算 $${lead.budget}／月 · 匹配度 ${lead.score}%</div>
    </div>`;
  container.appendChild(t);
  setTimeout(() => t.remove(), 6000);
}

function autoToast(lead) {
  const container = document.getElementById('toasts');
  const t = document.createElement('div');
  t.className = 'toast new-lead';
  t.innerHTML = `
    <div class="toast-icon">📡</div>
    <div class="toast-body">
      <div class="toast-title">偵測到新租屋需求</div>
      <div class="toast-desc">${lead.srcName} · ${lead.area} · ${lead.type} · 匹配 ${lead.score}%</div>
    </div>`;
  container.appendChild(t);
  setTimeout(() => t.remove(), 5000);
}

// ── LOG ──
const logItems = [];
function addLog(color, msg) {
  const now = new Date();
  const t = now.getHours().toString().padStart(2,'0') + ':' + now.getMinutes().toString().padStart(2,'0');
  logItems.unshift({ color, msg, t });
  if (logItems.length > 12) logItems.pop();
  renderLog();
}

function renderLog() {
  document.getElementById('log-list').innerHTML = logItems.map(l =>
    `<div class="log-item">
      <span class="log-time">${l.t}</span>
      <div class="log-dot ${l.color}"></div>
      <span class="log-msg">${l.msg}</span>
    </div>`
  ).join('');
}

// ── KEYWORDS ──
function renderKeywords() {
  document.getElementById('kw-list').innerHTML = keywords.map((k, i) =>
    `<div class="kw-item">
      <div class="kw-dot ${k.tier}"></div>
      <span class="kw-text">${k.text}</span>
      <span class="kw-cnt">${k.cnt} 筆</span>
      <button class="kw-rm" onclick="removeKeyword(${i})">×</button>
    </div>`
  ).join('');
}

function addKeyword() {
  const inp = document.getElementById('kw-input');
  const val = inp.value.trim();
  if (!val) return;
  keywords.push({ text: val, cnt: 0, tier: 'a' });
  inp.value = '';
  renderKeywords();
  addLog('b', `新增關鍵字：<strong>${val}</strong>`);
}

function removeKeyword(i) {
  keywords.splice(i, 1);
  renderKeywords();
}

// ── RADAR TOGGLE ──
function toggleRadar() {
  isRunning = !isRunning;
  const pill  = document.getElementById('radar-status');
  const label = document.getElementById('radar-label');
  const btn   = document.getElementById('toggle-btn');
  if (isRunning) {
    pill.className = 'status-pill on';
    label.textContent = '掃描中';
    btn.textContent = '暫停';
    addLog('g', '雷達已重新啟動');
  } else {
    pill.className = 'status-pill off';
    label.textContent = '已暫停';
    btn.textContent = '啟動';
    addLog('a', '雷達已暫停');
  }
}

// ── BROWSER NOTIFY ──
function requestNotify() {
  if ('Notification' in window) {
    Notification.requestPermission().then(p => {
      if (p === 'granted') {
        new Notification('租客雷達 🏠', { body: '推播通知已啟用！有新租屋需求時會即時通知您。' });
        addLog('g', '瀏覽器通知權限已取得');
      } else {
        addLog('a', '通知權限被拒絕，請在瀏覽器設定中允許');
      }
    });
  }
}

// ── CLOCK ──
function updateClock() {
  const now = new Date();
  document.getElementById('clock').textContent =
    now.toLocaleTimeString('zh-TW', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
}

// ── SCANNING SRC ROTATION ──
let scanIdx = 0;
setInterval(() => {
  if (!isRunning) return;
  document.getElementById('scan-src').textContent = SCAN_SRCS[scanIdx % SCAN_SRCS.length];
  scanIdx++;
}, 2800);

// ── SIMULATE INCOMING LEADS ──
function injectLead() {
  if (!isRunning) return;
  const lead = makeLead();
  allLeads.unshift(lead);
  if (allLeads.length > 40) allLeads.pop();
  todayCount++;
  updateBadges();
  updateStats();

  // auto-toast for high match
  if (lead.score >= 80) autoToast(lead);

  // age old leads
  allLeads.forEach((l, i) => {
    if (i > 0) {
      const mins = [1,3,5,8,12,20,35,60];
      const idx = Math.min(i, mins.length - 1);
      l.time = mins[idx] + ' 分鐘前';
      l.isNew = false;
    }
  });

  addLog(lead.score >= 80 ? 'g' : 'b',
    `偵測到：<strong>${lead.name}</strong>｜${lead.srcName}｜${lead.area} ${lead.type}`);

  renderLeads();
}

// ── INITIALIZATION ──
function init() {
  setInterval(updateClock, 1000);
  updateClock();
  renderKeywords();
  document.getElementById('stat-converted').textContent = convertedCount;
  addLog('b', '租客雷達系統初始化成功...');
  
  // 每 4 秒自動灌入一筆新資料
  setInterval(injectLead, 4000);
}

window.onload = init;
</script>
</body>
</html>
