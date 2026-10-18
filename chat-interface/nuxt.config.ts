export default defineNuxtConfig({
  compatibilityDate: "2026-01-01",
  devtools: { enabled: true },

  app: {
    head: {
      title: "Assistant documentaire",
      htmlAttrs: { lang: "fr" },
      link: [
        { rel: "preconnect", href: "https://fonts.googleapis.com" },
        { rel: "preconnect", href: "https://fonts.gstatic.com", crossorigin: "" },
        {
          rel: "stylesheet",
          href: "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap",
        },
      ],
    },
  },

  runtimeConfig: {
    // Adresse INTERNE du rag-service, utilisee uniquement par le
    // serveur Nuxt (route server/api/ask.post.ts), jamais par le
    // navigateur. Dans Docker : NUXT_RAG_API_URL=http://rag-service:8000
    ragApiUrl: "http://127.0.0.1:8000",
  },
});
