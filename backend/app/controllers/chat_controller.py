from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.core.security import validate_access_token
from app.services.chat_service import ChatService
import json

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []  # [{"role": "user"|"assistant", "content": "..."}]

@router.post("/chat")
async def chat_with_llm(request: ChatRequest, user=Depends(validate_access_token)):
    if not request.message:
        raise HTTPException(status_code=400, detail="Message is required.")
    
    async def stream_generator():
        """Stream response chunks from ChatService and format as JSON lines."""
        try:
            response_text = ""
            alert = False
            
            async for chunk in ChatService.chat(request.message, request.history):
                # Check if this is the alert marker
                if chunk.startswith("|ALERT|"):
                    alert_str = chunk.split("|")[2]
                    alert = alert_str == "true"
                    continue
                
                response_text += chunk
                # Yield each chunk as a JSON line for the frontend
                yield json.dumps({"text": chunk, "done": False}) + "\n"
            
            # Send final response with alert flag
            yield json.dumps({"text": "", "done": True, "alert": alert}) + "\n"
        except Exception as e:
            yield json.dumps({"error": str(e)}) + "\n"
    
    return StreamingResponse(stream_generator(), media_type="application/x-ndjson")

