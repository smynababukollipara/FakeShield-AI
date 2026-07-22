// ─────────────────────────────────────────────────────────────
// frontend/script.js  (Redesign — same functionality, new UI hooks)
// ─────────────────────────────────────────────────────────────

const API_URL      = '/predict';
const HISTORY_KEY  = 'fnd_history';   // localStorage key
const THEME_KEY     = 'fnd_theme';    // localStorage key for theme
const MAX_HISTORY  = 10;              // keep last 10 checks
let currentMode    = 'news';

// ── DOM elements ───────────────────────────────────────────────
const textInput     = document.getElementById('textInput');
const checkBtn      = document.getElementById('checkBtn');
const clearBtn      = document.getElementById('clearBtn');
const btnText       = document.getElementById('btnText');
const btnSpinner    = document.getElementById('btnSpinner');
const charCount     = document.getElementById('charCount');
const inputLabel    = document.getElementById('inputLabel');
const exampleBtns   = document.getElementById('exampleBtns');

const resultCard    = document.getElementById('resultCard');
const verdictBanner = document.getElementById('verdictBanner');
const verdictIcon   = document.getElementById('verdictIcon');
const verdictLabel  = document.getElementById('verdictLabel');
const realBar       = document.getElementById('realBar');
const fakeBar       = document.getElementById('fakeBar');
const realPct       = document.getElementById('realPct');
const fakePct       = document.getElementById('fakePct');
const explanation   = document.getElementById('explanation');
const modeBadge     = document.getElementById('modeBadge');

const errorCard     = document.getElementById('errorCard');
const errorMsg      = document.getElementById('errorMsg');

const historyPanel  = document.getElementById('historyPanel');
const historyList   = document.getElementById('historyList');
const clearHistory  = document.getElementById('clearHistory');
const historyEmpty  = document.getElementById('historyEmpty');
const historyCount  = document.getElementById('historyCount');

const statTotal     = document.getElementById('statTotal');
const statFakePct   = document.getElementById('statFakePct');
const statRealPct   = document.getElementById('statRealPct');

// ── New UI-only elements (navbar / theme) ───────────────────────
const themeToggle      = document.getElementById('themeToggle');
const themeToggleIcon  = document.getElementById('themeToggleIcon');
const navMobileToggle  = document.getElementById('navMobileToggle');
const navbarEl         = document.querySelector('.navbar');
const navLinks         = document.getElementById('navLinks');

// ── Example content per mode ───────────────────────────────────
const EXAMPLES = {
  news: {
    label: 'Paste your news article or headline below:',
    placeholder: "e.g. 'BREAKING: Scientists reveal that drinking lemon water cures all diseases — government doesn't want you to know this!'",
    items: [
      {
        label: '🔴 Fake headline',
        text: `SHOCKING: Government scientists have CONFIRMED that 5G towers are being used to control human behaviour. A whistleblower from inside the agency has leaked documents proving that world leaders have known about this since 2015 but refuse to act. Share this before it gets deleted!`
      },
      {
        label: '🟢 Real headline',
        text: `The Federal Reserve raised its benchmark interest rate by 25 basis points on Wednesday, the tenth increase since early last year, as policymakers continue efforts to bring inflation back to the 2 percent target. The decision was widely expected by financial markets.`
      },
      {
        label: '🟡 Political news',
        text: `Parliament approved the annual budget proposal after a three-day committee hearing, with 287 votes in favour and 201 against. The chancellor said the measures were necessary to reduce the deficit while protecting public services.`
      }
    ]
  },
  sms: {
    label: 'Paste your SMS or WhatsApp message below:',
    placeholder: "e.g. 'Congratulations! You have won £5,000. Click here to claim your prize before it expires!'",
    items: [
      {
        label: '🔴 Prize scam',
        text: `Congratulations! You've won a $500 Amazon gift card. Click here to claim within 24 hours or it will expire: http://amaz0n-prize.xyz`
      },
      {
        label: '🔴 Bank scam',
        text: `URGENT: Your bank account has been suspended due to suspicious activity. Verify now at http://secure-bank-login.net or lose access permanently.`
      },
      {
        label: '🟢 Real SMS',
        text: `Your Amazon order #405-1234567 has been shipped and will arrive by Thursday. Track your package at amazon.com/orders. No action needed.`
      }
    ]
  }
};

