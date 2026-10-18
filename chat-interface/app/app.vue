<script setup lang="ts">
import MarkdownIt from "markdown-it";

interface Citation {
  number: number;
  source: string;
  excerpt: string;
}

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  citations?: Citation[];
  isError?: boolean;
}

// Le LLM repond en Markdown. html: false = tout HTML present dans la
// reponse est echappe, pas interprete (pas d'injection via v-html).
const markdown = new MarkdownIt({ html: false, linkify: true, breaks: true });

// Les marqueurs [n] deviennent des pastilles liees a la source n.
// Seuls des chiffres sont captures : aucun contenu externe n'est injecte.
function renderAnswer(text: string): string {
  return markdown
    .render(text)
    .replace(
      /\[(\d+)\]/g,
      '<button type="button" class="marker" data-n="$1" aria-label="Voir la source $1">$1</button>'
    );
}

// Retire l'extension .md pour afficher un nom de page lisible.
function pageName(source: string): string {
  return source.replace(/\.md$/i, "");
}

const examples = [
  "Qu'est-ce qu'un Pod dans Kubernetes ?",
  "Quelle est la différence entre Prometheus et Grafana ?",
  "Comment un pipeline CI/CD peut-il exécuter Terraform ?",
  "Quelles sont les bonnes pratiques de sécurité ?",
];

const messages = ref<ChatMessage[]>([]);
const question = ref("");
const isLoading = ref(false);
const activeSource = ref<string | null>(null); // "indexMessage-numero"

// Theme clair / sombre. Par defaut : reglage du systeme. Le choix
// de l'utilisateur est memorise dans le navigateur (localStorage).
type Theme = "light" | "dark";
const theme = ref<Theme>("light");

function applyTheme(value: Theme) {
  theme.value = value;
  document.documentElement.dataset.theme = value;
}

function toggleTheme() {
  const next: Theme = theme.value === "dark" ? "light" : "dark";
  applyTheme(next);
  try {
    localStorage.setItem("theme", next);
  } catch {
    // stockage indisponible (navigation privee...) : le choix n'est
    // simplement pas memorise
  }
}

onMounted(() => {
  let saved: string | null = null;
  try {
    saved = localStorage.getItem("theme");
  } catch {
    saved = null;
  }
  if (saved === "light" || saved === "dark") {
    applyTheme(saved);
  } else {
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    applyTheme(prefersDark ? "dark" : "light");
  }
});

const messagesContainer = ref<HTMLElement | null>(null);
const inputRef = ref<HTMLTextAreaElement | null>(null);

async function scrollToBottom() {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
}

function autoResize() {
  const el = inputRef.value;
  if (!el) return;
  el.style.height = "auto";
  el.style.height = `${Math.min(el.scrollHeight, 160)}px`;
}

function onKeydown(event: KeyboardEvent) {
  // Entree = envoyer ; Maj + Entree = nouvelle ligne
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendQuestion();
  }
}

function askExample(text: string) {
  question.value = text;
  sendQuestion();
}

// Survol / clic d'une pastille dans le texte : met en evidence la source.
function onAnswerPointer(event: Event, index: number) {
  const target = (event.target as HTMLElement).closest(".marker") as HTMLElement | null;
  activeSource.value = target ? `${index}-${target.dataset.n}` : null;
}

