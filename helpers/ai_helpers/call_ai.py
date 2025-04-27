# helpers/ai_helpers/call_ai.py

from aiohttp import ClientSession


async def call_ai(hass, prompt: str) -> str:
    """Send a prompt to the Google Generative Language API and return the raw text response."""
    api_key = hass.data.get("context_provider", {}).get("google_api_key")
    if not api_key:
        raise RuntimeError("Missing Google API key for context_provider integration")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    async with ClientSession() as session:
        try:
            async with session.post(
                url,
                json={"contents": [{"parts": [{"text": prompt}]}]},
                headers={"Content-Type": "application/json"},
                timeout=30,
            ) as response:
                if response.status != 200:
                    raise RuntimeError(
                        f"API error {response.status}: {await response.text()}"
                    )

                data = await response.json()
                raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                return raw_text.strip()

        except Exception as e:
            raise RuntimeError(f"Failed to call Google AI: {e}") from e