// ── Render example buttons ────────────────────────────────────
function renderExamples() {
  const items = EXAMPLES[currentMode].items;
  exampleBtns.innerHTML = items
    .map((item, i) => `<button class="example-btn" data-index="${i}">${item.label}</button>`)
    .join('');

  exampleBtns.querySelectorAll('.example-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = EXAMPLES[currentMode].items[Number(btn.dataset.index)];
      textInput.value = item.text;
      textInput.dispatchEvent(new Event('input'));
      hideAll();
    });
  });
}

// ── Mode toggle ───────────────────────────────────────────────
document.querySelectorAll('.mode-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    currentMode = btn.dataset.mode;
    document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const cfg = EXAMPLES[currentMode];
    inputLabel.textContent = cfg.label;
    textInput.placeholder  = cfg.placeholder;
    renderExamples();
    textInput.value = '';
    charCount.textContent = '0 characters';
    hideAll();
  });
});

renderExamples();

// ── Character counter ─────────────────────────────────────────
textInput.addEventListener('input', () => {
  const len = textInput.value.length;
  charCount.textContent = `${len.toLocaleString()} character${len !== 1 ? 's' : ''}`;
});

// ── Clear button ──────────────────────────────────────────────
clearBtn.addEventListener('click', () => {
  textInput.value = '';
  charCount.textContent = '0 characters';
  hideAll();
  textInput.focus();
});

// ── Check button + Ctrl+Enter ─────────────────────────────────
checkBtn.addEventListener('click', runCheck);
textInput.addEventListener('keydown', e => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') runCheck();
});

async function runCheck() {
  const text = textInput.value.trim();
  if (!text) { showError('Please paste some text before checking.'); return; }
  if (text.split(/\s+/).length < 5) {
    showError('Text is too short. Please paste at least a sentence or two.');
    return;
  }

  hideAll();

showLoading(async () => {

setLoading(true);

try {
    const response = await fetch(API_URL, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ text, mode: currentMode })
    });
    const data = await response.json();

    if (!response.ok || data.error) {
      showError(data.error || 'Something went wrong. Please try again.');
      return;
    }
    showResult(data, text);
    saveToHistory({ text, data, mode: currentMode });
    loadStats();

  } catch {
    showError('Could not reach the server. Make sure Flask is running (python app/main.py).');
  } finally {

    setLoading(false);

}

});
}

// ── Display result ────────────────────────────────────────────
function showResult(data, _text) {
  const isFake = data.label === 'FAKE';
  const modeLabel = currentMode === 'sms' ? 'SMS / WhatsApp' : 'News Article';

  verdictBanner.className = `verdict ${isFake ? 'fake' : 'real'}`;
  verdictIcon.textContent  = isFake ? '🔴' : '🟢';

  if (isFake) {
    verdictLabel.textContent = currentMode === 'sms'
      ? `SCAM MESSAGE — ${data.confidence}% confidence`
      : `FAKE NEWS — ${data.confidence}% confidence`;
  } else {
    verdictLabel.textContent = currentMode === 'sms'
      ? `LOOKS LEGIT — ${data.confidence}% confidence`
      : `REAL NEWS — ${data.confidence}% confidence`;
  }

  // Reset bars first so the width transition animates from 0 on every run
  realBar.style.width = '0%';
  fakeBar.style.width = '0%';
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      realBar.style.width = `${data.real_prob}%`;
      fakeBar.style.width = `${data.fake_prob}%`;
    });
  });

  realPct.textContent = `${currentMode === 'sms' ? 'Legit' : 'Real'}: ${data.real_prob}%`;
  fakePct.textContent = `${currentMode === 'sms' ? 'Scam' : 'Fake'}: ${data.fake_prob}%`;
  realPct.style.color = 'var(--real-green)';
  fakePct.style.color = 'var(--fake-red)';

  if (currentMode === 'sms') {
    explanation.textContent = isFake
      ? `This message shows patterns common in scam SMS/WhatsApp messages — things like prize claims, urgency pressure, suspicious links, or requests for personal/bank details. Do NOT click any links or reply with personal information.`
      : `This message shows patterns typical of legitimate notifications — clear sender identity, no urgency pressure, no suspicious links, and no requests for sensitive information.`;
  } else {
    explanation.textContent = isFake
      ? `The AI found patterns in this text that strongly match fake news — emotional language, unverified claims, urgency cues, or sensational phrasing. Always cross-check with trusted sources before sharing.`
      : `The AI found patterns consistent with factual, neutral reporting — measured language, verifiable claims, and a journalistic tone. When in doubt, verify with a trusted source.`;
  }

  modeBadge.textContent = `Analysed as: ${modeLabel}`;
  resultCard.classList.remove('hidden');
  resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ─────────────────────────────────────────────────────────────