function onAnswerClick(event: Event, index: number) {
  const target = (event.target as HTMLElement).closest(".marker") as HTMLElement | null;
  if (!target) return;
  activeSource.value = `${index}-${target.dataset.n}`;
  document
    .getElementById(`source-${index}-${target.dataset.n}`)
    ?.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

async function sendQuestion() {
  const trimmed = question.value.trim();

  if (!trimmed || isLoading.value) {
    return;
  }

  messages.value.push({ role: "user", content: trimmed });
  question.value = "";
  await nextTick();
  autoResize();
  isLoading.value = true;
  scrollToBottom();

  try {
    // Appel a la route serveur Nuxt (meme origine que la page) :
    // c'est elle qui relaie la question au rag-service en interne.
    const response = await $fetch<{ answer: string; citations: Citation[] }>(
      "/api/ask",
      {
        method: "POST",
        body: { question: trimmed },
      }
    );

    messages.value.push({
      role: "assistant",
      content: response.answer,
      citations: response.citations,
    });
  } catch (error: any) {
    const detail = error?.data?.data?.detail ?? error?.data?.detail;

    messages.value.push({
      role: "assistant",
      content:
        detail ??
        "Le service de réponse est injoignable. Vérifiez que le rag-service est lancé, puis réessayez.",
      isError: true,
    });
  } finally {
    isLoading.value = false;
    scrollToBottom();
    inputRef.value?.focus();
  }
}
</script>

<template>
  <div class="app">
    <header class="topbar">
      <div class="brand">
        <span class="brand-mark" aria-hidden="true">
          <svg viewBox="0 0 24 24" width="18" height="18">
            <path d="M5 4h9l5 5v11H5z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" />
            <path d="M8 13h8M8 16.5h5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
          </svg>
        </span>
        <div>
          <h1>Assistant documentaire</h1>
          <p class="scope">Répond à partir des espaces Confluence Infra et DevOps, en citant ses sources.</p>
        </div>
        <button
          type="button"
          class="theme-toggle"
          :aria-label="theme === 'dark' ? 'Passer en mode clair' : 'Passer en mode sombre'"
          :title="theme === 'dark' ? 'Mode clair' : 'Mode sombre'"
          @click="toggleTheme"
        >
          <!-- Soleil (affiche en mode sombre) -->
          <svg v-if="theme === 'dark'" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
            <circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.8" />
            <path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M5.3 18.7l1.6-1.6M17.1 6.9l1.6-1.6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
          </svg>
          <!-- Lune (affichee en mode clair) -->
          <svg v-else viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
            <path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" />
          </svg>
        </button>
      </div>
    </header>

    <main class="thread" ref="messagesContainer" aria-live="polite">
      <div class="thread-inner">
        <section v-if="messages.length === 0" class="welcome">
          <h2>Posez une question sur la documentation technique.</h2>
          <p>
            Chaque réponse s'appuie uniquement sur les pages Confluence et indique d'où vient
            chaque information. Si la documentation ne couvre pas le sujet, l'assistant le dit.
          </p>
          <ul class="examples">
            <li v-for="example in examples" :key="example">
              <button type="button" @click="askExample(example)">{{ example }}</button>
            </li>
          </ul>
        </section>

        <template v-for="(message, index) in messages" :key="index">
          <div v-if="message.role === 'user'" class="question">
            <p>{{ message.content }}</p>
          </div>

          <article v-else-if="message.isError" class="answer answer-error">
            <p>{{ message.content }}</p>
          </article>

          <article v-else class="answer">
            <div
              class="answer-body"
              v-html="renderAnswer(message.content)"
              @mouseover="onAnswerPointer($event, index)"
              @mouseleave="activeSource = null"
              @focusin="onAnswerPointer($event, index)"
              @click="onAnswerClick($event, index)"
            />

            <section v-if="message.citations && message.citations.length" class="sources">
              <h3>Sources</h3>
              <ol>
                <li
                  v-for="citation in message.citations"
                  :id="`source-${index}-${citation.number}`"
                  :key="citation.number"
                  class="source"
                  :class="{ active: activeSource === `${index}-${citation.number}` }"
                  @mouseenter="activeSource = `${index}-${citation.number}`"
                  @mouseleave="activeSource = null"
                >
                  <span class="marker marker-static" aria-hidden="true">{{ citation.number }}</span>
                  <div>
                    <p class="source-name">{{ pageName(citation.source) }}</p>
                    <p class="source-excerpt">{{ citation.excerpt }}</p>
                  </div>
                </li>
              </ol>
            </section>
          </article>
        </template>

        <div v-if="isLoading" class="answer answer-loading" role="status">
          <span class="pulse" aria-hidden="true" />
          Recherche dans la documentation…
        </div>
      </div>
    </main>

    <footer class="composer">
      <form class="composer-inner" @submit.prevent="sendQuestion">
        <label for="question" class="visually-hidden">Votre question</label>
        <textarea
          id="question"
          ref="inputRef"
          v-model="question"
          rows="1"
          placeholder="Posez votre question…"
          :disabled="isLoading"
          autofocus
          @input="autoResize"
          @keydown="onKeydown"
        />
        <button type="submit" class="send" :disabled="isLoading || !question.trim()">
          Envoyer
        </button>
      </form>
      <p class="hint">Entrée pour envoyer, Maj + Entrée pour aller à la ligne.</p>
    </footer>
  </div>
</template>

<style>
/* Styles globaux : palette (clair par defaut, sombre via data-theme),
   polices et fond de page. */
:root {
  --bg: #edf1f6;
  --surface: #ffffff;
  --text: #17233a;
  --text-soft: #4a5872;
  --text-faint: #8591a7;
  --line: #d9e0ea;
  --signal: #1f5fd1;
  --signal-hover: #1a51b3;
  --focus-ring: rgba(31, 95, 209, 0.15);
  --mark: #ffe58a;
  --mark-strong: #f5c21b;
  --mark-ink: #17233a;
  --mark-wash: #fff8dc;
  --bar-bg: #17233a;
  --bar-text: #ffffff;
  --bar-text-soft: #b8c3d6;
  --bubble-bg: #17233a;
  --bubble-text: #ffffff;
  --code-bg: #edf1f6;
  --pre-bg: #17233a;
  --pre-text: #e6ecf5;
  --danger: #b4232f;
  --danger-bg: #fdf0f1;
  --danger-line: #f0c4c8;
  --disabled: #b9c3d3;
  --font-sans: "IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, Consolas, monospace;
  color-scheme: light;
}

:root[data-theme="dark"] {
  --bg: #0f1726;
  --surface: #172235;
  --text: #e6ecf5;
  --text-soft: #a9b5ca;
  --text-faint: #76839b;
  --line: #2a3850;
  --signal: #6f9bff;
  --signal-hover: #8cb0ff;
  --focus-ring: rgba(111, 155, 255, 0.25);
  --mark: #e8c54a;
  --mark-strong: #ffd95e;
  --mark-ink: #17233a;
  --mark-wash: rgba(232, 197, 74, 0.14);
  --bar-bg: #0b1220;
  --bar-text: #e6ecf5;
  --bar-text-soft: #8b98b0;
  --bubble-bg: #2a3a57;
  --bubble-text: #f2f5fa;
  --code-bg: #22304a;
  --pre-bg: #0b1220;
  --pre-text: #dbe3f0;
  --danger: #ff9aa2;
  --danger-bg: #3a1d24;
  --danger-line: #5a2a33;
  --disabled: #3a4760;
  color-scheme: dark;
}

html,
body {
  margin: 0;
  height: 100%;
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-sans);
  -webkit-font-smoothing: antialiased;
}
</style>

