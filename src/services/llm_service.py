import ollama


class LLMService:

    def generate_answer(self, prompt: str) -> str:

        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0,
                "seed": 42
            }
        )

        return response["message"]["content"]