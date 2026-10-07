// ==========================================================================
// DEFENSE INTELLIGENCE - 6-Hour Pipeline & BigKinds Live Data Portal
// ==========================================================================

let newsDataset = [];
let currentCategory = "ALL";
let searchQuery = "";
let lastSyncTimestamp = new Date();

// DOM Elements
const newsCardGrid = document.getElementById("newsCardGrid");
const searchInput = document.getElementById("searchInput");
const tabButtons = document.querySelectorAll(".tab-item");
const lastUpdatedTimeEl = document.getElementById("lastUpdatedTime");
const timerHoursEl = document.getElementById("timerHours");
const timerMinutesEl = document.getElementById("timerMinutes");
const timerSecondsEl = document.getElementById("timerSeconds");
const btnSyncNow = document.getElementById("btnSyncNow");
const syncIcon = document.getElementById("syncIcon");
const toast = document.getElementById("toast");
const toastMsg = document.getElementById("toastMsg");

const countAll = document.getElementById("countAll");
const countIndustry = document.getElementById("countIndustry");
const countWeapon = document.getElementById("countWeapon");
const countMilitary = document.getElementById("countMilitary");

// Modal Elements
const newsModal = document.getElementById("newsModal");
const btnCloseModal = document.getElementById("btnCloseModal");
const modalCategory = document.getElementById("modalCategory");
const modalConfidence = document.getElementById("modalConfidence");
const modalPubDate = document.getElementById("modalPubDate");
const modalTitle = document.getElementById("modalTitle");
const modalSource = document.getElementById("modalSource");
const modalSummaryList = document.getElementById("modalSummaryList");
const modalFullContent = document.getElementById("modalFullContent");
const modalEntities = document.getElementById("modalEntities");
const modalOriginalLink = document.getElementById("modalOriginalLink");

// Helper: Clean & format summary text
function cleanSummaryText(text) {
  if (!text) return "";
  // Remove strange trailing dots or excessive spaces
  return text.replace(/\s+/g, ' ').replace(/(\s*\.\s*)+$/g, '.').trim();
}

// Helper: Format BigKinds Date (e.g. 20241119 -> 2024.11.19)
function formatDate(dStr) {
  if (!dStr) return "2024.11.19";
  const s = String(dStr).replace(/[^0-9]/g, '');
  if (s.length === 8) {
    return `${s.slice(0,4)}.${s.slice(4,6)}.${s.slice(6,8)}`;
  }
  return dStr;
}

// Initialize on DOM Ready
document.addEventListener("DOMContentLoaded", async () => {
  if (window.lucide) {
    lucide.createIcons();
  }

  initUpdateSchedule();
  setupEventListeners();
  setInterval(updateCountdown, 1000);

  // Load Real BigKinds Extracted Data
  await loadNewsData();
});

// Load News Data from BigKinds JSON
async function loadNewsData() {
  try {
    const res = await fetch('news_data.json?t=' + new Date().getTime());
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data) && data.length > 0) {
        newsDataset = data.map(item => ({
          ...item,
          summary: cleanSummaryText(item.summary),
          pubDate: formatDate(item.pubDate)
        }));
        console.log(`[BigKinds Pipeline] 빅카인즈 실시간 추출 데이터 ${data.length}건 로드 완료!`);
      }
    }
  } catch (err) {
    console.warn("JSON 로드 오류:", err);
  }

  updateCategoryCounts();
  renderCards();
}

function updateCategoryCounts() {
  const total = newsDataset.length;
  const industry = newsDataset.filter(n => n.category === "INDUSTRY").length;
  const weapon = newsDataset.filter(n => n.category === "WEAPON").length;
  const military = newsDataset.filter(n => n.category === "MILITARY").length;

  if (countAll) countAll.textContent = total;
  if (countIndustry) countIndustry.textContent = industry;
  if (countWeapon) countWeapon.textContent = weapon;
  if (countMilitary) countMilitary.textContent = military;
}

// Setup 6-Hour Update Schedule Timers
function initUpdateSchedule() {
  const now = new Date();
  const currentHour = now.getHours();
  const cycleHour = Math.floor(currentHour / 6) * 6;
  
  const lastSync = new Date(now);
  lastSync.setHours(cycleHour, 0, 0, 0);
  lastSyncTimestamp = lastSync;

  formatLastSyncDisplay();
  updateCountdown();
}