<style scoped>
* {
  box-sizing: border-box;
}

.app {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
  white-space: nowrap;
}

/* ---------- En-tete ---------- */
.topbar {
  background: var(--bar-bg);
  color: var(--bar-text);
  padding: 14px 24px;
}

.brand {
  max-width: 880px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 14px;
}

.theme-toggle {
  margin-left: auto;
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 9px;
  background: transparent;
  color: var(--bar-text);
  cursor: pointer;
  flex-shrink: 0;
}

.theme-toggle:hover {
  background: rgba(255, 255, 255, 0.08);
}

.brand-mark {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  border-radius: 9px;
  background: var(--mark);
  color: var(--mark-ink);
  flex-shrink: 0;
}

.brand h1 {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 600;
  letter-spacing: 0.005em;
}

.scope {
  margin: 2px 0 0;
  font-size: 0.85rem;
  color: var(--bar-text-soft);
}

/* ---------- Fil de discussion ---------- */
.thread {
  flex: 1;
  overflow-y: auto;
}

.thread-inner {
  max-width: 880px;
  margin: 0 auto;
  padding: 32px 24px 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Accueil */
.welcome {
  padding: 40px 0 8px;
  max-width: 640px;
}

.welcome h2 {
  margin: 0 0 12px;
  font-size: 1.75rem;
  line-height: 1.25;
  font-weight: 600;
  letter-spacing: -0.01em;
}

.welcome p {
  margin: 0 0 28px;
  font-size: 1rem;
  line-height: 1.6;
  color: var(--text-soft);
}

.examples {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 10px;
}

.examples button {
  width: 100%;
  text-align: left;
  padding: 14px 16px;
  border: 1px solid var(--line);
  border-radius: 10px;
  background: var(--surface);
  color: var(--text);
  font: inherit;
  font-size: 0.93rem;
  line-height: 1.45;
  cursor: pointer;
}

.examples button:hover {
  border-color: var(--signal);
  color: var(--signal);
}

/* Question */
.question {
  align-self: flex-end;
  max-width: 75%;
  background: var(--bubble-bg);
  color: var(--bubble-text);
  padding: 12px 16px;
  border-radius: 14px 14px 4px 14px;
}

.question p {
  margin: 0;
  line-height: 1.5;
  white-space: pre-wrap;
}

/* Reponse : un bloc de lecture, pas une bulle */
.answer {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 22px 26px;
}

.answer-body {
  font-size: 1rem;
  line-height: 1.65;
  max-width: 68ch;
}

.answer-body :deep(p) {
  margin: 0 0 12px;
}

.answer-body :deep(p:last-child) {
  margin-bottom: 0;
}

.answer-body :deep(ul),
.answer-body :deep(ol) {
  margin: 6px 0 14px;
  padding-left: 22px;
}

.answer-body :deep(li) {
  margin-bottom: 4px;
}

.answer-body :deep(li > ul) {
  margin: 6px 0 10px;
}

.answer-body :deep(strong) {
  font-weight: 600;
}

.answer-body :deep(h1),
.answer-body :deep(h2),
.answer-body :deep(h3) {
  font-size: 1.05rem;
  font-weight: 600;
  margin: 18px 0 8px;
}

.answer-body :deep(code) {
  font-family: var(--font-mono);
  font-size: 0.88em;
  background: var(--code-bg);
  padding: 1px 5px;
  border-radius: 4px;
}

.answer-body :deep(pre) {
  background: var(--pre-bg);
  color: var(--pre-text);
  padding: 14px 16px;
  border-radius: 8px;
  overflow-x: auto;
  line-height: 1.5;
}

.answer-body :deep(pre code) {
  background: none;
  padding: 0;
  color: inherit;
}

/* Pastilles de citation : l'element signature de l'interface */
.answer :deep(.marker) {
  display: inline-grid;
  place-items: center;
  min-width: 1.35em;
  height: 1.35em;
  padding: 0 0.3em;
  margin: 0 1px;
  border: 0;
  border-radius: 4px;
  background: var(--mark);
  color: var(--mark-ink);
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 500;
  line-height: 1;
  vertical-align: 0.15em;
  cursor: pointer;
}

.answer :deep(button.marker:hover),
.answer :deep(button.marker:focus-visible) {
  background: var(--mark-strong);
}

/* Sources */
.sources {
  margin-top: 22px;
  padding-top: 16px;
  border-top: 1px solid var(--line);
}

.sources h3 {
  margin: 0 0 10px;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-soft);
}

