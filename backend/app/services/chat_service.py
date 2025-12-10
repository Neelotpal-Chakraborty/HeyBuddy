from app.core.config import settings
import asyncio

try:
    from openai import OpenAI, AsyncOpenAI
except Exception as e:
    raise ImportError(
        "The openai client is required for ChatService but could not be imported: "
        f"{e}. Install `openai` in the running environment."
    )

SYSTEM_PROMPT = (
    "You are HeyBuddy, a supportive AI mental health companion. "
    "Your job is to help users relieve stress, provide empathetic conversation, and uplift their mood. "
    "If the user seems sad, anxious, or in distress, respond with extra care and encouragement. "
    "If you detect signs of crisis or urgent need for mental support, set the alert flag. "
    "You can also suggest reading a joke or taking a break if the user seems down. "
    "Always be positive, non-judgmental, and supportive. "
    "Never give medical advice, but encourage seeking professional help if needed."
)


def _build_messages(message: str, history: list[dict]) -> list[dict]:
    """Build OpenAI-compatible messages list from history and current message."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for h in history:
        messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})
    messages.append({"role": "user", "content": message})
    return messages


class ChatService:
    @staticmethod
    async def chat(message: str, history: list[dict]):
        """Stream OpenAI API responses and yield text chunks."""
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is not set; cannot call OpenAI API")

        alert_keywords = [
            "suicide",
            "kill myself",
            "end my life",
            "can't go on",
            "hopeless",
            "crisis",
            "urgent help",
        ]

        user_text = message.lower()
        messages = _build_messages(message, history)
        model = getattr(settings, "OPENAI_MODEL", "gpt-3.5-turbo")

        def _call_sync_stream():
            """Call OpenAI with streaming enabled."""
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            stream = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                stream=True
            )
            return stream

        # Run the streaming call in a thread
        stream = await asyncio.to_thread(_call_sync_stream)

        # Yield chunks from the stream
        full_response = ""
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_response += content
                yield content

        # Detect alert based on full response or user message
        alert = any(word in user_text for word in alert_keywords)
        # Yield final alert status as JSON
        yield f'|ALERT|{str(alert).lower()}|'