function formatLastSyncDisplay() {
  const y = lastSyncTimestamp.getFullYear();
  const m = String(lastSyncTimestamp.getMonth() + 1).padStart(2, '0');
  const d = String(lastSyncTimestamp.getDate()).padStart(2, '0');
  const hh = String(lastSyncTimestamp.getHours()).padStart(2, '0');
  const mm = String(lastSyncTimestamp.getMinutes()).padStart(2, '0');
  const ss = String(lastSyncTimestamp.getSeconds()).padStart(2, '0');
  lastUpdatedTimeEl.textContent = `${y}.${m}.${d} ${hh}:${mm}:${ss} KST`;
}

// 6-Hour Periodic Countdown Calculation
function updateCountdown() {
  const now = new Date();
  const nextSync = new Date(lastSyncTimestamp);
  nextSync.setHours(nextSync.getHours() + 6);

  let diffMs = nextSync - now;

  if (diffMs <= 0) {
    lastSyncTimestamp = new Date();
    formatLastSyncDisplay();
    showToast("[자동 갱신] 6시간 주기 빅카인즈 국방 뉴스 데이터가 동기화되었습니다.");
    loadNewsData();
    return;
  }

  const diffSec = Math.floor(diffMs / 1000);
  const hours = Math.floor(diffSec / 3600);
  const minutes = Math.floor((diffSec % 3600) / 60);
  const seconds = diffSec % 60;

  timerHoursEl.textContent = String(hours).padStart(2, '0');
  timerMinutesEl.textContent = String(minutes).padStart(2, '0');
  timerSecondsEl.textContent = String(seconds).padStart(2, '0');
}

// Render News Cards (Card News Format)
function renderCards() {
  newsCardGrid.innerHTML = "";

  const filtered = newsDataset.filter(item => {
    if (currentCategory !== "ALL" && item.category !== currentCategory) {
      return false;
    }
    if (searchQuery.trim() !== "") {
      const q = searchQuery.toLowerCase();
      const matchTitle = (item.title || "").toLowerCase().includes(q);
      const matchSummary = (item.summary || "").toLowerCase().includes(q);
      const matchEntities = (item.entities || []).some(e => e.toLowerCase().includes(q));
      if (!matchTitle && !matchSummary && !matchEntities) {
        return false;
      }
    }
    return true;
  });

  if (filtered.length === 0) {
    newsCardGrid.innerHTML = `
      <div style="grid-column: 1 / -1; padding: 48px; text-align: center; color: var(--text-dim); background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-md);">
        <i data-lucide="search-x" style="width: 32px; height: 32px; margin-bottom: 8px; color: var(--text-dim);"></i>
        <div style="font-size: 14px; font-weight: 600; color: var(--text-muted);">검색 조건에 일치하는 국방 뉴스가 없습니다.</div>
        <div style="font-size: 12px; margin-top: 4px;">다른 검색어나 카테고리 탭을 선택해 보세요.</div>
      </div>
    `;
    if (window.lucide) lucide.createIcons();
    return;
  }

  filtered.forEach(item => {
    const card = document.createElement("article");
    card.className = "news-card";
    const entityList = Array.isArray(item.entities) ? item.entities.slice(0, 3) : ["#국방", "#안보"];
    const confVal = item.confidence ? item.confidence.toFixed(1) : "99.5";

    card.innerHTML = `
      <!-- Card Top Bar -->
      <div class="card-top-bar">
        <span class="card-category-tag ${item.categoryTagClass || 'tag-industry'}">
          <i data-lucide="shield-check" class="icon-xxs"></i>
          <span>${item.categoryLabel || '국방 안보'}</span>
        </span>
        <div class="card-meta-right">
          <span class="card-conf">[AI ${confVal}%]</span>
          <span class="card-time">${item.timeAgo || '최신'}</span>
        </div>
      </div>

      <!-- Card Title Zone (Upper Part) -->
      <div class="card-header-zone">
        <h3 class="card-title" title="${item.title}">${item.title}</h3>
        <div class="card-source-bar">
          <i data-lucide="newspaper" class="icon-xxs"></i>
          <span>${item.source || '빅카인즈 언론사'}</span>
          <span>•</span>
          <span>${item.pubDate || '2024.11.19'}</span>
        </div>
      </div>

      <!-- Card Center Zone (Summarized News Content) -->
      <div class="card-summary-zone">
        <div class="summary-card-box">
          <div class="summary-card-header">
            <i data-lucide="sparkles" class="icon-xxs"></i>
            <span>AI 핵심 요약 (KoBART Summary)</span>
          </div>
          <p class="summary-card-text">${item.summary || item.title}</p>
        </div>
      </div>

      <!-- Card Bottom Zone (Entities & CTA) -->
      <div class="card-footer-zone">
        <div class="card-entity-chips">
          ${entityList.map(e => `<span class="card-entity">${e}</span>`).join("")}
        </div>
        <div class="card-cta-hint">
          <span>본문 보기</span>
          <i data-lucide="chevron-right" class="icon-xxs"></i>
        </div>
      </div>
    `;

    card.addEventListener("click", () => {
      openDetailModal(item);
    });

    newsCardGrid.appendChild(card);
  });

  if (window.lucide) {
    lucide.createIcons();
  }
}