.sources ol {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.source {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  padding: 8px 10px;
  margin: 0 -10px;
  border-radius: 8px;
  transition: background-color 120ms ease;
}

.source.active {
  background: var(--mark-wash);
}

.source .marker-static {
  margin-top: 2px;
  cursor: default;
}

.source-name {
  margin: 0;
  font-size: 0.9rem;
  font-weight: 600;
}

.source-excerpt {
  margin: 2px 0 0;
  font-size: 0.85rem;
  line-height: 1.5;
  color: var(--text-soft);
}

/* Etats */
.answer-error {
  background: var(--danger-bg);
  border-color: var(--danger-line);
  color: var(--danger);
}

.answer-error p {
  margin: 0;
}

.answer-loading {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--text-soft);
  font-size: 0.95rem;
}

.pulse {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--mark-strong);
  animation: pulse 1.1s ease-in-out infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 0.35;
    transform: scale(0.85);
  }
  50% {
    opacity: 1;
    transform: scale(1);
  }
}

/* ---------- Zone de saisie ---------- */
.composer {
  background: var(--surface);
  border-top: 1px solid var(--line);
  padding: 14px 24px 10px;
}

.composer-inner {
  max-width: 880px;
  margin: 0 auto;
  display: flex;
  gap: 10px;
  align-items: flex-end;
}

.composer textarea {
  flex: 1;
  resize: none;
  padding: 12px 14px;
  border: 1px solid var(--line);
  border-radius: 10px;
  background: var(--bg);
  color: var(--text);
  font: inherit;
  font-size: 1rem;
  line-height: 1.5;
  max-height: 160px;
}

.composer textarea:focus {
  outline: none;
  border-color: var(--signal);
  box-shadow: 0 0 0 3px var(--focus-ring);
}

.send {
  padding: 12px 22px;
  border: 0;
  border-radius: 10px;
  background: var(--signal);
  color: #fff;
  font: inherit;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
}

:global(:root[data-theme="dark"]) .send {
  color: #0b1220;
}

.send:hover:not(:disabled) {
  background: var(--signal-hover);
}

.send:disabled {
  background: var(--disabled);
  cursor: not-allowed;
}

.hint {
  max-width: 880px;
  margin: 6px auto 0;
  font-size: 0.78rem;
  color: var(--text-faint);
}

/* Focus clavier visible partout */
button:focus-visible,
textarea:focus-visible {
  outline: 2px solid var(--signal);
  outline-offset: 2px;
}

/* ---------- Mobile ---------- */
@media (max-width: 640px) {
  .topbar,
  .composer {
    padding-left: 16px;
    padding-right: 16px;
  }

  .thread-inner {
    padding: 20px 16px;
  }

  .scope,
  .hint {
    display: none;
  }

  .welcome h2 {
    font-size: 1.4rem;
  }

  .question {
    max-width: 90%;
  }

  .answer {
    padding: 18px 18px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .pulse {
    animation: none;
  }

  .source {
    transition: none;
  }
}
</style>
