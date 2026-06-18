const passwordInput = document.getElementById("password");
const togglePasswordBtn = document.getElementById("togglePassword");
const checkBtn = document.getElementById("checkBtn");
const themeToggleBtn = document.getElementById("themeToggle");

const resultPlaceholder = document.getElementById("resultPlaceholder");
const resultContent = document.getElementById("resultContent");
const scoreBadge = document.getElementById("scoreBadge");
const leakStatus = document.getElementById("leakStatus");
const detailsList = document.getElementById("detailsList");
const tipsList = document.getElementById("tipsList");
const strengthMeterFill = document.getElementById("strengthMeterFill");
const strengthPercent = document.getElementById("strengthPercent");
const strengthMeterText = document.getElementById("strengthMeterText");

const API_URL = "/api/check";
const THEME_STORAGE_KEY = "password-checker-theme";
const DEFAULT_PLACEHOLDER =
  "Введите пароль и нажмите «Проверить пароль», чтобы увидеть результат.";
const systemThemeMedia = window.matchMedia("(prefers-color-scheme: dark)");

let latestCheckId = 0;
let wasStrengthFull = false;

initTheme();
resetResult();
updateStrengthMeter("");

if (passwordInput) {
  passwordInput.addEventListener("input", () => {
    const value = passwordInput.value || "";
    checkBtn.disabled = !value;
    latestCheckId += 1;
    updateStrengthMeter(value);
    renderLivePreview(value);
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

    await checkPassword(value);
  });
}

if (themeToggleBtn) {
  themeToggleBtn.addEventListener("click", toggleTheme);
}

async function checkPassword(value) {
  const checkId = latestCheckId + 1;
  latestCheckId = checkId;

  setLoadingState();
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

    if (checkId !== latestCheckId) return;

    const payload = await response.json();
    renderResult(mapBackendResponse(payload));
  } catch (error) {
    if (checkId !== latestCheckId) return;
    renderError(error);
  } finally {
    if (checkId === latestCheckId) {
      checkBtn.textContent = "Проверить пароль";
      checkBtn.disabled = !passwordInput.value;
    }
  }
}

function resetResult() {
  resultPlaceholder.textContent = DEFAULT_PLACEHOLDER;
  resultPlaceholder.hidden = false;
  resultContent.hidden = true;
}

function setLoadingState() {
  resultPlaceholder.textContent = "Проверяем пароль...";
  resultPlaceholder.hidden = false;
  resultContent.hidden = true;
}

function renderResult(analysis) {
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

function renderError(error) {
  resultPlaceholder.hidden = true;
  resultContent.hidden = false;
  scoreBadge.textContent = "Ошибка проверки";
  scoreBadge.classList.remove("score-medium", "score-strong");
  leakStatus.textContent =
    "Не удалось получить ответ от бэкенда. Проверьте, что сервер запущен.";
  leakStatus.classList.remove("ok");
  leakStatus.classList.add("bad");
  detailsList.innerHTML = "<li>Повторите попытку позже.</li>";
  tipsList.innerHTML =
    "<li>Проверьте, что бэкенд запущен и принимает POST-запросы.</li>";
  console.error("Password check failed:", error);
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
  const hasBreach = reasons.some((reason) =>
    reason.toLowerCase().includes("утеч")
  );
  const leakText = hasBreach
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

  return {
    level,
    scoreLabel,
    leakText,
    leakStatusClass,
    details,
    tips: reasons.length > 0 ? reasons : ["Явных замечаний нет."],
  };
}

function updateStrengthMeter(password) {
  const strength = estimatePasswordStrength(password);

  if (strengthMeterFill) {
    strengthMeterFill.style.width = `${strength.percent}%`;
    strengthMeterFill.dataset.level = strength.level;
  }

  if (strengthPercent) {
    strengthPercent.textContent = `${strength.percent}%`;
  }

  if (strengthMeterText) {
    strengthMeterText.textContent = strength.text;
  }

  if (strength.percent === 100 && !wasStrengthFull) {
    launchConfetti();
  }

  wasStrengthFull = strength.percent === 100;
}

function estimatePasswordStrength(password) {
  if (!password) {
    return {
      percent: 0,
      level: "empty",
      text: "Начните вводить пароль",
      tips: ["Введите пароль, чтобы увидеть предварительную оценку."],
    };
  }

  const checks = [
    {
      passed: password.length >= 8,
      tip: "Сделайте пароль минимум 8 символов.",
    },
    {
      passed: password.length >= 12,
      tip: "Для высокой стойкости лучше использовать 12+ символов.",
    },
    {
      passed: /[a-zа-яё]/.test(password),
      tip: "Добавьте строчные буквы.",
    },
    {
      passed: /[A-ZА-ЯЁ]/.test(password),
      tip: "Добавьте заглавные буквы.",
    },
    {
      passed: /\d/.test(password),
      tip: "Добавьте цифры.",
    },
    {
      passed: /[^A-Za-zА-Яа-яЁё0-9]/.test(password),
      tip: "Добавьте специальный символ.",
    },
  ];
  const passedChecks = checks.filter((check) => check.passed).length;
  const percent = Math.min(100, Math.round((passedChecks / checks.length) * 100));
  const tips = checks
    .filter((check) => !check.passed)
    .map((check) => check.tip)
    .slice(0, 3);

  if (percent >= 100) {
    return {
      percent,
      level: "strong",
      text: "Отлично, пароль выглядит мощно",
      tips: ["Предварительно пароль выглядит сильным."],
    };
  }

  if (percent >= 67) {
    return {
      percent,
      level: "medium",
      text: "Уже неплохо, можно усилить ещё",
      tips,
    };
  }

  if (percent >= 34) {
    return {
      percent,
      level: "weak",
      text: "Пароль пока средний по составу",
      tips,
    };
  }

  return {
    percent,
    level: "weak",
    text: "Добавьте длину, цифры и спецсимволы",
    tips,
  };
}

function renderLivePreview(password) {
  if (!password) {
    resetResult();
    return;
  }

  const strength = estimatePasswordStrength(password);
  const scoreLabel =
    strength.level === "strong"
      ? "Сильный пароль"
      : strength.level === "medium"
        ? "Средний пароль"
        : "Слабый пароль";

  renderResult({
    level: strength.level,
    scoreLabel,
    leakText: "Проверка по базе утечек выполнится после нажатия кнопки.",
    leakStatusClass: "ok",
    details: [
      {
        label: "Предварительная надёжность",
        value: `${strength.percent}%`,
        state:
          strength.level === "strong"
            ? "ok"
            : strength.level === "medium"
              ? "warn"
              : "bad",
      },
      {
        label: "Статус проверки",
        value: "ожидает запуска",
        state: "warn",
      },
    ],
    tips: strength.tips,
  });
}

function launchConfetti() {
  const layer = document.createElement("div");
  layer.className = "confetti-layer";
  document.body.appendChild(layer);

  const colors = ["#2d8cff", "#d4a373", "#2f8d4b", "#fff5d6", "#c44557"];
  const piecesCount = 42;

  for (let i = 0; i < piecesCount; i += 1) {
    const piece = document.createElement("span");
    piece.className = "confetti-piece";
    piece.style.left = `${Math.random() * 100}%`;
    piece.style.background = colors[i % colors.length];
    piece.style.animationDelay = `${Math.random() * 0.18}s`;
    piece.style.setProperty("--shift", `${Math.random() * 220 - 110}px`);
    piece.style.setProperty("--spin", `${Math.random() * 540 + 180}deg`);
    layer.appendChild(piece);
  }

  setTimeout(() => {
    layer.remove();
  }, 1400);
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
