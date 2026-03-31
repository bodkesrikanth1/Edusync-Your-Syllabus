/* =========================================================
   Edusync - app.js (Full)
   Includes:
   1) Animated Counters (Landing + Dashboard)
   2) Unit Accordion Toggle (Results page)
   3) Topic Search Filter (Results page)
   4) Login Show/Hide Password
   5) Register Show/Hide Password + Confirm Match Validation
========================================================= */


/* ---------- 1) Reusable Counter Animation ---------- */
function animateCounter(id, target, suffix = "", speed = 18) {
  const el = document.getElementById(id);
  if (!el) return;

  let current = 0;
  const step = Math.max(1, Math.floor(target / 45));

  const timer = setInterval(() => {
    current += step;
    if (current >= target) {
      current = target;
      clearInterval(timer);
    }
    el.textContent = current + suffix;
  }, speed);
}


/* ---------- 2) Results Page: Unit Toggle Accordion ---------- */
function toggleUnit(btn, forceOpen = false) {
  const card = btn.closest(".unit-card");
  if (!card) return;

  const body = card.querySelector(".unit-body");
  const expanded = btn.getAttribute("aria-expanded") === "true";

  const shouldOpen = forceOpen ? true : !expanded;

  btn.setAttribute("aria-expanded", shouldOpen ? "true" : "false");
  card.classList.toggle("unit-open", shouldOpen);

  if (body) {
    body.hidden = !shouldOpen;
  }
}


/* ---------- 3) DOM Loaded Actions ---------- */
window.addEventListener("DOMContentLoaded", () => {

  /* Landing Page Stats */
  animateCounter("landingStat1", 250);
  animateCounter("landingStat2", 120);
  animateCounter("landingStat3", 70, "%");

  /* Dashboard Hero Stats (base.html hero-strip) */
  animateCounter("statTopics", 120);
  animateCounter("statUnits", 6);
  animateCounter("statSpeed", 2, "s");

  /* Results Page: Auto expand first unit */
  const firstUnit = document.querySelector(".unit-card .unit-toggle");
  if (firstUnit) toggleUnit(firstUnit, true);

  /* Results Page: Topic Search Filter */
  const topicSearch = document.getElementById("topicSearch");
  if (topicSearch) {
    topicSearch.addEventListener("input", () => {
      const q = topicSearch.value.trim().toLowerCase();
      document.querySelectorAll(".topic-block").forEach(block => {
        const topic = (block.getAttribute("data-topic") || "").toLowerCase();
        block.style.display = topic.includes(q) ? "block" : "none";
      });
    });
  }

  /* Login Page: Show / Hide Password */
  const togglePassword = document.getElementById("togglePassword");
  const loginPassword = document.getElementById("password");

  if (togglePassword && loginPassword) {
    togglePassword.addEventListener("click", () => {
      const hidden = loginPassword.type === "password";
      loginPassword.type = hidden ? "text" : "password";
      togglePassword.textContent = hidden ? "🙈" : "👁";
    });
  }

  /* Register Page: Show / Hide Password */
  const regPassword = document.getElementById("regPassword");
  const regConfirm = document.getElementById("regConfirm");

  const toggleRegPassword = document.getElementById("toggleRegPassword");
  const toggleRegConfirm = document.getElementById("toggleRegConfirm");

  function toggleVisibility(btn, input) {
    if (!btn || !input) return;
    btn.addEventListener("click", () => {
      const hidden = input.type === "password";
      input.type = hidden ? "text" : "password";
      btn.textContent = hidden ? "🙈" : "👁";
    });
  }

  toggleVisibility(toggleRegPassword, regPassword);
  toggleVisibility(toggleRegConfirm, regConfirm);

  /* Register Page: Password Match Validation */
  const matchHint = document.getElementById("matchHint");
  const createBtn = document.getElementById("createBtn");

  function validateMatch() {
    if (!regPassword || !regConfirm || !matchHint || !createBtn) return;

    if (regConfirm.value.length === 0) {
      matchHint.textContent = "";
      matchHint.className = "help-text";
      createBtn.disabled = false;
      return;
    }

    if (regPassword.value === regConfirm.value) {
      matchHint.textContent = "✅ Passwords match";
      matchHint.className = "help-text match-ok";
      createBtn.disabled = false;
    } else {
      matchHint.textContent = "❌ Passwords do not match";
      matchHint.className = "help-text match-bad";
      createBtn.disabled = true;
    }
  }

  if (regPassword && regConfirm) {
    regPassword.addEventListener("input", validateMatch);
    regConfirm.addEventListener("input", validateMatch);
  }

});
