const passwordInput = document.getElementById("password");
const togglePasswordBtn = document.getElementById("togglePassword");
const checkBtn = document.getElementById("checkBtn");
const themeToggleBtn = document.getElementById("themeToggle");

const resultPlaceholder = document.getElementById("resultPlaceholder");
const resultContent = document.getElementById("resultContent");
const resultCard = document.getElementById("resultCard");
const closeResultPopup = document.getElementById("closeResultPopup");
const scoreBadge = document.getElementById("scoreBadge");
const leakStatus = document.getElementById("leakStatus");
const detailsList = document.getElementById("detailsList");
const tipsList = document.getElementById("tipsList");
const API_URL = "/api/check";
const THEME_STORAGE_KEY = "password-checker-theme";
const systemThemeMedia = window.matchMedia("(prefers-color-scheme: dark)");

initTheme();

if (passwordInput) {
  passwordInput.addEventListener("input", () => {
    checkBtn.disabled = !passwordInput.value;
  });
}

if (togglePasswordBtn && passwordInput) {
  togglePasswordBtn.addEventListener("click", () => {
    const isHidden = passwordInput.type === "password";
    passwordInput.type = isHidden ? "text" : "password";
    togglePasswordBtn.textContent = isHidden ? "Скрыть" : "Показать";
  });
}

if (checkBtn && passwordInput) {
  checkBtn.addEventListener("click", async () => {
    const value = passwordInput.value || "";
    if (!value) return;

    checkBtn.disabled = true;
    checkBtn.textContent = "Проверяем...";

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ password: value }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const payload = await response.json();
      const analysis = mapBackendResponse(payload);
      renderResult(analysis);
    } catch (error) {
      resultPlaceholder.hidden = true;
      resultContent.hidden = false;
      scoreBadge.textContent = "Ошибка проверки";
      scoreBadge.classList.remove("score-medium", "score-strong");
      leakStatus.textContent =
        "Не удалось получить ответ от бэкенда. Проверьте, что сервер запущен и CORS разрешен.";
      leakStatus.classList.remove("ok");
      leakStatus.classList.add("bad");
      detailsList.innerHTML = "<li>Повторите попытку позже.</li>";
      tipsList.innerHTML = "<li>Проверьте, что бэкенд запущен и принимает POST-запросы.</li>";
      console.error("Password check failed:", error);
    } finally {
      checkBtn.textContent = "Проверить пароль";
      checkBtn.disabled = !passwordInput.value;
    }
  });
}

if (closeResultPopup) {
  closeResultPopup.addEventListener("click", closePopup);
}

if (themeToggleBtn) {
  themeToggleBtn.addEventListener("click", toggleTheme);
}

function renderResult(analysis) {
  openPopup();
  resultPlaceholder.hidden = true;
  resultContent.hidden = false;

  scoreBadge.textContent = analysis.scoreLabel;
  scoreBadge.classList.remove("score-medium", "score-strong");
  if (analysis.level === "medium") {
    scoreBadge.classList.add("score-medium");
  } else if (analysis.level === "strong") {
    scoreBadge.classList.add("score-strong");
  }

  leakStatus.textContent = analysis.leakText;
  leakStatus.classList.remove("bad", "ok");
  leakStatus.classList.add(analysis.leakStatusClass);

  detailsList.innerHTML = "";
  analysis.details.forEach((item) => {
    const li = document.createElement("li");
    li.innerHTML = `<span class="key">${item.label}:</span> <span class="${item.state}">${item.value}</span>`;
    detailsList.appendChild(li);
  });

  tipsList.innerHTML = "";
  analysis.tips.forEach((tip) => {
    const li = document.createElement("li");
    li.textContent = tip;
    tipsList.appendChild(li);
  });
}

function openPopup() {
  if (!resultCard) return;
  resultCard.classList.add("is-open");
  resultCard.setAttribute("aria-hidden", "false");
  document.body.classList.add("popup-open");
}

function closePopup() {
  if (!resultCard) return;
  resultCard.classList.remove("is-open");
  resultCard.setAttribute("aria-hidden", "true");
  document.body.classList.remove("popup-open");
}

function mapBackendResponse(payload) {
  const levelRaw = String(payload?.strength || "weak").toLowerCase();
  const level =
    levelRaw === "strong"
      ? "strong"
      : levelRaw === "medium"
        ? "medium"
        : "weak";

  const scoreLabel =
    level === "strong"
      ? "Сильный пароль"
      : level === "medium"
        ? "Средний пароль"
        : "Слабый пароль";

  const reasons = Array.isArray(payload?.reasons) ? payload.reasons : [];
  const scoreValue = Number(payload?.scores ?? 0);
  const breachReason = reasons.find((r) => r.toLowerCase().includes("утеч"));
  const hasBreach = Boolean(breachReason);
  const leakText =
    hasBreach
      ? "Пароль обнаружен в базе утечек. Не используйте его."
      : "Признаки утечки по результату проверки не обнаружены.";
  const leakStatusClass = hasBreach ? "bad" : "ok";

  const details = [
    {
      label: "Уровень стойкости",
      value: level,
      state: level === "strong" ? "ok" : level === "medium" ? "warn" : "bad",
    },
    {
      label: "Итоговый балл",
      value: String(scoreValue),
      state: scoreValue >= 4 ? "ok" : scoreValue >= 2 ? "warn" : "bad",
    },
  ];

  const tips = reasons.length > 0 ? reasons : ["Явных замечаний нет."];

  return {
    level,
    scoreLabel,
    leakText,
    leakStatusClass,
    details,
    tips,
  };
}

function initTheme() {
  if (isMobileThemeMode()) {
    setTheme(getSystemTheme(), false);
    subscribeToSystemThemeChanges();
    return;
  }

  const savedTheme = localStorage.getItem(THEME_STORAGE_KEY) || "light";
  setTheme(savedTheme);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme") || "light";
  const next = current === "dark" ? "light" : "dark";
  setTheme(next);
}

function getSystemTheme() {
  return systemThemeMedia.matches ? "dark" : "light";
}

function isMobileThemeMode() {
  return window.innerWidth <= 800;
}

function subscribeToSystemThemeChanges() {
  if (systemThemeMedia.addEventListener) {
    systemThemeMedia.addEventListener("change", applySystemThemeForMobile);
  } else {
    systemThemeMedia.addListener(applySystemThemeForMobile);
  }
}

function applySystemThemeForMobile() {
  if (!isMobileThemeMode()) return;
  setTheme(getSystemTheme(), false);
}

function setTheme(theme, persist = true) {
  const normalized = theme === "dark" ? "dark" : "light";
  document.documentElement.setAttribute("data-theme", normalized);

  if (persist) {
    localStorage.setItem(THEME_STORAGE_KEY, normalized);
  }

  if (themeToggleBtn) {
    themeToggleBtn.textContent =
      normalized === "dark" ? "Светлая тема" : "Тёмная тема";
  }
}
