// Route serveur Nuxt (pattern BFF, "Backend For Frontend").
//
// Le navigateur appelle POST /api/ask sur le serveur Nuxt (meme
// origine que la page, donc pas de CORS). Ce code s'execute cote
// serveur, dans le conteneur chat-interface, et relaie la question au
// rag-service par le reseau interne Docker. Le rag-service n'a donc
// plus besoin d'etre expose au navigateur.

interface Citation {
  number: number;
  source: string;
  excerpt: string;
}

interface AskResponse {
  answer: string;
  citations: Citation[];
}

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event);
  const body = await readBody<{ question?: string }>(event);

  try {
    return await $fetch<AskResponse>(`${config.ragApiUrl}/ask`, {
      method: "POST",
      body: { question: body?.question },
    });
  } catch (error: any) {
    // On retransmet le code et le detail renvoyes par FastAPI
    // (ex. 400 question vide, 422 champ manquant). Si le rag-service
    // est injoignable, il n'y a pas de reponse : 502 Bad Gateway.
    const statusCode = error?.response?.status ?? 502;
    const detail =
      error?.data?.detail ??
      "Le service de réponse (rag-service) est injoignable.";

    throw createError({
      statusCode,
      statusMessage: "Erreur du rag-service",
      data: { detail },
    });
  }
});
