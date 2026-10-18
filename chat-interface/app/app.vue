<script setup lang="ts">
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

const messages = ref<ChatMessage[]>([]);
const question = ref("");
const isLoading = ref(false);

const messagesContainer = ref<HTMLElement | null>(null);

async function scrollToBottom() {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
}

async function sendQuestion() {
  const trimmed = question.value.trim();

  if (!trimmed || isLoading.value) {
    return;
  }

  messages.value.push({ role: "user", content: trimmed });
  question.value = "";
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
    // La route /api/ask retransmet le detail renvoye par FastAPI
    // (ex. question vide, service pas encore pret) dans
    // error.data.data.detail -- on l'affiche si disponible, sinon un
    // message generique.
    const detail = error?.data?.data?.detail ?? error?.data?.detail;

    messages.value.push({
      role: "assistant",
      content:
        detail ??
        "Une erreur est survenue en contactant l'assistant. Vérifie que le rag-service est bien lancé.",
      isError: true,
    });
  } finally {
    isLoading.value = false;
    scrollToBottom();
  }
}
</script>

<template>
  <div class="page">
    <header class="header">
      <h1>Assistant documentaire</h1>
      <p class="subtitle">Recherche sur la documentation Confluence</p>
    </header>

    <main class="messages" ref="messagesContainer">
      <p v-if="messages.length === 0" class="empty-state">
        Pose une question sur la documentation pour commencer.
      </p>

      <div
        v-for="(message, index) in messages"
        :key="index"
        class="message-row"
        :class="message.role"
      >
        <div class="bubble" :class="{ error: message.isError }">
          <p class="content">{{ message.content }}</p>

          <div v-if="message.citations && message.citations.length" class="citations">
            <span class="citations-label">Citations :</span>
            <ul>
              <li v-for="citation in message.citations" :key="citation.number">
                <span class="citation-number">[{{ citation.number }}]</span>
                <span class="citation-source">{{ citation.source }}</span>
                <span class="citation-excerpt">{{ citation.excerpt }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <div v-if="isLoading" class="message-row assistant">
        <div class="bubble loading">
          <span class="dot" />
          <span class="dot" />
          <span class="dot" />
        </div>
      </div>
    </main>

    <form class="input-bar" @submit.prevent="sendQuestion">
      <input
        v-model="question"
        type="text"
        placeholder="Écris ta question ici..."
        :disabled="isLoading"
        autofocus
      />
      <button type="submit" :disabled="isLoading || !question.trim()">
        Envoyer
      </button>
    </form>
  </div>
</template>

<style scoped>
* {
  box-sizing: border-box;
}

.page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 760px;
  margin: 0 auto;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
  background: #f7f7f5;
}

.header {
  padding: 20px 24px 12px;
  border-bottom: 1px solid #e4e2dd;
  background: #fff;
}

.header h1 {
  margin: 0;
  font-size: 1.3rem;
  color: #1f1e1c;
}

.subtitle {
  margin: 4px 0 0;
  font-size: 0.85rem;
  color: #7a776f;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.empty-state {
  margin: auto;
  color: #9c988e;
  font-size: 0.95rem;
  text-align: center;
}

.message-row {
  display: flex;
}

.message-row.user {
  justify-content: flex-end;
}

.message-row.assistant {
  justify-content: flex-start;
}

.bubble {
  max-width: 78%;
  padding: 10px 14px;
  border-radius: 12px;
  line-height: 1.45;
  font-size: 0.95rem;
}

.message-row.user .bubble {
  background: #0f6e56;
  color: #fff;
  border-bottom-right-radius: 4px;
}

.message-row.assistant .bubble {
  background: #fff;
  color: #2c2c2a;
  border: 1px solid #e4e2dd;
  border-bottom-left-radius: 4px;
}

.bubble.error {
  border-color: #d98c8c;
  background: #fdf3f3;
  color: #8a2f2f;
}

.content {
  margin: 0;
  white-space: pre-wrap;
}

.citations {
  margin-top: 10px;
  padding-top: 8px;
  border-top: 1px solid #ececea;
  font-size: 0.8rem;
  color: #6b6862;
}

.citations-label {
  font-weight: 600;
}

.citations ul {
  margin: 6px 0 0;
  padding-left: 0;
  list-style: none;
}

.citations li {
  margin-bottom: 6px;
  line-height: 1.4;
}

.citation-number {
  font-weight: 600;
  color: #0f6e56;
  margin-right: 4px;
}

.citation-source {
  font-weight: 600;
  margin-right: 6px;
}

.citation-excerpt {
  color: #8a877d;
  font-style: italic;
}

.bubble.loading {
  display: flex;
  gap: 4px;
  align-items: center;
  padding: 14px;
}

.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #b4b2a9;
  animation: bounce 1.2s infinite ease-in-out;
}

.dot:nth-child(2) {
  animation-delay: 0.15s;
}

.dot:nth-child(3) {
  animation-delay: 0.3s;
}

@keyframes bounce {
  0%,
  80%,
  100% {
    transform: translateY(0);
    opacity: 0.5;
  }
  40% {
    transform: translateY(-4px);
    opacity: 1;
  }
}

.input-bar {
  display: flex;
  gap: 10px;
  padding: 16px 20px;
  border-top: 1px solid #e4e2dd;
  background: #fff;
}

.input-bar input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid #d8d5cd;
  border-radius: 8px;
  font-size: 0.95rem;
  outline: none;
}

.input-bar input:focus {
  border-color: #0f6e56;
}

.input-bar button {
  padding: 10px 20px;
  background: #0f6e56;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
}

.input-bar button:disabled {
  background: #b4b2a9;
  cursor: not-allowed;
}
</style>