// HISTORY
// localStorage stores an array of entry objects.
// Each entry: { id, text, label, confidence, real_prob, fake_prob, mode, timestamp }
// ─────────────────────────────────────────────────────────────

function loadHistory() {
  try {
    return JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]');
  } catch {
    return [];
  }
}

function saveHistory(entries) {
  localStorage.setItem(HISTORY_KEY, JSON.stringify(entries));
}

function saveToHistory({ text, data, mode }) {
  const entries = loadHistory();

  // Build a new entry
  const entry = {
    id:         Date.now(),               // unique ID = timestamp in ms
    text:       text.slice(0, 200),       // store first 200 chars only (saves space)
    label:      data.label,              // 'FAKE' or 'REAL'
    confidence: data.confidence,
    real_prob:  data.real_prob,
    fake_prob:  data.fake_prob,
    mode,                                // 'news' or 'sms'
    timestamp:  new Date().toISOString() // e.g. "2025-07-02T14:30:00.000Z"
  };

  // Prepend newest first, keep only MAX_HISTORY entries
  const updated = [entry, ...entries].slice(0, MAX_HISTORY);
  saveHistory(updated);
  renderHistory();
}

function formatTimestamp(iso) {
  // Converts "2025-07-02T14:30:00.000Z" → "2 Jul 2025, 2:30 pm"
  const d = new Date(iso);
  return d.toLocaleString('en-GB', {
    day: 'numeric', month: 'short', year: 'numeric',
    hour: 'numeric', minute: '2-digit', hour12: true
  });
}

function renderHistory() {
  const entries = loadHistory();

  // Update counter badge
  historyCount.textContent = entries.length;
  historyCount.classList.toggle('hidden', entries.length === 0);

  if (entries.length === 0) {
    historyEmpty.classList.remove('hidden');
    historyList.innerHTML = '';
    return;
  }

  historyEmpty.classList.add('hidden');

  historyList.innerHTML = entries.map(entry => {
    const isFake      = entry.label === 'FAKE';
    const modeIcon    = entry.mode === 'sms' ? '💬' : '📰';
    const modeText    = entry.mode === 'sms' ? 'SMS' : 'News';
    const verdictText = isFake
      ? (entry.mode === 'sms' ? 'SCAM' : 'FAKE')
      : (entry.mode === 'sms' ? 'LEGIT' : 'REAL');
    const preview = entry.text.length > 90
      ? entry.text.slice(0, 90) + '…'
      : entry.text;

    return `
      <div class="history-item ${isFake ? 'fake' : 'real'}"
           data-id="${entry.id}"
           title="Click to reload this text">
        <div class="history-item-top">
          <span class="history-verdict-badge ${isFake ? 'fake' : 'real'}">
            ${isFake ? '🔴' : '🟢'} ${verdictText} ${entry.confidence}%
          </span>
          <span class="history-meta">${modeIcon} ${modeText} · ${formatTimestamp(entry.timestamp)}</span>
        </div>
        <p class="history-preview">${escapeHtml(preview)}</p>
      </div>`;
  }).join('');

  // Click any history item → reload that text into the textarea
  historyList.querySelectorAll('.history-item').forEach(item => {
    item.addEventListener('click', () => {
      const id    = Number(item.dataset.id);
      const entry = loadHistory().find(e => e.id === id);
      if (!entry) return;

      // Switch to the right mode first
      if (entry.mode !== currentMode) {
        const modeBtn = document.querySelector(`.mode-btn[data-mode="${entry.mode}"]`);
        if (modeBtn) modeBtn.click();
      }
      textInput.value = entry.text;
      textInput.dispatchEvent(new Event('input'));
      textInput.scrollIntoView({ behavior: 'smooth' });
      textInput.focus();
      hideAll();
    });
  });
}

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// Clear history button
clearHistory.addEventListener('click', () => {
  if (loadHistory().length === 0) return;
  localStorage.removeItem(HISTORY_KEY);
  renderHistory();
});

// Render history on page load
renderHistory();

// ─────────────────────────────────────────────────────────────
// USAGE STATS
// Fetches server-side counters from GET /stats and displays them.
// Unlike history (per-browser, localStorage), these totals are
// shared across everyone who uses the app.
// ─────────────────────────────────────────────────────────────

async function loadStats() {
  try {
    const response = await fetch('/stats');
    if (!response.ok) return;
    const stats = await response.json();

    animateStatValue(statTotal, stats.total_checks, false);
    animateStatValue(statFakePct, stats.fake_pct, true);
    animateStatValue(statRealPct, stats.real_pct, true);
  } catch {
    // Stats are a nice-to-have — silently skip if the server isn't reachable yet.
  }
}

