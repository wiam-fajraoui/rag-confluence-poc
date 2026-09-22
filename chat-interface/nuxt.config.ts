export default defineNuxtConfig({
  compatibilityDate: "2026-01-01",
  devtools: { enabled: true },

  runtimeConfig: {
    public: {
      // Adresse de l'API FastAPI. Valeur par defaut adaptee au
      // developpement local (les deux serveurs tournent sur la
      // meme machine). Peut etre surchargee sans toucher au code,
      // via la variable d'environnement NUXT_PUBLIC_API_BASE
      // (meme principe que DATA_SOURCE/VECTOR_STORE/LLM_SERVICE
      // cote backend).
      apiBase: "http://127.0.0.1:8000",
    },
  },
});