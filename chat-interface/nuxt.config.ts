export default defineNuxtConfig({
  compatibilityDate: "2026-01-01",
  devtools: { enabled: true },

  runtimeConfig: {
    // Adresse INTERNE du rag-service, utilisee uniquement par le
    // serveur Nuxt (route server/api/ask.post.ts), jamais par le
    // navigateur : elle n'est pas dans "public", donc elle n'est pas
    // envoyee au client.
    // Valeur par defaut : developpement local (les deux serveurs sur
    // la meme machine). Dans Docker, surchargee par la variable
    // d'environnement NUXT_RAG_API_URL=http://rag-service:8000
    // (nom du service sur le reseau interne Docker).
    ragApiUrl: "http://127.0.0.1:8000",
  },
});
