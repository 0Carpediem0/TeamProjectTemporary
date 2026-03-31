const passwordInput = document.getElementById("password");
const togglePasswordBtn = document.getElementById("togglePassword");
const checkBtn = document.getElementById("checkBtn");

const resultPlaceholder = document.getElementById("resultPlaceholder");
const resultContent = document.getElementById("resultContent");
const scoreBadge = document.getElementById("scoreBadge");
const leakStatus = document.getElementById("leakStatus");
const detailsList = document.getElementById("detailsList");
const tipsList = document.getElementById("tipsList");

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
  checkBtn.addEventListener("click", () => {
    const value = passwordInput.value || "";
    if (!value) return;

    const analysis = analyzePassword(value);

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
  });
}

function analyzePassword(password) {
  const length = password.length;
  const hasLower = /[a-zа-яё]/.test(password);
  const hasUpper = /[A-ZА-ЯЁ]/.test(password);
  const hasDigit = /\d/.test(password);
  const hasSymbol = /[^0-9a-zA-Zа-яА-ЯёЁ]/.test(password);

  let score = 0;
  if (length >= 8) score += 1;
  if (length >= 12) score += 1;
  if (hasLower && hasUpper) score += 1;
  if (hasDigit) score += 1;
  if (hasSymbol) score += 1;

  const lowerPassword = password.toLowerCase();
  const badPatterns = ["password", "qwerty", "1234", "admin", "letmein"];
  const hasBadPattern = badPatterns.some((p) => lowerPassword.includes(p));

  if (hasBadPattern) {
    score = Math.max(0, score - 2);
  }

  let level = "weak";
  let scoreLabel = "Слабый пароль";
  if (score >= 4) {
    level = "strong";
    scoreLabel = "Сильный пароль";
  } else if (score === 3) {
    level = "medium";
    scoreLabel = "Средний пароль";
  }

  const mockLeakCount = hasBadPattern ? 5321 : 0;
  const leakText =
    mockLeakCount > 0
      ? `Пароль найден в утечках (${mockLeakCount.toLocaleString("ru-RU")} раз). Не используйте его.`
      : "Пароль не найден в известных базах утечек (демо‑режим).";
  const leakStatusClass = mockLeakCount > 0 ? "bad" : "ok";

  const details = [
    {
      label: "Длина",
      value:
        length >= 12
          ? `${length} символов (отлично)`
          : `${length} символов (рекомендуется ≥ 12)`,
      state: length >= 12 ? "ok" : length >= 8 ? "warn" : "bad",
    },
    {
      label: "Строчные буквы",
      value: hasLower ? "есть" : "нет",
      state: hasLower ? "ok" : "bad",
    },
    {
      label: "Заглавные буквы",
      value: hasUpper ? "есть" : "нет",
      state: hasUpper ? "ok" : "warn",
    },
    {
      label: "Цифры",
      value: hasDigit ? "есть" : "нет",
      state: hasDigit ? "ok" : "warn",
    },
    {
      label: "Специальные символы",
      value: hasSymbol ? "есть" : "нет",
      state: hasSymbol ? "ok" : "warn",
    },
    {
      label: "Шаблоны / популярные пароли",
      value: hasBadPattern ? "обнаружены" : "не обнаружены",
      state: hasBadPattern ? "bad" : "ok",
    },
  ];

  const tips = [];
  if (length < 12) {
    tips.push("Увеличьте длину пароля до 12+ символов.");
  }
  if (!(hasLower && hasUpper)) {
    tips.push("Используйте смесь строчных и заглавных букв.");
  }
  if (!hasDigit) {
    tips.push("Добавьте в пароль цифры.");
  }
  if (!hasSymbol) {
    tips.push("Добавьте спецсимволы, например !@#?$%^&*.");
  }
  if (hasBadPattern) {
    tips.push(
      "Избегайте очевидных слов и последовательностей (password, qwerty, 1234 и т.п.).",
    );
  }
  if (tips.length === 0) {
    tips.push("Пароль выглядит хорошо. Важно не использовать его на разных сервисах.");
  }

  return {
    level,
    scoreLabel,
    leakText,
    leakStatusClass,
    details,
    tips,
  };
}