// Smoothly counts a stat element up to its target value.
// Purely cosmetic — does not change the final displayed value or data source.
function animateStatValue(el, targetValue, isPercent) {
  const target = Number(targetValue) || 0;
  const start = 0;
  const duration = 700;
  const startTime = performance.now();

  function frame(now) {
    const progress = Math.min((now - startTime) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.round(start + (target - start) * eased);
    el.textContent = isPercent ? `${current}%` : current.toLocaleString();
    if (progress < 1) requestAnimationFrame(frame);
    else el.textContent = isPercent ? `${target}%` : target.toLocaleString();
  }
  requestAnimationFrame(frame);
}

loadStats();

// ── Utilities ─────────────────────────────────────────────────
function showError(msg) {
  errorMsg.textContent = msg;
  errorCard.classList.remove('hidden');
  errorCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function setLoading(on) {
  checkBtn.disabled = on;
  btnText.textContent = on ? 'Analysing...' : '🔍 Check Now';
  btnSpinner.classList.toggle('hidden', !on);
}

function hideAll() {
  resultCard.classList.add('hidden');
  errorCard.classList.add('hidden');
}

// ─────────────────────────────────────────────────────────────
// UI-ONLY ADDITIONS (theme toggle + mobile nav)
// These are purely presentational and do not touch prediction,
// history, or stats logic/IDs above.
// ─────────────────────────────────────────────────────────────

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  if (themeToggleIcon) themeToggleIcon.textContent = theme === 'light' ? '☀️' : '🌙';
}

function initTheme() {
  const saved = localStorage.getItem(THEME_KEY);
  const prefersLight = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
  const theme = saved || (prefersLight ? 'light' : 'dark');
  applyTheme(theme);
}

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
    const next = current === 'light' ? 'dark' : 'light';
    applyTheme(next);
    localStorage.setItem(THEME_KEY, next);
  });
}

initTheme();

if (navMobileToggle && navbarEl) {
  navMobileToggle.addEventListener('click', () => {
    const isOpen = navbarEl.classList.toggle('nav-open');
    navMobileToggle.setAttribute('aria-expanded', String(isOpen));
  });
}

if (navLinks) {
  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      if (navbarEl) navbarEl.classList.remove('nav-open');
    });
  });
}
const tryFreeBtn = document.getElementById("tryFreeBtn");

if (tryFreeBtn) {
    tryFreeBtn.addEventListener("click", () => {
        document.getElementById("check").scrollIntoView({
            behavior: "smooth"
        });

        document.getElementById("textInput").focus();
    });
}

/* ============================================
   AI Loading Animation
============================================ */

const loadingOverlay = document.getElementById("loadingOverlay");
const loadingBar = document.getElementById("loadingBar");
const loadingPercent = document.getElementById("loadingPercent");
const loadingMessage = document.getElementById("loadingMessage");

const loadingSteps = [
    "Cleaning text...",
    "Extracting features...",
    "Running Machine Learning model...",
    "Calculating confidence...",
    "Preparing results..."
];

function showLoading(callback){

    loadingOverlay.classList.remove("hidden");

    let progress = 0;
    let step = 0;

    loadingBar.style.width = "0%";
    loadingPercent.innerText = "0%";

    const interval = setInterval(()=>{

        progress += 20;

        loadingBar.style.width = progress + "%";

        loadingPercent.innerText = progress + "%";

        if(step < loadingSteps.length){

            loadingMessage.innerText = loadingSteps[step];

            step++;

        }

        if(progress >= 100){

            clearInterval(interval);

            setTimeout(()=>{

                loadingOverlay.classList.add("hidden");

                if(callback) callback();

            },500);

        }

    },500);

}

const txtUpload=document.getElementById("txtUpload");

const fileName=document.getElementById("fileName");

txtUpload.addEventListener("change",(e)=>{

    const file=e.target.files[0];

    if(!file) return;

    fileName.textContent=file.name;

    const reader=new FileReader();

    reader.onload=function(event){

        document.getElementById("textInput").value=event.target.result;

        updateCharCount();

    };

    reader.readAsText(file);

});
function updateCharCount() {
    const textInput = document.getElementById("textInput");
    const charCount = document.getElementById("charCount");

    if (textInput && charCount) {
        charCount.textContent = textInput.value.length + " characters";
    }
}
document.getElementById("textInput").addEventListener("input", updateCharCount);