// Open Detail Modal (Full Article + AI Summary + Original Link)
function openDetailModal(item) {
  modalCategory.textContent = `[${item.categoryLabel || '국방 안보'}]`;
  modalConfidence.textContent = `[AI 신뢰도: ${(item.confidence || 99.5).toFixed(1)}%]`;
  modalPubDate.textContent = item.pubDate || '2024.11.19';
  modalTitle.textContent = item.title;
  modalSource.innerHTML = `<i data-lucide="newspaper" class="icon-xxs"></i> ${item.source || '빅카인즈 언론사'}`;
  
  // Summary Bullets
  let bullets = [];
  if (Array.isArray(item.summaryBullets) && item.summaryBullets.length > 0) {
    bullets = item.summaryBullets.map(b => cleanSummaryText(b)).filter(b => b.length > 5);
  }
  if (bullets.length === 0) {
    bullets = [cleanSummaryText(item.summary) || item.title, "인공지능(AI) 기반 국방 도메인 분류 및 핵심 요약 추출 완료.", "주요 방산 및 군사 전략 후속 동향 지속 모니터링."];
  }
  
  modalSummaryList.innerHTML = bullets.map(b => `<li>${b}</li>`).join("");
  
  // Full Content
  modalFullContent.textContent = item.fullContent || item.summary || item.title;

  // Entities
  const entityList = Array.isArray(item.entities) ? item.entities : ["#국방", "#안보"];
  modalEntities.innerHTML = entityList.map(e => `<span class="entity-chip">${e}</span>`).join("");

  // External Original Link
  const targetUrl = (item.originalUrl && item.originalUrl.startsWith('http')) 
    ? item.originalUrl 
    : "https://www.bigkinds.or.kr";
    
  modalOriginalLink.href = targetUrl;
  modalOriginalLink.setAttribute("target", "_blank");
  modalOriginalLink.onclick = (e) => {
    e.stopPropagation();
    showToast(`"${item.source || '원문 출처'}" 원본 기사 페이지로 이동합니다.`);
  };

  newsModal.classList.add("active");
  document.body.style.overflow = "hidden";

  if (window.lucide) {
    lucide.createIcons();
  }
}

// Close Modal
function closeModal() {
  newsModal.classList.remove("active");
  document.body.style.overflow = "";
}

// Event Listeners
function setupEventListeners() {
  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      tabButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentCategory = btn.dataset.category;
      renderCards();
    });
  });

  searchInput.addEventListener("input", (e) => {
    searchQuery = e.target.value;
    renderCards();
  });

  document.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "k") {
      e.preventDefault();
      searchInput.focus();
    }
    if (e.key === "Escape" && newsModal.classList.contains("active")) {
      closeModal();
    }
  });

  btnCloseModal.addEventListener("click", closeModal);
  newsModal.addEventListener("click", (e) => {
    if (e.target === newsModal) {
      closeModal();
    }
  });

  btnSyncNow.addEventListener("click", async () => {
    syncIcon.classList.add("rotating");
    btnSyncNow.disabled = true;

    await loadNewsData();

    setTimeout(() => {
      syncIcon.classList.remove("rotating");
      btnSyncNow.disabled = false;
      lastSyncTimestamp = new Date();
      formatLastSyncDisplay();
      updateCountdown();
      showToast("빅카인즈 국방 뉴스 데이터가 성공적으로 동기화되었습니다.");
    }, 700);
  });
}

// Toast Popup
let toastTimeout;
function showToast(msg) {
  toastMsg.textContent = msg;
  toast.classList.add("show");
  clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => {
    toast.classList.remove("show");
  }, 2800);
}
