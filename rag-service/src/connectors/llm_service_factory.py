"""Choix du connecteur LLM via LLM_SERVICE (imports differes)."""

import os


def build_llm_service():

    name = os.getenv("LLM_SERVICE", "ollama").strip().lower()

    if name == "ollama":
        from connectors.llm_service import LLMService
        return LLMService()

    if name == "azure_openai":
        from connectors.llm_service_azure_openai import LLMServiceAzureOpenAI
        return LLMServiceAzureOpenAI(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini"),
        )

    raise SystemExit(f"LLM_SERVICE='{name}' invalide (attendu : 'ollama' ou 'azure_openai').")
