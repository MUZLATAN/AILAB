
from collections import defaultdict
from typing import Dict, List

from fastapi import APIRouter
from fastapi import Query, WebSocket, Body
from starlette.websockets import WebSocketDisconnect

from .utils import request, stream_request

router = APIRouter(prefix="/openai")


@router.websocket("/chat")
async def websocket_chat(websocket: WebSocket):
    try:
        await websocket.accept()
        message = list()
        while True:
            data = await websocket.receive_text()
            print(data)
            message.append({"role": "user", "content": data})
            if data == "quit":
                await websocket.close()
                break
            url = "https://api.openai.com/v1/chat/completions"
            params = {
                "stream": True,
                "messages": message,
                "temperature": 0.8,
                "max_tokens": 1000,
                "model": "gpt-3.5-turbo",
                "n": 1
            }
            result = defaultdict(str)
            async for line in stream_request(url, params):
                role = line.get("role")
                content = line.get("content")
                if role:
                    result["role"] = role
                if content:
                    await websocket.send_text(content)
                    result["content"] += content
            message.append(dict(result))
    except WebSocketDisconnect:
        return


@router.post("/chat")
async def chat(message: List[Dict[str, str]] = Body(...)):
    url = "https://api.openai.com/v1/chat/completions"
    params = {
        "stream": False,
        "messages": message,
        "temperature": 0.8,
        "max_tokens": 2048,
        "model": "gpt-3.5-turbo",
        "n": 1
    }
    return (await request(url, params)).get("choices")[0]


@router.get("/translate")
async def translate(inp: str = Query(...), lang: str = Query("en")):
    """翻译"""
    url = "https://api.openai.com/v1/completions"
    data = {
        "stream": False,
        "prompt": "translate '" + inp + "' to " + lang,
        "temperature": 0.9,
        "max_tokens": 3000,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "model": "text-davinci-002"
    }
    return (await request(url, data)).get("choices")[0]
